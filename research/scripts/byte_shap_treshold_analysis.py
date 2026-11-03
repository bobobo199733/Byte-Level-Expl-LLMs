"""
byte_shap_cluster_analysis.py  (v3 -- edge-to-edge connecting lines)
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

BASE_DIR          = Path(__file__).resolve().parent.parent
SHAP_DIR          = BASE_DIR / "shap_bytecode"
TEST_FEATURES_CSV = BASE_DIR / "test_data" / "features" / "processed_bytecode_features.csv"
OUT_DIR           = BASE_DIR / "shap_bytecode" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR / "scripts"))

# ── configure ────────────────────────────────────────────────────────
BYTE_SELECTION = ["byte_14", "byte_16", "byte_54", "byte_28",
                  "byte_18", "byte_24", "byte_12", "byte_32"]
SHOW_TITLE     = False

DBSCAN_EPS         = 0.4
DBSCAN_MIN_SAMPLES = 3

# ── Python opcode group boundaries ───────────────────────────────────
OPCODE_BOUNDARIES = [
    (45,  "binary/build"),
    (53,  "CALL family"),
    (58,  "compare/delete/jump"),
    (82,  "LOAD_* family"),
    (97,  "POP_JUMP_IF_*"),
    (101, "raise/return/misc"),
    (108, "STORE_* family"),
    (115, "unpack/yield"),
    (149, "RESUME"),
]

COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}
CLASS_NAMES = ["llama", "mistral", "qwen"]

FS_LABEL  = 13
FS_TICK   = 12
FS_LEGEND = 11
FS_ANNOT  = 10


def nearest_boundary(x, boundaries):
    dists = [(abs(x - b), label, b) for b, label in boundaries]
    dists.sort()
    return dists[0]


def find_sign_change_threshold(x1, y1, x2, y2):
    """Linear interpolation between two points; returns x where y=0.
    Returns None if both points are on the same side of 0."""
    if y1 * y2 >= 0:
        return None
    t = -y1 / (y2 - y1)
    return x1 + t * (x2 - x1)


def cluster_edge_points(x_data, y_data, labels, k):
    """Return (x_max, mean_y_at_xmax) and (x_min, mean_y_at_xmin)
    for cluster k — the rightmost and leftmost points of the cluster."""
    mask   = labels == k
    xk     = x_data[mask]
    yk     = y_data[mask]

    x_max  = xk.max()
    x_min  = xk.min()
    y_at_xmax = yk[xk == x_max].mean()
    y_at_xmin = yk[xk == x_min].mean()

    return (x_max, y_at_xmax), (x_min, y_at_xmin)


def main():
    shap_path = SHAP_DIR / "shap_values_multiclass_test.npy"
    if not shap_path.exists():
        shap_path = SHAP_DIR / "shap_values_multiclass.npy"
        print("WARNING: test-only SHAP not found, falling back to combined")

    shap_values = np.load(shap_path)
    features    = json.loads((SHAP_DIR / "feature_names.json").read_text())

    df      = pd.read_csv(TEST_FEATURES_CSV)
    y       = df["model"].values
    feat_df = df[[c for c in df.columns if c.startswith("byte_")]]
    feat_df = feat_df[[f for f in features if f in feat_df.columns]]

    n_bytes = len(BYTE_SELECTION)
    n_cls   = len(CLASS_NAMES)

    fig, axes = plt.subplots(
        n_cls, n_bytes,
        figsize=(n_bytes * 3.8, n_cls * 3.2),
        squeeze=False,
    )
    fig.patch.set_facecolor("white")

    print("=" * 70)
    print("2D CLUSTER-BASED SHAP SIGN-CHANGE ANALYSIS (DBSCAN, edge-to-edge)")
    print("=" * 70)

    for bi, byte_name in enumerate(BYTE_SELECTION):
        if byte_name not in features:
            continue

        feat_col_idx = features.index(byte_name)
        raw_vals     = feat_df[byte_name].values

        print(f"\n{byte_name}")
        print("-" * 50)

        for ci, cls in enumerate(CLASS_NAMES):
            ax = axes[ci][bi]
            ax.set_facecolor("#fafafa")

            if shap_values.ndim == 3:
                shap_col = shap_values[:, feat_col_idx, ci]
            else:
                shap_col = shap_values[ci][:, feat_col_idx]

            # ── scatter ───────────────────────────────────────────────
            draw_order = [m for m in CLASS_NAMES if m != cls] + [cls]
            for model in draw_order:
                mask = y == model
                ax.scatter(
                    raw_vals[mask], shap_col[mask],
                    color=COLORS[model], alpha=0.45, s=14,
                    edgecolors="none",
                    zorder=3 if model != cls else 4,
                )

            # ── 2D DBSCAN ─────────────────────────────────────────────
            valid  = raw_vals != -1
            x_data = raw_vals[valid].astype(float)
            y_data = shap_col[valid]

            X2d    = np.column_stack([x_data, y_data])
            scaler = StandardScaler()
            X2d_sc = scaler.fit_transform(X2d)

            db     = DBSCAN(eps=DBSCAN_EPS,
                            min_samples=DBSCAN_MIN_SAMPLES).fit(X2d_sc)
            labels = db.labels_

            unique_labels = sorted(set(labels) - {-1})
            n_clusters    = len(unique_labels)

            # compute cluster centroids + sizes, sort by x-centroid
            cluster_info = []
            for k in unique_labels:
                mask_k = labels == k
                cx     = x_data[mask_k].mean()
                cy     = y_data[mask_k].mean()
                csize  = mask_k.sum()
                cluster_info.append((cx, cy, csize, k))
            cluster_info.sort(key=lambda r: r[0])

            # draw cluster centroids
            for cx, cy, csize, k in cluster_info:
                ax.scatter(
                    cx, cy,
                    color=COLORS[cls], s=80 + csize * 2,
                    marker="D", zorder=8,
                    edgecolors="white", linewidths=1.0,
                    alpha=0.9,
                )

            # draw edge-to-edge connecting lines between adjacent clusters
            for i in range(len(cluster_info) - 1):
                _, _, _, k1 = cluster_info[i]
                _, _, _, k2 = cluster_info[i + 1]

                (x_end,   y_end),   _ = cluster_edge_points(
                    x_data, y_data, labels, k1)
                _,   (x_start, y_start) = cluster_edge_points(
                    x_data, y_data, labels, k2)

                # connecting line from right edge of cluster i
                # to left edge of cluster i+1
                ax.plot([x_end, x_start], [y_end, y_start],
                        color=COLORS[cls], linewidth=1.8,
                        alpha=0.85, zorder=6, linestyle="-")

                # sign change along the connecting line
                threshold = find_sign_change_threshold(
                    x_end, y_end, x_start, y_start)
                if threshold is None:
                    continue

                ax.axvline(threshold, color=COLORS[cls],
                           linewidth=1.5, linestyle="--",
                           alpha=0.9, zorder=7)
                ax.text(threshold + 1.5, 0,
                        f"{threshold:.0f}",
                        fontsize=FS_ANNOT, color=COLORS[cls],
                        va="bottom", ha="left", fontweight="bold")

                dist, blabel, bx = nearest_boundary(
                    threshold, OPCODE_BOUNDARIES)
                aligned = "✓ ALIGNED" if dist <= 6 else \
                          f"  (off by {dist:.1f})"
                print(f"  SHAP→{cls:8s}: sign change at {threshold:6.1f}  "
                      f"({y_end:+.3f} → {y_start:+.3f})  "
                      f"nearest boundary: {bx} '{blabel}'  {aligned}")

            # draw noise points faded
            valid_indices  = np.where(valid)[0]
            noise_in_valid = labels == -1
            if noise_in_valid.sum() > 0:
                noise_indices = valid_indices[noise_in_valid]
                ax.scatter(
                    raw_vals[noise_indices], shap_col[noise_indices],
                    color="#cccccc", alpha=0.3, s=10,
                    edgecolors="none", zorder=2,
                )

            if n_clusters == 0:
                print(f"  SHAP→{cls:8s}: no clusters found")

            # ── opcode boundaries ─────────────────────────────────────
            for bx, blabel in OPCODE_BOUNDARIES:
                if x_data.min() <= bx <= x_data.max():
                    ax.axvline(bx, color="#cccccc", linewidth=0.8,
                               linestyle="--", alpha=0.5, zorder=2)

            # ── formatting ────────────────────────────────────────────
            ax.axhline(0, color="#555", linewidth=0.9, zorder=3)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.tick_params(labelsize=FS_TICK)
            ax.set_xlabel("raw byte value", fontsize=FS_LABEL)
            if bi == 0:
                ax.set_ylabel(f"SHAP\u2192{cls}",
                              fontsize=FS_LABEL,
                              color=COLORS[cls],
                              fontweight="bold")
            if ci == 0:
                ax.set_title(byte_name, fontsize=FS_LABEL + 2,
                             fontweight="bold")

    # ── legend ────────────────────────────────────────────────────────
    model_handles = [mpatches.Patch(color=COLORS[m], label=m)
                     for m in CLASS_NAMES]
    boundary_h = plt.Line2D([0], [0], color="#cccccc",
                             linewidth=0.8, linestyle="--",
                             label="opcode group boundary")
    change_h   = plt.Line2D([0], [0], color="#888888",
                             linewidth=1.5, linestyle="--",
                             label="SHAP sign change")
    cluster_h  = plt.Line2D([0], [0], color="#888888",
                             linewidth=0, marker="D", markersize=6,
                             label="cluster centroid")
    fig.legend(
        handles=model_handles + [boundary_h, change_h, cluster_h],
        loc="upper center",
        bbox_to_anchor=(0.5, 0.0),
        ncol=len(CLASS_NAMES) + 3,
        fontsize=FS_LEGEND,
        framealpha=0.9,
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    out_path = OUT_DIR / "byte_shap_cluster_analysis.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
