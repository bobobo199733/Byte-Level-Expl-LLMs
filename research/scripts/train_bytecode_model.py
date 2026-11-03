from pathlib import Path
import pickle
import json

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_DATA_FILE = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_DATA_FILE = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

MODEL_FILE = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

TARGET_COLUMN = "model"

# Choose one:
MODEL_TYPE = "xgboost"
# MODEL_TYPE = "random_forest"
# MODEL_TYPE = "hist_gradient_boosting"

METADATA_COLUMNS = [
    "file",
    "file_name",
    "path",
    "task",
    "task_id",
    "prompt",
    "prompt_id",
    "run",
    "run_id",
    "model",
]


def split_features_and_target(df: pd.DataFrame):
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    y = df[TARGET_COLUMN]

    columns_to_drop = [
        col for col in METADATA_COLUMNS
        if col in df.columns
    ]

    X = df.drop(columns=columns_to_drop)

    return X, y


def align_train_test_features(X_train: pd.DataFrame, X_test: pd.DataFrame):
    X_train, X_test = X_train.align(
        X_test,
        join="outer",
        axis=1,
        fill_value=0,
    )

    columns = sorted(X_train.columns)

    return X_train[columns], X_test[columns]


def build_model(model_type: str):
    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            max_features="sqrt",
            random_state=13,
            class_weight="balanced",
            n_jobs=-1,
        )

    if model_type == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(
            max_iter=1000,
            learning_rate=0.05,
            max_leaf_nodes=31,
            l2_regularization=0.1,
            min_samples_leaf=20,
            max_depth=4,
            random_state=42,
            class_weight="balanced",
        )

    if model_type == "xgboost":
        return XGBClassifier(
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

    raise ValueError(f"Unsupported MODEL_TYPE: {model_type}")


def main():
    train_df = pd.read_csv(TRAIN_DATA_FILE)
    test_df = pd.read_csv(TEST_DATA_FILE)

    X_train, y_train = split_features_and_target(train_df)
    X_test, y_test = split_features_and_target(test_df)

    X_train, X_test = align_train_test_features(X_train, X_test)

    model = build_model(MODEL_TYPE)

    label_encoder = None

    if MODEL_TYPE == "xgboost":
        label_encoder = LabelEncoder()
        y_train_fit = label_encoder.fit_transform(y_train)
        y_test_eval = label_encoder.transform(y_test)
        class_names = list(label_encoder.classes_)
    else:
        y_train_fit = y_train
        y_test_eval = y_test
        class_names = sorted(y_train.unique())

    model.fit(X_train, y_train_fit)

    predictions = model.predict(X_test)

    if label_encoder is not None:
        predictions = label_encoder.inverse_transform(predictions)
        y_test_for_report = y_test
    else:
        y_test_for_report = y_test_eval

    accuracy = accuracy_score(y_test_for_report, predictions)
    report = classification_report(
        y_test_for_report,
        predictions,
        labels=class_names,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(
        y_test_for_report,
        predictions,
        labels=class_names,
    )

    with MODEL_FILE.open("wb") as f:
        pickle.dump(
            {
                "model": model,
                "label_encoder": label_encoder,
                "model_type": MODEL_TYPE,
            },
            f,
        )

    payload = {
        "target": TARGET_COLUMN,
        "model_type": MODEL_TYPE,
        "classes": class_names,
        "features": list(X_train.columns),
        "num_features": X_train.shape[1],
        "train_file": str(TRAIN_DATA_FILE),
        "test_file": str(TEST_DATA_FILE),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix_labels": class_names,
        "confusion_matrix": matrix.tolist(),
    }

    REPORT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 60)
    print("BYTECODE LLM CLASSIFIER TRAINING COMPLETE")
    print("=" * 60)
    print(f"Model type:    {MODEL_TYPE}")
    print(f"Train file:    {TRAIN_DATA_FILE}")
    print(f"Test file:     {TEST_DATA_FILE}")
    print(f"Train samples: {len(X_train)}")
    print(f"Test samples:  {len(X_test)}")
    print(f"Features:      {X_train.shape[1]}")
    print(f"Classes:       {class_names}")
    print(f"Accuracy:      {accuracy:.4f}")
    print(f"Saved model:   {MODEL_FILE}")
    print(f"Saved report:  {REPORT_FILE}")


if __name__ == "__main__":
    main()
