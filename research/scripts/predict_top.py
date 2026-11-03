from pathlib import Path
import sys
import json
import pickle

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from bytecode_utils import preprocess_single_file


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"

PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"

GLOBAL_IMPORTANCE_FILE = (
    BASE_DIR
    / "shap_feature_selection"
    / "global_shap_importance.csv"
)

OUT_DIR = BASE_DIR / "shap_bytecode" / "partial_paths"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EFFECTS_CSV = OUT_DIR / "partial_effects.csv"
PLOT_FILE = OUT_DIR / "partial_ternary_path.svg"

CLASS_NAMES = ["llama", "mistral", "qwen"]

PLOT_MODE = "global_top_n"
# Options:
# "local_top_n"
# "global_top_n"

TOP_N = 16


# ============================================================
# HELPERS
# ============================================================

def infer_task_from_filename(py_file: Path) -> str:
    return py_file.stem.split("_")[0]


def load_target_function(py_file: Path) -> str:
    task = infer_task_from_filename(py_file)
    meta_file = PROMPTS_DIR / task / "meta.json"

    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    return meta["function_name"]


def load_model_bundle():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)

    return (
        loaded["model"],
        loaded.get("label_encoder"),
        loaded.get("model_type"),
    )


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def align_features_to_model(X, trained_features):
    for col in trained_features:
        if col not in X.columns:
            X[col] = 0

    extra = [c for c in X.columns if c not in trained_features]

    if extra:
        X = X.drop(columns=extra)

    return X[trained_features]


def preprocess_generated_file(py_file, feature_columns):
    target_function = load_target_function(py_file)

    return preprocess_single_file(
        py_file=py_file,
        feature_columns=feature_columns,
        target_function=target_function,
    )


def get_class_shap_values(shap_values, class_index):
    if isinstance(shap_values, list):
        return shap_values[class_index]

    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_index]

    raise ValueError("Unexpected SHAP format")


def softmax(x):
    x = np.array(x, dtype=float)
    x = x - np.max(x)

    exp = np.exp(x)
    return exp / exp.sum()


def ternary_to_xy(probs):
    llama, mistral, qwen = probs

    x = mistral + 0.5 * qwen
    y = (np.sqrt(3) / 2) * qwen

    return x, y


# ============================================================
# BUILD EFFECTS DATAFRAME
# ============================================================

def build_effects_dataframe(
    X,
    shap_values,
    class_names,
    feature_names,
):
    rows = []

    for j, feature_name in enumerate(feature_names):

        if not feature_name.startswith("byte_"):
            continue

        effect_vec = np.array([
            get_class_shap_values(shap_values, class_idx)[0, j]
            for class_idx in range(len(class_names))
        ])

        magnitude = np.linalg.norm(effect_vec)

        row = {
            "feature": feature_name,
            "feature_value": X.iloc[0][feature_name],
            "magnitude": magnitude,
            "byte_index": int(feature_name.replace("byte_", "")),
        }

        for class_idx, cls in enumerate(class_names):
            row[f"shap_{cls}"] = effect_vec[class_idx]

        rows.append(row)

    df = pd.DataFrame(rows)

    return df


# ============================================================
# FEATURE SELECTION
# ============================================================

def select_features(effects_df):

    if PLOT_MODE == "local_top_n":
        selected = (
            effects_df
            .sort_values("magnitude", ascending=False)
            .head(TOP_N)
        )

    elif PLOT_MODE == "global_top_n":

        importance_df = pd.read_csv(GLOBAL_IMPORTANCE_FILE)

        selected_features = (
            importance_df
            .head(TOP_N)["feature"]
            .tolist()
        )

        selected = effects_df[
            effects_df["feature"].isin(selected_features)
        ]

    else:
        raise ValueError(f"Unknown PLOT_MODE: {PLOT_MODE}")

    return (
        selected
        .sort_values("byte_index", ascending=True)
        .reset_index(drop=True)
    )


# ============================================================
# TRIANGLE
# ============================================================

def draw_triangle(ax):

    h = np.sqrt(3) / 2

    corners = {
        "llama": (0, 0),
        "mistral": (1, 0),
        "qwen": (0.5, h),
    }

    colors = {
        "llama": "red",
        "mistral": "green",
        "qwen": "blue",
    }

    ax.plot(
        [0, 1, 0.5, 0],
        [0, 0, h, 0],
        color="black",
        linewidth=2,
    )

    for cls, (x, y) in corners.items():
        ax.scatter([x], [y], s=180, color=colors[cls])

        ax.text(
            x,
            y + 0.04,
            cls,
            fontsize=15,
            ha="center",
            color=colors[cls],
            fontweight="bold",
        )

    ax.set_aspect("equal")
    ax.axis("off")


