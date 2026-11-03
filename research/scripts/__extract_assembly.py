from pathlib import Path
import sys
import dis
import ast
import types


def extract_code(text: str) -> str:
    return text.strip()


def keep_only_defs(code: str) -> str:
    tree = ast.parse(code)
    tree.body = [
        node for node in tree.body
        if isinstance(node, (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
            ast.Import,
            ast.ImportFrom,
        ))
    ]
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def get_top_level_code_objects(module_code_obj):
    return {
        const.co_name: const
        for const in module_code_obj.co_consts
        if isinstance(const, types.CodeType)
    }


def recursive_dis_ordered(code_obj, indent=0):
    prefix = " " * indent

    print("\n" + "=" * 80)
    print(f"{prefix}CODE OBJECT: {code_obj.co_name}")
    print("=" * 80)

    dis.dis(code_obj)

    nested = [
        const for const in code_obj.co_consts
        if isinstance(const, types.CodeType)
    ]

    for child in nested:
        recursive_dis_ordered(child, indent + 4)


def inspect_file(py_file: Path, target_function: str):
    raw = py_file.read_text(encoding="utf-8", errors="ignore")
    code = keep_only_defs(extract_code(raw))

    compiled = compile(code, filename=str(py_file), mode="exec")

    top_level = get_top_level_code_objects(compiled)

    if target_function not in top_level:
        raise ValueError(
            f"Target function '{target_function}' not found. "
            f"Available: {sorted(top_level.keys())}"
        )

    print("\nTARGET FUNCTION FIRST")
    recursive_dis_ordered(top_level[target_function])

    print("\nHELPERS / OTHER TOP-LEVEL CODE OBJECTS")
    for name in sorted(top_level.keys()):
        if name == target_function:
            continue
        recursive_dis_ordered(top_level[name])


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("python inspect_bytecode_order.py path/to/script.py target_function_name")
        return

    py_file = Path(sys.argv[1])
    target_function = sys.argv[2]

    inspect_file(py_file, target_function)


if __name__ == "__main__":
    main()
