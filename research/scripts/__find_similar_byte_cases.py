from pathlib import Path
import json
import dis
import textwrap
import itertools
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"
PROMPTS_DIR = BASE_DIR / "prompts"
OUT_DIR = BASE_DIR / "shap_bytecode"

MODEL_ALIASES = ["llama", "mistral", "qwen"]

BYTE_INDEX = 107

OUTPUT_CSV = OUT_DIR / f"similar_cases_byte_{BYTE_INDEX}.csv"
OUTPUT_TXT = OUT_DIR / f"similar_cases_byte_{BYTE_INDEX}.txt"


def parse_file_name(file_name: str) -> dict:
    stem = file_name.replace(".py", "")
    parts = stem.split("_")

    return {
        "task": parts[0],
        "prompt": parts[1],
        "run": parts[2],
        "model": parts[3],
        "case_id": "_".join(parts[:2]),  # task + prompt only
    }


def load_function_name(task_id: str) -> str:
    meta_path = PROMPTS_DIR / task_id / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return meta["function_name"]


def load_function(py_file: Path, function_name: str):
    code = py_file.read_text(encoding="utf-8")
    namespace = {}
    exec(code, namespace)

    fn = namespace.get(function_name)
    if not callable(fn):
        raise ValueError(f"Function {function_name} not found")

    return fn, code


def instruction_covering_byte(fn, byte_index: int):
    instructions = list(dis.get_instructions(fn, show_caches=True))

    for i, instr in enumerate(instructions):
        start = instr.offset
        end = instructions[i + 1].offset if i + 1 < len(instructions) else len(fn.__code__.co_code)

        if start <= byte_index < end:
            position_type = "opcode_byte" if byte_index == start else "argument_or_cache_byte"
            return instr, start, end, position_type

    return None, None, None, None


def get_source_context(code: str, line_no: int | None, window: int = 3) -> str:
    lines = code.splitlines()

    if line_no is None:
        return ""

    start = max(1, line_no - window)
    end = min(len(lines), line_no + window)

    out = []
    for i in range(start, end + 1):
        marker = ">>" if i == line_no else "  "
        out.append(f"{marker} {i:03d}: {lines[i - 1]}")

    return "\n".join(out)


def trace_file(py_file: Path) -> dict:
    info = parse_file_name(py_file.name)
    function_name = load_function_name(info["task"])

    try:
        fn, code = load_function(py_file, function_name)
        code_bytes = list(fn.__code__.co_code)
        bytecode_length = len(code_bytes)

        base = {
            **info,
            "file_name": py_file.name,
            "file": str(py_file.relative_to(BASE_DIR)),
            "function_name": function_name,
            "byte_index": BYTE_INDEX,
            "bytecode_length": bytecode_length,
        }

        if BYTE_INDEX >= bytecode_length:
            return {
                **base,
                "status": "out_of_range",
                "byte_value": None,
                "position_type": "padding_or_missing",
                "instruction_offset": None,
                "instruction_end": None,
                "opname": None,
                "arg": None,
                "argrepr": None,
                "starts_line": None,
                "source_context": "",
                "full_code": code,
            }

        byte_value = code_bytes[BYTE_INDEX]
        instr, start, end, position_type = instruction_covering_byte(fn, BYTE_INDEX)

        if instr is None:
            return {
                **base,
                "status": "no_instruction_found",
                "byte_value": byte_value,
                "position_type": None,
                "instruction_offset": None,
                "instruction_end": None,
                "opname": None,
                "arg": None,
                "argrepr": None,
                "starts_line": None,
                "source_context": "",
                "full_code": code,
            }

        return {
            **base,
            "status": "ok",
            "byte_value": byte_value,
            "position_type": position_type,
            "instruction_offset": start,
            "instruction_end": end,
            "opname": instr.opname,
            "arg": instr.arg,
            "argrepr": instr.argrepr,
            "starts_line": instr.starts_line,
            "source_context": get_source_context(code, instr.starts_line),
            "full_code": code,
        }

    except Exception as e:
        return {
            **info,
            "file_name": py_file.name,
            "file": str(py_file.relative_to(BASE_DIR)),
            "function_name": function_name,
            "byte_index": BYTE_INDEX,
            "bytecode_length": None,
            "status": "error",
            "byte_value": None,
            "position_type": None,
            "instruction_offset": None,
            "instruction_end": None,
            "opname": None,
            "arg": None,
            "argrepr": None,
            "starts_line": None,
            "source_context": "",
            "full_code": "",
            "error": str(e),
        }


def collect_traces() -> pd.DataFrame:
    rows = []

    for model_alias in MODEL_ALIASES:
        cleaned_dir = OUTPUTS_DIR / model_alias / "cleaned"
        if not cleaned_dir.exists():
            continue

        for py_file in sorted(cleaned_dir.glob("t*_*.py")):
            rows.append(trace_file(py_file))

    return pd.DataFrame(rows)


