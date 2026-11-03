"""
For each task, takes the top-N most influential byte positions from SHAP,
then traces each position back to the actual Python bytecode instruction
it corresponds to in each file, grouped by model.

Requires bytecode_utils.py to be importable (same scripts/ folder).
"""
from pathlib import Path
import json
import sys
import dis
import types
import re
import ast
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ══════════════════════════════════════════════════════════════════════════════
# ── config ────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

TASK_ID      = os.environ.get("TASK_ID", "t44")
TOP_N_BYTES  = 10
USE_CATEGORIES = True  # set to False to show raw opnames

BASE_DIR     = Path(__file__).resolve().parent.parent
PROMPTS_DIR  = BASE_DIR / "test_data" / "prompts"
REPORT_FILE  = BASE_DIR / "models" / "bytecode_llm_classifier_report.json"
ANALYSIS_DIR = BASE_DIR / "analysis" / TASK_ID
OUT_DIR      = BASE_DIR / "analysis" / TASK_ID / "byte_traces"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["llama", "mistral", "qwen"]
COLORS      = {"llama": "#e05c5c", "mistral": "#5cb85c", "qwen": "#5b8dd9"}

# ── opcode categories ─────────────────────────────────────────────────────────
OPCODE_CATEGORIES = {
    # Stack — Load
    "LOAD_FAST": "Stack: Load", "LOAD_CONST": "Stack: Load",
    "LOAD_GLOBAL": "Stack: Load", "LOAD_DEREF": "Stack: Load",
    "LOAD_ATTR": "Stack: Load", "LOAD_NAME": "Stack: Load",
    "LOAD_FAST_LOAD_FAST": "Stack: Load", "LOAD_CLASSDEREF": "Stack: Load",
    # Stack — Store
    "STORE_FAST": "Stack: Store", "STORE_NAME": "Stack: Store",
    "STORE_ATTR": "Stack: Store", "STORE_DEREF": "Stack: Store",
    "STORE_SUBSCR": "Stack: Store", "STORE_FAST_STORE_FAST": "Stack: Store",
    # Stack — Other
    "POP_TOP": "Stack: Other", "COPY": "Stack: Other",
    "SWAP": "Stack: Other", "PUSH_NULL": "Stack: Other",
    "PUSH_EXC_INFO": "Stack: Other", "DUP_TOP": "Stack: Other",
    # Arithmetic & Comparison
    "BINARY_OP": "Arithmetic/Compare", "COMPARE_OP": "Arithmetic/Compare",
    "BINARY_SUBSCR": "Arithmetic/Compare", "BINARY_SLICE": "Arithmetic/Compare",
    "CONTAINS_OP": "Arithmetic/Compare", "IS_OP": "Arithmetic/Compare",
    "UNARY_NEGATIVE": "Arithmetic/Compare", "UNARY_NOT": "Arithmetic/Compare",
    "UNARY_INVERT": "Arithmetic/Compare",
    # Control Flow
    "JUMP_FORWARD": "Control Flow", "JUMP_BACKWARD": "Control Flow",
    "POP_JUMP_IF_TRUE": "Control Flow", "POP_JUMP_IF_FALSE": "Control Flow",
    "POP_JUMP_IF_NONE": "Control Flow", "POP_JUMP_IF_NOT_NONE": "Control Flow",
    "JUMP_IF_TRUE_OR_POP": "Control Flow", "JUMP_IF_FALSE_OR_POP": "Control Flow",
    "FOR_ITER": "Control Flow", "GET_ITER": "Control Flow",
    "JUMP_BACKWARD_NO_INTERRUPT": "Control Flow",
    # Function Calls
    "CALL": "Function Call", "CALL_FUNCTION_EX": "Function Call",
    "CALL_INTRINSIC_1": "Function Call",
    "RETURN_VALUE": "Function Call", "RETURN_CONST": "Function Call",
    "YIELD_VALUE": "Function Call", "SEND": "Function Call",
    # Function Definition
    "MAKE_FUNCTION": "Function Definition", "MAKE_CELL": "Function Definition",
    "COPY_FREE_VARS": "Function Definition", "SET_FUNCTION_ATTRIBUTE": "Function Definition",
    # Data Structures
    "BUILD_LIST": "Data Structures", "BUILD_DICT": "Data Structures",
    "BUILD_TUPLE": "Data Structures", "BUILD_SET": "Data Structures",
    "BUILD_SLICE": "Data Structures", "BUILD_STRING": "Data Structures",
    "LIST_APPEND": "Data Structures", "SET_ADD": "Data Structures",
    "DICT_UPDATE": "Data Structures", "LIST_EXTEND": "Data Structures",
    "DICT_MERGE": "Data Structures",
    # Imports
    "IMPORT_NAME": "Import", "IMPORT_FROM": "Import", "IMPORT_STAR": "Import",
    # Exception Handling
    "SETUP_FINALLY": "Exception", "POP_EXCEPT": "Exception",
    "RAISE_VARARGS": "Exception", "RERAISE": "Exception",
    "CHECK_EXC_MATCH": "Exception",
    # Misc
    "CACHE": "CACHE", "RESUME": "Misc", "NOP": "Misc",
    "END_FOR": "Misc", "END_SEND": "Misc", "TO_BOOL": "Misc",
}

