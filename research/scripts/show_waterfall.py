"""
show_waterfall.py

Cumulative SHAP step plot for a specific file.
Shows 3 lines (llama/mistral/qwen), each stepping through the top-N bytes
in order of the predicted model's magnitude. Each step moves the running
total left or right by that byte's SHAP value.

Usage:
    python scripts/show_waterfall.py t47_p3_r2_llama.py
    python scripts/show_waterfall.py t47_p3_r2_llama.py --top 15
    python scripts/show_waterfall.py ../test_data/outputs/llama/cleaned/t47_p3_r2_llama.py
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR     = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "analysis"

COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
CLASS_NAMES = ["llama", "mistral", "qwen"]


def load_effects(task: str, filestem: str) -> pd.DataFrame | None:
    path = ANALYSIS_DIR / task / f"{filestem}_effects.csv"
    if not path.exists():
        print(f"Effects CSV not found: {path}")
        return None
    return pd.read_csv(path)


def load_summary_row(task: str, filename: str) -> dict | None:
    path = ANALYSIS_DIR / task / f"{task}_summary.csv"
    if not path.exists():
        return None
    df   = pd.read_csv(path)
    rows = df[df["file"] == filename]
    if rows.empty:
        return None
    return rows.iloc[0].to_dict()


def plot_cumulative_shap(effects: pd.DataFrame,
                         predicted: str, correct: bool,
                         filename: str, top_n: int, out_path: Path):
    """
    Cumulative step plot. X axis = running SHAP total. Y axis = feature steps.
    3 lines, one per class. Sorted by predicted class magnitude (top features first).
    Rest of features collapsed into a final single step per line.
    """
    df = effects[["feature", "value",
                  "shap_llama", "shap_mistral", "shap_qwen",
                  "magnitude"]].copy()

    # sort by predicted class magnitude
    df = df.sort_values("magnitude", ascending=False)
    top  = df.head(top_n).copy()
    rest = df.iloc[top_n:].copy()

    # rest row
    rest_row = pd.DataFrame([{
        "feature":      f"({len(rest)} other features)",
        "shap_llama":   rest["shap_llama"].sum(),
        "shap_mistral": rest["shap_mistral"].sum(),
        "shap_qwen":    rest["shap_qwen"].sum(),
        "magnitude":    0,
    }])
    display = pd.concat([top, rest_row], ignore_index=True)

    n_steps  = len(display)
    tick     = "✓" if correct else "✗"
    title    = f"{filename}\nPredicted: {predicted}  {tick}"

    fig, ax = plt.subplots(figsize=(11, max(6, n_steps * 0.55 + 2)))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")

    def make_label(row):
        if not str(row["feature"]).startswith("byte_"):
            return row["feature"]
        val = row.get("value", "?")
        return f"{row['feature']} (val={int(val) if val != '?' else '?'})"

    y_labels = [make_label(row) for _, row in display.iterrows()]
    lane = {"llama": 0.2, "mistral": 0.0, "qwen": -0.2}

    for model in CLASS_NAMES:
        col    = f"shap_{model}"
        color  = COLORS[model]
        vals   = display[col].values
        off_y  = lane[model]

        # lighter version of color for negative contributions
        import matplotlib.colors as mc
        def lighten(hex_color, factor=0.45):
            rgb = mc.to_rgb(hex_color)
            return tuple(1 - (1 - ch) * factor for ch in rgb)
        color_light = lighten(color)

        x = [0.0]
        for v in vals:
            x.append(x[-1] + v)

        for i in range(n_steps):
            y_base = n_steps - i
            y_line = y_base + off_y
            x_from = x[i]
            x_to   = x[i + 1]

            line_color = color if x_to >= x_from else color_light
            ax.plot([x_from, x_to], [y_line, y_line],
                    color=line_color, linewidth=2.5, alpha=0.95,
                    solid_capstyle="round")

            if i < n_steps - 1:
                y_next = (n_steps - i - 1) + off_y
                ax.plot([x_to, x_to], [y_line, y_next],
                        color=color, linewidth=1.0,
                        alpha=0.4, linestyle="--")

            dot_color = color if x_to >= x_from else color_light
            ax.scatter(x_to, y_line, color=dot_color, s=20, zorder=5)

            if model == predicted and abs(x_to - x_from) > 0.01:
                ha   = "left" if x_to > x_from else "right"
                loff = 0.005 if x_to > x_from else -0.005
                ax.text(x_to + loff, y_line + 0.07,
                        f"{x_to - x_from:+.3f}",
                        fontsize=7, color=color, ha=ha, va="bottom")

        ax.scatter(x[-1], 0, color=color, s=60, zorder=6, marker="D")
        ax.text(x[-1], 0.45, f"{x[-1]:+.3f}",
                fontsize=8, color=color, ha="center", va="top",
                fontweight="bold")

    # base line
    ax.axvline(0, color="#555", linewidth=1.2, zorder=4)
    ax.text(0, n_steps + 0.3, "base\n(0)", fontsize=7.5,
            color="#666", ha="center", va="bottom")

    # y axis labels — features at their step positions
    ax.set_yticks(range(1, n_steps + 1))
    ax.set_yticklabels(y_labels[::-1], fontsize=8.5, fontfamily="monospace")
    ax.set_ylim(0, n_steps + 0.8)

    ax.set_xlabel("Cumulative SHAP value", fontsize=9)
    ax.set_title(title, fontsize=10, pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    # legend
    handles = [mpatches.Patch(color=COLORS[m], alpha=0.85, label=m)
               for m in CLASS_NAMES]
    ax.legend(handles=handles, fontsize=9, loc="lower right")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="e.g. t47_p3_r2_llama.py")
    parser.add_argument("--top", type=int, default=10,
                        help="Number of top features to show (default: 10)")
    args = parser.parse_args()

    fname = Path(args.filename).name
    if not fname.endswith(".py"):
        fname += ".py"

    parts = Path(fname).stem.split("_")
    task  = parts[0]
    stem  = Path(fname).stem

    effects = load_effects(task, stem)
    if effects is None:
        sys.exit(1)

    summary_row = load_summary_row(task, fname)
    if summary_row is None:
        print(f"Could not find {fname} in {task}_summary.csv")
        sys.exit(1)

    predicted  = summary_row.get("predicted", summary_row.get("pred", "?"))
    true_model = summary_row.get("true", "?")
    correct    = bool(summary_row.get("correct", False))

    print(f"File:      {fname}")
    print(f"True:      {true_model}")
    print(f"Predicted: {predicted}  {'✓' if correct else '✗'}")

    out_dir  = ANALYSIS_DIR / task / "bytecode_viz"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{stem}_waterfall_cumulative.png"

    plot_cumulative_shap(effects, predicted, correct,
                         fname, top_n=args.top, out_path=out_path)


if __name__ == "__main__":
    main()
