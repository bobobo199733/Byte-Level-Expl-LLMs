"""
full_population_check.py

For a given (byte_pos, model, raw_opcode), scans ALL test files where
that model's bytecode has the target opcode at the target byte position
(no divergence/threshold filtering), and reports full aggregate stats
(SHAP range/mean, byte_vote, correctness) across the entire population.

Run from the project root:
    python scripts/full_population_check.py
"""

from pathlib import Path
import dis
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]

# ── configure ────────────────────────────────────────────────────────
TARGETS = [
    (54, "mistral", 91), # LOAD_GLOBAL
    (54, "mistral", 85), # LOAD_FAST
    (54, "llama", 53),   # CALL
    (24, "llama",  91),  # LOAD_GLOBAL
    (12, "llama",  110), # STORE_FAST
    (12, "mistral", 85), # LOAD_FAST
    (28, "qwen",  97),   # POP_JUMP_IF_FALSE
    (28, "llama", 53),   # CALL
    (32, "llama", 45),   # BINARY_OP
    (16, "mistral",110),   # STORE_FAST
    (14, "llama", 91),   # LOAD_GLOBAL

]


def get_byte_vote(eff, byte_pos, true_model):
    row = eff[eff["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None
    shap_vec = {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
    return max(shap_vec, key=shap_vec.get) == true_model


def main():
    for byte_pos, model, raw_val in TARGETS:
        opname = dis.opname[raw_val]
        rows = []

        for task in TASKS:
            summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
            if not summary_path.exists():
                continue
            summary = pd.read_csv(summary_path)
            for _, rec in summary[summary["true"] == model].iterrows():
                eff_path = ANALYSIS_DIR / task / f"{Path(rec['file']).stem}_effects.csv"
                if not eff_path.exists():
                    continue
                eff = pd.read_csv(eff_path)
                row = eff[eff["feature"] == f"byte_{byte_pos}"]
                if row.empty:
                    continue
                raw_observed = int(row.iloc[0]["value"])
                if raw_observed != raw_val:
                    continue
                shap = float(row.iloc[0][f"shap_{model}"])
                vote = get_byte_vote(eff, byte_pos, model)
                rows.append({
                    "task": task, "prompt": rec["prompt"], "run": rec["run"],
                    "shap": shap, "byte_vote": vote, "correct": bool(rec["correct"]),
                    "file": rec["file"],
                })

        df = pd.DataFrame(rows)
        print("=" * 70)
        print(f"byte_{byte_pos} = {opname}({raw_val}) in {model} files -- FULL POPULATION")
        print("=" * 70)
        if df.empty:
            print("n=0\n")
            continue

        n = len(df)
        n_correct = df["correct"].sum()
        n_vote = df["byte_vote"].sum()
        tasks = sorted(df["task"].unique().tolist())

        print(df.to_string(index=False))
        print(f"\nn={n}")
        print(f"SHAP range: {df['shap'].min():+.3f} to {df['shap'].max():+.3f}")
        print(f"SHAP mean:  {df['shap'].mean():+.3f}")
        print(f"byte_vote:  {n_vote}/{n}")
        print(f"correct:    {n_correct}/{n}")
        print(f"tasks:      {','.join(tasks)}")
        print()


if __name__ == "__main__":
    main()
