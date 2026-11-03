"""
qwen_collapse_analysis.py

Tests the "Qwen collapse" hypothesis:
  - Are misclassified Qwen files predicted with high confidence?
  - Does Qwen lack a strong model-specific signal compared to LLaMA/Mistral?

Loads test-set predictions from analysis/{task}/{task}_summary.csv.
Recomputes predicted probabilities from the saved classifier + features CSV
(since probabilities are not stored in summary CSVs).

Run from project root:
    python scripts/qwen_collapse_analysis.py

Outputs:
    analysis/qwen_collapse/  -- all plots + CSV summary
"""

import json
import pickle
import warnings
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

warnings.filterwarnings("ignore")

# ── paths (discovered from repo structure) ────────────────────────────────
BASE_DIR          = Path(__file__).resolve().parent.parent
MODEL_FILE        = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE       = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
ANALYSIS_DIR      = BASE_DIR / "analysis"
OUT_DIR           = ANALYSIS_DIR / "qwen_collapse"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TASKS       = [f"t{i}" for i in range(41, 51)]
CLASS_NAMES = ["llama", "mistral", "qwen"]
COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}

SHOW_TITLES = False

# font sizes
FS_TITLE  = 14
FS_LABEL  = 13
FS_TICK   = 12
FS_LEGEND = 11


# ══════════════════════════════════════════════════════════════════════════════
# 1. load model + features
# ══════════════════════════════════════════════════════════════════════════════

def load_model():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)
    if isinstance(loaded, dict) and "model" in loaded:
        return loaded["model"], loaded.get("label_encoder"), loaded.get("model_type")
    return loaded, None, type(loaded).__name__


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def load_predictions():
    """Load true/predicted labels from summary CSVs."""
    rows = []
    files_used = []
    for task in TASKS:
        summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
        if not summary_path.exists():
            print(f"  WARNING: {summary_path} not found, skipping")
            continue
        files_used.append(str(summary_path))
        summary = pd.read_csv(summary_path)
        for _, rec in summary.iterrows():
            rows.append({
                "task":      task,
                "file":      rec["file"],
                "true":      rec["true"],
                "predicted": rec.get("predicted", None),
                "correct":   bool(rec["correct"]),
            })
    return pd.DataFrame(rows), files_used


# ══════════════════════════════════════════════════════════════════════════════
# 2. compute probabilities
# ══════════════════════════════════════════════════════════════════════════════

def compute_probabilities(pred_df, model, trained_features, class_names):
    """
    For each file in pred_df, look up its feature vector from the
    test features CSV and run predict_proba.
    Returns pred_df with added columns: prob_llama, prob_mistral, prob_qwen,
    confidence, predicted_from_proba.
    """
    feat_df = pd.read_csv(TEST_FEATURES_CSV)
    # index by file_name (strip .py if present)
    feat_df["stem"] = feat_df["file_name"].str.replace(".py", "", regex=False)
    feat_df = feat_df.set_index("stem")

    prob_rows = []
    missing   = []
    for _, rec in pred_df.iterrows():
        stem = Path(rec["file"]).stem
        if stem not in feat_df.index:
            missing.append(stem)
            prob_rows.append({c: np.nan for c in class_names})
            continue

        X = feat_df.loc[[stem], [f for f in trained_features
                                  if f in feat_df.columns]]
        # fill any missing features with 0
        for col in trained_features:
            if col not in X.columns:
                X[col] = 0
        X = X[trained_features]

        probs = model.predict_proba(X)[0]
        prob_rows.append({c: float(p) for c, p in zip(class_names, probs)})

    if missing:
        print(f"  WARNING: {len(missing)} files not found in features CSV")

    prob_df = pd.DataFrame(prob_rows, index=pred_df.index)
    out     = pd.concat([pred_df, prob_df], axis=1)
    out["confidence"]          = out[[f for f in class_names]].max(axis=1)
    out["predicted_from_proba"] = out[[f for f in class_names]].idxmax(axis=1)
    return out


