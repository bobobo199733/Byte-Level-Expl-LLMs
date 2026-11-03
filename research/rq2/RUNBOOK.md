# RQ2 — Evaluating explanations of code-origin classifier decisions

**Research question:** To what extent do explanations of a bytecode-based
LLM-origin classifier identify stable, traceable implementation patterns
that generalize to previously unseen programming tasks?

This is the **first RQ2 computational experiment**. It does not claim to
explain the generating LLM's internal decision process.

## Motivation from completed RQ1

The full nested RQ1 experiment found roughly 65% accuracy for raw AST
features, but the later controlled experiment found ~64.7% for
length/documentation-only features and only ~36–40% when removing those
confounders. The bytecode full-opcode frequency baseline produced ~40.75%
mean accuracy on unseen tasks over three shuffled partition seeds.

We therefore begin RQ2 with **complete opcode frequencies**, not the
confounded AST classifier and not the historical fixed-position classifier.
The bytecode signal is modest, so any explanation claims must be
interpreted conditionally on limited classifier performance.

## What the pipeline does

Entry point: `research/rq2/run_explanations.py`.

1. **Source provenance and exact historical agreement.** Uses CPython
   **3.13**, extracts all recursive opcode/decoded-argument pairs from
   archived cleaned programs, and fails if the original first 320
   saved positional feature values differ. No generated program is
   executed. Only parsing, compilation and disassembly occur.
2. **Task-disjoint models.** Runs task-grouped outer folds for seeds 7,
   42, 101, selecting multinomial Logistic Regression regularization
   using inner task-grouped CV. Standardization and background means
   are derived only from each outer training subset.
3. **SHAP-equivalent linear attributions.** For a linear multinomial
   classifier with an independent-feature interventional background,
   the *exact* per-feature contribution in logit units is
   `(x_j - E_train[x_j]) * beta_class,j`.
   The implementation calculates this formula directly rather than
   loading the separate `shap` package. It is an exact analytical
   special case of interventional linear SHAP, **not** TreeSHAP,
   probability-space SHAP, or an explanation of LLM internals.
   Opcode frequency vectors are compositional, so the independence
   assumption and single-feature replacement can generate vectors
   that are not physically valid code representations.
4. **Faithfulness to the classifier (algebraic).** Verify on every
   held-out program that baseline logit plus feature contributions
   reconstructs the classifier's decision function. Additionally,
   replace selected features with their outer-train reference mean
   and verify actual logit change matches the attributed contribution.
   **This is not a source-code intervention or causal study.**
5. **Selection only on training tasks.** Select top-k per-class opcode
   features from the outer training set's mean absolute logit
   attributions. On *held-out tasks*, report prevalence, mean
   contribution and positive-contribution fraction.
6. **Simple-baseline comparison.** Compare the selected attribution
   ranking against class-versus-rest raw opcode-frequency differences,
   computed only on training examples. Report top-k overlap per class
   and fold; overlap does not establish SHAP adds value.
7. **Stability.** Pairwise top-k set Jaccard across independent models'
   outer folds and partition seeds. Recurrent features are described
   by opcode and support across fits, not as established LLM habits.
8. **Grounded source examples.** For selected positive held-out
   examples with nonzero opcode frequency, use the canonical Phase 1
   `instruction_trace_from_file` implementation to connect opcode
   occurrences with exact compiled instructions and normalized source
   lines. The normalized line number **is not the original file's
   physical line number**. Evidence is observational and examples
   are deliberately curated, not a systematic correctness proof.

## Run on UvA IVI cluster

Ensure your active interpreter is Python 3.13 and your current directory
is the repository root:

```bash
cd ~/Byte-Level-Expl-LLMs
git fetch origin
git switch --track origin/feat/rq2-bytecode-explanation-validation-20261103
# If branch already exists locally:
# git switch feat/rq2-bytecode-explanation-validation-20261103
# git pull --ff-only
source research/.venv313/bin/activate
python --version
python -c "import numpy, pandas, sklearn; print('Dependencies OK')"
```

If packages are missing, use:

```bash
uv pip install --python research/.venv313/bin/python numpy pandas scikit-learn
```

**First — preparation and bytecode consistency audit (no classifier):**

```bash
python research/rq2/run_explanations.py \
  --prepare-only \
  --output-dir research/experiments/rq2_prepare_001
```

**Then — short end-to-end smoke test:**

```bash
python research/rq2/run_explanations.py \
  --seeds 7 --outer-folds 2 --inner-folds 2 \
  --top-k 5 --max-examples 1 \
  --output-dir research/experiments/rq2_smoke_001
```

**Finally — primary RQ2 experiment:**

```bash
python research/rq2/run_explanations.py \
  --seeds 7 42 101 \
  --outer-folds 5 --inner-folds 4 \
  --top-k 10 --max-examples 2 --jobs 1 \
  --output-dir research/experiments/rq2_opcode_full_001
```

This is CPU-only; on HPC run the main experiment inside an **allocated
CPU compute session**, not the shared login node. It recompiles source
and traces examples; it may take longer than the RQ1 classifier run.
Each output directory must be new: the script refuses overwriting
existing experiment directories.

**After successful execution, commit the experiment outputs:**

```bash
git add -f research/experiments/rq2_prepare_001/
git add -f research/experiments/rq2_smoke_001/
git add -f research/experiments/rq2_opcode_full_001/
git diff --cached --name-only
git commit -m "Add RQ2 classifier explanation and source evidence results"
git push origin feat/rq2-bytecode-explanation-validation-20261103
```

Do not commit models, virtual environments or caches. The experiment
does **not** write or overwrite the original bytecode/SHAP results.

## Output and claim boundary

| File | Interpretation |
| --- | --- |
| `manifest.json` | Exact input hashes, versions, evaluation protocol, feature assumptions |
| `source_audit.csv` | Source digests and historical feature contract verification |
| `oof_predictions.csv` | Out-of-task predictions, logit scores and class labels |
| `feature_attributions.csv` | Training-selected opcodes and held-out attribution summaries |
| `faithfulness_audit.csv` | Numerical logit reconstruction and model-feature replacement errors |
| `rank_stability.csv` | Class-level top-k overlap and recurrent opcode support across folds |
| `source_evidence.json` | Specific normalized-source instructions underlying selected held-out examples |
| `fold_scores.csv` | Inner tuning and outer performance per fit |
| `results.json` | Aggregate diagnostics and explicit scientific limitations |

This first implementation does **not** measure behavioral correctness
of generated code, source-level semantics-preserving intervention
faithfulness, or a human-grounded notion of useful explanation. Those
are separate RQ2 validation questions. No classifier attribution,
however stable, establishes why an LLM generated a particular
implementation.

## Recommended publication framing

Report explanations as **candidate classifier-associated opcode
patterns**. Demand (i) nontrivial out-of-task classifier signal,
(ii) stable train-selected features, (iii) source trace support
and task coverage, and (iv) stronger evidence from behavior-preserving
code interventions *before* claiming semantic implementation strategies.
Include simple frequency baselines; a feature already obvious from
class-conditional opcode frequencies is not a unique SHAP insight.
