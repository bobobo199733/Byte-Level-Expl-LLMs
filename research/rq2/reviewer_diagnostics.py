"""Reviewer diagnostics from existing RQ2 held-out predictions and explanations.

Provides task-cluster confidence intervals, per-class metrics, recurrent
feature task coverage and counterexamples. No retraining or code execution.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_recall_fscore_support

CLASSES = ("llama", "mistral", "qwen")


def score(y, p):
    precision, recall, fs, support = precision_recall_fscore_support(
        y, p, labels=CLASSES, zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(y, p)),
        "balanced_accuracy": float(balanced_accuracy_score(y, p)),
        "macro_f1": float(f1_score(y, p, labels=CLASSES, average="macro", zero_division=0)),
        "by_class": {
            cl: {"precision": float(precision[i]), "recall": float(recall[i]),
                 "f1": float(fs[i]), "support": int(support[i])}
            for i, cl in enumerate(CLASSES)
        },
    }


def task_bootstrap(data: pd.DataFrame, *, draws: int, seed: int):
    rng = np.random.default_rng(seed)
    groups = [block for _, block in data.groupby("task")]
    observed = score(data["true_model"], data["predicted_model"])
    keys = ["accuracy", "balanced_accuracy", "macro_f1"]
    numbers = {key: [] for key in keys}
    class_recalls = {cl: [] for cl in CLASSES}
    for _ in range(draws):
        chosen = rng.integers(0, len(groups), len(groups))
        sample = pd.concat([groups[j] for j in chosen], ignore_index=True)
        val = score(sample["true_model"], sample["predicted_model"])
        for key in keys:
            numbers[key].append(val[key])
        for cl in CLASSES:
            class_recalls[cl].append(val["by_class"][cl]["recall"])
    return {
        "point": observed,
        "task_bootstrap_95": {
            key: [float(np.quantile(values, .025)), float(np.quantile(values, .975))]
            for key, values in numbers.items()
        },
        "per_class_recall_task_bootstrap_95": {
            key: [float(np.quantile(values, .025)), float(np.quantile(values, .975))]
            for key, values in class_recalls.items()
        },
    }


def run(input_dir: Path, output_dir: Path, draws: int, seed: int):
    if output_dir.exists():
        raise FileExistsError(f"Will not overwrite {output_dir}")
    if draws < 100:
        raise ValueError("Use >=100 bootstrap iterations")
    predicted = pd.read_csv(input_dir / "oof_predictions.csv")
    features = pd.read_csv(input_dir / "feature_attributions.csv")
    evidence_path = input_dir / "source_evidence.json"
    evidence = pd.read_json(evidence_path) if evidence_path.exists() else pd.DataFrame()
    needed = {"seed", "row_id", "task", "file_name", "true_model", "predicted_model"}
    if not needed.issubset(predicted):
        raise ValueError(f"Missing columns {needed - set(predicted)}")
    if predicted.duplicated(["seed","row_id"]).any():
        raise ValueError("Repeated OOF program row within a seed")
    summaries = {}
    for partition_seed, block in predicted.groupby("seed"):
        if block["task"].nunique() < 10:
            raise ValueError("Insufficient unique held-out tasks")
        summaries[str(partition_seed)] = task_bootstrap(
            block, draws=draws, seed=seed + int(partition_seed)
        )
    # Evidence file is deliberately curated, not a population sample.
    coverage = []
    if not evidence.empty:
        for (klass, opcode, opname), group in evidence.groupby(
            ["explained_class", "opcode", "opname"]
        ):
            confirmed = group[
                (group["true_model"] == klass)
                & (group["prediction"] == klass)
                & (group["heldout_logit_shap"] > 0)
            ]
            contrary = group[
                (group["true_model"] != klass)
                & (group["heldout_logit_shap"] > 0)
            ]
            coverage.append({
                "class": klass, "opcode": int(opcode), "opname": opname,
                "curated_examples": int(len(group)),
                "unique_tasks_in_curated_evidence": int(group["file_name"].str.extract(r"^(t\d+)")[0].nunique()),
                "unique_true_positive_tasks": int(confirmed["file_name"].str.extract(r"^(t\d+)")[0].nunique()),
                "true_positive_examples": len(confirmed),
                "counterexample_examples_from_other_models": len(contrary),
                "scope_warning": "Curated selected evidence, NOT population-wide task prevalence",
            })
    ranks = []
    for (klass, opcode), group in features.groupby(["class","opcode"]):
        ranks.append({
            "class": klass, "opcode": int(opcode),
            "fold_support": int(len(group)),
            "n_partition_seeds": int(group["seed"].nunique()),
            "mean_train_importance": float(group["train_mean_abs_logit_shap"].mean()),
            "positive_effect_fraction_on_heldout": float(group["test_positive_fraction"].mean()),
        })
    output_dir.mkdir(parents=True)
    pd.DataFrame(coverage).to_csv(output_dir / "curated_source_evidence_audit.csv", index=False)
    pd.DataFrame(ranks).sort_values(
        ["class","fold_support","opcode"], ascending=[True,False,True]
    ).to_csv(output_dir / "feature_recurrence.csv", index=False)
    report = {
        "method": "posthoc_review_diagnostics_no_retraining",
        "by_seed": summaries,
        "n_seeds": len(summaries),
        "n_unique_programs": int(predicted["row_id"].nunique()),
        "all_examples": int(len(predicted)),
        "warning": [
            "Three task partitions resample the same tasks and are not independent replications.",
            "Curated source evidence counts cannot establish prevalence in the full corpus.",
            "SHAP validates classifier logit contributions but not LLM internal causality.",
            "No correctness-controlled conclusions can be derived here.",
        ],
    }
    (output_dir / "review_diagnostics.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "by_seed": {key: {"accuracy":v["point"]["accuracy"],
                         "accuracy_ci":v["task_bootstrap_95"]["accuracy"]}
                    for key,v in summaries.items()},
        "evidence_cases": len(evidence), "n_recurrent_features": len(ranks)
    }, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-dir", type=Path,
                   default=Path(__file__).resolve().parents[1] / "experiments/rq2_opcode_full_001")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--bootstrap-draws", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()
    run(a.input_dir, a.output_dir, a.bootstrap_draws, a.seed)


if __name__ == "__main__":
    main()
