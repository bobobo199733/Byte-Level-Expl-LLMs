"""
byte_opcode_summary.py

Generalized version: deduplicates byte{N}_examples.csv down to unique
(task, prompt, <target_model>_run) combinations where <target_model>'s
byte_{N} == <target opcode>, and extracts the source line for all three
models at that byte position, for full three-way comparison.

Configure TARGET_BYTE, TARGET_MODEL, and TARGET_RAW below.

Run from the project root:
    python scripts/byte_opcode_summary.py
"""

import dis
import types
import json
from pathlib import Path
from xml.parsers.expat import model

import pandas as pd

# ── configurable ────────────────────────────────────────────────────────
TARGET_BYTE  = 18
TARGET_MODEL = "llama"
TARGET_RAW   = 72  # LOAD_GLOBAL
# ───────────────────────────────────────────────────────────────────────

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"
PROMPTS_DIR  = BASE_DIR / "test_data" / "prompts"
IN_FILE      = ANALYSIS_DIR / f"byte{TARGET_BYTE}_examples.csv"

CLASS_NAMES = ["llama", "mistral", "qwen"]

import sys
sys.path.insert(0, str(BASE_DIR / "scripts"))


# ══════════════════════════════════════════════════════════════════════════════
# Bytecode + source helpers
# ══════════════════════════════════════════════════════════════════════════════

