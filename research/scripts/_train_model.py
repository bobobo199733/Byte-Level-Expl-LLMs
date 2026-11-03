from pathlib import Path
import json
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_FEATURES = BASE_DIR / "features" / "processed_features.csv"
MODELS_DIR = BASE_DIR / "models"

MODEL_FILE = MODELS_DIR / "score_model.pkl"
CONFIG_FILE = MODELS_DIR / "model_config.json"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(PROCESSED_FEATURES)

    y = df["score"]
    X = df.drop(columns=["score"])

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )

    model.fit(X, y)

    with MODEL_FILE.open("wb") as f:
        pickle.dump(model, f)

    config = {
        "target": "score",
        "model_type": "RandomForestRegressor",
        "n_estimators": 300,
        "random_state": 42,
        "features": list(X.columns),
        "num_rows": len(df)
    }

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")

    print(f"Saved model to: {MODEL_FILE}")
    print(f"Saved config to: {CONFIG_FILE}")
    print(f"Training rows: {len(df)}")
    print(f"Feature count: {X.shape[1]}")


if __name__ == "__main__":
    main()
