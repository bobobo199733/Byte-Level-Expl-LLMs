"""Full 1,316-program task-test correctness audit, using only isolated Apptainer.

Includes valid_cases, explicit_cases, invalid_cases. "Pass" means passing
all provided task examples; it never implies correctness on all possible inputs.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "rq1"))
from run_nested_cv import DEFAULT_TEST, DEFAULT_TRAIN, RESEARCH_ROOT, load_dataset  # noqa: E402
from run_validation import source_path  # noqa: E402
from validation_common import digest, run_in_sandbox, verify_sandbox  # noqa: E402


def evaluate(args):
    if platform.python_version_tuple()[:2] != ("3", "13"):
        raise RuntimeError("CPython 3.13 host required")
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing to overwrite: {args.output_dir}")
    verify_sandbox(args.sandbox_image)
    df, _ = load_dataset(args.train_csv, args.test_csv)
    rows = []
    try:
        for j, row in df.iterrows():
            split = row["_historical_split"]
            meta = args.research_root / (
                "prompts" if split == "train" else "test_data/prompts"
            ) / row["_task"] / "meta.json"
            source = source_path(args.research_root, row["file_name"], row["model"], split)
            if not meta.is_file() or not source.is_file():
                raise FileNotFoundError(f"Missing source/meta {source} {meta}")
            verdict = run_in_sandbox(args.sandbox_image, source, meta, timeout=args.timeout)
            status = ("pass" if verdict.get("ok") and verdict.get("all_pass")
                      else "fail" if verdict.get("ok") else "untestable")
            item = {
                "row_id": int(j), "task": row["_task"], "model": row["model"],
                "file_name": row["file_name"], "status": status,
                "n_cases": verdict.get("n_cases"),
                "n_pass": verdict.get("n_pass"), "n_failed": verdict.get("n_failed"),
                "valid_cases": verdict.get("by_category", {}).get("valid_cases", {}).get("n"),
                "valid_passed": verdict.get("by_category", {}).get("valid_cases", {}).get("passed"),
                "explicit_cases": verdict.get("by_category", {}).get("explicit_cases", {}).get("n"),
                "explicit_passed": verdict.get("by_category", {}).get("explicit_cases", {}).get("passed"),
                "invalid_cases": verdict.get("by_category", {}).get("invalid_cases", {}).get("n"),
                "invalid_passed": verdict.get("by_category", {}).get("invalid_cases", {}).get("passed"),
                "error_type": verdict.get("error_type", ""),
                "error": verdict.get("error", ""),
                "source_sha256": digest(source),
                "metadata_sha256": digest(meta),
            }
            rows.append(item)
            if (j + 1) % 50 == 0:
                print(f"Audited {j+1}/{len(df)} programs", flush=True)
    except BaseException:
        # Fail-closed: preserve progress to a separate named incomplete folder.
        partial = args.output_dir.with_name(args.output_dir.name + "_incomplete")
        if not partial.exists():
            partial.mkdir(parents=True)
            pd.DataFrame(rows).to_csv(partial / "progress.csv", index=False)
        raise
    if len(rows) != len(df) or len({r["row_id"] for r in rows}) != len(df):
        raise AssertionError("Not all retained programs audited exactly once")
    data = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True)
    data.to_csv(args.output_dir / "correctness_results.csv", index=False)
    summary = {
        "n_programs": len(rows),
        "status_counts": dict(Counter(data["status"])),
        "per_model": data.groupby(["model", "status"]).size().unstack(fill_value=0).to_dict("index"),
        "per_task": data.groupby(["task", "status"]).size().unstack(fill_value=0).to_dict("index"),
        "total_task_cases_evaluated": int(data["n_cases"].fillna(0).sum()),
        "limitations": [
            "Task-test correctness only; not formal correctness over arbitrary inputs.",
            "Untestable includes sandbox errors and execution timeouts, not presumed incorrect.",
            "Original metadata includes valid_cases, explicit_cases, invalid_cases.",
            "All 1316 retained files, not discarded generations, are included.",
        ],
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.output_dir / "manifest.json").write_text(json.dumps({
        "python": platform.python_version(),
        "sandbox_image_sha256": digest(args.sandbox_image),
        "sandbox_worker_sha256": digest(Path(__file__).with_name("sandbox_validation_worker.py")),
        "train_csv_sha256": digest(args.train_csv),
        "test_csv_sha256": digest(args.test_csv),
        "timeout": args.timeout,
    }, indent=2) + "\n")
    print(json.dumps({k: v for k,v in summary.items() if k != "per_task"}, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    p.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    p.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    p.add_argument("--sandbox-image", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--timeout", type=int, default=20)
    evaluate(p.parse_args())


if __name__ == "__main__":
    main()