def get_byte_vote(effects_df, byte_pos, true_model):
    """Returns True if this byte's SHAP values (across all 3 classes) favor true_model."""
    row = effects_df[effects_df["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return None
    shap_vec = {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
    top_class = max(shap_vec, key=shap_vec.get)
    return top_class == true_model


def file_to_bytecode_display(py_file: Path, target_fn: str) -> list[dict]:
    from bytecode_utils import extract_code, keep_only_defs, get_top_level_code_objects

    raw_text = py_file.read_text(encoding="utf-8")
    code     = keep_only_defs(extract_code(raw_text))
    compiled = compile(code, filename=str(py_file), mode="exec")

    top_level = get_top_level_code_objects(compiled)
    if target_fn not in top_level:
        raise ValueError(f"'{target_fn}' not found. Available: {sorted(top_level.keys())}")

    ordered_top = [top_level[target_fn]]
    for name in sorted(top_level.keys()):
        if name != target_fn:
            ordered_top.append(top_level[name])

    def walk(co, base_pos):
        pos = base_pos
        for instr in dis.get_instructions(co, show_caches=False):
            lineno = None
            if hasattr(instr, "positions") and instr.positions:
                lineno = instr.positions.lineno
            elif instr.starts_line is not None:
                lineno = instr.starts_line

            yield {
                "byte_pos": pos,
                "arg_pos":  pos + 1,
                "opname":   instr.opname,
                "arg_raw":  instr.arg if instr.arg is not None else 0,
                "argval":   str(instr.argval)[:60],
                "lineno":   lineno,
            }
            pos += 2

        for const in co.co_consts:
            if isinstance(const, types.CodeType):
                yield from walk(const, pos)
                pos += _count_instructions(const) * 2

    def _count_instructions(co):
        n = sum(1 for _ in dis.get_instructions(co, show_caches=False))
        for const in co.co_consts:
            if isinstance(const, types.CodeType):
                n += _count_instructions(const)
        return n

    rows = []
    pos  = 0
    for top_co in ordered_top:
        rows.extend(walk(top_co, pos))
        pos += _count_instructions(top_co) * 2

    return rows


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


def get_py_path(file_field, model):
    f = file_field
    return Path(f) if "/" in f else \
        BASE_DIR / "test_data" / "outputs" / model / "cleaned" / f


def get_target_fn(task_id):
    return json.loads(
        (PROMPTS_DIR / task_id / "meta.json").read_text(encoding="utf-8")
    )["function_name"]


def get_byte_info(py_path, target_fn, byte_pos):
    """Returns (opname, raw, argval, source_line) at byte_pos, or all-None on failure."""
    try:
        bc_rows = file_to_bytecode_display(py_path, target_fn)
        match = next(
            (r for r in bc_rows
             if r["byte_pos"] == byte_pos or r["arg_pos"] == byte_pos),
            None
        )
        if match is None:
            return None, None, None, None
        source_line = get_source_line(py_path, match["lineno"])
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
    df = pd.read_csv(IN_FILE)

    opname = dis.opname[TARGET_RAW]
    op_col   = f"{TARGET_MODEL}_op"
    raw_col  = f"{TARGET_MODEL}_raw"
    run_col  = f"{TARGET_MODEL}_run"

    subset = df[df[raw_col] == TARGET_RAW].copy()
    subset = subset.drop_duplicates(subset=["task", "prompt", run_col]).reset_index(drop=True)

    print(f"Found {len(subset)} unique {TARGET_MODEL} files with "
          f"byte_{TARGET_BYTE} = {opname}({TARGET_RAW})\n")

    out_file = ANALYSIS_DIR / f"byte{TARGET_BYTE}_{TARGET_MODEL}_{opname.lower()}_summary.csv"

    out_rows = []
    target_fn_cache = {}

    for _, row in subset.iterrows():
        task = row["task"]
        if task not in target_fn_cache:
            target_fn_cache[task] = get_target_fn(task)
        target_fn = target_fn_cache[task]

        out_row = {
            "task": task,
            "prompt": row["prompt"],
        }

        print(f"{task}/{row['prompt']}")

        for model in CLASS_NAMES:
            mrun_col  = f"{model}_run"
            mfile_col = f"{model}_file"
            mshap_col = f"{model}_shap"
            mcorr_col = f"{model}_correct"

            run  = row.get(mrun_col)
            file_field = row.get(mfile_col)
            shap = row.get(mshap_col)
            corr = row.get(mcorr_col)

            if pd.isna(file_field) if file_field is not None else True:
                file_field = None

            if file_field is None:
                print(f"    {model:7s}: no file recorded")
                out_row[f"{model}_run"]      = run
                out_row[f"{model}_op"]       = None
                out_row[f"{model}_raw"]      = None
                out_row[f"{model}_argval"]   = None
                out_row[f"{model}_source"]   = None
                out_row[f"{model}_shap"]     = shap
                out_row[f"{model}_correct"]  = corr
                out_row[f"{model}_byte_vote"] = None
                continue

            py_path = get_py_path(file_field, model)
            op, raw, argval, source_line = get_byte_info(py_path, target_fn, TARGET_BYTE)

            # load full effects row to compute byte vote (argmax of all 3 shap values)
            effects_path = ANALYSIS_DIR / task / f"{Path(file_field).stem}_effects.csv"
            byte_vote = None
            if effects_path.exists():
                effects_df = pd.read_csv(effects_path)
                erow = effects_df[effects_df["feature"] == f"byte_{TARGET_BYTE}"]
                if not erow.empty:
                    shap_vec = {c: float(erow.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}
                    top_class = max(shap_vec, key=shap_vec.get)
                    byte_vote = (top_class == model)

            out_row[f"{model}_run"]      = run
            out_row[f"{model}_op"]       = op
            out_row[f"{model}_raw"]      = raw
            out_row[f"{model}_argval"]   = argval
            out_row[f"{model}_source"]   = source_line
            out_row[f"{model}_shap"]     = shap
            out_row[f"{model}_correct"]  = corr
            out_row[f"{model}_byte_vote"] = byte_vote

            tick = "✓" if corr else ("✗" if pd.notna(corr) else "?")
            vote_tick = "✓" if byte_vote else ("✗" if byte_vote is not None else "?")
            shap_str = f"{shap:+.3f}" if pd.notna(shap) else "?"
            print(f"    {model:7s} ({run}): {str(op):22s} raw={raw!s:<6} "
                  f"shap={shap_str:>7}  correct={tick}  byte_vote={vote_tick}")
            print(f"             source: {source_line}")

        out_rows.append(out_row)
        print()

    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(out_file, index=False)
    print(f"Saved {len(out_df)} rows to {out_file}")

    shaps = out_df[f"{TARGET_MODEL}_shap"]
    n_correct = out_df[f"{TARGET_MODEL}_correct"].sum()
    n_byte_vote = out_df[f"{TARGET_MODEL}_byte_vote"].sum()
    print(f"\nSummary: n={len(out_df)}, {TARGET_MODEL} SHAP range "
          f"{shaps.min():+.3f} to {shaps.max():+.3f}, mean {shaps.mean():+.3f}, "
          f"{TARGET_MODEL} correct {n_correct}/{len(out_df)}, "
          f"{TARGET_MODEL} byte_vote {n_byte_vote}/{len(out_df)}")


if __name__ == "__main__":
    main()