def row_distance(a: pd.Series, b: pd.Series) -> float:
    distance = 0.0

    if pd.notna(a["byte_value"]) and pd.notna(b["byte_value"]):
        distance += abs(float(a["byte_value"]) - float(b["byte_value"]))
    else:
        distance += 25

    if a["opname"] != b["opname"]:
        distance += 30

    if a["position_type"] != b["position_type"]:
        distance += 15

    if a["status"] != b["status"]:
        distance += 20

    return distance


def triplet_distance(rows: list[pd.Series]) -> float:
    total = 0.0

    for a, b in itertools.combinations(rows, 2):
        total += row_distance(a, b)

    return total


def choose_most_similar_triplet(group: pd.DataFrame):
    model_rows = {}

    for model in MODEL_ALIASES:
        sub = group[(group["model"] == model) & (group["status"].isin(["ok", "out_of_range"]))]
        if sub.empty:
            return None, None
        model_rows[model] = [row for _, row in sub.iterrows()]

    best_triplet = None
    best_score = float("inf")

    for combo in itertools.product(
        model_rows["llama"],
        model_rows["mistral"],
        model_rows["qwen"],
    ):
        rows = list(combo)
        score = triplet_distance(rows)

        # Prefer all-ok triplets over padding/out-of-range
        score -= sum(r["status"] == "ok" for r in rows) * 5

        if score < best_score:
            best_score = score
            best_triplet = rows

    return best_triplet, best_score


def summarize_triplet(rows: list[pd.Series]) -> dict:
    return {
        "selected_files": ", ".join([r["file_name"] for r in rows]),
        "selected_runs": ", ".join([f"{r['model']}={r['run']}" for r in rows]),
        "byte_values": ", ".join([f"{r['model']}={r['byte_value']}" for r in rows]),
        "opnames": ", ".join([f"{r['model']}={r['opname']}" for r in rows]),
        "position_types": ", ".join([f"{r['model']}={r['position_type']}" for r in rows]),
        "statuses": ", ".join([f"{r['model']}={r['status']}" for r in rows]),
    }


def write_case_report(df: pd.DataFrame, top_n: int = 10):
    case_scores = []
    selected_triplets = {}

    for case_id, group in df.groupby("case_id"):
        triplet, score = choose_most_similar_triplet(group)

        if triplet is None:
            continue

        selected_triplets[case_id] = triplet
        summary = summarize_triplet(triplet)

        case_scores.append({
            "case_id": case_id,
            "similarity_score": score,
            **summary,
        })

    ranked = pd.DataFrame(case_scores).sort_values("similarity_score", ascending=True)

    lines = []
    lines.append(f"Most convergent task+prompt cases for byte_{BYTE_INDEX}")
    lines.append("Runs are treated as repeated stochastic samples.")
    lines.append("For each task+prompt, one representative run per model is selected.")
    lines.append("Lower score = more similar.")
    lines.append("=" * 90)

    for _, row in ranked.head(top_n).iterrows():
        case_id = row["case_id"]
        triplet = selected_triplets[case_id]

        lines.append("\n" + "=" * 90)
        lines.append(f"CASE: {case_id}")
        lines.append(f"similarity_score: {row['similarity_score']}")
        lines.append(f"selected runs: {row['selected_runs']}")
        lines.append(f"byte values: {row['byte_values']}")
        lines.append(f"opnames: {row['opnames']}")
        lines.append(f"position types: {row['position_types']}")
        lines.append(f"statuses: {row['statuses']}")
        lines.append("=" * 90)

        for r in sorted(triplet, key=lambda x: x["model"]):
            lines.append(f"\n--- MODEL: {r['model']} ---")
            lines.append(f"file: {r['file_name']}")
            lines.append(f"run: {r['run']}")
            lines.append(f"status: {r['status']}")
            lines.append(f"byte_value: {r['byte_value']}")
            lines.append(f"bytecode_length: {r['bytecode_length']}")
            lines.append(f"position_type: {r['position_type']}")
            lines.append(f"instruction: {r['opname']} {r['argrepr']}")
            lines.append(f"instruction_offset: {r['instruction_offset']} - {r['instruction_end']}")
            lines.append(f"starts_line: {r['starts_line']}")

            if r["source_context"]:
                lines.append("\nSource context:")
                lines.append(r["source_context"])
            else:
                lines.append("\nSource context: not available")

            lines.append("\nFull code:")
            lines.append(textwrap.indent(r["full_code"], "    "))

    OUTPUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    return ranked


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = collect_traces()
    df.to_csv(OUTPUT_CSV, index=False)

    ranked = write_case_report(df, top_n=10)

    print(f"Saved trace CSV to: {OUTPUT_CSV}")
    print(f"Saved report TXT to: {OUTPUT_TXT}")

    print("\nTop convergent task+prompt cases:")
    print(ranked.head(10))


if __name__ == "__main__":
    main()