CATEGORY_COLORS = {
    "Stack: Load":         "#4e79a7",
    "Stack: Store":        "#f28e2b",
    "Stack: Other":        "#aecde8",
    "Arithmetic/Compare":  "#e15759",
    "Control Flow":        "#76b7b2",
    "Function Call":       "#59a14f",
    "Function Definition": "#edc948",
    "Data Structures":     "#b07aa1",
    "Import":              "#ff9da7",
    "Exception":           "#9c755f",
    "CACHE":               "#cccccc",
    "Misc":                "#bab0ac",
    "Other":               "#dddddd",
}

def to_category(opname: str) -> str:
    return OPCODE_CATEGORIES.get(opname, "Other")


sys.path.insert(0, str(BASE_DIR / "scripts"))
from bytecode_utils import (
    extract_code,
    keep_only_defs,
    get_top_level_code_objects,
    collect_ordered_script_bytes,
)


# ══════════════════════════════════════════════════════════════════════════════
# helpers
# ══════════════════════════════════════════════════════════════════════════════

def load_target_function() -> str:
    meta = json.loads((PROMPTS_DIR / TASK_ID / "meta.json").read_text(encoding="utf-8"))
    return meta["function_name"]


def load_report():
    return json.loads(REPORT_FILE.read_text(encoding="utf-8"))


def get_top_bytes_for_task() -> list[int]:
    files = sorted(ANALYSIS_DIR.glob("*_effects.csv"))
    if not files:
        raise FileNotFoundError(f"No effects CSVs found in {ANALYSIS_DIR}")
    dfs = [pd.read_csv(f) for f in files]
    all_effects = pd.concat(dfs, ignore_index=True)
    top = (all_effects.groupby("byte_index")["magnitude"]
           .mean().nlargest(TOP_N_BYTES).index.tolist())
    return sorted(top)


def find_task_files() -> list[Path]:
    candidates = [
        BASE_DIR / "test_data" / "generated",
        BASE_DIR / "test_data" / "scripts",
        BASE_DIR / "data" / "generated",
        BASE_DIR / "generated",
        BASE_DIR / "scripts",
    ]
    found = []
    for d in candidates:
        if d.exists():
            found.extend(sorted(d.glob(f"{TASK_ID}_*.py")))
    if not found:
        found = sorted(BASE_DIR.rglob(f"{TASK_ID}_p*_r*_*.py"))
    return found


# ══════════════════════════════════════════════════════════════════════════════
# bytecode disassembly
# ══════════════════════════════════════════════════════════════════════════════

def get_flat_instructions(py_file: Path, target_function: str) -> list[dict]:
    raw  = py_file.read_text(encoding="utf-8")
    code = extract_code(raw)
    code = keep_only_defs(code)

    compiled = compile(code, filename=str(py_file), mode="exec")
    byte_values, _ = collect_ordered_script_bytes(compiled, target_function)

    top_level = get_top_level_code_objects(compiled)

    ordered_code_objects = []
    if target_function in top_level:
        ordered_code_objects.append(top_level[target_function])
    for name in sorted(top_level.keys()):
        if name != target_function:
            ordered_code_objects.append(top_level[name])

    def collect_code_objects_recursive(code_obj) -> list[types.CodeType]:
        result = [code_obj]
        for const in code_obj.co_consts:
            if isinstance(const, types.CodeType):
                result.extend(collect_code_objects_recursive(const))
        return result

    all_code_objects = []
    for co in ordered_code_objects:
        all_code_objects.extend(collect_code_objects_recursive(co))

    instructions = []
    pos = 0
    for co in all_code_objects:
        for instr in dis.get_instructions(co):
            instructions.append({
                "position":  pos,
                "opcode":    instr.opcode,
                "opname":    instr.opname,
                "arg":       instr.arg,
                "argval":    str(instr.argval),
                "code_name": co.co_name,
            })
            pos += 2

    return instructions, byte_values


def get_instruction_at_position(instructions: list[dict], position: int) -> dict | None:
    instr_index = position // 2
    if instr_index >= len(instructions):
        return None
    instr = instructions[instr_index].copy()
    instr["byte_role"]  = "opcode" if position % 2 == 0 else "arg"
    instr["byte_value"] = instr["opcode"] if position % 2 == 0 else instr["arg"]
    return instr


