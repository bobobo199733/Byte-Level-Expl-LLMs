import pandas as pd
import numpy as np

CSV_PATH = "../shap_bytecode/predicted_probabilities.csv"  # update to your actual path

df = pd.read_csv(CSV_PATH)

df["predicted_model"] = df[["prob_llama", "prob_mistral", "prob_qwen"]].idxmax(axis=1).str.replace("prob_", "")
df["correct"] = df["predicted_model"] == df["true_model"]
df["task"] = df["file_name"].str.extract(r"(t\d+)_")
df["max_prob"] = df[["prob_llama", "prob_mistral", "prob_qwen"]].max(axis=1)

# --- Per-task accuracy ---
print("=" * 50)
print("ACCURACY PER TASK")
print("=" * 50)
task_acc = df.groupby("task")["correct"].agg(["sum", "count", "mean"]).rename(
    columns={"sum": "correct", "count": "total", "mean": "accuracy"}
)
task_acc["accuracy"] = task_acc["accuracy"].map("{:.1%}".format)
print(task_acc.to_string())

# --- Per-task per-model accuracy ---
print("\n" + "=" * 50)
print("ACCURACY PER TASK PER MODEL")
print("=" * 50)
task_model_acc = (
    df.groupby(["task", "true_model"])["correct"]
    .agg(["sum", "count", "mean"])
    .rename(columns={"sum": "correct", "count": "total", "mean": "accuracy"})
)
task_model_acc["accuracy"] = task_model_acc["accuracy"].map("{:.1%}".format)
print(task_model_acc.to_string())

# --- Confusion per task ---
print("\n" + "=" * 50)
print("CONFUSION PER TASK (true → predicted counts)")
print("=" * 50)
for task, group in df.groupby("task"):
    print(f"\n{task}:")
    confusion = pd.crosstab(group["true_model"], group["predicted_model"])
    print(confusion.to_string())

# --- Duplicate prediction vectors ---
print("\n" + "=" * 50)
print("DUPLICATE PROBABILITY VECTORS")
print("=" * 50)
prob_cols = ["prob_llama", "prob_mistral", "prob_qwen"]
dupes = df[df.duplicated(subset=prob_cols, keep=False)].sort_values(prob_cols)
if dupes.empty:
    print("None found.")
else:
    print(f"{len(dupes)} files share a probability vector with at least one other file:")
    print(dupes[["file_name", "true_model", "task"] + prob_cols].to_string(index=False))

# --- Low-confidence predictions ---
print("\n" + "=" * 50)
print("LOW CONFIDENCE PREDICTIONS (max_prob < 0.6)")
print("=" * 50)
low_conf = df[df["max_prob"] < 0.6].sort_values("max_prob")
print(f"{len(low_conf)} files:")
print(low_conf[["file_name", "true_model", "predicted_model", "max_prob"]].to_string(index=False))

# --- Overall accuracy ---
print("\n" + "=" * 50)
print(f"OVERALL ACCURACY: {df['correct'].mean():.1%}  ({df['correct'].sum()}/{len(df)})")
print("=" * 50)
