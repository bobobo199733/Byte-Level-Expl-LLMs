"""RQ2 controlled AST edits: held-out model/attribution response with sandbox testing.

No generated code is executed on the host. The paired originals and edits
are only executed inside a user-supplied Apptainer Python-3.13 image using
--containall --net --network none. If the sandbox cannot run, FAIL CLOSED.

Tests establish equivalence only on available task cases, NOT all inputs.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RQ2 = Path(__file__).resolve().parent
ROOT = RQ2.parent
for directory in (ROOT / "rq1", ROOT / "scripts", RQ2):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from bytecode_utils import extract_script_bytecode  # noqa: E402
from run_nested_cv import CLASSES, RESEARCH_ROOT, DEFAULT_TRAIN, DEFAULT_TEST, assert_partition, load_dataset  # noqa: E402
from run_validation import build_validation_features, source_path  # noqa: E402
from run_explanations import linear_logit_shap  # noqa: E402


def mutate(source: str, function_name: str, kind: str) -> str:
    tree = ast.parse(source)
    targets = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    ]
    if len(targets) != 1:
        raise ValueError("Expected one top-level target function")
    target = targets[0]
    body = target.body
    at = 1 if (body and isinstance(body[0], ast.Expr)
               and isinstance(body[0].value, ast.Constant)
               and isinstance(body[0].value.value, str)) else 0
    if at == len(body):
        raise ValueError("No executable function body")
    if kind == "insert_pass":
        body.insert(at, ast.Pass())
    elif kind == "wrap_try_finally":
        # No-op finally, but changes compiled control flow. Equivalent
        # behavior is a HYPOTHESIS checked only against task tests.
        body[at:] = [ast.Try(body=body[at:], handlers=[],
                            orelse=[], finalbody=[ast.Pass()])]
    else:
        raise ValueError(f"Unknown transformation: {kind}")
    ast.fix_missing_locations(tree)
    result = ast.unparse(tree) + "\n"
    compile(result, "rq2_edited.py", "exec")  # compilation, not execution
    return result


def normalized_opcode_hist(values: list[int]) -> np.ndarray:
    op = np.asarray(values[::2], dtype=np.int64)
    if len(values) % 2 or len(op) == 0 or np.any((op < 0) | (op > 255)):
        raise ValueError("Invalid extracted opcode trace")
    freq = np.bincount(op, minlength=256).astype(float)
    return freq / len(op)


def isolated_test(
    image: Path, original: str, edited: str, metadata: dict, *,
    timeout: int,
) -> dict:
    if not image.is_file():
        raise FileNotFoundError(f"Isolated sandbox image missing: {image}")
    if timeout <= 0:
        raise ValueError("Sandbox timeout must be positive")
    checker = RQ2 / "sandbox_pair_checker.py"
    with tempfile.TemporaryDirectory(prefix="rq2_pair_") as tmp:
        folder = Path(tmp)
        for name, data in (
            ("original.py", original), ("edited.py", edited),
            ("meta.json", json.dumps(metadata)),
            ("check.py", checker.read_text()),
        ):
            (folder / name).write_text(data, encoding="utf-8")
        cmd = [
            "apptainer", "exec", "--containall", "--cleanenv",
            "--net", "--network", "none", "--no-home",
            "--bind", f"{folder.resolve()}:/work:ro",
            str(image.resolve()), "python3", "/work/check.py",
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"accepted": False, "reason": "timeout"}
        except OSError as exc:
            return {"accepted": False, "reason": "sandbox_launch_error",
                    "detail": str(exc)[:180]}
        try:
            value = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return {"accepted": False, "reason": "sandbox_no_valid_report",
                    "stderr": proc.stderr[-240:]}
        if proc.returncode != 0 or not value.get("accepted"):
            return {"accepted": False, "reason": value.get("reason", "sandbox_failed"),
                    "detail": value.get("message", "")}
        return {"accepted": True, "tests": int(value["tests"])}


def fit_heldout_models(df, X: np.ndarray, *, seed: int, outer: int, inner: int):
    groups = df["_task"].to_numpy()
    y = np.array([CLASSES.index(name) for name in df["model"]], dtype=int)
    splitter = StratifiedGroupKFold(n_splits=outer, shuffle=True, random_state=seed)
    for fold, (train, test) in enumerate(splitter.split(X, y, groups), 1):
        assert_partition(train, test, groups)
        cv = list(StratifiedGroupKFold(
            n_splits=inner, shuffle=True, random_state=seed + 10000 + fold
        ).split(X[train], y[train], groups[train]))
        for a, b in cv:
            assert_partition(a, b, groups[train])
        grid = GridSearchCV(
            Pipeline([("scale", StandardScaler()),
                      ("clf", LogisticRegression(max_iter=2500, random_state=seed))]),
            {"clf__C": [0.1, 1.0, 10.0]},
            scoring="f1_macro", cv=cv, error_score="raise", refit=True, n_jobs=1,
        )
        grid.fit(X[train], y[train])
        yield fold, train, test, grid.best_estimator_


def run(args):
    if platform.python_version_tuple()[:2] != ("3", "13"):
        raise RuntimeError("Use CPython 3.13 for historical opcode agreement")
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing overwrite: {args.output_dir}")
    if not args.sandbox_image.is_file():
        raise FileNotFoundError("A real Apptainer Python image is REQUIRED")
    if args.max_cases < 1 or args.max_per_model < 1:
        raise ValueError("max-cases and max-per-model must be positive")
    df, columns = load_dataset(args.train_csv, args.test_csv)
    feature, audit = build_validation_features(
        df, columns, args.research_root, ("opcode_full",), ngram_buckets=256
    )
    X = feature["opcode_full"].to_numpy(dtype=float)
    # Fixed and deterministic selection: diversify by model then task.
    chosen = set()
    counts = {model: 0 for model in CLASSES}
    for model in CLASSES:
        for task, block in df.loc[df["model"].eq(model)].groupby("_task", sort=True):
            if counts[model] >= args.max_per_model or len(chosen) >= args.max_cases:
                break
            index = int(block.sort_values("file_name").index[0])
            chosen.add(index)
            counts[model] += 1
    if not chosen:
        raise ValueError("No candidates selected")
    output = []
    for fold, train, test, fitted in fit_heldout_models(
        df, X, seed=args.seed, outer=args.outer_folds, inner=args.inner_folds
    ):
        train_mean = X[train].mean(axis=0)
        for index in sorted(chosen.intersection(set(map(int, test)))):
            row = df.iloc[index]
            task = str(row["_task"])
            split = str(row["_historical_split"])
            source = source_path(args.research_root, row["file_name"], row["model"], split)
            meta_file = args.research_root / (
                "prompts" if split == "train" else "test_data/prompts"
            ) / task / "meta.json"
            meta = json.loads(meta_file.read_text())
            original = source.read_text(encoding="utf-8")
            orig_vec = X[index]
            orig_logits = fitted.decision_function(orig_vec.reshape(1, -1))[0]
            orig_prediction = CLASSES[int(np.argmax(orig_logits))]
            orig_attr, _ = linear_logit_shap(fitted, orig_vec[None], train_mean)
            for kind in args.transforms:
                record = {
                    "seed": args.seed, "fold": fold, "task": task,
                    "file_name": row["file_name"], "true_model": row["model"],
                    "original_prediction": orig_prediction, "edit_kind": kind,
                    "source_sha256": hashlib.sha256(original.encode()).hexdigest(),
                    "status": "rejected",
                }
                try:
                    edited = mutate(original, meta["function_name"], kind)
                    with tempfile.TemporaryDirectory(prefix="rq2_extract_") as scratch:
                        path = Path(scratch) / source.name
                        path.write_text(edited)
                        changed, _ = extract_script_bytecode(
                            path, target_function=meta["function_name"]
                        )
                    new_vec = normalized_opcode_hist(changed)
                    diff = float(np.abs(new_vec - orig_vec).sum())
                    record["opcode_hist_l1_change"] = diff
                    record["edited_source_sha256"] = hashlib.sha256(edited.encode()).hexdigest()
                    if diff <= 1e-12:
                        record["reason"] = "no_change_to_opcode_representation"
                        output.append(record)
                        continue
                    verdict = isolated_test(
                        args.sandbox_image, original, edited, meta,
                        timeout=args.timeout,
                    )
                    if not verdict["accepted"]:
                        record["reason"] = verdict["reason"]
                        record["sandbox_detail"] = verdict.get("detail", "")
                        output.append(record)
                        continue
                    new_logits = fitted.decision_function(new_vec[None])[0]
                    new_attr, _ = linear_logit_shap(fitted, new_vec[None], train_mean)
                    expected_delta = (new_attr[0] - orig_attr[0]).sum(axis=0)
                    actual_delta = new_logits - orig_logits
                    residual = float(np.max(np.abs(expected_delta - actual_delta)))
                    if residual > 1e-8:
                        raise AssertionError("Logit change cannot be explained by attribution change")
                    predicted = CLASSES[int(np.argmax(new_logits))]
                    class_index = CLASSES.index(row["model"])
                    top_orig = set(np.argsort(-np.abs(orig_attr[0, :, class_index]))[:10])
                    top_new = set(np.argsort(-np.abs(new_attr[0, :, class_index]))[:10])
                    record.update({
                        "status": "accepted_on_supplied_tests",
                        "tests_passed_each": verdict["tests"],
                        "edited_prediction": predicted,
                        "prediction_flipped": predicted != orig_prediction,
                        "true_class_logit_change": float(actual_delta[class_index]),
                        "max_attribution_delta_residual": residual,
                        "attribution_top10_jaccard": (
                            len(top_orig & top_new) / len(top_orig | top_new)
                        ),
                    })
                except Exception as exc:
                    record["reason"] = type(exc).__name__
                    record["detail"] = str(exc)[:200]
                output.append(record)
        print(f"Finished held-out fold {fold}/{args.outer_folds}", flush=True)
    args.output_dir.mkdir(parents=True)
    pd.DataFrame(output).to_csv(args.output_dir / "interventions.csv", index=False)
    summary = {
        "attempts": len(output),
        "statuses": pd.Series([v["status"] for v in output]).value_counts().to_dict(),
        "accepted": sum(x["status"] == "accepted_on_supplied_tests" for x in output),
        "safety": "No untrusted generated code executed outside Apptainer",
        "limitations": [
            "Functional equivalence supported only on task-provided test cases; it is not a proof for all inputs",
            "Edits may change introspection, errors or behavior outside tested inputs",
            "An opcode frequency shift does not isolate a unique semantic concept",
            "No SHAP claim about LLM internals follows from classifier logit changes",
            "Do not select only prediction-flipping edits for analysis; report rejected and accepted cases",
        ],
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.output_dir / "manifest.json").write_text(json.dumps({
        "seed": args.seed, "outer_folds": args.outer_folds,
        "inner_folds": args.inner_folds, "transforms": args.transforms,
        "sandbox_image_sha256": sha256(args.sandbox_image),
        "python_host": platform.python_version(),
        "max_cases": args.max_cases, "max_per_model": args.max_per_model,
        "historical_feature_audit_rows": len(audit),
    }, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    parser.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    parser.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    parser.add_argument("--sandbox-image", type=Path, required=True,
                        help="Existing Apptainer image running Python 3.13")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outer-folds", type=int, default=5)
    parser.add_argument("--inner-folds", type=int, default=4)
    parser.add_argument("--max-cases", type=int, default=36)
    parser.add_argument("--max-per-model", type=int, default=12)
    parser.add_argument("--transforms", nargs="+",
                        choices=("insert_pass", "wrap_try_finally"),
                        default=["insert_pass", "wrap_try_finally"])
    parser.add_argument("--timeout", type=int, default=12)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
