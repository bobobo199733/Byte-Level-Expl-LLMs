"""
find_byte16_examples.py

For a fixed byte position (default: byte_16), scans all tasks/prompts and
reports every llama/mistral file pair where:
  - the opcode at this byte differs between llama and mistral
  - at least one of llama or mistral has |SHAP| above a threshold at this byte

Correctness (overall prediction correct/incorrect) is reported for all
three models as observed -- it is NOT a selection criterion.

Run from the project root:
    python scripts/find_byte16_examples.py
"""

from pathlib import Path
from itertools import product
import pandas as pd
import dis

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"

TASKS         = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
CLASS_NAMES   = ["llama", "mistral", "qwen"]
TARGET_BYTE   = 14
SHAP_THRESHOLD = 0.10  # at least one of llama/mistral must exceed this in |shap_<own class>|


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


def find_candidates(task, summary, byte_pos):
    results = []

    for prompt in summary["prompt"].unique():
        prompt_summary = summary[summary["prompt"] == prompt]

        # get ALL rows per model for this prompt (all runs)
        rows_per_model = {}
        for model in CLASS_NAMES:
            rows = prompt_summary[prompt_summary["true"] == model]
            rows_per_model[model] = rows.to_dict("records")

        if not rows_per_model.get("llama") or not rows_per_model.get("mistral") or not rows_per_model.get("qwen"):
            continue

        # iterate over all llama x mistral run combinations
        for llama_rec, mistral_rec, qwen_rec in product(rows_per_model["llama"], rows_per_model["mistral"], rows_per_model['qwen']):
            files = {"llama": llama_rec["file"], "mistral": mistral_rec["file"], "qwen": qwen_rec["file"]}
            runs  = {"llama": llama_rec["run"],  "mistral": mistral_rec["run"], "qwen": qwen_rec["run"]}
            correct = {"llama": bool(llama_rec["correct"]), "mistral": bool(mistral_rec["correct"]), "qwen": bool(qwen_rec["correct"])}

            # qwen: just take all available runs too, report each separately
            qwen_recs = rows_per_model.get("qwen", [])

            effects = {}
            skip = False
            for model in ("llama", "mistral", "qwen"):
                ef = load_effects(task, files[model])
                if ef is None:
                    skip = True
                    break
                effects[model] = ef
            if skip:
                continue

            opnames, raws, shaps = {}, {}, {}
            ok = True
            for model in ("llama", "mistral", "qwen"):
                opname, raw = get_opname(effects[model], byte_pos)
                shap_val = get_shap_for_class(effects[model], byte_pos, model)
                if opname is None or shap_val is None:
                    ok = False
                    break
                opnames[model], raws[model], shaps[model] = opname, raw, shap_val
            if not ok:
                continue

            diff_opnames = opnames["llama"] != opnames["mistral"]
            above_threshold = (
                abs(shaps["llama"]) >= SHAP_THRESHOLD or
                abs(shaps["mistral"]) >= SHAP_THRESHOLD
            )
            if not (diff_opnames and above_threshold):
                continue

            # for qwen, just take the first available run (or report all -- your choice)
            for qwen_rec in (qwen_recs[:1] if qwen_recs else [None]):
                qwen_op, qwen_raw, qwen_shap, qwen_correct, qwen_run = None, None, None, None, None
                if qwen_rec is not None:
                    qwen_ef = load_effects(task, qwen_rec["file"])
                    if qwen_ef is not None:
                        qwen_op, qwen_raw = get_opname(qwen_ef, byte_pos)
                        qwen_shap = get_shap_for_class(qwen_ef, byte_pos, "qwen")
                    qwen_correct = bool(qwen_rec["correct"])
                    qwen_run = qwen_rec["run"]

                results.append({
                    "task": task, "prompt": prompt, "byte_pos": byte_pos,
                    "llama_run": runs["llama"], "llama_op": opnames["llama"],
                    "llama_raw": raws["llama"], "llama_shap": shaps["llama"],
                    "llama_correct": correct["llama"],
                    "mistral_run": runs["mistral"], "mistral_op": opnames["mistral"],
                    "mistral_raw": raws["mistral"], "mistral_shap": shaps["mistral"],
                    "mistral_correct": correct["mistral"],
                    "qwen_run": qwen_run, "qwen_op": qwen_op,
                    "qwen_raw": qwen_raw, "qwen_shap": qwen_shap,
                    "qwen_correct": qwen_correct,
                    "llama_file": files["llama"], "mistral_file": files["mistral"], "qwen_file": files["qwen"]
                })

    return pd.DataFrame(results) if results else pd.DataFrame()


def main():
    all_results = []
    for task in TASKS:
        summary = load_summary(task)
        if summary is None:
            continue
        df = find_candidates(task, summary, TARGET_BYTE)
        if not df.empty:
            all_results.append(df)

    if not all_results:
        print("No candidates found.")
        return

    combined = pd.concat(all_results, ignore_index=True)

    # deduplicate on the actual underlying files (run-level), not just task/prompt
    combined = combined.drop_duplicates(
        subset=["task", "prompt", "llama_run", "llama_file",
                "mistral_run", "mistral_file"]
    ).reset_index(drop=True)

    out_path = ANALYSIS_DIR / f"byte{TARGET_BYTE}_examples.csv"
    combined.to_csv(out_path, index=False)
    print(f"Saved {len(combined)} deduplicated rows to {out_path}\n")

    for _, row in combined.iterrows():
        print(f"{row['task']}/{row['prompt']}  byte_{TARGET_BYTE}  "
              f"(llama={row['llama_run']}, mistral={row['mistral_run']}, qwen={row.get('qwen_run')})")
        for model in CLASS_NAMES:
            op   = row.get(f"{model}_op")
            raw  = row.get(f"{model}_raw")
            shap = row.get(f"{model}_shap")
            corr = row.get(f"{model}_correct")
            if op is None:
                print(f"    {model:7s}: not found")
                continue
            tick = "✓" if corr else ("✗" if corr is not None else "?")
            shap_str = f"{shap:+.3f}" if shap is not None else "?"
            print(f"    {model:7s}: {op:25s} raw={raw:<6} shap={shap_str:>7}  pred_correct={tick}")
        print()

    # ── aggregate stats: STORE_FAST vs non-STORE_FAST for mistral ──────────
    mistral_storefast = combined[combined["mistral_op"] == "STORE_FAST"]
    mistral_other     = combined[combined["mistral_op"] != "STORE_FAST"]

    print("=" * 60)
    print("AGGREGATE: mistral SHAP at byte_"+str(TARGET_BYTE)+", by opcode")
    print("=" * 60)

    if not mistral_storefast.empty:
        shaps = mistral_storefast["mistral_shap"]
        n_correct = mistral_storefast["mistral_correct"].sum()
        print(f"\nSTORE_FAST (n={len(mistral_storefast)}):")
        print(f"  SHAP range: {shaps.min():+.3f} to {shaps.max():+.3f}")
        print(f"  SHAP mean:  {shaps.mean():+.3f}")
        print(f"  correct:    {n_correct}/{len(mistral_storefast)}")
        print(f"  instances:  " + ", ".join(
            f"{r.task}/{r.prompt}(m={r.mistral_run})" for r in mistral_storefast.itertuples()
        ))

    if not mistral_other.empty:
        shaps = mistral_other["mistral_shap"]
        n_correct = mistral_other


if __name__ == "__main__":
    main()
