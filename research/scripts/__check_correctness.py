from pathlib import Path
import sys
import json
import pickle

import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from bytecode_utils import preprocess_single_file


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "bytecode_llm_classifier.pkl"
REPORT_FILE = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"

OUT_DIR = BASE_DIR / "shap_bytecode" / "local_predictions"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CUMULATIVE_COVERAGE = 0.95


def infer_task_from_filename(py_file: Path) -> str:
    return py_file.stem.split("_")[0]


def load_target_function(py_file: Path) -> str:
    task = infer_task_from_filename(py_file)
    meta_file = PROMPTS_DIR / task / "meta.json"

    if not meta_file.exists():
        raise FileNotFoundError(f"Missing meta.json for task {task}: {meta_file}")

    meta = json.loads(meta_file.read_text(encoding="utf-8"))

    if "function_name" not in meta:
        raise ValueError(f"Missing function_name in {meta_file}")

    return meta["function_name"]


def load_model_bundle():
    with MODEL_FILE.open("rb") as f:
        loaded = pickle.load(f)

    if isinstance(loaded, dict) and "model" in loaded:
        return (
            loaded["model"],
            loaded.get("label_encoder"),
            loaded.get("model_type", type(loaded["model"]).__name__),
        )

    return loaded, None, type(loaded).__name__


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def preprocess_generated_file(py_file: Path, feature_columns: list[str]) -> pd.DataFrame:
    target_function = load_target_function(py_file)

    return preprocess_single_file(
        py_file=py_file,
        feature_columns=feature_columns,
        target_function=target_function,
    )


def align_features_to_model(X: pd.DataFrame, trained_features: list[str]) -> pd.DataFrame:
    for col in trained_features:
        if col not in X.columns:
            X[col] = 0

    extra_cols = [col for col in X.columns if col not in trained_features]
    if extra_cols:
        X = X.drop(columns=extra_cols)

    return X[trained_features]


def ternary_to_xy(probs):
    llama, mistral, qwen = probs
    x = mistral + 0.5 * qwen
    y = (np.sqrt(3) / 2) * qwen
    return x, y


def project_to_simplex(v):
    v = np.array(v, dtype=float)

    if np.all(v >= 0) and np.isclose(v.sum(), 1):
        return v

    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)

    rho = np.nonzero(u * np.arange(1, n + 1) > (cssv - 1))[0][-1]
    theta = (cssv[rho] - 1) / (rho + 1)

    return np.maximum(v - theta, 0)


def normalize_path_for_visualization(points, scale=0.42):
    points = np.array(points, dtype=float)

    center = np.array([1 / 3, 1 / 3, 1 / 3])
    centered = points - center

    max_distance = max(np.linalg.norm(p) for p in centered)

    if max_distance == 0:
        return points

    normalized = centered / max_distance
    normalized *= scale

    visual_points = center + normalized

    return np.array([project_to_simplex(p) for p in visual_points])


def draw_triangle(ax, class_names):
    height = np.sqrt(3) / 2

    corners = {
        class_names[0]: {"xy": (0, 0), "color": "red"},
        class_names[1]: {"xy": (1, 0), "color": "green"},
        class_names[2]: {"xy": (0.5, height), "color": "blue"},
    }

    ax.plot([0, 1, 0.5, 0], [0, 0, height, 0], linewidth=2.2, color="black")

    for name, info in corners.items():
        x, y = info["xy"]
        color = info["color"]

        ax.scatter([x], [y], s=180, color=color, zorder=5)
        ax.text(
            x,
            y + 0.045,
            name,
            ha="center",
            va="center",
            fontsize=16,
            fontweight="bold",
            color=color,
        )

    ax.set_aspect("equal")
    ax.axis("off")


def get_class_shap_values(shap_values, class_index):
    if isinstance(shap_values, list):
        return shap_values[class_index]

    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_index]

    raise ValueError(
        f"Unexpected SHAP format: {type(shap_values)}, "
        f"shape={getattr(shap_values, 'shape', None)}"
    )


def get_expected_values(explainer):
    expected = explainer.expected_value

    if isinstance(expected, list):
        expected = np.array(expected)

    expected = np.array(expected, dtype=float)

    if expected.ndim > 1:
        expected = expected.flatten()

    total = expected.sum()
    if total != 0:
        expected = expected / total

    return expected


def select_effects_by_coverage(effects, coverage: float):
    total_magnitude = sum(e["magnitude"] for e in effects)

    if total_magnitude == 0:
        return effects, 1.0

    selected = []
    running = 0.0

    for effect in effects:
        selected.append(effect)
        running += effect["magnitude"]

        if running / total_magnitude >= coverage:
            break

    return selected, running / total_magnitude