# ============================================================
# PLOT
# ============================================================

def get_arrow_direction(xy_from, xy_to, class_names):
    """
    Determine which triangle corner the arrow is geometrically
    moving toward, by projecting the displacement vector onto
    the direction from the current point to each corner.
    """
    corner_positions = {
        "llama":   np.array([0.0, 0.0]),
        "mistral": np.array([1.0, 0.0]),
        "qwen":    np.array([0.5, np.sqrt(3) / 2]),
    }

    move = np.array(xy_to) - np.array(xy_from)

    projections = {
        cls: np.dot(corner - np.array(xy_from), move)
        for cls, corner in corner_positions.items()
        if cls in class_names
    }

    return max(projections, key=projections.get)


def plot_partial_path(
    selected_df,
    class_names,
    output_file,
):

    raw = np.zeros(len(class_names))

    points = [softmax(raw)]

    for _, row in selected_df.iterrows():

        effect = np.array([
            row[f"shap_{cls}"]
            for cls in class_names
        ])

        raw += effect

        points.append(softmax(raw))

    points = np.array(points)

    xy_points = np.array([
        ternary_to_xy(p)
        for p in points
    ])

    deltas = xy_points[1:] - xy_points[:-1]

    distances = np.linalg.norm(deltas, axis=1)

    max_dist = distances.max()

    fig, ax = plt.subplots(figsize=(16, 14))

    draw_triangle(ax)

    colors = {
        "llama": "red",
        "mistral": "green",
        "qwen": "blue",
    }

    for i, (_, row) in enumerate(selected_df.iterrows()):

        x1, y1 = xy_points[i]
        x2, y2 = xy_points[i + 1]

        # Color by the corner the arrow is geometrically moving toward,
        # not by argmax of raw SHAP values (which can mislead when a large
        # negative value on one class drives movement toward another).
        direction = get_arrow_direction((x1, y1), (x2, y2), class_names)

        norm = distances[i] / max_dist

        linewidth = max(0.4, norm * 3)
        arrow_size = max(2, norm * 14)

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=linewidth,
                color=colors[direction],
                mutation_scale=arrow_size,
                alpha=0.9,
            ),
        )

        if norm > 0.3:

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            ax.text(
                mid_x,
                mid_y,
                str(int(row["byte_index"])),
                fontsize=11,
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.15",
                    fc="white",
                    ec="none",
                    alpha=0.8,
                ),
            )

    start_x, start_y = xy_points[0]
    end_x, end_y = xy_points[-1]

    ax.scatter(
        [start_x],
        [start_y],
        marker="x",
        s=150,
        color="black",
        zorder=6,
    )

    ax.scatter(
        [end_x],
        [end_y],
        marker="*",
        s=250,
        color="black",
        zorder=7,
    )

    endpoint = points[-1]

    endpoint_class = class_names[np.argmax(endpoint)]

    ax.set_title(
        f"Partial SHAP attribution path ({PLOT_MODE}, top={TOP_N})\n"
        f"partial endpoint={endpoint_class}",
        fontsize=18,
        pad=20,
    )

    plt.savefig(output_file, bbox_inches="tight")
    plt.close()

    return endpoint


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python partial_shap_paths.py path/to/script.py")
        return

    py_file = Path(sys.argv[1]).resolve()

    report = load_report()

    trained_features = report["features"]

    class_names = report["classes"]

    model, label_encoder, model_type = load_model_bundle()

    X = preprocess_generated_file(
        py_file,
        trained_features,
    )

    X = align_features_to_model(
        X,
        trained_features,
    )

    probs = model.predict_proba(X)[0]

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X)

    effects_df = build_effects_dataframe(
        X,
        shap_values,
        class_names,
        list(X.columns),
    )

    effects_df.to_csv(EFFECTS_CSV, index=False)

    selected_df = select_features(effects_df)

    endpoint = plot_partial_path(
        selected_df,
        class_names,
        PLOT_FILE,
    )

    print("=" * 60)
    print("PARTIAL SHAP PATH COMPLETE")
    print("=" * 60)

    print(f"File: {py_file.name}")

    print("\nFull model prediction:")
    for cls, prob in zip(class_names, probs):
        print(f"{cls}: {prob:.4f}")

    print("\nPartial endpoint:")
    for cls, prob in zip(class_names, endpoint):
        print(f"{cls}: {prob:.4f}")

    print(f"\nSaved effects CSV: {EFFECTS_CSV}")
    print(f"Saved plot:        {PLOT_FILE}")


if __name__ == "__main__":
    main()
