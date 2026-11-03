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
| 1 | Practical SE motivation | Open | Proposed use case below | Confirm use case; revise abstract and introduction |
| 2 | SHAP overclaim | Partial | Classifier-vs-generator boundary in code and protocol | Revise manuscript title, RQs, abstract and conclusion |
| 3 | Brittle byte position | Covered | Full opcode frequency/bigram RQ1 alternatives | Report original positional limitations |
| 4 | Simpler representations | Partial | AST, opcode, n-gram, positional and length controls | Matched source-token representation and structural motif baseline not run |
| 5 | Value added by SHAP | Partial | Matched opcode-frequency ranking baseline and overlap | Permutation importance baseline and externally validated explanation usefulness absent |
| 6 | Weak classifier signal | Partial | Grouped RQ1 validation, uncertainty, negative findings | Limit scope; cannot infer strong implementation-specific signal |
| 7 | Single split | Covered | 3 seeds, 5x4 task-disjoint grouped CV | Independent external replication is still absent |
| 8 | Confidence and significance | Partial | RQ1 task-bootstrap; new RQ2 task-bootstrap and class-recall CIs | Run and inspect new report; grouped baseline contrasts and multiplicity control |
| 9 | SHAP ranking stability | Partial | Top-10 Jaccard over 15 fits and recurrent support | Full 256-feature rank correlations not archived |
| 10 | Code correctness | Partial | New `evaluate_correctness.py` audits every retained program and `analyze_correctness_effect.py` rechecks OOF accuracy and attributions by task-test status | Run and inspect results; tasks t31–t40 have no executable task test oracle, so full correctness cannot be established from the archive |
| 11 | Task/length/preprocessing confounds | Partial | RQ1 size/docstring controls reveal confounding | Recheck specific STORE_FAST association with controls |
| 12 | Semantics-preserving robustness | Partial | Completed 72 original intervention attempts; new `evaluate_equivalence.py` checks original/edited behavior on task inputs plus additional probes | Run new validation; observed agreement is not formal general semantic equivalence |
| 13 | Specific implementation insights | Partial | Source trace and new recurrence/counterexample diagnostics | Structured qualitative interpretation and source-level task breadth |
| 14 | Backtracking subjectivity | Partial | Deterministic bytecode-to-source trace and structured counterexample auditing | Interpretation cannot be independently validated using this artifact alone |
| 15 | Faithfulness | Partial | Exact class-logit additivity, intervention results and new differential probe checks | Run and interpret new empirical study; no unrestricted semantic/causal guarantee |
| 16 | Per-class evaluation | Covered | Confusion, classification reports, per-task scores, confidence | Discuss poor class performance in manuscript |
| 17 | Generation failures/exclusions | Open | Generation artifact inventory script | Run; verify true attempts and exclusion causes using logs |

Note: The spreadsheet has 17 items, indexed 0–16. The matrix
uses item numbers 1–17 for the **same** 17 reviewer items.
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

**Automated interpretation evidence for each pattern:**
1. Report model class, opcode, held-out fold support and program task.
2. Resolve the opcode to normalized-source instructions using the canonical trace.
3. Distinguish true generating class, predicted class and class-logit contribution.
4. Report supporting cases *and* counterexamples from different models/tasks.
5. Compare class-associated features against training-only opcode frequency differences.
6. Label anything beyond the verified source construct as a candidate
   classifier association, not a proven LLM implementation preference.

This study does not include independent human interpretation validation.
Therefore the corresponding reviewer concern is **not closed** and any claim
about usefulness to developers must remain qualified.

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

- To assess correctness, run the new isolated full-dataset evaluator.
  Tasks **t31–t40 have no executable test oracle** in their archived
  metadata, so those programs remain untestable until verifiable
  reference tests are supplied. Execute generated programs only
  in the approved, resource-limited isolated sandbox.
- To address true source-level intervention faithfulness, plan a
  controlled semantics-preserving edit study. Edits must pass original
  and edited task tests, be independently reviewed, and be shown to
  change the intended implementation construct; deletion of a
  docstring or arbitrary opcode replacement does **not** satisfy
  these requirements.
- Subjective interpretation is a remaining limitation; automated
  tracing and counterexample auditing do not replace external validation.
- To address full-rank SHAP stability, save all feature contributions
  in a newly versioned RQ2 rerun; current top-10 exports cannot
  reconstruct ranks 11–256.

## Final automated validation stage

[Full correctness and observed-equivalence protocol](FULL_CORRECTNESS_AND_EQUIVALENCE.md)
provides the commands for a 1,316-program inventory of task-test outcomes,
reassessment of all 72 original intervention pairs using task cases and extra
differential probes, and correctness-stratified OOF accuracy/SHAP analyses.
These scripts require execution; their existence does **not** mark a reviewer
concern as closed. No human-review data are generated.
