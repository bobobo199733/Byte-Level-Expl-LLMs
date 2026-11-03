"""RQ2: out-of-task explanations of a full-opcode attribution classifier.

This is **classifier** explainability, not causal explanation of LLM generation.
We use exact linear, interventional-background SHAP contributions in *logit*
space for a multinomial logistic classifier. Features are full-program
relative opcode frequencies; the independent-feature intervention is a
mathematical model explanation, not a valid modification to Python code.

From repository root:
  python research/rq2/run_explanations.py --output-dir research/experiments/rq2_opcode_001

Python 3.13 required to reproduce historical opcode features.
Only source compilation/disassembly occurs; generated programs are NOT run.
"""
from __future__ import annotations

import argparse
import dis
import hashlib
import json
import platform
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RQ1_DIR = Path(__file__).resolve().parents[1] / "rq1"
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
for directory in (RQ1_DIR, SCRIPTS_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from run_nested_cv import CLASSES, DEFAULT_TRAIN, DEFAULT_TEST, RESEARCH_ROOT, assert_partition, file_digest, load_dataset, paired_task_bootstrap  # noqa: E402
from run_validation import build_validation_features, source_path  # noqa: E402
from bytecode_utils import instruction_trace_from_file  # noqa: E402

METHOD = "linear_interventional_shap_logit"


def linear_logit_shap(
    fitted_pipeline: Pipeline, X: np.ndarray, train_mean: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Exact independent-feature linear SHAP for a reference at train_mean.

    For a linear decision function, E[f(X) | do(X_S=x_S)] with an
    independent-feature interventional background has contributions
    (x_j - mean_train_j) * coefficient_j on the LOGIT scale. The
    baseline includes the intercept plus coefficient-weighted background
    after scaling. Outputs: [n_samples, n_features, n_classes] and
    [n_classes] background logits, ordered by estimator.classes_.
    """
    scaler = fitted_pipeline.named_steps["scale"]
    model = fitted_pipeline.named_steps["clf"]
    if len(model.classes_) != len(CLASSES):
        raise ValueError("Expected three classes for multinomial logit SHAP")
    coef = model.coef_ / scaler.scale_[None, :]
    base = model.intercept_ + (train_mean - scaler.mean_) @ coef.T
    attr = (X - train_mean[None, :])[:, :, None] * coef.T[None, :, :]
    return attr, base


def attribution_diagnostics(
    fitted_pipeline: Pipeline, X: np.ndarray, ref_mean: np.ndarray,
    attr: np.ndarray, base: np.ndarray, *, atol: float = 1e-8
) -> dict:
    logits = fitted_pipeline.decision_function(X)
    recovered = base[None, :] + attr.sum(axis=1)
    max_residual = float(np.max(np.abs(logits - recovered)))
    if max_residual > atol:
        raise AssertionError(f"SHAP logit additivity failed: {max_residual}")
    # Replace ONE feature at a time by its outer-training mean. This tests
    # the trained classifier, not whether the perturbed vector is valid code.
    rng = range(min(len(X), 10))
    cols = range(min(X.shape[1], 15))
    errors = []
    for row in rng:
        for col in cols:
            edited = X[row].copy()
            edited[col] = ref_mean[col]
            new_logits = fitted_pipeline.decision_function(edited.reshape(1, -1))[0]
            delta = logits[row] - new_logits
            errors.append(float(np.max(np.abs(delta - attr[row, col]))))
    intervention_residual = max(errors, default=0.0)
    if intervention_residual > atol:
        raise AssertionError(
            f"Single-feature logit intervention failed: {intervention_residual}"
        )
    return {
        "max_logit_additivity_error": max_residual,
        "max_feature_replacement_error": intervention_residual,
        "scale": "decision_function_logit",
        "background": "outer_training_mean",
        "intervention_warning": "A modified feature vector need not represent valid Python code",
    }


def frequency_baseline(
    Xtrain: np.ndarray, ytrain: np.ndarray, class_index: int,
) -> np.ndarray:
    """Direct class-minus-rest mean frequency, computed on training tasks only."""
    inside = Xtrain[ytrain == class_index]
    outside = Xtrain[ytrain != class_index]
    if len(inside) < 1 or len(outside) < 1:
        raise ValueError("Missing train class for frequency baseline")
    return inside.mean(axis=0) - outside.mean(axis=0)


def select_top_indices(values: np.ndarray, count: int) -> np.ndarray:
    # Deterministic stable ranking, even when importance ties exactly.
    return np.argsort(-np.asarray(values), kind="stable")[:count]


def jaccard(a: set[int], b: set[int]) -> float:
    return len(a & b) / len(a | b) if (a | b) else 1.0


def evidence_for_feature(
    root: Path, filename: str, true_model: str, split: str,
    opcode: int, target_function: str, *, maximum: int = 3,
) -> dict:
    file = source_path(root, filename, true_model, split)
    trace = instruction_trace_from_file(file, target_function)
    matching = [x for x in trace if x["opcode"] == opcode]
    return {
        "file_name": filename,
        "source_path": str(file.relative_to(root)),
        "opcode": int(opcode),
        "opname": dis.opname[opcode],
        "occurrences": len(matching),
        "sample_source_lines": [
            {"normalized_line": item["lineno"],
             "normalized_source": item["source_line"],
             "function": item["co_name"],
             "instruction_offset": item["dis_offset"]}
            for item in matching[:maximum]
        ],
        "line_number_warning": "Compiled AST-normalized source positions; not original raw file lines",
    }


def nested_explanations(
    df: pd.DataFrame, X: np.ndarray, root: Path, *,
    seeds: list[int], outer_folds: int, inner_folds: int,
    top_k: int, jobs: int, max_examples: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ytext = df["model"].to_numpy()
    encoded = np.array([CLASSES.index(x) for x in ytext], dtype=np.int64)
    groups = df["_task"].to_numpy()
    filenames = df["file_name"].to_numpy()
    splits = df["_historical_split"].to_numpy()
    n = len(X)
    if n < 3 or len(np.unique(groups)) < max(outer_folds, inner_folds + 1):
        raise ValueError("Not enough samples/tasks")
    pred_rows, feature_rows, audit_rows, fold_rows, evidence_rows = [], [], [], [], []
    meta_names = {}
    for seed in seeds:
        splitter = StratifiedGroupKFold(
            n_splits=outer_folds, shuffle=True, random_state=seed
        )
        for fold, (tr, te) in enumerate(splitter.split(X, encoded, groups), 1):
            assert_partition(tr, te, groups)
            inner_cv = list(StratifiedGroupKFold(
                n_splits=inner_folds, shuffle=True,
                random_state=seed + 10000 + fold,
            ).split(X[tr], encoded[tr], groups[tr]))
            for a, b in inner_cv:
                assert_partition(a, b, groups[tr])
            search = GridSearchCV(
                Pipeline([
                    ("scale", StandardScaler()),
                    ("clf", LogisticRegression(max_iter=2500, random_state=seed)),
                ]),
                {"clf__C": [0.1, 1.0, 10.0]},
                cv=inner_cv, scoring="f1_macro", n_jobs=jobs,
                refit=True, error_score="raise",
            )
            search.fit(X[tr], encoded[tr])
            fitted = search.best_estimator_
            output = fitted.predict(X[te]).astype(int)
            proba = fitted.predict_proba(X[te])
            train_mean = X[tr].mean(axis=0)
            contrib_test, baseline = linear_logit_shap(fitted, X[te], train_mean)
            contrib_train, _ = linear_logit_shap(fitted, X[tr], train_mean)
            diagnostics = attribution_diagnostics(
                fitted, X[te], train_mean, contrib_test, baseline
            )
            audit_rows.append({"seed": seed, "fold": fold, **diagnostics,
                               "train_task_count": len(set(groups[tr])),
                               "test_task_count": len(set(groups[te]))})
            fold_rows.append({
                "seed": seed, "fold": fold,
                "inner_macro_f1": float(search.best_score_),
                "best_C": float(search.best_params_["clf__C"]),
                "n_train": len(tr), "n_test": len(te),
                "task_disjoint": True,
                "accuracy": float(accuracy_score(encoded[te], output)),
                "macro_f1": float(f1_score(encoded[te], output, average="macro")),
            })
            for j, idx in enumerate(te):
                item = {
                    "seed": seed, "fold": fold, "row_id": int(idx),
                    "file_name": filenames[idx], "task": groups[idx],
                    "true_model": ytext[idx], "predicted_model": CLASSES[output[j]],
                    "confidence": float(proba[j, output[j]]),
                }
                for c, name in enumerate(CLASSES):
                    item[f"logit_{name}"] = float(
                        baseline[c] + contrib_test[j, :, c].sum()
                    )
                pred_rows.append(item)

            for cls, classname in enumerate(CLASSES):
                importance = np.mean(np.abs(contrib_train[:, :, cls]), axis=0)
                freq_diff = frequency_baseline(X[tr], encoded[tr], cls)
                baseline_rank = select_top_indices(np.abs(freq_diff), top_k)
                top = select_top_indices(importance, top_k)
                overlap = jaccard(set(map(int, top)), set(map(int, baseline_rank)))
                # Selection only uses TRAIN tasks; supporting examples and
                # observed contribution signs are inspected on held-out tasks.
                for rank, feat in enumerate(top, 1):
                    held = contrib_test[:, feat, cls]
                    row = {
                        "seed": seed, "fold": fold, "class": classname,
                        "rank": rank, "feature": f"opcode_{feat}",
                        "opcode": int(feat), "opname": dis.opname[int(feat)],
                        "train_mean_abs_logit_shap": float(importance[feat]),
                        "training_class_minus_rest_frequency": float(freq_diff[feat]),
                        "topk_overlap_with_frequency_baseline": overlap,
                        "test_mean_logit_shap": float(np.mean(held)),
                        "test_mean_abs_logit_shap": float(np.mean(np.abs(held))),
                        "test_positive_fraction": float(np.mean(held > 0)),
                        "test_opcode_present_fraction": float(np.mean(X[te, feat] > 0)),
                    }
                    feature_rows.append(row)

                for feature_idx in top[:min(3, len(top))]:
                    ranking = np.argsort(-contrib_test[:, feature_idx, cls])
                    examples = 0
                    for test_pos in ranking:
                        if examples >= max_examples:
                            break
                        if contrib_test[test_pos, feature_idx, cls] <= 0:
                            break
                        if X[te[test_pos], feature_idx] <= 0:
                            continue
                        idx = int(te[test_pos])
                        task = str(groups[idx])
                        key = (task, splits[idx])
                        if key not in meta_names:
                            folder = "prompts" if splits[idx] == "train" else "test_data/prompts"
                            path = root / folder / task / "meta.json"
                            meta_names[key] = json.loads(path.read_text())["function_name"]
                        proof = evidence_for_feature(
                            root, str(filenames[idx]), str(ytext[idx]),
                            str(splits[idx]), int(feature_idx), meta_names[key],
                        )
                        if proof["occurrences"] <= 0:
                            raise AssertionError("Nonzero opcode frequency without a matching instruction")
                        evidence_rows.append({
                            "seed": seed, "fold": fold, "explained_class": classname,
                            "true_model": ytext[idx], "prediction": CLASSES[output[test_pos]],
                            "feature": f"opcode_{feature_idx}",
                            "heldout_logit_shap": float(contrib_test[test_pos, feature_idx, cls]),
                            "heldout_opcode_frequency": float(X[idx, feature_idx]),
                            **proof,
                        })
                        examples += 1
        print(f"Completed RQ2 outer folds for seed {seed}", flush=True)
    return (pd.DataFrame(pred_rows), pd.DataFrame(feature_rows),
            pd.DataFrame(audit_rows), pd.DataFrame(fold_rows),
            pd.DataFrame(evidence_rows))


def stability_table(features: pd.DataFrame, top_k: int) -> pd.DataFrame:
    """Top-k SHAP rank-set stability across independent outer models."""
    rows = []
    for name, group in features.groupby("class"):
        sets = [
            set(subset.loc[subset["rank"] <= top_k, "opcode"].astype(int))
            for _, subset in group.groupby(["seed", "fold"])
        ]
        scores = [jaccard(a, b) for a, b in combinations(sets, 2)]
        counts = group.loc[group["rank"] <= top_k].groupby(
            ["opcode", "opname"]
        ).size().sort_values(ascending=False)
        rows.append({
            "class": name, "n_models": len(sets), "k": top_k,
            "mean_pairwise_topk_jaccard": float(np.mean(scores)) if scores else None,
            "min_pairwise_topk_jaccard": float(min(scores)) if scores else None,
            "max_pairwise_topk_jaccard": float(max(scores)) if scores else None,
            "top_recurrent_features": json.dumps([
                {"opcode": int(op), "opname": opname, "fold_support": int(n)}
                for (op, opname), n in counts.head(top_k).items()
            ]),
        })
    return pd.DataFrame(rows)


def summarize(predictions, features, audits, folds, stability) -> dict:
    by_seed = {}
    for seed, block in predictions.groupby("seed"):
        by_seed[str(seed)] = {
            "n": len(block), "n_tasks": int(block["task"].nunique()),
            "accuracy": float(accuracy_score(block["true_model"], block["predicted_model"])),
            "macro_f1": float(f1_score(
                block["true_model"], block["predicted_model"], labels=CLASSES,
                average="macro", zero_division=0,
            )),
            "confusion_matrix": confusion_matrix(
                block["true_model"], block["predicted_model"], labels=CLASSES
            ).tolist(),
        }
    comparison = features.groupby("class").agg(
        mean_train_importance=("train_mean_abs_logit_shap", "mean"),
        mean_frequency_baseline_overlap=("topk_overlap_with_frequency_baseline", "mean"),
        mean_heldout_positive_fraction=("test_positive_fraction", "mean"),
    ).to_dict(orient="index")
    return {
        "method": METHOD,
        "scale": "logit",
        "n_seed_evaluations": len(by_seed),
        "n_outer_models": len(audits),
        "by_seed": by_seed,
        "max_additivity_error": float(audits["max_logit_additivity_error"].max()),
        "max_feature_intervention_error": float(audits["max_feature_replacement_error"].max()),
        "per_class_selected_feature_summary": comparison,
        "attribution_rank_stability": stability.to_dict(orient="records"),
        "cautions": [
            "SHAP explains the auxiliary code-origin classifier, NOT why an LLM generated code",
            "Relative opcode features are correlated and constrained to sum to one; independent interventions may leave the feasible input manifold",
            "Feature-level intervention checks are algebraic/model-based; they are NOT semantics-preserving code interventions",
            "Repeated task splits reuse the same tasks and are not statistically independent samples",
            "Importance overlap with raw frequency differences does not prove added explanatory value",
        ],
    }


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    p.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    p.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--seeds", nargs="+", type=int, default=[7, 42, 101])
    p.add_argument("--outer-folds", type=int, default=5)
    p.add_argument("--inner-folds", type=int, default=4)
    p.add_argument("--top-k", type=int, default=10)
    p.add_argument("--max-examples", type=int, default=2)
    p.add_argument("--jobs", type=int, default=1)
    p.add_argument("--prepare-only", action="store_true")
    return p.parse_args(argv)


def main(args=None):
    args = parse_args() if args is None else args
    if (args.outer_folds < 2 or args.inner_folds < 2 or args.top_k < 1
            or args.top_k > 256 or args.max_examples < 0):
        raise ValueError("Invalid fold or explanation configuration")
    if len(set(args.seeds)) != len(args.seeds) or not args.seeds:
        raise ValueError("Seeds must be nonempty and unique")
    if args.output_dir.exists():
        raise FileExistsError(f"Will not overwrite previous experiment: {args.output_dir}")
    df, columns = load_dataset(args.train_csv, args.test_csv)
    features, source_audit = build_validation_features(
        df, columns, args.research_root, ("opcode_full",), ngram_buckets=256
    )
    X = features["opcode_full"].to_numpy(dtype=float)
    if not np.allclose(X.sum(axis=1), 1.0, atol=1e-12):
        raise AssertionError("Relative opcode frequencies do not sum to one")
    args.output_dir.mkdir(parents=True)
    source_audit.to_csv(args.output_dir / "source_audit.csv", index=False)
    manifest = {
        "method": METHOD,
        "feature_representation": "complete_opcode_relative_frequencies",
        "source_line_provenance": "AST_normalized_source",
        "attribution_background": "outer_training_mean",
        "attribution_scale": "multiclass_logit",
        "topk_selection": "train_only_class_specific_mean_absolute_attribution",
        "seeds": args.seeds, "outer_folds": args.outer_folds,
        "inner_folds": args.inner_folds, "top_k": args.top_k,
        "classes": list(CLASSES), "n_programs": len(df),
        "n_tasks": int(df["_task"].nunique()),
        "python": platform.python_version(),
        "numpy": np.__version__, "pandas": pd.__version__,
        "sklearn": __import__("sklearn").__version__,
        "train_csv_sha256": file_digest(args.train_csv),
        "test_csv_sha256": file_digest(args.test_csv),
        "source_audit_sha256": file_digest(args.output_dir / "source_audit.csv"),
        "prepare_only": bool(args.prepare_only),
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if args.prepare_only:
        print(f"Audited all {len(df)} programs; outputs at {args.output_dir.resolve()}")
        return
    predictions, top_features, audits, folds, evidence = nested_explanations(
        df, X, args.research_root, seeds=args.seeds,
        outer_folds=args.outer_folds, inner_folds=args.inner_folds,
        top_k=args.top_k, jobs=args.jobs, max_examples=args.max_examples,
    )
    if len(predictions) != len(df) * len(args.seeds):
        raise AssertionError("Out-of-fold prediction count incomplete")
    if predictions.duplicated(["seed", "row_id"]).any():
        raise AssertionError("A program appears twice in the same seed")
    stable = stability_table(top_features, args.top_k)
    predictions.to_csv(args.output_dir / "oof_predictions.csv", index=False)
    top_features.to_csv(args.output_dir / "feature_attributions.csv", index=False)
    audits.to_csv(args.output_dir / "faithfulness_audit.csv", index=False)
    folds.to_csv(args.output_dir / "fold_scores.csv", index=False)
    stable.to_csv(args.output_dir / "rank_stability.csv", index=False)
    if not evidence.empty:
        evidence.to_json(args.output_dir / "source_evidence.json", orient="records", indent=2)
    report = summarize(predictions, top_features, audits, folds, stable)
    (args.output_dir / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"Saved RQ2 experiment to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
