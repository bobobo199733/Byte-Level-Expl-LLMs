"""
bytecode_viz2.py

Visualizes source -> bytecode -> SHAP for a specific byte position.
Produces ONE compact figure per model (source window | bytecode window |
SHAP bar chart), suitable for stacking individually in a thesis.

Run with: python scripts/bytecode_viz2.py
"""

import dis
import types
import json
import pickle
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

# ── config ────────────────────────────────────────────────────────────────────
TASK_ID   = "t45"
PROMPT    = "p3"
BYTE_POS  = 16
EXPLICIT  = {
    "llama":   (PROMPT, "r1"),
    "mistral": (PROMPT, "r1"),
    "qwen":    (PROMPT, "r1"),
}

COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
FONT_FAMILY = "DejaVu Sans"
CLASS_NAMES = ["llama", "mistral", "qwen"]

SOURCE_WINDOW    = 4   # lines above/below the highlighted line to show
BYTECODE_WINDOW  = 5   # instructions above/below to show
SOURCE_MAX_CHARS = 46  # truncate long source lines to this many chars
ARGVAL_MAX_CHARS = 20  # truncate long argvals to this many chars
ROW_MAX_CHARS    = 48  # overall bytecode row width backstop

BASE_DIR    = Path(__file__).resolve().parent.parent
MODEL_FILE  = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"
OUT_DIR     = BASE_DIR / "analysis" / TASK_ID
PLOT_DIR    = BASE_DIR / "analysis" / TASK_ID / "bytecode_viz"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / "scripts"))


# ══════════════════════════════════════════════════════════════════════════════
# Bytecode extraction
# ══════════════════════════════════════════════════════════════════════════════

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
                "argval":   str(instr.argval)[:40],
                "lineno":   lineno,
                "co_name":  co.co_name,
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


def get_source_highlight_line(py_file, target_fn, byte_pos):
    try:
        rows = file_to_bytecode_display(py_file, target_fn)
        for r in rows:
            if r["byte_pos"] == byte_pos or r["arg_pos"] == byte_pos:
                return r["lineno"]
    except Exception:
        pass
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Record helpers
# ══════════════════════════════════════════════════════════════════════════════

def resolve_record(records, model, explicit_files):
    if explicit_files and model in explicit_files:
        p, r = explicit_files[model]
        match = [x for x in records
                 if x["true"] == model and x["prompt"] == p and x["run"] == r]
        if match:
            return match[0]
    fallback = [x for x in records if x["true"] == model]
    return fallback[0] if fallback else None


def get_py_path(rec, model):
    f = rec["file"]
    return Path(f) if "/" in f else \
        BASE_DIR / "test_data" / "outputs" / model / "cleaned" / f


def get_source(rec, model):
    try:
        return get_py_path(rec, model).read_text(encoding="utf-8").strip()
    except Exception:
        return f"# could not read {rec['file']}"


def get_shap_vals(rec, byte_pos):
    eff = rec["effects"]
    row = eff[eff["feature"] == f"byte_{byte_pos}"]
    if row.empty:
        return {c: 0.0 for c in CLASS_NAMES}
    return {c: float(row.iloc[0][f"shap_{c}"]) for c in CLASS_NAMES}


# ══════════════════════════════════════════════════════════════════════════════
# Drawing helpers
# ══════════════════════════════════════════════════════════════════════════════

def trunc(s, n):
    return s if len(s) <= n else s[:n - 1] + "…"


