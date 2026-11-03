"""Synthetic regression tests for reviewer diagnostics and inventory."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

RQ2 = Path(__file__).resolve().parents[1] / "rq2"
sys.path.insert(0, str(RQ2))
import audit_generation_inventory as inventory
import reviewer_diagnostics as diagnostic


class ReviewerArtifactTests(unittest.TestCase):
    def test_inventory_has_complete_design_and_unknown_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for model in inventory.MODELS:
                file = root / "outputs" / model / "cleaned" / f"t1_p1_r1_{model}.py"
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("def f(x): return x")
            for location in ("features", "test_data/features"):
                (root / location).mkdir(parents=True)
            rows = [{"file_name": f"t1_p1_r1_{model}.py"} for model in inventory.MODELS]
            pd.DataFrame(rows).to_csv(root / "features/processed_bytecode_features.csv", index=False)
            pd.DataFrame({"file_name": []}).to_csv(root / "test_data/features/processed_bytecode_features.csv", index=False)
            result = inventory.run(root, root / "audit")
            self.assertEqual(result["expected_design_cells_not_verified_api_attempts"], 1350)
            self.assertEqual(result["retained_in_features"], 3)
            self.assertEqual(result["not_archived"], 1347)
            with self.assertRaises(FileExistsError):
                inventory.run(root, root / "audit")

    def test_task_bootstrap_and_recurrence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "input"
            input_dir.mkdir()
            cases = []
            for seed in (7, 42):
                for task in range(1, 11):
                    for cls in diagnostic.CLASSES:
                        cases.append({
                            "seed": seed, "row_id": (task - 1) * 3 + diagnostic.CLASSES.index(cls),
                            "task": f"t{task}", "file_name": f"t{task}_p1_r1_{cls}.py",
                            "true_model": cls, "predicted_model": cls,
                        })
            pd.DataFrame(cases).to_csv(input_dir / "oof_predictions.csv", index=False)
            pd.DataFrame([
                {"class": "llama", "opcode": 85, "seed": 7, "fold": 1,
                 "train_mean_abs_logit_shap": 0.5, "test_positive_fraction": 0.7}
            ]).to_csv(input_dir / "feature_attributions.csv", index=False)
            pd.DataFrame([{
                "explained_class": "llama", "opcode": 85, "opname": "LOAD_FAST",
                "true_model": "qwen", "prediction": "qwen",
                "heldout_logit_shap": 0.2, "file_name": "t2_p1_r1_qwen.py",
            }]).to_json(input_dir / "source_evidence.json", orient="records")
            diagnostic.run(input_dir, root / "out", draws=100, seed=42)
            result = json.loads((root / "out/review_diagnostics.json").read_text())
            self.assertEqual(result["n_seeds"], 2)
            self.assertEqual(result["n_unique_programs"], 30)
            self.assertEqual(result["by_seed"]["7"]["point"]["accuracy"], 1.0)
            coverage = pd.read_csv(root / "out/curated_source_evidence_audit.csv")
            self.assertEqual(coverage.iloc[0]["counterexample_examples_from_other_models"], 1)
            with self.assertRaises(FileExistsError):
                diagnostic.run(input_dir, root / "out", draws=100, seed=42)


if __name__ == "__main__":
    unittest.main()
