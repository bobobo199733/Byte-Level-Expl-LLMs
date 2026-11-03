from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"

TASKS = ["t41", "t42", "t43", "t44", "t45", "t46", "t47", "t48", "t49", "t50"]


def run_step(script_name: str, env_vars: dict = None):
    script_path = SCRIPTS_DIR / script_name
    print(f"\n=== Running {script_name} ===")

    import os
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code {result.returncode}"
        )


def run_step_with_task(script_name: str, task_id: str):
    """Run a script with TASK_ID injected as environment variable."""
    script_path = SCRIPTS_DIR / script_name
    print(f"\n=== Running {script_name} [task={task_id}] ===")

    import os
    env = os.environ.copy()
    env["TASK_ID"] = task_id

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed for task {task_id} "
            f"with exit code {result.returncode}"
        )


def main():
    # 1. Generate code from all LLMs
    run_step("generate.py")

    # 2. Extract bytecode features from generated code
    run_step("extract_bytecode_features.py")

    # 3. Convert raw features into ML-ready numeric dataset
    run_step("preprocess_features.py")

    # 4. Train classifier: bytecode features → LLM model
    run_step("train_bytecode_model.py")

    # 5. Run global SHAP explanations (beeswarm + bar plots)
    run_step("run_shap_bytecode.py")

    # 6. Per-task SHAP analysis (ternary plots, heatmaps, top bytes)
    for task in TASKS:
        run_step_with_task("analyze_task_n.py", task)

    # 7. Per-task byte trace analysis (divergence heatmap, opname distribution)
    for task in TASKS:
        run_step_with_task("analyze_bytes.py", task)

    # 8. Cross-task comparison plots
    run_step("compare_tasks.py")

    # 9. Global ternary prediction map
    run_step("plot_global_ternary.py")

    print("\n=== Pipeline complete ===")
    print("All thesis figures saved to analysis/")


if __name__ == "__main__":
    main()
