"""
byte_value_scan.py

For a given byte position and a list of raw values, scans ALL test files
(any model) and for each file where byte_{byte_pos} matches one of the
target raw values, reports:
  - the file's true model and predicted model
  - SHAP value at that byte toward the true class
  - whether the byte "voted" correctly (argmax of its 3 SHAP values == true class)
  - whether the overall prediction was correct
  - the corresponding source code line

Run from the project root:
    python scripts/byte_value_scan.py
"""

from pathlib import Path
import dis
import json
import sys
import types

import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
PROMPTS_DIR  = BASE_DIR / "test_data" / "prompts"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]

sys.path.insert(0, str(BASE_DIR / "scripts"))

# ── configure ────────────────────────────────────────────────────────
BYTE_POS = 54
RAW_VALUES = list(range(100, 151))   # list of raw values to scan for; e.g. [110, 109, 85]


# ══════════════════════════════════════════════════════════════════════════════
# Bytecode + source helpers
# ══════════════════════════════════════════════════════════════════════════════

def file_to_bytecode_display(py_file: Path, target_fn: str) -> list[dict]:
    """Use exactly the opcode-argument ordering used by the classifier."""
    from bytecode_utils import instruction_trace_from_file
    return instruction_trace_from_file(py_file, target_fn)


def get_source_line(py_file, lineno):
    if lineno is None:
        return ""
    try:
        lines = py_file.read_text(encoding="utf-8").split("\n")
        if 1 <= lineno <= len(lines):
            return lines[lineno - 1].strip()
    except Exception:
        pass
    return ""


def get_py_path(stem, model):
    return BASE_DIR / "test_data" / "outputs" / model / "cleaned" / f"{stem}.py"


def get_target_fn(task_id):
    return json.loads(
        (PROMPTS_DIR / task_id / "meta.json").read_text(encoding="utf-8")
    )["function_name"]


def get_byte_info(py_path, target_fn, byte_pos):
    try:
        bc_rows = file_to_bytecode_display(py_path, target_fn)
        match = next(
            (r for r in bc_rows
             if r["byte_pos"] == byte_pos or r["arg_pos"] == byte_pos),
            None
        )
        if match is None:
            return None, None, None, None
        source_line = match["source_line"]  # AST-normalized source used for compilation
        if match["byte_pos"] == byte_pos:
            raw_display = dis.opmap.get(match["opname"], "?")
        else:
            raw_display = match["arg_raw"]
        return match["opname"], raw_display, match["argval"], source_line
    except Exception as e:
        print(f"  ERROR {py_path}: {e}")
        return None, None, None, None


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    raw_set = set(RAW_VALUES)
    opnames = {}
    for rv in RAW_VALUES:
        try:
            opnames[rv] = dis.opname[rv]
        except Exception:
            opnames[rv] = "?"

    labels = ", ".join(f"{rv} ({opnames[rv]})" for rv in RAW_VALUES)
    print(f"Scanning for byte_{BYTE_POS} in {{{labels}}} across all test files\n")

    target_fn_cache = {}
    out_rows = []

    for task in TASKS:
        summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
        if not summary_path.exists():
            continue
        summary = pd.read_csv(summary_path)

        if task not in target_fn_cache:
            target_fn_cache[task] = get_target_fn(task)
        target_fn = target_fn_cache[task]

        for _, rec in summary.iterrows():
            true_model = rec["true"]
            stem = Path(rec["file"]).stem

            eff_path = ANALYSIS_DIR / task / f"{stem}_effects.csv"
            if not eff_path.exists():
                continue
            eff = pd.read_csv(eff_path)

            row = eff[eff["feature"] == f"byte_{BYTE_POS}"]
            if row.empty:
                continue

            observed_raw = int(row.iloc[0]["value"])
            if observed_raw not in raw_set:
                continue

            # SHAP toward true class
            shap_true = float(row.iloc[0][f"shap_{true_model}"])

            # byte vote: which class does this byte's SHAP favor?
            shap_vec = {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
            byte_vote_class = max(shap_vec, key=shap_vec.get)
            byte_vote_correct = (byte_vote_class == true_model)

            correct = bool(rec["correct"])
            predicted = rec.get("predicted", "?")

            py_path = get_py_path(stem, true_model)
            observed_opname, _, _, source_line = get_byte_info(py_path, target_fn, BYTE_POS)

            print(f"{task}/{rec['prompt']} ({true_model}={rec['run']})  "
                  f"file={rec['file']}  raw={observed_raw} ({observed_opname})")
            print(f"    true={true_model:8s} predicted={str(predicted):8s} "
                  f"overall_correct={'✓' if correct else '✗'}")
            print(f"    shap_toward_true={shap_true:+.3f}  "
                  f"byte_vote={byte_vote_class:8s} ({'✓' if byte_vote_correct else '✗'})")
            print(f"    source: {source_line}")
            print()

            out_rows.append({
                "task": task, "prompt": rec["prompt"], "run": rec["run"],
                "true": true_model, "predicted": predicted, "correct": correct,
                "raw_value": observed_raw, "opname": observed_opname,
                "shap_toward_true": shap_true,
                "byte_vote_class": byte_vote_class, "byte_vote_correct": byte_vote_correct,
                "source": source_line, "file": rec["file"],
            })

    out_df = pd.DataFrame(out_rows)
    raw_str = "-".join(str(rv) for rv in RAW_VALUES)
    out_file = ANALYSIS_DIR / f"byte{BYTE_POS}_value{raw_str}_scan.csv"
    out_df.to_csv(out_file, index=False)

    print("=" * 70)
    print(f"n={len(out_df)}")
    if not out_df.empty:
        print(f"SHAP toward true class: range {out_df['shap_toward_true'].min():+.3f} "
              f"to {out_df['shap_toward_true'].max():+.3f}, "
              f"mean {out_df['shap_toward_true'].mean():+.3f}")
        print(f"byte_vote correct: {out_df['byte_vote_correct'].sum()}/{len(out_df)}")
        print(f"overall correct:   {out_df['correct'].sum()}/{len(out_df)}")
        print(f"by true model:")
        print(out_df.groupby("true").size())
        print(f"by raw value:")
        print(out_df.groupby("raw_value").size())
    print(f"\nSaved to {out_file}")


if __name__ == "__main__":
    main()
