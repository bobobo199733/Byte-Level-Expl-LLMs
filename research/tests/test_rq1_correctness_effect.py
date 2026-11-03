"""Correctness-stratified RQ1 diagnostics (no generated program execution)."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rq1"))
import rq1_correctness_analysis as rq1_correct


class RQ1CorrectnessTests(unittest.TestCase):
    def setUp(self):
        self.inventory = pd.DataFrame([
            {"row_id": i, "task": f"t{i // 3}", "model": ("llama", "mistral", "qwen")[i % 3],
             "file_name": f"t{i // 3}_p1_r1_{('llama','mistral','qwen')[i%3]}.py",
             "status": ("pass", "fail", "untestable")[i % 3]}
            for i in range(1316)
        ])
        # A duplicate file-name is not allowed even when row_id is unique.
        self.inventory["file_name"] = [f"t{i // 3}_p1_r{1+i//1310}_{('llama','mistral','qwen')[i%3]}.py"
                                       for i in range(1316)]

    def test_inventory_contract(self):
        valid = rq1_correct.validate_inventory(self.inventory)
        self.assertEqual(len(valid), 1316)
        with self.assertRaises(ValueError):
            rq1_correct.validate_inventory(self.inventory.iloc[:-1])
        duplicated = self.inventory.copy()
        duplicated.loc[1, "file_name"] = duplicated.loc[0, "file_name"]
        with self.assertRaises(ValueError):
            rq1_correct.validate_inventory(duplicated)

    def test_merge_fails_on_misaligned_task_or_origin(self):
        inventory = rq1_correct.validate_inventory(self.inventory)
        frame = pd.DataFrame([{
            "seed": 42, "row_id": 0, "task": "tWRONG",
            "file_name": self.inventory.iloc[0]["file_name"],
            "truth": "llama", "prediction": "qwen", "variant": "opcode_full",
        }])
        with self.assertRaises(ValueError):
            rq1_correct.merge_oof(frame, inventory, source="test",
                                  truth="truth", predicted="prediction",
                                  variant="variant", seed="seed")

    def test_paired_accuracy_difference_and_task_resampling(self):
        rows = []
        for task in ("t1", "t2", "t3"):
            for i in (0, 1, 2):
                for variant, pred in (("opcode_full", "llama"),
                                      ("length_only", "qwen")):
                    rows.append({
                        "row_id": 3 * int(task[1:]) + i,
                        "task": task, "status": "pass", "variant": variant,
                        "truth": "llama", "prediction": pred,
                    })
        df = pd.DataFrame(rows)
        result = rq1_correct.paired_bootstrap(df, "opcode_full",
                       "length_only", draws=100, seed=42)
        self.assertEqual(result["accuracy_difference_a_minus_b"], 1.0)
        self.assertEqual(result["task_bootstrap_95_ci"], [1.0, 1.0])
        self.assertEqual(result["n_tasks"], 3)
        bad = df.drop(df.index[0])
        with self.assertRaises(ValueError):
            rq1_correct.paired_bootstrap(bad, "opcode_full",
                                         "length_only", draws=100, seed=42)

    def test_empty_group_not_promoted_to_correct(self):
        self.assertEqual(rq1_correct.metrics(pd.DataFrame()), {"n": 0, "n_tasks": 0})


if __name__ == "__main__":
    unittest.main()
