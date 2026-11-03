"""
function_count_check.py

For each file (t1-t50), counts top-level ast.FunctionDef nodes.
Reports mean function count and fraction of multi-function files per
model per task, separately for train (t1-t40) and test (t41-t50).

Run from project root:
    python scripts/function_count_check.py
"""

import ast
from pathlib import Path

import pandas as pd
import numpy as np

BASE_DIR               = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV      = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
TRAIN_FEATURES_CSV     = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_OUTPUTS_DIR       = BASE_DIR / "test_data" / "outputs"
TRAIN_OUTPUTS_DIR      = BASE_DIR / "outputs"

TRAIN_TASKS = [f"t{i}" for i in range(1, 41)]
TEST_TASKS  = [f"t{i}" for i in range(41, 51)]
MODELS      = ["llama", "mistral", "qwen"]
HIGHLIGHT   = {"t42", "t46", "t47", "t49", "t50"}


def count_top_level_functions(py_path: Path) -> int | None:
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
        return sum(1 for node in ast.iter_child_nodes(tree)
                   if isinstance(node, ast.FunctionDef))
    except Exception:
        return None


def get_source_path(stem: str, model: str, outputs_dir: Path) -> Path:
    return outputs_dir / model / "cleaned" / f"{stem}.py"


def build_dataset(features_csv: Path, outputs_dir: Path, tasks: list[str]) -> pd.DataFrame:
    df = pd.read_csv(features_csv)
    parts      = df["file_name"].str.split("_", expand=True)
    df["task"] = parts[0]
    df["stem"] = df["file_name"].str.replace(".py", "", regex=False)
    df = df[df["task"].isin(tasks)]

    rows = []
    for _, rec in df.iterrows():
        stem    = rec["stem"]
        model   = rec["model"]
        task    = rec["task"]
        py_path = get_source_path(stem, model, outputs_dir)
        n_fns   = count_top_level_functions(py_path)
        n_nest  = count_nested_functions(py_path)
        if n_fns is None or n_nest is None:
            continue
        rows.append({
            "task": task, "model": model, "stem": stem,
            "n_functions": n_fns, "n_nested": n_nest,
        })

    return pd.DataFrame(rows)


def count_nested_functions(py_path: Path) -> int | None:
    """Count FunctionDef/AsyncFunctionDef nodes nested inside the
    top-level function bodies (not module-level)."""
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    # get top-level function nodes
    top_level = [node for node in ast.iter_child_nodes(tree)
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]

    nested = 0
    for fn in top_level:
        for node in ast.walk(fn):
            # skip the top-level function itself
            if node is fn:
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nested += 1

    return nested


def print_summary(data: pd.DataFrame, tasks: list[str], label: str):
    data = data.copy()
    data["multi_fn"] = data["n_functions"] > 1

    print()
    print("=" * 65)
    print(f"{label}")
    print("=" * 65)

    # mean functions per model per task
    mean_pivot  = data.groupby(["task","model"])["n_functions"].mean().unstack()[MODELS].round(2)
    multi_pivot = data.groupby(["task","model"])["multi_fn"].mean().unstack()[MODELS]

    print(f"\n  {'task':6s}  {'llama(mean/multi%)':22s}  "
          f"{'mistral(mean/multi%)':22s}  {'qwen(mean/multi%)':22s}")
    print(f"  {'-'*6}  {'-'*22}  {'-'*22}  {'-'*22}")

    for task in tasks:
        if task not in mean_pivot.index:
            continue
        marker = "★" if task in HIGHLIGHT else " "
        parts_str = []
        for model in MODELS:
            mn  = mean_pivot.loc[task, model]
            mp  = multi_pivot.loc[task, model]
            parts_str.append(f"{mn:.2f} / {mp:.0%}")
        print(f"  {task}{marker}  {parts_str[0]:22s}  {parts_str[1]:22s}  {parts_str[2]:22s}")


    # overall per model
    print(f"\n  Overall (all {label.split()[0].lower()} tasks):")
    overall = data.groupby("model")["multi_fn"].agg(["mean","sum","count"])
    for model in MODELS:
        row = overall.loc[model]
        print(f"    {model:8s}: {row['sum']:.0f}/{row['count']:.0f} "
              f"({row['mean']:.1%}) files have >1 function")

    # distribution
    print(f"\n  Function count distribution:")
    for model in MODELS:
        counts = data[data["model"]==model]["n_functions"].value_counts().sort_index()
        print(f"    {model:8s}: {dict(counts)}")

