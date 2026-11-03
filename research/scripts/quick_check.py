"""
quick_check.py — no filtering, just report.
"""
from pathlib import Path
import dis
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]

BYTE_POS = 24
MODEL = "qwen"
RAW = 47  # BUILD_LIST

rows = []
for task in TASKS:
    summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
    if not summary_path.exists():
        continue
    summary = pd.read_csv(summary_path)
    for _, rec in summary[summary["true"] == MODEL].iterrows():
        eff_path = ANALYSIS_DIR / task / f"{Path(rec['file']).stem}_effects.csv"
        if not eff_path.exists():
            continue
        eff = pd.read_csv(eff_path)
        row = eff[eff["feature"] == f"byte_{BYTE_POS}"]
        if row.empty:
            continue
        raw_val = int(row.iloc[0]["value"])
        if raw_val != RAW:
            continue
        shap = float(row.iloc[0][f"shap_{MODEL}"])
        rows.append({"task": task, "prompt": rec["prompt"], "run": rec["run"],
                      "shap": shap, "correct": rec["correct"]})

df = pd.DataFrame(rows)
print(df)
print(f"\nn={len(df)}, shap mean={df['shap'].mean():.3f}" if not df.empty else "n=0, opcode never appears here for this model")
