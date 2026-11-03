from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

BASE_DIR  = Path(__file__).resolve().parent.parent
TASKS     = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]

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

OUT_DIR = BASE_DIR / "analysis" / "comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
TASK_COLORS = {
    "t41": "#4e79a7", "t42": "#f28e2b", "t43": "#e15759",
    "t44": "#76b7b2", "t45": "#59a14f", "t46": "#edc948",
    "t47": "#b07aa1", "t48": "#ff9da7", "t49": "#9c755f", "t50": "#bab0ac",
}

# font sizes tuned for \textwidth figures at 11pt thesis body text
FS_TITLE  = 10
FS_TICK   = 9
FS_LABEL  = 9
FS_ANNOT  = 7
FS_LEGEND = 8


def load_summary(task):
    path = BASE_DIR / "analysis" / task / f"{task}_summary.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df["task"] = task
    return df


def load_effects(task):
    task_dir = BASE_DIR / "analysis" / task
    if not task_dir.exists():
        return None
    files = sorted(task_dir.glob("*_effects.csv"))
    if not files:
        return None
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        stem  = f.stem.replace("_effects", "")
        parts = stem.split("_")
        df["task"]       = task
        df["true_model"] = parts[-1] if len(parts) >= 4 else "?"
        df["prompt"]     = parts[1]  if len(parts) >= 2 else "?"
        df["run"]        = parts[2]  if len(parts) >= 3 else "?"
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def plot_accuracy_by_task(summaries, out_dir):
    fig, ax = plt.subplots(figsize=(10, 4))

    n_tasks  = len(TASKS)
    n_models = len(CLASS_NAMES)
    width    = 0.22
    x        = np.arange(n_tasks)

    for mi, model in enumerate(CLASS_NAMES):
        accs = []
        for task in TASKS:
            df = summaries.get(task)
            if df is None:
                accs.append(0); continue
            sub = df[df["true"] == model]
            accs.append(sub["correct"].mean() if len(sub) else 0)
        offset = (mi - 1) * width
        bars = ax.bar(x + offset, accs, width, label=model,
                      color=COLORS[model], alpha=0.85)
        for bar, acc in zip(bars, accs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{acc:.0%}", ha="center", va="bottom", fontsize=FS_ANNOT)

    overall = []
    for task in TASKS:
        df = summaries.get(task)
        overall.append(df["correct"].mean() if df is not None else 0)
    ax.plot(x, overall, "k--o", linewidth=1.5, markersize=4,
            label="overall", zorder=5)
    ax.axhline(1/3, color="gray", linewidth=1, linestyle=":",
               label="random baseline")

    ax.set_xticks(x)
    ax.set_xticklabels(TASKS, fontsize=FS_TICK)
    ax.set_ylabel("Accuracy", fontsize=FS_LABEL)
    ax.set_ylim(0, 1.15)
    ax.set_title("Classification accuracy per task per model",
                 fontsize=FS_TITLE)
    ax.legend(loc="upper right", fontsize=FS_LEGEND)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_dir / "accuracy_by_task.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved accuracy_by_task.png")


def plot_shap_magnitude_by_task(effects, out_dir):
    fig, ax = plt.subplots(figsize=(9, 4))

    means, stds = [], []
    for task in TASKS:
        df = effects.get(task)
        if df is None:
            means.append(0); stds.append(0); continue
        top5 = df.groupby(["task", "true_model", "prompt", "run"]).apply(
            lambda g: g.nlargest(5, "magnitude")["magnitude"].mean()
        ).reset_index(name="top5_mean")
        means.append(top5["top5_mean"].mean())
        stds.append(top5["top5_mean"].std())

    x    = np.arange(len(TASKS))
    bars = ax.bar(x, means, yerr=stds, capsize=3,
                  color=[TASK_COLORS[t] for t in TASKS], alpha=0.85)
    for bar, m in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                f"{m:.3f}", ha="center", va="bottom", fontsize=FS_ANNOT)

    ax.set_xticks(x)
    ax.set_xticklabels(TASKS, fontsize=FS_TICK)
    ax.set_ylabel("Mean top-5 SHAP magnitude", fontsize=FS_LABEL)
    ax.set_title("SHAP signal strength per task\n"
                 "(mean of top-5 feature magnitudes per file +/- std)",
                 fontsize=FS_TITLE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_dir / "shap_magnitude_by_task.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved shap_magnitude_by_task.png")


