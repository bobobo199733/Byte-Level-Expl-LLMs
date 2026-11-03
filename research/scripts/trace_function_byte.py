from pathlib import Path
import json
import dis
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"
PROMPTS_DIR = BASE_DIR / "prompts"
TRACE_DIR = BASE_DIR / "shap_bytecode"

BYTE_INDEX = 106
OUTPUT_CSV = TRACE_DIR / f"byte_{BYTE_INDEX}_instruction_trace.csv"
SUMMARY_CSV = TRACE_DIR / f"byte_{BYTE_INDEX}_model_summary.csv"

MODEL_ALIASES = ["llama", "mistral", "qwen"]


def parse_file_name(file_name: str) -> dict:
    stem = file_name.replace(".py", "")
    parts = stem.split("_")

    if len(parts) < 4:
        raise ValueError(f"Unexpected file name format: {file_name}")

    return {
        "task": parts[0],
        "prompt": parts[1],
        "run": parts[2],
        "model": parts[3],
    }


def load_function_name(task_id: str) -> str:
    meta_path = PROMPTS_DIR / task_id / "meta.json"

    if not meta_path.exists():
        raise FileNotFoundError(f"Missing meta.json: {meta_path}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    function_name = meta.get("function_name")

    if not function_name:
        raise ValueError(f"No function_name in {meta_path}")

    return function_name


def load_function(py_file: Path, function_name: str):
    code = py_file.read_text(encoding="utf-8")
    namespace = {}

    exec(code, namespace)

    fn = namespace.get(function_name)

    if not callable(fn):
        raise ValueError(f"Function '{function_name}' not found or not callable")

    return fn


def instruction_covering_byte(fn, byte_index: int):
    instructions = list(dis.get_instructions(fn, show_caches=True))

    if not instructions:
        return None, None, None, None

    for i, instr in enumerate(instructions):
        start = instr.offset

        if i + 1 < len(instructions):
            end = instructions[i + 1].offset
        else:
            end = len(fn.__code__.co_code)

        if start <= byte_index < end:
            position_type = "opcode_byte" if byte_index == start else "argument_or_cache_byte"
            return instr, start, end, position_type

    return None, None, None, None


def trace_file(py_file: Path, model_alias: str) -> dict:
    file_name = py_file.name

    try:
        meta = parse_file_name(file_name)
        function_name = load_function_name(meta["task"])
        fn = load_function(py_file, function_name)

        code_bytes = list(fn.__code__.co_code)
        bytecode_length = len(code_bytes)

        base_row = {
            "file_name": file_name,
            "file": str(py_file.relative_to(BASE_DIR)),
            "task": meta["task"],
            "prompt": meta["prompt"],
            "run": meta["run"],
            "model": meta["model"],
            "function_name": function_name,
            "byte_index": BYTE_INDEX,
            "bytecode_length": bytecode_length,
        }

        if BYTE_INDEX >= bytecode_length:
            return {
                **base_row,
                "byte_value": None,
                "status": "out_of_range",
                "instruction_offset": None,
                "instruction_end": None,
                "position_type": "padding_or_missing",
                "opcode": None,
                "opname": None,
                "arg": None,
                "argval": None,
                "argrepr": None,
                "starts_line": None,
                "is_jump_target": None,
                "error": None,
            }

        byte_value = code_bytes[BYTE_INDEX]
        instr, start, end, position_type = instruction_covering_byte(fn, BYTE_INDEX)

        if instr is None:
            return {
                **base_row,
                "byte_value": byte_value,
                "status": "no_instruction_found",
                "instruction_offset": None,
                "instruction_end": None,
                "position_type": None,
                "opcode": None,
                "opname": None,
                "arg": None,
                "argval": None,
                "argrepr": None,
                "starts_line": None,
                "is_jump_target": None,
                "error": None,
            }

        return {
            **base_row,
            "byte_value": byte_value,
            "status": "ok",
            "instruction_offset": start,
            "instruction_end": end,
            "position_type": position_type,
            "opcode": instr.opcode,
            "opname": instr.opname,
            "arg": instr.arg,
            "argval": str(instr.argval),
            "argrepr": instr.argrepr,
            "starts_line": instr.starts_line,
            "is_jump_target": instr.is_jump_target,
            "error": None,
        }

    except Exception as e:
        return {
            "file_name": file_name,
            "file": str(py_file.relative_to(BASE_DIR)),
            "task": None,
            "prompt": None,
            "run": None,
            "model": model_alias,
            "function_name": None,
            "byte_index": BYTE_INDEX,
            "byte_value": None,
            "bytecode_length": None,
            "status": "error",
            "instruction_offset": None,
            "instruction_end": None,
            "position_type": None,
            "opcode": None,
            "opname": None,
            "arg": None,
            "argval": None,
            "argrepr": None,
            "starts_line": None,
            "is_jump_target": None,
            "error": str(e),
        }


def build_model_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []

    for model_name in sorted(df["model"].dropna().unique()):
        subset = df[df["model"] == model_name]

        summary_rows.append({
            "model": model_name,
            "rows": len(subset),
            "ok_rows": int((subset["status"] == "ok").sum()),
            "out_of_range_rows": int((subset["status"] == "out_of_range").sum()),
            "error_rows": int((subset["status"] == "error").sum()),
            "mean_byte_value": subset["byte_value"].mean(),
            "median_byte_value": subset["byte_value"].median(),
            "min_byte_value": subset["byte_value"].min(),
            "max_byte_value": subset["byte_value"].max(),
            "most_common_byte_value": (
                subset["byte_value"].value_counts(dropna=True).index[0]
                if not subset["byte_value"].dropna().empty
                else None
            ),
            "most_common_opname": (
                subset["opname"].value_counts(dropna=True).index[0]
                if not subset["opname"].dropna().empty
                else None
            ),
            "most_common_position_type": (
                subset["position_type"].value_counts(dropna=True).index[0]
                if not subset["position_type"].dropna().empty
                else None
            ),
        })

    return pd.DataFrame(summary_rows)


def print_global_summary(df: pd.DataFrame):
    print(f"\nSaved trace to: {OUTPUT_CSV}")
    print(f"Rows: {len(df)}")

    print("\nGLOBAL status counts:")
    print(df["status"].value_counts(dropna=False))

    print("\nGLOBAL position type counts:")
    print(df["position_type"].value_counts(dropna=False))

    print("\nGLOBAL top opnames:")
    print(df["opname"].value_counts(dropna=False).head(20))

    print("\nGLOBAL top byte values:")
    print(df["byte_value"].value_counts(dropna=False).head(20))


def print_per_model_summary(df: pd.DataFrame):
    for model_name in sorted(df["model"].dropna().unique()):
        subset = df[df["model"] == model_name]

        print("\n" + "=" * 70)
        print(f"MODEL: {model_name}")
        print("=" * 70)

        print("\nStatus counts:")
        print(subset["status"].value_counts(dropna=False))

        print("\nPosition type counts:")
        print(subset["position_type"].value_counts(dropna=False))

        print("\nTop opnames:")
        print(subset["opname"].value_counts(dropna=False).head(15))

        print("\nTop byte values:")
        print(subset["byte_value"].value_counts(dropna=False).head(15))

        print("\nByte value statistics:")
        print(subset["byte_value"].describe())

        print("\nMean byte value by opname:")
        print(
            subset.groupby("opname")["byte_value"]
            .mean()
            .sort_values(ascending=True)
            .head(15)
        )


def main():
    rows = []

    for model_alias in MODEL_ALIASES:
        cleaned_dir = OUTPUTS_DIR / model_alias / "cleaned"

        if not cleaned_dir.exists():
            print(f"Skipping missing directory: {cleaned_dir}")
            continue

        for py_file in sorted(cleaned_dir.glob("t*_*.py")):
            rows.append(trace_file(py_file, model_alias))

    df = pd.DataFrame(rows)

    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    summary_df = build_model_summary(df)
    summary_df.to_csv(SUMMARY_CSV, index=False)

    print_global_summary(df)
    print_per_model_summary(df)

    print(f"\nSaved model summary to: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
