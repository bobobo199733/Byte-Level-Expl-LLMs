"""
cross_check_population.py

Compares the raw feature CSV (ground truth, all 263 test files) against
the per-file _effects.csv files used by the scan scripts, for a given
(byte_pos, model, raw_opcode) -- to check whether effects.csv coverage
is complete.

Run from the project root:
    python scripts/cross_check_population.py
"""

from pathlib import Path
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]

BYTE_POS = 16
MODEL = "mistral"
RAW = 110


def main():
    df = pd.read_csv(FEATURES_CSV)
    col = f"byte_{BYTE_POS}"

    # ground truth: all mistral files with byte_16 == 110
    gt = df[(df["model"] == MODEL) & (df[col] == RAW)]
    print(f"Ground truth (processed_bytecode_features.csv): "
          f"{len(gt)} {MODEL} files with byte_{BYTE_POS}={RAW}")

    # total mistral files for reference
    total_mistral = (df["model"] == MODEL).sum()
    print(f"Total {MODEL} files in features CSV: {total_mistral}")

    if "file" in gt.columns or "filename" in gt.columns:
        file_col = "file" if "file" in gt.columns else "filename"
        print("\nFiles in ground truth:")
        print(sorted(gt[file_col].tolist()))
    else:
        print("\n(no filename column found in features CSV -- columns are:)")
        print(list(df.columns)[:10], "...")

    # now check effects.csv coverage
    n_effects_found = 0
    n_effects_missing = []
    for task in TASKS:
        summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
        if not summary_path.exists():
            continue
        summary = pd.read_csv(summary_path)
        for _, rec in summary[summary["true"] == MODEL].iterrows():
            eff_path = ANALYSIS_DIR / task / f"{Path(rec['file']).stem}_effects.csv"
            if eff_path.exists():
                n_effects_found += 1
            else:
                n_effects_missing.append(rec["file"])

    print(f"\n_effects.csv coverage for {MODEL}: {n_effects_found} found, "
          f"{len(n_effects_missing)} missing")
    if n_effects_missing:
        print("Missing files:", n_effects_missing)


if __name__ == "__main__":
    main()
