"""Differential behavioral equivalence follow-up for original RQ2 interventions.

Checks all original task examples and up to 40 deterministic EXTRA probes.
Pair agreement is reported separately from task correctness. All source
is executed in the isolated Apptainer container, never on the host.

The candidate edits are generated afresh using the original AST transform.
No source-level equivalence theorem is claimed; probes can be out of domain.
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
from run_nested_cv import RESEARCH_ROOT, DEFAULT_TRAIN, DEFAULT_TEST, load_dataset  # noqa: E402
from run_validation import source_path  # noqa: E402
from run_source_interventions import mutate  # noqa: E402
from validation_common import digest, run_in_sandbox, verify_sandbox  # noqa: E402

def evaluate(args):
    if platform.python_version_tuple()[:2] != ("3", "13"):
        raise RuntimeError("CPython 3.13 host required")
    if args.output_dir.exists():
        raise FileExistsError(f"Refusing to overwrite: {args.output_dir}")
    verify_sandbox(args.sandbox_image)
    df, _ = load_dataset(args.train_csv, args.test_csv)
    lookup = df.set_index("file_name")
    history = pd.read_csv(args.original_interventions)
    needed = {"file_name", "edit_kind", "status", "prediction_flipped", "attribution_top10_jaccard"}
    if not needed.issubset(history):
        raise ValueError(f"Missing historical columns: {needed-set(history.columns)}")
    if history.duplicated(["file_name", "edit_kind"]).any():
        raise ValueError("Repeated original intervention case")
    results = []
    for j, old in history.iterrows():
        filename = str(old["file_name"])
        if filename not in lookup.index:
            raise ValueError(f"Historical intervention missing in dataset: {filename}")
        row = lookup.loc[filename]
        split = row["_historical_split"]
        source = source_path(args.research_root, filename, row["model"], split)
        meta = args.research_root / (
            "prompts" if split == "train" else "test_data/prompts"
        ) / row["_task"] / "meta.json"
        attempt = {
            "file_name": filename, "task": row["_task"], "true_model": row["model"],
            "edit_kind": str(old["edit_kind"]), "original_intervention_status": old["status"],
            "original_prediction_flipped": old["prediction_flipped"],
            "original_attribution_top10_jaccard": old["attribution_top10_jaccard"],
            "original_sha256": digest(source), "metadata_sha256": digest(meta),
        }
        try:
            edited = mutate(source.read_text(encoding="utf-8"),
                            json.loads(meta.read_text())["function_name"],
                            attempt["edit_kind"])
        except Exception as exc:
            attempt.update({"status": "untestable", "reason": f"edit_{type(exc).__name__}"})
            results.append(attempt)
            continue
        verdict = run_in_sandbox(args.sandbox_image, source, meta, edited=edited, timeout=args.timeout)
        if not verdict.get("ok"):
            attempt.update({"status": "untestable", "reason": verdict.get("error_type", "sandbox_error")})
        else:
            equal = bool(verdict["behavior_matches_on_tests_and_probes"])
            attempt.update({
                "status": "matched_on_observed_inputs" if equal else "behavior_mismatch",
                "n_task_cases": verdict["n_cases"],
                "original_n_pass": verdict["n_pass"],
                "original_correct_on_task_cases": verdict["all_pass"],
                "edited_n_pass": verdict["edit_n_pass"],
                "edited_correct_on_task_cases": verdict["edit_all_pass"],
                "task_outputs_match": verdict["task_outputs_match"],
                "n_extra_probes": verdict["n_probe_cases"],
                "extra_probe_disagreements": verdict["n_probe_disagreements"],
                "probes_domain_validated": False,
            })
        results.append(attempt)
        if (j + 1) % 12 == 0:
            print(f"Completed {j+1}/{len(history)} paired checks", flush=True)
    if len(results) != len(history):
        raise AssertionError("Incomplete paired check coverage")
    result = pd.DataFrame(results)
    args.output_dir.mkdir(parents=True)
    result.to_csv(args.output_dir / "equivalence_results.csv", index=False)
    counts = dict(Counter(result["status"]))
    candidates = result.loc[result["status"].eq("matched_on_observed_inputs")]
    summary = {
        "n_interventions": len(result),
        "n_unique_programs": int(result["file_name"].nunique()),
        "statuses": counts,
        "n_behavior_matches": len(candidates),
        "n_matching_originals_not_correct": int((~candidates["original_correct_on_task_cases"].astype(bool)).sum()) if not candidates.empty else 0,
        "n_originals_correct_on_task_cases": int(result["original_correct_on_task_cases"].fillna(False).sum()),
        "n_extra_probes": int(result["n_extra_probes"].fillna(0).sum()),
        "n_extra_probe_disagreements": int(result["extra_probe_disagreements"].fillna(0).sum()),
        "limitations": [
            "Agreement on task examples and generated probes is not formal semantic equivalence.",
            "Extra probes are type-derived and NOT guaranteed to be within the specification domain.",
            "No independence among transformations of the same original program.",
            "Original/edited correctness is assessed separately from pair agreement.",
            "No demonstrated equivalence of side effects, timing, tracebacks, or introspection.",
        ],
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.output_dir / "manifest.json").write_text(json.dumps({
        "python": platform.python_version(),
        "sandbox_image_sha256": digest(args.sandbox_image),
        "sandbox_worker_sha256": digest(Path(__file__).with_name("sandbox_validation_worker.py")),
        "original_interventions_sha256": digest(args.original_interventions),
        "timeout": args.timeout, "intervention_selection": "original published fixed 72 pair list",
    }, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN)
    p.add_argument("--test-csv", type=Path, default=DEFAULT_TEST)
    p.add_argument("--research-root", type=Path, default=RESEARCH_ROOT)
    p.add_argument("--sandbox-image", required=True, type=Path)
    p.add_argument("--original-interventions", type=Path,
                   default=ROOT / "experiments/rq2_interventions_final_001/interventions.csv")
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--timeout", type=int, default=20)
    evaluate(p.parse_args())


if __name__ == "__main__":
    main()
