import re
import ast
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import threading
import time
from bytecode_utils import keep_only_defs, extract_code

import requests


# ===== CONFIG =====
MODELS = {
    "llama": "llama3.1:8b",
    "mistral": "mistral",
    "qwen": "qwen2.5:7b"
}

RUNS_PER_PROMPT = 3
MAX_WORKERS = 1

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "test_data" / "prompts"
OUTPUTS_DIR = BASE_DIR / "test_data" / "outputs"


# ===== LLM CALL =====
def call_llm(prompt: str, ollama_model: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": ollama_model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()

    if "response" not in data:
        raise RuntimeError(f"Unexpected Ollama response: {data}")

    return data["response"].strip()


# ===== JOB LOGIC =====
def generate_one(task_name: str, prompt_id: str, run: int, model_alias: str, ollama_model: str, prompt_text: str) -> str:
    output_dir = OUTPUTS_DIR / model_alias
    raw_dir = output_dir / "raw"
    cleaned_dir = output_dir / "cleaned"

    raw_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    raw_filename = f"{task_name}_{prompt_id}_r{run}_{model_alias}_raw.txt"
    clean_filename = f"{task_name}_{prompt_id}_r{run}_{model_alias}.py"

    raw_path = raw_dir / raw_filename
    clean_path = cleaned_dir / clean_filename

    job_id = f"{task_name}_{prompt_id}_r{run}_{model_alias}"

    thread_name = threading.current_thread().name
    start_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] START {job_id} on {thread_name}")

    # Case 1: both exist
    if raw_path.exists() and clean_path.exists():
        duration = time.time() - start_time
        return f"SKIP {job_id} already exists ({duration:.2f}s)"

    # Case 2: raw exists, cleaned missing
    if raw_path.exists() and not clean_path.exists():
        raw_output = raw_path.read_text(encoding="utf-8")
        code = keep_only_defs(extract_code(raw_output))
        clean_path.write_text(code, encoding="utf-8")

        duration = time.time() - start_time
        return f"REBUILT {job_id} cleaned from raw ({duration:.2f}s)"

    # Case 3: generate
    raw_output = call_llm(prompt_text, ollama_model)

    raw_path.write_text(raw_output, encoding="utf-8")

    code = keep_only_defs(extract_code(raw_output))
    clean_path.write_text(code, encoding="utf-8")

    duration = time.time() - start_time
    return f"DONE {job_id} ({duration:.2f}s)"


def collect_jobs():
    jobs = []

    for task_dir in sorted(PROMPTS_DIR.iterdir()):
        if not task_dir.is_dir():
            continue

        task_name = task_dir.name

        for prompt_file in sorted(task_dir.glob("p*.txt")):
            prompt_id = prompt_file.stem
            prompt_text = prompt_file.read_text(encoding="utf-8")

            for run in range(1, RUNS_PER_PROMPT + 1):
                for model_alias, ollama_model in MODELS.items():
                    jobs.append(
                        (task_name, prompt_id, run, model_alias, ollama_model, prompt_text)
                    )

    return jobs


# ===== MAIN =====
def main():
    jobs = collect_jobs()
    print(f"Total jobs discovered: {len(jobs)}")
    print(f"Max workers: {MAX_WORKERS}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(generate_one, *job)
            for job in jobs
        ]

        for future in as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
