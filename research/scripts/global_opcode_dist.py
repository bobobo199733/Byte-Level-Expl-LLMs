"""
plot_global_opcode_distribution.py

Plots opcode distribution at top SHAP byte positions across ALL test tasks.
Each subplot = one byte position. Stacked bars show opcode fractions per model.

Run from project root:
    python scripts/plot_global_opcode_distribution.py
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import opcode as opcode_module

BASE_DIR     = Path(__file__).resolve().parent.parent
SHAP_DIR     = BASE_DIR / "shap_bytecode"
FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
OUT_DIR      = SHAP_DIR / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / "scripts"))

CLASS_NAMES      = ["llama", "mistral", "qwen"]
TOP_OPS_PER_BYTE = 8
N_COLS           = 4
SHOW_TITLES = False  # set True for dev/debugging; keep False for thesis figures

# font sizes
FS_TITLE   = 20
FS_SUBTITLE = 18
FS_TICK    = 18
FS_LABEL   = 18
FS_LEGEND  = 14
FS_ANNOT   = 17

# ── SHAP-based byte selection ────────────────────────────────────────────────
SHAP_VALUES_FILE   = SHAP_DIR / "shap_values_multiclass.npy"
FEATURE_NAMES_FILE = SHAP_DIR / "feature_names.json"
CLASS_NAMES_FILE   = SHAP_DIR / "class_names.json"

TOP_N_BYTES = 8


def opname_for(val):
    if val == -1:
        return "PAD"
    try:
        name = opcode_module.opname[int(val)]
        return name if name != "<?>" else f"op_{int(val)}"
    except Exception:
        return f"op_{val}"


def opname_label(opname):
    raw = opcode_module.opmap.get(opname)
    return f"{opname} ({raw})" if raw is not None else opname


# Academic/publication-friendly palette
DISTINCT_PALETTE = [
    "#004D99",  # dark blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#D55E00",  # vermillion
    "#CC79A7",  # magenta
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#4E79A7",  # muted blue
    "#F28E2B",  # muted orange
    "#E15759",  # muted red
    "#76B7B2",  # teal
    "#59A14F",  # dark green
    "#984EA3",  # deep purple
    "#FF9DA7",  # salmon
    "#9C755F",  # brown
    "#BAB0AC",  # gray
    "#7F7F7F",  # dark gray
]
OPNAME_COLORS = {}  # unused, kept for compatibility

OPNAME_COLORS = {}  # unused, kept for compatibility

PINNED_OPCODE_COLORS = {
    # blues
    "BINARY_OP":              "#1F4E79",  # dark navy
    "LOAD_CONST":             "#6E8FB0",  # slate blue
    "GET_ITER":               "#6FB7E8",  # sky blue
    # greens (kept distinct from each other)
    "CALL":                   "#2CA858",  # teal-green
    "LOAD_GLOBAL":            "#8FBFB5",  # sage/gray-teal
    "POP_JUMP_IF_FALSE":      "#7C9C4A",  # olive green
    "SET_FUNCTION_ATTRIBUTE": "#5E3C99",  # deep violet
    # oranges / reds
    "LOAD_FAST":              "#F4A03C",  # muted orange
    "BUILD_LIST":             "#E8B400",  # gold
    "COMPARE_OP":             "#D2691E",  # burnt orange
    "LOAD_FAST_LOAD_FAST":    "#E0635C",  # salmon red
    # pinks / mauves
    "STORE_FAST":             "#F2A0B8",  # bright pink
    "FOR_ITER":               "#C97B9C",  # mauve/rose
    "STORE_FAST_STORE_FAST":  "#9C7A54",  # brown
    # purples
    "RAISE_VARARGS":          "#B07AA1",  # light purple
    # yellow
    "LOAD_ATTR":              "#F5E642",  # yellow
    # grays/browns
    "POP_TOP":                "#A89B91",  # gray-brown
    "TO_BOOL":                "#C9BDB5",  # light tan
}


def assign_colors(all_opnames, palette):
    """Assign colors to opnames: pinned colors first, palette for the rest."""
    color_map = {}
    used_colors = set(PINNED_OPCODE_COLORS.values())
    available = [c for c in palette if c not in used_colors]
    pi = 0
    for op in sorted(all_opnames):
        if op in PINNED_OPCODE_COLORS:
            color_map[op] = PINNED_OPCODE_COLORS[op]
        else:
            color_map[op] = available[pi % len(available)]
            pi += 1
    return color_map


def build_global_color_map(all_opnames):
    """Assign colors to opnames: pinned colors first, palette for the rest."""
    palette = [c for c in DISTINCT_PALETTE if c != "#fffac8"]  # skip beige
    color_map = assign_colors(all_opnames, palette)
    color_map["other"] = "#dddddd"
    return color_map


def get_class_shap_values(shap_values, class_index: int):
    if isinstance(shap_values, list):
        return shap_values[class_index]
    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_index]
    raise ValueError(f"Unexpected SHAP values shape/type: {type(shap_values)}")


def compute_top_even_bytes(top_n=TOP_N_BYTES):
    """
    Compute the top_n most important even-indexed byte positions,
    ranked by mean |SHAP| summed across all classes.
    """
    shap_values = np.load(SHAP_VALUES_FILE, allow_pickle=True)
    if isinstance(shap_values, np.ndarray) and shap_values.dtype == object and shap_values.shape == ():
        shap_values = shap_values.item()

    feature_names = json.loads(FEATURE_NAMES_FILE.read_text(encoding="utf-8"))
    class_names   = json.loads(CLASS_NAMES_FILE.read_text(encoding="utf-8"))

    per_class_importance = np.array([
        np.abs(get_class_shap_values(shap_values, ci)).mean(axis=0)
        for ci in range(len(class_names))
    ])  # shape: (n_classes, n_features)
    total_importance = per_class_importance.sum(axis=0)  # shape: (n_features,)

    # map feature -> byte index, keep only even-indexed bytes
    byte_importance = {}
    for feat, imp in zip(feature_names, total_importance):
        if not feat.startswith("byte_"):
            continue
        byte_idx = int(feat.replace("byte_", ""))
        if byte_idx % 2 != 0:
            continue
        byte_importance[byte_idx] = imp

    ranked = sorted(byte_importance.items(), key=lambda kv: kv[1], reverse=True)
    top_bytes = [byte_idx for byte_idx, _ in ranked[:top_n]]
    print(f"  Top {top_n} even-indexed bytes by global SHAP importance: {top_bytes}")
    return top_bytes


def main():
    print("Loading features...")
    df = pd.read_csv(FEATURES_CSV)
    print(f"  {len(df)} files, {len(df.columns)} columns")

    top_bytes = compute_top_even_bytes()
    print(f"  Using computed bytes: {top_bytes}")

    # ── first pass: collect all opnames to build global color map ────────────
    all_opnames = set()
    byte_data   = {}
    for byte_pos in top_bytes:
        col = f"byte_{byte_pos}"
        if col not in df.columns:
            continue
        sub = df[["model", col]].copy()
        sub["opname"] = sub[col].apply(opname_for)
        sub = sub[sub["opname"] != "PAD"]
        if sub.empty:
            continue
        top_ops = sub["opname"].value_counts().head(TOP_OPS_PER_BYTE).index.tolist()
        sub["display"] = sub["opname"].apply(lambda x: x if x in top_ops else "other")
        all_opnames.update(top_ops)
        byte_data[byte_pos] = {"sub": sub, "top_ops": top_ops}

    color_map = build_global_color_map(all_opnames)

    # ── plot ──────────────────────────────────────────────────────────────────
    n_rows = (len(top_bytes) + N_COLS - 1) // N_COLS
    fig, axes = plt.subplots(n_rows, N_COLS,
                             figsize=(N_COLS * 3.2, n_rows * 4 + 1),
                             squeeze=False)
    axes = axes.flatten()

    if SHOW_TITLES:
        fig.suptitle(
            "Opcode distribution at top SHAP byte positions — all test tasks combined\n"
            "Each bar shows fraction of files per model with that opcode at that position",
            fontsize=FS_TITLE, y=1.01
        )

    plotted = []
    for i, byte_pos in enumerate(top_bytes):
        ax = axes[i]
        if byte_pos not in byte_data:
            ax.set_visible(False)
            continue

        sub     = byte_data[byte_pos]["sub"]
        top_ops = byte_data[byte_pos]["top_ops"]
        display_order = top_ops + (["other"] if (sub["display"] == "other").any() else [])

        bottoms = np.zeros(len(CLASS_NAMES))
        x       = np.arange(len(CLASS_NAMES))

        for op in display_order:
            heights = []
            for model in CLASS_NAMES:
                msub  = sub[sub["model"] == model]
                total = len(msub)
                pct   = (msub["display"] == op).sum() / total if total else 0
                heights.append(pct)
            ax.bar(x, heights, bottom=bottoms,
                   color=color_map.get(op, "#dddddd"), alpha=0.88)
            bottoms += np.array(heights)
            if op not in [p[0] for p in plotted]:
                plotted.append((op, color_map.get(op, "#dddddd")))

        ax.set_xticks(x)
        ax.set_xticklabels(CLASS_NAMES, fontsize=FS_TICK, rotation=20)
        ax.set_title(f"byte_{byte_pos}", fontsize=FS_SUBTITLE, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i % N_COLS == 0:
            ax.set_ylabel("fraction of files", fontsize=FS_LABEL)

    for i in range(len(top_bytes), len(axes)):
        axes[i].set_visible(False)

    # ── single shared legend with unique entries ──────────────────────────────
    # sort by opname, "other" last
    plotted_sorted = sorted([p for p in plotted if p[0] != "other"], key=lambda x: x[0])
    if any(p[0] == "other" for p in plotted):
        plotted_sorted.append(("other", "#cccccc"))

    handles = [mpatches.Patch(color=c, alpha=0.88,
                               label=opname_label(op) if op != "other" else "other")
               for op, c in plotted_sorted]

    fig.legend(handles=handles,
               loc="lower center", fontsize=FS_LEGEND,
               ncol=min(len(handles), 4),
               bbox_to_anchor=(0.5, -0.18), framealpha=0.9)

    plt.tight_layout()
    out_path = OUT_DIR / "global_opcode_distribution_opnames.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"\nSaved {out_path}")

    # second plot: top-3 most persistent opcodes per model per byte
    plot_top3_persistent(df, top_bytes)

    # third plot: divergent opcodes highlighted, consensus grayed out
    plot_divergence_highlighted(df, top_bytes, color_map)


def plot_top3_persistent(df, top_bytes):
    """For each byte position, show the top-3 most common opcodes per model
    as grouped bars. One group per model, three bars per group."""

    n_rows = (len(top_bytes) + N_COLS - 1) // N_COLS
    fig, axes = plt.subplots(n_rows, N_COLS,
                             figsize=(N_COLS * 3.8, n_rows * 4 + 1),
                             squeeze=False)
    axes = axes.flatten()

    if SHOW_TITLES:
        fig.suptitle(
            "Top-3 most frequent opcodes per model at top SHAP byte positions\n"
            "Each group = one model; bars show fraction of files with that opcode",
            fontsize=FS_TITLE, y=1.01
        )

    # collect all top-3 opnames across all bytes/models for global color map
    all_top3 = set()
    top3_data = {}
    for byte_pos in top_bytes:
        col = f"byte_{byte_pos}"
        if col not in df.columns:
            continue
        sub = df[["model", col]].copy()
        sub["opname"] = sub[col].apply(opname_for)
        sub = sub[sub["opname"] != "PAD"]
        if sub.empty:
            continue
        per_model = {}
        for model in CLASS_NAMES:
            msub = sub[sub["model"] == model]
            top3 = msub["opname"].value_counts().head(3)
            per_model[model] = top3
            all_top3.update(top3.index.tolist())
        top3_data[byte_pos] = per_model

    palette = DISTINCT_PALETTE
    color_map = assign_colors(all_top3, palette)

    plotted = []
    x_base  = np.arange(len(CLASS_NAMES))
    width   = 0.25

    for i, byte_pos in enumerate(top_bytes):
        ax = axes[i]
        if byte_pos not in top3_data:
            ax.set_visible(False)
            continue

        per_model = top3_data[byte_pos]

        for m_idx, model in enumerate(CLASS_NAMES):
            top3  = per_model[model]
            total = len(df[df["model"] == model])
            for rank, (opname, count) in enumerate(top3.items()):
                frac = count / total
                x    = m_idx + (rank - 1) * width
                ax.bar(x, frac, width=width * 0.9,
                       color=color_map.get(opname, "#dddddd"), alpha=0.88)
                if opname not in [p[0] for p in plotted]:
                    plotted.append((opname, color_map[opname]))

        ax.set_xticks(x_base)
        ax.set_xticklabels(CLASS_NAMES, fontsize=FS_TICK, rotation=20)
        ax.set_title(f"byte_{byte_pos}", fontsize=FS_SUBTITLE, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i % N_COLS == 0:
            ax.set_ylabel("fraction of files", fontsize=FS_LABEL)

    for i in range(len(top_bytes), len(axes)):
        axes[i].set_visible(False)

    plotted_sorted = sorted(plotted, key=lambda x: x[0])
    handles = [mpatches.Patch(color=c, alpha=0.88, label=opname_label(op))
               for op, c in plotted_sorted]
    fig.legend(handles=handles,
               loc="lower center", fontsize=FS_LEGEND,
               ncol=min(len(handles), 4),
               bbox_to_anchor=(0.5, -0.12), framealpha=0.9)

    plt.tight_layout()
    out_path = OUT_DIR / "global_opcode_top3_persistent.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path}")


def plot_divergence_highlighted(df, top_bytes, color_map, min_presence=0.30, max_absence=0.08):
    # scan ALL opcodes at each byte position
    # normalize each opcode's distribution across models, rank by spread
    # plot original fractions for divergent opcodes only
    n_rows = (len(top_bytes) + N_COLS - 1) // N_COLS
    fig, axes = plt.subplots(n_rows, N_COLS,
                             figsize=(N_COLS * 3.2, n_rows * 4 + 1),
                             squeeze=False)
    axes = axes.flatten()

    if SHOW_TITLES:
        fig.suptitle(
            "Divergent opcode distribution at top SHAP byte positions\n"
            f"Opcodes selected by normalized spread >= {min_presence:.0%} across models (min 5% presence)",
            fontsize=FS_TITLE, y=1.01
        )

    # build a global color map across all divergent opnames
    all_divergent = set()
    byte_div_data = {}
    for byte_pos in top_bytes:
        col = f"byte_{byte_pos}"
        if col not in df.columns:
            continue
        sub = df[["model", col]].copy()
        sub["opname"] = sub[col].apply(opname_for)
        sub = sub[sub["opname"] != "PAD"]
        if sub.empty:
            continue
        all_ops = sub["opname"].unique().tolist()
        fracs = {}
        for op in all_ops:
            heights = []
            for model in CLASS_NAMES:
                msub  = sub[sub["model"] == model]
                total = len(msub)
                heights.append((msub["opname"] == op).sum() / total if total else 0)
            fracs[op] = heights

        # normalize each opcode's fractions across models to [0,1]
        # so rare and common opcodes are judged equally on divergence
        # then pick divergent ones by normalized spread, plot original fracs
        divergent = {}
        for op, heights in fracs.items():
            total_presence = sum(heights)
            if total_presence == 0:
                continue
            normalized = [h / total_presence for h in heights]
            spread = max(normalized) - min(normalized)
            if spread >= min_presence and max(heights) >= 0.05:  # must appear in at least 5% somewhere
                divergent[op] = heights
        all_divergent.update(divergent.keys())
        byte_div_data[byte_pos] = {"sub": sub, "divergent": divergent}

    div_color_map = assign_colors(all_divergent, DISTINCT_PALETTE)

    plotted = []
    for i, byte_pos in enumerate(top_bytes):
        ax = axes[i]
        if byte_pos not in byte_div_data:
            ax.set_visible(False)
            continue

        divergent = byte_div_data[byte_pos]["divergent"]
        if not divergent:
            ax.set_visible(False)
            continue

        # sort divergent ops by total spread descending
        sorted_ops = sorted(divergent.keys(),
                            key=lambda op: max(divergent[op]) - min(divergent[op]),
                            reverse=True)

        bottoms = np.zeros(len(CLASS_NAMES))
        x       = np.arange(len(CLASS_NAMES))

        for op in sorted_ops:
            heights = divergent[op]
            c = div_color_map.get(op, "#dddddd")
            ax.bar(x, heights, bottom=bottoms, color=c, alpha=0.88)
            bottoms += np.array(heights)
            if op not in [p[0] for p in plotted]:
                plotted.append((op, c))

        ax.set_xticks(x)
        ax.set_xticklabels(CLASS_NAMES, fontsize=FS_TICK, rotation=20)
        ax.set_title(f"byte_{byte_pos}", fontsize=FS_SUBTITLE, fontweight="bold")
        ax.set_ylim(0, max(bottoms) * 1.15 + 0.05)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if i % N_COLS == 0:
            ax.set_ylabel("fraction of files", fontsize=FS_LABEL)

    for i in range(len(top_bytes), len(axes)):
        axes[i].set_visible(False)

    plotted_sorted = sorted(plotted, key=lambda x: x[0])
    if not plotted_sorted:
        print("  WARNING: no divergent opcodes found — try lowering min_presence or raising max_absence")
        plt.close()
        return
    handles = [mpatches.Patch(color=c, alpha=0.88, label=opname_label(op))
               for op, c in plotted_sorted]
    fig.legend(handles=handles,
               loc="lower center", fontsize=FS_LEGEND,
               ncol=min(len(handles), 4),
               bbox_to_anchor=(0.5, -0.14), framealpha=0.9)

    plt.tight_layout()
    out_path = OUT_DIR / "global_opcode_divergence_highlighted.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
