from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FEATURES = BASE_DIR / "features" / "processed_features.csv"
MODEL_FILE = BASE_DIR / "models" / "score_model.pkl"

SHAP_DIR = BASE_DIR / "shap"
PLOTS_DIR = SHAP_DIR / "plots"

SHAP_VALUES_FILE = SHAP_DIR / "shap_values.npy"
FEATURE_NAMES_FILE = SHAP_DIR / "feature_names.json"

SHAP_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(PROCESSED_FEATURES)

    y = df["score"]
    X = df.drop(columns=["score"])

    with MODEL_FILE.open("rb") as f:
        model = pickle.load(f)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    np.save(SHAP_VALUES_FILE, shap_values)
    FEATURE_NAMES_FILE.write_text(
        json.dumps(list(X.columns), indent=2),
        encoding="utf-8"
    )

    # Beeswarm plot
    plt.figure()
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "summary_beeswarm.png", dpi=200, bbox_inches="tight")
    plt.close()

    # Bar plot
    plt.figure()
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "summary_bar.png", dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved SHAP values to: {SHAP_VALUES_FILE}")
    print(f"Saved feature names to: {FEATURE_NAMES_FILE}")
    print(f"Saved plots to: {PLOTS_DIR}")


if __name__ == "__main__":
    main()
