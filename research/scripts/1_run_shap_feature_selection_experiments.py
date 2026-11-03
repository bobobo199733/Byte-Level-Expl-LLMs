from pathlib import Path
import subprocess
import sys
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

SCRIPT = BASE_DIR / "scripts" / "1_train_shap_selected_model.py"
OUT_DIR = BASE_DIR / "shap_feature_selection"
SUMMARY_FILE = OUT_DIR / "selected_feature_results.csv"

TOP_N_VALUES = [16, 18, 32, 48, 64, 96, 128, 192, 256]


def main():
    rows = []

    for top_n in TOP_N_VALUES:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(top_n)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError(f"Failed for top_n={top_n}")

        last_line = result.stdout.strip().splitlines()[-1]
        payload = json.loads(last_line)

        rows.append(payload)

        print(f"top_n={top_n}, accuracy={payload['accuracy']:.4f}")

    df = pd.DataFrame(rows)
    df.to_csv(SUMMARY_FILE, index=False)

    print(f"\nSaved summary to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
