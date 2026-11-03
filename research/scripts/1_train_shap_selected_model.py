from pathlib import Path
import sys
import json
import pickle

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_DATA_FILE = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_DATA_FILE = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

IMPORTANCE_FILE = BASE_DIR / "shap_feature_selection" / "global_shap_importance.csv"

OUT_DIR = BASE_DIR / "shap_feature_selection"
MODELS_DIR = OUT_DIR / "selected_models"
REPORTS_DIR = OUT_DIR / "selected_reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

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


def split_features_and_target(df):
    y = df[TARGET_COLUMN]
    X = df.drop(columns=[col for col in METADATA_COLUMNS if col in df.columns])
    return X, y


def align_features(X_train, X_test, selected_features):
    for col in selected_features:
        if col not in X_train.columns:
            X_train[col] = 0
        if col not in X_test.columns:
            X_test[col] = 0

    return X_train[selected_features], X_test[selected_features]


def build_model():
    return HistGradientBoostingClassifier(
        max_iter=800,
        learning_rate=0.02,
        max_leaf_nodes=31,
        l2_regularization=0.5,
        min_samples_leaf=20,
        random_state=28,
        class_weight="balanced",
    )


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python train_shap_selected_model.py TOP_N")
        return

    top_n = int(sys.argv[1])

    importance_df = pd.read_csv(IMPORTANCE_FILE)
    selected_features = importance_df.head(top_n)["feature"].tolist()

    train_df = pd.read_csv(TRAIN_DATA_FILE)
    test_df = pd.read_csv(TEST_DATA_FILE)

    X_train, y_train = split_features_and_target(train_df)
    X_test, y_test = split_features_and_target(test_df)

    X_train, X_test = align_features(X_train, X_test, selected_features)

    model = build_model()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    class_names = sorted(y_train.unique())

    report = classification_report(
        y_test,
        predictions,
        labels=class_names,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=class_names,
    )

    model_file = MODELS_DIR / f"shap_top_{top_n}_model.pkl"
    report_file = REPORTS_DIR / f"shap_top_{top_n}_report.json"

    with model_file.open("wb") as f:
        pickle.dump(model, f)

    payload = {
        "feature_selection": "global_shap_importance",
        "top_n": top_n,
        "classes": class_names,
        "features": selected_features,
        "num_features": len(selected_features),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix_labels": class_names,
        "confusion_matrix": matrix.tolist(),
    }

    report_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps({
        "top_n": top_n,
        "accuracy": accuracy,
        "model_file": str(model_file),
        "report_file": str(report_file),
    }))


if __name__ == "__main__":
    main()
