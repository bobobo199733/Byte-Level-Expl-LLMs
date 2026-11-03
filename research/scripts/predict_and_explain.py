"""
predict_and_explain.py

Runs TreeSHAP on a single generated Python file and produces two plots:
  1. Ternary SHAP byte-attribution path (probability simplex trajectory)
  2. Cumulative SHAP waterfall (3 parallel staircase lines, one per class)

Both plots share the same SHAP computation, so they always agree.

Baseline design:
  - Ternary: starts at the centroid (1/3, 1/3, 1/3); dashed residual arrow
    absorbs expected_value offset + remaining features, lands on predict_proba.
  - Waterfall: lines start at 0; colored steps show raw SHAP deltas; a final
    gray dashed step per class bridges to the actual model probability,
    absorbing expected_value + remaining features. Diamonds labeled with probs.

Usage:
    python scripts/predict_and_explain.py t47_p3_r2_llama.py
    python scripts/predict_and_explain.py t47_p3_r2_llama.py --top 15
    python scripts/predict_and_explain.py path/to/t47_p3_r2_llama.py --top 15
"""

import argparse
import json
import pickle
import sys
from pathlib import Path

import matplotlib.colors as mc
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
MODEL_FILE  = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"

sys.path.insert(0, str(BASE_DIR / "scripts"))
from bytecode_utils import preprocess_single_file

# ── constants ──────────────────────────────────────────────────────────────────
CLASS_NAMES   = ["llama", "mistral", "qwen"]
COLORS        = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
FONT_FAMILY   = "DejaVu Sans"
CORNER_OFFSET = 0.07
SHOW_TITLES = False

# font sizes for waterfall plot (tuned for 0.8\textwidth in LaTeX)
FS_YTICK   = 13
FS_XLABEL  = 15
FS_DELTA   = 11
FS_FINAL   = 13
FS_BASE    = 12
FS_LEGEND  = 14
FS_TITLE   = 16


# ══════════════════════════════════════════════════════════════════════════════
# shared helpers
# ══════════════════════════════════════════════════════════════════════════════

def load_model_bundle():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)
    if isinstance(loaded, dict) and "model" in loaded:
        return loaded["model"], loaded.get("label_encoder"), loaded.get("model_type")
    return loaded, None, type(loaded).__name__


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def load_target_function(task_id: str) -> str:
    meta_file = PROMPTS_DIR / task_id / "meta.json"
    if not meta_file.exists():
        raise FileNotFoundError(f"Missing meta.json: {meta_file}")
    return json.loads(meta_file.read_text(encoding="utf-8"))["function_name"]


def align_features(X: pd.DataFrame, trained_features: list[str]) -> pd.DataFrame:
    for col in trained_features:
        if col not in X.columns:
            X[col] = 0
    extra = [c for c in X.columns if c not in trained_features]
    if extra:
        X = X.drop(columns=extra)
    return X[trained_features]


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


def ternary_to_xy(probs):
    llama, mistral, qwen = probs
    return mistral + 0.5 * qwen, (np.sqrt(3) / 2) * qwen


def build_effects_df(X: pd.DataFrame, shap_values) -> pd.DataFrame:
    rows = []
    for j, feat in enumerate(X.columns):
        effect_vec = np.array([get_class_shap(shap_values, ci)[0, j]
                               for ci in range(3)])
        rows.append({
            "feature":    feat,
            "byte_index": int(feat.replace("byte_", "")),
            "value":      float(X.iloc[0, j]),
            **{f"shap_{c}": float(effect_vec[ci])
               for ci, c in enumerate(CLASS_NAMES)},
            "magnitude":  float(np.linalg.norm(effect_vec)),
        })
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# ternary plot
# ══════════════════════════════════════════════════════════════════════════════

def _draw_triangle(ax):
    h      = np.sqrt(3) / 2
    cx, cy = 0.5, h / 3
    corners = {"llama": (0, 0), "mistral": (1, 0), "qwen": (0.5, h)}

    ax.plot([0, 1, 0.5, 0], [0, 0, h, 0],
            color="#444444", linewidth=1.8, zorder=1)

    for mx, my in [(0.75, h / 2), (0.25, h / 2), (0.5, 0)]:
        ax.plot([cx, mx], [cy, my],
                color="#cccccc", linewidth=0.6, linestyle="--", zorder=0)

    for cls, (x, y) in corners.items():
        ax.scatter([x], [y], s=160, color=COLORS[cls],
                   zorder=5, edgecolors="white", linewidths=1.2)
        dx, dy = x - cx, y - cy
        norm   = (dx**2 + dy**2) ** 0.5
        lx, ly = x + dx / norm * CORNER_OFFSET, y + dy / norm * CORNER_OFFSET
        ax.text(lx, ly, cls,
                ha="center", va="center",
                fontsize=14, fontweight="bold",
                color=COLORS[cls], fontfamily=FONT_FAMILY,
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])

    ax.set_aspect("equal")
    ax.axis("off")