# ══════════════════════════════════════════════════════════════════════════════
# 3. stats + interpretation
# ══════════════════════════════════════════════════════════════════════════════

def print_confidence_stats(df):
    print("\n" + "=" * 65)
    print("CONFIDENCE STATISTICS (correct vs incorrect, per true model)")
    print("=" * 65)
    for model in CLASS_NAMES:
        sub = df[df["true"] == model]
        cor = sub[sub["correct"]]["confidence"]
        inc = sub[~sub["correct"]]["confidence"]
        print(f"\n  {model.upper()} (n={len(sub)}, correct={len(cor)}, "
              f"incorrect={len(inc)})")
        for label, vals in [("correct  ", cor), ("incorrect", inc)]:
            if len(vals) == 0:
                continue
            print(f"    {label}: mean={vals.mean():.3f}  "
                  f"median={vals.median():.3f}  "
                  f"std={vals.std():.3f}  "
                  f"min={vals.min():.3f}  "
                  f"max={vals.max():.3f}")
        # Mann-Whitney U test
        if len(cor) >= 3 and len(inc) >= 3:
            stat, p = stats.mannwhitneyu(cor, inc, alternative="greater")
            print(f"    Mann-Whitney U (correct > incorrect): "
                  f"U={stat:.1f}, p={p:.4f}"
                  + (" *" if p < 0.05 else ""))


def print_confusion_confidence(df):
    print("\n" + "=" * 65)
    print("MEAN CONFIDENCE BY (true_label, predicted_label)")
    print("=" * 65)
    grp = df.groupby(["true", "predicted"])["confidence"].agg(
        ["mean", "count"]).round(3)
    print(grp.to_string())


def print_qwen_interpretation(df):
    print("\n" + "=" * 65)
    print("QWEN COLLAPSE INTERPRETATION")
    print("=" * 65)
    qdf = df[df["true"] == "qwen"]

    # misclassification targets
    mis = qdf[~qdf["correct"]]
    print(f"\n  Qwen misclassifications: {len(mis)}/{len(qdf)}")
    print(f"  Misclassified as llama:   "
          f"{(mis['predicted']=='llama').sum()} "
          f"({(mis['predicted']=='llama').mean():.0%})")
    print(f"  Misclassified as mistral: "
          f"{(mis['predicted']=='mistral').sum()} "
          f"({(mis['predicted']=='mistral').mean():.0%})")

    # confidence of misclassifications
    print(f"\n  Confidence of Qwen misclassifications:")
    print(f"    mean={mis['confidence'].mean():.3f}  "
          f"median={mis['confidence'].median():.3f}  "
          f"std={mis['confidence'].std():.3f}")
    print(f"    high-confidence (>0.5) misclassifications: "
          f"{(mis['confidence']>0.5).sum()}/{len(mis)} "
          f"({(mis['confidence']>0.5).mean():.0%})")
    print(f"    high-confidence (>0.7) misclassifications: "
          f"{(mis['confidence']>0.7).sum()}/{len(mis)} "
          f"({(mis['confidence']>0.7).mean():.0%})")

    # compare qwen correct confidence vs llama/mistral correct
    print(f"\n  Mean confidence of CORRECT predictions:")
    for model in CLASS_NAMES:
        cor = df[(df["true"]==model) & df["correct"]]["confidence"]
        print(f"    {model:8s}: mean={cor.mean():.3f}  n={len(cor)}")

    print(f"\n  Interpretation:")
    qwen_mis_conf = mis["confidence"].mean()
    llama_cor_conf = df[(df["true"]=="llama") & df["correct"]]["confidence"].mean()
    if qwen_mis_conf > 0.5:
        print(f"    Qwen is misclassified with HIGH confidence "
              f"(mean={qwen_mis_conf:.3f}) -- the classifier is not")
        print(f"    uncertain when it misclassifies Qwen; it confidently")
        print(f"    assigns Qwen files to LLaMA or Mistral. This SUPPORTS")
        print(f"    the hypothesis that Qwen lacks a strong model-specific")
        print(f"    signal: Qwen's bytecode actively looks like the other")
        print(f"    two models' code, rather than being merely ambiguous.")
    else:
        print(f"    Qwen is misclassified with LOW confidence "
              f"(mean={qwen_mis_conf:.3f}) -- the classifier IS")
        print(f"    uncertain. This PARTIALLY supports the hypothesis:")
        print(f"    Qwen's bytecode is ambiguous, but not strongly")
        print(f"    associated with LLaMA/Mistral patterns.")


