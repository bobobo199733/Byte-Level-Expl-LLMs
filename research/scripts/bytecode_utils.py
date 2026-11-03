from pathlib import Path
import re
import ast
import types
import pandas as pd
import dis

PAD_VALUE = -1


def extract_code(text: str) -> str:
    pattern = r"```(?:python)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        return matches[0].strip()

    return text.strip()


def keep_only_defs(code: str) -> str:
    try:
        tree = ast.parse(code)
    except Exception:
        return code

    new_body = []

    for node in tree.body:
        if isinstance(node, (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
            ast.Import,
            ast.ImportFrom,
        )):
            new_body.append(node)

    tree.body = new_body
    ast.fix_missing_locations(tree)

    return ast.unparse(tree)

def debug_collect(code_obj, indent=0):
    prefix = " " * indent

    own_bytes = list(code_obj.co_code)

    print(f"{prefix}{code_obj.co_name}")
    print(f"{prefix}own co_code length: {len(own_bytes)}")

    total = len(own_bytes)

    for const in code_obj.co_consts:
        if isinstance(const, types.CodeType):
            child_total = debug_collect(const, indent + 4)
            total += child_total

    print(f"{prefix}total recursive length: {total}")
    return total


def collect_code_bytes(code_obj) -> list[int]:
    byte_values = []
    for instr in dis.get_instructions(code_obj, show_caches=False):
        byte_values.append(instr.opcode)
        byte_values.append(instr.arg if instr.arg is not None else 0)

    for const in code_obj.co_consts:
        if isinstance(const, types.CodeType):
            byte_values.extend(collect_code_bytes(const))

    return byte_values


def get_top_level_code_objects(module_code_obj) -> dict[str, types.CodeType]:
    code_objects = {}

    for const in module_code_obj.co_consts:
        if isinstance(const, types.CodeType):
            code_objects[const.co_name] = const

    return code_objects


def collect_ordered_script_bytes(
    module_code_obj,
    target_function: str,
) -> tuple[list[int], str]:
    top_level_code_objects = get_top_level_code_objects(module_code_obj)

    if target_function not in top_level_code_objects:
        available = sorted(top_level_code_objects.keys())
        raise ValueError(
            f"Target function '{target_function}' not found. "
            f"Available top-level code objects: {available}"
        )

    byte_values = []

    # 1. Target function first
    target_code_obj = top_level_code_objects[target_function]
    byte_values.extend(collect_code_bytes(target_code_obj))

    # 2. Helper functions/classes after, in deterministic order
    for name in sorted(top_level_code_objects.keys()):
        if name == target_function:
            continue

        byte_values.extend(
            collect_code_bytes(top_level_code_objects[name])
        )

    return byte_values, target_function


def extract_script_bytecode(
    py_file: Path,
    target_function: str | None = None,
) -> tuple[list[int], str]:
    raw_text = py_file.read_text(encoding="utf-8")

    code = extract_code(raw_text)
    code = keep_only_defs(code)

    compiled = compile(code, filename=str(py_file), mode="exec")

    if target_function is not None:
        byte_values, extraction_scope = collect_ordered_script_bytes(
            module_code_obj=compiled,
            target_function=target_function,
        )
    else:
        byte_values = collect_code_bytes(compiled)
        extraction_scope = "full_script"

    if not byte_values:
        raise ValueError(f"No bytecode found in {py_file}")

    return byte_values, extraction_scope


def pad_or_truncate(values: list[int], max_len: int) -> tuple[list[int], list[int]]:
    values = values[:max_len]
    mask = [1] * len(values)

    padding_len = max_len - len(values)

    values = values + [PAD_VALUE] * padding_len
    mask = mask + [0] * padding_len

    return values, mask


def build_bytecode_row_from_file(
    py_file: Path,
    max_len: int,
    target_function: str | None = None,
) -> dict:
    byte_values, extraction_scope = extract_script_bytecode(
        py_file=py_file,
        target_function=target_function,
    )

    fixed, mask = pad_or_truncate(byte_values, max_len)

    row = {
        "function_name": extraction_scope,
        "original_byte_length": len(byte_values),
        "was_truncated": len(byte_values) > max_len,
    }

    for i, value in enumerate(fixed):
        row[f"byte_{i}"] = value

    # for i, value in enumerate(mask):
    #     row[f"mask_{i}"] = value

    return row


def preprocess_single_file(
    py_file: Path,
    feature_columns: list[str],
    target_function: str | None = None,
) -> pd.DataFrame:
    byte_cols = [c for c in feature_columns if c.startswith("byte_")]
    max_len = len(byte_cols)

    row = build_bytecode_row_from_file(
        py_file=py_file,
        max_len=max_len,
        target_function=target_function,
    )

    df = pd.DataFrame([row])

    if "was_truncated" in df.columns:
        df["was_truncated"] = df["was_truncated"].astype(int)

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]
    df.to_csv("debug_single_file.csv", index=False)

    return df
