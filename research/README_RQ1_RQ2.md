# Research structure: RQ1 and RQ2

This repository contains historical experiments and a new maintained
research workflow. Legacy scripts and saved outputs remain in place to
preserve reproducibility; they have **not** been moved or deleted.

## RQ1 — Model attribution on unseen programming tasks

**Question:** To what extent can Python bytecode distinguish code generated
by different LLMs across unseen programming tasks?

Maintained entry point: [rq1/run_nested_cv.py](rq1/run_nested_cv.py)\n\nAdditional reviewer-driven checks: [rq1/VALIDATION.md](rq1/VALIDATION.md)\n([rq1/run_validation.py](rq1/run_validation.py)).

- Train/evaluate with fully task-disjoint outer GroupKFold splits
- Tune hyperparameters and select the representation+model **only** by
  inner task-grouped validation
- Compare original positional opcode/argument features with
  normalized opcode-frequency and source AST-count baselines
- Compare XGBoost, logistic regression, and optional random forest
- Save per-example out-of-fold predictions, per-task metrics, class reports,
  confusion matrices, fold configurations, and task-level bootstrap intervals
- Write every run to a **new output directory**; never mutate the historical
  models, datasets, or saved SHAP analyses

The existing `scripts/cross_validation.py` is a **historical, exploratory**
500-partition evaluation, not the nested confirmation experiment. Its
`cross_validation/cv_stats.json` results should remain unchanged.

Historical data were reproduced by the researcher using CPython 3.13.18
for all 1,053 training and 263 held-out feature vectors. The old classifier
was also loaded and reproduced the saved 112/263 accuracy (42.5856%).
These facts establish representation and artifact reproducibility, not
generalization across tasks.

## RQ2 — Explaining source-level implementation differences

**Question:** To what extent can SHAP attributions to bytecode features be
linked to interpretable source-level implementation differences across
LLM-generated programs?

Roadmap: [rq2/README.md](rq2/README.md)

The existing scripts in `scripts/` and artifacts in `shap_bytecode/`
remain preserved. Do not recompute these against a model with a different
input schema or training provenance without an explicit new experiment.

## Legacy folders and provenance

| Path | Role |
| --- | --- |
| `scripts/` | Historical data generation, training, SHAP, analyses, and visualizations |
| `features/` | Historical training features (preserve) |
| `test_data/features/` | Historical held-out feature vectors (preserve) |
| `models/` | Historical trained models and reports (preserve) |
| `cross_validation/` | Historical 500-partition results (preserve) |
| `shap_bytecode/` | Historical SHAP analyses (preserve) |
| `rq1/` | Maintained RQ1 experiment entry points |
| `rq2/` | RQ2 experiment design and forthcoming implementations |
| `experiments/` | User-supplied output location for independent runs |

## Running RQ1 on the HPC cluster

From the root of the repository, activate a Python 3.13 environment with
`numpy`, `pandas`, `scikit-learn`, and `xgboost` installed.

**Fast smoke run** (2 outer folds, 2 inner folds, logistic regression):

```bash
python research/rq1/run_nested_cv.py \
  --representations positional opcode_hist \
  --models logistic \
  --outer-folds 2 --inner-folds 2 \
  --bootstrap-draws 100 \
  --output-dir research/experiments/rq1_smoke_001
```

**Primary experiment** (5 outer folds, 4 inner folds, two classifier
families, three representations):

```bash
python research/rq1/run_nested_cv.py \
  --representations positional opcode_hist ast \
  --models xgboost logistic \
  --outer-folds 5 --inner-folds 4 \
  --bootstrap-draws 1000 --jobs 1 \
  --output-dir research/experiments/rq1_nested_001
```

Use a **new output directory** for each repeat. Never run the historical
parameter sweeps against the held-out task set as a way of selecting the
reported model.

Results will appear in:
- `manifest.json`: exact input SHA-256, version and experiment configuration
- `fold_scores.csv`: inner selection scores and outer fold diagnostics
- `selected_oof_predictions.csv`: strictly out-of-task predictions from
  the inner-selected representation and classifier
- `candidate_oof_predictions.csv`: same folds for each fixed candidate
- `paired_comparisons.json`: paired task-bootstrap differences against fixed candidate baselines\n- `ast_source_inventory.csv`: SHA-256 of each original source used for the AST baseline\n- `task_scores.csv`: out-of-task accuracy for each task
- `results.json`: overall metrics, confusion matrix and task-bootstrap CIs

**Interpretation:** the selected nested model's outer-fold predictions
provide an out-of-task estimate of the complete selection procedure.
The candidate results are secondary comparisons and should not be used to
choose a 'winning' model using test-set performance.

## Limitations

These data contain multiple generations per task, so the unit of resampling
must be the task, not the individual program. Random task folds can be
heterogeneous and their scores are correlated. Task-bootstrap intervals
are descriptive estimates conditional on this dataset and splitting design;
they are not evidence of causality.

The AST-count baseline reads cleaned code from disk but never runs it.
It intentionally differs from positional-bytecode representations; any
claims about 'source independent' attribution must be restricted to the
bytecode-based candidates.