# ══════════════════════════════════════════════════════════════════════════════
# main analysis
# ══════════════════════════════════════════════════════════════════════════════

def analyze_bytes():
    target_fn = load_target_function()
    top_bytes = get_top_bytes_for_task()
    files     = find_task_files()

    print(f"\nTask: {TASK_ID}  |  target: {target_fn}")
    print(f"Top {TOP_N_BYTES} bytes to trace: {top_bytes}")
    print(f"Files: {len(files)}")

    rows = []
    for py_file in files:
        parts      = py_file.stem.split("_")
        true_model = parts[-1]
        prompt_id  = parts[1] if len(parts) > 1 else "?"
        run_id     = parts[2] if len(parts) > 2 else "?"

        try:
            instructions, byte_values = get_flat_instructions(py_file, target_fn)
        except Exception as e:
            print(f"  ERROR {py_file.name}: {e}")
            continue

        for byte_pos in top_bytes:
            instr = get_instruction_at_position(instructions, byte_pos)
            if instr is None:
                opname    = "OUT_OF_RANGE"
                arg       = -1
                role      = "?"
                argval    = "?"
                code_name = "?"
                raw_value = -1
            else:
                opname    = instr["opname"]
                arg       = instr["arg"]
                role      = instr["byte_role"]
                argval    = instr["argval"]
                code_name = instr["code_name"]
                raw_value = byte_values[byte_pos] if byte_pos < len(byte_values) else -1

            rows.append({
                "file":       py_file.name,
                "true_model": true_model,
                "prompt":     prompt_id,
                "run":        run_id,
                "byte_pos":   byte_pos,
                "byte_role":  role,
                "raw_value":  raw_value,
                "opname":     opname,
                "arg":        arg,
                "argval":     argval,
                "code_name":  code_name,
            })

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "byte_trace_raw.csv", index=False)
    print(f"\nSaved byte_trace_raw.csv ({len(df)} rows)")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# print summary
# ══════════════════════════════════════════════════════════════════════════════

def print_byte_summary(df: pd.DataFrame):
    print("\n" + "="*70)
    print(f"BYTE TRACE SUMMARY — {TASK_ID}")
    print("="*70)

    for byte_pos in sorted(df["byte_pos"].unique()):
        sub  = df[df["byte_pos"] == byte_pos]
        role = sub["byte_role"].mode()[0]
        print(f"\nbyte_{byte_pos} ({role}):")

        for model in CLASS_NAMES:
            msub = sub[sub["true_model"] == model]
            if msub.empty:
                continue
            counts = msub["opname"].value_counts()
            top    = counts.index[0]
            pct    = counts.iloc[0] / len(msub)
            others = ", ".join(f"{k}({v})" for k, v in counts.items() if k != top)
            print(f"  {model:8s}: {top} ({pct:.0%})"
                  + (f"  also: {others}" if others else ""))

        model_modes = {m: sub[sub["true_model"] == m]["opname"].mode()
                       for m in CLASS_NAMES}
        model_modes = {m: v[0] if len(v) else "?" for m, v in model_modes.items()}
        unique_ops  = set(model_modes.values())
        if len(unique_ops) > 1:
            print(f"  *** MODELS DIFFER: {model_modes}")
        else:
            print(f"  (all models: {list(unique_ops)[0]})")


# ══════════════════════════════════════════════════════════════════════════════
# plots
# ══════════════════════════════════════════════════════════════════════════════

