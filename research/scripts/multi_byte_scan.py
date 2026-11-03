"""
multi_byte_scan.py

For a list of (byte_pos, model, raw_opcode) targets, generates
byte{N}_examples.csv if missing (reusing the find_byte16_examples.py
logic, generalized over byte_pos), then computes aggregate SHAP/
byte_vote/correctness statistics for each target -- producing ONE
combined summary table across multiple byte positions.

Run from the project root:
    python scripts/multi_byte_scan.py
"""

from pathlib import Path
from itertools import product
import dis
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"

TASKS       = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]
SHAP_THRESHOLD = 0.10

# ── targets to scan: (byte_pos, model, raw_opcode) ──────────────────────
TARGETS = [
    (54, "mistral", 91), # LOAD_GLOBAL
    (54, "mistral", 85), # LOAD_FAST
    (54, "llama", 53),   # CALL
    (24, "llama",  91),   # BUILD_LIST
    (12, "llama",  110),   # BINARY_OP
    (12, "mistral", 85), # LOAD_FAST
    (28, "qwen",  97),   # POP_JUMP_IF_FALSE
    (28, "llama", 53),   # CALL
    (32, "llama", 45),   # BINARY_OP
]


# ══════════════════════════════════════════════════════════════════════════════
# candidate-finding (generalized from find_byte16_examples.py)
# ══════════════════════════════════════════════════════════════════════════════

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


def get_opname(effects_df, byte_pos):
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None, None
    raw = int(row.iloc[0]["value"])
    if raw == -1:
        return None, None
    try:
        name = dis.opname[raw]
        if name == "<?>":
            return None, None
    except Exception:
        return None, None
    return name, raw


def get_shap_for_class(effects_df, byte_pos, class_name):
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None
    return float(row.iloc[0][f"shap_{class_name}"])


def get_byte_vote(effects_df, byte_pos, true_model):
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None
    shap_vec = {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
    return max(shap_vec, key=shap_vec.get) == true_model


def find_candidates(task, summary, byte_pos):
    results = []
    for prompt in summary["prompt"].unique():
        prompt_summary = summary[summary["prompt"] == prompt]
        rows_per_model = {}
        for model in CLASS_NAMES:
            rows = prompt_summary[prompt_summary["true"] == model]
            rows_per_model[model] = rows.to_dict("records")

        if not all(rows_per_model.get(m) for m in CLASS_NAMES):
            continue

        for llama_rec, mistral_rec, qwen_rec in product(
                rows_per_model["llama"], rows_per_model["mistral"], rows_per_model["qwen"]):

            recs  = {"llama": llama_rec, "mistral": mistral_rec, "qwen": qwen_rec}
            files = {m: recs[m]["file"] for m in CLASS_NAMES}
            runs  = {m: recs[m]["run"]  for m in CLASS_NAMES}
            correct = {m: bool(recs[m]["correct"]) for m in CLASS_NAMES}

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

            opnames, raws, shaps, votes = {}, {}, {}, {}
            for model in CLASS_NAMES:
                opname, raw = get_opname(effects[model], byte_pos)
                shap_val = get_shap_for_class(effects[model], byte_pos, model)
                vote = get_byte_vote(effects[model], byte_pos, model)
                opnames[model], raws[model], shaps[model], votes[model] = opname, raw, shap_val, vote

            # ── generalized filter ──────────────────────────────────────
            # 1. at least two of the three models' opcodes differ at this byte
            ops = [opnames[m] for m in CLASS_NAMES]
            any_diff = len(set(ops)) > 1

            # 2. at least one model has |SHAP| >= threshold (toward its own class)
            shap_vals = [v for v in shaps.values() if v is not None]
            above_threshold = any(abs(v) >= SHAP_THRESHOLD for v in shap_vals)

            if not (any_diff and above_threshold):
                continue

            row_out = {"task": task, "prompt": prompt, "byte_pos": byte_pos}
            for model in CLASS_NAMES:
                row_out[f"{model}_run"]       = runs[model]
                row_out[f"{model}_op"]        = opnames[model]
                row_out[f"{model}_raw"]       = raws[model]
                row_out[f"{model}_shap"]      = shaps[model]
                row_out[f"{model}_correct"]   = correct[model]
                row_out[f"{model}_byte_vote"] = votes[model]
                row_out[f"{model}_file"]      = files[model]
            results.append(row_out)

    return pd.DataFrame(results) if results else pd.DataFrame()


def get_or_build_examples(byte_pos):
    out_path = ANALYSIS_DIR / f"byte{byte_pos}_examples.csv"
    if out_path.exists():
        return pd.read_csv(out_path)

    all_results = []
    for task in TASKS:
        summary = load_summary(task)
        if summary is None:
            continue
        df = find_candidates(task, summary, byte_pos)
        if not df.empty:
            all_results.append(df)
    if not all_results:
        return pd.DataFrame()

    combined = pd.concat(all_results, ignore_index=True)
    combined = combined.drop_duplicates(
        subset=["task", "prompt", "llama_run", "llama_file",
                "mistral_run", "mistral_file", "qwen_run", "qwen_file"]
    ).reset_index(drop=True)
    combined.to_csv(out_path, index=False)
    return combined


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    summary_rows = []

    for byte_pos, model, raw_val in TARGETS:
        df = get_or_build_examples(byte_pos)
        if df.empty:
            print(f"byte_{byte_pos}: no examples found, skipping")
            continue

        raw_col = f"{model}_raw"
        run_col = f"{model}_run"
        shap_col = f"{model}_shap"
        corr_col = f"{model}_correct"
        vote_col = f"{model}_byte_vote"

        subset = df[df[raw_col] == raw_val].copy()
        subset = subset.drop_duplicates(subset=["task", "prompt", run_col])

        opname = dis.opname[raw_val]
        if subset.empty:
            print(f"byte_{byte_pos} / {model} / {opname}({raw_val}): n=0")
            continue

        shaps = subset[shap_col].dropna()
        n = len(subset)
        n_correct = subset[corr_col].sum()
        n_vote = subset[vote_col].sum()
        tasks = sorted(subset["task"].unique().tolist())

        summary_rows.append({
            "byte_pos": byte_pos,
            "model": model,
            "opcode": opname,
            "raw": raw_val,
            "n": n,
            "shap_min": shaps.min(),
            "shap_max": shaps.max(),
            "shap_mean": shaps.mean(),
            "byte_vote": f"{int(n_vote)}/{n}",
            "correct": f"{int(n_correct)}/{n}",
            "tasks": ",".join(tasks),
        })

    res_df = pd.DataFrame(summary_rows)
    out_path = ANALYSIS_DIR / "multi_byte_scan_summary.csv"
    res_df.to_csv(out_path, index=False)

    print(f"{'byte':>6} {'model':8s} {'opcode':22s} {'n':>3} "
          f"{'shap_min':>9} {'shap_max':>9} {'shap_mean':>9} "
          f"{'byte_vote':>10} {'correct':>8}  tasks")
    print("-" * 110)
    for _, row in res_df.iterrows():
        print(f"{row['byte_pos']:>6} {row['model']:8s} {row['opcode']:22s} {row['n']:>3} "
              f"{row['shap_min']:>+9.3f} {row['shap_max']:>+9.3f} {row['shap_mean']:>+9.3f} "
              f"{row['byte_vote']:>10} {row['correct']:>8}  {row['tasks']}")

    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
