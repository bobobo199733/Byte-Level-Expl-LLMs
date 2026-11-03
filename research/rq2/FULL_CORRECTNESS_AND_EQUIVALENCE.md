# Final automated correctness and observed-equivalence validation

Three scripts close the **automatable** part of the remaining reviewer
requests. They require Python 3.13 on the host, the existing
\`research/.venv313\` packages, and \`python313.sif\` with network-isolated
Apptainer execution. NO human reviewers or manual CSV completion.

Prior results in \`rq1_*\`, \`rq2_opcode_full_001\`, and
\`rq2_interventions_final_001\` stay unchanged.

## Run these three FINAL experiments in order

From the repository root and **inside an allocated CPU compute-node
session** with sufficient wall-clock time:

\`\`\`bash
cd ~/Byte-Level-Expl-LLMs
git fetch origin
git switch feat/rq2-bytecode-explanation-validation-20261103
git pull --ff-only origin feat/rq2-bytecode-explanation-validation-20261103
source research/.venv313/bin/activate

# 1. Score every one of 1,316 retained programs against ALL provided task
#    cases (valid_cases, explicit_cases, invalid_cases).
python research/rq2/evaluate_correctness.py \
  --sandbox-image "$PWD/python313.sif" \
  --timeout 20 \
  --output-dir research/experiments/rq2_correctness_final_001

# 2. Recheck the original 72 source interventions on task cases and up
#    to 40 additional deterministic differential probes per pair.
python research/rq2/evaluate_equivalence.py \
  --sandbox-image "$PWD/python313.sif" \
  --original-interventions research/experiments/rq2_interventions_final_001/interventions.csv \
  --timeout 20 \
  --output-dir research/experiments/rq2_equivalence_final_001

# 3. Analyze held-out classifier accuracy as a function of the new
#    program correctness status and join the original interventions.
python research/rq2/analyze_correctness_effect.py \
  --correctness research/experiments/rq2_correctness_final_001/correctness_results.csv \
  --equivalence research/experiments/rq2_equivalence_final_001/equivalence_results.csv \
  --output-dir research/experiments/rq2_correctness_analysis_final_001
\`\`\`

**Do not rerun existing RQ1 or RQ2 classifiers.** These are additive
validations. Each output folder must be new (fail-closed no overwrite).

## Check final outputs

\`\`\`bash
cat research/experiments/rq2_correctness_final_001/summary.json
cat research/experiments/rq2_equivalence_final_001/summary.json
cat research/experiments/rq2_correctness_analysis_final_001/correctness_analysis.json
\`\`\`

If the sandbox cannot launch, its results are reported as
\`untestable\`; such cases must **not** be counted as incorrect or
equivalent. If the image is absent, first obtain a Python 3.13 image
and validate \`apptainer exec --containall --cleanenv --net --network
none --no-home python313.sif python3 --version\`.
Do not disable sandbox isolation flags to force a result.

## What correctness means

The task metadata are read directly from archived
\`research/prompts/t*/meta.json\` and
\`research/test_data/prompts/t*/meta.json\`. The sandbox checks:
- \`valid_cases\`: reference output equality;
- \`explicit_cases\`: reference output equality (previous checker
  failed to include this field);
- \`invalid_cases\`: expected exception type;
- \`allow_multiple_expected\`: accepts any documented expected result.

The resulting \`correctness_results.csv\` contains 1316 rows and
per-program counts, model, task, source hashes, and one of
\`pass\` / \`fail\` / \`untestable\`. A program is \`pass\` only when
**all available documented cases pass**.

The classifier follow-up combines this table with the already committed
out-of-fold predictions and reports accuracy/macro F1 within these
groups with confidence intervals resampling tasks, NOT individual
examples. These are subgroup analyses of **previously trained models**,
not new models trained on correct-only programs.

## What observed equivalence means

The \`evaluate_equivalence.py\` script uses the *same 72 archived
interventions* rather than silently selecting more favorable cases.
Original and edited programs are both executed inside the sandbox.
It checks equality of observed output values / exception **types**
on every original task input, then generates up to 40 **deterministic,
metadata-derived probes** by varying primitive inputs. The probes are
not guaranteed to satisfy the task's domain constraints, so they are
used **only for paired differential comparison**, not correctness.

Original correctness is reported separately: an incorrect program
might nonetheless behave identically after a transformation. Accepted
pairs are marked \`matched_on_observed_inputs\` — NEVER described as
a formal proof of general semantic equivalence. These tests do not
establish equivalence of introspection, side effects, execution time,
or tracebacks. Python's general program-equivalence problem cannot be
solved exhaustively by randomized tests.

Outputs:
- \`rq2_correctness_final_001/correctness_results.csv\`
- \`rq2_correctness_final_001/summary.json\`
- \`rq2_equivalence_final_001/equivalence_results.csv\`
- \`rq2_equivalence_final_001/summary.json\`
- \`rq2_correctness_analysis_final_001/correctness_joined_oof.csv\`
- \`rq2_correctness_analysis_final_001/intervention_correctness_joined.csv\`
- \`rq2_correctness_analysis_final_001/correctness_analysis.json\`

## Commit the final experimental outputs

\`\`\`bash
git add -f research/experiments/rq2_correctness_final_001/
git add -f research/experiments/rq2_equivalence_final_001/
git add -f research/experiments/rq2_correctness_analysis_final_001/
git commit -m "Add full RQ2 correctness and differential equivalence validation"
git push origin feat/rq2-bytecode-explanation-validation-20261103
\`\`\`

## Cautions for reviewers

1. Correctness is on archived task cases, not mathematical proof.
2. Differential input probes are type-based, not independently
   verified task-domain generators.
3. Outcome equality compares return values and exception types
   on sampled inputs, not all observable effects.
4. The 72 intervention rows are paired around 36 originals; they
   are not 72 independent programs.
5. A program that does not pass tests is not automatically
   classified as non-equivalent to its modified version.
6. The classifier measures code-origin signals; SHAP explains the
   auxiliary classifier and not the original generating LLM.
