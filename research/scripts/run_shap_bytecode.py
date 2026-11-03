from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


BASE_DIR = Path(__file__).resolve().parent.parent

# ── both datasets ─────────────────────────────────────────────────────────────
TRAIN_FEATURES = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_FEATURES  = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

MODEL_FILE  = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

SHAP_DIR  = BASE_DIR / "shap_bytecode"
PLOTS_DIR = SHAP_DIR / "plots"

SHAP_VALUES_FILE        = SHAP_DIR / "shap_values_multiclass.npy"
SHAP_VALUES_TEST_FILE   = SHAP_DIR / "shap_values_multiclass_test.npy"
FEATURE_NAMES_FILE      = SHAP_DIR / "feature_names.json"
CLASS_NAMES_FILE        = SHAP_DIR / "class_names.json"
PRED_PROBS_FILE         = SHAP_DIR / "predicted_probabilities.csv"

SHAP_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

METADATA_COLUMNS = [
    "file", "file_name", "path", "task", "task_id",
    "prompt", "prompt_id", "run", "run_id", "model",
]


def get_class_shap_values(shap_values, class_index: int):
    if isinstance(shap_values, list):
        return shap_values[class_index]
    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_index]
    raise ValueError(f"Unexpected SHAP values shape/type: {type(shap_values)}, {getattr(shap_values, 'shape', None)}")


def load_model_bundle():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)
    if isinstance(loaded, dict) and "model" in loaded:
        return loaded["model"], loaded.get("label_encoder"), loaded.get("model_type", type(loaded["model"]).__name__)
    return loaded, None, type(loaded).__name__


def prepare_features(df: pd.DataFrame, trained_features: list[str]) -> pd.DataFrame:
    X = df.drop(columns=[col for col in METADATA_COLUMNS if col in df.columns])
    for col in trained_features:
        if col not in X.columns:
            X[col] = 0
    extra = [col for col in X.columns if col not in trained_features]
    if extra:
        X = X.drop(columns=extra)
    return X[trained_features]

def plot_cumulative_top_bytes(shap_values, feature_names, class_names, top_n=20):
    """
    Stacked bar chart of the top_n most important byte positions overall.
    Each bar's total height is the sum across classes of mean |SHAP|;
    segments show each class's contribution to that total.
    """
    per_class_importance = np.array([
        np.abs(get_class_shap_values(shap_values, ci)).mean(axis=0)
        for ci in range(len(class_names))
    ])  # shape: (n_classes, n_features)

    total_importance = per_class_importance.sum(axis=0)  # shape: (n_features,)

    order = np.argsort(total_importance)[::-1][:top_n]
    ordered_features = [feature_names[i].replace("byte_", "") for i in order]
    ordered_per_class = per_class_importance[:, order]  # (n_classes, top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(top_n)
    colors = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}

    x = np.arange(top_n)
    for ci, class_name in enumerate(class_names):
        ax.bar(
            x, ordered_per_class[ci],
            bottom=bottom,
            label=class_name,
            color=colors.get(class_name, None),
        )
        bottom += ordered_per_class[ci]

    ax.set_xticks(x)
    ax.set_xticklabels(ordered_features, rotation=45, ha="right", fontsize=20)
    ax.tick_params(axis="y", labelsize=20)
    ax.set_ylabel("Mean |SHAP value|", fontsize=22)
    ax.set_xlabel("Byte position", fontsize=22)
    ax.legend(fontsize=20)
    ax.set_xlim(-0.6, top_n - 0.4)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "cumulative_top20_bytes.png", dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved cumulative top-{top_n} bytes plot to {PLOTS_DIR / 'cumulative_top20_bytes.png'}")


