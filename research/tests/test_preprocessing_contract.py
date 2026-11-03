"""Tests for the classifier input schema (metadata must not become predictors)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import preprocess_features


class PreprocessingContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "features").mkdir()
        self.input_path = self.base / "features" / "function_bytecode_features.csv"
        self.valid_row = {
            "model": "mistral",
            "file_name": "t1_p1_r1_mistral.py",
            "task": "t1",
            "function_name": "solution",
            "bytecode_extract_status": "ok",
            "python_version": "3.11.8",
            "representation_kind": "opcode_argument_pairs_v1",
            "original_byte_length": 2,
            "was_truncated": False,
            "byte_0": 100,
            "byte_1": 0,
        }

    def run_preprocessing(self):
        with patch.object(preprocess_features, "BASE_DIR", self.base), patch.object(
            sys, "argv", ["preprocess_features.py", "0"]
        ):
            preprocess_features.main()

    def test_metadata_is_not_a_classifier_feature(self):
        pd.DataFrame([self.valid_row]).to_csv(self.input_path, index=False)
        self.run_preprocessing()
        output = pd.read_csv(self.base / "features" / "processed_bytecode_features.csv")
        self.assertEqual(output.columns.tolist(), ["model", "file_name", "byte_0", "byte_1"])
        config = json.loads(
            (self.base / "features" / "processed_bytecode_config.json").read_text()
        )
        self.assertEqual(config["num_features"], 2)
        self.assertEqual(config["feature_columns"], ["byte_0", "byte_1"])
        self.assertEqual(config["representation_length"], 2)

    def test_unexpected_columns_fail_closed(self):
        row = dict(self.valid_row, unexpected_feature="accidental")
        pd.DataFrame([row]).to_csv(self.input_path, index=False)
        with self.assertRaisesRegex(ValueError, "Unexpected classifier input"):
            self.run_preprocessing()


if __name__ == "__main__":
    unittest.main()
