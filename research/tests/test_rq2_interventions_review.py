"""Tests for controlled source interventions and independent-review workflow."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] / "rq2"
sys.path.insert(0, str(ROOT))
import explanation_assessment
import run_source_interventions as intervention


class SourceInterventionTests(unittest.TestCase):
    def test_docstring_is_preserved_by_both_transforms(self):
        original = 'def solve(x):\n    """Keep this docstring."""\n    return x + 1\n'
        for kind in ("insert_pass", "wrap_try_finally"):
            edited = intervention.mutate(original, "solve", kind)
            self.assertIn('Keep this docstring.', edited)
            self.assertNotEqual(edited, original)
            self.assertIn("return x + 1", edited)

    def test_missing_target_fails(self):
        with self.assertRaises(ValueError):
            intervention.mutate("def f(x): return x", "absent", "insert_pass")

    def test_opcode_hist_normalization(self):
        values = [100, 0, 100, 0, 91, 2]
        vec = intervention.normalized_opcode_hist(values)
        self.assertAlmostEqual(vec.sum(), 1)
        self.assertAlmostEqual(vec[100], 2 / 3)
        self.assertAlmostEqual(vec[91], 1 / 3)

    def test_missing_sandbox_image_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = Path(tmp) / "missing.sif"
            with self.assertRaises(FileNotFoundError):
                intervention.isolated_test(result, "x", "y", {"function_name": "f"}, timeout=3)


class HumanReviewTests(unittest.TestCase):
    def test_two_blind_sheets_and_review_agreement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            examples = []
            for cls in ("llama", "mistral", "qwen"):
                for task in (1, 2):
                    examples.append({
                        "seed": 42, "fold": 1,
                        "explained_class": cls,
                        "true_model": cls if task == 1 else "qwen",
                        "prediction": cls if task == 1 else "mistral",
                        "file_name": f"t{task}_p1_r1_{cls}.py",
                        "opcode": 91 if task == 1 else 53,
                        "opname": "LOAD_GLOBAL" if task == 1 else "CALL",
                        "heldout_logit_shap": 0.8,
                        "sample_source_lines": [
                            {"function": "solve", "normalized_line": 2,
                             "normalized_source": "return f(x)"}
                        ],
                    })
            path = root / "source.json"
            pd.DataFrame(examples).to_json(path, orient="records")
            explanation_assessment.prepare(path, root / "review", max_cases=6)
            key = pd.read_csv(root / "review/private_case_key.csv")
            self.assertEqual(len(key), 6)
            a = pd.read_csv(root / "review/reviewer_A.csv", keep_default_na=False)
            b = pd.read_csv(root / "review/reviewer_B.csv", keep_default_na=False)
            self.assertNotIn("true_model", a.columns)
            with self.assertRaises(ValueError):
                explanation_assessment.adjudicate(root / "review", root / "out")
            for letter, data in (("A", a), ("B", b)):
                data["interpretation_label"] = "syntactic_structure"
                data["interpretation_reason"] = "Visible conditional structural pattern"
                data["confidence_1_to_5"] = "3"
                data.to_csv(root / f"review/reviewer_{letter}.csv", index=False)
            explanation_assessment.adjudicate(root / "review", root / "out")
            report = json.loads((root / "out/review_agreement.json").read_text())
            self.assertEqual(report["exact_agreement"], 1.0)
            self.assertEqual(report["n_disagreements_pending_adjudication"], 0)
            self.assertEqual(len(pd.read_csv(root / "out/adjudication_queue.csv")), 6)


if __name__ == "__main__":
    unittest.main()
