from pathlib import Path
import re
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_DIRS = [
    BASE_DIR / "prompts",
    BASE_DIR / "test_data" / "prompts",
]

OUT_FILE = BASE_DIR / "prompt_constraint_audit.csv"

PATTERNS = {
    "exactly_one_function": r"\bexactly\s+one\s+function\b",
    "one_function": r"\bone\s+function\b",
    "single_function": r"\bsingle\s+function\b",
    "only_function": r"\bonly\s+(?:one\s+)?function\b",
    "no_helpers": r"\b(?:do\s+not|don't)\s+(?:define|use|create|include)\s+(?:helper|helpers|helper\s+functions?)\b",
    "no_classes": r"\b(?:do\s+not|don't)\s+(?:define|use|create|include)\s+classes\b",
    "no_tests": r"\b(?:do\s+not|don't)\s+(?:include|write|add)\s+tests\b",
    "helper_mentioned": r"\bhelper\s+functions?\b|\bhelpers\b",
}


def audit_prompt_file(prompt_file: Path) -> dict:
    text = prompt_file.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()

    row = {
        "prompt_file": str(prompt_file.relative_to(BASE_DIR)),
        "task": prompt_file.parent.name,
        "file_name": prompt_file.name,
    }

    for label, pattern in PATTERNS.items():
        row[label] = bool(re.search(pattern, lower))

    row["matched_any_constraint"] = any(
        row[label] for label in PATTERNS
        if label != "helper_mentioned"
    )

    return row


def main():
    rows = []

    for prompt_dir in PROMPT_DIRS:
        if not prompt_dir.exists():
            continue

        for prompt_file in sorted(prompt_dir.glob("t*/p*.txt")):
            rows.append(audit_prompt_file(prompt_file))

    df = pd.DataFrame(rows)
    df.to_csv(OUT_FILE, index=False)

    print(f"Saved audit to: {OUT_FILE}")
    print(f"Prompt files checked: {len(df)}")

    if len(df) == 0:
        return

    print("\nConstraint counts:")
    for col in PATTERNS:
        print(f"{col}: {df[col].sum()}")

    print(f"\nMatched any constraint: {df['matched_any_constraint'].sum()}")

    flagged = df[df["matched_any_constraint"]]

    print("\nFlagged prompts:")
    if flagged.empty:
        print("None")
    else:
        print(flagged[["prompt_file"] + list(PATTERNS.keys())].to_string(index=False))


if __name__ == "__main__":
    main()
