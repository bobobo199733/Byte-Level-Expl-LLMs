from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"


def run_step(script_name: str):
    script_path = SCRIPTS_DIR / script_name
    print(f"\n=== Running {script_name} ===")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed with exit code {result.returncode}")


def main():
    run_step("generate.py")
    run_step("_evaluate.py")
    run_step("_feature_extract.py")
    run_step("_preprocess_features.py")
    run_step("_train_model.py")
    run_step("_run_shap.py")
    print("\n=== Pipeline complete ===")


if __name__ == "__main__":
    main()
