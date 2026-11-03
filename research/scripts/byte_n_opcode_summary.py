"""
byte_full_population_sources.py

For a given (byte_pos, model, raw_opcode / range / list), scans ALL
test files for that model (no filtering), and for each instance where
byte_pos matches one of the target opcodes, extracts the source line +
the corresponding llama/mistral/qwen comparison at that byte position.

Configure TARGET_BYTE, TARGET_MODEL, and ONE of TARGET_RAW,
TARGET_RAW_RANGE, or TARGET_RAW_LIST below.

Run from the project root:
    python scripts/byte_full_population_sources.py
"""

import dis
import types
import json
from pathlib import Path

import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
PROMPTS_DIR  = BASE_DIR / "test_data" / "prompts"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]

# ── configure ────────────────────────────────────────────────────────
TARGET_BYTE  = 54
TARGET_MODEL = "mistral"

TARGET_RAW        = 91          # single opcode,   e.g. 53
TARGET_RAW_RANGE  = None    # inclusive range, e.g. (100, 255)
TARGET_RAW_LIST   = None          # explicit list,   e.g. [100, 110, 115]
# ───────────────────────────────────────────────────────────────────

import sys
sys.path.insert(0, str(BASE_DIR / "scripts"))


def _resolve_targets():
    """Resolve configure flags into a set of raw values and a filename label."""
    if TARGET_RAW_LIST is not None:
        raw_set = set(TARGET_RAW_LIST)
        label   = "-".join(str(v) for v in sorted(raw_set))
    elif TARGET_RAW_RANGE is not None:
        lo, hi  = TARGET_RAW_RANGE
        # skip unassigned opcode slots (e.g. <119>..<148>)
        raw_set = {v for v in range(lo, hi + 1)
                   if not dis.opname[v].startswith("<")}
        label   = f"range{lo}-{hi}"
    elif TARGET_RAW is not None:
        raw_set = {TARGET_RAW}
        label   = str(TARGET_RAW)
    else:
        raise ValueError(
            "Set exactly one of TARGET_RAW, TARGET_RAW_RANGE, or TARGET_RAW_LIST.")
    return raw_set, label


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


def get_effects(task, stem):
    path = ANALYSIS_DIR / task / f"{stem}_effects.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    raw_set, label = _resolve_targets()

    # human-readable description for print output
    if len(raw_set) == 1:
        rv           = next(iter(raw_set))
        opname_label = f"{dis.opname[rv]}({rv})"
        file_label   = dis.opname[rv].lower()
    else:
        names        = sorted({dis.opname[rv] for rv in raw_set
                                if not dis.opname[rv].startswith("<")})
        opname_label = (f"{len(raw_set)} opcodes: "
                        + ", ".join(names[:5])
                        + ("..." if len(names) > 5 else ""))
        file_label   = label

    print(f"byte_{TARGET_BYTE} matching {{{opname_label}}} "
          f"in {TARGET_MODEL} files\n")

    target_fn_cache = {}
    out_rows        = []

    for task in TASKS:
        summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
        if not summary_path.exists():
            continue
        summary = pd.read_csv(summary_path)

        if task not in target_fn_cache:
            target_fn_cache[task] = get_target_fn(task)
        target_fn = target_fn_cache[task]

        for _, rec in summary[summary["true"] == TARGET_MODEL].iterrows():
            stem = Path(rec["file"]).stem
            eff  = get_effects(task, stem)
            if eff is None:
                continue
            row = eff[eff["feature"] == f"byte_{TARGET_BYTE}"]
            if row.empty:
                continue
            observed_raw = int(row.iloc[0]["value"])
            if observed_raw not in raw_set:
                continue

            prompt = rec["prompt"]
            run    = rec["run"]

            print(f"{task}/{prompt}  ({TARGET_MODEL}={run})  "
                  f"raw={observed_raw} ({dis.opname[observed_raw]})")
            out_row = {
                "task":             task,
                "prompt":           prompt,
                f"{TARGET_MODEL}_run": run,
                "observed_raw":     observed_raw,
                "observed_opname":  dis.opname[observed_raw],
            }

            for model in CLASS_NAMES:
                if model == TARGET_MODEL:
                    mrec  = rec
                    mstem = stem
                    meff  = eff
                else:
                    mrows = summary[
                        (summary["true"] == model) &
                        (summary["prompt"] == prompt)
                    ]
                    if mrows.empty:
                        print(f"    {model:7s}: no file for this prompt")
                        continue
                    mrec  = mrows.iloc[0]
                    mstem = Path(mrec["file"]).stem
                    meff  = get_effects(task, mstem)

                py_path = get_py_path(mstem, model)
                op, raw, argval, source_line = get_byte_info(
                    py_path, target_fn, TARGET_BYTE)

                shap_val = None
                if meff is not None:
                    mrow = meff[meff["feature"] == f"byte_{TARGET_BYTE}"]
                    if not mrow.empty:
                        shap_val = float(mrow.iloc[0][f"shap_{model}"])

                correct  = bool(mrec["correct"])
                tick     = "✓" if correct else "✗"
                shap_str = f"{shap_val:+.3f}" if shap_val is not None else "?"
                print(f"    {model:7s} ({mrec['run']}): {str(op):22s} "
                      f"raw={raw!s:<6} shap={shap_str:>7}  correct={tick}")
                print(f"             source: {source_line}")

                out_row[f"{model}_run"]     = mrec["run"]
                out_row[f"{model}_op"]      = op
                out_row[f"{model}_raw"]     = raw
                out_row[f"{model}_source"]  = source_line
                out_row[f"{model}_shap"]    = shap_val
                out_row[f"{model}_correct"] = correct
                out_row[f"{model}_file"]    = mrec["file"]

            out_rows.append(out_row)
            print()

    out_df   = pd.DataFrame(out_rows)
    out_file = ANALYSIS_DIR / \
        f"byte{TARGET_BYTE}_{TARGET_MODEL}_{file_label}_full_sources.csv"
    out_df.to_csv(out_file, index=False)
    print(f"Saved {len(out_df)} rows to {out_file}")

    if not out_df.empty:
        shap_col = f"{TARGET_MODEL}_shap"
        if shap_col in out_df.columns:
            shaps = out_df[shap_col].dropna()
            n_cor = out_df[f"{TARGET_MODEL}_correct"].sum()
            print(f"\nSummary: n={len(out_df)}, SHAP range "
                  f"{shaps.min():+.3f} to {shaps.max():+.3f}, "
                  f"mean {shaps.mean():+.3f}, "
                  f"correct {n_cor}/{len(out_df)}")
        print("\nBy observed opcode:")
        print(out_df.groupby(["observed_raw", "observed_opname"])
              .size().rename("n").to_string())


if __name__ == "__main__":
    main()
