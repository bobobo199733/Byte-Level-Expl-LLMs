"""RQ1 validation: AST confound ablations, complete opcode baselines and repeatability.

No generated program is executed by this module. It reads archived source,
compiles it to bytecode (no execution), and validates the historical first 320
feature values before using any complete-opcode representation.

Run from repository root with CPython 3.13 and installed dependencies:
 python research/rq1/run_validation.py --output-dir research/experiments/rq1_validation_001

Outputs are immutable; always supply a NEW directory. The original RQ1
results and historical classifier are never overwritten.
"""
from __future__ import annotations

import argparse
import ast
import copy
import dis
import hashlib
import json
import platform
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction import FeatureHasher
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from run_nested_cv import (
    AST_NODE_NAMES, CLASSES, DEFAULT_TEST, DEFAULT_TRAIN,
    RESEARCH_ROOT, assert_partition, file_digest, load_dataset,
    metrics, paired_task_bootstrap, task_id,
)

SCRIPT_DIR = RESEARCH_ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from bytecode_utils import extract_script_bytecode  # noqa: E402

VARIANTS = (
    "ast_original",       # Replicates original AST baseline
    "ast_no_length",      # Counts without explicit total or source lines
    "ast_core_count",     # Docstrings removed; no total nodes or source lines
    "ast_core_prop",      # Docstrings removed, normalized AST node frequencies
    "length_only",        # Potential length/docstring confound control
    "opcode_full",        # Frequencies over ALL opcodes, not 320-position prefix
    "opcode_ngram",       # Stable-hashed opcode bigrams over ALL instructions
)
DEFAULT_VARIANTS = VARIANTS


def source_path(root: Path, filename: str, model: str, split: str) -> Path:
    folder = "outputs" if split == "train" else "test_data/outputs"
    return root / folder / model / "cleaned" / filename


def strip_docstrings(tree: ast.AST) -> ast.AST:
    """Remove *only* actual module/class/function docstring statements."""
    tree = copy.deepcopy(tree)

    class Strip(ast.NodeTransformer):
        def remove(self, node):
            self.generic_visit(node)
            body = getattr(node, "body", None)
            if isinstance(body, list) and body:
                first = body[0]
                if (isinstance(first, ast.Expr)
                        and isinstance(first.value, ast.Constant)
                        and isinstance(first.value.value, str)):
                    body.pop(0)
                    if not body and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        body.append(ast.Pass())
            return node

        def visit_Module(self, node): return self.remove(node)
        def visit_FunctionDef(self, node): return self.remove(node)
        def visit_AsyncFunctionDef(self, node): return self.remove(node)
        def visit_ClassDef(self, node): return self.remove(node)

    return Strip().visit(tree)


def count_docstrings(tree: ast.AST) -> int:
    result = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        body = getattr(node, "body", [])
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            result += 1
    return result


def ast_vectors(source: str) -> dict[str, dict[str, float]]:
    tree = ast.parse(source)
    no_docs = strip_docstrings(tree)
    full = Counter(type(node).__name__ for node in ast.walk(tree))
    clean = Counter(type(node).__name__ for node in ast.walk(no_docs))
    original = {f"ast_{name}": float(full.get(name, 0)) for name in AST_NODE_NAMES}
    original.update(ast_total_nodes=float(sum(full.values())),
                    ast_source_lines=float(len(source.splitlines())))
    no_length = {f"ast_{name}": float(full.get(name, 0)) for name in AST_NODE_NAMES}
    core_count = {f"ast_{name}": float(clean.get(name, 0)) for name in AST_NODE_NAMES}
    total = max(float(sum(core_count.values())), 1.0)
    core_prop = {key: value / total for key, value in core_count.items()}
    length_only = {
        "ast_source_lines": float(len(source.splitlines())),
        "ast_total_nodes": float(sum(full.values())),
        "ast_docstring_count": float(count_docstrings(tree)),
        "ast_docstring_characters": float(sum(
            len(node.body[0].value.value)
            for node in ast.walk(tree)
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and getattr(node, "body", [])
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        )),
    }
    return {
        "ast_original": original, "ast_no_length": no_length,
        "ast_core_count": core_count, "ast_core_prop": core_prop,
        "length_only": length_only,
    }


