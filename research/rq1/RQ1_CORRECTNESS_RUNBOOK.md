# RQ1 correctness-stratified validation (final additive analysis)

This analysis uses the **already committed** RQ2 task-test correctness inventory
for all **1,316 retained programs**, together with historical RQ1 out-of-fold
predictions. No generated source is executed, no model is retrained, and
existing RQ1/RQ2 experiment folders are never modified.

It is intentionally separated from the RQ2 explainability analysis:
- RQ1 tests whether the origin-classification signal and comparative
  representation performance are associated with task-test correctness.
- RQ2 assesses the model explanation's properties and intervention response.
- Both use **exactly the same** correctness status labels, including
  \`untestable\` (do NOT treat missing task oracles as incorrect programs).

## Final command

From repository root on Python 3.13 with the same research environment:

\`\`\`bash
cd ~/Byte-Level-Expl-LLMs
git switch feat/rq2-bytecode-explanation-validation-20261103
git pull --ff-only origin feat/rq2-bytecode-explanation-validation-20261103
source research/.venv313/bin/activate

python research/rq1/analyze_correctness_effect.py \
  --correctness research/experiments/rq2_correctness_final_001/correctness_results.csv \
  --validation-oof research/experiments/rq1_validation_full_001/oof_predictions.csv \
  --selected-oof research/experiments/rq1_nested_full_001/selected_oof_predictions.csv \
  --bootstrap-draws 2000 \
  --output-dir research/experiments/rq1_correctness_final_001
\`\`\`

If the output folder already exists, use a **new** suffix; existing
data is never overwritten.

## Outputs

- \`correctness_joined_rq1_oof.csv\`: program-level OOF predictions and
  correctness status, with exact task/label/file-name checks
- \`correctness_subgroup_metrics.csv\`: accuracy, balanced accuracy,
  macro-F1, model support, and number of tasks for each representation,
  seed, and correctness group
- \`correctness_paired_variant_contrasts.csv\`: task-bootstrap 95%
  intervals for **matched** code-origin representation comparisons
  (opcode frequencies versus length-only/AST, opcode bigrams, etc.)
- \`within_task_correctness_differences.csv\`: descriptive pass-vs-fail
  classification accuracy on the same task (only where both groups exist)
- \`summary.json\`: data coverage, seeds, sample counts, limitations

The RQ1 nested selected classifier is analyzed separately from the
three-seed representation validation. It is not pooled with those models.

## Commit the new artifact

\`\`\`bash
git add -f research/experiments/rq1_correctness_final_001/
git commit -m "Add final RQ1 correctness-stratified representation validation"
git push origin feat/rq2-bytecode-explanation-validation-20261103
\`\`\`

## Interpretation boundaries

The existing full-data task-disjoint classifiers were trained on the
entire historical dataset. Therefore this is an OOF **stratification**
by correctness, not a claim that the classifiers would maintain the same
performance if *trained exclusively* on correct code. If reviewers ask
for a correct-only re-training ablation, that is a distinct experiment
which must preserve task-grouped outer splits and tune exclusively
within the outer-training partition.

Some tasks (notably t31–t40) have no executable test oracle in their
metadata, and remain \`untestable\` in the correctness inventory. The
within-task comparisons and task-bootstrap intervals account for task
clustering; nevertheless, correctness subgroups differ by task and
generating LLM, so differences are descriptive, **not causal**.
Multiple representation contrast intervals are exploratory and
not adjusted for simultaneous hypothesis testing.

Review the outputs before updating manuscript claims. Do not silently
treat merely implemented scripts as empirical evidence.