def plot_opname_distribution(df: pd.DataFrame):
    top_bytes = sorted(df["byte_pos"].unique())
    n = len(top_bytes)

    n_cols = (n + 1) // 2
    n_rows = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2.5, 10))
    axes = axes.flatten()

    mode_str = "categories" if USE_CATEGORIES else "opnames"
    fig.suptitle(f"{TASK_ID} — instruction at each top SHAP byte position, by model ({mode_str})",
                 fontsize=11)

    for i, (ax, byte_pos) in enumerate(zip(axes, top_bytes)):
        sub = df[(df["byte_pos"] == byte_pos) & (df["opname"] != "OUT_OF_RANGE")].copy()
        if sub.empty:
            ax.set_visible(False)
            continue

        role = sub["byte_role"].mode()[0]

        if USE_CATEGORIES:
            sub["display"] = sub["opname"].apply(to_category)
            color_map = CATEGORY_COLORS
        else:
            sub["display"] = sub["opname"]
            all_ops   = sub["opname"].unique()
            op_colors = plt.cm.tab20(np.linspace(0, 1, len(all_ops)))
            color_map = dict(zip(all_ops, op_colors))

        all_display = sub["display"].unique()
        bottoms = np.zeros(len(CLASS_NAMES))
        x       = np.arange(len(CLASS_NAMES))

        for op in all_display:
            heights = []
            for model in CLASS_NAMES:
                msub = sub[sub["true_model"] == model]
                pct  = (msub["display"] == op).mean() if len(msub) else 0
                heights.append(pct)
            ax.bar(x, heights, bottom=bottoms, label=op,
                   color=color_map.get(op, "#dddddd"), alpha=0.85)
            bottoms += np.array(heights)

        ax.set_xticks(x)
        ax.set_xticklabels(CLASS_NAMES, fontsize=8, rotation=30)
        ax.set_title(f"byte_{byte_pos}\n({role})", fontsize=8)
        ax.set_ylim(0, 1.05)
        if i % n_cols == 0:
            ax.set_ylabel("fraction of files")

        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(handles, labels, fontsize=5, loc="upper right",
                      framealpha=0.7)

    for i in range(len(top_bytes), len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()
    out_name = f"opname_distribution_{mode_str}.png"
    plt.savefig(OUT_DIR / out_name, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_name}")


def plot_raw_value_distribution(df: pd.DataFrame):
    top_bytes = sorted(df["byte_pos"].unique())
    n = len(top_bytes)

    fig, axes = plt.subplots(1, n, figsize=(n * 2.2, 4), sharey=False)
    if n == 1:
        axes = [axes]

    fig.suptitle(f"{TASK_ID} — raw byte value distribution per model", fontsize=11)

    for ax, byte_pos in zip(axes, top_bytes):
        sub  = df[df["byte_pos"] == byte_pos]
        data = [sub[(sub["true_model"] == m) & (sub["raw_value"] != -1)]["raw_value"].values
                for m in CLASS_NAMES]
        bp = ax.boxplot(data, patch_artist=True, widths=0.5)
        for patch, model in zip(bp["boxes"], CLASS_NAMES):
            patch.set_facecolor(COLORS[model])
            patch.set_alpha(0.7)
        ax.set_xticks(range(1, len(CLASS_NAMES) + 1))
        ax.set_xticklabels(CLASS_NAMES, fontsize=7, rotation=30)
        ax.set_title(f"byte_{byte_pos}", fontsize=8)
        if ax == axes[0]:
            ax.set_ylabel("raw byte value")

    plt.tight_layout()
    plt.savefig(OUT_DIR / "raw_value_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved raw_value_distribution.png")


def plot_model_divergence_heatmap(df: pd.DataFrame):
    top_bytes   = sorted(df["byte_pos"].unique())
    model_pairs = [("llama", "mistral"), ("llama", "qwen"), ("mistral", "qwen")]
    pair_labels = ["llama vs\nmistral", "llama vs\nqwen", "mistral vs\nqwen"]

    matrix = np.zeros((len(top_bytes), len(model_pairs)))

    for bi, byte_pos in enumerate(top_bytes):
        sub = df[df["byte_pos"] == byte_pos]
        for pi, (m1, m2) in enumerate(model_pairs):
            s1 = sub[sub["true_model"] == m1].set_index(["prompt", "run"])["opname"]
            s2 = sub[sub["true_model"] == m2].set_index(["prompt", "run"])["opname"]
            common = s1.index.intersection(s2.index)
            if len(common) == 0:
                matrix[bi, pi] = 0
                continue
            matrix[bi, pi] = (s1.loc[common] != s2.loc[common]).mean()

    fig, ax = plt.subplots(figsize=(6, max(4, len(top_bytes) * 0.5)))
    im = ax.imshow(matrix, aspect="auto", cmap="Reds", vmin=0, vmax=1)

    ax.set_xticks(range(len(model_pairs)))
    ax.set_xticklabels(pair_labels, fontsize=9)
    ax.set_yticks(range(len(top_bytes)))
    ax.set_yticklabels([f"byte_{b}" for b in top_bytes], fontsize=8)
    ax.set_title(f"{TASK_ID} — inter-model instruction divergence\n"
                 "fraction of (prompt,run) pairs where models use different opcode",
                 fontsize=10)

    for bi in range(len(top_bytes)):
        for pi in range(len(model_pairs)):
            ax.text(pi, bi, f"{matrix[bi, pi]:.0%}",
                    ha="center", va="center", fontsize=8,
                    color="white" if matrix[bi, pi] > 0.5 else "black")

    plt.colorbar(im, ax=ax, label="divergence fraction")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "model_divergence_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved model_divergence_heatmap.png")


# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    df = analyze_bytes()
    print_byte_summary(df)
    print("\nGenerating plots...")
    plot_opname_distribution(df)
    plot_raw_value_distribution(df)
    plot_model_divergence_heatmap(df)
    print(f"\nAll outputs saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
