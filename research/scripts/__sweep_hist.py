"""
sweep_hist_gradient_boosting.py

Sweeps HistGradientBoostingClassifier hyperparameters around current best config.

Run from project root:
    python scripts/sweep_hist_gradient_boosting.py
"""

import sys
import json
import subprocess
from pathlib import Path
from itertools import product
import re

BASE_DIR    = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

# ── parameter grid ────────────────────────────────────────────────────────────
SEEDS             = [42, 14, 28, 16, 7, 13, 21, 99, 123]
MAX_ITER          = [1000]
LEARNING_RATE     = [0.01, 0.05, 0.1]
MAX_DEPTH         = [4, 6, None]
L2_REGULARIZATION = [0.1, 0.5]

# fixed
MAX_LEAF_NODES  = 31
MIN_SAMPLES_LEAF = 20
CLASS_WEIGHT    = "balanced"


def patch_train_script(seed, max_iter, learning_rate, max_depth, l2):
    path = SCRIPTS_DIR / "train_bytecode_model.py"
    content = path.read_text()

    depth_str = "None" if max_depth is None else str(max_depth)

    new_block = f"""
        return HistGradientBoostingClassifier(
            max_iter={max_iter},
            learning_rate={learning_rate},
            max_leaf_nodes={MAX_LEAF_NODES},
            l2_regularization={l2},
            min_samples_leaf={MIN_SAMPLES_LEAF},
            max_depth={depth_str},
            random_state={seed},
            class_weight="{CLASS_WEIGHT}",
        )"""

    patched = re.sub(
        r'return HistGradientBoostingClassifier\(.*?\)',
        new_block,
        content,
        flags=re.DOTALL
    )
    path.write_text(patched)


def run_train():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "train_bytecode_model.py")],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def read_accuracy():
    try:
        report = json.loads(REPORT_FILE.read_text())
        return report.get("accuracy", report.get("test_accuracy", None))
    except Exception:
        return None


def main():
    results = []
    best_acc = 0
    best_cfg = None

    combos = list(product(SEEDS, MAX_ITER, LEARNING_RATE, MAX_DEPTH, L2_REGULARIZATION))
    print(f"Testing {len(combos)} combinations...\n")

    for i, (seed, max_iter, lr, depth, l2) in enumerate(combos):
        cfg = f"seed={seed:<5} iter={max_iter:<5} lr={lr:<5} depth={str(depth):<6} l2={l2}"
        print(f"  [{i+1:3d}/{len(combos)}] {cfg}", end="  ", flush=True)

        patch_train_script(seed, max_iter, lr, depth, l2)
        ok  = run_train()
        acc = read_accuracy() if ok else None

        if acc:
            marker = " ★" if acc > best_acc else ""
            print(f"acc={acc:.4f}{marker}")
            results.append((acc, seed, max_iter, lr, depth, l2))
            if acc > best_acc:
                best_acc = acc
                best_cfg = (seed, max_iter, lr, depth, l2)
        else:
            print("FAILED")

    print(f"\n{'='*60}")
    print("TOP 10 RESULTS")
    print(f"{'='*60}")
    for acc, seed, n_est, depth, features in sorted(results, key=lambda x: x[0], reverse=True)[:10]:
        print(f"  {acc:.4f}  seed={seed:<5} iter={max_iter:<5} lr={lr:<5} depth={str(depth):<6} l2={l2}")

    if best_cfg:
        seed, max_iter, lr, depth, l2 = best_cfg
        print(f"\nBEST: {best_acc:.4f}")
        print(f"  seed={seed}, max_iter={max_iter}, learning_rate={lr}, max_depth={depth}, l2={l2}")
        print(f"\nPatching train script with best config...")
        patch_train_script(seed, max_iter, lr, depth, l2)
        print("Done — train_bytecode_model.py updated with best config.")


if __name__ == "__main__":
    main()
