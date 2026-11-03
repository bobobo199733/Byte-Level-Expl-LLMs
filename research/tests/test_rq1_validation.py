"""Regression tests for RQ1 confound/complete-bytecode validation."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "rq1"))
sys.path.insert(0, str(ROOT / "scripts"))

from bytecode_utils import extract_script_bytecode, pad_or_truncate
import run_validation as validate


class RQ1ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_docstring_removal_and_no_length(self):
        documented = (
            '"""module description"""\n'
            'def solve(x):\n'
            '    """explanation that is not executable"""\n'
            '    return x + 1\n'
        )
        plain = "def solve(x):\n    return x + 1\n"
        a = validate.ast_vectors(documented)
        b = validate.ast_vectors(plain)
        self.assertEqual(a["ast_core_count"], b["ast_core_count"])
        self.assertEqual(a["ast_core_prop"], b["ast_core_prop"])
        self.assertNotEqual(a["length_only"], b["length_only"])
        self.assertNotIn("ast_source_lines", a["ast_core_count"])
        self.assertNotIn("ast_total_nodes", a["ast_core_count"])

    def test_complete_opcode_histogram_includes_late_instructions(self):
        values = [149, 0] * 161 + [100, 2] * 4
        features = validate.opcode_features(values, ngram_buckets=16)
        full = features["opcode_full"]
        self.assertAlmostEqual(full["op_149"], 161 / 165)
        self.assertAlmostEqual(full["op_100"], 4 / 165)
        self.assertAlmostEqual(sum(full.values()), 1)
        self.assertEqual(len(features["opcode_ngram"]), 16)

    def test_correctness_coverage_missing_is_unknown(self):
        df = pd.DataFrame([
            {"file_name": "t1_p1_r1_llama.py", "model": "llama", "_task": "t1"},
            {"file_name": "t1_p1_r1_qwen.py", "model": "qwen", "_task": "t1"},
        ])
        folder = self.root / "scores"
        folder.mkdir()
        pd.DataFrame([{
            "file": "t1_p1_r1_llama.py", "model": "llama",
            "score": 1.0, "passed": 2, "total": 2, "status": "ok"
        }]).to_csv(folder / "scores_llama.csv", index=False)
        merged, report = validate.correctness_coverage(df, folder)
        self.assertEqual(report["rows_with_known_correctness"], 1)
        self.assertEqual(report["rows_unknown"], 1)
        self.assertEqual(merged.iloc[0]["correctness_label"], "all_pass")
        self.assertEqual(merged.iloc[1]["correctness_label"], "unknown")

    def test_stratified_splits_task_disjoint(self):
        from sklearn.model_selection import StratifiedGroupKFold
        groups = np.repeat(np.arange(10), 3)
        labels = np.tile(np.arange(3), 10)
        for tr, te in StratifiedGroupKFold(
            n_splits=5, shuffle=True, random_state=42
        ).split(np.zeros(len(labels)), labels, groups):
            validate.assert_partition(tr, te, groups)

    @unittest.skipUnless(sys.version_info[:2] == (3, 13), "Exact historical opcode agreement requires Python 3.13")
    def test_end_to_end_prepare_only_verifies_untruncated_bytes(self):
        rows = []
        for task_number in range(1, 9):
            split = "train" if task_number <= 5 else "test"
            task = f"t{task_number}"
            metadata = self.root / ("prompts" if split == "train" else "test_data/prompts") / task / "meta.json"
            metadata.parent.mkdir(parents=True, exist_ok=True)
            metadata.write_text(json.dumps({"function_name": "solve"}))
            for j, model in enumerate(validate.CLASSES):
                filename = f"{task}_p1_r1_{model}.py"
                file = validate.source_path(self.root, filename, model, split)
                file.parent.mkdir(parents=True, exist_ok=True)
                source = (
                    'def solve(x):\n'
                    + ('    """generated docstring"""\n' if j == 0 else '')
                    + f'    return x + {j}\n'
                )
                file.write_text(source)
                sequence, _ = extract_script_bytecode(file, "solve")
                fixed, _ = pad_or_truncate(sequence, 320)
                row = {"model": model, "file_name": filename}
                row.update({f"byte_{i}": value for i, value in enumerate(fixed)})
                rows.append((split, row))
        train_path = self.root / "train.csv"
        test_path = self.root / "test.csv"
        for split, path in (("train", train_path), ("test", test_path)):
            pd.DataFrame([row for section, row in rows if section == split]).to_csv(path, index=False)
        args = SimpleNamespace(
            train_csv=train_path, test_csv=test_path,
            research_root=self.root, scores_dir=self.root / "scores",
            output_dir=self.root / "validation",
            variants=["ast_original", "ast_core_prop", "opcode_full", "opcode_ngram"],
            seeds=[7], outer_folds=2, inner_folds=2,
            bootstrap_draws=10, ngram_buckets=16,
            jobs=1, prepare_only=True,
        )
        validate.main(args)
        audit = pd.read_csv(args.output_dir / "source_audit.csv")
        self.assertEqual(len(audit), 24)
        self.assertTrue(audit["first_320_exact_match"].all())
        self.assertTrue((args.output_dir / "correctness_summary.json").exists())
        self.assertEqual(audit["full_opcode_count"].min() > 0, True)
        with self.assertRaises(FileExistsError):
            validate.main(args)


if __name__ == "__main__":
    unittest.main()
