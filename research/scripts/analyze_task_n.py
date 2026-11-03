from pathlib import Path
import json
import pickle
import sys

import numpy as np
import pandas as pd
import os
import shap
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec


# ══════════════════════════════════════════════════════════════════════════════
# ── config — change these ─────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

TASK_ID = os.environ.get("TASK_ID", "t41")

# ── consistent palette ─────────────────────────────────────────────────────────
COLORS = {
    "llama":   "#e05c5c",
    "mistral": "#5cb85c",
    "qwen":    "#5b8dd9",
}
FONT_FAMILY   = "DejaVu Sans"
CORNER_OFFSET = 0.07
TOP_N_GRID = 16  # features shown per subplot in all_ternary grid

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
MODEL_FILE  = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"
OUT_DIR     = BASE_DIR / "analysis" / TASK_ID
OUT_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["llama", "mistral", "qwen"]

sys.path.insert(0, str(BASE_DIR / "scripts"))
from bytecode_utils import preprocess_single_file


# ══════════════════════════════════════════════════════════════════════════════
# helpers
# ══════════════════════════════════════════════════════════════════════════════

def load_model_bundle():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)
    if isinstance(loaded, dict) and "model" in loaded:
        return loaded["model"], loaded.get("model_type", "unknown")
    return loaded, type(loaded).__name__


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def load_target_function() -> str:
    meta = json.loads((PROMPTS_DIR / TASK_ID / "meta.json").read_text(encoding="utf-8"))
    return meta["function_name"]


def get_class_shap(shap_values, class_idx: int) -> np.ndarray:
    if isinstance(shap_values, list):
        return shap_values[class_idx]
    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_idx]
    raise ValueError(f"Unexpected SHAP format: {type(shap_values)}")


def softmax(x):
    x = np.array(x, dtype=float) - np.max(x)
    e = np.exp(x)
    return e / e.sum()


def ternary_xy(probs):
    llama, mistral, qwen = probs
    return mistral + 0.5 * qwen, (np.sqrt(3) / 2) * qwen


# ══════════════════════════════════════════════════════════════════════════════
# collect task files
# ══════════════════════════════════════════════════════════════════════════════

def find_task_files() -> list[Path]:
    candidates = [
        BASE_DIR / "test_data" / "generated",
        BASE_DIR / "test_data" / "scripts",
        BASE_DIR / "data" / "generated",
        BASE_DIR / "generated",
        BASE_DIR / "scripts",
    ]
    found = []
    for d in candidates:
        if d.exists():
            found.extend(sorted(d.glob(f"{TASK_ID}_*.py")))
    if not found:
        found = sorted(BASE_DIR.rglob(f"{TASK_ID}_p*_r*_*.py"))
    return found


# ══════════════════════════════════════════════════════════════════════════════
# per-file SHAP analysis
# ══════════════════════════════════════════════════════════════════════════════

def analyze_file(py_file: Path, model, explainer, trained_features, target_fn):
    true_model = py_file.stem.split("_")[-1]
    parts      = py_file.stem.split("_")
    prompt_id  = parts[1] if len(parts) > 1 else "?"
    run_id     = parts[2] if len(parts) > 2 else "?"

    X = preprocess_single_file(py_file, trained_features, target_fn)
    for col in trained_features:
        if col not in X.columns:
            X[col] = 0
    extra = [c for c in X.columns if c not in trained_features]
    if extra:
        X = X.drop(columns=extra)
    X = X[trained_features]

    probs     = model.predict_proba(X)[0]
    predicted = CLASS_NAMES[int(np.argmax(probs))]
    correct   = predicted == true_model
    sv        = explainer.shap_values(X)

    rows = []
    for j in range(X.shape[1]):
        effect_vec = np.array([get_class_shap(sv, ci)[0, j] for ci in range(3)])
        rows.append({
            "feature":    X.columns[j],
            "byte_index": int(X.columns[j].replace("byte_", "")),
            "value":      float(X.iloc[0, j]),
            **{f"shap_{c}": float(effect_vec[ci]) for ci, c in enumerate(CLASS_NAMES)},
            "magnitude":  float(np.linalg.norm(effect_vec)),
            "top_class":  CLASS_NAMES[int(np.argmax(effect_vec))],
        })
    effects = pd.DataFrame(rows).sort_values("magnitude", ascending=False).reset_index(drop=True)

    return {
        "file":        py_file.name,
        "true":        true_model,
        "predicted":   predicted,
        "correct":     correct,
        "prompt":      prompt_id,
        "run":         run_id,
        "probs":       {c: float(p) for c, p in zip(CLASS_NAMES, probs)},
        "max_prob":    float(np.max(probs)),
        "effects":     effects,
        "X":           X,
        "shap_values": sv,
    }


