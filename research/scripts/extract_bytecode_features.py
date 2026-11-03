from pathlib import Path
import json
import sys
import pandas as pd

from bytecode_utils import build_bytecode_row_from_file


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_ALIASES = ["llama", "mistral", "qwen"]
MAX_LEN = 320


def parse_file_name(file_name: str) -> dict:
    stem = file_name.replace(".py", "")
    parts = stem.split("_")

    return {
        "task": parts[0],
        "prompt": parts[1],
        "run": parts[2],
        "model": parts[3],
    }


def main():
    global USE_TEST_DATA, MAX_LEN
    USE_TEST_DATA = False
    if len(sys.argv) >= 2:
        USE_TEST_DATA = sys.argv[1] == "1"
    if len(sys.argv) >= 3:
        MAX_LEN = int(sys.argv[2])
    rows = []

    if USE_TEST_DATA:
        OUTPUTS_DIR = BASE_DIR / "test_data" / "outputs"
        PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"
        OUTPUT_CSV = BASE_DIR / "test_data" / "features" / "function_bytecode_features.csv"

    else:
        OUTPUTS_DIR = BASE_DIR / "outputs"
        PROMPTS_DIR = BASE_DIR / "prompts"
        OUTPUT_CSV = BASE_DIR / "features" / "function_bytecode_features.csv"

    for model_alias in MODEL_ALIASES:
        cleaned_dir = OUTPUTS_DIR / model_alias / "cleaned"

        if not cleaned_dir.exists():
            continue

        for py_file in sorted(cleaned_dir.glob("t*_*.py")):
            file_name = py_file.name
            meta = parse_file_name(file_name)

            try:
                meta_file = PROMPTS_DIR / meta["task"] / "meta.json"
                task_meta = json.loads(meta_file.read_text(encoding="utf-8"))

                target_function = task_meta["function_name"]

                bytecode_row = build_bytecode_row_from_file(
                    py_file=py_file,
                    max_len=MAX_LEN,
                    target_function=target_function,
                )

                row = {
                    "file_name": file_name,
                    "file": str(py_file.relative_to(BASE_DIR)),
                    "task": meta["task"],
                    "prompt": meta["prompt"],
                    "run": meta["run"],
                    "model": meta["model"],
                    "bytecode_extract_status": "ok",
                    **bytecode_row,
                }

            except Exception as e:
                row = {
                    "file_name": file_name,
                    "file": str(py_file.relative_to(BASE_DIR)),
                    "task": meta["task"],
                    "prompt": meta["prompt"],
                    "run": meta["run"],
                    "model": meta["model"],
                    "function_name": None,
                    "original_byte_length": 0,
                    "was_truncated": False,
                    "bytecode_extract_status": "error",
                    "bytecode_extract_error": str(e),
                }

                for i in range(MAX_LEN):
                    row[f"byte_{i}"] = 0

            rows.append(row)

    bytecode_df = pd.DataFrame(rows)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    bytecode_df.to_csv(OUTPUT_CSV, index=False)

    print(f"Saved to: {OUTPUT_CSV}")
    print(f"Rows: {len(bytecode_df)}")
    print(f"Feature length: {MAX_LEN}")
    print(
        f"Extraction errors: "
        f"{(bytecode_df['bytecode_extract_status'] == 'error').sum()}"
    )


if __name__ == "__main__":
    main()
