"""
plot_byte_shap_scatter.py

For each selected byte position, plots:
  - X axis: raw byte value
  - Y axis: SHAP value for each class
  - Color: true model label
  - One subplot per class

Run from project root:
    python scripts/plot_byte_shap_scatter.py
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import opcode as opcode_module

BASE_DIR     = Path(__file__).resolve().parent.parent
SHAP_DIR     = BASE_DIR / "shap_bytecode"
TRAIN_FEATURES_CSV = BASE_DIR / "features" / "processed_bytecode_features.csv"
TEST_FEATURES_CSV  = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
OUT_DIR      = BASE_DIR / "shap_bytecode" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / "scripts"))

COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
CLASS_NAMES = ["llama", "mistral", "qwen"]

# ── byte selection ──────────────────────────────────────────────────────
# Set to "top_n" to select the top N even-indexed bytes by global mean |SHAP|.
# Set to "manual" to use the explicit BYTE_SELECTION list below.
SELECTION_MODE = "manual"   # "top_n" or "manual"

TOP_N_BYTES = 4    # used when SELECTION_MODE == "top_n"

BYTE_SELECTION = ["byte_14", "byte_16", "byte_54", "byte_12"]  # used when SELECTION_MODE == "manual"

OUT_FILENAME = "byte_value_vs_shap.png"  # change if generating multiple variants

SHOW_TITLE = False  # set True to show the figure suptitle

# font sizes tuned for thesis (paper-appropriate)
FS_TITLE    = 14
FS_SUBTITLE = 16
FS_TICK     = 13
FS_LABEL    = 14
FS_YLABEL   = 14
FS_LEGEND   = 13


def opname_for(val: int) -> str:
    if val == -1:
        return "PAD"
    try:
        name = opcode_module.opname[val]
        return name if name != "<?>" else str(val)
    except Exception:
        return str(val)


def main():
    shap_path = SHAP_DIR / "shap_values_multiclass_test.npy"
    if not shap_path.exists():
        shap_path = SHAP_DIR / "shap_values_multiclass.npy"
        print("WARNING: test-only SHAP not found, falling back to combined")
    shap_values = np.load(shap_path)
    features    = json.loads((SHAP_DIR / "feature_names.json").read_text())
    class_names = json.loads((SHAP_DIR / "class_names.json").read_text())

    df = pd.read_csv(TEST_FEATURES_CSV)
    y       = df["model"].values
    feat_df = df[[c for c in df.columns if c.startswith("byte_")]]
    feat_df = feat_df[[f for f in features if f in feat_df.columns]]

    if SELECTION_MODE == "top_n":
        mean_abs    = np.abs(shap_values).mean(axis=(0, 2)) if shap_values.ndim == 3 \
                      else np.abs(shap_values).mean(axis=0)
        all_top_idx = np.argsort(mean_abs)[::-1]
        top_idx     = [i for i in all_top_idx
                       if int(features[i].replace("byte_", "")) % 2 == 0][:TOP_N_BYTES]
        top_bytes   = [features[i] for i in top_idx]
    elif SELECTION_MODE == "manual":
        top_bytes = [b for b in BYTE_SELECTION if b in features]
        missing   = [b for b in BYTE_SELECTION if b not in features]
        if missing:
            print(f"WARNING: bytes not found in features and skipped: {missing}")
    else:
        raise ValueError(f"Unknown SELECTION_MODE: {SELECTION_MODE!r}")

    n_bytes = len(top_bytes)
    print(f"Plotting bytes ({SELECTION_MODE}): {top_bytes}")

    n_rows = len(CLASS_NAMES)  # one row per class, all bytes in one row
    fig, axes = plt.subplots(
        n_rows, n_bytes,
        figsize=(n_bytes * 3.2, n_rows * 3.0),
        squeeze=False
    )
    fig.patch.set_facecolor("white")

    if SHOW_TITLE:
        fig.suptitle(
            "Byte value vs SHAP value per class\n"
            "Each point = one test file. Color = true model.",
            fontsize=FS_TITLE, y=1.02
        )

    for bi, byte_name in enumerate(top_bytes):
        if byte_name not in feat_df.columns or byte_name not in features:
            continue

        feat_col_idx = features.index(byte_name)
        raw_vals     = feat_df[byte_name].values

        for ci, cls in enumerate(CLASS_NAMES):
            ax = axes[ci][bi]
            ax.set_facecolor("#fafafa")

            if shap_values.ndim == 3:
                shap_col = shap_values[:, feat_col_idx, ci]
            else:
                shap_col = shap_values[ci][:, feat_col_idx]

            draw_order = [m for m in CLASS_NAMES if m != cls] + [cls]
            for model in draw_order:
                mask = y == model
                ax.scatter(
                    raw_vals[mask], shap_col[mask],
                    color=COLORS[model], alpha=0.7, s=18,
                    edgecolors="white", linewidths=0.3,
                    zorder=3 if model != cls else 4
                )

            ax.axhline(0, color="#888", linewidth=0.8, zorder=2)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.tick_params(labelsize=FS_TICK)
            ax.set_xlabel("raw byte value", fontsize=FS_LABEL)

            if bi == 0:
                ax.set_ylabel(f"SHAP\u2192{cls}", fontsize=FS_YLABEL,
                              color=COLORS[cls], fontweight="bold")
            if ci == 0:
                ax.set_title(byte_name, fontsize=FS_SUBTITLE, fontweight="bold")

    plt.tight_layout()

    handles = [mpatches.Patch(color=COLORS[m], label=m) for m in CLASS_NAMES]
    fig.legend(handles=handles,
               loc="upper center",
               bbox_to_anchor=(0.5, 0.0),
               ncol=len(CLASS_NAMES),
               fontsize=FS_LEGEND,
               title="true model",
               title_fontsize=FS_LEGEND,
               framealpha=0.9)

    plt.subplots_adjust(bottom=0.08)

    out_path = OUT_DIR / OUT_FILENAME
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