def draw_source_window(ax, source, color, highlight_lineno,
                        window=SOURCE_WINDOW, max_chars=SOURCE_MAX_CHARS):
    """Show only `window` lines above/below the highlighted line."""
    ax.set_facecolor("#fafafa")
    ax.axis("off")

    lines = source.split("\n")
    n     = len(lines)

    if highlight_lineno is None:
        lo, hi = 0, min(n - 1, 2 * window)
    else:
        center = highlight_lineno - 1  # 0-indexed
        lo = max(0, center - window)
        hi = min(n - 1, center + window)

    display_rows = []
    if lo > 0:
        display_rows.append(("dots", f"...  ({lo} lines above)"))
    for i in range(lo, hi + 1):
        line = trunc(lines[i], max_chars)
        display_rows.append(("line", i, line))
    if hi < n - 1:
        display_rows.append(("dots", f"...  ({n - hi - 1} lines below)"))

    n_rows = len(display_rows)
    line_h = min(0.10, 0.95 / max(n_rows, 1))

    for idx, item in enumerate(display_rows):
        y = 0.95 - idx * line_h
        if item[0] == "dots":
            ax.text(0.02, y, item[1], transform=ax.transAxes, fontsize=8,
                    color="#bbb", fontfamily="monospace", va="top",
                    fontstyle="italic", clip_on=True)
            continue

        i, line = item[1], item[2]
        hl = highlight_lineno is not None and (i + 1) == highlight_lineno
        if hl:
            ax.add_patch(mpatches.FancyBboxPatch(
                (0.005, y - line_h * 0.78), 0.99, line_h * 1.2,
                transform=ax.transAxes, boxstyle="round,pad=0.005",
                facecolor=color + "25", edgecolor=color,
                linewidth=1.2, zorder=1, clip_on=True
            ))
            lc, fw = color, "bold"
        else:
            lc, fw = "#333", "normal"
        ax.text(0.02, y, line, transform=ax.transAxes, fontsize=9,
                color=lc, fontfamily="monospace", va="top",
                fontweight=fw, clip_on=True, zorder=2)

    ax.add_patch(mpatches.FancyBboxPatch(
        (0, 0), 1, 1, transform=ax.transAxes,
        boxstyle="round,pad=0.01", linewidth=1.5,
        edgecolor=color, facecolor="none"
    ))


def draw_bytecode_window(ax, rows, byte_pos, color, window=BYTECODE_WINDOW,
                          argval_max_chars=ARGVAL_MAX_CHARS):
    ax.set_facecolor("#fafafa")
    ax.axis("off")

    target_idx = next(
        (i for i, r in enumerate(rows)
         if r["byte_pos"] == byte_pos or r["arg_pos"] == byte_pos),
        None
    )

    if target_idx is None:
        ax.text(0.5, 0.5, f"byte_{byte_pos} not found",
                ha="center", va="center", fontsize=8, color="#aaa",
                fontfamily="monospace", transform=ax.transAxes)
        ax.add_patch(mpatches.FancyBboxPatch(
            (0, 0), 1, 1, transform=ax.transAxes,
            boxstyle="round,pad=0.01", linewidth=1.5,
            edgecolor=color, facecolor="none"
        ))
        return

    lo = max(0, target_idx - window)
    hi = min(len(rows) - 1, target_idx + window)

    items = []
    if lo > 0:
        items.append(("dots", f"...  ({lo} instructions above)"))
    for i in range(lo, hi + 1):
        items.append(("row", rows[i]))
    if hi < len(rows) - 1:
        items.append(("dots", f"...  ({len(rows) - hi - 1} instructions below)"))

    n_rows = len(items)
    line_h = min(0.10, 0.95 / max(n_rows, 1))

    for idx, item in enumerate(items):
        y = 0.95 - idx * line_h
        if item[0] == "dots":
            ax.text(0.02, y, item[1], transform=ax.transAxes, fontsize=8,
                    color="#bbb", fontfamily="monospace", va="top",
                    fontstyle="italic", clip_on=True)
            continue

        r      = item[1]
        argval = r["argval"] if r["argval"] not in ("None", "") else ""
        argval = trunc(argval, argval_max_chars)
        is_hl  = (r["byte_pos"] == byte_pos or r["arg_pos"] == byte_pos)

        if is_hl:
            if r["byte_pos"] == byte_pos:
                raw_display = dis.opmap.get(r["opname"], "?")
            else:
                raw_display = r["arg_raw"]
            opname_with_raw = f"({raw_display}) {r['opname']}"
            opname_with_raw = trunc(opname_with_raw, 22)
            txt = f"{r['byte_pos']:>4}  {opname_with_raw:<22} {argval}"
        else:
            txt = f"{r['byte_pos']:>4}  {r['opname']:<22} {argval}"

        txt = trunc(txt, ROW_MAX_CHARS)

        if is_hl:
            ax.add_patch(mpatches.FancyBboxPatch(
                (0.005, y - line_h * 0.78), 0.99, line_h * 1.2,
                transform=ax.transAxes, boxstyle="round,pad=0.005",
                facecolor=color + "25", edgecolor=color,
                linewidth=1.2, zorder=1, clip_on=True
            ))
            lc, fw = color, "bold"
        else:
            lc, fw = "#555", "normal"

        ax.text(0.02, y, txt, transform=ax.transAxes, fontsize=9,
                color=lc, fontfamily="monospace", va="top",
                fontweight=fw, clip_on=True, zorder=2)

    ax.add_patch(mpatches.FancyBboxPatch(
        (0, 0), 1, 1, transform=ax.transAxes,
        boxstyle="round,pad=0.01", linewidth=1.5,
        edgecolor=color, facecolor="none"
    ))


