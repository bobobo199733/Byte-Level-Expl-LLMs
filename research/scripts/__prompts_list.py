from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


def main():
    function_names = []

    for task_dir in sorted(PROMPTS_DIR.glob("t*")):
        meta_file = task_dir / "meta.json"

        if not meta_file.exists():
            print(f"Missing meta.json in {task_dir.name}")
            continue

        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))

            function_name = meta.get("function_name")

            if not function_name:
                print(f"No function_name in {meta_file}")
                continue

            function_names.append((task_dir.name, function_name))

        except Exception as e:
            print(f"Failed to read {meta_file}")
            print(f"Reason: {e}")

    print("\n" + "=" * 50)
    print("FUNCTION NAMES")
    print("=" * 50)

    for task_id, fn_name in function_names:
        print(f"{task_id}: {fn_name}")

    print("\nTotal functions:", len(function_names))


if __name__ == "__main__":
    main()
