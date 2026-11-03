import numpy as np
import json
from pathlib import Path

BASE_DIR    = Path(__file__).resolve().parent.parent
shap_values = np.load(BASE_DIR / "shap_bytecode" / "shap_values_multiclass.npy")
features    = json.loads((BASE_DIR / "shap_bytecode" / "feature_names.json").read_text())

mean_abs = np.abs(shap_values).mean(axis=(0, 2)) if shap_values.ndim == 3 else np.abs(shap_values).mean(axis=0)

top_idx   = np.argsort(mean_abs)[::-1][:40]
top_bytes = [features[i] for i in top_idx]
print(top_bytes)