def plot_imbalance_ratio(summaries, effects, out_dir):
    from collections import Counter
    fig, ax = plt.subplots(figsize=(9, 4))

    ratios = []
    for task in TASKS:
        summary = summaries.get(task)
        eff     = effects.get(task)
        if summary is None or eff is None:
            ratios.append(1.0); continue
        summary = summary.copy()
        summary["true_model"] = summary["true"]
        correct_lookup = {
            (row["true_model"], str(row["prompt"]), str(row["run"])): bool(row["correct"])
            for _, row in summary.iterrows()
        }
        correct_counts, incorrect_counts = Counter(), Counter()
        for (true_model, prompt, run), group in eff.groupby(["true_model", "prompt", "run"]):
            is_correct = correct_lookup.get((true_model, str(prompt), str(run)))
            if is_correct is None: continue
            top5_bytes = group.nlargest(5, "magnitude")["byte_index"].tolist()
            if is_correct: correct_counts.update(top5_bytes)
            else:          incorrect_counts.update(top5_bytes)
        n_correct   = int(summary["correct"].sum())
        n_incorrect = int((~summary["correct"]).sum())
        if n_correct == 0 or n_incorrect == 0:
            ratios.append(1.0); continue
        c_norm = sum(correct_counts.values())   / n_correct
        i_norm = sum(incorrect_counts.values()) / n_incorrect
        ratios.append(i_norm / c_norm if c_norm > 0 else float("inf"))

    colors = ["#e05c5c" if r > 1.2 else "#5cb85c" if r < 0.8 else "#f0ad4e"
              for r in ratios]
    bars = ax.bar(np.arange(len(TASKS)), ratios, color=colors, alpha=0.85)
    ax.axhline(1.0, color="black", linewidth=1.2, linestyle="--",
               label="equal (ratio = 1)")
    for bar, r in zip(bars, ratios):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{r:.2f}x", ha="center", va="bottom", fontsize=FS_ANNOT)
    ax.set_xticks(np.arange(len(TASKS)))
    ax.set_xticklabels(TASKS, fontsize=FS_TICK)
    ax.set_ylabel("Incorrect / correct ratio", fontsize=FS_LABEL)
    ax.set_title("Byte imbalance ratio per task", fontsize=FS_TITLE)
    ax.legend(fontsize=FS_LEGEND)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_dir / "byte_imbalance_ratio.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved byte_imbalance_ratio.png")


