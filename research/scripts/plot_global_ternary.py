"""
Plots all test file predictions in the ternary simplex as a scatter plot.
One dot per file, colored and shaped by true model.
Reads from the per-task summary CSVs produced by analyze_task.py.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# ── config ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
TASKS       = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
OUT_DIR     = BASE_DIR / "analysis" / "comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TASK_NAMES = {
    "t41": "group_anagrams",
    "t42": "course_schedule",
    "t43": "binary_tree_inorder",
    "t44": "rotate_array",
    "t45": "search_insert_position",
    "t46": "text_justification",
    "t47": "basic_calculator",
    "t48": "median_of_two_sorted_arrays",
    "t49": "word_break",
    "t50": "find_all_anagrams",
}

CLASS_NAMES   = ["llama", "mistral", "qwen"]
COLORS        = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
MARKERS       = {"llama": "o", "mistral": "s", "qwen": "^"}
FONT_FAMILY   = "DejaVu Sans"
CORNER_OFFSET = 0.07

# ── font sizes tuned for figsize=(7,6.5) at \textwidth (~160mm) ───────────────
FS_CORNER  = 12   # corner model labels
FS_TITLE   = 11   # figure title
FS_LEGEND  = 9    # legend text
FS_ANNOT   = 9    # accuracy annotation


def ternary_xy(probs):
    llama, mistral, qwen = probs
    return mistral + 0.5 * qwen, (np.sqrt(3) / 2) * qwen


def draw_triangle(ax):
    h      = np.sqrt(3) / 2
    cx, cy = 0.5, h / 3
    corners = {"llama": (0, 0), "mistral": (1, 0), "qwen": (0.5, h)}

    ax.plot([0, 1, 0.5, 0], [0, 0, h, 0],
            color="#444444", linewidth=1.5, zorder=1)

    for mx, my in [(0.75, h/2), (0.25, h/2), (0.5, 0)]:
        ax.plot([cx, mx], [cy, my],
                color="#cccccc", linewidth=0.6, linestyle="--", zorder=0)

    for cls, (x, y) in corners.items():
        ax.scatter([x], [y], s=100, color=COLORS[cls],
                   zorder=5, edgecolors="white", linewidths=1.0)
        dx, dy = x - cx, y - cy
        norm   = (dx**2 + dy**2) ** 0.5
        lx, ly = x + dx/norm * CORNER_OFFSET, y + dy/norm * CORNER_OFFSET
        ax.text(lx, ly, cls,
                ha="center", va="center",
                fontsize=FS_CORNER, fontweight="bold",
                color=COLORS[cls], fontfamily=FONT_FAMILY,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_aspect("equal")
    ax.axis("off")


def load_all_summaries() -> pd.DataFrame:
    dfs = []
    for task in TASKS:
        path = BASE_DIR / "analysis" / task / f"{task}_summary.csv"
        if not path.exists():
            print(f"  WARNING: missing {path}")
            continue
        df = pd.read_csv(path)
        df["task"] = task
        dfs.append(df)
    if not dfs:
        raise FileNotFoundError("No summary CSVs found.")
    return pd.concat(dfs, ignore_index=True)


def plot_global_ternary(df: pd.DataFrame, out_dir: Path):
    fig, ax = plt.subplots(figsize=(7, 6.5))
    fig.patch.set_facecolor("white")

    draw_triangle(ax)

    for correct, alpha, size, zorder in [(False, 0.20, 30, 2),
                                          (True,  0.80, 45, 3)]:
        sub = df[df["correct"] == correct]
        for model in CLASS_NAMES:
            msub = sub[sub["true"] == model]
            if msub.empty:
                continue
            xs, ys = zip(*[
                ternary_xy([row[f"prob_{c}"] for c in CLASS_NAMES])
                for _, row in msub.iterrows()
            ])
            ax.scatter(xs, ys,
                       color=COLORS[model],
                       marker=MARKERS[model],
                       s=size, alpha=alpha,
                       zorder=zorder,
                       edgecolors="white" if correct else "none",
                       linewidths=0.5)

    model_handles = [
        plt.scatter([], [], color=COLORS[m], marker=MARKERS[m],
                    s=45, label=m, edgecolors="white", linewidths=0.5)
        for m in CLASS_NAMES
    ]
    status_handles = [
        plt.scatter([], [], color="#888888", marker="o",
                    s=45, alpha=0.80, label="correct",
                    edgecolors="white", linewidths=0.5),
        plt.scatter([], [], color="#888888", marker="o",
                    s=30, alpha=0.20, label="incorrect",
                    edgecolors="none"),
    ]

    leg1 = ax.legend(handles=model_handles,
                     title="true model", title_fontsize=FS_LEGEND,
                     fontsize=FS_LEGEND, loc="upper right",
                     framealpha=0.9, edgecolor="#cccccc", fancybox=True)
    ax.add_artist(leg1)
    leg2 = ax.legend(handles=status_handles,
                     title="prediction", title_fontsize=FS_LEGEND,
                     fontsize=FS_LEGEND, loc="upper left",
                     framealpha=0.9, edgecolor="#cccccc", fancybox=True)
    for leg in [leg1, leg2]:
        for text in leg.get_texts():
            text.set_fontfamily(FONT_FAMILY)

    total   = len(df)
    correct = df["correct"].sum()
    ax.text(0.5, -0.07,
            f"Overall accuracy: {correct}/{total} = {correct/total:.1%}   "
            f"(random baseline: 33.3\%)",
            ha="center", va="center",
            fontsize=FS_ANNOT, color="#444444",
            fontfamily=FONT_FAMILY,
            transform=ax.transAxes)

    ax.set_title(
        "Global ternary prediction map\n"
        "all test files — position = predicted probability vector",
        fontsize=FS_TITLE, pad=20,
        fontfamily=FONT_FAMILY, color="#222222",
    )

    plt.tight_layout()
    out_path = out_dir / "global_ternary.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path}")


def plot_global_ternary_by_task(df: pd.DataFrame, out_dir: Path):
    ncols = int(np.ceil(len(TASKS) / 2))
    fig, axes = plt.subplots(2, ncols, figsize=(ncols * 3.5, 8))
    fig.patch.set_facecolor("white")
    axes = axes.flatten()

    fig.suptitle("Per-task ternary prediction maps",
                 fontsize=FS_TITLE, color="#222222",
                 fontfamily=FONT_FAMILY, y=1.02)

    for ax, task in zip(axes, TASKS):
        sub = df[df["task"] == task]
        draw_triangle(ax)

        for model in CLASS_NAMES:
            msub = sub[sub["true"] == model]
            if msub.empty:
                continue
            for rows, alpha, size, ec in [
                (msub[~msub["correct"]], 0.20, 25, "none"),
                (msub[msub["correct"]],  0.80, 35, "white"),
            ]:
                if rows.empty:
                    continue
                xs, ys = zip(*[
                    ternary_xy([row[f"prob_{c}"] for c in CLASS_NAMES])
                    for _, row in rows.iterrows()
                ])
                ax.scatter(xs, ys, color=COLORS[model], marker=MARKERS[model],
                           s=size, alpha=alpha, zorder=3,
                           edgecolors=ec, linewidths=0.4)

        acc = sub["correct"].mean()
        ax.set_title(f"{task} — {TASK_NAMES[task]}\nacc={acc:.0%}",
                     fontsize=7, pad=14,
                     fontfamily=FONT_FAMILY, color="#222222")

    for idx in range(len(TASKS), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    out_path = out_dir / "global_ternary_by_task.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path}")


def main():
    print("Loading summaries...")
    df = load_all_summaries()
    print(f"  {len(df)} files across {df['task'].nunique()} tasks")
    print("\nGenerating plots...")
    plot_global_ternary(df, OUT_DIR)
    plot_global_ternary_by_task(df, OUT_DIR)
    print(f"\nSaved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
