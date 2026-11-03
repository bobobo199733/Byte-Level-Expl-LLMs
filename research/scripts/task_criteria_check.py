"""
task_criteria_check.py
"""
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]

df = pd.read_csv(TEST_FEATURES_CSV)
byte_cols = [c for c in df.columns if c.startswith("byte_")]
parts = df["file_name"].str.split("_", expand=True)
df["task"] = parts[0]
df["prompt"] = parts[1]

rows = []
for task in TASKS:
    tdf = df[df["task"] == task]

    # truncation rate: fraction of files where byte_319 != -1 (i.e. not padded)
    trunc_rate = (tdf["byte_319"] != -1).mean()

    # mean pairwise Hamming distance (fraction of differing bytes) within each prompt
    hamming_dists = []
    for prompt, group in tdf.groupby("prompt"):
        vecs = group[byte_cols].values.astype(int)
        for i, j in combinations(range(len(vecs)), 2):
            dist = (vecs[i] != vecs[j]).mean()
            hamming_dists.append(dist)
    mean_hamming = np.mean(hamming_dists) if hamming_dists else np.nan

    rows.append({"task": task, "trunc_rate": trunc_rate, "mean_hamming": mean_hamming})

out = pd.DataFrame(rows).set_index("task")

# merge with existing combined summary
combined = pd.read_csv(ANALYSIS_DIR / "task_summary_combined.csv", index_col="task")
merged = combined.join(out)
merged = merged.sort_values("overall_accuracy")

print(merged.round(3))

# correlations with overall_accuracy
print("\nCorrelations with overall_accuracy:")
print(merged.corr()["overall_accuracy"].round(3))

merged.to_csv(ANALYSIS_DIR / "task_criteria_combined.csv")
print(f"\nSaved to {ANALYSIS_DIR / 'task_criteria_combined.csv'}")
