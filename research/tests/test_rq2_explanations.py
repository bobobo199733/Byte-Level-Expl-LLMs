"""RQ2 tests: exact logit decomposition, leakage safeguards and source traces."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "rq2"))
sys.path.insert(0, str(ROOT / "scripts"))
import run_explanations as rq2
from bytecode_utils import extract_script_bytecode, pad_or_truncate


class AttributionTests(unittest.TestCase):
    def test_shap_logit_additivity_and_intervention(self):
        X = np.array([
            [1., 0., 2.], [2., 1., 1.], [3., 0., 0.],
            [0., 2., 1.], [1., 3., 1.], [3., 2., 0.],
            [2., 2., 2.], [0., 1., 3.], [1., 0., 0.],
        ])
        y = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000)),
        ]).fit(X, y)
        attr, base = rq2.linear_logit_shap(pipe, X, X.mean(axis=0))
        self.assertEqual(attr.shape, (9, 3, 3))
        result = rq2.attribution_diagnostics(pipe, X, X.mean(axis=0), attr, base)
        self.assertLess(result["max_logit_additivity_error"], 1e-9)
        self.assertLess(result["max_feature_replacement_error"], 1e-9)

    def test_frequency_baseline_and_stable_ranking(self):
        X = np.array([[1., 0.], [2., 0.], [0., 1.], [0., 2.]])
        labels = np.array([0, 0, 1, 1])
        contrast = rq2.frequency_baseline(X, labels, 0)
        np.testing.assert_array_equal(contrast, [1.5, -1.5])
        np.testing.assert_array_equal(
            rq2.select_top_indices(np.array([1., 1., 2.]), 3), [2, 0, 1]
        )
        self.assertAlmostEqual(rq2.jaccard({1, 2}, {2, 3}), 1 / 3)

    def test_rank_stability(self):
        features = pd.DataFrame([
            {"class": "llama", "seed": 7, "fold": 1, "rank": 1, "opcode": 100, "opname": "LOAD_CONST"},
            {"class": "llama", "seed": 7, "fold": 1, "rank": 2, "opcode": 149, "opname": "RESUME"},
            {"class": "llama", "seed": 42, "fold": 1, "rank": 1, "opcode": 100, "opname": "LOAD_CONST"},
            {"class": "llama", "seed": 42, "fold": 1, "rank": 2, "opcode": 90, "opname": "STORE_NAME"},
        ])
        stable = rq2.stability_table(features, 2)
        self.assertEqual(len(stable), 1)
        self.assertAlmostEqual(stable.iloc[0]["mean_pairwise_topk_jaccard"], 1 / 3)

    @unittest.skipUnless(sys.version_info[:2] == (3, 13), "Historical bytecode values require 3.13")
    def test_prepare_only_with_archived_feature_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            records = []
            for task_number in range(1, 9):
                task = f"t{task_number}"
                split = "train" if task_number <= 5 else "test"
                meta = root / ("prompts" if split == "train" else "test_data/prompts") / task / "meta.json"
                meta.parent.mkdir(parents=True, exist_ok=True)
                meta.write_text(json.dumps({"function_name": "solve"}))
                for cls, model in enumerate(rq2.CLASSES):
                    filename = f"{task}_p1_r1_{model}.py"
                    source = rq2.source_path(root, filename, model, split)
                    source.parent.mkdir(parents=True, exist_ok=True)
                    source.write_text(f"def solve(x):\\n    return x + {cls}\\n".replace("\\n", "\n"))
                    values, _ = extract_script_bytecode(source, "solve")
                    saved, _ = pad_or_truncate(values, 320)
                    record = {"model": model, "file_name": filename}
                    record.update({f"byte_{pos}": v for pos, v in enumerate(saved)})
                    records.append((split, record))
            for split, target in (("train", "train.csv"), ("test", "test.csv")):
                pd.DataFrame([row for section, row in records if section == split]).to_csv(root / target, index=False)
            args = SimpleNamespace(
                train_csv=root / "train.csv", test_csv=root / "test.csv",
                research_root=root, output_dir=root / "results",
                seeds=[7], outer_folds=2, inner_folds=2,
                top_k=3, max_examples=1, jobs=1, prepare_only=True,
            )
            rq2.main(args)
            self.assertTrue((args.output_dir / "manifest.json").exists())
            self.assertEqual(len(pd.read_csv(args.output_dir / "source_audit.csv")), 24)
            with self.assertRaises(FileExistsError):
                rq2.main(args)


if __name__ == "__main__":
    unittest.main()