def main():
    # ── load and combine both datasets ────────────────────────────────────────
    train_df = pd.read_csv(TRAIN_FEATURES)
    test_df  = pd.read_csv(TEST_FEATURES)
    df = pd.concat([train_df, test_df], ignore_index=True)
    print(f"Combined dataset: {len(train_df)} train + {len(test_df)} test = {len(df)} total files")

    y = df["model"]

    model, label_encoder, model_type = load_model_bundle()

    with REPORT_FILE.open("r", encoding="utf-8") as f:
        report_payload = json.load(f)

    trained_features = report_payload["features"]
    class_names      = report_payload["classes"]

    X            = prepare_features(df, trained_features)
    feature_names = list(X.columns)

    print(f"Running TreeSHAP on {len(X)} files (combined)...")
    explainer        = shap.TreeExplainer(model)
    shap_values      = explainer.shap_values(X)
    np.save(SHAP_VALUES_FILE, shap_values)
    print(f"Saved combined SHAP values to {SHAP_VALUES_FILE}")

    # also compute test-only SHAP for scatter plot
    X_test      = prepare_features(test_df, trained_features)
    print(f"Running TreeSHAP on {len(X_test)} test files only...")
    shap_values_test = explainer.shap_values(X_test)
    np.save(SHAP_VALUES_TEST_FILE, shap_values_test)
    print(f"Saved test-only SHAP values to {SHAP_VALUES_TEST_FILE}")
    FEATURE_NAMES_FILE.write_text(json.dumps(feature_names, indent=2), encoding="utf-8")
    CLASS_NAMES_FILE.write_text(json.dumps(class_names, indent=2), encoding="utf-8")

    probs    = model.predict_proba(X)
    probs_df = pd.DataFrame(probs, columns=[f"prob_{cls}" for cls in class_names])
    probs_df.insert(0, "row_id", df.index)
    probs_df.insert(1, "true_model", y)
    probs_df.insert(2, "file_name", df["file_name"])
    probs_df.to_csv(PRED_PROBS_FILE, index=False)

    for class_index, class_name in enumerate(class_names):
        class_shap = get_class_shap_values(shap_values, class_index)

        plt.rcParams.update({
            "font.size": 24,
            "axes.labelsize": 26,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
        })

        fig = plt.figure(figsize=(10, 12))
        shap.summary_plot(class_shap, X, show=False, max_display=9)
        ax = plt.gca()
        ax.set_xlabel("SHAP value (impact on model output)", fontsize=18)
        ax.tick_params(axis='y', labelsize=18)
        ax.tick_params(axis='x', labelsize=18)

        # adjust colorbar label if present
        for cb_ax in fig.axes[1:]:
            cb_ax.set_ylabel(cb_ax.get_ylabel(), fontsize=18)
            cb_ax.tick_params(labelsize=18)

        plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.12)
        plt.savefig(PLOTS_DIR / f"summary_beeswarm_bytecode_{class_name}.png", dpi=200)
        plt.close()

        plt.figure(figsize=(8, 7))
        shap.summary_plot(class_shap, X, plot_type="bar", show=False, max_display=9)
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / f"summary_bar_bytecode_{class_name}.png", dpi=200, bbox_inches="tight")
        plt.close()

    for class_index, class_name in enumerate(class_names):
        class_shap = get_class_shap_values(shap_values, class_index)
        explanation = shap.Explanation(
            values=class_shap[0],
            base_values=explainer.expected_value[class_index],
            data=X.iloc[0].values,
            feature_names=feature_names,
        )

        plt.figure(figsize=(10, 8))
        shap.plots.waterfall(explanation, max_display=8, show=False)
        fig = plt.gcf()
        ax = fig.axes[0]

        ax.tick_params(axis='y', labelsize=18)
        ax.tick_params(axis='x', labelsize=18)

        for t in ax.texts:
            t.set_fontsize(14)
        # adjust colorbar label if present
        for cb_ax in fig.axes[1:]:
            cb_ax.set_ylabel(cb_ax.get_ylabel(), fontsize=18)
            cb_ax.tick_params(labelsize=16)

        plt.tight_layout()
        plt.savefig(PLOTS_DIR / f"waterfall_bytecode_{class_name}.png", dpi=200, bbox_inches="tight")
        plt.close()
    plot_cumulative_top_bytes(shap_values, feature_names, class_names, top_n=20)

    print(f"Model type:    {model_type}")
    print(f"Total files:   {len(df)} ({len(train_df)} train + {len(test_df)} test)")
    print(f"Features:      {len(feature_names)}")
    print(f"Classes:       {class_names}")
    print(f"Saved SHAP values to:  {SHAP_VALUES_FILE}")
    print(f"Saved feature names to: {FEATURE_NAMES_FILE}")
    print(f"Saved probabilities to: {PRED_PROBS_FILE}")
    print(f"Saved plots to:        {PLOTS_DIR}")


if __name__ == "__main__":
    main()