def draw_shap_bars(ax, shap_vals, color):
    labels_r = CLASS_NAMES[::-1]
    vals_r   = [shap_vals[c] for c in labels_r]
    colors_r = [COLORS[c] for c in labels_r]
    bars = ax.barh(labels_r, vals_r, color=colors_r, alpha=0.85, height=0.5)
    ax.axvline(0, color="#888", linewidth=0.8)
    ax.set_xlabel("SHAP value", fontsize=9, color="#444")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#ccc")
    ax.spines["bottom"].set_color("#ccc")
    ax.tick_params(labelsize=9)
    ax.set_facecolor("#fafafa")

    max_abs = max((abs(v) for v in vals_r), default=1.0) or 1.0
    pad = max_abs * 0.25
    ax.set_xlim(-(max_abs + pad), max_abs + pad)
    ax.set_ylim(-0.6, len(labels_r) - 0.4)  # extra headroom for labels above bars

    for bar, val in zip(bars, vals_r):
        ax.text(val, bar.get_y() + bar.get_height() + 0.05,
                f"{val:+.3f}", ha="center", va="bottom",
                fontsize=8, color="#333")

    pos = ax.get_position()
    label_pad = 0.03  # fraction of figure width to reserve for labels
    ax.set_position([pos.x0 + label_pad, pos.y0, pos.width - label_pad, pos.height])


# ══════════════════════════════════════════════════════════════════════════════
# One figure per model
# ══════════════════════════════════════════════════════════════════════════════

def plot_single_model_flow(model, data, byte_pos, out_dir, file_stem):
    color = COLORS[model]

    fig = plt.figure(figsize=(13, 3.2))
    fig.patch.set_facecolor("white")
    gs = gridspec.GridSpec(1, 3, figure=fig,
                           width_ratios=[2.6, 2.6, 1.6], wspace=0.18)

    ax_src = fig.add_subplot(gs[0, 0])
    draw_source_window(ax_src, data["source"], color, data["hl"])

    ax_bc = fig.add_subplot(gs[0, 1])
    draw_bytecode_window(ax_bc, data["bc_rows"], byte_pos, color)

    ax_shap = fig.add_subplot(gs[0, 2])
    draw_shap_bars(ax_shap, data["shap_vals"], color)

    plt.tight_layout()
    out_path = out_dir / f"{file_stem}_byte{byte_pos}_flow.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    import shap
    from analyze_task_n import analyze_file

    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)
    clf       = loaded["model"] if isinstance(loaded, dict) else loaded
    report    = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
    features  = report["features"]
    explainer = shap.TreeExplainer(clf)

    target_fn = json.loads(
        (PROMPTS_DIR / TASK_ID / "meta.json").read_text(encoding="utf-8")
    )["function_name"]

    files = sorted((BASE_DIR / "test_data").rglob(f"{TASK_ID}_p*_r*_*.py"))
    print(f"Found {len(files)} files for {TASK_ID}")

    records = []
    for f in files:
        try:
            rec = analyze_file(f, clf, explainer, features, target_fn)
            records.append(rec)
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
    print(f"Loaded {len(records)} records")

    for model in CLASS_NAMES:
        rec = resolve_record(records, model, EXPLICIT)
        if rec is None:
            print(f"  no record for {model}")
            continue
        py_path = get_py_path(rec, model)
        try:
            bc_rows = file_to_bytecode_display(py_path, target_fn)
        except Exception as e:
            print(f"  bytecode error {model}: {e}")
            bc_rows = []

        hl = get_source_highlight_line(py_path, target_fn, BYTE_POS)
        data = {
            "source":    get_source(rec, model),
            "bc_rows":   bc_rows,
            "shap_vals": get_shap_vals(rec, BYTE_POS),
            "hl":        hl,
        }

        file_stem = Path(rec["file"]).stem
        plot_single_model_flow(model, data, BYTE_POS, PLOT_DIR, file_stem)


if __name__ == "__main__":
    main()