def opcode_features(values: list[int], *, ngram_buckets: int) -> dict[str, dict[str, float]]:
    if len(values) % 2:
        raise ValueError("Odd opcode/argument trace length")
    opcode = np.asarray(values[::2], dtype=np.int64)
    if len(opcode) == 0 or (opcode < 0).any() or (opcode > 255).any():
        raise ValueError("Invalid opcode trace")
    hist = np.bincount(opcode, minlength=256).astype(float)
    hist /= float(len(opcode))
    pairs = Counter(f"op2_{a}_{b}" for a, b in zip(opcode[:-1], opcode[1:]))
    # FeatureHasher is stateless: no test-fold vocabulary peeking.
    hasher = FeatureHasher(n_features=ngram_buckets, input_type="dict", alternate_sign=False)
    matrix = hasher.transform([pairs]).toarray()[0].astype(float)
    if len(opcode) > 1:
        matrix /= float(len(opcode) - 1)
    return {
        "opcode_full": {f"op_{j}": float(v) for j, v in enumerate(hist)},
        "opcode_ngram": {f"op2_hash_{j}": float(v) for j, v in enumerate(matrix)},
    }


def build_validation_features(
    df: pd.DataFrame, columns: list[str], root: Path,
    variants: tuple[str, ...], *, ngram_buckets: int,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    if platform.python_version_tuple()[:2] != ("3", "13"):
        raise RuntimeError(
            "This dataset's historical opcode values require CPython 3.13; "
            f"running {platform.python_version()}"
        )
    rows = {name: [] for name in variants}
    audit = []
    seen_meta = {}
    for index, (filename, model, split) in enumerate(
        df[["file_name", "model", "_historical_split"]].itertuples(index=False, name=None)
    ):
        file = source_path(root, filename, model, split)
        if not file.is_file():
            raise FileNotFoundError(f"Missing source: {file}")
        source = file.read_text(encoding="utf-8")
        task = task_id(filename)
        if task not in seen_meta:
            meta_dir = "prompts" if split == "train" else "test_data/prompts"
            meta = root / meta_dir / task / "meta.json"
            if not meta.is_file():
                raise FileNotFoundError(f"Missing metadata for {task}: {meta}")
            seen_meta[task] = json.loads(meta.read_text(encoding="utf-8"))["function_name"]
        byte_values, _ = extract_script_bytecode(file, seen_meta[task])
        historical = df.loc[index, columns].to_numpy(dtype=np.int64)
        padded = (byte_values[:len(columns)]
                  + [-1] * max(0, len(columns) - len(byte_values)))
        if not np.array_equal(np.asarray(padded, dtype=np.int64), historical):
            raise AssertionError(
                f"Bytecode historical feature mismatch at {filename}; "
                "check interpreter version and feature provenance"
            )
        ast_data = ast_vectors(source) if any(x.startswith("ast_") or x == "length_only" for x in variants) else {}
        opcode_data = opcode_features(byte_values, ngram_buckets=ngram_buckets) if any(x.startswith("opcode_") for x in variants) else {}
        for name in variants:
            rows[name].append((ast_data | opcode_data)[name])
        audit.append({
            "row_id": int(index), "file_name": filename, "model": model,
            "task": task, "historical_split": split,
            "source_sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
            "full_opcode_count": int(len(byte_values) // 2),
            "first_320_exact_match": True,
            "source_lines": int(len(source.splitlines())),
            "docstring_count": int(count_docstrings(ast.parse(source))),
        })
        if (index + 1) % 200 == 0:
            print(f"Validated sources: {index + 1}/{len(df)}", flush=True)
    return ({k: pd.DataFrame(v, dtype=float) for k, v in rows.items()},
            pd.DataFrame(audit))


def correctness_coverage(df: pd.DataFrame, scores_dir: Path) -> tuple[pd.DataFrame, dict]:
    """Join existing score files by exact file name; never assume missing=incorrect."""
    paths = sorted(scores_dir.glob("scores_*.csv")) if scores_dir.exists() else []
    records = []
    for path in paths:
        data = pd.read_csv(path)
        required = {"file", "model", "score", "passed", "total", "status"}
        if not required.issubset(data.columns):
            raise ValueError(f"Incorrect score schema in {path}")
        records.append(data[list(sorted(required))])
    if records:
        source = pd.concat(records, ignore_index=True)
        if source["file"].duplicated().any():
            raise ValueError("Duplicate correctness scores for a filename")
        merged = df[["file_name", "model", "_task"]].merge(
            source, how="left", left_on="file_name", right_on="file",
            validate="one_to_one",
        )
        known = merged["file"].notna()
        if (merged.loc[known, "model_x"] != merged.loc[known, "model_y"]).any():
            raise ValueError("Correctness-score model differs from filename model")
    else:
        merged = df[["file_name", "model", "_task"]].copy()
        for key in ("file", "score", "passed", "total", "status"):
            merged[key] = np.nan
        merged["model_x"] = merged["model"]
        merged["model_y"] = np.nan
    merged = merged.rename(columns={"model_x": "generating_model", "_task": "task"})
    evaluated = merged["status"].eq("ok") & merged["total"].gt(0)
    merged["correctness_label"] = np.select(
        [evaluated & merged["passed"].eq(merged["total"]),
         evaluated & merged["passed"].lt(merged["total"])],
        ["all_pass", "not_all_pass"], default="unknown",
    )
    by_model = (
        merged.groupby("generating_model")["correctness_label"]
        .value_counts().unstack(fill_value=0).to_dict(orient="index")
    )
    coverage = {
        "score_sources": [str(path) for path in paths],
        "rows_total": len(df),
        "rows_with_known_correctness": int(evaluated.sum()),
        "rows_unknown": int((~evaluated).sum()),
        "by_model": by_model,
        "warning": "Archival scores may cover only training tasks. Missing is UNKNOWN, not incorrect.",
    }
    return merged[[
        "file_name", "generating_model", "task", "score",
        "passed", "total", "status", "correctness_label",
    ]], coverage


def estimator(seed: int):
    return Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2500, random_state=seed)),
    ]), {"clf__C": [0.1, 1.0, 10.0]}


