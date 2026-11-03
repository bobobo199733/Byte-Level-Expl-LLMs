"""
byte14_load_global_check.py

Check (a): distribution of byte_14 == 91 (LOAD_GLOBAL) across true model
labels, for all 263 test files. Uses the features CSV directly -- no SHAP
needed for this check.

Run from project root:
    python scripts/byte14_load_global_check.py
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV = BASE_DIR / "features" / "processed_bytecode_features.csv"

BYTE_POS = 14
RAW_VALUE = 91  # LOAD_GLOBAL


def main():
    df = pd.read_csv(TEST_FEATURES_CSV)
    col = f"byte_{BYTE_POS}"

    total_per_model = df.groupby("model").size()
    match = df[df[col] == RAW_VALUE]
    match_per_model = match.groupby("model").size()

    print(f"byte_{BYTE_POS} == {RAW_VALUE} (LOAD_GLOBAL) -- distribution by true model")
    print("=" * 60)

    summary = pd.DataFrame({
        "total_files": total_per_model,
        "n_with_load_global": match_per_model,
    }).fillna(0)
    summary["n_with_load_global"] = summary["n_with_load_global"].astype(int)
    summary["fraction"] = (summary["n_with_load_global"] / summary["total_files"]).round(3)

    print(summary)
    print(f"\nTotal: {len(match)}/{len(df)} files ({len(match)/len(df):.1%}) "
          f"have byte_{BYTE_POS} == {RAW_VALUE}")
    print(f"Baseline (uniform across 3 models): {1/3:.1%} of files per model")


if __name__ == "__main__":
    main()
