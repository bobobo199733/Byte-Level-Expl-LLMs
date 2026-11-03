"""
qwen_similarity_check.py

1. Mean pairwise Hamming distance (normalized) between qwen↔llama and
   qwen↔mistral files, per task, for same-prompt pairs only.
2. Mean bytecode length (non-(-1) values in the 320-byte vector) per
   model per task.

Run from project root:
    python scripts/qwen_similarity_check.py
"""

from pathlib import Path
from itertools import product
import numpy as np
import pandas as pd

BASE_DIR          = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

TASKS      = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]
HIGHLIGHT  = {"t42", "t46", "t47", "t49", "t50"}
BYTE_COLS  = [f"byte_{i}" for i in range(320)]


def main():
    df = pd.read_csv(TEST_FEATURES_CSV)

    # parse task/prompt from file_name
    parts        = df["file_name"].str.split("_", expand=True)
    df["task"]   = parts[0]
    df["prompt"] = parts[1]

    byte_df = df[BYTE_COLS].values.astype(int)
    df["_idx"] = np.arange(len(df))

    # ── 1. pairwise Hamming distance qwen↔llama and qwen↔mistral ─────────
    print("=" * 65)
    print("1. MEAN PAIRWISE HAMMING DISTANCE (normalized, same-prompt pairs)")
    print("   qwen↔llama  vs  qwen↔mistral  per task")
    print("=" * 65)

    hamming_rows = []
    for task in TASKS:
        tdf = df[df["task"] == task]
        ql_dists, qm_dists = [], []

        for prompt, pgroup in tdf.groupby("prompt"):
            q_rows = pgroup[pgroup["model"] == "qwen"]["_idx"].tolist()
            l_rows = pgroup[pgroup["model"] == "llama"]["_idx"].tolist()
            m_rows = pgroup[pgroup["model"] == "mistral"]["_idx"].tolist()

            for qi, li in product(q_rows, l_rows):
                dist = (byte_df[qi] != byte_df[li]).mean()
                ql_dists.append(dist)

            for qi, mi in product(q_rows, m_rows):
                dist = (byte_df[qi] != byte_df[mi]).mean()
                qm_dists.append(dist)

        ql_mean = np.mean(ql_dists) if ql_dists else np.nan
        qm_mean = np.mean(qm_dists) if qm_dists else np.nan
        closer  = "llama" if ql_mean < qm_mean else "mistral"
        hamming_rows.append({
            "task": task,
            "qwen↔llama":   round(ql_mean, 3),
            "qwen↔mistral": round(qm_mean, 3),
            "closer_to":    closer,
            "highlight":    "★" if task in HIGHLIGHT else "",
        })

    ham_df = pd.DataFrame(hamming_rows).set_index("task")
    for task, row in ham_df.iterrows():
        marker = row["highlight"]
        print(f"  {task} {marker:1s}  qwen↔llama={row['qwen↔llama']:.3f}  "
              f"qwen↔mistral={row['qwen↔mistral']:.3f}  "
              f"[closer to {row['closer_to']}]")

    print()
    print("Tasks of interest:")
    for task in ["t45","t46","t47","t49","t50"]:
        row = ham_df.loc[task]
        print(f"  {task}: qwen↔llama={row['qwen↔llama']:.3f}  "
              f"qwen↔mistral={row['qwen↔mistral']:.3f}  "
              f"closer to {row['closer_to']}")

    # ── 2. mean bytecode length per model per task ────────────────────────
    print()
    print("=" * 65)
    print("2. MEAN BYTECODE LENGTH (non-(-1) bytes in 320-vector) per model")
    print("=" * 65)

    df["bc_length"] = (byte_df != -1).sum(axis=1)
    length_pivot = df.groupby(["task", "model"])["bc_length"].mean().unstack()
    length_pivot = length_pivot[["llama", "mistral", "qwen"]]
    length_pivot["qwen-llama"]   = (length_pivot["qwen"] - length_pivot["llama"]).round(1)
    length_pivot["qwen-mistral"] = (length_pivot["qwen"] - length_pivot["mistral"]).round(1)

    for task in TASKS:
        row    = length_pivot.loc[task]
        marker = "★" if task in HIGHLIGHT else " "
        print(f"  {task} {marker}  llama={row['llama']:5.1f}  "
              f"mistral={row['mistral']:5.1f}  qwen={row['qwen']:5.1f}  "
              f"(qwen-llama={row['qwen-llama']:+.1f}  "
              f"qwen-mistral={row['qwen-mistral']:+.1f})")

    print()
    print("Tasks of interest:")
    for task in ["t45","t46","t47","t49","t50"]:
        row = length_pivot.loc[task]
        closer = "llama" if abs(row["qwen-llama"]) < abs(row["qwen-mistral"]) \
                 else "mistral"
        print(f"  {task}: qwen={row['qwen']:.1f}  llama={row['llama']:.1f}  "
              f"mistral={row['mistral']:.1f}  "
              f"[length closer to {closer}]")


if __name__ == "__main__":
    main()