# ══════════════════════════════════════════════════════════════════════════════
# ternary plot
# ══════════════════════════════════════════════════════════════════════════════

def draw_triangle(ax):
    h      = np.sqrt(3) / 2
    cx, cy = 0.5, h / 3   # centroid

    corners = {"llama": (0, 0), "mistral": (1, 0), "qwen": (0.5, h)}

    # edges
    ax.plot([0, 1, 0.5, 0], [0, 0, h, 0],
            color="#444444", linewidth=1.5, zorder=1)

    # altitude lines: centroid → midpoint of each opposite edge only
    midpoints = [
        (0.75, h / 2),   # opposite llama
        (0.25, h / 2),   # opposite mistral
        (0.5,  0),       # opposite qwen
    ]
    for mx, my in midpoints:
        ax.plot([cx, mx], [cy, my],
                color="#cccccc", linewidth=0.6,
                linestyle="--", zorder=0)

    # corner dots + labels
    for cls, (x, y) in corners.items():
        ax.scatter([x], [y], s=100, color=COLORS[cls],
                   zorder=5, edgecolors="white", linewidths=1.0)
        dx, dy = x - cx, y - cy
        norm   = (dx**2 + dy**2) ** 0.5
        lx = x + dx / norm * CORNER_OFFSET
        ly = y + dy / norm * CORNER_OFFSET
        ax.text(lx, ly, cls,
                ha="center", va="center",
                fontsize=9, fontweight="bold",
                color=COLORS[cls], fontfamily=FONT_FAMILY,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_aspect("equal")
    ax.axis("off")


def plot_ternary(rec, ax, title, expected_value, model_probs=None):
    effects = rec["effects"].sort_values("magnitude", ascending=False)

    # truncate to top N for readability
    plot_effects = effects.head(TOP_N_GRID)

    raw    = np.array(expected_value, dtype=float)
    points = [softmax(raw)]
    for _, row in plot_effects.iterrows():
        raw += np.array([row[f"shap_{c}"] for c in CLASS_NAMES])
        points.append(softmax(raw))

    points = np.array(points)
    xy     = np.array([ternary_xy(p) for p in points])
    deltas = np.linalg.norm(xy[1:] - xy[:-1], axis=1)
    max_d  = deltas.max() if deltas.max() > 0 else 1.0

    draw_triangle(ax)
    ax.scatter(*xy[0], marker="X", s=90, color="#333333",
               zorder=6, label="baseline",
               edgecolors="white", linewidths=0.7)

    for i, (_, row) in enumerate(plot_effects.iterrows()):
        x1, y1 = xy[i]; x2, y2 = xy[i + 1]
        dp     = points[i + 1] - points[i]
        color  = COLORS.get(CLASS_NAMES[int(np.argmax(dp))], "#888888")
        nd     = deltas[i] / max_d
        lw     = max(0.6, nd * 3.0)
        ms     = max(4,   nd * 14)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color,
                                   linewidth=lw, alpha=0.85,
                                   mutation_scale=ms,
                                   shrinkA=0, shrinkB=0))

    # residual arrow from last top-N point to true prediction
    if model_probs is not None:
        mp = np.array([model_probs[c] for c in CLASS_NAMES]) \
             if isinstance(model_probs, dict) \
             else np.array(model_probs, dtype=float)
        final_xy = ternary_xy(mp)
        ax.annotate("", xy=(final_xy[0], final_xy[1]),
                    xytext=(xy[-1][0], xy[-1][1]),
                    arrowprops=dict(arrowstyle="->", color="#888888",
                                   linewidth=1.0, alpha=0.6,
                                   linestyle="dashed", mutation_scale=7,
                                   shrinkA=0, shrinkB=0))
        ax.scatter(*final_xy, marker="*", s=160, color="#222222",
                   zorder=7, label="prediction",
                   edgecolors="white", linewidths=0.7)
    else:
        ax.scatter(*xy[-1], marker="*", s=160, color="#222222",
                   zorder=7, label="endpoint",
                   edgecolors="white", linewidths=0.7)

    end_cls = CLASS_NAMES[int(np.argmax(points[-1]))]
    verdict = "✓" if rec["correct"] else "✗"
    ax.set_title(
        f"{title}\ntrue={rec['true']}  pred={end_cls} {verdict}  "
        f"conf={rec['max_prob']:.2f}",
        fontsize=8, pad=5, fontfamily=FONT_FAMILY, color="#222222",
    )
    ax.legend(fontsize=6, loc="upper right",
              framealpha=0.8, edgecolor="#cccccc")