def plot_local_shap_path(
    X,
    probs,
    shap_values,
    explainer,
    class_names,
    feature_names,
    py_file,
):
    sample_index = 0

    base_probs = get_expected_values(explainer)
    final_probs = probs[sample_index]

    class_colors = {
        class_names[0]: "red",
        class_names[1]: "green",
        class_names[2]: "blue",
    }

    def effect_color(effect_vec):
        strongest_idx = int(np.argmax(effect_vec))
        return class_colors[class_names[strongest_idx]]

    effects = []

    for j, feature_name in enumerate(feature_names):
        effect_vec = np.array([
            get_class_shap_values(shap_values, class_idx)[sample_index, j]
            for class_idx in range(len(class_names))
        ])

        effects.append({
            "feature": feature_name,
            "effect_vec": effect_vec,
            "magnitude": np.linalg.norm(effect_vec),
        })

    effects = sorted(effects, key=lambda x: x["magnitude"], reverse=True)

    selected_effects, actual_coverage = select_effects_by_coverage(
        effects,
        CUMULATIVE_COVERAGE,
    )

    effects_df = pd.DataFrame([
        {
            "rank": rank + 1,
            "feature": effect["feature"],
            "feature_value": X.iloc[sample_index][effect["feature"]],
            "magnitude": effect["magnitude"],
            **{
                f"shap_{class_names[class_idx]}": effect["effect_vec"][class_idx]
                for class_idx in range(len(class_names))
            },
            "strongest_direction": class_names[int(np.argmax(effect["effect_vec"]))],
            "shown_in_plot": effect in selected_effects,
        }
        for rank, effect in enumerate(effects)
    ])

    effects_output_path = OUT_DIR / "current_shap_effects.csv"
    effects_df.to_csv(effects_output_path, index=False)

    raw_path_points = [base_probs.copy()]
    current = base_probs.copy()

    for effect in selected_effects:
        current = current + effect["effect_vec"]
        raw_path_points.append(current.copy())

    selected_sum = np.sum([e["effect_vec"] for e in selected_effects], axis=0)
    all_sum = np.sum([e["effect_vec"] for e in effects], axis=0)
    residual_effect = all_sum - selected_sum
    residual_magnitude = np.linalg.norm(residual_effect)

    if residual_magnitude > 1e-8:
        current = current + residual_effect
        raw_path_points.append(current.copy())

    raw_path_points.append(final_probs.copy())

    visual_points = normalize_path_for_visualization(raw_path_points)

    fig, ax = plt.subplots(figsize=(20, 18))
    draw_triangle(ax, class_names)

    base_x, base_y = ternary_to_xy(visual_points[0])
    final_x, final_y = ternary_to_xy(visual_points[-1])

    ax.scatter([base_x], [base_y], s=140, marker="x", color="black", label="baseline", zorder=6)
    ax.scatter([final_x], [final_y], s=240, marker="*", color="black", label="final prediction", zorder=7)

    ax.annotate(
        "",
        xy=(final_x, final_y),
        xytext=(base_x, base_y),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=2,
            alpha=0.25,
            color="black",
            shrinkA=0,
            shrinkB=0,
        ),
    )

    for i, effect in enumerate(selected_effects):
        x1, y1 = ternary_to_xy(visual_points[i])
        x2, y2 = ternary_to_xy(visual_points[i + 1])

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                mutation_scale=8,
                linewidth=2,
                alpha=1.0,
                color=effect_color(effect["effect_vec"]),
                shrinkA=0,
                shrinkB=0,
            ),
        )

    if residual_magnitude > 1e-8:
        residual_start_idx = len(selected_effects)
        residual_end_idx = len(selected_effects) + 1

        x1, y1 = ternary_to_xy(visual_points[residual_start_idx])
        x2, y2 = ternary_to_xy(visual_points[residual_end_idx])

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=3,
                alpha=0.75,
                color="gray",
                linestyle="dashed",
                shrinkA=0,
                shrinkB=0,
            ),
        )

    predicted = class_names[np.argmax(final_probs)]

    ax.set_title(
        f"Local SHAP ternary path\n"
        f"{py_file.name}\n"
        f"predicted={predicted}",
        fontsize=18,
        pad=20,
    )

    ax.text(
        0.5,
        -0.08,
        (
            f"Showing {len(selected_effects)}/{len(effects)} features "
            f"covering {actual_coverage:.1%} of total SHAP magnitude. "
            "Dashed arrow represents remaining attribution. "
            "Path is scaled for readability."
        ),
        ha="center",
        va="center",
        fontsize=11,
        alpha=0.75,
        transform=ax.transAxes,
    )

    ax.legend(loc="upper right", fontsize=12)

    output_path = OUT_DIR / "current_ternary_shap.svg"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"\nSaved SHAP effects table to:\n{effects_output_path}")
    print(f"Saved ternary SHAP plot to:\n{output_path}")
    print(f"Selected features: {len(selected_effects)} / {len(effects)}")
    print(f"Coverage: {actual_coverage:.4f}")
    print(f"Residual magnitude: {residual_magnitude:.6f}")


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python predict_and_explain.py path/to/generated_script.py")
        return

    py_file = Path(sys.argv[1]).resolve()

    if not py_file.exists():
        raise FileNotFoundError(py_file)

    report = load_report()
    trained_features = report["features"]
    class_names = report["classes"]

    model, label_encoder, model_type = load_model_bundle()

    X = preprocess_generated_file(py_file, trained_features)
    X = align_features_to_model(X, trained_features)

    feature_names = list(X.columns)

    probs = model.predict_proba(X)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    plot_local_shap_path(
        X=X,
        probs=probs,
        shap_values=shap_values,
        explainer=explainer,
        class_names=class_names,
        feature_names=feature_names,
        py_file=py_file,
    )

    predicted = class_names[np.argmax(probs[0])]

    print("\nPrediction:")
    print(predicted)

    print("\nProbabilities:")
    for cls, prob in zip(class_names, probs[0]):
        print(f"{cls}: {prob:.4f}")

    print(f"\nModel type: {model_type}")
    print("Done.")


if __name__ == "__main__":
    main()
