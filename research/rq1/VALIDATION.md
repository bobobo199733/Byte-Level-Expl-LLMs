# RQ1 validation experiments — second-stage preregistered checks

The original RQ1 experiment under `research/experiments/rq1_nested_full_001`
is an archived result. Do **not** overwrite it. The validation here is a
separate experiment designed to address ICSE reviewer concerns about brittle
fixed positions, superficial length/docstring cues, limited task split
diversity, opcode truncation, and code correctness.

Maintained script: `research/rq1/run_validation.py`.

## Scope and guarantees

1. **Full bytecode:** recompile all archived Python programs using CPython
   **3.13** and the same canonical `bytecode_utils.extract_script_bytecode`
   pipeline used for the historical dataset. Before using a program,
   compare its first 320 values with every stored `byte_N` value;
   fail the entire run immediately if they differ. Then use all
   opcode instructions for normalized frequency and bigram features.
   These are opcode/decoded-argument pairs, *not* raw CPython bytes.
2. **AST ablations:** distinguish raw AST counts (original baseline) from
   AST counts without explicit total-node/source-line features, AST counts
   with module/function/class docstrings stripped, normalized docstring-free
   AST frequencies, and an explicit source-length/docstring control.
   Removing total-node count alone does **not** fully eliminate length
   information in the remaining AST counts, which motivates normalized
   AST frequencies.
3. **Repeated unseen-task assessment:** use five-fold
   `StratifiedGroupKFold`, grouped by task, with shuffled assignments
   across three predefined seeds. Logistic Regression regularization is
   selected by a *different* four-fold task-grouped inner CV for each
   outer fold. All standardization fits on outer-training folds only.
   We deliberately fix the classifier family to Logistic Regression:
   the first full experiment selected AST+Logistic in all five folds.
4. **Correctness evidence:** merge existing `research/evaluation/scores`
   records by exact program filename, refuse duplicate or inconsistent
   labels, and report score availability, pass-all and not-pass-all
   cases. Also report observational out-of-fold performance on the
   subset with known correctness. **Never infer missing=incorrect**.
   This module **never executes generated programs**; missing scores
   must be produced with a separate execution sandbox and documented
   task-specific tests before full correct/incorrect causal claims.
5. **Provenance:** store all output in a new directory, including a SHA-256
   per source file, test/train input hashes and CPython/library versions.
   Rerunning the same output directory is refused.

## HPC commands

From the root of your clone, check out the existing branch and activate
your Python 3.13 environment:

```bash
cd ~/Byte-Level-Expl-LLMs
git fetch origin
git switch feat/rq1-nested-task-cv-20261103
git pull --ff-only origin feat/rq1-nested-task-cv-20261103

# If a different venv is active, deactivate that before this line.
source research/.venv313/bin/activate
python --version
python -c "import numpy,pandas,sklearn; print('Dependencies OK')"
```

If packages are missing, run:

```bash
uv pip install --python research/.venv313/bin/python numpy pandas scikit-learn
```

**Step A — Extract and verify all representations, without training:**

```bash
python research/rq1/run_validation.py \
  --prepare-only \
  --output-dir research/experiments/rq1_validation_prep_001
```

Expect the program to report 1,316 verified sources with exact historical
first-320 matches. Review `source_audit.csv`, `correctness_summary.json`,
and `correctness_coverage.csv`.

**Step B — Run the main validation with three distinct task partition seeds:**

```bash
python research/rq1/run_validation.py \
  --seeds 7 42 101 \
  --outer-folds 5 \
  --inner-folds 4 \
  --bootstrap-draws 1000 \
  --ngram-buckets 256 \
  --jobs 1 \
  --output-dir research/experiments/rq1_validation_full_001
```

This can be CPU-intensive. Run inside an allocated compute node rather
than the shared HPC login node; it does not require a GPU.
Use unique names for further repeats.

**Optional quick dry run**, including model training:

```bash
python research/rq1/run_validation.py \
  --seeds 7 \
  --variants ast_original ast_core_prop length_only opcode_full \
  --outer-folds 2 --inner-folds 2 \
  --bootstrap-draws 50 \
  --ngram-buckets 32 \
  --output-dir research/experiments/rq1_validation_smoke_001
```

## Results and interpretation

- `manifest.json`: experiment version, task partitioning, feature list,
  seeds, software versions, input file digests and correctness coverage
- `source_audit.csv`: filename, source checksum, original split,
  full opcode count, first-320 exact-validation status
- `correctness_coverage.csv`, `correctness_summary.json`: which
  archived programs have usable scoring evidence, by true class
- `correctness_oof_diagnostics.json`: descriptive OOF metrics on known
  pass-all and known not-pass-all subsets; not a representative estimate
  unless scoring coverage is complete
- `oof_predictions.csv`: one prediction for each archived program in
  each seed and each representation under a task-disjoint outer fold
- `fold_scores.csv`: best inner hyperparameters and outer test scores
- `task_partitions.json`: exact train/test task IDs in every split
- `results.json`: per-seed performance and paired **task-bootstrap**
  differences relative to the original AST baseline

The statistical unit is the **task**, not the individual generation.
Task bootstrap is computed separately for every partition seed; the
three partition seeds are correlated views of the same 50 tasks and
must not be treated as independent datasets.

**Go/no-go for RQ2:** if AST still outperforms length-only and normalized
docstring-free AST remains effective across task splits, RQ2 can begin
with AST classifier explanations. Bytecode explanation claims require
their **own** validated opcode-based classifier signal; strong AST
accuracy alone does not establish bytecode explanation validity.
Even with good accuracy, SHAP explains classifier behavior, not the
causal process inside the generating LLM.

## Publication/reviewer caveats

- The baseline includes only 50 existing task types and three LLMs; do
  not claim transfer to unrelated languages, larger models, or real-world
  repositories.
- This script audits existing correctness-score coverage and subgroup
  performance, but **does not establish correctness for unscored code**.
  For a full correctness-controlled study, collect complete scores in a
  secure sandbox and rerun the subgroup audit using that score directory.
- Raw AST counts include structural code-size information even after
  docstring removal. The normalized `ast_core_prop` variant is the
  strongest control for size effects included here.
- Opcode n-gram hashes may collide. The hash is deterministic and fixed
  *before* data splitting, not selected using held-out programs.
- Repeated partitions reduce sensitivity to a single task split but do
  not replace evaluation on an independent new task corpus.
