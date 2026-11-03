from pathlib import Path
import ast
import csv


# ===== CONFIG =====
MODEL_ALIASES = ["llama", "mistral", "qwen"]

# ===== PATHS =====
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"
SCORES_DIR = BASE_DIR / "evaluation" / "scores"
FEATURES_DIR = BASE_DIR / "features"
OUTPUT_FILE = FEATURES_DIR / "raw_features.csv"

FEATURES_DIR.mkdir(parents=True, exist_ok=True)


# ===== AST FEATURE EXTRACTOR =====

class FeatureExtractor(ast.NodeVisitor):
    def __init__(self):
        self.features = {
            "num_functions": 0,
            "num_returns": 0,
            "num_assignments": 0,
            "num_if": 0,
            "num_for": 0,
            "num_while": 0,
            "num_try": 0,
            "num_raise": 0,
            "num_calls": 0,
            "num_compares": 0,
            "num_binary_ops": 0,
            "num_unary_ops": 0,
            "num_dict_literals": 0,
            "has_try_except": 0,
            "has_raise": 0,
            "has_membership_check": 0,
            "max_nesting_depth": 0,
        }
        self.current_depth = 0

    def _enter_block(self):
        self.current_depth += 1
        self.features["max_nesting_depth"] = max(
            self.features["max_nesting_depth"],
            self.current_depth
        )

    def _leave_block(self):
        self.current_depth -= 1

    def visit_FunctionDef(self, node):
        self.features["num_functions"] += 1
        self.generic_visit(node)

    def visit_Return(self, node):
        self.features["num_returns"] += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.features["num_assignments"] += 1
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.features["num_assignments"] += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.features["num_assignments"] += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.features["num_if"] += 1
        self._enter_block()
        self.generic_visit(node)
        self._leave_block()

    def visit_For(self, node):
        self.features["num_for"] += 1
        self._enter_block()
        self.generic_visit(node)
        self._leave_block()

    def visit_While(self, node):
        self.features["num_while"] += 1
        self._enter_block()
        self.generic_visit(node)
        self._leave_block()

    def visit_Try(self, node):
        self.features["num_try"] += 1
        self.features["has_try_except"] = 1
        self._enter_block()
        self.generic_visit(node)
        self._leave_block()

    def visit_Raise(self, node):
        self.features["num_raise"] += 1
        self.features["has_raise"] = 1
        self.generic_visit(node)

    def visit_Call(self, node):
        self.features["num_calls"] += 1
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.features["num_compares"] += 1
        for op in node.ops:
            if isinstance(op, (ast.In, ast.NotIn)):
                self.features["has_membership_check"] = 1
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.features["num_binary_ops"] += 1
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        self.features["num_unary_ops"] += 1
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.features["num_dict_literals"] += 1
        self.generic_visit(node)


def extract_ast_features(code: str) -> dict:
    base = {
        "num_functions": 0,
        "num_returns": 0,
        "num_assignments": 0,
        "num_if": 0,
        "num_for": 0,
        "num_while": 0,
        "num_try": 0,
        "num_raise": 0,
        "num_calls": 0,
        "num_compares": 0,
        "num_binary_ops": 0,
        "num_unary_ops": 0,
        "num_dict_literals": 0,
        "has_try_except": 0,
        "has_raise": 0,
        "has_membership_check": 0,
        "max_nesting_depth": 0,
        "num_lines": len([line for line in code.splitlines() if line.strip()]),
        "num_chars": len(code),
        "syntax_valid": 0,
        "has_validation_logic": 0,
        "validation_score": 0,
    }

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return base

    extractor = FeatureExtractor()
    extractor.visit(tree)

    features = extractor.features
    features["num_lines"] = base["num_lines"]
    features["num_chars"] = base["num_chars"]
    features["syntax_valid"] = 1

    features["has_validation_logic"] = int(
        features["num_if"] > 0 and features["num_raise"] > 0
    )

    features["validation_score"] = (
        features["num_if"]
        + features["num_raise"]
        + features["has_membership_check"]
    )

    return features


# ===== HELPERS =====

def parse_filename(file_name: str) -> dict:
    """
    Expected format:
    t1_p1_r1_llama.py
    t1_p1_r1_mistral.py
    t1_p1_r1_qwen.py
    """
    stem = file_name.replace(".py", "")
    parts = stem.split("_")

    if len(parts) < 4:
        raise ValueError(f"Unexpected filename format: {file_name}")

    return {
        "task": parts[0],
        "prompt": parts[1],
        "run": parts[2],
        "model": parts[3],
    }


def load_scores(model_alias: str) -> dict:
    scores_file = SCORES_DIR / f"scores_{model_alias}.csv"
    scores = {}

    if not scores_file.exists():
        print(f"WARNING: Missing scores file: {scores_file}")
        return scores

    with scores_file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores[row["file"]] = row

    return scores


# ===== MAIN =====

def main():
    rows = []

    for model_alias in MODEL_ALIASES:
        cleaned_dir = OUTPUTS_DIR / model_alias / "cleaned"

        if not cleaned_dir.exists():
            print(f"Skipping {model_alias}: no cleaned directory found")
            continue

        scores = load_scores(model_alias)

        print(f"\n=== Extracting features for {model_alias} ===")

        for file_path in sorted(cleaned_dir.glob("t*_*.py")):
            file_name = file_path.name
            print(f"Extracting features from {file_name}...")

            meta = parse_filename(file_name)
            code = file_path.read_text(encoding="utf-8")
            features = extract_ast_features(code)

            score_row = scores.get(file_name)

            if score_row is None:
                score = ""
                status = "missing_score"
                passed = ""
                total = ""
            else:
                score = score_row["score"]
                status = score_row["status"]
                passed = score_row["passed"]
                total = score_row["total"]

            row = {
                "file": file_name,
                "task": meta["task"],
                "prompt": meta["prompt"],
                "run": meta["run"],
                "model": meta["model"],
                "score": score,
                "status": status,
                "passed": passed,
                "total": total,
                "timeout_flag": int(status == "timeout"),
                "error_flag": int(status == "error"),
                **features,
            }

            rows.append(row)

    fieldnames = [
        "file",
        "task",
        "prompt",
        "run",
        "model",
        "score",
        "status",
        "passed",
        "total",
        "timeout_flag",
        "error_flag",
        "num_functions",
        "num_returns",
        "num_assignments",
        "num_if",
        "num_for",
        "num_while",
        "num_try",
        "num_raise",
        "num_calls",
        "num_compares",
        "num_binary_ops",
        "num_unary_ops",
        "num_dict_literals",
        "has_try_except",
        "has_raise",
        "has_membership_check",
        "max_nesting_depth",
        "num_lines",
        "num_chars",
        "syntax_valid",
        "has_validation_logic",
        "validation_score",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Wrote combined features to: {OUTPUT_FILE}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
