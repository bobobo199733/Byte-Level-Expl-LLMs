"""Prepare blinded human interpretation sheets; merge genuine independent ratings.

Never generates ratings or claims human agreement without completed sheets.
No generated Python programs are executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

LABELS = (
    "syntactic_structure", "implementation_strategy",
    "size_or_documentation", "generic_python_opcode", "unclear",
)


def prepare(evidence_file: Path, out: Path, max_cases: int = 36):
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite {out}")
    if max_cases < 6:
        raise ValueError("Select at least six examples")
    evidence = pd.read_json(evidence_file)
    required = {
        "explained_class", "true_model", "prediction", "file_name",
        "opcode", "opname", "heldout_logit_shap", "sample_source_lines",
        "seed", "fold",
    }
    if not required.issubset(evidence):
        raise ValueError(f"Missing evidence columns: {required - set(evidence)}")
    if evidence.empty:
        raise ValueError("Source evidence file is empty")
    evidence["task"] = evidence["file_name"].str.extract(r"^(t\d+)")[0]
    if evidence["task"].isna().any():
        raise ValueError("Unrecognized task filenames")
    evidence["case_type"] = np.where(
        (evidence["true_model"] == evidence["explained_class"])
        & (evidence["prediction"] == evidence["true_model"]),
        "matched_class_and_prediction",
        "contradictory_or_other_model",
    )
    # Curate one example per (explained class, task, opcode, case type),
    # prioritizing large positive heldout contributions, then diversify.
    candidates = evidence.sort_values(
        ["heldout_logit_shap", "file_name"], ascending=[False, True]
    ).drop_duplicates(["explained_class", "task", "opcode", "case_type"])
    selections = []
    used = set()
    for category in ("matched_class_and_prediction", "contradictory_or_other_model"):
        for klass in sorted(evidence["explained_class"].unique()):
            view = candidates[
                (candidates["case_type"] == category)
                & (candidates["explained_class"] == klass)
            ]
            quota = max(1, max_cases // 6)
            for _, item in view.head(quota).iterrows():
                key = (item["file_name"], item["explained_class"], int(item["opcode"]))
                if key not in used:
                    selections.append(item)
                    used.add(key)
    for _, item in candidates.iterrows():
        if len(selections) >= max_cases:
            break
        key = (item["file_name"], item["explained_class"], int(item["opcode"]))
        if key not in used:
            selections.append(item)
            used.add(key)
    selections = selections[:max_cases]
    if not selections:
        raise ValueError("No cases selected")
    details = []
    sheets = []
    for order, item in enumerate(selections, 1):
        case_id = f"C{order:03}"
        lines = item["sample_source_lines"]
        context = " | ".join(
            f"{r.get('function', '?')}:{r.get('normalized_line', '?')} {r.get('normalized_source', '')}"
            for r in (lines if isinstance(lines, list) else [])[:3]
        )
        if not context:
            raise ValueError(f"No trace snippet for {item['file_name']}")
        source_hash = hashlib.sha256(
            (str(item["file_name"]) + str(item["opcode"]) + str(item["explained_class"])).encode()
        ).hexdigest()
        details.append({
            "case_id": case_id, "file_name": item["file_name"],
            "task": item["task"], "explained_class": item["explained_class"],
            "true_model": item["true_model"], "prediction": item["prediction"],
            "case_type": item["case_type"], "opcode": int(item["opcode"]),
            "opname": item["opname"],
            "logit_contribution": float(item["heldout_logit_shap"]),
            "evidence_sha256": source_hash,
            "context": context, "seed": int(item["seed"]),
            "fold": int(item["fold"]),
        })
        sheets.append({
            "case_id": case_id, "task": item["task"],
            "opcode": int(item["opcode"]), "opname": item["opname"],
            "source_context": context,
            "interpretation_label": "",
            "interpretation_reason": "",
            "confidence_1_to_5": "",
        })
    out.mkdir(parents=True)
    pd.DataFrame(details).to_csv(out / "private_case_key.csv", index=False)
    pd.DataFrame(sheets).to_csv(out / "reviewer_A.csv", index=False)
    pd.DataFrame(sheets).to_csv(out / "reviewer_B.csv", index=False)
    (out / "instructions.json").write_text(json.dumps({
        "labels": LABELS,
        "process": [
            "Give reviewer_A.csv and reviewer_B.csv to different human reviewers separately.",
            "Do not show either reviewer private_case_key.csv or the other reviewer sheet.",
            "Review only the opcode and contextual source snippets. Label what the evidence JUSTIFIES, not the presumed true generator.",
            "Return the two completed CSVs without changing case IDs or source context.",
            "Do not pool judgments before both files are finalized.",
            "Run --adjudicate after both sheets are complete.",
        ],
        "label_definitions": {
            "syntactic_structure": "A recognizable syntactic construct, but insufficient evidence for a generator-specific implementation preference",
            "implementation_strategy": "A coherent implementation choice visible in the source, not merely an opcode label",
            "size_or_documentation": "Likely length, boilerplate, or documentation-dependent artifact",
            "generic_python_opcode": "Generic compiler behavior without specific implementation meaning",
            "unclear": "Insufficient trace to make a defensible determination",
        },
        "n_cases": len(sheets),
        "limitations": "Blind review documents human interpretations; it does not establish model causality or independent semantic validation",
    }, indent=2) + "\n")
    print(f"Prepared {len(sheets)} blind-review cases in {out}")


def adjudicate(folder: Path, out: Path):
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite {out}")
    reviews = []
    for reviewer in ("A", "B"):
        data = pd.read_csv(folder / f"reviewer_{reviewer}.csv", keep_default_na=False)
        required = {"case_id", "interpretation_label", "interpretation_reason", "confidence_1_to_5"}
        if not required.issubset(data.columns):
            raise ValueError(f"Reviewer {reviewer} sheet missing required columns")
        if data["case_id"].duplicated().any():
            raise ValueError(f"Reviewer {reviewer} has duplicate case IDs")
        if not data["interpretation_label"].isin(LABELS).all():
            raise ValueError(f"Reviewer {reviewer} labels incomplete/invalid; real human completion required")
        if (data["interpretation_reason"].str.strip() == "").any():
            raise ValueError(f"Reviewer {reviewer} must provide a reason for every case")
        if not data["confidence_1_to_5"].astype(str).isin(["1", "2", "3", "4", "5"]).all():
            raise ValueError(f"Reviewer {reviewer} confidence must be 1–5")
        data = data[sorted(required)].rename(columns={
            "interpretation_label": f"label_{reviewer}",
            "interpretation_reason": f"reason_{reviewer}",
            "confidence_1_to_5": f"confidence_{reviewer}",
        })
        reviews.append(data)
    merged = reviews[0].merge(reviews[1], on="case_id", how="outer", validate="one_to_one", indicator=True)
    key = pd.read_csv(folder / "private_case_key.csv")
    if not (merged["_merge"] == "both").all() or set(key["case_id"]) != set(merged["case_id"]):
        raise ValueError("Reviewers have mismatched or missing cases")
    merged = merged.drop(columns="_merge").merge(key, on="case_id", validate="one_to_one")
    merged["agreement"] = merged["label_A"] == merged["label_B"]
    # Reviewers disagreeing need genuine adjudication: leave blanks, never pretend.
    merged["adjudicated_label"] = np.where(merged["agreement"], merged["label_A"], "")
    merged["adjudication_notes"] = ""
    exact = float(merged["agreement"].mean())
    kappa = float(cohen_kappa_score(merged["label_A"], merged["label_B"], labels=LABELS))
    out.mkdir(parents=True)
    merged.to_csv(out / "adjudication_queue.csv", index=False)
    (out / "review_agreement.json").write_text(json.dumps({
        "n_cases": len(merged), "n_agreements": int(merged["agreement"].sum()),
        "exact_agreement": exact, "cohen_kappa": kappa,
        "n_disagreements_pending_adjudication": int((~merged["agreement"]).sum()),
        "caution": "These numbers measure agreement on labeled curated evidence, not validity or population-wide explanatory usefulness.",
    }, indent=2) + "\n")
    print(f"Agreement: {exact:.3f}; Cohen kappa: {kappa:.3f}; unresolved: {(~merged['agreement']).sum()}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", action="store_true")
    group.add_argument("--adjudicate", action="store_true")
    p.add_argument("--source-evidence", type=Path,
                   default=Path(__file__).resolve().parents[1] / "experiments/rq2_opcode_full_001/source_evidence.json")
    p.add_argument("--review-dir", type=Path)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--max-cases", type=int, default=36)
    args = p.parse_args()
    if args.prepare:
        prepare(args.source_evidence, args.output_dir, args.max_cases)
    else:
        if args.review_dir is None:
            p.error("--adjudicate requires --review-dir")
        adjudicate(args.review_dir, args.output_dir)


if __name__ == "__main__":
    main()
