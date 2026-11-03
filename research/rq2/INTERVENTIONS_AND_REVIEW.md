# RQ2 final focused validation: source interventions and independent review

These are *new* reviewer-facing experiments, separate from the existing
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
python -m unittest discover -s research/tests -p 'test_rq2_interventions_review.py' -v
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

### B. Two independently assessed source-level explanations

\`human_review.py\` selects up to 36 cases from the previously committed
held-out source evidence and generates:

- \`private_case_key.csv\`: **keep hidden** until after both reviewers
  submit; contains true generating model, predicted model, explained
  class and evidence contribution.
- \`reviewer_A.csv\`: blank first review sheet, without class or
  generating-model columns.
- \`reviewer_B.csv\`: independent blank review sheet, likewise blinded.
- \`instructions.json\`: five allowed interpretation labels and rubric.

Create sheets:

\`\`\`bash
python research/rq2/human_review.py --prepare \
  --source-evidence research/experiments/rq2_opcode_full_001/source_evidence.json \
  --max-cases 36 \
  --output-dir research/experiments/rq2_human_review_001
\`\`\`

Give the two reviewers their sheets separately. Each should fill in
\`interpretation_label\`, \`interpretation_reason\`, and
\`confidence_1_to_5\` for every case; keep IDs and other columns
unchanged. Reviewers should not inspect each other's sheets or the
private key before finalization.

Categories:

- \`syntactic_structure\`
- \`implementation_strategy\`
- \`size_or_documentation\`
- \`generic_python_opcode\`
- \`unclear\`

After two genuinely independent human assessments have been returned,
run:

\`\`\`bash
python research/rq2/human_review.py --adjudicate \
  --review-dir research/experiments/rq2_human_review_001 \
  --output-dir research/experiments/rq2_human_agreement_001
\`\`\`

The script refuses missing labels/reasons/confidences and case-ID
mismatches, then writes the \`adjudication_queue.csv\` with agreements
pre-filled and disagreements left blank for a real adjudicator, plus
\`review_agreement.json\` with exact agreement and Cohen's kappa.
A kappa value can be undefined (stored as JSON null) when labels
have no variability.

**Do not invent ratings or treat automated labels as independent
human review.** Agreement is a reliability measure of these selected
cases, not proof of LLM generation causality.

### Commit reviewed artifacts

Only after you confirm that the CSVs contain no sensitive data,
unintended source material or human names:

\`\`\`bash
git add -f research/experiments/rq2_interventions_smoke_001/
git add -f research/experiments/rq2_interventions_full_001/
git add -f research/experiments/rq2_human_review_001/
# After real review is complete:
# git add -f research/experiments/rq2_human_agreement_001/
git diff --cached --name-only
git commit -m "Add RQ2 intervention and independent-review artifacts"
git push origin feat/rq2-bytecode-explanation-validation-20261103
\`\`\`

For blinded assessment, **do not make \`private_case_key.csv\` public
before both reviewers complete their sheets**. This repository may be
public; preferably share blinded sheets privately and only commit the
case key and final agreement after review/adjudication is finished.

## What these experiments can and cannot close

- Intervention experiments can give bounded **source-edit sensitivity**
  evidence when a real network-isolated sandbox runs and both original
  and edited programs pass the same task tests.
- Independent human reviews can provide evidence on **interpretation
  consistency** and disagreement patterns.
- They cannot recover missing correctness scores for the other programs,
  establish general semantic equivalence on all inputs, or prove the
  originating LLM's internal implementation rationale.
