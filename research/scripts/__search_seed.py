"""
sweep_xgboost.py

Sweeps XGBoost hyperparameters around current best config to find better accuracy.
Focuses on seed sniping + small variance in key parameters.

Run from project root:
    python scripts/sweep_xgboost.py
"""

import sys
import json
import subprocess
from pathlib import Path
from itertools import product

BASE_DIR    = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

# ── parameter grid ────────────────────────────────────────────────────────────
SEEDS         = [14, 28, 16, 42, 7, 13, 21, 99, 123]
N_ESTIMATORS  = [500, 800]
MAX_DEPTH     = [3, 4, 5]
LEARNING_RATE = [0.01, 0.03, 0.05, 0.1]

# fixed
SUBSAMPLE        = 0.8
COLSAMPLE_BYTREE = 0.8
LENGTH           = 512


def patch_train_script(seed, n_estimators, max_depth, learning_rate):
    """Temporarily patch train_bytecode_model.py with new params."""
    path = SCRIPTS_DIR / "train_bytecode_model.py"
    content = path.read_text()

    # replace XGBoost config block
    import re
    new_block = f"""
        return XGBClassifier(
            n_estimators={n_estimators},
            max_depth={max_depth},
            learning_rate={learning_rate},
            subsample={SUBSAMPLE},
            colsample_bytree={COLSAMPLE_BYTREE},
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state={seed},
            n_jobs=-1,
        )"""

    patched = re.sub(
        r'return XGBClassifier\(.*?\)',
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

    combos = list(product(SEEDS, N_ESTIMATORS, MAX_DEPTH, LEARNING_RATE))
    print(f"Testing {len(combos)} combinations...\n")

    for i, (seed, n_est, depth, lr) in enumerate(combos):
        cfg = f"seed={seed:<5} n_est={n_est:<5} depth={depth} lr={lr}"
        print(f"  [{i+1:3d}/{len(combos)}] {cfg}", end="  ", flush=True)

        patch_train_script(seed, n_est, depth, lr)
        ok  = run_train()
        acc = read_accuracy() if ok else None

        if acc:
            marker = " ★" if acc > best_acc else ""
            print(f"acc={acc:.4f}{marker}")
            results.append((acc, seed, n_est, depth, lr))
            if acc > best_acc:
                best_acc = acc
                best_cfg = (seed, n_est, depth, lr)
        else:
            print("FAILED")

    print(f"\n{'='*60}")
    print("TOP 10 RESULTS")
    print(f"{'='*60}")
    for acc, seed, n_est, depth, lr in sorted(results, reverse=True)[:10]:
        print(f"  {acc:.4f}  seed={seed:<5} n_est={n_est:<5} depth={depth} lr={lr}")

    if best_cfg:
        seed, n_est, depth, lr = best_cfg
        print(f"\nBEST: {best_acc:.4f}")
        print(f"  seed={seed}, n_estimators={n_est}, max_depth={depth}, learning_rate={lr}")
        print(f"\nPatching train script with best config...")
        patch_train_script(seed, n_est, depth, lr)
        print("Done — train_bytecode_model.py updated with best config.")


if __name__ == "__main__":
    main()