def evaluate_variants(
    df: pd.DataFrame, representations: dict[str, pd.DataFrame],
    *, seeds: tuple[int, ...], outer_folds: int, inner_folds: int, jobs: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    labels = df["model"].to_numpy()
    groups = df["_task"].to_numpy()
    coded = np.array([CLASSES.index(label) for label in labels], dtype=np.int64)
    records, folds, partitions = [], [], []
    n = len(df)
    for seed in seeds:
        outer = StratifiedGroupKFold(n_splits=outer_folds, shuffle=True, random_state=seed)
        for fold, (train, test) in enumerate(outer.split(np.zeros(n), coded, groups), 1):
            assert_partition(train, test, groups)
            inner = StratifiedGroupKFold(
                n_splits=inner_folds, shuffle=True, random_state=seed + 10000 + fold
            )
            cv = list(inner.split(np.zeros(len(train)), coded[train], groups[train]))
            for itrain, ival in cv:
                assert_partition(itrain, ival, groups[train])
            partitions.append({
                "seed": seed, "fold": fold, "train_tasks": sorted(set(groups[train])),
                "test_tasks": sorted(set(groups[test])),
            })
            for name, dataframe in representations.items():
                X = dataframe.to_numpy(dtype=float)
                base, grid = estimator(seed)
                search = GridSearchCV(
                    base, grid, scoring="f1_macro", cv=cv, n_jobs=jobs,
                    refit=True, error_score="raise",
                )
                search.fit(X[train], coded[train])
                predictions = search.best_estimator_.predict(X[test]).astype(int)
                truth = labels[test]
                predicted = np.asarray(CLASSES)[predictions]
                folds.append({
                    "seed": seed, "fold": fold, "variant": name,
                    "inner_macro_f1": float(search.best_score_),
                    "parameters": json.dumps(search.best_params_, sort_keys=True),
                    "n_test": len(test), "test_tasks": len(set(groups[test])),
                    **metrics(truth, predicted),
                })
                for row_id, pred in zip(test, predicted):
                    records.append({
                        "seed": seed, "fold": fold, "row_id": int(row_id),
                        "task": groups[row_id], "file_name": df.iloc[row_id]["file_name"],
                        "truth": labels[row_id], "variant": name,
                        "prediction": pred,
                    })
        print(f"Completed seed {seed}", flush=True)
    predicted_df = pd.DataFrame(records)
    expected_rows = n * len(seeds)
    for name, subset in predicted_df.groupby("variant"):
        if len(subset) != expected_rows or subset.duplicated(["seed", "row_id"]).any():
            raise AssertionError(f"Missing or repeated held-out rows in {name}")
    return predicted_df, pd.DataFrame(folds), pd.DataFrame(partitions)


def summarize(
    predictions: pd.DataFrame, baseline: str, seeds: tuple[int, ...],
    *, bootstrap_draws: int, bootstrap_seed: int,
) -> dict:
    results = {}
    for variant, group in predictions.groupby("variant"):
        by_seed = {}
        for seed, frame in group.groupby("seed"):
            by_seed[str(seed)] = metrics(frame["truth"], frame["prediction"])
        results[variant] = {
            "seed_metrics": by_seed,
            "accuracy_mean_across_seeds": float(np.mean(
                [row["accuracy"] for row in by_seed.values()]
            )),
            "accuracy_min_across_seeds": float(np.min(
                [row["accuracy"] for row in by_seed.values()]
            )),
            "accuracy_max_across_seeds": float(np.max(
                [row["accuracy"] for row in by_seed.values()]
            )),
        }
    if baseline not in results:
        raise ValueError("The comparison baseline is not in selected variants")
    paired = {}
    for seed in seeds:
        base = predictions.loc[
            (predictions["seed"] == seed) & (predictions["variant"] == baseline)
        ]
        for variant in results:
            if variant == baseline:
                continue
            challenger = predictions.loc[
                (predictions["seed"] == seed) & (predictions["variant"] == variant)
            ]
            paired[f"seed_{seed}/{variant}_minus_{baseline}"] = paired_task_bootstrap(
                challenger, base, draws=bootstrap_draws, seed=bootstrap_seed + seed,
            )
    return {"variants": results, "paired_task_bootstraps_by_seed": paired,
            "note": "Bootstrap over tasks within each seed; repeated partitions are not independent datasets."}



def correctness_subgroup_diagnostics(
    predictions: pd.DataFrame, correctness: pd.DataFrame
) -> dict:
    """Descriptive OOF metrics only for records with independently known scores.

    No claims are made about rows lacking score files, and no classifier is
    retrained on this subset. A fully controlled correctness-stratified
    validation would require complete scores for all 50 tasks.
    """
    fields = correctness[["file_name", "correctness_label"]]
    joined = predictions.merge(fields, on="file_name", how="left", validate="many_to_one")
    report = {}
    for seed, part in joined.groupby("seed"):
        report[str(seed)] = {}
        for label in ("all_pass", "not_all_pass"):
            selected = part[part["correctness_label"] == label]
            unique_rows = selected.drop_duplicates("row_id")
            details = {
                "n": int(len(unique_rows)),
                "n_tasks": int(unique_rows["task"].nunique()),
                "n_by_true_class": unique_rows["truth"].value_counts().to_dict(),
                "coverage_of_full_dataset": float(
                    len(unique_rows) / max(part["row_id"].nunique(), 1)
                ),
            }
            if len(selected) and selected["truth"].nunique() == len(CLASSES):
                for name, subset in selected.groupby("variant"):
                    details[name] = metrics(subset["truth"], subset["prediction"])
            report[str(seed)][label] = details
    return {
        "by_seed_and_correctness": report,
        "warning": "Observational subgroup analysis on SCORED records only; "
                   "missing correctness is unknown. Neither balanced across "
                   "task/model nor necessarily representative of the full dataset.",
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    parser.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    parser.add_argument("--scores-dir", type=Path, default=RESEARCH_ROOT / "evaluation/scores")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--variants", nargs="+", choices=VARIANTS, default=list(DEFAULT_VARIANTS))
    parser.add_argument("--seeds", nargs="+", type=int, default=[7, 42, 101])
    parser.add_argument("--outer-folds", type=int, default=5)
    parser.add_argument("--inner-folds", type=int, default=4)
    parser.add_argument("--bootstrap-draws", type=int, default=1000)
    parser.add_argument("--ngram-buckets", type=int, default=256)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--prepare-only", action="store_true",
                        help="Extract and audit representations, but skip classifier evaluation.")
    return parser.parse_args(argv)


def main(args=None):
    args = parse_args() if args is None else args
    variants = tuple(dict.fromkeys(args.variants))
    seeds = tuple(dict.fromkeys(args.seeds))
    if not seeds or len(seeds) != len(args.seeds):
        raise ValueError("Seeds must be present and unique")
    if not variants or args.ngram_buckets < 8:
        raise ValueError("No variants or too few hash buckets")
    if args.outer_folds < 2 or args.inner_folds < 2 or args.bootstrap_draws < 1:
        raise ValueError("Folds >=2 and bootstrap draws >=1 required")

    df, cols = load_dataset(args.train_csv, args.test_csv)
    incorrect_names = df.loc[
        ~df.apply(lambda row: row["file_name"].endswith("_" + row["model"] + ".py"), axis=1),
        "file_name",
    ]
    if not incorrect_names.empty:
        raise ValueError(
            "Filename suffix and model label disagree: "
            + ", ".join(incorrect_names.head(5).tolist())
        )
    features, inventory = build_validation_features(
        df, cols, args.research_root, variants, ngram_buckets=args.ngram_buckets
    )
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing to overwrite: {args.output_dir}")
    args.output_dir.mkdir(parents=True)
    inventory.to_csv(args.output_dir / "source_audit.csv", index=False)
    scores, coverage = correctness_coverage(df, args.scores_dir)
    scores.to_csv(args.output_dir / "correctness_coverage.csv", index=False)
    (args.output_dir / "correctness_summary.json").write_text(
        json.dumps(coverage, indent=2) + "\n", encoding="utf-8"
    )
    manifest = {
        "experiment": "rq1_validation_v1",
        "seeds": list(seeds), "outer_folds": args.outer_folds,
        "inner_folds": args.inner_folds, "bootstrap_draws": args.bootstrap_draws,
        "variants": list(variants),
        "ngrams": "complete_opcode_bigrams_stable_hashed",
        "ngram_buckets": args.ngram_buckets,
        "classifier": "logistic_regression",
        "tuning": "inner_task_grouped_macro_f1",
        "task_partition": "stratified_groupkfold_shuffled_by_seed",
        "n": int(len(df)), "n_tasks": int(df["_task"].nunique()),
        "python": platform.python_version(),
        "numpy": np.__version__, "pandas": pd.__version__,
        "sklearn": __import__("sklearn").__version__,
        "train_sha256": file_digest(args.train_csv),
        "test_sha256": file_digest(args.test_csv),
        "source_audit_sha256": file_digest(args.output_dir / "source_audit.csv"),
        "correctness_score_coverage": int(coverage["rows_with_known_correctness"]),
        "prepare_only": bool(args.prepare_only),
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if args.prepare_only:
        print(f"Prepared {len(df)} verified programs; report: {args.output_dir}")
        return
    prediction, folds, partition = evaluate_variants(
        df, features, seeds=seeds, outer_folds=args.outer_folds,
        inner_folds=args.inner_folds, jobs=args.jobs,
    )
    prediction.to_csv(args.output_dir / "oof_predictions.csv", index=False)
    correctness_diagnostics = correctness_subgroup_diagnostics(prediction, scores)
    (args.output_dir / "correctness_oof_diagnostics.json").write_text(
        json.dumps(correctness_diagnostics, indent=2) + "\n"
    )
    folds.to_csv(args.output_dir / "fold_scores.csv", index=False)
    partition.to_json(args.output_dir / "task_partitions.json", orient="records", indent=2)
    report = summarize(
        prediction, "ast_original" if "ast_original" in variants else variants[0],
        seeds, bootstrap_draws=args.bootstrap_draws, bootstrap_seed=42,
    )
    (args.output_dir / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["variants"], indent=2))
    print(f"Saved RQ1 validation outputs to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
