from pathlib import Path
import re
import ast
import types
import pandas as pd
import dis
import sys
import re

# Positional opcode/decoded-argument pairs, not literal CPython co_code bytes.
REPRESENTATION_KIND = "opcode_argument_pairs_v1"
DEFAULT_REPRESENTATION_LENGTH = 320

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


def instruction_trace_from_file(
    py_file: Path,
    target_function: str,
) -> list[dict]:
    """Trace the exact positional features produced by extract_script_bytecode.

    Each instruction contributes two feature positions: its opcode and its
    decoded integer argument (zero when absent). CACHE instructions are
    excluded. These feature positions are *not* CPython co_code offsets.

    Source lines refer to the AST-normalized text compiled by this pipeline,
    not necessarily the original file's line numbering.
    """
    raw = py_file.read_text(encoding="utf-8")
    normalized_source = keep_only_defs(extract_code(raw))
    compiled = compile(normalized_source, filename=str(py_file), mode="exec")
    top_level = get_top_level_code_objects(compiled)
    if target_function not in top_level:
        raise ValueError(
            f"Target function '{target_function}' not found: "
            f"{sorted(top_level)}"
        )

    ordered = [top_level[target_function]]
    ordered.extend(
        top_level[name] for name in sorted(top_level)
        if name != target_function
    )
    source_lines = normalized_source.splitlines()
    rows = []

    def visit(code_obj):
        for instr in dis.get_instructions(code_obj, show_caches=False):
            index = len(rows) * 2
            line = (
                instr.positions.lineno
                if getattr(instr, "positions", None) is not None
                else instr.starts_line
            )
            line_text = (
                source_lines[line - 1].strip()
                if line is not None and 1 <= line <= len(source_lines)
                else ""
            )
            rows.append({
                "byte_pos": index,
                "arg_pos": index + 1,
                "opname": instr.opname,
                "opcode": instr.opcode,
                "arg_raw": instr.arg if instr.arg is not None else 0,
                "argval": str(instr.argval)[:60],
                "lineno": line,
                "source_line": line_text,
                "source_line_origin": "normalized_source",
                "co_name": code_obj.co_name,
                "dis_offset": instr.offset,
            })
        for child in code_obj.co_consts:
            if isinstance(child, types.CodeType):
                visit(child)

    for code_obj in ordered:
        visit(code_obj)

    # Fail closed if backtracking and the classifier use different positions.
    expected, _ = collect_ordered_script_bytes(compiled, target_function)
    observed = [
        value
        for row in rows
        for value in (row["opcode"], row["arg_raw"])
    ]
    if observed != expected:
        raise AssertionError("Instruction trace does not match feature extraction")
    return rows


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
        "python_version": sys.version.split()[0],
        "representation_kind": REPRESENTATION_KIND,
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
    representation_length: int | None = None,
) -> pd.DataFrame:
    """Recreate trained feature positions without inventing missing values.

    For a full 0..N-1 byte schema, N is inferred. For a sparse selection,
    the caller must supply the original representation length explicitly.
    """
    if not feature_columns or len(set(feature_columns)) != len(feature_columns):
        raise ValueError("Feature list must be nonempty and contain no duplicates")

    byte_cols = [c for c in feature_columns if re.fullmatch(r"byte_\d+", c)]
    indices = sorted(int(c[5:]) for c in byte_cols)
    if not indices:
        raise ValueError("No positional byte features were requested")

    if representation_length is None:
        if indices != list(range(len(indices))):
            raise ValueError(
                "Sparse feature selection requires representation_length "
                "from the trained model's configuration"
            )
        representation_length = len(indices)

    if representation_length <= 0 or max(indices) >= representation_length:
        raise ValueError("Requested feature position exceeds representation length")

    row = build_bytecode_row_from_file(
        py_file=py_file,
        max_len=representation_length,
        target_function=target_function,
    )
    df = pd.DataFrame([row])
    if "was_truncated" in df.columns:
        df["was_truncated"] = df["was_truncated"].astype(int)

    missing = sorted(set(feature_columns) - set(df.columns))
    if missing:
        raise ValueError(f"Missing requested features: {missing}")
    return df.loc[:, feature_columns].copy()
