"""Regression tests for the positional opcode/decoded-argument representation.

Run from the repository root:
    python -m unittest discover -s research/tests -v
"""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from bytecode_utils import (
    REPRESENTATION_KIND,
    build_bytecode_row_from_file,
    extract_script_bytecode,
    instruction_trace_from_file,
    preprocess_single_file,
)


SOURCE = """def target(values):
    total = 0
    for value in values:
        total += value
    def nested(x):
        return x + total
    return nested(1)

def helper():
    return 5
"""


class BytecodeRepresentationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source_path = Path(self.tmp.name) / "sample.py"
        self.source_path.write_text(SOURCE, encoding="utf-8")

    def test_canonical_trace_agrees_with_extracted_feature_values(self):
        values, _ = extract_script_bytecode(self.source_path, "target")
        trace = instruction_trace_from_file(self.source_path, "target")
        flattened = [v for r in trace for v in (r["opcode"], r["arg_raw"])]
        self.assertEqual(values, flattened)
        self.assertEqual([r["byte_pos"] for r in trace], list(range(0, len(values), 2)))
        self.assertEqual([r["arg_pos"] for r in trace], list(range(1, len(values), 2)))
        self.assertTrue(all(r["source_line_origin"] == "normalized_source" for r in trace))
        self.assertIn("helper", {r["co_name"] for r in trace})
        self.assertIn("nested", {r["co_name"] for r in trace})

    def test_extracted_rows_include_provenance_and_padding(self):
        row = build_bytecode_row_from_file(self.source_path, 320, "target")
        self.assertEqual(row["representation_kind"], REPRESENTATION_KIND)
        self.assertIn("python_version", row)
        self.assertEqual(len([k for k in row if k.startswith("byte_")]), 320)
        self.assertIsInstance(row["was_truncated"], bool)

    def test_sparse_selected_features_require_explicit_original_length(self):
        selected = ["byte_0", "byte_16"]
        with self.assertRaisesRegex(ValueError, "Sparse feature selection"):
            preprocess_single_file(self.source_path, selected, "target")
        df = preprocess_single_file(
            self.source_path, selected, "target", representation_length=320
        )
        row = build_bytecode_row_from_file(self.source_path, 320, "target")
        self.assertEqual(df.iloc[0]["byte_0"], row["byte_0"])
        self.assertEqual(df.iloc[0]["byte_16"], row["byte_16"])

    def test_contiguous_full_feature_schema_works(self):
        names = [f"byte_{i}" for i in range(320)]
        frame = preprocess_single_file(self.source_path, names, "target")
        self.assertEqual(frame.columns.tolist(), names)
        self.assertEqual(frame.shape, (1, 320))

    def test_missing_features_are_never_silently_zero_filled(self):
        with self.assertRaisesRegex(ValueError, "Missing requested features"):
            preprocess_single_file(
                self.source_path, ["byte_0", "unknown_feature"],
                "target", representation_length=320
            )

    def test_representation_does_not_depend_on_source_comments(self):
        other = Path(self.tmp.name) / "other.py"
        other.write_text("# leading comment\n" + SOURCE, encoding="utf-8")
        first, _ = extract_script_bytecode(self.source_path, "target")
        second, _ = extract_script_bytecode(other, "target")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
