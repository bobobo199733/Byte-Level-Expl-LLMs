"""RQ1: nested task-disjoint model-origin attribution experiments.

Run from repository root:
  python research/rq1/run_nested_cv.py --output-dir research/experiments/rq1_001

Requires numpy, pandas, scikit-learn; XGBoost only if --models includes xgboost.
Do not change the historical features or stored baseline model.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRAIN = RESEARCH_ROOT / "features" / "processed_bytecode_features.csv"
DEFAULT_TEST = RESEARCH_ROOT / "test_data" / "features" / "processed_bytecode_features.csv"
CLASSES = ("llama", "mistral", "qwen")
AST_NODE_NAMES = (
    "FunctionDef", "AsyncFunctionDef", "ClassDef", "Return", "Assign",
    "AnnAssign", "AugAssign", "If", "For", "AsyncFor", "While", "Try",
    "ExceptHandler", "With", "AsyncWith", "Call", "Name", "Constant",
    "Attribute", "Subscript", "BinOp", "BoolOp", "Compare", "IfExp",
    "Lambda", "ListComp", "DictComp", "SetComp", "GeneratorExp",
    "List", "Tuple", "Dict", "Set", "Import", "ImportFrom", "Yield",
    "YieldFrom", "Await", "Raise", "Assert", "Break", "Continue",
)
FEATURE_FAMILIES = ("positional", "opcode_hist", "ast")
MODEL_NAMES = ("xgboost", "logistic", "random_forest")


def task_id(filename: str) -> str:
    match = re.fullmatch(r"(t[0-9]+)_p[0-9]+_r[0-9]+_(llama|mistral|qwen)\.py", filename)
    if match is None:
        raise ValueError(f"Invalid filename, cannot guarantee task grouping: {filename!r}")
    return match.group(1)


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_dataset(train: Path, test: Path) -> tuple[pd.DataFrame, list[str]]:
    a = pd.read_csv(train)
    b = pd.read_csv(test)
    if a.columns.tolist() != b.columns.tolist():
        raise ValueError("Training and test CSV schemas differ")
    for required in ("model", "file_name"):
        if required not in a:
            raise ValueError(f"Missing required column: {required}")
    features = [c for c in a if re.fullmatch(r"byte_[0-9]+", c)]
    ordered = sorted(features, key=lambda c: int(c[5:]))
    if [int(c[5:]) for c in ordered] != list(range(len(ordered))):
        raise ValueError("Positional feature columns must cover 0..N-1")
    if not features:
        raise ValueError("No positional features found")
    df = pd.concat(
        [a.assign(_historical_split="train"), b.assign(_historical_split="test")],
        ignore_index=True,
    )
    if df["file_name"].isna().any() or df["file_name"].duplicated().any():
        raise ValueError("Missing or duplicate file names")
    df["_task"] = df["file_name"].map(task_id)
    if set(a["file_name"].map(task_id)) & set(b["file_name"].map(task_id)):
        raise ValueError("Original train/test partitions overlap by task")
    if set(df["model"]) != set(CLASSES):
        raise ValueError(f"Expected exactly three known classes: {CLASSES}")
    if df[ordered].isna().any().any():
        raise ValueError("Missing byte values; refusing imputation")
    numeric = df[ordered].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError("Byte features must be finite")
    if not np.array_equal(numeric.to_numpy(), numeric.to_numpy().astype(np.int64)):
        raise ValueError("Byte features must be integer-valued")
    df[ordered] = numeric.astype(np.int64)
    # Even positions are opcodes; odd positions are decoded arguments.
    opcode_values = df[ordered[::2]].to_numpy()
    if ((opcode_values < -1) | (opcode_values > 255)).any():
        raise ValueError("Unexpected opcode values outside -1..255")
    if len(df["_task"].unique()) < 8:
        raise ValueError("Not enough distinct tasks for nested grouped validation")
    return df, ordered


def ast_features(df: pd.DataFrame, root: Path) -> pd.DataFrame:
    """Source AST count baseline: parse archived cleaned programs, never execute."""
    vectors = []
    source_inventory = []
    for filename, model, split in df[
        ["file_name", "model", "_historical_split"]
    ].itertuples(index=False, name=None):
        subdir = "outputs" if split == "train" else "test_data/outputs"
        file = root / subdir / model / "cleaned" / filename
        if not file.is_file():
            raise FileNotFoundError(f"Missing archived source for AST baseline: {file}")
        source = file.read_text(encoding="utf-8")
        source_inventory.append({
            "file_name": filename,
            "source_path": str(file.relative_to(root)),
            "source_sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
        })
        tree = ast.parse(source, filename=str(file))
        counts = Counter(type(n).__name__ for n in ast.walk(tree))
        record = {f"ast_{name}": counts.get(name, 0) for name in AST_NODE_NAMES}
        record["ast_total_nodes"] = sum(counts.values())
        record["ast_source_lines"] = len(source.splitlines())
        vectors.append(record)
    features = pd.DataFrame(vectors, dtype=float)
    features.attrs["source_inventory"] = source_inventory
    return features


def build_representations(
    df: pd.DataFrame, columns: list[str], root: Path, selected: list[str]
) -> dict[str, pd.DataFrame]:
    result = {}
    if "positional" in selected:
        result["positional"] = df[columns].astype(float).reset_index(drop=True)
    if "opcode_hist" in selected:
        values = df[columns[::2]].to_numpy(dtype=np.int64)
        counts = np.array(
            [np.bincount(row[row >= 0], minlength=256)[:256] for row in values],
            dtype=np.float64,
        )
        # Normalize by the number of observed opcode instructions, so code length
        # is not implicitly the only discriminative factor.
        totals = counts.sum(axis=1, keepdims=True)
        counts = counts / np.maximum(totals, 1.0)
        result["opcode_hist"] = pd.DataFrame(
            counts, columns=[f"opcode_{i}" for i in range(256)]
        )
    if "ast" in selected:
        result["ast"] = ast_features(df, root)
    return result


def estimator_grid(name: str, seed: int):
    if name == "xgboost":
        try:
            from xgboost import XGBClassifier
        except ImportError as exc:
            raise RuntimeError("Install xgboost or omit it from --models") from exc
        est = XGBClassifier(
            objective="multi:softprob", eval_metric="mlogloss",
            random_state=seed, n_jobs=1, tree_method="hist",
        )
        return est, {"n_estimators": [250], "max_depth": [3, 5],
                     "learning_rate": [0.05], "subsample": [0.8],
                     "colsample_bytree": [0.8]}
    if name == "logistic":
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=seed)),
        ])
        return pipe, {"clf__C": [0.1, 1.0, 10.0]}
    if name == "random_forest":
        from sklearn.ensemble import RandomForestClassifier
        est = RandomForestClassifier(
            n_estimators=300, random_state=seed, n_jobs=1,
            class_weight="balanced_subsample",
        )
        return est, {"max_features": ["sqrt"], "min_samples_leaf": [1, 3]}
    raise ValueError(f"Unknown model: {name}")


def metrics(y_true, y_pred) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=list(CLASSES), average="macro", zero_division=0)),
    }


def bootstrap_by_task(predictions: pd.DataFrame, *, draws: int, seed: int) -> dict:
    """Percentile bootstrap over TASKS, preserving all generations per task."""
    rng = np.random.default_rng(seed)
    tasks = np.array(sorted(predictions["task"].unique()))
    if len(tasks) < 2 or draws < 1:
        raise ValueError("Need at least two tasks and one bootstrap draw")
    blocks = {
        task: predictions.loc[predictions["task"] == task, ["truth", "prediction"]]
        for task in tasks
    }
    draws_by_metric = {k: [] for k in ("accuracy", "balanced_accuracy", "macro_f1")}
    for _ in range(draws):
        sampled = rng.choice(tasks, size=len(tasks), replace=True)
        sample = pd.concat([blocks[task] for task in sampled], ignore_index=True)
        score = metrics(sample["truth"], sample["prediction"])
        for name in draws_by_metric:
            draws_by_metric[name].append(score[name])
    return {
        name: {
            "lower_95": float(np.quantile(values, 0.025)),
            "upper_95": float(np.quantile(values, 0.975)),
        }
        for name, values in draws_by_metric.items()
    }



def paired_task_bootstrap(
    selected: pd.DataFrame, baseline: pd.DataFrame, *, draws: int, seed: int
) -> dict:
    """Paired task-bootstrap score differences on identical out-of-fold samples.

    A confidence interval excluding zero is descriptive evidence of a
    difference on these tasks, not a license for post-hoc model selection.
    """
    selected = selected.sort_values("row_id").reset_index(drop=True)
    baseline = baseline.sort_values("row_id").reset_index(drop=True)
    if not np.array_equal(selected["row_id"], baseline["row_id"]):
        raise ValueError("Cannot pair predictions with different row IDs")
    if not np.array_equal(selected["truth"], baseline["truth"]):
        raise ValueError("Cannot pair predictions with different labels")
    if not np.array_equal(selected["task"], baseline["task"]):
        raise ValueError("Cannot pair predictions with different task IDs")
    tasks = np.array(sorted(selected["task"].unique()))
    by_task = {
        task: selected.index[selected["task"] == task].to_numpy(dtype=int)
        for task in tasks
    }
    selected_scores = metrics(selected["truth"], selected["prediction"])
    baseline_scores = metrics(baseline["truth"], baseline["prediction"])
    rng = np.random.default_rng(seed)
    values = {"accuracy": [], "macro_f1": [], "balanced_accuracy": []}
    truth = selected["truth"].to_numpy()
    a = selected["prediction"].to_numpy()
    b = baseline["prediction"].to_numpy()
    for _ in range(draws):
        indices = np.concatenate([
            by_task[task] for task in rng.choice(tasks, size=len(tasks), replace=True)
        ])
        sm = metrics(truth[indices], a[indices])
        bm = metrics(truth[indices], b[indices])
        for key in values:
            values[key].append(sm[key] - bm[key])
    return {
        key: {
            "observed_difference": selected_scores[key] - baseline_scores[key],
            "lower_95": float(np.quantile(sample, 0.025)),
            "upper_95": float(np.quantile(sample, 0.975)),
            "bootstrap_fraction_positive": float(np.mean(np.array(sample) > 0)),
        }
        for key, sample in values.items()
    }


def assert_partition(train_ids, test_ids, groups):
    first = set(groups[np.asarray(train_ids, dtype=int)])
    second = set(groups[np.asarray(test_ids, dtype=int)])
    if first & second:
        raise AssertionError(f"Task leakage between folds: {sorted(first & second)}")
    if not first or not second:
        raise AssertionError("Empty training or test tasks")


def run_experiment(args):
    df, feature_names = load_dataset(args.train_csv, args.test_csv)
    if args.outer_folds < 2 or args.inner_folds < 2:
        raise ValueError("Both fold counts must be >= 2")
    if args.bootstrap_draws < 1:
        raise ValueError("Bootstrap draws must be >= 1")

    groups = df["_task"].to_numpy()
    y_text = df["model"].to_numpy()
    class_to_int = {name: i for i, name in enumerate(CLASSES)}
    y = np.asarray([class_to_int[x] for x in y_text], dtype=int)
    representations = build_representations(
        df, feature_names, args.research_root, args.representations
    )
    if len(np.unique(groups)) < args.outer_folds:
        raise ValueError("Insufficient unique tasks for requested outer folds")
    outer_splitter = GroupKFold(n_splits=args.outer_folds)
    outer_splits = list(outer_splitter.split(np.zeros(len(y)), y, groups))
    if min(len(set(groups[train_idx])) for train_idx, _ in outer_splits) < args.inner_folds:
        raise ValueError("Not enough outer-training tasks for requested inner folds")

    out = args.output_dir
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite existing experiment directory: {out}")
    out.mkdir(parents=True)

    if "ast" in representations:
        inventory = pd.DataFrame(representations["ast"].attrs["source_inventory"])
        inventory.to_csv(out / "ast_source_inventory.csv", index=False)
        source_digest = hashlib.sha256(
            inventory.to_csv(index=False).encode("utf-8")
        ).hexdigest()
    else:
        source_digest = None

    manifest = {
        "ast_source_inventory_sha256": source_digest,
        "method": "nested_groupkfold_classification",
        "description": "Source-independent model attribution across disjoint programming tasks",
        "timestamp_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "seed": args.seed,
        "outer_folds": args.outer_folds,
        "inner_folds": args.inner_folds,
        "bootstrap_draws": args.bootstrap_draws,
        "representations": args.representations,
        "models": args.models,
        "classes": list(CLASSES),
        "n_samples": int(len(df)),
        "n_tasks": int(len(np.unique(groups))),
        "train_csv": str(args.train_csv.resolve()),
        "test_csv": str(args.test_csv.resolve()),
        "train_sha256": file_digest(args.train_csv),
        "test_sha256": file_digest(args.test_csv),
        "source_inventory_file": "ast_source_inventory.csv" if source_digest else None,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "sklearn_version": __import__("sklearn").__version__,
        "xgboost_version": (
            __import__("xgboost").__version__ if "xgboost" in args.models else None
        ),
        "representation_length": len(feature_names),
        "note": "AST baseline reads original archived cleaned sources; does not run them.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    fold_rows = []
    chosen_predictions = []
    all_candidate_predictions = []
    for fold, (outer_train, outer_test) in enumerate(
        outer_splits, start=1
    ):
        assert_partition(outer_train, outer_test, groups)
        inner_groups = groups[outer_train]
        inner_cv = list(GroupKFold(n_splits=args.inner_folds).split(
            np.zeros(len(outer_train)), y[outer_train], inner_groups
        ))
        for itrain, ival in inner_cv:
            assert_partition(itrain, ival, inner_groups)

        winners = []
        for representation_name, Xdf in representations.items():
            X = Xdf.to_numpy(dtype=float)
            Xtr, Xte = X[outer_train], X[outer_test]
            for model_name in args.models:
                estimator, grid = estimator_grid(model_name, args.seed)
                search = GridSearchCV(
                    estimator, grid, scoring="f1_macro",
                    cv=inner_cv, n_jobs=args.jobs, refit=True,
                    error_score="raise", return_train_score=False,
                )
                search.fit(Xtr, y[outer_train])
                pred = search.best_estimator_.predict(Xte).astype(int)
                record = {
                    "fold": fold, "representation": representation_name,
                    "model": model_name, "inner_macro_f1": float(search.best_score_),
                    "parameters": json.dumps(search.best_params_, sort_keys=True),
                    **metrics(y_text[outer_test], np.array(CLASSES)[pred]),
                }
                fold_rows.append(record)
                winners.append((search.best_score_, representation_name, model_name, pred))
                for index, prediction in zip(outer_test, pred):
                    all_candidate_predictions.append({
                        "fold": fold, "row_id": int(index),
                        "task": groups[index], "file_name": df.iloc[index]["file_name"],
                        "truth": y_text[index],
                        "representation": representation_name,
                        "model": model_name,
                        "prediction": CLASSES[prediction],
                    })

        # Select representation AND model exclusively by grouped inner-CV score.
        # Sorted tie-breaking is deterministic, independent of test performance.
        best = sorted(winners, key=lambda x: (-x[0], x[1], x[2]))[0]
        _, rep, mod, pred = best
        for index, prediction in zip(outer_test, pred):
            chosen_predictions.append({
                "fold": fold, "row_id": int(index),
                "task": groups[index], "file_name": df.iloc[index]["file_name"],
                "truth": y_text[index], "prediction": CLASSES[prediction],
                "chosen_representation": rep, "chosen_model": mod,
            })

        # Non-learned majority-class control, trained only on outer train.
        dummy = DummyClassifier(strategy="most_frequent")
        dummy.fit(np.zeros((len(outer_train), 1)), y[outer_train])
        naive_pred = dummy.predict(np.zeros((len(outer_test), 1)))
        for index, prediction in zip(outer_test, naive_pred):
            all_candidate_predictions.append({
                "fold": fold, "row_id": int(index),
                "task": groups[index], "file_name": df.iloc[index]["file_name"],
                "truth": y_text[index], "representation": "control",
                "model": "majority", "prediction": CLASSES[int(prediction)],
            })
        print(f"Fold {fold}/{args.outer_folds}: "
              f"selected {rep}/{mod}, inner F1={best[0]:.4f}, "
              f"held-out tasks={len(set(groups[outer_test]))}", flush=True)

    selected = pd.DataFrame(chosen_predictions).sort_values("row_id")
    if not np.array_equal(selected["row_id"].to_numpy(), np.arange(len(df))):
        raise AssertionError("Each sample must be held out exactly once")
    candidate = pd.DataFrame(all_candidate_predictions)
    scores = {
        "selected_nested": summarize_predictions(selected, args.bootstrap_draws, args.seed)
    }
    for (rep, model), subset in candidate.groupby(["representation", "model"]):
        subset = subset.sort_values("row_id")
        if not np.array_equal(subset["row_id"].to_numpy(), np.arange(len(df))):
            raise AssertionError(f"Candidate {rep}/{model} lacks held-out coverage")
        scores[f"{rep}/{model}"] = summarize_predictions(
            subset, args.bootstrap_draws, args.seed
        )
    pairwise = {}
    for (rep, model), subset in candidate.groupby(["representation", "model"]):
        pairwise[f"selected_vs_{rep}/{model}"] = paired_task_bootstrap(
            selected, subset, draws=args.bootstrap_draws, seed=args.seed,
        )
    (out / "paired_comparisons.json").write_text(
        json.dumps(pairwise, indent=2) + "\n"
    )
    selected.to_csv(out / "selected_oof_predictions.csv", index=False)
    candidate.to_csv(out / "candidate_oof_predictions.csv", index=False)
    pd.DataFrame(fold_rows).to_csv(out / "fold_scores.csv", index=False)
    (out / "results.json").write_text(json.dumps(scores, indent=2) + "\n")
    task_report = selected.groupby("task").apply(
        lambda block: pd.Series({
            "n": len(block),
            "accuracy": float(np.mean(block["truth"] == block["prediction"])),
        }),
        include_groups=False,
    ).reset_index()
    task_report.to_csv(out / "task_scores.csv", index=False)
    print(json.dumps(scores["selected_nested"], indent=2))
    print(f"Saved results to {out.resolve()}")


def summarize_predictions(predictions: pd.DataFrame, draws: int, seed: int) -> dict:
    truth = predictions["truth"].to_numpy()
    pred = predictions["prediction"].to_numpy()
    return {
        "n": len(predictions),
        "n_tasks": int(predictions["task"].nunique()),
        **metrics(truth, pred),
        "bootstrap_task_95": bootstrap_by_task(predictions, draws=draws, seed=seed),
        "classification_report": classification_report(
            truth, pred, labels=list(CLASSES), output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(truth, pred, labels=list(CLASSES)).tolist(),
        "class_order": list(CLASSES),
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    parser.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--representations", nargs="+", choices=FEATURE_FAMILIES,
                        default=list(FEATURE_FAMILIES))
    parser.add_argument("--models", nargs="+", choices=MODEL_NAMES,
                        default=["xgboost", "logistic"])
    parser.add_argument("--outer-folds", type=int, default=5)
    parser.add_argument("--inner-folds", type=int, default=4)
    parser.add_argument("--bootstrap-draws", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--jobs", type=int, default=1)
    return parser.parse_args(argv)


if __name__ == "__main__":
    run_experiment(parse_args())
