"""
bytecode_snippet.py  —  dis.dis()-style listing, caches stripped, truncated for thesis

Usage:
    python bytecode_snippet.py myfile.py --fn group_anagrams --n 20
    python bytecode_snippet.py myfile.py --fn group_anagrams --n 20 --out figure.pdf
"""

import argparse
import dis
import types
from pathlib import Path


def disassemble_lines(co, indent=0) -> list[str]:
    """
    Reproduce dis.dis() text output with show_caches=False.
    Recursively handles nested code objects.
    """
    lines  = []
    prefix = "  " * indent
    prev_lineno = None

    for instr in dis.get_instructions(co, show_caches=False):
        # --- line number column (leftmost, like dis.dis) ---
        lineno = None
        if hasattr(instr, "positions") and instr.positions:
            lineno = instr.positions.lineno
        elif instr.starts_line is not None:
            lineno = instr.starts_line

        if lineno is not None and lineno != prev_lineno:
            lno_str = f"{lineno:>3}"
            prev_lineno = lineno
        else:
            lno_str = "   "

        # --- offset ---
        offset_str = f"{instr.offset:>6}"

        # --- opname ---
        op_str = f"{instr.opname:<24}"

        # --- arg + argval ---
        if instr.arg is not None:
            arg_str = f"{instr.arg:<5}"
            av = str(instr.argval) if instr.argval not in (None, instr.arg, "") else ""
            argval_str = f" ({av})" if av else ""
        else:
            arg_str    = "     "
            argval_str = ""

        lines.append(f"{prefix}{lno_str}  {offset_str}  {op_str} {arg_str}{argval_str}")

    # recurse into nested code objects (same order as dis.dis)
    for const in co.co_consts:
        if isinstance(const, types.CodeType):
            lines.append(f"")
            lines.append(f"{prefix}Disassembly of {const}:")
            lines.extend(disassemble_lines(const, indent=indent))

    return lines


def get_code_object(py_file, fn_name):
    source   = py_file.read_text(encoding="utf-8")
    compiled = compile(source, filename=str(py_file), mode="exec")
    if fn_name is None:
        return compiled
    for c in compiled.co_consts:
        if isinstance(c, types.CodeType) and c.co_name == fn_name:
            return c
    available = [c.co_name for c in compiled.co_consts if isinstance(c, types.CodeType)]
    raise ValueError(f"'{fn_name}' not found. Available: {available}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--fn",  default=None,  help="Function name (omit for whole module)")
    ap.add_argument("--n",   type=int, default=None, help="Max instructions to show")
    ap.add_argument("--out", default=None,  help="Output file (.txt, .pdf, .svg, .png)")
    args = ap.parse_args()

    py_file = Path(args.file)
    co      = get_code_object(py_file, args.fn)
    lines   = disassemble_lines(co)

    # truncate instruction lines only (skip blank / "Disassembly of" lines)
    if args.n is not None:
        kept, instr_count, truncated_at = [], 0, None
        for i, l in enumerate(lines):
            stripped = l.strip()
            is_instr = stripped and not stripped.startswith("Disassembly")
            if is_instr:
                if instr_count >= args.n:
                    truncated_at = i
                    break
                instr_count += 1
            kept.append(l)
        if truncated_at is not None:
            remaining = sum(
                1 for l in lines[truncated_at:]
                if l.strip() and not l.strip().startswith("Disassembly")
            )
            kept.append(f"        ... ({remaining} more instruction{'s' if remaining != 1 else ''})")
        lines = kept

    text = "\n".join(lines)

    if args.out is None:
        print(text)
        return

    # ── render to image/pdf ─────────────────────────────────────────────────
    import matplotlib.pyplot as plt

    out     = Path(args.out)
    fmt     = out.suffix.lstrip(".") or "pdf"
    n_lines = len(lines)
    max_len = max((len(l) for l in lines), default=40)

    fig_w = max(6.0, max_len * 0.068 + 0.4)
    fig_h = max(2.0, n_lines * 0.19 + 0.4)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    for i, line in enumerate(lines):
        y       = 1.0 - (i + 0.5) / n_lines
        is_meta = line.strip().startswith("Disassembly") or line.strip() == ""
        is_dots = line.strip().startswith("...")
        color   = "#888" if is_meta else ("#aaa" if is_dots else "#111")
        style   = "italic" if (is_meta or is_dots) else "normal"
        ax.text(0.01, y, line, transform=ax.transAxes,
                fontsize=8, fontfamily="monospace",
                color=color, va="center", fontstyle=style)

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(out, bbox_inches="tight", facecolor="white", format=fmt, dpi=250)
    plt.close()
    print(f"Saved → {out}")


if __name__ == "__main__":
    main()