def print_nested_summary(data: pd.DataFrame, tasks: list[str], label: str):
    data = data.copy()
    data["has_nested"] = data["n_nested"] > 0

    print()
    print("=" * 65)
    print(f"NESTED FUNCTIONS -- {label}")
    print("=" * 65)

    mean_pivot  = data.groupby(["task","model"])["n_nested"].mean().unstack()
    frac_pivot  = data.groupby(["task","model"])["has_nested"].mean().unstack()

    # fill missing model columns
    for col in MODELS:
        if col not in mean_pivot.columns:
            mean_pivot[col]  = np.nan
        if col not in frac_pivot.columns:
            frac_pivot[col]  = np.nan

    mean_pivot  = mean_pivot[MODELS].round(2)
    frac_pivot  = frac_pivot[MODELS]

    print(f"\n  1. Mean nested functions per model per task")
    print(f"  {'task':6s}  {'llama':8s}  {'mistral':8s}  {'qwen':8s}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*8}")
    for task in tasks:
        if task not in mean_pivot.index:
            continue
        marker = "★" if task in HIGHLIGHT else " "
        row = mean_pivot.loc[task]
        print(f"  {task}{marker}  {row['llama']:8.2f}  "
              f"{row['mistral']:8.2f}  {row['qwen']:8.2f}")

    print(f"\n  2. Fraction of files with ≥1 nested function per model per task")
    print(f"  {'task':6s}  {'llama':8s}  {'mistral':8s}  {'qwen':8s}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*8}")
    for task in tasks:
        if task not in frac_pivot.index:
            continue
        marker = "★" if task in HIGHLIGHT else " "
        row = frac_pivot.loc[task]
        print(f"  {task}{marker}  {row['llama']:8.0%}  "
              f"{row['mistral']:8.0%}  {row['qwen']:8.0%}")

    print(f"\n  3. Overall fraction with ≥1 nested function per model")
    overall = data.groupby("model")["has_nested"].agg(["mean","sum","count"])
    for model in MODELS:
        if model not in overall.index:
            continue
        row = overall.loc[model]
        print(f"    {model:8s}: {row['sum']:.0f}/{row['count']:.0f} "
              f"({row['mean']:.1%}) files have ≥1 nested function")

    print(f"\n  Nested function count distribution:")
    for model in MODELS:
        counts = data[data["model"]==model]["n_nested"].value_counts().sort_index()
        print(f"    {model:8s}: {dict(counts)}")

def main():
    print("Loading train data...")
    train_data = build_dataset(TRAIN_FEATURES_CSV, TRAIN_OUTPUTS_DIR, TRAIN_TASKS)
    print(f"  {len(train_data)} files loaded")

    print("Loading test data...")
    test_data = build_dataset(TEST_FEATURES_CSV, TEST_OUTPUTS_DIR, TEST_TASKS)
    print(f"  {len(test_data)} files loaded")

    print_summary(train_data, TRAIN_TASKS, "TRAIN (t1-t40)  mean functions / fraction >1 function")
    print_summary(test_data,  TEST_TASKS,  "TEST  (t41-t50) mean functions / fraction >1 function")
    print_nested_summary(test_data, TEST_TASKS,  "TEST  (t41-t50)")
    print_nested_summary(train_data, TRAIN_TASKS, "TRAIN (t1-t40)")

    # ── direct train vs test comparison per model ─────────────────────────
    print()
    print("=" * 65)
    print("TRAIN vs TEST comparison (overall, per model)")
    print("=" * 65)
    for model in MODELS:
        t_rate = (train_data[train_data["model"]==model]["n_functions"] > 1).mean()
        te_rate = (test_data[test_data["model"]==model]["n_functions"] > 1).mean()
        print(f"  {model:8s}:  train multi-fn={t_rate:.1%}  "
              f"test multi-fn={te_rate:.1%}  "
              f"delta={te_rate-t_rate:+.1%}")


if __name__ == "__main__":
    main()
