from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd
import shap


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_DATA_FILE = BASE_DIR / "features" / "processed_bytecode_features.csv"
MODEL_FILE = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

OUT_DIR = BASE_DIR / "shap_feature_selection"
OUT_FILE = OUT_DIR / "global_shap_importance.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COLUMN = "model"

METADATA_COLUMNS = [
    "file",
    "file_name",
    "filename",
    "path",
    "task",
    "task_id",
    "prompt",
    "prompt_id",
    "run",
    "run_id",
    "function_name",
    "bytecode_extract_status",
    "bytecode_extract_error",
    "original_byte_length",
    "was_truncated",
    "model",
]


def load_model():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)

    if isinstance(loaded, dict) and "model" in loaded:
        return loaded["model"]

    return loaded


def get_shap_array(shap_values):
    if isinstance(shap_values, list):
        return np.stack(shap_values, axis=-1)

    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values

    raise ValueError(f"Unexpected SHAP format: {type(shap_values)}, {getattr(shap_values, 'shape', None)}")


def main():
    df = pd.read_csv(TRAIN_DATA_FILE)

    report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
    trained_features = report["features"]
    class_names = report["classes"]

    X = df.drop(columns=[col for col in METADATA_COLUMNS if col in df.columns])

    for col in trained_features:
        if col not in X.columns:
            X[col] = 0

    X = X[trained_features]

    model = load_model()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    shap_arr = get_shap_array(shap_values)

    # shape: samples x features x classes
    global_importance = np.mean(
        np.sum(np.abs(shap_arr), axis=2),
        axis=0,
    )

    rows = []

    for i, feature in enumerate(trained_features):
        row = {
            "feature": feature,
            "global_importance": global_importance[i],
        }

        for class_idx, class_name in enumerate(class_names):
            row[f"importance_{class_name}"] = np.mean(
                np.abs(shap_arr[:, i, class_idx])
            )

        rows.append(row)

    importance_df = pd.DataFrame(rows)
    importance_df = importance_df.sort_values(
        "global_importance",
        ascending=False,
    ).reset_index(drop=True)

    importance_df.insert(0, "rank", importance_df.index + 1)

    importance_df.to_csv(OUT_FILE, index=False)

    print(f"Saved global SHAP importance to: {OUT_FILE}")
    print(f"Features ranked: {len(importance_df)}")


if __name__ == "__main__":
    main()
