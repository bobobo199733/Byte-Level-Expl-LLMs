"""Host-side safe launcher; never evaluates the generated source on host."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

WORKER = Path(__file__).with_name("sandbox_validation_worker.py")
MARKER = "RQ2_VALIDATION_JSON="


def digest(file: Path):
    sha = hashlib.sha256()
    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(2**20), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_sandbox(image: Path):
    image = image.resolve()
    if not image.is_file():
        raise FileNotFoundError(f"Python 3.13 Apptainer image not found: {image}")
    if not WORKER.is_file():
        raise FileNotFoundError(WORKER)
    return image


def run_in_sandbox(image: Path, original: Path, meta: Path,
                   edited: str | None = None, timeout: int = 20) -> dict:
    image = verify_sandbox(image)
    if timeout < 4:
        raise ValueError("Timeout must be at least 4 seconds")
    with tempfile.TemporaryDirectory(prefix="rq2_validate_") as temp:
        folder = Path(temp)
        (folder / "original.py").write_bytes(original.read_bytes())
        (folder / "meta.json").write_bytes(meta.read_bytes())
        (folder / "worker.py").write_bytes(WORKER.read_bytes())
        if edited is not None:
            (folder / "edited.py").write_text(edited, encoding="utf-8")
        cmd = [
            "apptainer", "exec", "--containall", "--cleanenv",
            "--net", "--network", "none", "--no-home",
            "--bind", f"{folder.resolve()}:/work:ro",
            str(image), "python3", "/work/worker.py",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            return {"ok": False, "error_type": "sandbox_timeout"}
        except OSError as exc:
            return {"ok": False, "error_type": "sandbox_launch_failed",
                    "error": str(exc)[:160]}
        report_lines = [
            line[len(MARKER):] for line in result.stdout.splitlines()
            if line.startswith(MARKER)
        ]
        if result.returncode != 0 or len(report_lines) != 1:
            return {"ok": False, "error_type": "sandbox_runtime_failed",
                    "returncode": result.returncode, "stderr": result.stderr[-300:]}
        try:
            data = json.loads(report_lines[0])
        except json.JSONDecodeError:
            return {"ok": False, "error_type": "invalid_sandbox_report"}
        if not isinstance(data, dict) or not isinstance(data.get("ok"), bool):
            return {"ok": False, "error_type": "invalid_sandbox_schema"}
        return data
