"""
find_best_example.py

For each test task, finds (prompt, run_llama, run_mistral, run_qwen) combinations where:
  - each model was correctly predicted in its respective run
  - at least one even byte position has a different opname for each model
  - for that byte, the SHAP value pushes toward the correct model

Scans ALL even byte positions (not just top SHAP), using effects CSVs directly.

Run from the project root:
    python scripts/find_best_example.py
"""

from pathlib import Path
from itertools import product
import pandas as pd
import dis

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS        = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
CLASS_NAMES  = ["llama", "mistral", "qwen"]
MAX_LEN      = 320  # scan all even positions up to this
TOP_N_BYTES  = 20   # only consider top N bytes by mean SHAP magnitude


def load_summary(task):
    path = ANALYSIS_DIR / task / f"{task}_summary.csv"
    if not path.exists():
        print(f"  [{task}] missing summary CSV, skipping")
        return None
    return pd.read_csv(path)


def load_effects(task, fname):
    path = ANALYSIS_DIR / task / f"{Path(fname).stem}_effects.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def get_opname(effects_df, byte_pos):
    """Get opname at byte_pos from effects CSV (raw value → dis.opname)."""
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None, None
    raw = int(row.iloc[0]["value"])
    if raw == -1:
        return None, None  # padding
    try:
        name = dis.opname[raw]
        if name == "<?>":
            return None, None
    except Exception:
        return None, None
    return name, raw


