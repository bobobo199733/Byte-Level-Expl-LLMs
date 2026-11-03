"""Audit generation/exclusion coverage from archived raw/cleaned/feature artifacts.

Does not assume missing raw files imply a failed generation: attempts that
never reached disk are UNKNOWN. Does not run untrusted generated code.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODELS = ("llama", "mistral", "qwen")
FILE = re.compile(r"(t\d+)_p([123])_r([123])_(llama|mistral|qwen)(?:_raw)?\.(?:txt|py)$")


def run(root: Path, out: Path) -> dict:
    if out.exists():
        raise FileExistsError(f"Output already exists: {out}")
    records = []
    for task_no in range(1, 51):
        task = f"t{task_no}"
        subdir = "outputs" if task_no <= 40 else "test_data/outputs"
        for model in MODELS:
            for prompt in (1, 2, 3):
                for run_id in (1, 2, 3):
                    stem = f"{task}_p{prompt}_r{run_id}_{model}"
                    raw = root / subdir / model / "raw" / f"{stem}_raw.txt"
                    cleaned = root / subdir / model / "cleaned" / f"{stem}.py"
                    records.append({
                        "task": task, "model": model, "prompt": prompt,
                        "repeat": run_id, "raw_archived": raw.is_file(),
                        "cleaned_archived": cleaned.is_file(),
                        "raw_bytes": raw.stat().st_size if raw.is_file() else None,
                        "cleaned_bytes": cleaned.stat().st_size if cleaned.is_file() else None,
                        "file_name": cleaned.name,
                    })
    frame = pd.DataFrame.from_records(records)
    if len(frame) != 1350:
        raise AssertionError("Expected 50 tasks × 3 models × 3 prompts × 3 repeats")
    available = set()
    for split in ("features", "test_data/features"):
        file = root / split / "processed_bytecode_features.csv"
        if not file.is_file():
            raise FileNotFoundError(file)
        features = pd.read_csv(file, usecols=["file_name"])
        if features["file_name"].duplicated().any():
            raise ValueError("Duplicate file names within processed dataset")
        available.update(features["file_name"].tolist())
    frame["retained_features"] = frame["file_name"].isin(available)
    if (frame["retained_features"] & ~frame["cleaned_archived"]).any():
        raise AssertionError("Retained features have no archived cleaned source")
    frame["artifact_status"] = frame.apply(
        lambda r: (
            "retained" if r["retained_features"]
            else "cleaned_not_retained" if r["cleaned_archived"]
            else "raw_only" if r["raw_archived"]
            else "not_archived"
        ), axis=1
    )
    out.mkdir(parents=True)
    frame.to_csv(out / "generation_inventory.csv", index=False)
    summary = {
        "expected_design_cells_not_verified_api_attempts": len(frame),
        "archived_raw_count": int(frame["raw_archived"].sum()),
        "archived_cleaned_count": int(frame["cleaned_archived"].sum()),
        "retained_in_features": int(frame["retained_features"].sum()),
        "not_archived": int((frame["artifact_status"] == "not_archived").sum()),
        "by_model": frame.groupby("model")["artifact_status"].value_counts().unstack(fill_value=0).to_dict("index"),
        "by_task_model": frame.groupby(["task","model"])["artifact_status"].value_counts().unstack(fill_value=0).reset_index().to_dict("records"),
        "limitations": [
            "1350 denotes expected design cells, NOT logged successful API requests.",
            "Missing/empty raw files cannot be assigned a generation failure reason without run logs.",
            "Cleaned-but-unretained may reflect parsing, compilation, preprocessing or filtering; this audit does not infer which.",
            "Artifact coverage alone cannot exclude selection bias, but quantifies the retained subset.",
        ],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k,v in summary.items() if k not in ("by_task_model",)}, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    run(args.research_root, args.output_dir)


if __name__ == "__main__":
    main()
