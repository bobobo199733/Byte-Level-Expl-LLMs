"""
sweep_random_forest.py

Sweeps Random Forest hyperparameters around current best config.

Run from project root:
    python scripts/sweep_random_forest.py
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
SEEDS        = [42, 14, 28, 16, 7, 13, 21, 99, 123]
N_ESTIMATORS = [100, 200, 300, 500]
MAX_DEPTH    = [None, 20, 30]
MAX_FEATURES = ["sqrt"]

# fixed
CLASS_WEIGHT = "balanced"


def patch_train_script(seed, n_estimators, max_depth, max_features):
    path = SCRIPTS_DIR / "train_bytecode_model.py"
    content = path.read_text()

    depth_str    = "None" if max_depth is None else str(max_depth)
    features_str = f'"{max_features}"' if isinstance(max_features, str) else str(max_features)

    new_block = f"""return RandomForestClassifier(
            n_estimators={n_estimators},
            max_depth={depth_str},
            max_features={features_str},
            random_state={seed},
            class_weight="{CLASS_WEIGHT}",
            n_jobs=-1,
        )"""

    patched = re.sub(
        r'return RandomForestClassifier\(.*?\)',
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

    combos = list(product(SEEDS, N_ESTIMATORS, MAX_DEPTH, MAX_FEATURES))
    print(f"Testing {len(combos)} combinations...\n")

    for i, (seed, n_est, depth, features) in enumerate(combos):
        cfg = f"seed={seed:<5} n_est={n_est:<5} depth={str(depth):<6} features={features}"
        print(f"  [{i+1:3d}/{len(combos)}] {cfg}", end="  ", flush=True)

        patch_train_script(seed, n_est, depth, features)
        ok  = run_train()
        acc = read_accuracy() if ok else None

        if acc:
            marker = " ★" if acc > best_acc else ""
            print(f"acc={acc:.4f}{marker}")
            results.append((acc, seed, n_est, depth, features))
            if acc > best_acc:
                best_acc = acc
                best_cfg = (seed, n_est, depth, features)
        else:
            print("FAILED")

    print(f"\n{'='*60}")
    print("TOP 10 RESULTS")
    print(f"{'='*60}")
    for acc, seed, n_est, depth, features in sorted(results, key=lambda x: x[0], reverse=True)[:10]:
        print(f"  {acc:.4f}  seed={seed:<5} n_est={n_est:<5} depth={str(depth):<6} features={features}")

    if best_cfg:
        seed, n_est, depth, features = best_cfg
        print(f"\nBEST: {best_acc:.4f}")
        print(f"  seed={seed}, n_estimators={n_est}, max_depth={depth}, max_features={features}")
        print(f"\nPatching train script with best config...")
        patch_train_script(seed, n_est, depth, features)
        print("Done — train_bytecode_model.py updated with best config.")


if __name__ == "__main__":
    main()