# ══════════════════════════════════════════════════════════════════════════════
# 4. plots
# ══════════════════════════════════════════════════════════════════════════════

def plot_confidence_correct_vs_incorrect(df):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=False)
    fig.patch.set_facecolor("white")

    for i, model in enumerate(CLASS_NAMES):
        ax  = axes[i]
        sub = df[df["true"] == model]
        cor = sub[sub["correct"]]["confidence"]
        inc = sub[~sub["correct"]]["confidence"]

        bins = np.linspace(0.3, 1.0, 20)
        ax.hist(cor, bins=bins, alpha=0.7, color=COLORS[model],
                label=f"correct (n={len(cor)})", density=True)
        ax.hist(inc, bins=bins, alpha=0.5, color=COLORS[model],
                label=f"incorrect (n={len(inc)})", density=True,
                hatch="//", edgecolor="white")
        ax.set_title(model, fontsize=FS_LABEL, fontweight="bold",
                     color=COLORS[model])
        ax.set_xlabel("confidence", fontsize=FS_LABEL)
        ax.set_ylabel("density", fontsize=FS_LABEL)
        ax.tick_params(labelsize=FS_TICK)
        ax.legend(fontsize=FS_LEGEND)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUT_DIR / "confidence_correct_vs_incorrect.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved {out.name}")


def plot_confidence_per_model(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("white")

    bins = np.linspace(0.3, 1.0, 25)
    for model in CLASS_NAMES:
        sub = df[df["true"] == model]["confidence"]
        ax.hist(sub, bins=bins, alpha=0.6, color=COLORS[model],
                label=model, density=True)

    ax.set_xlabel("confidence", fontsize=FS_LABEL)
    ax.set_ylabel("density", fontsize=FS_LABEL)
    ax.tick_params(labelsize=FS_TICK)
    ax.legend(fontsize=FS_LEGEND)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    out = OUT_DIR / "confidence_per_model.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved {out.name}")


def plot_confusion_matrix(df):
    cm = confusion_matrix(df["true"], df["predicted"],
                          labels=CLASS_NAMES)
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor("white")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=CLASS_NAMES)
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.tick_params(labelsize=FS_TICK)
    plt.tight_layout()
    out = OUT_DIR / "confusion_matrix.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved {out.name}")


