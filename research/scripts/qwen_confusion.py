"""
qwen_confusion.py
"""
from pathlib import Path
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]

rows = []
for task in TASKS:
    summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
    if not summary_path.exists():
        continue
    summary = pd.read_csv(summary_path)
    qsub = summary[summary["true"] == "qwen"]
    for _, rec in qsub.iterrows():
        rows.append({"task": task, "prompt": rec["prompt"], "run": rec["run"],
                      "predicted": rec.get("predicted", "?"), "correct": rec["correct"]})

df = pd.DataFrame(rows)
print(df.to_string(index=False))
print("\nPrediction distribution for true=qwen, by task:")
print(df.groupby(["task", "predicted"]).size().unstack(fill_value=0))
