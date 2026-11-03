"""
task_bytecode_summary.py

Two analyses, tied together for a per-task / per-model performance writeup:

1. Source code length distribution per task (lines of code, across all
   prompts/runs/models for that task) -- to characterize task complexity.

2. Cross-model bytecode collisions: for each (task, prompt, run), checks
   whether two or more models produced byte-identical feature vectors
   (byte_0..byte_319), which would make them indistinguishable to the
   classifier by construction.

Run from the project root:
    python scripts/task_bytecode_summary.py
"""

from pathlib import Path
from itertools import combinations

import numpy as np
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
ANALYSIS_DIR = BASE_DIR / "analysis"
TASKS = ["t41","t42","t43","t44","t45","t46","t47","t48","t49","t50"]
CLASS_NAMES = ["llama", "mistral", "qwen"]


def get_source_path(stem, model):
    return BASE_DIR / "test_data" / "outputs" / model / "cleaned" / f"{stem}.py"


def count_lines(py_path):
    if not py_path.exists():
        return None
    text = py_path.read_text(encoding="utf-8")
    # count non-empty, non-comment-only lines
    lines = [l for l in text.splitlines()
             if l.strip() and not l.strip().startswith("#")]
    return len(lines)


# ══════════════════════════════════════════════════════════════════════════════
# 1. source code length per task
# ══════════════════════════════════════════════════════════════════════════════

def source_length_analysis(df):
    rows = []
    for _, rec in df.iterrows():
        stem = Path(rec["file_name"]).stem
        model = rec["model"]
        task = stem.split("_")[0]
        if task not in TASKS:
            continue
        py_path = get_source_path(stem, model)
        if not py_path.exists():
            print(f"MISSING: {py_path}")
        n_lines = count_lines(py_path)
        if n_lines is None:
            continue
        rows.append({"task": task, "model": model, "file": stem, "lines": n_lines})

    print(f"rows collected: {len(rows)}")
    if rows:
        print("first row:", rows[0])

    out = pd.DataFrame(rows)
    if out.empty:
        print("ERROR: no rows collected -- check file_name format and source paths")
        return out, pd.DataFrame()

    summary = out.groupby("task")["lines"].agg(["mean", "std", "min", "max", "count"])
    summary = summary.sort_values("mean", ascending=False)

    print("=" * 70)
    print("SOURCE CODE LENGTH PER TASK (non-empty, non-comment-only lines)")
    print("=" * 70)
    print(summary.round(1))
    print()

    # per-task, per-model breakdown
    per_model = out.groupby(["task", "model"])["lines"].mean().unstack()
    print("Mean lines per task x model:")
    print(per_model.round(1))
    print()

    out_file = ANALYSIS_DIR / "source_length_by_task.csv"
    out.to_csv(out_file, index=False)
    print(f"Saved per-file data to {out_file}\n")

    return out, summary


# ══════════════════════════════════════════════════════════════════════════════
# 2. cross-model bytecode collisions
# ══════════════════════════════════════════════════════════════════════════════

def bytecode_collision_analysis(df):
    byte_cols = [c for c in df.columns if c.startswith("byte_")]

    collisions = []
    df = df.copy()
    parts = df["file_name"].str.split("_", expand=True)
    df["task"]   = parts[0]
    df["prompt"] = parts[1]
    df["run"]    = parts[2]

    for (task, prompt), group in df.groupby(["task", "prompt"]):
        if len(group) < 2:
            continue
        for (i1, r1), (i2, r2) in combinations(group.iterrows(), 2):
            # skip same-file comparisons (shouldn't happen, but just in case)
            if r1["file_name"] == r2["file_name"]:
                continue
            vec1 = r1[byte_cols].values.astype(int)
            vec2 = r2[byte_cols].values.astype(int)
            if np.array_equal(vec1, vec2):
                collisions.append({
                    "task": task, "prompt": prompt,
                    "model_a": r1["model"], "run_a": r1["run"], "file_a": r1["file_name"],
                    "model_b": r2["model"], "run_b": r2["run"], "file_b": r2["file_name"],
                    "same_model": r1["model"] == r2["model"],
                })

    out = pd.DataFrame(collisions)
    print("=" * 70)
    print("BYTECODE COLLISIONS (identical byte_0..byte_319), within each (task, prompt)")
    print("=" * 70)
    if out.empty:
        print("No collisions found.\n")
    else:
        print(out.to_string(index=False))
        print(f"\nn={len(out)} collisions")
        print("\nBy task:")
        print(out.groupby("task").size())
        print("\nCross-model only (excluding same-model run pairs):")
        cross = out[~out["same_model"]]
        print(f"n={len(cross)}")
        if not cross.empty:
            cross = cross.copy()
            cross["pair"] = cross.apply(lambda r: tuple(sorted([r["model_a"], r["model_b"]])), axis=1)
            print(cross.groupby("pair").size())

        out_file = ANALYSIS_DIR / "bytecode_collisions.csv"
        out.to_csv(out_file, index=False)
        print(f"\nSaved to {out_file}\n")

    return out


# ══════════════════════════════════════════════════════════════════════════════
# 3. tie together with per-task / per-model accuracy
# ══════════════════════════════════════════════════════════════════════════════

def accuracy_per_task_model():
    rows = []
    for task in TASKS:
        summary_path = ANALYSIS_DIR / task / f"{task}_summary.csv"
        if not summary_path.exists():
            continue
        summary = pd.read_csv(summary_path)
        for model in CLASS_NAMES:
            msub = summary[summary["true"] == model]
            if msub.empty:
                continue
            rows.append({
                "task": task, "model": model,
                "n": len(msub), "correct": msub["correct"].sum(),
                "accuracy": msub["correct"].mean(),
            })
    out = pd.DataFrame(rows)
    pivot = out.pivot(index="task", columns="model", values="accuracy")
    print("=" * 70)
    print("ACCURACY PER TASK x MODEL")
    print("=" * 70)
    print((pivot * 100).round(1))
    print()
    return out, pivot


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    df = pd.read_csv(TEST_FEATURES_CSV)

    src_df, src_summary = source_length_analysis(df)
    collisions = bytecode_collision_analysis(df)
    acc_df, acc_pivot = accuracy_per_task_model()

    # ── tie together: merge source length (per task, mean) with accuracy ──
    src_by_task = src_df.groupby("task")["lines"].mean().rename("mean_lines")
    overall_acc = acc_df.groupby("task")["correct"].sum() / acc_df.groupby("task")["n"].sum()
    overall_acc = overall_acc.rename("overall_accuracy")

    combined = pd.concat([src_by_task, overall_acc], axis=1)

    if not collisions.empty:
        n_collisions_per_task = collisions.groupby("task").size().rename("n_collisions")
        combined = combined.join(n_collisions_per_task, how="left")
        combined["n_collisions"] = combined["n_collisions"].fillna(0).astype(int)
    else:
        combined["n_collisions"] = 0

    combined = combined.sort_values("overall_accuracy")

    print("=" * 70)
    print("COMBINED: mean source length, overall accuracy, bytecode collisions per task")
    print("=" * 70)
    print(combined.round(3))

    out_file = ANALYSIS_DIR / "task_summary_combined.csv"
    combined.to_csv(out_file)
    print(f"\nSaved to {out_file}")


if __name__ == "__main__":
    main()
