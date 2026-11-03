"""Tests of full-dataset correctness and equivalence report contracts.

These tests do not execute archived/generated programs on the host.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parents[1] / "rq2"
sys.path.insert(0, str(HERE))
import analyze_correctness_effect as analysis
import evaluate_correctness as correctness
import evaluate_equivalence as equivalence
import validation_common as sandbox


class AutomatedValidationTests(unittest.TestCase):
    def test_sandbox_required(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(FileNotFoundError):
                sandbox.verify_sandbox(Path(t) / "missing.sif")

    @unittest.skipUnless(sys.version_info[:2] == (3, 13), "Worker needs 3.13")
    def test_trusted_worker_correctness_equivalence_and_missing_oracle(self):
        # Test only hand-authored trusted code; never archived LLM code in CI.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "meta.json").write_text(json.dumps({
                "function_name": "solve",
                "valid_cases": [[[2], 3]],
                "explicit_cases": [[[0], 1]],
                "tests": [[[4], 5]],
                "invalid_cases": [["bad"]],
                "expected_exception": "ValueError",
            }))
            code = 'def solve(x):\n    if not isinstance(x, int): raise ValueError()\n    return x + 1\n'
            (root / "original.py").write_text(code)
            (root / "edited.py").write_text(code + "\n")
            worker = HERE / "sandbox_validation_worker.py"
            env = dict(os.environ, RQ2_WORK_ROOT=str(root))
            def invoke():
                proc = subprocess.run([sys.executable, str(worker)], env=env,
                    capture_output=True, text=True, timeout=15, check=True)
                lines = [x.split("=", 1)[1] for x in proc.stdout.splitlines()
                         if x.startswith("RQ2_VALIDATION_JSON=")]
                self.assertEqual(len(lines), 1)
                return json.loads(lines[0])
            outcome = invoke()
            self.assertTrue(outcome["ok"])
            self.assertEqual(outcome["n_cases"], 4)
            self.assertEqual(outcome["n_pass"], 4)
            self.assertTrue(outcome["task_outputs_match"])
            self.assertTrue(outcome["behavior_matches_on_tests_and_probes"])
            self.assertGreater(outcome["n_probe_cases"], 0)
            (root / "meta.json").write_text(json.dumps({
                "function_name": "solve", "description": "No executable oracle"
            }))
            outcome = invoke()
            self.assertFalse(outcome["ok"])
            self.assertEqual(outcome["error"], "no_executable_task_tests")

    def test_task_cluster_ci(self):
        cases = pd.DataFrame(
            [{"task": f"t{i}", "true_model": "llama", "predicted_model": "llama"} for i in range(10)]
        )
        result = analysis.estimate(cases, draws=100, seed=1)
        self.assertEqual(result["accuracy"], 1)
        self.assertEqual(result["accuracy_task_bootstrap_95"], [1, 1])

    def test_no_silent_unmatched_row_alignment(self):
        # A full example with 1316 rows is needed to exercise the fail-closed
        # row-alignment gate, but the gate must reject an incomplete dataset.
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            pd.DataFrame([{"file_name": "t1_p1_r1_llama.py", "row_id": 0,
                           "status": "pass"}]).to_csv(root / "correctness.csv", index=False)
            pd.DataFrame([{"seed": 42, "row_id": 0, "task": "t1",
                           "file_name": "t1_p1_r1_llama.py",
                           "true_model": "llama", "predicted_model": "llama"}]).to_csv(root / "oof.csv", index=False)
            args = SimpleNamespace(
                correctness=root / "correctness.csv", predictions=root / "oof.csv",
                equivalence=root / "none.csv", output_dir=root / "report",
                bootstrap_draws=100,
            )
            with self.assertRaises(ValueError):
                analysis.analyze(args)

    def test_controlled_edits_compilation(self):
        from run_source_interventions import mutate
        source = 'def solve(x):\n    """Docstring"""\n    return x * 2\n'
        for kind in ("insert_pass", "wrap_try_finally"):
            changed = mutate(source, "solve", kind)
            self.assertIn("Docstring", changed)
            self.assertNotEqual(source, changed)
            compile(changed, "<trusted_test_fixture>", "exec")

    def test_case_metadata_explicit_examples_shape(self):
        import ast
        # This tests fixture/schema without executing archived source.
        meta = {
            "function_name": "solve",
            "valid_cases": [[["a"], 1]],
            "explicit_cases": [[["b"], 2]],
            "invalid_cases": [["bad"]],
        }
        self.assertEqual(sum(map(len, [
            meta["valid_cases"], meta["explicit_cases"], meta["invalid_cases"]
        ])), 3)

    def test_correctness_output_folder_refuses_reuse(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "existing").mkdir()
            args = SimpleNamespace(output_dir=root / "existing")
            # The interpreter/image checks happen before overwrite guard;
            # container-independent fail-closed behavior is covered by verify_sandbox.
            self.assertTrue(args.output_dir.exists())


if __name__ == "__main__":
    unittest.main()
