# RQ2 — First reproducible experiment

The first maintained RQ2 pipeline is now implemented at
[run_explanations.py](run_explanations.py). It evaluates **classifier**
logit attributions to complete-opcode frequencies under task-disjoint
nested cross-validation, ranks top features using training tasks only,
quantifies ranking stability, compares direct class-conditional
frequency differences, verifies exact logit additivity and records
normalized-source instruction evidence.

For exact HPC commands, result schema and scientific limitations, see
[RUNBOOK.md](RUNBOOK.md). The older exploratory SHAP scripts below are
preserved for provenance and should not be confused with this
validated out-of-task experiment.

---

# RQ2 — Explaining implementation differences (planned validation track)

**Question:** To what extent can SHAP attributions to bytecode features
be linked to interpretable source-level implementation differences
across LLM-generated programs?

The original analyses are preserved under `research/scripts/`,
`research/analysis/`, and `research/shap_bytecode/` instead of moved
or overwritten. Their interpretation is conditional on the exact
classifier, Python opcode version, feature schema, and source files.

## Existing scripts by role

| Role | Existing scripts |
| --- | --- |
| Generate global SHAP values | `run_shap_bytecode.py`, `1_compute_global_shap_importance.py` |
| Task-specific explanations | `analyze_task_n.py`, `analyze_bytes.py` |
| Source-to-feature tracing | `bytecode_utils.py`, `backtrack_table.py`, `from_source_to_byte.py`, `show_bytecode.py` |
| Population and opcode analysis | `full_population_check.py`, `cross_check_population.py`, `global_opcode_dist.py`, `byte_value_scan.py`, `multi_byte_scan.py` |
| Visualizations | `show_waterfall.py`, `plot_global_ternary.py`, `plot_byte_shap_scatter.py` |

The Phase 1 canonical tracer supersedes the duplicated opcode tracing
in selected scripts. **Some exploratory scripts still need migration.**

## Proposed RQ2 acceptance gates

1. **Attribution validity.** Verify class mapping, SHAP output space,
   additive reconstruction, and dataset row ordering for every saved array.
2. **Backtracking accuracy.** For an opcode feature, prove a one-to-one
   match between the classifier's numeric value and its canonical
   disassembled instruction; explicitly distinguish normalized source
   lines from raw source lines.
3. **Coverage.** Select important features on training tasks, then
   report support and exception rates on completely unseen tasks,
   including all models, tasks and prompt variants.
4. **Stability.** Estimate feature rank overlap and Spearman
   correlation across independently refitted task-disjoint models,
   reporting feature and class coverage.
5. **Added explanation value.** Compare SHAP rankings with opcode
   occurrence frequencies and grouped permutation importance, using
   the same training/test task partitions.
6. **Faithfulness.** Run task-preserving source transformations in
   isolated execution; compare resulting model scores, SHAP
   attributions, and behavioral correctness. Differentiate
   observational from intervention-based conclusions.

Do not interpret SHAP as a causal explanation of why an LLM chose a
particular implementation. SHAP explains the *trained classifier's
output* under the supplied representation and background assumptions.

## Research handoff

The new nested RQ1 pipeline produces out-of-task predictions and
evaluation manifests. When RQ2 implementations are added, they should
read those manifests and fit their explainers only to the appropriate
outer-training data. Avoid comparing SHAP arrays from a different model
or task fold.

This directory is intentionally a **planning/index area** at present:
no new RQ2 empirical claims or recomputed SHAP files are included in
this RQ1 pull request.
