from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FEATURES = BASE_DIR / "features" / "raw_features.csv"
PROCESSED_FEATURES = BASE_DIR / "features" / "processed_features.csv"


def main():
    df = pd.read_csv(RAW_FEATURES)
    df = df.copy()

    # Convert score
    df["score"] = df["score"].astype(float)

    # Drop columns that should not be model features
    drop_cols = [
        "file",
        # "status",
        "passed",
        "total"
    ]

    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # One-hot encode categorical columns
    categorical_cols = [
        "task",
        "prompt",
        "run",
        "model",
        "status"
    ]

    df = pd.get_dummies(
        df,
        columns=[c for c in categorical_cols if c in df.columns],
        drop_first=False
    )

    # Ensure all booleans become 0/1
    for col in df.columns:
        if df[col].dtype == "bool":
            df[col] = df[col].astype(int)

    df.to_csv(PROCESSED_FEATURES, index=False)

    print(f"Saved processed features to: {PROCESSED_FEATURES}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()