def plot_violin_confidence(df):
    FS_V_TITLE  = 22
    FS_V_LABEL  = 20
    FS_V_TICK   = 18

    fig, axes = plt.subplots(1, 3, figsize=(14, 6), sharey=True)
    fig.patch.set_facecolor("white")

    for i, model in enumerate(CLASS_NAMES):
        ax       = axes[i]
        sub      = df[df["true"] == model]
        data_cor = sub[sub["correct"]]["confidence"].values
        data_inc = sub[~sub["correct"]]["confidence"].values

        parts = ax.violinplot(
            [data_cor, data_inc],
            positions=[0, 1],
            showmedians=True,
            showextrema=True,
        )
        for pc, color in zip(parts["bodies"], [COLORS[model], "#cccccc"]):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)

        # median/whisker line styling
        for partname in ("cmedians", "cmins", "cmaxes", "cbars"):
            if partname in parts:
                parts[partname].set_linewidth(1.8)
                parts[partname].set_color("#333333")

        # add n= annotations
        ax.text(0, 0.28, f"n={len(data_cor)}", ha="center",
                fontsize=FS_V_TICK - 1, color="#444")
        ax.text(1, 0.28, f"n={len(data_inc)}", ha="center",
                fontsize=FS_V_TICK - 1, color="#444")

        ax.set_xticks([0, 1])
        ax.set_xticklabels(["correct", "incorrect"], fontsize=FS_V_TICK)
        ax.set_title(model, fontsize=FS_V_TITLE, fontweight="bold",
                     color=COLORS[model], pad=10)
        ax.set_ylabel("confidence", fontsize=FS_V_LABEL)
        ax.tick_params(axis="y", labelsize=FS_V_TICK)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylim(0.25, 1.05)

    plt.tight_layout()
    out = OUT_DIR / "violin_confidence.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved {out.name}")


def plot_confusion_pair_confidence(df):
    """Confidence distribution for each (true, predicted) pair."""
    pairs = [(t, p) for t in CLASS_NAMES for p in CLASS_NAMES]
    n     = len(pairs)
    fig, axes = plt.subplots(3, 3, figsize=(12, 10), sharey=False)
    fig.patch.set_facecolor("white")

    for idx, (true_m, pred_m) in enumerate(pairs):
        ax  = axes[idx // 3][idx % 3]
        sub = df[(df["true"] == true_m) & (df["predicted"] == pred_m)]
        ax.set_facecolor("#f9f9f9")

        if len(sub) == 0:
            ax.text(0.5, 0.5, "n=0", ha="center", va="center",
                    transform=ax.transAxes, fontsize=FS_TICK, color="#aaa")
        else:
            color  = COLORS[true_m] if true_m == pred_m else "#888888"
            bins   = np.linspace(0.3, 1.0, 15)
            ax.hist(sub["confidence"], bins=bins, color=color,
                    alpha=0.8, density=True)
            ax.axvline(sub["confidence"].mean(), color="#333",
                       linewidth=1.5, linestyle="--",
                       label=f"mean={sub['confidence'].mean():.2f}")
            ax.legend(fontsize=8)

        correct_flag = "✓" if true_m == pred_m else "✗"
        ax.set_title(f"true={true_m} → pred={pred_m}  {correct_flag}  "
                     f"n={len(sub)}", fontsize=9)
        ax.set_xlabel("confidence", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = OUT_DIR / "confusion_pair_confidence.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved {out.name}")


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("Loading model and report...")
    model, label_encoder, model_type = load_model()
    report          = load_report()
    trained_features = report["features"]
    class_names      = report["classes"]
    print(f"  Model type:     {model_type}")
    print(f"  Classes:        {class_names}")
    print(f"  Features:       {len(trained_features)}")

    print("\nLoading predictions from summary CSVs...")
    pred_df, files_used = load_predictions()
    print(f"  Files used ({len(files_used)}):")
    for f in files_used:
        print(f"    {f}")
    print(f"  Total records: {len(pred_df)}")

    print("\nComputing predicted probabilities...")
    df = compute_probabilities(pred_df, model, trained_features, class_names)
    df = df.dropna(subset=["confidence"])
    print(f"  Records with probabilities: {len(df)}")

    # save full results
    out_csv = OUT_DIR / "predictions_with_confidence.csv"
    df.to_csv(out_csv, index=False)
    print(f"  Saved {out_csv.name}")

    # stats
    print_confidence_stats(df)
    print_confusion_confidence(df)
    print_qwen_interpretation(df)

    # plots
    print("\nGenerating plots...")
    plot_confusion_matrix(df)
    plot_confidence_correct_vs_incorrect(df)
    plot_confidence_per_model(df)
    plot_violin_confidence(df)
    plot_confusion_pair_confidence(df)

    print(f"\nAll outputs saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
