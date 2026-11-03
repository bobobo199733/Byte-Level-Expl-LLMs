"""Relate held-out code-origin classifier predictions to sandboxed correctness.

No generated-code execution. Optional model refitting reconstructs per-program
attributions under the ORIGINAL nested task folds, for correctness-stratified
explanation analysis. Task-bootstrap uncertainty is applied separately within
each known-correctness subset. Unknown cases
remain an explicit third group. This is an OOF subgroup analysis of models
trained on the full population, NOT "trained only on correct solutions."
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

CLASSES = ["llama", "mistral", "qwen"]


def estimate(frame: pd.DataFrame, seed=42, draws=1000):
    if frame.empty:
        return {"n": 0}
    point = float(accuracy_score(frame["true_model"], frame["predicted_model"]))
    result = {
        "n": int(len(frame)), "n_tasks": int(frame["task"].nunique()),
        "accuracy": point,
        "macro_f1": float(f1_score(frame["true_model"], frame["predicted_model"],
                                    labels=CLASSES, average="macro", zero_division=0)),
    }
    blocks = [piece for _, piece in frame.groupby("task")]
    if len(blocks) < 2:
        result["accuracy_task_bootstrap_95"] = None
    else:
        rng = np.random.default_rng(seed)
        scores = []
        for _ in range(draws):
            idx = rng.integers(0, len(blocks), len(blocks))
            chosen = pd.concat([blocks[j] for j in idx])
            scores.append(float(accuracy_score(chosen["true_model"], chosen["predicted_model"])))
        result["accuracy_task_bootstrap_95"] = [
            float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))
        ]
    return result



def recompute_local_attributions(joined: pd.DataFrame) -> pd.DataFrame:
    """Recreate local explanations for archived OOF models without test leakage.

    Archived RQ2 exports contain top-10 training-selected features, not the
    complete per-program local SHAP tensor. Refit the original exact nested
    grouped-CV pipeline and assert identical held-out predictions.
    """
    import platform
    import sys
    from pathlib import Path
    if platform.python_version_tuple()[:2] != ("3", "13"):
        raise RuntimeError("CPython 3.13 required for historical opcode audit")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "rq1"))
    from run_nested_cv import DEFAULT_TRAIN, DEFAULT_TEST, RESEARCH_ROOT, load_dataset
    from run_validation import build_validation_features
    from run_source_interventions import fit_heldout_models
    from run_explanations import linear_logit_shap

    df, cols = load_dataset(DEFAULT_TRAIN, DEFAULT_TEST)
    features, _ = build_validation_features(
        df, cols, RESEARCH_ROOT, ("opcode_full",), ngram_buckets=256
    )
    X = features["opcode_full"].to_numpy(dtype=float)
    if len(X) != joined["row_id"].nunique():
        raise ValueError("Attribution dataset does not match correctness rows")
    result = []
    for seed in sorted(joined["seed"].unique()):
        seen = set()
        for fold, tr, te, fitted in fit_heldout_models(
            df, X, seed=int(seed), outer=5, inner=4
        ):
            train_mean = X[tr].mean(axis=0)
            attr, _ = linear_logit_shap(fitted, X[te], train_mean)
            predicted = fitted.predict(X[te])
            historical = joined[joined["seed"].eq(seed)].set_index("row_id")
            for local, index in enumerate(te):
                original_row = historical.loc[int(index)]
                model_prediction = fitted.named_steps["clf"].classes_[int(predicted[local])]
                # Class IDs are 0/1/2, mapped through the canonical ordering.
                predicted_name = ["llama", "mistral", "qwen"][int(model_prediction)]
                if original_row["predicted_model"] != predicted_name:
                    raise AssertionError(
                        f"Refitted OOF decision differs from archived seed={seed} row={index}"
                    )
                true_index = ["llama", "mistral", "qwen"].index(
                    original_row["true_model"]
                )
                vec = np.abs(attr[local, :, true_index])
                mass = float(vec.sum())
                top10 = float(np.sort(vec)[-10:].sum()) if mass else 0.0
                result.append({
                    "seed": int(seed), "fold": fold, "row_id": int(index),
                    "file_name": original_row["file_name"],
                    "task": original_row["task"],
                    "true_model": original_row["true_model"],
                    "correctness_status": original_row["status"],
                    "true_class_abs_logit_shap_sum": mass,
                    "true_class_top10_shap_mass_fraction": (
                        top10 / mass if mass > 0 else None
                    ),
                    "true_class_max_abs_logit_shap": float(vec.max()),
                })
                seen.add(int(index))
        if len(seen) != len(df):
            raise AssertionError(f"Missing held-out attribution rows seed {seed}")
    table = pd.DataFrame(result)
    if table.duplicated(["seed", "row_id"]).any():
        raise AssertionError("Duplicate local SHAP results")
    return table


def analyze(args):
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing overwrite: {args.output_dir}")
    correctness = pd.read_csv(args.correctness)
    predictions = pd.read_csv(args.predictions)
    if len(correctness) != 1316 or correctness["file_name"].duplicated().any():
        raise ValueError("Expected one correctness row per 1316 original retained files")
    if not set(correctness["status"]).issubset({"pass", "fail", "untestable"}):
        raise ValueError("Unexpected correctness status")
    required = {"seed", "row_id", "file_name", "task", "true_model", "predicted_model"}
    if not required.issubset(predictions):
        raise ValueError("Missing OOF prediction columns")
    if predictions.duplicated(["seed", "row_id"]).any():
        raise ValueError("Duplicate program/seed in OOF predictions")
    joined = predictions.merge(
        correctness[["row_id", "file_name", "model", "task", "status"]],
        on=["row_id", "file_name"], how="left", validate="many_to_one",
        suffixes=("", "_correctness"), indicator=True,
    )
    if (joined["_merge"] != "both").any() or (joined["task"] != joined["task_correctness"]).any() or (joined["true_model"] != joined["model"]).any():
        raise ValueError("Correctness/prediction row or model alignment mismatch")
    joined = joined.drop(columns=["_merge", "model", "task_correctness"])
    summary = {
        "correctness_status_counts": correctness["status"].value_counts().to_dict(),
        "classifier_training_population": "all retained programs, as in original RQ2; no correctness-only retraining",
        "by_seed": {},
    }
    for seed, block in joined.groupby("seed"):
        summary["by_seed"][str(seed)] = {
            status: estimate(block[block["status"].eq(status)],
                             seed=int(seed) + 99, draws=args.bootstrap_draws)
            for status in ("pass", "fail", "untestable")
        }
    args.output_dir.mkdir(parents=True)
    joined.to_csv(args.output_dir / "correctness_joined_oof.csv", index=False)
    if getattr(args, "with_attributions", False):
        local = recompute_local_attributions(joined)
        local.to_csv(args.output_dir / "correctness_local_attributions.csv", index=False)
        grouped = local.groupby(["seed", "true_model", "correctness_status"]).agg(
            n=("row_id", "size"),
            n_tasks=("task", "nunique"),
            mean_abs_logit_shap_sum=("true_class_abs_logit_shap_sum", "mean"),
            mean_top10_concentration=("true_class_top10_shap_mass_fraction", "mean"),
            mean_max_abs_contribution=("true_class_max_abs_logit_shap", "mean"),
        ).reset_index()
        grouped.to_csv(args.output_dir / "correctness_attribution_summary.csv", index=False)
        summary["attribution_analysis"] = {
            "n_local_explanations": len(local),
            "n_seed_folds": 15,
            "note": "Models refitted on the original entire-training-task folds; evaluated on held-out programs and stratified by known task-test correctness.",
        }
    if args.equivalence.is_file():
        equiv = pd.read_csv(args.equivalence)
        merged = equiv.merge(
            correctness[["file_name", "status"]].rename(
                columns={"status": "full_correctness_status"}
            ), on="file_name", validate="many_to_one"
        )
        merged.to_csv(args.output_dir / "intervention_correctness_joined.csv", index=False)
        summary["intervention_by_correctness"] = pd.crosstab(
            merged["full_correctness_status"], merged["status"]
        ).to_dict("index")
        summary["intervention_prediction_changes_in_matched_pairs"] = {
            status: {
                "n_pairs": int(len(block)),
                "original_prediction_flip_rate": float(
                    block["original_prediction_flipped"].astype(str).str.lower().eq("true").mean()
                ) if len(block) else None,
            }
            for status, block in merged.loc[
                merged["status"].eq("matched_on_observed_inputs")
            ].groupby("full_correctness_status")
        }
    summary["limitations"] = [
        "Correctness means passing the available task tests, not proven universal correctness.",
        "Grouped confidence intervals resample tasks, not independent programs.",
        "The three OOF seeds reuse the same tasks; seed metrics are not independent.",
        "Correctness groups may have different task composition and may be very small.",
        "Subgroup OOF evaluation does not substitute for retraining solely on correct programs.",
        "SHAP magnitude by correctness is observational; it does not validate the LLM's causal explanation.",
        "No causal inference between model origin and correctness is justified.",
    ]
    (args.output_dir / "correctness_analysis.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--correctness", type=Path, required=True)
    p.add_argument("--predictions", type=Path,
                   default=Path(__file__).resolve().parents[1] / "experiments/rq2_opcode_full_001/oof_predictions.csv")
    p.add_argument("--equivalence", type=Path,
                   default=Path(__file__).resolve().parents[1] / "experiments/rq2_equivalence_final_001/equivalence_results.csv")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--bootstrap-draws", type=int, default=1000)
    p.add_argument("--with-attributions", action="store_true",
                   help="Refit original 15 OOF classifiers to recover local attributions")
    a = p.parse_args()
    if a.bootstrap_draws < 100:
        p.error("--bootstrap-draws must be at least 100")
    analyze(a)


if __name__ == "__main__":
    main()
