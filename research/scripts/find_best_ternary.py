"""
find_best_ternary_files.py

For each task, finds prompts where llama and mistral are correctly predicted,
and where the top influential bytes are predominantly even (opcodes).
Qwen is shown but not required to be correct.

Run from project root:
    python scripts/find_best_ternary_files.py
"""

from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"

TASKS       = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]
TOP_N       = 10   # top N bytes by magnitude to check


def load_summary(task):
    path = ANALYSIS_DIR / task / f"{task}_summary.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_effects(task, fname):
    path = ANALYSIS_DIR / task / f"{Path(fname).stem}_effects.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def even_byte_fraction(effects_df, top_n=TOP_N):
    """Fraction of top_n most influential bytes that are even-indexed."""
    top = effects_df.nlargest(top_n, "magnitude")
    even = (top["byte_index"] % 2 == 0).sum()
    return even / top_n


def main():
    all_results = []

    for task in TASKS:
        summary = load_summary(task)
        if summary is None:
            continue

        for prompt in summary["prompt"].unique():
            psub = summary[summary["prompt"] == prompt]

            # llama and mistral must have correct predictions
            best_lm = {}
            for model in ["llama", "mistral"]:
                correct = psub[
                    (psub["true"] == model) &
                    (psub["correct"] == True)
                ].sort_values("max_prob", ascending=False)
                if correct.empty:
                    break
                best_lm[model] = correct.iloc[0]
            else:
                # qwen: correct if available, otherwise any
                qwen_rows = psub[psub["true"] == "qwen"]
                qwen_correct = qwen_rows[qwen_rows["correct"] == True]
                if not qwen_correct.empty:
                    best_lm["qwen"] = qwen_correct.sort_values(
                        "max_prob", ascending=False).iloc[0]
                elif not qwen_rows.empty:
                    best_lm["qwen"] = qwen_rows.sort_values(
                        "max_prob", ascending=False).iloc[0]
                else:
                    continue

                # load effects for llama and mistral, compute even fraction
                fracs = []
                skip  = False
                for model in ["llama", "mistral"]:
                    eff = load_effects(task, best_lm[model]["file"])
                    if eff is None:
                        skip = True
                        break
                    fracs.append(even_byte_fraction(eff))
                if skip:
                    continue

                mean_even_frac = np.mean(fracs)
                mean_lm_conf   = np.mean([best_lm[m]["max_prob"]
                                          for m in ["llama", "mistral"]])

                all_results.append({
                    "task":           task,
                    "prompt":         prompt,
                    "mean_even_frac": mean_even_frac,
                    "mean_lm_conf":   mean_lm_conf,
                    "llama_file":     best_lm["llama"]["file"],
                    "llama_run":      best_lm["llama"]["run"],
                    "llama_conf":     best_lm["llama"]["max_prob"],
                    "mistral_file":   best_lm["mistral"]["file"],
                    "mistral_run":    best_lm["mistral"]["run"],
                    "mistral_conf":   best_lm["mistral"]["max_prob"],
                    "qwen_file":      best_lm["qwen"]["file"],
                    "qwen_run":       best_lm["qwen"]["run"],
                    "qwen_conf":      best_lm["qwen"]["max_prob"],
                    "qwen_correct":   bool(best_lm["qwen"]["correct"]),
                })

    if not all_results:
        print("No candidates found.")
        return

    df = pd.DataFrame(all_results)
    # combined score: weight even_frac and lm_conf equally
    df["score"] = df["mean_even_frac"] * 0.5 + df["mean_lm_conf"] * 0.5
    df = df.sort_values("score", ascending=False)

    print("=" * 70)
    print("BEST PROMPTS: llama+mistral correct, top bytes predominantly even")
    print(f"Sorted by score = 0.5*even_frac + 0.5*mean_lm_conf")
    print(f"Even fraction = fraction of top {TOP_N} bytes by magnitude that are even")
    print("=" * 70)

    for _, row in df.head(20).iterrows():
        qwen_mark = "✓" if row["qwen_correct"] else "✗"
        print(f"\n  {row['task']} / {row['prompt']}  "
              f"score={row['score']:.3f}  "
              f"even_frac={row['mean_even_frac']:.2f}  "
              f"lm_conf={row['mean_lm_conf']:.3f}")
        for model in ["llama", "mistral"]:
            print(f"    {model:7s} ({row[f'{model}_run']}): "
                  f"conf={row[f'{model}_conf']:.3f}  "
                  f"file={row[f'{model}_file']}")
        print(f"    {'qwen':7s} ({row['qwen_run']}): "
              f"conf={row['qwen_conf']:.3f}  "
              f"file={row['qwen_file']}  {qwen_mark}")

    out_path = ANALYSIS_DIR / "best_ternary_files.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