# ══════════════════════════════════════════════════════════════════════════════
# summary plots
# ══════════════════════════════════════════════════════════════════════════════

def _style_ax(ax, title=None, xlabel=None, ylabel=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(colors="#444444")
    if title:
        ax.set_title(title, fontsize=11, pad=8,
                     fontfamily=FONT_FAMILY, color="#222222")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color="#444444")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color="#444444")


def plot_accuracy_heatmap(records, out_dir):
    prompts = sorted({r["prompt"] for r in records})

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.patch.set_facecolor("white")
    fig.suptitle(f"{TASK_ID} — per-prompt accuracy & confidence per model",
                 fontsize=12, color="#222222", fontfamily=FONT_FAMILY, y=1.02)

    for ax, model in zip(axes, CLASS_NAMES):
        recs = [r for r in records if r["true"] == model]
        runs = sorted({r["run"] for r in recs})
        grid = np.full((len(prompts), len(runs)), np.nan)
        for r in recs:
            pi = prompts.index(r["prompt"])
            ri = runs.index(r["run"])
            grid[pi, ri] = 1.0 if r["correct"] else 0.0

        im = ax.imshow(grid, vmin=0, vmax=1,
                       cmap="RdYlGn", aspect="auto")
        ax.set_xticks(range(len(runs)))
        ax.set_xticklabels(runs, fontfamily=FONT_FAMILY, fontsize=8)
        ax.set_yticks(range(len(prompts)))
        ax.set_yticklabels(prompts, fontfamily=FONT_FAMILY, fontsize=8)
        ax.set_xlabel("run", fontsize=9, color="#444444")
        ax.set_ylabel("prompt", fontsize=9, color="#444444")
        ax.set_title(model, fontsize=11, fontfamily=FONT_FAMILY,
                     color=COLORS[model], fontweight="bold")

        for r in recs:
            pi = prompts.index(r["prompt"])
            ri = runs.index(r["run"])
            ax.text(ri, pi, f"{r['max_prob']:.2f}",
                    ha="center", va="center", fontsize=8,
                    fontfamily=FONT_FAMILY,
                    color="white" if not r["correct"] else "#222222")

        cb = plt.colorbar(im, ax=ax, fraction=0.046)
        cb.ax.tick_params(labelsize=7)

    plt.tight_layout()
    plt.savefig(out_dir / "accuracy_heatmap.png", dpi=150,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved accuracy_heatmap.png")


def plot_top_bytes(records, out_dir, top_n=15):
    from collections import Counter
    correct_counts   = Counter()
    incorrect_counts = Counter()
    for r in records:
        top5 = r["effects"].head(5)["byte_index"].tolist()
        if r["correct"]:
            correct_counts.update(top5)
        else:
            incorrect_counts.update(top5)

    all_bytes = sorted(set(correct_counts) | set(incorrect_counts))
    c_vals = [correct_counts.get(b, 0) for b in all_bytes]
    i_vals = [incorrect_counts.get(b, 0) for b in all_bytes]
    total  = [c + i for c, i in zip(c_vals, i_vals)]
    order  = sorted(range(len(all_bytes)), key=lambda x: -total[x])[:top_n]

    bytes_ = [all_bytes[o] for o in order]
    c_vals = [c_vals[o]    for o in order]
    i_vals = [i_vals[o]    for o in order]

    x = np.arange(len(bytes_))
    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor("white")
    ax.bar(x - 0.2, c_vals, 0.4, label="correct",   color="#5b8dd9", alpha=0.85)
    ax.bar(x + 0.2, i_vals, 0.4, label="incorrect", color="#e05c5c", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([f"byte_{b}" for b in bytes_],
                       rotation=45, ha="right",
                       fontfamily=FONT_FAMILY, fontsize=8)
    _style_ax(ax,
              title=f"{TASK_ID} — most influential bytes: correct vs incorrect predictions",
              ylabel="# times in top-5 most influential")
    ax.legend(fontsize=9, framealpha=0.8, edgecolor="#cccccc")
    plt.tight_layout()
    plt.savefig(out_dir / "top_bytes_correct_vs_incorrect.png", dpi=150,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved top_bytes_correct_vs_incorrect.png")


def plot_shap_direction_per_byte(records, out_dir, top_n=10):
    effects_all = []
    for r in records:
        df = r["effects"].copy()
        df["correct"] = r["correct"]
        df["true"]    = r["true"]
        effects_all.append(df)
    all_effects = pd.concat(effects_all, ignore_index=True)

    top_bytes = (
        all_effects.groupby("byte_index")["magnitude"]
        .mean().nlargest(top_n).index.tolist()
    )

    fig, axes = plt.subplots(2, top_n, figsize=(top_n * 2.2, 7),
                             sharey="all")
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"{TASK_ID} — average SHAP per class for top influential bytes\n"
        "(top row: correct predictions   bottom: incorrect)",
        fontsize=11, color="#222222", fontfamily=FONT_FAMILY,
    )

    for col, bidx in enumerate(top_bytes):
        for row, (correct, label) in enumerate(
                [(True, "correct"), (False, "incorrect")]):
            ax  = axes[row][col]
            sub = all_effects[(all_effects["byte_index"] == bidx) &
                               (all_effects["correct"]   == correct)]
            if sub.empty:
                ax.set_visible(False)
                continue
            means  = [sub[f"shap_{c}"].mean() for c in CLASS_NAMES]
            colors = [COLORS[c] for c in CLASS_NAMES]
            ax.bar(CLASS_NAMES, means, color=colors, alpha=0.85)
            ax.axhline(0, color="#888888", linewidth=0.6)
            ax.set_title(f"byte_{bidx}", fontsize=8,
                         fontfamily=FONT_FAMILY, color="#222222")
            if col == 0:
                ax.set_ylabel(f"mean SHAP\n({label})",
                              fontsize=8, color="#444444")
            ax.tick_params(axis="x", labelsize=7)
            ax.tick_params(axis="y", labelsize=7)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color("#cccccc")
            ax.spines["bottom"].set_color("#cccccc")
            for tick in ax.get_xticklabels():
                tick.set_fontfamily(FONT_FAMILY)

    plt.tight_layout()
    plt.savefig(out_dir / "shap_direction_per_byte.png", dpi=150,
                bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved shap_direction_per_byte.png")


def plot_all_ternary(records, out_dir, expected_value):
    """
    Grid of ternary plots for all files in the task.
    Saved as SVG for crisp rendering at any zoom level.
    No byte labels — kept clean for readability at small subplot size.
    """
    n     = len(records)
    ncols = 9
    nrows = (n + ncols - 1) // ncols
    fig   = plt.figure(figsize=(ncols * 3.5, nrows * 3.8))
    fig.patch.set_facecolor("white")
    gs    = gridspec.GridSpec(nrows, ncols, figure=fig,
                              hspace=0.6, wspace=0.35)

    for idx, rec in enumerate(records):
        ax = fig.add_subplot(gs[idx // ncols, idx % ncols])
        plot_ternary(
            rec, ax,
            title=f"{rec['prompt']}_{rec['run']}_{rec['true']}",
            expected_value=expected_value,
            model_probs=rec["probs"],
        )

    for idx in range(n, nrows * ncols):
        fig.add_subplot(gs[idx // ncols, idx % ncols]).set_visible(False)

    fig.suptitle(f"{TASK_ID} — ternary SHAP paths for all files",
                 fontsize=14, y=1.01, color="#222222",
                 fontfamily=FONT_FAMILY)

    # save as SVG for full resolution
    out_path = out_dir / "all_ternary_plots.svg"
    plt.savefig(out_path, bbox_inches="tight", facecolor="white", format="svg")
    plt.close()
    print(f"Saved all_ternary_plots.svg")


# ══════════════════════════════════════════════════════════════════════════════
# text summary
# ══════════════════════════════════════════════════════════════════════════════

def print_summary(records):
    print("\n" + "="*60)
    print(f"{TASK_ID} FULL ANALYSIS SUMMARY")
    print("="*60)

    total   = len(records)
    correct = sum(r["correct"] for r in records)
    print(f"\nOverall accuracy: {correct}/{total} = {correct/total:.1%}")

    print("\n--- Per model ---")
    for model in CLASS_NAMES:
        sub = [r for r in records if r["true"] == model]
        c   = sum(r["correct"] for r in sub)
        print(f"  {model:8s}: {c}/{len(sub)} = {c/len(sub):.1%}")

    print("\n--- Per prompt ---")
    for prompt in sorted({r["prompt"] for r in records}):
        sub = [r for r in records if r["prompt"] == prompt]
        c   = sum(r["correct"] for r in sub)
        print(f"  {prompt}: {c}/{len(sub)} = {c/len(sub):.1%}")

    print("\n--- Per prompt × model ---")
    for prompt in sorted({r["prompt"] for r in records}):
        for model in CLASS_NAMES:
            sub = [r for r in records if r["prompt"] == prompt
                   and r["true"] == model]
            if not sub: continue
            c     = sum(r["correct"] for r in sub)
            confs = [f"{r['max_prob']:.2f}" for r in sub]
            tick  = "✓" if c == len(sub) else ("~" if c > 0 else "✗")
            print(f"  {prompt} {model:8s}: {tick} {c}/{len(sub)}  "
                  f"conf={confs}")

    print("\n--- Duplicate probability vectors ---")
    prob_map: dict[tuple, list[str]] = {}
    for r in records:
        key = tuple(round(r["probs"][c], 6) for c in CLASS_NAMES)
        prob_map.setdefault(key, []).append(r["file"])
    dupes = {k: v for k, v in prob_map.items() if len(v) > 1}
    if dupes:
        print(f"  {sum(len(v) for v in dupes.values())} files share a vector:")
        for key, files in dupes.items():
            print(f"    probs={key}")
            for f in files: print(f"      {f}")
    else:
        print("  None.")

    print("\n--- Top influential bytes overall (mean magnitude) ---")
    all_effects = pd.concat(
        [r["effects"].assign(file=r["file"]) for r in records],
        ignore_index=True,
    )
    top = (all_effects.groupby("byte_index")["magnitude"]
           .mean().nlargest(15).reset_index())
    print(top.to_string(index=False))

    print("\n--- Top bytes per model (mean |SHAP| for own class) ---")
    for model in CLASS_NAMES:
        sub = pd.concat(
            [r["effects"].assign(true=r["true"])
             for r in records if r["true"] == model],
            ignore_index=True,
        )
        col  = f"shap_{model}"
        top5 = (sub.groupby("byte_index")[col]
                .apply(lambda x: x.abs().mean()).nlargest(5))
        print(f"  {model}: {top5.to_dict()}")

    print("\n--- Low confidence files (max_prob < 0.6) ---")
    low = sorted([r for r in records if r["max_prob"] < 0.6],
                 key=lambda r: r["max_prob"])
    for r in low:
        tick = "✓" if r["correct"] else "✗"
        print(f"  {tick} {r['file']:40s}  true={r['true']:8s}  "
              f"pred={r['predicted']:8s}  conf={r['max_prob']:.3f}")


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    report           = load_report()
    trained_features = report["features"]

    model, model_type = load_model_bundle()
    target_fn         = load_target_function()
    explainer         = shap.TreeExplainer(model)
    expected_value    = explainer.expected_value

    files = find_task_files()
    if not files:
        print(f"No {TASK_ID} files found. Searched under {BASE_DIR}")
        print("Pass the directory as an argument: "
              "python analyze_task.py /path/to/scripts")
        if len(sys.argv) > 1:
            d     = Path(sys.argv[1])
            files = sorted(d.glob(f"{TASK_ID}_p*_r*_*.py"))
        if not files:
            sys.exit(1)

    print(f"Found {len(files)} {TASK_ID} files. Running SHAP analysis...")

    records = []
    for i, f in enumerate(files, 1):
        print(f"  [{i}/{len(files)}] {f.name}", end=" ... ", flush=True)
        try:
            rec = analyze_file(f, model, explainer, trained_features, target_fn)
            records.append(rec)
            tick = "✓" if rec["correct"] else "✗"
            print(f"{tick}  pred={rec['predicted']}  conf={rec['max_prob']:.2f}")
        except Exception as e:
            print(f"ERROR: {e}")

    if not records:
        print("No files processed successfully.")
        sys.exit(1)

    for rec in records:
        stem = Path(rec["file"]).stem
        rec["effects"].to_csv(OUT_DIR / f"{stem}_effects.csv", index=False)

    summary_rows = []
    for rec in records:
        row = {
            "file":      rec["file"],
            "true":      rec["true"],
            "predicted": rec["predicted"],
            "correct":   rec["correct"],
            "prompt":    rec["prompt"],
            "run":       rec["run"],
            "max_prob":  rec["max_prob"],
            **{f"prob_{c}": rec["probs"][c] for c in CLASS_NAMES},
            **{f"top{i+1}_byte": int(rec["effects"].iloc[i]["byte_index"])
               for i in range(min(10, len(rec["effects"])))},
        }
        summary_rows.append(row)
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / f"{TASK_ID}_summary.csv", index=False)
    print(f"\nSaved {TASK_ID}_summary.csv ({len(summary_df)} rows)")

    print_summary(records)

    print("\nGenerating plots...")
    plot_accuracy_heatmap(records, OUT_DIR)
    plot_top_bytes(records, OUT_DIR)
    plot_shap_direction_per_byte(records, OUT_DIR)
    plot_all_ternary(records, OUT_DIR, expected_value=expected_value)

    print(f"\nAll outputs saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