def plot_byte_overlap(effects, out_dir, top_n=20):
    task_top = {}
    for task in TASKS:
        df = effects.get(task)
        if df is None:
            task_top[task] = {}; continue
        top = df.groupby("byte_index")["magnitude"].mean().nlargest(top_n)
        task_top[task] = top.to_dict()
    all_bytes = sorted(set(b for d in task_top.values() for b in d))
    matrix = np.zeros((len(all_bytes), len(TASKS)))
    for ti, task in enumerate(TASKS):
        for bi, byte in enumerate(all_bytes):
            matrix[bi, ti] = task_top[task].get(byte, 0)
    col_max = matrix.max(axis=0, keepdims=True)
    col_max[col_max == 0] = 1
    matrix_norm = matrix / col_max
    presence = (matrix > 0).sum(axis=1)
    order    = np.argsort(-presence)
    matrix_norm = matrix_norm[order]
    all_bytes   = [all_bytes[i] for i in order]

    fig, ax = plt.subplots(figsize=(9, max(5, len(all_bytes) * 0.3)))
    im = ax.imshow(matrix_norm, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
    ax.set_xticks(range(len(TASKS)))
    ax.set_xticklabels(TASKS, fontsize=FS_TICK)
    ax.set_yticks(range(len(all_bytes)))
    ax.set_yticklabels([f"byte_{b}" for b in all_bytes], fontsize=7)
    ax.set_title(f"Byte importance overlap across tasks (top {top_n} per task)",
                 fontsize=FS_TITLE)
    plt.colorbar(im, ax=ax, label="normalised mean SHAP magnitude")
    plt.tight_layout()
    plt.savefig(out_dir / "byte_overlap_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved byte_overlap_heatmap.png")


def plot_duplicate_vectors(summaries, out_dir):
    fig, ax = plt.subplots(figsize=(9, 4))
    counts = []
    totals = []
    for task in TASKS:
        df = summaries.get(task)
        if df is None:
            counts.append(0); totals.append(0); continue
        prob_cols = [f"prob_{c}" for c in CLASS_NAMES]
        dupes = df[df.duplicated(subset=prob_cols, keep=False)]
        counts.append(len(dupes))
        totals.append(len(df))
    x = np.arange(len(TASKS))
    ax.bar(x, counts, color=[TASK_COLORS[t] for t in TASKS], alpha=0.85)
    for xi, (c, total) in enumerate(zip(counts, totals)):
        pct = c / total if total else 0
        ax.text(xi, c + 0.3, f"{c}\n({pct:.0%})",
                ha="center", va="bottom", fontsize=FS_ANNOT)
    ax.set_xticks(x)
    ax.set_xticklabels(TASKS, fontsize=FS_TICK)
    ax.set_ylabel("# files with duplicate probability vector", fontsize=FS_LABEL)
    ax.set_title("Duplicate prediction vectors per task", fontsize=FS_TITLE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(out_dir / "duplicate_vectors.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved duplicate_vectors.png")


def plot_confidence_distribution(summaries, out_dir):
    fig, axes = plt.subplots(2, len(TASKS)//2, figsize=(14, 7), sharey=True)
    fig.suptitle("Confidence distribution per task (correct vs incorrect)",
                 fontsize=FS_TITLE)
    for ax, task in zip(axes.flat, TASKS):
        df = summaries.get(task)
        if df is None:
            ax.set_visible(False); continue
        correct   = df[df["correct"]]["max_prob"]
        incorrect = df[~df["correct"]]["max_prob"]
        bins = np.linspace(0.3, 1.0, 15)
        ax.hist(correct,   bins=bins, alpha=0.6, color="#5cb85c", label="correct")
        ax.hist(incorrect, bins=bins, alpha=0.6, color="#e05c5c", label="incorrect")
        ax.axvline(correct.mean(),   color="#2d7a2d", linewidth=1.2, linestyle="--")
        ax.axvline(incorrect.mean(), color="#a02020", linewidth=1.2, linestyle="--")
        ax.set_title(task, fontsize=FS_TICK)
        ax.set_xlabel("confidence", fontsize=FS_ANNOT)
        if ax == axes.flat[0]:
            ax.set_ylabel("# files", fontsize=FS_LABEL)
            ax.legend(fontsize=FS_ANNOT)
    plt.tight_layout()
    plt.savefig(out_dir / "confidence_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved confidence_distribution.png")


def print_comparison(summaries):
    print("\n" + "="*70)
    print("CROSS-TASK COMPARISON SUMMARY")
    print("="*70)
    print(f"\n{'Task':<6} {'Function':<25} {'Overall':>8} {'Llama':>8} "
          f"{'Mistral':>8} {'Qwen':>8} {'Dupes':>6}")
    print("-" * 70)
    for task in TASKS:
        df = summaries.get(task)
        if df is None:
            print(f"{task:<6} {'N/A':<25}"); continue
        overall  = df["correct"].mean()
        by_model = {m: df[df["true"] == m]["correct"].mean() for m in CLASS_NAMES}
        prob_cols = [f"prob_{c}" for c in CLASS_NAMES]
        dupes = df[df.duplicated(subset=prob_cols, keep=False)]
        print(f"{task:<6} {TASK_NAMES[task]:<25} {overall:>7.1%} "
              f"{by_model['llama']:>7.1%} {by_model['mistral']:>7.1%} "
              f"{by_model['qwen']:>7.1%} {len(dupes):>6}")


def main():
    print("Loading summaries...")
    summaries = {}
    for task in TASKS:
        df = load_summary(task)
        if df is not None:
            summaries[task] = df
            print(f"  {task}: {len(df)} files")

    print("\nLoading effects...")
    effects = {}
    for task in TASKS:
        df = load_effects(task)
        if df is not None:
            effects[task] = df
            print(f"  {task}: {len(df)} feature rows")

    if not summaries:
        print("No data found.")
        sys.exit(1)

    print_comparison(summaries)
    print("\nGenerating plots...")
    plot_accuracy_by_task(summaries, OUT_DIR)
    plot_shap_magnitude_by_task(effects, OUT_DIR)
    plot_imbalance_ratio(summaries, effects, OUT_DIR)
    plot_byte_overlap(effects, OUT_DIR)
    plot_duplicate_vectors(summaries, OUT_DIR)
    plot_confidence_distribution(summaries, OUT_DIR)
    print(f"\nAll outputs saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
