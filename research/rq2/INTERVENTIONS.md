# RQ2 focused validation: controlled source interventions

This is a *new* reviewer-facing experiment, separate from the existing
\`rq2_opcode_full_001\` and \`rq2_review_diagnostics_001\` outputs. They do
not modify historical generated programs or existing experiment artifacts.

## Scope

### A. Behavior-checked source interventions

\`run_source_interventions.py\` selects up to 36 archived programs,
diversified across LLaMA, Mistral and Qwen, and associates each with the
classifier trained on **other tasks** (nested grouped CV, seed 42).

Two candidate transformations are supported:

- \`insert_pass\`: introduce a no-op \`pass\` after any function docstring,
  which can alter compiler instruction layout without changing tested
  return values.
- \`wrap_try_finally\`: wrap the executable function body in
  \`try: ... finally: pass\`. This alters bytecode and may alter exception,
  traceback, introspection or other behavior. This is an *experimental
  hypothesis* and is **not automatically called semantics-preserving**.

Each edited source is compiled and full recursive opcode frequencies
extracted using the canonical representation. Unchanged opcode
histograms are recorded as rejected (not cherry-picked away).
Every meaningfully changed edit is sent, together with the original,
to the checker **inside a network-isolated Apptainer container**.
Both must pass the available task-specific tests with the same
outcomes. All unsafe/unavailable/failed checks are rejected and
recorded, not treated as evidence.

Only then does the script report classifier prediction flips,
class-specific logit shifts, changes to per-opcode attributions,
top-10 overlap, and exact attribution-difference additivity.

**A test pass is empirical agreement on finite available tests, not
proof of semantic equivalence for all possible inputs.** A Python
\`pass\` insertion may change tracing/introspection; the try/finally
edit may change exception handling. We must disclose those caveats.

#### Sandbox requirements

Untrusted generated programs **MUST NOT** run directly on the shared
login node, the analysis host, or without isolation.

The checker requires an existing Apptainer image with **Python 3.13**,
a network namespace turned off, restricted host mounts, and a wall-clock
timeout. Inside the checker, CPU and virtual address-space limits are
applied before executing any generated program. The script **fails
closed** if Apptainer's network namespace cannot be created. Do not
disable \`--net --network none\` just to make the test pass.

If your cluster's Apptainer policy blocks rootless network namespaces,
ask administrators for an approved fully isolated execution sandbox;
otherwise no source-execution claims can be made. The existing
\`python311.sif\` is not suitable for this Python-3.13-specific run.

From a permitted build location with container registry access,
you may build a Python 3.13 runtime image using:

\`\`\`bash
apptainer pull python313.sif docker://python:3.13-slim
\`\`\`

Only do this where your cluster permits network pulls, and record the
resulting image checksum in the experiment manifest. This is a
container image for **testing**, not an installation dependency for
the host's training environment.

#### HPC commands

\`\`\`bash
cd ~/Byte-Level-Expl-LLMs
git fetch origin
git switch feat/rq2-bytecode-explanation-validation-20261103
git pull --ff-only origin feat/rq2-bytecode-explanation-validation-20261103
source research/.venv313/bin/activate
python --version
python -m unittest discover -s research/tests -p 'test_rq2_source_interventions.py' -v
\`\`\`

Allocate a CPU compute node before running untrusted-code tests.
The driver itself must use Python 3.13. Smoke test:

\`\`\`bash
python research/rq2/run_source_interventions.py \
  --sandbox-image "$PWD/python313.sif" \
  --max-cases 6 --max-per-model 2 \
  --timeout 12 \
  --output-dir research/experiments/rq2_interventions_smoke_001
\`\`\`

Main test:

\`\`\`bash
python research/rq2/run_source_interventions.py \
  --sandbox-image "$PWD/python313.sif" \
  --seed 42 --outer-folds 5 --inner-folds 4 \
  --max-cases 36 --max-per-model 12 \
  --transforms insert_pass wrap_try_finally \
  --timeout 12 \
  --output-dir research/experiments/rq2_interventions_full_001
\`\`\`

Check \`summary.json\` and \`interventions.csv\` before interpreting
results. Zero accepted cases means **no supported intervention
conclusion**, not that the classifier is robust. A high rejection rate
may mean limited tests, invalid edits or an unavailable sandbox. Do
not silently delete rejected rows.

### Commit intervention artifacts

After validating the generated CSV output:

\`\`\`bash
git add -f research/experiments/rq2_interventions_smoke_001/
git add -f research/experiments/rq2_interventions_full_001/
git diff --cached --name-only
git commit -m "Add RQ2 source intervention artifacts"
git push origin feat/rq2-bytecode-explanation-validation-20261103
\`\`\`

## What this experiment can and cannot close

- Intervention experiments can give bounded **source-edit sensitivity**
  evidence when a real network-isolated sandbox runs and both original
  and edited programs pass the same task tests.
- The experiment cannot recover missing correctness scores for the other programs,
  establish general semantic equivalence on all inputs, or prove the
  originating LLM's internal implementation rationale.
