from pathlib import Path
import json
import sys
import re
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


TARGET_COLUMN = "model"

DROP_COLUMNS = [
    "file",
    # "file_name",
    "function_name",
    "python_version",
    "representation_kind",
    "task",
    "prompt",
    "run",
    "score",
    "passed",
    "total",
    "status",
    "num_failures",
    "bytecode_extract_status",
    "bytecode_extract_error",
    "original_byte_length",
    "was_truncated",
]


def main():
    global USE_TEST_DATA
    USE_TEST_DATA = False
    if len(sys.argv) >= 2:
        USE_TEST_DATA = sys.argv[1] == "1"


    if USE_TEST_DATA:
        INPUT_CSV = BASE_DIR / "test_data" / "features" / "function_bytecode_features.csv"
        OUTPUT_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
        CONFIG_FILE = BASE_DIR / "test_data" / "features" / "processed_bytecode_config.json"

    else:
        INPUT_CSV = BASE_DIR / "features" / "function_bytecode_features.csv"
        OUTPUT_CSV = BASE_DIR / "features" / "processed_bytecode_features.csv"
        CONFIG_FILE = BASE_DIR / "features" / "processed_bytecode_config.json"

    df = pd.read_csv(INPUT_CSV, low_memory=False)

    if "bytecode_extract_status" in df.columns:
        df = df[df["bytecode_extract_status"] == "ok"].copy()

    df = df[df[TARGET_COLUMN].notna()].copy()

    y = df[TARGET_COLUMN]

    X = df.drop(
        columns=[
            c for c in DROP_COLUMNS + [TARGET_COLUMN]
            if c in df.columns
        ]
    )

    # Retain filename as metadata for downstream auditing, never as a predictor.
    metadata = X[["file_name"]].copy() if "file_name" in X else pd.DataFrame(index=X.index)
    features = X.drop(columns=["file_name"], errors="ignore")
    byte_cols = [c for c in features if re.fullmatch(r"byte_\d+", c)]
    unexpected = sorted(set(features.columns) - set(byte_cols))
    if unexpected:
        raise ValueError(f"Unexpected classifier input columns: {unexpected}")
    if not byte_cols:
        raise ValueError("No byte features in extracted dataset")
    indexes = sorted(int(c[5:]) for c in byte_cols)
    if indexes != list(range(len(indexes))):
        raise ValueError("Byte features must be a contiguous 0..N-1 sequence")
    features = features[[f"byte_{i}" for i in indexes]]
    if features.isna().any().any():
        raise ValueError("Missing byte-feature values; refusing to impute")
    features = features.apply(pd.to_numeric, errors="raise")
    X = pd.concat([metadata, features], axis=1)

    processed = pd.concat([
        y.rename(TARGET_COLUMN),
        X,
    ], axis=1)

    processed.to_csv(OUTPUT_CSV, index=False)

    config = {
        "input_csv": str(INPUT_CSV.relative_to(BASE_DIR)),
        "output_csv": str(OUTPUT_CSV.relative_to(BASE_DIR)),
        "target_column": TARGET_COLUMN,
        "rows": len(processed),
        "num_features": X.shape[1],
        "classes": sorted(y.unique().tolist()),
        "feature_columns": features.columns.tolist(),
        "metadata_columns": metadata.columns.tolist(),
        "representation_kind": "opcode_argument_pairs_v1",
        "representation_length": len(byte_cols),
    }

    CONFIG_FILE.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8",
    )

    print(f"Saved processed features to: {OUTPUT_CSV}")
    print(f"Rows: {len(processed)}")
    print(f"Features: {X.shape[1]}")
    print(f"Classes: {sorted(y.unique().tolist())}")


if __name__ == "__main__":
    main()
