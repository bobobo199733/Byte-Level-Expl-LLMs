from pathlib import Path
import json
import csv
import traceback
from datetime import datetime
import multiprocessing as mp


# ===== PATHS =====
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_ALIASES = ["llama", "mistral", "qwen"]
PROMPTS_DIR = BASE_DIR / "prompts"
SCORES_DIR = BASE_DIR / "evaluation" / "scores"
LOGS_DIR = BASE_DIR / "evaluation" / "logs"

SCORES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT_SECONDS = 5


# ===== HELPERS =====

def load_meta(task_id: str) -> dict:
    meta_path = PROMPTS_DIR / task_id / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing meta.json for {task_id}")
    return json.loads(meta_path.read_text(encoding="utf-8"))


def load_code(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def get_callable(namespace: dict, name: str):
    fn = namespace.get(name)
    if not callable(fn):
        raise ValueError(f"Function '{name}' not found or not callable")
    return fn


def call_function(fn, inp):
    """
    Supports:
    - single argument: fn(inp)
    - multiple arguments: fn(*inp) when inp is a list
    """
    if isinstance(inp, list):
        return fn(*inp)
    return fn(inp)


def safe_score(passed: int, total: int) -> float:
    """
    Guarantees score is always between 0 and 1.
    """
    if total <= 0:
        return 0.0

    score = passed / total
    return max(0.0, min(1.0, score))


def get_expected_test_info(task_id: str):
    """
    Used for errors/timeouts too, so total is not randomly 0.
    """
    try:
        meta = load_meta(task_id)
        valid_cases = meta.get("valid_cases", [])
        invalid_cases = meta.get("invalid_cases", [])

        return {
            "function_name": meta.get("function_name"),
            "valid_case_count": len(valid_cases),
            "invalid_case_count": len(invalid_cases),
            "total_expected_tests": len(valid_cases) + len(invalid_cases),
        }

    except Exception:
        return {
            "function_name": None,
            "valid_case_count": None,
            "invalid_case_count": None,
            "total_expected_tests": 0,
        }


def run_valid_cases(fn, cases):
    passed = 0
    total = 0
    failures = []

    for inp, expected in cases:
        total += 1

        try:
            result = call_function(fn, inp)

            if result == expected:
                passed += 1
            else:
                failures.append(
                    f"VALID {inp!r}: expected {expected!r}, got {result!r}"
                )

        except Exception as e:
            failures.append(
                f"VALID {inp!r}: raised {type(e).__name__}: {e}"
            )

    return passed, total, failures


def run_invalid_cases(fn, cases, expected_exception_name: str):
    passed = 0
    total = 0
    failures = []

    for inp in cases:
        total += 1

        try:
            call_function(fn, inp)
            failures.append(
                f"INVALID {inp!r}: expected {expected_exception_name}, but no exception"
            )

        except Exception as e:
            if type(e).__name__ == expected_exception_name:
                passed += 1
            else:
                failures.append(
                    f"INVALID {inp!r}: expected {expected_exception_name}, got {type(e).__name__}: {e}"
                )

    return passed, total, failures


def append_jsonl(path: Path, record: dict):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ===== CHILD PROCESS WORKER =====

def evaluate_one_file_worker(file_path_str: str, queue: mp.Queue):
    """
    Runs inside a child process so it can be killed on timeout.
    """
    file_path = Path(file_path_str)
    file_name = file_path.name
    task_id = file_name.split("_")[0]

    try:
        meta = load_meta(task_id)

        function_name = meta["function_name"]
        valid_cases = meta.get("valid_cases", [])
        invalid_cases = meta.get("invalid_cases", [])
        expected_exception = meta.get("expected_exception", "ValueError")

        code = load_code(file_path)

        namespace = {}
        exec(code, namespace)

        fn = get_callable(namespace, function_name)

        v_passed, v_total, v_failures = run_valid_cases(fn, valid_cases)
        i_passed, i_total, i_failures = run_invalid_cases(
            fn,
            invalid_cases,
            expected_exception,
        )

        total_passed = v_passed + i_passed
        total_tests = v_total + i_total
        score = safe_score(total_passed, total_tests)

        failures = v_failures + i_failures

        queue.put({
            "status": "ok",
            "file": file_name,
            "task": task_id,
            "score": score,
            "passed": total_passed,
            "total": total_tests,
            "num_failures": len(failures),
            "failures": failures,
            "function_name": function_name,
            "valid_case_count": len(valid_cases),
            "invalid_case_count": len(invalid_cases),
            "traceback": None,
        })

    except Exception as e:
        info = get_expected_test_info(task_id)

        queue.put({
            "status": "error",
            "file": file_name,
            "task": task_id,
            "score": 0.0,
            "passed": 0,
            "total": info["total_expected_tests"],
            "num_failures": -1,
            "failures": [f"{type(e).__name__}: {e}"],
            "function_name": info["function_name"],
            "valid_case_count": info["valid_case_count"],
            "invalid_case_count": info["invalid_case_count"],
            "traceback": traceback.format_exc(),
        })


def evaluate_one_file_with_timeout(file_path: Path, timeout_seconds: int) -> dict:
    task_id = file_path.name.split("_")[0]

    queue = mp.Queue()

    process = mp.Process(
        target=evaluate_one_file_worker,
        args=(str(file_path), queue),
    )

    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()

        info = get_expected_test_info(task_id)

        return {
            "status": "timeout",
            "file": file_path.name,
            "task": task_id,
            "score": 0.0,
            "passed": 0,
            "total": info["total_expected_tests"],
            "num_failures": -1,
            "failures": [f"Evaluation timed out after {timeout_seconds} seconds"],
            "function_name": info["function_name"],
            "valid_case_count": info["valid_case_count"],
            "invalid_case_count": info["invalid_case_count"],
            "traceback": None,
        }

    if queue.empty():
        info = get_expected_test_info(task_id)

        return {
            "status": "error",
            "file": file_path.name,
            "task": task_id,
            "score": 0.0,
            "passed": 0,
            "total": info["total_expected_tests"],
            "num_failures": -1,
            "failures": ["Child process ended without returning a result"],
            "function_name": info["function_name"],
            "valid_case_count": info["valid_case_count"],
            "invalid_case_count": info["invalid_case_count"],
            "traceback": None,
        }

    result = queue.get()

    # Final safety guard. Score should never leave this script outside [0, 1].
    result["score"] = max(0.0, min(1.0, float(result.get("score", 0.0))))

    return result


# ===== MAIN =====

def evaluate_model(model_alias: str):
    cleaned_dir = BASE_DIR / "outputs" / model_alias / "cleaned"

    if not cleaned_dir.exists():
        print(f"Skipping {model_alias}: no cleaned directory found")
        return

    score_rows = []
    log_file = LOGS_DIR / f"eval_log_{model_alias}.jsonl"

    if log_file.exists():
        log_file.unlink()

    for file_path in sorted(cleaned_dir.glob("t*_*.py")):
        file_name = file_path.name
        print(f"Evaluating {file_name}...")

        timestamp = datetime.now().isoformat()
        result = evaluate_one_file_with_timeout(file_path, TIMEOUT_SECONDS)

        score_rows.append({
            "file": result["file"],
            "task": result["task"],
            "model": model_alias,
            "score": result["score"],
            "passed": result["passed"],
            "total": result["total"],
            "status": result["status"],
            "num_failures": result["num_failures"],
        })

        append_jsonl(log_file, {
            "timestamp": timestamp,
            "file": result["file"],
            "task": result["task"],
            "model": model_alias,
            "status": result["status"],
            "score": result["score"],
            "passed": result["passed"],
            "total": result["total"],
            "function_name": result["function_name"],
            "valid_case_count": result["valid_case_count"],
            "invalid_case_count": result["invalid_case_count"],
            "num_failures": result["num_failures"],
            "failures": result["failures"],
            "traceback": result["traceback"],
        })

        print(
            f"Done {file_name} -> {result['status']} "
            f"score={result['score']:.3f} "
            f"passed={result['passed']}/{result['total']}"
        )

    output_file = SCORES_DIR / f"scores_{model_alias}.csv"

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file",
                "task",
                "model",
                "score",
                "passed",
                "total",
                "status",
                "num_failures",
            ],
        )

        writer.writeheader()
        writer.writerows(score_rows)

    print(f"\nDone {model_alias}. Results saved to: {output_file}")
    print(f"Logs saved to: {log_file}")


def main():
    for model_alias in MODEL_ALIASES:
        print(f"\n=== Evaluating model: {model_alias} ===")
        evaluate_model(model_alias)


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