def get_shap_top_class(effects_df, byte_pos):
    """Return the class that SHAP pushes toward most for this byte."""
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None
    shap_vec = {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
    return max(shap_vec, key=shap_vec.get)


def find_candidates(task, summary):
    results = []
    even_positions = list(range(0, MAX_LEN, 2))  # all even byte positions

    for prompt in summary["prompt"].unique():
        prompt_summary = summary[summary["prompt"] == prompt]

        correct_per_model = {}
        for model in CLASS_NAMES:
            correct_files = prompt_summary[
                (prompt_summary["true"] == model) &
                (prompt_summary["correct"] == True)
            ][["file", "run"]].to_dict("records")
            correct_per_model[model] = correct_files

        if not all(correct_per_model[m] for m in CLASS_NAMES):
            continue

        for combo in product(
            correct_per_model["llama"],
            correct_per_model["mistral"],
            correct_per_model["qwen"],
        ):
            files = {m: c["file"] for m, c in zip(CLASS_NAMES, combo)}
            runs  = {m: c["run"]  for m, c in zip(CLASS_NAMES, combo)}

            # load effects for all three files
            effects = {}
            skip = False
            for model in CLASS_NAMES:
                ef = load_effects(task, files[model])
                if ef is None:
                    skip = True
                    break
                effects[model] = ef
            if skip:
                continue

            # sort even positions by mean SHAP magnitude across the three files
            def mean_magnitude(bp):
                total = 0.0
                for model in CLASS_NAMES:
                    row = effects[model][effects[model]["feature"] == f"byte_{bp}"]
                    if not row.empty:
                        total += float(row.iloc[0]["magnitude"])
                return total / 3

            sorted_positions = sorted(even_positions, key=mean_magnitude, reverse=True)[:TOP_N_BYTES]

            for byte_pos in sorted_positions:
                opnames  = {}
                raw_vals = {}
                for model in CLASS_NAMES:
                    opname, raw = get_opname(effects[model], byte_pos)
                    if opname is None:
                        break
                    opnames[model]  = opname
                    raw_vals[model] = raw
                else:
                    all_diff_opnames = len(set(opnames.values())) == 3
                    all_diff_raw     = len(set(raw_vals.values())) == 3

                    shap_ok = {}
                    for model in CLASS_NAMES:
                        top = get_shap_top_class(effects[model], byte_pos)
                        shap_ok[model] = (top == model)

                    all_shap_correct = all(shap_ok.values())

                    results.append({
                        "task":             task,
                        "prompt":           prompt,
                        "run_llama":        runs["llama"],
                        "run_mistral":      runs["mistral"],
                        "run_qwen":         runs["qwen"],
                        "byte_pos":         byte_pos,
                        "all_diff_opnames": all_diff_opnames,
                        "all_diff_raw":     all_diff_raw,
                        "all_shap_correct": all_shap_correct,
                        "llama_op":         opnames["llama"],
                        "mistral_op":       opnames["mistral"],
                        "qwen_op":          opnames["qwen"],
                        "llama_raw":        raw_vals["llama"],
                        "mistral_raw":      raw_vals["mistral"],
                        "qwen_raw":         raw_vals["qwen"],
                        "llama_file":       files["llama"],
                        "mistral_file":     files["mistral"],
                        "qwen_file":        files["qwen"],
                        "shap_llama_ok":    shap_ok.get("llama", False),
                        "shap_mistral_ok":  shap_ok.get("mistral", False),
                        "shap_qwen_ok":     shap_ok.get("qwen", False),
                    })

    return pd.DataFrame(results) if results else pd.DataFrame()


def _print_rows(df):
    for _, row in df.drop_duplicates(["prompt", "byte_pos"]).iterrows():
        print(f"    prompt={row['prompt']}  byte_{row['byte_pos']}")
        for model, op_col, run_col, raw_col, shap_col in [
            ("llama",   "llama_op",   "run_llama",   "llama_raw",   "shap_llama_ok"),
            ("mistral", "mistral_op", "run_mistral", "mistral_raw", "shap_mistral_ok"),
            ("qwen",    "qwen_op",    "run_qwen",    "qwen_raw",    "shap_qwen_ok"),
        ]:
            tick = "✓" if row.get(shap_col) else "✗"
            print(f"      {model:7s} ({row[run_col]}): {row[op_col]:25s} raw={row[raw_col]:<6} {tick}")


def print_results(task, df):
    if df.empty:
        print(f"  No candidates found for {task}")
        return

    best = df[df["all_diff_opnames"] & df["all_shap_correct"]]
    if not best.empty:
        print(f"\n  ★ BEST (diff opnames + SHAP pushes correct):")
        _print_rows(best)
        return

    diff_only = df[df["all_diff_opnames"]]
    if not diff_only.empty:
        print(f"\n  ✓ GOOD (diff opnames, SHAP direction not fully correct):")
        _print_rows(diff_only)
    else:
        print(f"  No fully divergent bytes found across any correct prediction combo")


def print_opname_aggregation(combined):
    best = combined[combined["all_diff_opnames"] & combined["all_shap_correct"]]
    best = best.drop_duplicates(["task", "prompt", "byte_pos"])

    if best.empty:
        print("\nNo BEST results to aggregate.")
        return

    print(f"\n{'='*60}")
    print("OPNAME PATTERNS IN BEST RESULTS (all tasks, SHAP-correct bytes only)")
    print(f"{'='*60}")
    print(f"Total BEST cases: {len(best)} (across {best['task'].nunique()} tasks)\n")

    for model, col in [("llama", "llama_op"), ("mistral", "mistral_op"), ("qwen", "qwen_op")]:
        counts = best[col].value_counts()
        print(f"{model.upper()}:")
        for opname, count in counts.items():
            tasks_with = sorted(best[best[col] == opname]["task"].unique())
            print(f"  {opname:<30} {count}x  (tasks: {', '.join(tasks_with)})")
        print()


def main():
    all_results = []

    for task in TASKS:
        print(f"\n{'='*60}")
        print(f"Task: {task}")
        summary = load_summary(task)
        if summary is None:
            continue

        print(f"  Searching all even byte positions (0-{MAX_LEN-2})...")
        df = find_candidates(task, summary)
        all_results.append(df) if not df.empty else None
        print_results(task, df)

    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        out_path = ANALYSIS_DIR / "best_visualization_candidates.csv"
        combined.to_csv(out_path, index=False)
        print(f"\n\nFull results saved to: {out_path}")
        print_opname_aggregation(combined)


if __name__ == "__main__":
    main()
