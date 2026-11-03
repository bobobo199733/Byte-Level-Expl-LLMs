"""
sweep_bytecode_length.py

Tests multiple bytecode lengths and reports classifier accuracy for each.

Usage:
    python scripts/sweep_bytecode_length.py
    python scripts/sweep_bytecode_length.py --lengths 16 32 64 128 192 256 320 384 512 768 1024 1536 2048
"""

import subprocess
import argparse
import sys
from pathlib import Path

BASE_DIR    = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"

DEFAULT_LENGTHS = [128, 192, 256, 320, 384, 512, 768]


def run(cmd, desc):
    print(f"\n  → {desc}")
    result = subprocess.run(
        [sys.executable] + cmd,
        cwd=BASE_DIR,
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"  ✗ FAILED (exit code {result.returncode})")
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lengths", type=int, nargs="+", default=DEFAULT_LENGTHS,
                        help="Bytecode lengths to test")
    args = parser.parse_args()

    results = []

    for length in args.lengths:
        print(f"\n{'='*60}")
        print(f"Testing bytecode length: {length}")
        print(f"{'='*60}")

        # test data (USE_TEST_DATA=1)
        ok = run([str(SCRIPTS_DIR / "extract_bytecode_features.py"), "1", str(length)],
                 f"extract features (test, length={length})")
        if not ok:
            results.append((length, "FAILED at extract test"))
            continue

        ok = run([str(SCRIPTS_DIR / "preprocess_features.py"), "1"],
                 "preprocess features (test)")
        if not ok:
            results.append((length, "FAILED at preprocess test"))
            continue

        # train data (USE_TEST_DATA=0)
        ok = run([str(SCRIPTS_DIR / "extract_bytecode_features.py"), "0", str(length)],
                 f"extract features (train, length={length})")
        if not ok:
            results.append((length, "FAILED at extract train"))
            continue

        ok = run([str(SCRIPTS_DIR / "preprocess_features.py"), "0"],
                 "preprocess features (train)")
        if not ok:
            results.append((length, "FAILED at preprocess train"))
            continue

        ok = run([str(SCRIPTS_DIR / "train_bytecode_model.py")],
                 "train model")
        if not ok:
            results.append((length, "FAILED at train"))
            continue

        # try to read accuracy from the report
        try:
            import json
            report_path = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
            report = json.loads(report_path.read_text())
            acc = report.get("accuracy", report.get("test_accuracy", "?"))
            results.append((length, acc))
            print(f"\n  ✓ length={length}  accuracy={acc}")
        except Exception as e:
            results.append((length, f"done (could not read accuracy: {e})"))

    print(f"\n\n{'='*60}")
    print("SWEEP RESULTS")
    print(f"{'='*60}")
    print(f"  {'length':>8}  {'accuracy'}")
    print(f"  {'-'*8}  {'-'*20}")
    for length, acc in results:
        print(f"  {length:>8}  {acc}")


if __name__ == "__main__":
    main()
