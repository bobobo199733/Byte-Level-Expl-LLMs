from pathlib import Path
import pickle
import json
import sys

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_DATA_FILE = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_DATA_FILE = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

MODEL_FILE = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

TARGET_COLUMN = "model"

METADATA_COLUMNS = [
    "file",
    "filename",
    "path",
    "task",
    "task_id",
    "prompt",
    "prompt_id",
    "run",
    "run_id",
    "model",
]


def split_features_and_target(df):
    y = df[TARGET_COLUMN]

    X = df.drop(
        columns=[col for col in METADATA_COLUMNS if col in df.columns]
    )

    return X, y


def align_train_test_features(X_train, X_test):
    X_train, X_test = X_train.align(
        X_test,
        join="outer",
        axis=1,
        fill_value=0,
    )

    columns = sorted(X_train.columns)

    return X_train[columns], X_test[columns]


def main():
    forest_seed = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    no_save = "--no-save" in sys.argv

    train_df = pd.read_csv(TRAIN_DATA_FILE)
    test_df = pd.read_csv(TEST_DATA_FILE)

    X_train, y_train = split_features_and_target(train_df)
    X_test, y_test = split_features_and_target(test_df)

    X_train, X_test = align_train_test_features(X_train, X_test)

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=forest_seed,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)
    matrix = confusion_matrix(y_test, predictions, labels=model.classes_)

    payload = {
        "target": TARGET_COLUMN,
        "model_type": "RandomForestClassifier",
        "forest_seed": forest_seed,
        "train_file": str(TRAIN_DATA_FILE),
        "test_file": str(TEST_DATA_FILE),
        "classes": list(model.classes_),
        "features": list(X_train.columns),
        "num_features": X_train.shape[1],
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix_labels": list(model.classes_),
        "confusion_matrix": matrix.tolist(),
    }

    if not no_save:
        with MODEL_FILE.open("wb") as f:
            pickle.dump(model, f)

        REPORT_FILE.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

    print(json.dumps({
        "forest_seed": forest_seed,
        "accuracy": accuracy,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "num_features": X_train.shape[1],
    }))


if __name__ == "__main__":
    main()
