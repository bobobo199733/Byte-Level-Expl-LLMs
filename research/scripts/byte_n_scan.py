"""
byte_scan.py

For byte{N}_examples.csv (where N is configurable below), scans all
(model, opcode) combinations and reports the top candidates PER MODEL --
i.e. for each model separately, which opcode at byte_N has the
strongest/most consistent SHAP signal toward that model's own class.

Run from the project root:
    python scripts/byte_scan.py
"""

from pathlib import Path
import dis
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"

# ── configurable ────────────────────────────────────────────────────────
TARGET_BYTE = 14
MIN_N       = 5   # minimum unique instances to report
TOP_K       = 5   # how many rows to show per model
# ───────────────────────────────────────────────────────────────────────

IN_FILE  = ANALYSIS_DIR / f"byte{TARGET_BYTE}_examples.csv"
OUT_FILE = ANALYSIS_DIR / f"byte{TARGET_BYTE}_scan.csv"

CLASS_NAMES = ["llama", "mistral", "qwen"]


def main():
    df = pd.read_csv(IN_FILE)

    results = []

    for model in CLASS_NAMES:
        op_col   = f"{model}_op"
        raw_col  = f"{model}_raw"
        shap_col = f"{model}_shap"
        corr_col = f"{model}_correct"
        run_col  = f"{model}_run"
        file_col = f"{model}_file"

        if not all(c in df.columns for c in [op_col, raw_col, shap_col, corr_col]):
            continue

        for raw_val in df[raw_col].dropna().unique():
            subset = df[df[raw_col] == raw_val].copy()
            dedup_cols = ["task", "prompt", run_col]
            if file_col in subset.columns:
                dedup_cols.append(file_col)
            subset = subset.drop_duplicates(subset=dedup_cols)

            if len(subset) < MIN_N:
                continue

            shaps = subset[shap_col].dropna()
            if shaps.empty:
                continue

            n_correct = subset[corr_col].sum()
            n = len(subset)

            try:
                opname = dis.opname[int(raw_val)]
            except Exception:
                opname = "?"

            results.append({
                "model": model,
                "opcode": opname,
                "raw": int(raw_val),
                "n": n,
                "shap_min": shaps.min(),
                "shap_max": shaps.max(),
                "shap_mean": shaps.mean(),
                "shap_abs_mean": shaps.abs().mean(),
                "correct": int(n_correct),
                "correct_pct": n_correct / n,
                "tasks": sorted(subset["task"].unique().tolist()),
            })

    if not results:
        print("No (model, opcode) combinations met the minimum count.")
        return

    res_df = pd.DataFrame(results)
    res_df["score"] = res_df["shap_abs_mean"] * res_df["correct_pct"]

    for model in CLASS_NAMES:
        sub = res_df[res_df["model"] == model].sort_values("score", ascending=False)
        if sub.empty:
            print(f"No qualifying (opcode) combinations for {model}.\n")
            continue
        print("=" * 90)
        print(f"MODEL: {model}  (byte_{TARGET_BYTE}, top {TOP_K} by score)")
        print("=" * 90)
        print(f"{'opcode':22s} {'raw':>4} {'n':>3} {'shap_min':>9} {'shap_max':>9} "
              f"{'shap_mean':>9} {'correct':>8}  tasks")
        for _, row in sub.head(TOP_K).iterrows():
            print(f"{row['opcode']:22s} {row['raw']:>4} {row['n']:>3} "
                  f"{row['shap_min']:>+9.3f} {row['shap_max']:>+9.3f} {row['shap_mean']:>+9.3f} "
                  f"{row['correct']}/{row['n']:<6} {','.join(row['tasks'])}")
        print()

    res_df.sort_values(["model", "score"], ascending=[True, False]).to_csv(OUT_FILE, index=False)
    print(f"Saved full ranking to {OUT_FILE}")


if __name__ == "__main__":
    main()
