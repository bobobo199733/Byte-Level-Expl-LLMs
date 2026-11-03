"""RQ1 regression and smoke tests; no repository artifacts are overwritten."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

RQ1_DIR = Path(__file__).resolve().parents[1] / "rq1"
sys.path.insert(0, str(RQ1_DIR))
import run_nested_cv as rq1


class NestedTaskCVTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.train = self.root / "train.csv"
        self.test = self.root / "test.csv"

        # Balanced three-class examples for 8 distinct tasks.
        rows = []
        for task in range(1, 9):
            for cls_id, model in enumerate(rq1.CLASSES):
                rows.append({
                    "model": model,
                    "file_name": f"t{task}_p1_r1_{model}.py",
                    "byte_0": 149,
                    "byte_1": 0,
                    "byte_2": 90 + cls_id,
                    "byte_3": task % 4,
                })
        frame = pd.DataFrame(rows)
        frame[frame["file_name"].str.extract(r"t(\d+)", expand=False).astype(int) <= 5].to_csv(
            self.train, index=False
        )
        frame[frame["file_name"].str.extract(r"t(\d+)", expand=False).astype(int) > 5].to_csv(
            self.test, index=False
        )

    def test_load_and_task_partition(self):
        frame, names = rq1.load_dataset(self.train, self.test)
        self.assertEqual(len(frame), 24)
        self.assertEqual(names, ["byte_0", "byte_1", "byte_2", "byte_3"])
        self.assertEqual(frame["_task"].nunique(), 8)
        self.assertEqual(set(frame["_historical_split"]), {"train", "test"})

    def test_group_split_and_leak_detection(self):
        frame, _ = rq1.load_dataset(self.train, self.test)
        groups = frame["_task"].to_numpy()
        train = np.flatnonzero(groups != "t8")
        heldout = np.flatnonzero(groups == "t8")
        rq1.assert_partition(train, heldout, groups)
        with self.assertRaises(AssertionError):
            rq1.assert_partition(train, np.array([train[0]]), groups)

    def test_opcode_histogram_is_normalized(self):
        frame, names = rq1.load_dataset(self.train, self.test)
        reps = rq1.build_representations(
            frame, names, self.root, ["positional", "opcode_hist"]
        )
        self.assertEqual(reps["positional"].shape, (24, 4))
        self.assertEqual(reps["opcode_hist"].shape, (24, 256))
        np.testing.assert_allclose(reps["opcode_hist"].sum(axis=1), 1.0)

    def test_ast_baseline_reads_source_and_records_digests(self):
        frame, cols = rq1.load_dataset(self.train, self.test)
        for filename, model, split in frame[
            ["file_name", "model", "_historical_split"]
        ].itertuples(index=False, name=None):
            folder = "outputs" if split == "train" else "test_data/outputs"
            path = self.root / folder / model / "cleaned" / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("def example(x):\n    return x + 1\n", encoding="utf-8")
        representations = rq1.build_representations(
            frame, cols, self.root, ["ast"]
        )
        ast_df = representations["ast"]
        self.assertEqual(len(ast_df), len(frame))
        self.assertEqual(len(ast_df.attrs["source_inventory"]), len(frame))
        self.assertEqual(ast_df.iloc[0]["ast_FunctionDef"], 1)

    def test_duplicate_filename_rejected(self):
        rows = pd.read_csv(self.test)
        train = pd.read_csv(self.train)
        rows.loc[0, "file_name"] = train.iloc[0]["file_name"]
        rows.to_csv(self.test, index=False)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            rq1.load_dataset(self.train, self.test)

    def test_bootstrap_task_ci(self):
        block = pd.DataFrame({
            "task": ["t1", "t1", "t2", "t2", "t3", "t3"],
            "truth": ["llama", "mistral"] * 3,
            "prediction": ["llama", "llama", "llama", "mistral", "mistral", "mistral"],
        })
        result = rq1.bootstrap_by_task(block, draws=20, seed=42)
        self.assertIn("macro_f1", result)
        self.assertGreaterEqual(result["accuracy"]["upper_95"], result["accuracy"]["lower_95"])

    def test_paired_bootstrap_self_difference_is_zero(self):
        frame = pd.DataFrame({
            "row_id": [0, 1, 2, 3],
            "task": ["t1", "t1", "t2", "t2"],
            "truth": ["llama", "mistral", "llama", "mistral"],
            "prediction": ["llama", "llama", "mistral", "mistral"],
        })
        diff = rq1.paired_task_bootstrap(frame, frame, draws=20, seed=42)
        for result in diff.values():
            self.assertEqual(result["observed_difference"], 0.0)
            self.assertEqual(result["lower_95"], 0.0)
            self.assertEqual(result["upper_95"], 0.0)

    def test_nested_cv_writes_oof_predictions_only(self):
        out = self.root / "results"
        args = SimpleNamespace(
            train_csv=self.train, test_csv=self.test,
            research_root=self.root, output_dir=out,
            representations=["positional", "opcode_hist"],
            models=["logistic"], outer_folds=2, inner_folds=2,
            bootstrap_draws=20, seed=42, jobs=1,
        )
        rq1.run_experiment(args)
        selected = pd.read_csv(out / "selected_oof_predictions.csv")
        all_predictions = pd.read_csv(out / "candidate_oof_predictions.csv")
        self.assertEqual(len(selected), 24)
        self.assertEqual(len(selected["row_id"].unique()), 24)
        self.assertTrue((out / "manifest.json").exists())
        self.assertTrue((out / "fold_scores.csv").exists())
        self.assertTrue((out / "task_scores.csv").exists())
        self.assertTrue((out / "results.json").exists())
        self.assertTrue((out / "paired_comparisons.json").exists())
        self.assertTrue({"positional", "opcode_hist", "control"}.issubset(
            set(all_predictions["representation"])
        ))
        with self.assertRaises(FileExistsError):
            rq1.run_experiment(args)


if __name__ == "__main__":
    unittest.main()
