"""
Exhaustive task-level 80/20 cross-validation for the bytecode LLM classifier.

Strategy:
  - Combine train (t1–t40) and test (t41–t50) into one dataset.
  - Each of the 50 tasks is treated as an atomic unit — all samples from
    a task must land in the same split (train or test).
  - Enumerate ALL unique ways to choose exactly 10 tasks (20 %) as the
    test set from 50, respecting task-level integrity.
    C(50, 10) = 10,272,278,170  — that is way too many to enumerate fully.
  - Instead: random sample N_SAMPLES splits, ensuring each split has
    ~20 % of tasks in the test set (exactly 10 tasks).
  - Record accuracy for every split, then plot distributions.

Outputs go to:  <project_root>/cross_validation/
"""

from pathlib import Path
import json
import random
import time
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_DATA_FILE = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_DATA_FILE  = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

OUT_DIR = BASE_DIR / "cross_validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Config ─────────────────────────────────────────────────────────────────
RANDOM_SEED   = 42
N_SAMPLES     = 500        # random splits to evaluate
TEST_N_TASKS  = 10         # exactly 10 tasks (20 %) held out each time
BASELINE_ACC  = 1 / 3      # random-chance for 3 classes

METADATA_COLUMNS = [
    "file", "file_name", "path",
    "task", "task_id",
    "prompt", "prompt_id",
    "run", "run_id",
    "model",
]

XGB_PARAMS = dict(
    n_estimators=800,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softprob",
    eval_metric="mlogloss",
    random_state=7,
    n_jobs=-1,
)

ORIGINAL_SPLIT_ACC = 0.4259   # the thesis disjoint split result


# ── Helpers ────────────────────────────────────────────────────────────────

def load_and_merge() -> pd.DataFrame:
    train = pd.read_csv(TRAIN_DATA_FILE)
    test  = pd.read_csv(TEST_DATA_FILE)
    df = pd.concat([train, test], ignore_index=True)
    print(f"Combined dataset: {len(df)} rows")
    return df


def get_task_ids(df: pd.DataFrame):
    # Task is encoded in file_name: t10_p1_r2_llama.py -> "t10"
    df["_task"] = df["file_name"].str.split("_").str[0]
    ids = sorted(df["_task"].unique())
    print(f"Unique tasks: {len(ids)}  (parsed from file_name)")
    return ids, "_task"


def split_df(df: pd.DataFrame, task_col: str, test_tasks: list):
    mask = df[task_col].isin(set(test_tasks))
    return df[~mask], df[mask]


def featurise(df: pd.DataFrame):
    drop = [c for c in METADATA_COLUMNS + ["_task"] if c in df.columns]
    X = df.drop(columns=drop)
    y = df["model"]
    return X, y


def align(X_tr, X_te):
    X_tr, X_te = X_tr.align(X_te, join="outer", axis=1, fill_value=0)
    cols = sorted(X_tr.columns)
    return X_tr[cols], X_te[cols]


