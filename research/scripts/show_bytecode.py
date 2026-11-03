"""
show_bytecode.py

Shows bytecode exactly as the feature extraction pipeline sees it.
Uses collect_ordered_script_bytes from bytecode_utils directly.

Usage:
    python scripts/show_bytecode.py t41_p1_r1_llama.py
    python scripts/show_bytecode.py t41_p1_r1_llama.py --highlight 69
    python scripts/show_bytecode.py t41_p1_r1_llama.py t41_p1_r1_mistral.py --highlight 69
    python scripts/show_bytecode.py t41_p1_r1_llama.py --highlight 69 --show-cache
"""

import sys
import dis
import types
import opcode as opcode_module
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))


def get_bytecode_rows(py_file: Path, target_fn: str) -> list[dict]:
    """
    Calls extract_script_bytecode to get the flat byte list — identical to the
    feature extraction pipeline. Then enriches each byte pair with opname/argval/lineno.
    """
    from bytecode_utils import (
        extract_script_bytecode, extract_code, keep_only_defs,
        get_top_level_code_objects
    )

    # get the flat byte list exactly as the pipeline does
    byte_values, _ = extract_script_bytecode(py_file, target_fn)

    # also get dis metadata (argval, lineno) — needs same traversal order
    raw_text = py_file.read_text(encoding="utf-8")
    code     = keep_only_defs(extract_code(raw_text))
    compiled = compile(code, filename=str(py_file), mode="exec")

    top_level = get_top_level_code_objects(compiled)
    ordered_top = [top_level[target_fn]]
    for name in sorted(top_level.keys()):
        if name != target_fn:
            ordered_top.append(top_level[name])

    # build lookup: flat_position -> dis instruction metadata
    def collect_instrs(co):
        result = []
        for instr in dis.get_instructions(co, show_caches=True):
            result.append((co, instr))
        for const in co.co_consts:
            if isinstance(const, types.CodeType):
                result.extend(collect_instrs(const))
        return result

    all_instrs = []
    for top_co in ordered_top:
        all_instrs.extend(collect_instrs(top_co))

    # now pair each 2-byte entry in byte_values with its dis metadata
    rows = []
    for i, (co, instr) in enumerate(all_instrs):
        pos = i * 2
        if pos + 1 >= len(byte_values):
            break

        op_val  = byte_values[pos]
        arg_val = byte_values[pos + 1]
        opname  = opcode_module.opname[op_val]

        lineno = None
        if hasattr(instr, "positions") and instr.positions:
            lineno = instr.positions.lineno
        elif instr.starts_line is not None:
            lineno = instr.starts_line

        rows.append({
            "byte_pos": pos,
            "arg_pos":  pos + 1,
            "op_val":   op_val,
            "arg_val":  arg_val,
            "opname":   opname,
            "argval":   str(instr.argval)[:40],
            "lineno":   lineno,
            "co_name":  co.co_name,
        })

    return rows


def print_bytecode(rows, filename, highlight_pos=None):
    print(f"\n{'='*75}")
    print(f"  {filename}  ({len(rows)} instructions, {len(rows)*2} bytes)")

    if highlight_pos is not None:
        match = next((r for r in rows
                      if r["byte_pos"] == highlight_pos or r["arg_pos"] == highlight_pos), None)
        if match:
            kind = "opcode" if match["byte_pos"] == highlight_pos else "arg"
            print(f"  byte_{highlight_pos} → {kind} of {match['opname']}  "
                  f"argval={match['argval']}  raw={match['arg_val']}")
        else:
            print(f"  byte_{highlight_pos} NOT FOUND")

    print(f"{'='*75}")
    print(f"  {'pos':>5}  {'opname':<26} {'argval':<38}  line  co")
    print(f"  {'-'*5}  {'-'*26} {'-'*38}  ----  --")

    for r in rows:
        is_hl  = highlight_pos is not None and (
            r["byte_pos"] == highlight_pos or r["arg_pos"] == highlight_pos
        )
        marker = ">>>" if is_hl else "   "
        lineno = str(r["lineno"]) if r["lineno"] else ""
        argval = r["argval"] if r["argval"] not in ("None", "") else ""
        print(f"  {marker} {r['byte_pos']:>4}  {r['opname']:<26} {argval:<38}  "
              f"{lineno:<4}  {r['co_name']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="File names e.g. t41_p1_r1_llama.py")
    parser.add_argument("--highlight", type=int, default=None,
                        help="Byte position to highlight")
    args = parser.parse_args()

    for fname in args.files:
        candidates = list(BASE_DIR.rglob(fname))
        if not candidates:
            print(f"File not found: {fname}")
            continue
        py_file = candidates[0]

        parts = py_file.stem.split("_")
        task  = parts[0]

        meta_path = BASE_DIR / "test_data" / "prompts" / task / "meta.json"
        if not meta_path.exists():
            meta_path = BASE_DIR / "prompts" / task / "meta.json"
        if not meta_path.exists():
            print(f"No meta.json for task {task}")
            continue

        target_fn = json.loads(meta_path.read_text())["function_name"]

        try:
            rows = get_bytecode_rows(py_file, target_fn)
            print_bytecode(rows, py_file.name, highlight_pos=args.highlight)
        except Exception as e:
            print(f"Error: {e}")
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
