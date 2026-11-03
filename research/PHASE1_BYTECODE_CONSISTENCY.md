# Phase 1: bytecode representation and trace consistency

This branch isolates corrections to the existing positional bytecode analysis without
changing the model architecture, generation prompts, historical metrics, or the
underlying definition of the extracted feature values.

## What the model actually receives

Each disassembled instruction contributes **two numeric features** in the
original extractor: the opcode integer and the *decoded integer argument*
(or 0 for absent arguments). Instruction caches are excluded. These are
`byte_0`, `byte_1`, etc. by historical convention, but they are not raw
`co_code` bytes or necessarily disassembly offsets. The feature count is
the number of flattened numeric positions, not the number of instructions.

The Python interpreter version is recorded with new extracted rows. Python
opcodes are version-dependent; only compare feature values produced under a
consistent interpreter version. The current change does **not** migrate or
regenerate the previously committed CSVs.

## Canonical source-to-position mapping

`instruction_trace_from_file(path, target_function)` lives in
`research/scripts/bytecode_utils.py`. It:

- extracts and AST-normalizes source using the exact existing preprocessor;
- compiles and walks the target function first, followed by other top-level
  functions in sorted order, recursively processing nested code objects;
- records the constructed opcode position, argument position, decoded
  argument, bytecode disassembly offset, and normalized-source line; and
- compares its flattened numeric sequence with the existing extractor,
  raising an error if they differ.

Source lines from the trace correspond to the **AST-normalized compiled
source**, not necessarily the original generated source's line numbers.
Do not use a normalized line number to highlight the raw source file without
an independently validated mapping.

The following scripts use this same trace API:
`show_bytecode.py`, `backtrack_table.py`, `byte_n_opcode_summary.py`,
`byte_value_scan.py` and `from_source_to_byte.py`. Other exploratory scripts
may still contain legacy tracing logic and should be migrated before relying
on their mappings for publication.

## Feature-schema guardrails

- `preprocess_features.py` retains `file_name` as an audit-only metadata
  column, excludes all other metadata, and admits only contiguous numeric
  `byte_0...byte_N` features as predictors.
- `preprocess_single_file()` refuses to fabricate missing values.
  For **sparse feature selections**, callers must pass the original
  `representation_length`. For a full contiguous schema, the length can be
  inferred.
- `train_bytecode_model.py` refuses unmatched feature sets, nulls,
  non-byte predictors, and overlapping task IDs between train and test.
- The ad-hoc `debug_single_file.csv` side effect was removed from prediction
  preprocessing.

These changes intentionally **fail closed** when input data cannot be
reconstructed faithfully. They may expose assumptions in old one-off scripts.

## Regression tests

Run from the repository root:

```bash
python -m pip install pandas
python -m unittest discover -s research/tests -v
```

A GitHub Actions workflow also tests the shared representation and
preprocessing on CPython 3.11 and 3.13.

## How to check the historical study

1. Preserve a snapshot of the original 1,316 features and saved XGBoost model.
2. Run the tests and verify the interpreter version used in the published data.
3. Reproduce the existing model predictions without regenerating features.
4. For representative files, compare `byte_14` and `byte_16` against
   `instruction_trace_from_file()`.
5. Only then regenerate datasets or revise published figures, in a new,
   versioned experiment. Do not silently overwrite the original artifacts.

## Not covered in Phase 1

This change does **not** establish model generalization, validate 42.59%
accuracy, run nested grouped cross-validation, establish SHAP faithfulness,
or execute the original LLM generation pipeline. Those are later phases.
