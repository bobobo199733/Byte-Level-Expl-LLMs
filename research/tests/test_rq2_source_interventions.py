"""Tests for controlled source interventions and sandbox safeguards."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "rq2"
sys.path.insert(0, str(ROOT))
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


if __name__ == "__main__":
    unittest.main()