def run_split(df, task_col, test_tasks) -> float:
    tr_df, te_df = split_df(df, task_col, test_tasks)
    X_tr, y_tr = featurise(tr_df)
    X_te, y_te = featurise(te_df)
    X_tr, X_te = align(X_tr, X_te)

    le = LabelEncoder()
    y_tr_enc = le.fit_transform(y_tr)

    clf = XGBClassifier(**XGB_PARAMS)
    clf.fit(X_tr, y_tr_enc)

    preds_enc = clf.predict(X_te)
    preds     = le.inverse_transform(preds_enc)
    return accuracy_score(y_te, preds)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    rng = random.Random(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    df = load_and_merge()
    task_ids, task_col = get_task_ids(df)

    assert len(task_ids) == 50, f"Expected 50 tasks, got {len(task_ids)}"

    # Sample N_SAMPLES distinct test-task subsets
    seen   = set()
    splits = []
    attempts = 0
    max_attempts = N_SAMPLES * 20

    while len(splits) < N_SAMPLES and attempts < max_attempts:
        attempts += 1
        test_tasks = tuple(sorted(rng.sample(task_ids, TEST_N_TASKS)))
        if test_tasks not in seen:
            seen.add(test_tasks)
            splits.append(test_tasks)

    print(f"Generated {len(splits)} unique splits (out of C(50,10) ≈ 10.3 B possible)")

    # Run every split
    accuracies = []
    t0 = time.time()

    for i, test_tasks in enumerate(splits):
        acc = run_split(df, task_col, list(test_tasks))
        accuracies.append(acc)
        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            eta = elapsed / (i + 1) * (len(splits) - i - 1)
            print(f"  [{i+1}/{len(splits)}]  acc={acc:.4f}  "
                  f"elapsed={elapsed:.0f}s  eta={eta:.0f}s")

    accuracies = np.array(accuracies)

    # ── Stats ──────────────────────────────────────────────────────────────
    stats = {
        "n_splits":          int(len(accuracies)),
        "mean_accuracy":     float(accuracies.mean()),
        "median_accuracy":   float(np.median(accuracies)),
        "std_accuracy":      float(accuracies.std()),
        "min_accuracy":      float(accuracies.min()),
        "max_accuracy":      float(accuracies.max()),
        "pct_above_baseline": float((accuracies > BASELINE_ACC).mean()),
        "pct_above_original": float((accuracies > ORIGINAL_SPLIT_ACC).mean()),
        "baseline":          BASELINE_ACC,
        "original_split_acc": ORIGINAL_SPLIT_ACC,
        "p10": float(np.percentile(accuracies, 10)),
        "p25": float(np.percentile(accuracies, 25)),
        "p75": float(np.percentile(accuracies, 75)),
        "p90": float(np.percentile(accuracies, 90)),
    }

    (OUT_DIR / "cv_stats.json").write_text(json.dumps(stats, indent=2))
    np.save(OUT_DIR / "cv_accuracies.npy", accuracies)

    print("\n── Cross-validation results ──────────────────────────────")
    for k, v in stats.items():
        print(f"  {k:<25} {v:.4f}" if isinstance(v, float) else f"  {k:<25} {v}")

    # ── Plots ──────────────────────────────────────────────────────────────
    STYLE = {
        "hist_color":    "#4C72B0",
        "hist_alpha":    0.72,
        "baseline_col":  "#E74C3C",
        "original_col":  "#2ECC71",
        "mean_col":      "#F39C12",
        "bg":            "#F8F9FA",
        "grid":          "#DEE2E6",
    }

    # 1. Histogram of accuracies
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_facecolor(STYLE["bg"])
    fig.patch.set_facecolor("white")

    ax.hist(accuracies, bins=30, color=STYLE["hist_color"],
            alpha=STYLE["hist_alpha"], edgecolor="white", linewidth=0.6)

    ax.axvline(BASELINE_ACC,        color=STYLE["baseline_col"],  lw=1.8,
               ls="--", label=f"Chance ({BASELINE_ACC:.3f})")
    ax.axvline(ORIGINAL_SPLIT_ACC,  color=STYLE["original_col"],  lw=1.8,
               ls="-.", label=f"Original split ({ORIGINAL_SPLIT_ACC:.4f})")
    ax.axvline(accuracies.mean(),   color=STYLE["mean_col"],      lw=1.8,
               ls=":",  label=f"CV mean ({accuracies.mean():.4f})")

    ax.set_xlabel("Test accuracy", fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    ax.set_title(f"Task-level 80/20 splits  —  {len(accuracies)} random draws",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, color=STYLE["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cv_histogram.png", dpi=150)
    plt.close(fig)

    # 2. Sorted accuracy ("robustness profile")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_facecolor(STYLE["bg"])
    fig.patch.set_facecolor("white")

    sorted_acc = np.sort(accuracies)
    ax.fill_between(range(len(sorted_acc)), BASELINE_ACC, sorted_acc,
                    where=(sorted_acc >= BASELINE_ACC),
                    alpha=0.3, color=STYLE["hist_color"], label="Above chance")
    ax.fill_between(range(len(sorted_acc)), sorted_acc, BASELINE_ACC,
                    where=(sorted_acc < BASELINE_ACC),
                    alpha=0.3, color=STYLE["baseline_col"], label="Below chance")
    ax.plot(sorted_acc, color=STYLE["hist_color"], lw=1.4)
    ax.axhline(BASELINE_ACC,       color=STYLE["baseline_col"], lw=1.6,
               ls="--", label=f"Chance ({BASELINE_ACC:.3f})")
    ax.axhline(ORIGINAL_SPLIT_ACC, color=STYLE["original_col"], lw=1.6,
               ls="-.", label=f"Original split ({ORIGINAL_SPLIT_ACC:.4f})")
    ax.axhline(accuracies.mean(),  color=STYLE["mean_col"], lw=1.6,
               ls=":", label=f"CV mean ({accuracies.mean():.4f})")

    ax.set_xlabel("Split rank (sorted by accuracy)", fontsize=11)
    ax.set_ylabel("Test accuracy", fontsize=11)
    ax.set_title("Robustness profile — all splits ranked", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, color=STYLE["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cv_robustness_profile.png", dpi=150)
    plt.close(fig)

    # 3. Box-plot (compact summary)
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.set_facecolor(STYLE["bg"])
    fig.patch.set_facecolor("white")

    bp = ax.boxplot(accuracies, patch_artist=True, widths=0.4,
                    medianprops=dict(color="white", lw=2),
                    boxprops=dict(facecolor=STYLE["hist_color"], alpha=0.8),
                    whiskerprops=dict(lw=1.4),
                    capprops=dict(lw=1.4),
                    flierprops=dict(marker="o", markersize=3,
                                   markerfacecolor=STYLE["hist_color"],
                                   alpha=0.5, linestyle="none"))

    ax.axhline(BASELINE_ACC,       color=STYLE["baseline_col"], lw=1.6,
               ls="--", label=f"Chance")
    ax.axhline(ORIGINAL_SPLIT_ACC, color=STYLE["original_col"], lw=1.6,
               ls="-.", label=f"Original split")

    ax.set_ylabel("Test accuracy", fontsize=11)
    ax.set_xticks([])
    ax.set_title("Accuracy distribution", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, color=STYLE["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cv_boxplot.png", dpi=150)
    plt.close(fig)

    # 4. Cumulative distribution (CDF)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_facecolor(STYLE["bg"])
    fig.patch.set_facecolor("white")

    xs = np.sort(accuracies)
    ys = np.arange(1, len(xs) + 1) / len(xs)
    ax.plot(xs, ys, color=STYLE["hist_color"], lw=2)
    ax.axvline(BASELINE_ACC,       color=STYLE["baseline_col"], lw=1.6,
               ls="--", label=f"Chance ({BASELINE_ACC:.3f})")
    ax.axvline(ORIGINAL_SPLIT_ACC, color=STYLE["original_col"], lw=1.6,
               ls="-.", label=f"Original split ({ORIGINAL_SPLIT_ACC:.4f})")
    ax.axvline(accuracies.mean(),  color=STYLE["mean_col"], lw=1.6,
               ls=":", label=f"CV mean ({accuracies.mean():.4f})")

    ax.set_xlabel("Test accuracy", fontsize=11)
    ax.set_ylabel("Cumulative fraction of splits", fontsize=11)
    ax.set_title("CDF of test accuracy across splits", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, color=STYLE["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cv_cdf.png", dpi=150)
    plt.close(fig)

    print(f"\nAll outputs saved to: {OUT_DIR}")
    print("  cv_stats.json")
    print("  cv_accuracies.npy")
    print("  cv_histogram.png")
    print("  cv_robustness_profile.png")
    print("  cv_boxplot.png")
    print("  cv_cdf.png")


if __name__ == "__main__":
    main()
