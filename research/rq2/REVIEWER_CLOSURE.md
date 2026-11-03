# ICSE 2027 reviewer-closure matrix (evidence-based)

This file tracks the 17 rows in `ICSE_2027_Review_Improvements.xlsx`
(the review improvement sheet). `Implemented` means executable code
exists; `evidenced` means a user-produced artifact supports the claim;
`closed` means the *entire* reviewer request is supported. They are not
synonyms. Do not mark rows as closed because a script was merely committed.

Last code update: 2026-11-03. The new scripts must be run on the actual
archive and their outputs inspected before any new rows can be closed.

| ID | Concern | Status before this PR | Added evidence/work | What still prevents full closure |
| --- | --- | --- | --- | --- |
| 1 | Practical SE motivation | Open | Paper framing below | Confirm use case and rewrite manuscript abstract/introduction |
| 2 | SHAP overclaim | Partial | Distinguish auxiliary classifier from generating LLM in every experiment protocol | Manuscript title, abstract, RQs and conclusions must follow same language |
| 3 | Brittle byte position | Covered | Full opcode frequency/bigram RQ1 tests | Report limitations of original positional experiments |
| 4 | Simpler representations | Partial | AST, full opcode counts, n-grams, positional + length baseline under task-aware CV | Source token baseline and relative-position structural motif baselines not run |
| 5 | Weak classifier | Partial | RQ1 task-disjoint results and ablations; limited signal admitted | Cannot upgrade modest signal by explanatory statistics; limit claims |
| 6 | Single split | Covered | Three seeds, 5x4 grouped CV | Same 50-task dataset, not external replication |
| 7 | Confidence/testing | Partial | Existing RQ1 task bootstrap; new `reviewer_diagnostics.py` adds RQ2 task-bootstrap accuracy, macro F1, class recall intervals | Run and review new report; grouped-baseline test/adjustment for multiple hypotheses still needed |
| 8 | SHAP ranking stability | Partial | Top-10 Jaccard across 15 fits and recurrent opcode support | Existing artifact contains ONLY top-k features; full rank correlation requires saving all 256 feature rankings per fold, then rerun |
| 9 | Generated-code correctness | Partial | Archival correctness coverage report (154/1316 known) | Independently run tests securely for remaining programs and repeat subgroup study |
| 10 | Confounders | Partial | RQ1 length-only control and size-normalized AST ablations expose severe confounding | Verify specific historical STORE_FAST claim conditioned on task/length/early assignments/correctness |
| 11 | Shifted-instruction robustness | Open | Design notes below | Actual behavior-preserving refactoring/compilation trials and SHAP reruns |
| 12 | Model-specific insights | Partial | New feature recurrence and curated source evidence/counterexample aggregation | Interpret candidate constructs manually, task breadth and false-positive sources |
| 13 | Subjective backtracking | Partial | Canonical instruction-to-normalized-source mapping plus review rubric below | Two independent human reviews and disagreement adjudication |
| 14 | Explanation faithfulness | Partial | Exact logit additivity and feature replacement effects in classifier space | Behavior-preserving source/bytecode edits and corresponding classifier changes |
| 15 | Per-class evaluation | Covered | Confusion, class metrics, RQ1 task outputs and predicted probabilities | Discuss class failures honestly in manuscript |
| 17 | Generation failures/exclusions | Open | New `audit_generation_inventory.py` catalogs planned design cells, raw/cleaned/retained artifacts | Execute inventory; raw generation attempt logs and exclusion reasons are not necessarily archived |
 

Note: The spreadsheet has 17 items, indexed 0–16. The matrix
uses human-friendly 1–17 for the **same** 17 reviewer items.
Additional cross-cutting reproducibility requirements (source checksums,
manifest, repeatable commands and a clean artifact) are tracked in the
existing runbooks and are not counted as an eighteenth sheet item.

## Non-optional paper claim boundary

**Practical use case (proposed, not reviewer-verified):** A researcher
investigating code-generating LLM output differences can use a
task-aware bytecode attribution audit to identify candidate differences,
trace them to implementation constructs, quantify their recurrence,
and reject unstable associations. It is **not** a reliable authorship
detector or an explanation of the original LLM's internal intentions.

**RQ1 finding:** Positional bytecode and relative opcode-frequency
classifiers generalize weakly; apparent strong AST classification
is mostly confounded by source length/documentation cues.
Report this negative finding prominently.

**RQ2 finding:** Exact linear SHAP-type logit contributions are
algebraically faithful to the auxiliary model; rankings show low-to-
moderate stability and source trace examples are *selected* cases,
not representative evidence of generated-code semantic choices.

**Interpretive protocol for each pattern:**
1. Record model class, opcode, fold-support count, selected-feature
   ranking, and the generation task ID.
2. Confirm opcode and source construct using the canonical trace;
   report that line numbers are for normalized source.
3. Verify true generating class, predicted class and sign of logit
   contribution separately. A positive class contribution is not
   evidence that the class won the prediction.
4. Report supporting examples *and* counterexamples from other
   generating models, including support across **different tasks**.
5. Compare against class-versus-rest opcode frequency difference.
   Do not call a ranking difference evidence that SHAP offers more
   human value.
6. Have two reviewers independently label the pattern:
   `syntactic_structure`, `implementation_strategy`,
   `size_or_documentation`, `generic_python_opcode`,
   `unclear`. Store two labels and notes before adjudication.
7. Accept a semantic implementation-style claim only when repeated
   across multiple tasks and supported by independent agreement AND
   a controlled code-level intervention; otherwise label it
   `candidate_classifier_association`.

**Manual review queue schema (create spreadsheet/CSV separately):**
`case_id,task,file_name,true_model,predicted_model,explained_class,opcode,opname,logit_contribution,source_snippet,reviewer_A_label,reviewer_A_reason,reviewer_B_label,reviewer_B_reason,agreement,adjudicated_label,adjudication_notes`.

## Running the new reviewer-oriented diagnostics

From repository root, Python 3.13 environment active:

```bash
python research/rq2/audit_generation_inventory.py \
  --output-dir research/experiments/rq2_generation_inventory_001

python research/rq2/reviewer_diagnostics.py \
  --input-dir research/experiments/rq2_opcode_full_001 \
  --output-dir research/experiments/rq2_review_diagnostics_001 \
  --bootstrap-draws 2000
```

Commit the two output folders using `git add -f` because
`research/experiments` is intentionally ignored.

## Explicit remaining prerequisites

- To address correctness fully, acquire full valid-case/invalid-case
  test results for **all** included programs. Execute untrusted
  generated code only in an isolated sandbox with time/memory/resource
  limits; never run it in this repository's login-node process.
- To address true source-level intervention faithfulness, plan a
  controlled semantics-preserving edit study. Edits must pass original
  and edited task tests, be independently reviewed, and be shown to
  change the intended implementation construct; deletion of a
  docstring or arbitrary opcode replacement does **not** satisfy
  these requirements.
- To address subjective interpretation, collect independent human
  judgments. A script cannot create genuine independent reviewer
  agreement.
- To address full-rank SHAP stability, save all feature contributions
  in a newly versioned RQ2 rerun; current top-10 exports cannot
  reconstruct ranks 11–256.