def plot_ternary(effects_df: pd.DataFrame, expected_value, model_probs,
                 file_meta: dict, top_n: int, out_path: Path):
    """Ternary SHAP trajectory — top_n arrows sorted by magnitude.

    Baseline (×) is fixed at the centroid (1/3, 1/3, 1/3) — equal uncertainty
    across all three classes. The dashed gray residual arrow absorbs both the
    expected_value offset and the remaining features, always landing exactly
    on the true predict_proba star (★).
    """
    plot_df = (effects_df
               .sort_values("magnitude", ascending=False)
               .head(top_n)
               .copy())

    # zero logits → softmax gives exact centroid (1/3, 1/3, 1/3)
    raw           = np.zeros(len(CLASS_NAMES), dtype=float)
    points_logits = [raw.copy()]
    for _, row in plot_df.iterrows():
        raw = raw + np.array([row[f"shap_{c}"] for c in CLASS_NAMES])
        points_logits.append(raw.copy())

    points    = np.array([softmax(p) for p in points_logits])
    xy_points = np.array([ternary_to_xy(p) for p in points])
    deltas    = np.linalg.norm(xy_points[1:] - xy_points[:-1], axis=1)
    max_dist  = deltas.max() if deltas.max() > 0 else 1.0

    fig, ax = plt.subplots(figsize=(9, 8))
    fig.patch.set_facecolor("white")
    _draw_triangle(ax)

    # baseline at centroid
    cx, cy = ternary_to_xy([1/3, 1/3, 1/3])
    ax.scatter([cx], [cy], marker="X", s=140, color="#333333",
               zorder=6, label="baseline (centroid)",
               edgecolors="white", linewidths=0.8)

    for i, (_, row) in enumerate(plot_df.iterrows()):
        x1, y1 = xy_points[i]
        x2, y2 = xy_points[i + 1]

        delta_prob = points[i + 1] - points[i]
        color      = COLORS[CLASS_NAMES[int(np.argmax(delta_prob))]]
        norm_dist  = deltas[i] / max_dist

        ax.annotate(
            "",
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->", color=color,
                linewidth=max(1, norm_dist * 3.0),
                alpha=0.85,
                mutation_scale=max(8, norm_dist * 16),
                shrinkA=0, shrinkB=0,
            ),
        )
        if norm_dist > 0.47:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my, str(int(row["byte_index"])),
                    fontsize=8, ha="center", va="center",
                    color="#222222", zorder=10, fontfamily=FONT_FAMILY,
                    bbox=dict(boxstyle="round,pad=0.2",
                              fc="white", ec="#cccccc",
                              alpha=0.5, linewidth=0.8))

    # residual arrow: top-N endpoint → true model prediction
    # absorbs expected_value offset + all remaining features
    mp       = np.array([model_probs[c] for c in CLASS_NAMES], dtype=float)
    final_xy = ternary_to_xy(mp)
    ax.annotate(
        "",
        xy=(final_xy[0], final_xy[1]),
        xytext=(xy_points[-1][0], xy_points[-1][1]),
        arrowprops=dict(
            arrowstyle="->", color="#888888",
            linewidth=1.5, alpha=0.6,
            linestyle="dashed", mutation_scale=10,
            shrinkA=0, shrinkB=0,
        ),
    )
    ax.scatter(*final_xy, marker="*", s=280, color="#222222",
               zorder=8, label="model prediction",
               edgecolors="white", linewidths=0.8)

    endpoint_class = CLASS_NAMES[int(np.argmax(points[-1]))]
    verdict        = "✓" if file_meta["true"] == file_meta["predicted"] else "✗"

    if SHOW_TITLES:
        ax.set_title(
            f"Ternary SHAP byte-attribution path\n"
            f"task={file_meta['task']}  prompt={file_meta['prompt']}  "
            f"run={file_meta['run']}  "
            f"true={file_meta['true']}  pred={file_meta['predicted']} {verdict}\n"
            f"features shown = {len(plot_df)}",
            fontsize=12, pad=24, fontfamily=FONT_FAMILY, color="#222222",
        )

    # legend = ax.legend(loc="upper right", fontsize=10,
    #                    framealpha=0.9, edgecolor="#cccccc", fancybox=True)
    # for text in legend.get_texts():
    #     text.set_fontfamily(FONT_FAMILY)


    plt.tight_layout()
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"Saved {out_path.name}")
    return endpoint_class


# ══════════════════════════════════════════════════════════════════════════════
# cumulative waterfall plot
# ══════════════════════════════════════════════════════════════════════════════

