"""
check_all_bytes_accuracy.py

For each byte feature and each test file, checks whether that byte's
SHAP contribution alone (the class with the highest SHAP value for
that byte) matches the true model label. Ranks all byte features by
this "standalone accuracy", reports the top N with per-model breakdown,
and compares aggregate statistics between even (opcode) and odd
(argument) byte positions.

Run from project root:
    python scripts/check_all_bytes_accuracy.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR     = Path(__file__).resolve().parent.parent
SHAP_DIR     = BASE_DIR / "shap_bytecode"
TEST_FEATURES = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"

SHAP_VALUES_TEST_FILE = SHAP_DIR / "shap_values_multiclass_test.npy"
FEATURE_NAMES_FILE    = SHAP_DIR / "feature_names.json"
CLASS_NAMES_FILE      = SHAP_DIR / "class_names.json"

# ── how many top bytes to show ────────────────────────────────────────────
TOP_N = 10


def get_class_shap_values(shap_values, class_index: int):
    if isinstance(shap_values, list):
        return shap_values[class_index]
    if isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        return shap_values[:, :, class_index]
    raise ValueError(f"Unexpected SHAP values shape/type: {type(shap_values)}")


def main():
    shap_values = np.load(SHAP_VALUES_TEST_FILE, allow_pickle=True)
    if isinstance(shap_values, np.ndarray) and shap_values.dtype == object and shap_values.shape == ():
        shap_values = shap_values.item()

    feature_names = json.loads(FEATURE_NAMES_FILE.read_text(encoding="utf-8"))
    class_names   = json.loads(CLASS_NAMES_FILE.read_text(encoding="utf-8"))

    test_df = pd.read_csv(TEST_FEATURES)
    y_true  = np.array(test_df["model"].values)

    n_files   = len(y_true)
    n_classes = len(class_names)

    all_class_shap = np.stack(
        [get_class_shap_values(shap_values, ci) for ci in range(n_classes)],
        axis=0
    )  # (n_classes, n_files, n_features)

    results = []
    for feat_idx, feat in enumerate(feature_names):
        if not feat.startswith("byte_"):
            continue

        byte_idx = int(feat.replace("byte_", ""))

        feat_shap = all_class_shap[:, :, feat_idx].T  # (n_files, n_classes)
        argmax_class_idx = feat_shap.argmax(axis=1)
        predicted = np.array([class_names[i] for i in argmax_class_idx])

        correct = predicted == y_true
        pct_correct = 100 * correct.sum() / n_files

        results.append((feat, byte_idx, correct, pct_correct))

    results.sort(key=lambda r: r[3], reverse=True)

    print(f"Test files: {n_files}")
    print(f"Total byte features evaluated: {len(results)}\n")
    print(f"Top {TOP_N} byte positions by standalone SHAP-argmax accuracy:")

    for feat, byte_idx, correct, pct in results[:TOP_N]:
        print(f"\n{feat}  (overall: {correct.sum()}/{n_files} = {pct:.2f}%)")
        for cls in class_names:
            mask = y_true == cls
            n_cls = mask.sum()
            if n_cls == 0:
                continue
            n_correct_cls = correct[mask].sum()
            print(f"    {cls:10s}: {n_correct_cls}/{n_cls} "
                  f"({100 * n_correct_cls / n_cls:.2f}%)")

    # ── even (opcode) vs odd (argument) comparison ─────────────────────────
    even_pcts = [pct for _, byte_idx, _, pct in results if byte_idx % 2 == 0]
    odd_pcts  = [pct for _, byte_idx, _, pct in results if byte_idx % 2 == 1]

    print("\n" + "=" * 50)
    print("Even (opcode) vs odd (argument) byte positions")
    print("=" * 50)
    print(f"\nEven (opcode) positions:   n={len(even_pcts)}")
    print(f"  mean accuracy:   {np.mean(even_pcts):.2f}%")
    print(f"  median accuracy: {np.median(even_pcts):.2f}%")
    print(f"  max accuracy:    {np.max(even_pcts):.2f}%")
    print(f"  min accuracy:    {np.min(even_pcts):.2f}%")

    print(f"\nOdd (argument) positions:  n={len(odd_pcts)}")
    print(f"  mean accuracy:   {np.mean(odd_pcts):.2f}%")
    print(f"  median accuracy: {np.median(odd_pcts):.2f}%")
    print(f"  max accuracy:    {np.max(odd_pcts):.2f}%")
    print(f"  min accuracy:    {np.min(odd_pcts):.2f}%")

    # how many of each are above chance (33.3%)?
    chance = 100 / n_classes
    even_above = sum(1 for p in even_pcts if p > chance)
    odd_above  = sum(1 for p in odd_pcts if p > chance)
    print(f"\nPositions above chance ({chance:.1f}%):")
    print(f"  even (opcode):   {even_above}/{len(even_pcts)}")
    print(f"  odd (argument):  {odd_above}/{len(odd_pcts)}")


if __name__ == "__main__":
    main()
