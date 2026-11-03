"""
Analyzes the bytecode length distribution of all generated Python solution
files, using the same extraction logic as bytecode_utils.py.

Helps determine a reasonable fixed-length cutoff for the feature vector.
"""

from pathlib import Path
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR    = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"  # ← update to your path
PROMPTS_DIR = BASE_DIR / "prompts"

sys.path.insert(0, str(BASE_DIR / "scripts"))
from bytecode_utils import extract_script_bytecode


def load_target_function(py_file: Path) -> str | None:
    task      = py_file.stem.split("_")[0]
    meta_file = PROMPTS_DIR / task / "meta.json"
    if not meta_file.exists():
        return None
    return json.loads(meta_file.read_text(encoding="utf-8"))["function_name"]


def main():
    py_files = sorted(OUTPUTS_DIR.rglob("*.py"))
    if not py_files:
        print(f"No Python files found in {OUTPUTS_DIR}")
        return

    sizes = []
    failed = 0

    for py_file in py_files:
        target_fn = load_target_function(py_file)
        try:
            byte_values, _ = extract_script_bytecode(py_file, target_fn)
            sizes.append(len(byte_values))
            print(f"{py_file.name:50s} → {len(byte_values)} bytes")
        except Exception as e:
            print(f"FAILED: {py_file.name}: {e}")
            failed += 1

    if not sizes:
        print("No files processed successfully.")
        return

    sizes = np.array(sizes)

    print("\n" + "=" * 60)
    print("BYTECODE LENGTH STATISTICS")
    print("=" * 60)
    print(f"Files analyzed:  {len(sizes)}  ({failed} failed)")
    print(f"Min:             {sizes.min()}")
    print(f"Max:             {sizes.max()}")
    print(f"Mean:            {sizes.mean():.1f}")
    print(f"Median:          {np.median(sizes):.1f}")
    print(f"90th percentile: {np.percentile(sizes, 90):.1f}")
    print(f"95th percentile: {np.percentile(sizes, 95):.1f}")
    print(f"99th percentile: {np.percentile(sizes, 99):.1f}")

    # how much data is retained at various cutoffs
    print("\n--- Coverage at different cutoffs ---")
    for cutoff in [128, 192, 256, 320, 384, 512]:
        pct = (sizes <= cutoff).mean()
        print(f"  cutoff={cutoff:4d}: {pct:.1%} of files fully retained")

    # ── plot ──────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("white")

    ax.hist(sizes, bins=40, color="#5b8dd9", alpha=0.85, edgecolor="white")

    # mark percentile lines
    for pct, label, color in [
        (90, "p90", "#f28e2b"),
        (95, "p95", "#e15759"),
        (99, "p99", "#b07aa1"),
    ]:
        val = np.percentile(sizes, pct)
        ax.axvline(val, color=color, linewidth=1.5,
                   linestyle="--", label=f"{label} = {val:.0f}")

    ax.axvline(sizes.mean(), color="#5cb85c", linewidth=1.5,
               linestyle="-", label=f"mean = {sizes.mean():.0f}")
    ax.axvline(np.median(sizes), color="#e05c5c", linewidth=1.5,
               linestyle="-", label=f"median = {np.median(sizes):.0f}")
    ax.set_xlabel("Bytecode length (bytes)", fontsize=11)
    ax.set_ylabel("Number of files",         fontsize=11)
    ax.set_title("Distribution of extracted bytecode lengths\n"
                 "(using same extraction logic as training pipeline)",
                 fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=9, framealpha=0.8, edgecolor="#cccccc")

    plt.tight_layout()
    plt.savefig(BASE_DIR / "analysis" / "bytecode_length_distribution.png",
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.show()
    print("\nSaved bytecode_length_distribution.png")


if __name__ == "__main__":
    main()