def _lighten(hex_color: str, factor: float = 0.45) -> tuple:
    rgb = mc.to_rgb(hex_color)
    return tuple(1 - (1 - ch) * factor for ch in rgb)


def plot_waterfall(effects_df: pd.DataFrame, expected_value,
                   predicted: str, correct: bool,
                   filename: str, top_n: int, out_path: Path):
    """
    Cumulative SHAP waterfall. Lines start at 0; colored steps show raw SHAP
    deltas for the top_n features. A final gray dashed step per class bridges
    from the top-N cumulative sum to the actual model probability, absorbing
    the expected_value offset and all remaining features. Diamonds are labeled
    with the final model probability so the endpoint is always interpretable.
    """
    df = effects_df.sort_values("magnitude", ascending=False).copy()

    top  = df.head(top_n)
    rest = df.iloc[top_n:]

    # final model probability per class = softmax(expected_value + all shap)
    ev   = np.array(expected_value, dtype=float)
    all_shap_sum = np.array([
        df[f"shap_{c}"].sum() for c in CLASS_NAMES
    ])
    final_probs = softmax(ev + all_shap_sum)   # matches predict_proba

    # top-N cumulative sums (raw SHAP, no expected_value)
    top_shap_sum = np.array([top[f"shap_{c}"].sum() for c in CLASS_NAMES])

    # residual per class: from top-N sum to final probability
    # this is what the gray step covers
    residual = final_probs - top_shap_sum  # in mixed space, just a visual bridge

    n_steps = top_n + 1   # top_n colored steps + 1 gray residual step
    tick    = "✓" if correct else "✗"
    title   = f"{filename}\nPredicted: {predicted}  {tick}"

    # build display rows: top features + residual row
    rest_label = f"({len(rest)} other features + base)"
    display_shap = []
    for _, row in top.iterrows():
        display_shap.append({c: row[f"shap_{c}"] for c in CLASS_NAMES})

    # residual step: expected_value + remaining SHAP (all in logit space)
    display_shap.append({
        c: float(ev[ci]) + rest[f"shap_{c}"].sum()
        for ci, c in enumerate(CLASS_NAMES)
    })

    y_labels = []
    for _, row in top.iterrows():
        feat = str(row["feature"])
        val  = row.get("value", float("nan"))
        val_str = str(int(val)) if pd.notna(val) else "?"
        y_labels.append(f"{feat} (val={val_str})")
    y_labels.append(rest_label)

    fig, ax = plt.subplots(figsize=(11, max(6, n_steps * 0.55 + 2)))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")
    ax.tick_params(axis="x", labelsize=FS_YTICK)

    lane = {"llama": 0.2, "mistral": 0.0, "qwen": -0.2}

    for model_idx, model in enumerate(CLASS_NAMES):
        color       = COLORS[model]
        color_light = _lighten(color)
        off_y       = lane[model]

        x = [0.0]
        for step in display_shap:
            x.append(x[-1] + step[model])

        for i in range(n_steps):
            y_base  = n_steps - i
            y_line  = y_base + off_y
            x_from  = x[i]
            x_to    = x[i + 1]
            is_gray = (i == n_steps - 1)   # last step is the residual

            line_color = color if x_to >= x_from else color_light
            dot_color  = color if x_to >= x_from else color_light

            if is_gray:
                # residual step: same color as class, dashed to distinguish
                ax.plot([x_from, x_to], [y_line, y_line],
                        color=color, linewidth=2.5, alpha=0.6,
                        linestyle="dashed", solid_capstyle="round")
                ax.scatter(x_to, y_line, color=color, s=20, zorder=5, alpha=0.6)
            else:
                ax.plot([x_from, x_to], [y_line, y_line],
                        color=line_color, linewidth=2.5, alpha=0.95,
                        solid_capstyle="round")
                ax.scatter(x_to, y_line, color=dot_color, s=20, zorder=5)

                # vertical connector to next step
                if i < n_steps - 2:
                    y_next = (n_steps - i - 1) + off_y
                    ax.plot([x_to, x_to], [y_line, y_next],
                            color=color, linewidth=1.0, alpha=0.4,
                            linestyle="--")

                # delta label on predicted class
                if model == predicted and abs(x_to - x_from) > 0.01:
                    ha   = "left"  if x_to > x_from else "right"
                    loff = 0.005   if x_to > x_from else -0.005
                    ax.text(x_to + loff, y_line + 0.07,
                            f"{x_to - x_from:+.3f}",
                            fontsize=FS_DELTA, color=color, ha=ha, va="bottom")

        ax.scatter(x[-1], 0, color=color, s=60, zorder=6, marker="D")
        ax.text(x[-1], 0.45, f"{x[-1]:+.3f}",
                fontsize=FS_FINAL, color=color, ha="center", va="top",
                fontweight="bold")

    ax.axvline(0, color="#555", linewidth=1.2, zorder=4)
    ax.text(0, n_steps + 0.3, "base\n(0)", fontsize=FS_BASE,
            color="#666", ha="center", va="bottom")

    ax.set_yticks(range(1, n_steps + 1))
    ax.set_yticklabels(y_labels[::-1], fontsize=FS_YTICK, fontfamily="monospace")
    ax.set_ylim(0, n_steps + 0.8)
    ax.set_xlabel("Cumulative SHAP value", fontsize=FS_XLABEL)
    if SHOW_TITLES:
        ax.set_title(title, fontsize=FS_TITLE, pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    # legend: colored patches, placed below the plot
    handles = [mpatches.Patch(color=COLORS[m], alpha=0.85, label=m)
               for m in CLASS_NAMES]
    ax.legend(handles=handles, fontsize=FS_LEGEND, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), ncol=3, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Run TreeSHAP on a single file and produce ternary + waterfall plots."
    )
    parser.add_argument("filename",
                        help="Generated Python file, e.g. t47_p3_r2_llama.py")
    parser.add_argument("--top-ternary", type=int, default=16,
                        help="Number of top features in ternary plot (default: 16)")
    parser.add_argument("--top-waterfall", type=int, default=10,
                        help="Number of top features in waterfall plot (default: 10)")
    args = parser.parse_args()

    py_file = Path(args.filename).resolve()
    if not py_file.exists():
        raise FileNotFoundError(py_file)

    # parse metadata from filename: t41_p1_r1_llama.py
    parts      = py_file.stem.split("_")
    task_id    = parts[0] if len(parts) > 0 else "?"
    prompt_id  = parts[1] if len(parts) > 1 else "?"
    run_id     = parts[2] if len(parts) > 2 else "?"
    true_model = parts[3] if len(parts) > 3 else "?"

    # ── load model + report ────────────────────────────────────────────────
    report           = load_report()
    trained_features = report["features"]
    class_names      = report["classes"]

    model, label_encoder, model_type = load_model_bundle()

    # ── preprocess ────────────────────────────────────────────────────────
    target_fn = load_target_function(task_id)
    X = preprocess_single_file(py_file, trained_features, target_fn)
    X = align_features(X, trained_features)

    # ── predict ───────────────────────────────────────────────────────────
    probs       = model.predict_proba(X)
    predicted   = class_names[int(np.argmax(probs[0]))]
    correct     = predicted == true_model
    model_probs = {c: float(p) for c, p in zip(class_names, probs[0])}

    # ── SHAP — computed once, shared by both plots ─────────────────────────
    explainer      = shap.TreeExplainer(model)
    shap_values    = explainer.shap_values(X)
    expected_value = explainer.expected_value

    effects_df = build_effects_df(X, shap_values)

    # ── output directory ──────────────────────────────────────────────────
    out_dir = BASE_DIR / "analysis" / task_id / "bytecode_viz"
    out_dir.mkdir(parents=True, exist_ok=True)

    stem           = py_file.stem
    ternary_path   = out_dir / f"{stem}_ternary.png"
    waterfall_path = out_dir / f"{stem}_waterfall.png"

    # ── plot 1: ternary ────────────────────────────────────────────────────
    file_meta = {
        "task":      task_id,
        "prompt":    prompt_id,
        "run":       run_id,
        "true":      true_model,
        "predicted": predicted,
    }
    endpoint_class = plot_ternary(
        effects_df=effects_df,
        expected_value=expected_value,
        model_probs=model_probs,
        file_meta=file_meta,
        top_n=args.top_ternary,
        out_path=ternary_path,
    )

    # ── plot 2: waterfall ──────────────────────────────────────────────────
    plot_waterfall(
        effects_df=effects_df,
        expected_value=expected_value,
        predicted=predicted,
        correct=correct,
        filename=py_file.name,
        top_n=args.top_waterfall,
        out_path=waterfall_path,
    )

    # ── summary ───────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("LOCAL SHAP EXPLANATION COMPLETE")
    print("=" * 60)
    print(f"File:             {py_file.name}")
    print(f"Model type:       {model_type}")
    print(f"True label:       {true_model}")
    print(f"Model prediction: {predicted}  {'✓' if correct else '✗'}")
    print()
    print("Model probabilities:")
    for cls, prob in model_probs.items():
        print(f"  {cls}: {prob:.4f}")
    print()
    print(f"SHAP endpoint class (top-{args.top_ternary} arrows): {endpoint_class}")
    print()
    print(f"Outputs → {out_dir}")
    print(f"  {ternary_path.name}")
    print(f"  {waterfall_path.name}")


if __name__ == "__main__":
    main()
