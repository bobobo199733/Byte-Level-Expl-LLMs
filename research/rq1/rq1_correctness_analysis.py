"""RQ1 correctness-stratified audit of existing task-held-out predictions.

Never re-trains a model, executes generated code, or modifies old results.
Uses the RQ2 1316-program correctness inventory, RQ1 7 validation
representation OOF files, and RQ1 nested selected-pipeline OOF predictions.

Accuracy contrasts use IDENTICAL cases for both methods; bootstrap resamples
whole tasks, never individual programs. These are subgroup evaluations of
models trained on ALL archived programs; they do not show the performance
of a classifier trained on correct-only solutions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

CLASSES = ("llama", "mistral", "qwen")
COMPARE = (
    ("opcode_full", "length_only"),
    ("opcode_full", "ast_original"),
    ("opcode_full", "ast_no_length"),
    ("opcode_ngram", "opcode_full"),
    ("ast_original", "length_only"),
    ("ast_no_length", "length_only"),
    ("ast_core_prop", "length_only"),
)


def validate_inventory(df):
    needed = {"row_id", "task", "model", "file_name", "status"}
    if not needed.issubset(df):
        raise ValueError(f"Correctness inventory missing columns {needed-set(df.columns)}")
    if len(df) != 1316 or df["row_id"].duplicated().any() or df["file_name"].duplicated().any():
        raise ValueError("Expected 1316 unique retained programs")
    if set(df.status) - {"pass", "fail", "untestable"}:
        raise ValueError("Unknown correctness status")
    if set(df.model) - set(CLASSES):
        raise ValueError("Unknown source-generation model")
    return df[list(needed)].copy()


def merge_oof(predictions, inventory, *, source, truth, predicted, variant=None, seed=None):
    required = {"row_id", "task", "file_name", truth, predicted}
    if variant is not None:
        required.add(variant)
    if seed is not None:
        required.add(seed)
    if not required.issubset(predictions):
        raise ValueError(f"{source} lacks {required-set(predictions.columns)}")
    p = predictions.copy()
    if seed is None:
        p["seed"] = 42  # historical selected RQ1 pipeline runs a single seed
        seed = "seed"
    if variant is None:
        p["variant"] = "nested_selected"
        variant = "variant"
    p = p.rename(columns={truth: "truth", predicted: "prediction", variant: "variant", seed: "seed"})
    if p.duplicated(["seed", "variant", "row_id"]).any():
        raise ValueError(f"Duplicate OOF program/seed/variant: {source}")
    joined = p.merge(
        inventory.rename(columns={"task": "correctness_task", "file_name": "correctness_file_name"}),
        on="row_id", how="left", validate="many_to_one", indicator=True,
    )
    if (joined["_merge"] != "both").any():
        raise ValueError(f"Unmatched correctness inventory rows for {source}")
    if ((joined["task"] != joined["correctness_task"]) |
        (joined["file_name"] != joined["correctness_file_name"]) |
        (joined["truth"] != joined["model"])).any():
        raise ValueError(f"Task, filename or generating-model mismatch in {source}")
    if not joined["prediction"].isin(CLASSES).all():
        raise ValueError(f"Unknown predicted origin in {source}")
    if not joined["truth"].isin(CLASSES).all():
        raise ValueError(f"Unknown actual origin in {source}")
    return joined.drop(columns=["_merge", "correctness_task", "correctness_file_name", "model"])


def complete_oof(merged, n=1316):
    for (seed, variant), subset in merged.groupby(["seed", "variant"]):
        if len(subset) != n or subset.row_id.nunique() != n:
            raise ValueError(f"Incomplete OOF coverage seed={seed}, variant={variant}")


def metrics(part):
    if part.empty:
        return {"n": 0, "n_tasks": 0}
    return {
        "n": int(len(part)), "n_tasks": int(part.task.nunique()),
        "by_true_model": {str(k): int(v) for k, v in part.truth.value_counts().items()},
        "accuracy": float(accuracy_score(part.truth, part.prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(part.truth, part.prediction)),
        "macro_f1": float(f1_score(part.truth, part.prediction, labels=CLASSES,
                                   average="macro", zero_division=0)),
    }


def paired_bootstrap(frame, first, second, draws, seed):
    """Correctly paired within each task, with task (not program) resampling."""
    left = frame.loc[frame.variant.eq(first), ["row_id", "task", "status", "truth", "prediction"]]
    right = frame.loc[frame.variant.eq(second), ["row_id", "prediction"]]
    data = left.merge(right, on="row_id", suffixes=("_a", "_b"), validate="one_to_one")
    if len(left) != len(right) or len(data) != len(left):
        raise ValueError("Paired variants did not use identical retained examples")
    if data.task.nunique() < 2:
        return None
    blocks = [part for _, part in data.groupby("task")]
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(draws):
        sample = pd.concat([blocks[k] for k in rng.integers(0, len(blocks), len(blocks))])
        acc_a = (sample.truth == sample.prediction_a).mean()
        acc_b = (sample.truth == sample.prediction_b).mean()
        diffs.append(float(acc_a - acc_b))
    point = float((data.truth == data.prediction_a).mean() -
                  (data.truth == data.prediction_b).mean())
    return {
        "method_a": first, "method_b": second,
        "n": len(data), "n_tasks": data.task.nunique(),
        "accuracy_difference_a_minus_b": point,
        "task_bootstrap_95_ci": [float(np.percentile(diffs, 2.5)),
                                 float(np.percentile(diffs, 97.5))],
        "n_bootstrap_draws": draws,
        "interpretation": "Task-stratified descriptive contrast; not corrected multi-hypothesis significance",
    }


def run(args):
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing overwrite: {args.output_dir}")
    inventory = validate_inventory(pd.read_csv(args.correctness))
    validation = merge_oof(pd.read_csv(args.validation_oof), inventory,
                           source="RQ1 validation", truth="truth",
                           predicted="prediction", variant="variant", seed="seed")
    selected = merge_oof(pd.read_csv(args.selected_oof), inventory,
                         source="RQ1 selected pipeline", truth="truth",
                         predicted="prediction")
    complete_oof(validation)
    complete_oof(selected)
    details = pd.concat([
        validation.assign(experiment="rq1_representation_validation"),
        selected.assign(experiment="rq1_nested_selected"),
    ], ignore_index=True)
    summaries = []
    for (experiment, seed, variant, status), group in details.groupby(
        ["experiment", "seed", "variant", "status"]
    ):
        summaries.append({
            "experiment": experiment, "seed": int(seed), "variant": variant,
            "correctness": status, **metrics(group),
        })
    primary = pd.DataFrame(summaries)
    contrasts = []
    for seed, block in validation.groupby("seed"):
        for status in ("pass", "fail", "untestable"):
            filtered = block.loc[block.status.eq(status)]
            variants = set(filtered.variant)
            for a, b in COMPARE:
                if a not in variants or b not in variants:
                    continue
                outcome = paired_bootstrap(filtered, a, b, draws=args.bootstrap_draws,
                                           seed=int(seed) + 100)
                if outcome is not None:
                    contrasts.append({"seed": int(seed), "correctness": status,
                                      **outcome})
    # Within-task correct-vs-incorrect differences are descriptive because
    # correctness groups can differ heavily by originating model.
    within_tasks = []
    for (seed, variant, task), block in validation.groupby(["seed", "variant", "task"]):
        passed = block.loc[block.status.eq("pass")]
        failed = block.loc[block.status.eq("fail")]
        if passed.empty or failed.empty:
            continue
        within_tasks.append({
            "seed": int(seed), "variant": variant, "task": task,
            "n_pass": len(passed), "n_fail": len(failed),
            "pass_accuracy": float((passed.truth == passed.prediction).mean()),
            "fail_accuracy": float((failed.truth == failed.prediction).mean()),
            "pass_minus_fail": float((passed.truth == passed.prediction).mean() -
                                     (failed.truth == failed.prediction).mean()),
        })
    args.output_dir.mkdir(parents=True)
    details[["experiment", "seed", "variant", "row_id", "task", "file_name",
             "truth", "prediction", "status"]].to_csv(
        args.output_dir / "correctness_joined_rq1_oof.csv", index=False
    )
    primary.to_csv(args.output_dir / "correctness_subgroup_metrics.csv", index=False)
    pd.DataFrame(contrasts).to_csv(args.output_dir / "correctness_paired_variant_contrasts.csv", index=False)
    pd.DataFrame(within_tasks).to_csv(args.output_dir / "within_task_correctness_differences.csv", index=False)
    summary = {
        "retained_programs": int(len(inventory)),
        "correctness_counts": {str(k): int(v) for k, v in inventory.status.value_counts().items()},
        "validation_seeds": sorted(int(x) for x in validation.seed.unique()),
        "validation_variants": sorted(validation.variant.unique().tolist()),
        "selected_pipeline_n_oof": int(len(selected)),
        "n_within_task_comparisons": len(within_tasks),
        "n_paired_variant_contrasts": len(contrasts),
        "limitations": [
            "No classifier is trained on a correct-only population; original task-disjoint OOF predictions are reused.",
            "Correctness means pass/fail on existing task oracle cases, not universal program correctness.",
            "Untestable is a separate group, not silently excluded or counted incorrect.",
            "Correctness groups are imbalanced by programming task and originating LLM.",
            "Within-task accuracy differences are descriptive, not causal correctness effects.",
            "Task bootstrap contrasts are unadjusted, descriptive confidence intervals; multiple-testing control is not claimed.",
            "The selected nested pipeline is a distinct, single-seed experiment; do not pool with three-seed representation study.",
        ],
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main():
    research = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--correctness", type=Path, default=research / "experiments/rq2_correctness_final_001/correctness_results.csv")
    p.add_argument("--validation-oof", type=Path, default=research / "experiments/rq1_validation_full_001/oof_predictions.csv")
    p.add_argument("--selected-oof", type=Path, default=research / "experiments/rq1_nested_full_001/selected_oof_predictions.csv")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--bootstrap-draws", type=int, default=2000)
    args = p.parse_args()
    if args.bootstrap_draws < 100:
        p.error("--bootstrap-draws must be at least 100")
    run(args)


if __name__ == "__main__":
    main()
