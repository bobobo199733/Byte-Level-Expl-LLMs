"""
truncation_per_model_check.py

Checks the number/fraction of truncated bytecode files per model per task,
and the average raw (pre-truncation) bytecode length per model.
A file is "truncated" if its raw (pre-padding) bytecode length exceeds
MAX_LEN=320, meaning none of its 320 feature positions are -1 (padding).

Run from project root:
    python scripts/truncation_per_model_check.py
"""

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR          = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

TASKS     = [f"t{i}" for i in range(41, 51)]
BYTE_COLS = [f"byte_{i}" for i in range(320)]


def main():
    df = pd.read_csv(TEST_FEATURES_CSV)

    parts        = df["file_name"].str.split("_", expand=True)
    df["task"]   = parts[0]
    df["prompt"] = parts[1]

    byte_df = df[BYTE_COLS].values.astype(int)

    # A file is truncated if it has NO padding (-1) anywhere in the 320 vector,
    # i.e. its raw bytecode length was >= 320 bytes before truncation.
    df["truncated"] = (byte_df != -1).all(axis=1)

    # Raw (pre-truncation, pre-padding) bytecode length, capped at 320 for
    # truncated files since the true length beyond 320 is not recoverable
    # from the padded/truncated feature vector alone.
    df["bc_length"] = (byte_df != -1).sum(axis=1)

    print("=" * 70)
    print("TRUNCATION RATE PER MODEL PER TASK")
    print("=" * 70)

    pivot = df.groupby(["task", "model"])["truncated"].mean().unstack()
    pivot = pivot[["llama", "mistral", "qwen"]]

    print(f"{'task':6s}  {'llama':>8s}  {'mistral':>8s}  {'qwen':>8s}")
    print("-" * 40)
    for task in TASKS:
        row = pivot.loc[task]
        print(f"{task:6s}  {row['llama']*100:7.1f}%  {row['mistral']*100:7.1f}%  "
              f"{row['qwen']*100:7.1f}%")

    print()
    print("=" * 70)
    print("OVERALL TRUNCATION RATE PER MODEL (all test tasks)")
    print("=" * 70)
    overall = df.groupby("model")["truncated"].agg(["sum", "count", "mean"])
    overall["mean"] = (overall["mean"] * 100).round(1)
    overall = overall.rename(columns={"sum": "n_truncated", "count": "n_total",
                                       "mean": "pct_truncated"})
    print(overall[["n_truncated", "n_total", "pct_truncated"]])

    print()
    print("=" * 70)
    print("AVERAGE BYTECODE LENGTH PER MODEL (capped at 320, all tasks)")
    print("=" * 70)
    length_stats = df.groupby("model")["bc_length"].agg(["mean", "median", "std"])
    length_stats = length_stats.round(2)
    print(length_stats)

    print()
    print("=" * 70)
    print("AVERAGE BYTECODE LENGTH PER MODEL PER TASK (capped at 320)")
    print("=" * 70)
    length_pivot = df.groupby(["task", "model"])["bc_length"].mean().unstack()
    length_pivot = length_pivot[["llama", "mistral", "qwen"]].round(1)

    print(f"{'task':6s}  {'llama':>8s}  {'mistral':>8s}  {'qwen':>8s}")
    print("-" * 40)
    for task in TASKS:
        row = length_pivot.loc[task]
        print(f"{task:6s}  {row['llama']:8.1f}  {row['mistral']:8.1f}  "
              f"{row['qwen']:8.1f}")

    # print()
    # print("=" * 70)
    # print("TRUNCATION RATE ON QWEN'S WORST TASKS (t42, t46, t47, t49, t50)")
    # print("=" * 70)
    # highlight = ["t42", "t46", "t47", "t49", "t50"]
    # for task in highlight:
    #     row = pivot.loc[task]
    #     print(f"  {task}: llama={row['llama']*100:5.1f}%  "
    #           f"mistral={row['mistral']*100:5.1f}%  qwen={row['qwen']*100:5.1f}%")

    # df.to_csv(BASE_DIR / "analysis" / "truncation_per_model.csv", index=False)
    # print(f"\nSaved per-file truncation data to analysis/truncation_per_model.csv")


if __name__ == "__main__":
    main()
