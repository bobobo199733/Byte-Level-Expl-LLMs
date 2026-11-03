"""Sandbox-only execution checker for paired original/edited Python functions.

This file MUST be executed INSIDE an externally isolated container. Never
import or run it in the analysis host process. Exit nonzero on any mismatch.
"""
import json
import sys
import traceback
from pathlib import Path


def invoke(fn, value):
    return fn(*value) if isinstance(value, list) else fn(value)


def outcome(fn, inp):
    try:
        return {"ok": True, "value": invoke(fn, inp)}
    except BaseException as exc:
        return {"ok": False, "exception": type(exc).__name__}


def acceptable(result, expected, multiple=False):
    if not result["ok"]:
        return False
    if multiple and isinstance(expected, list):
        return result["value"] in expected
    return result["value"] == expected


def verify(src, name, meta):
    namespace = {"__name__": "__rq2_sandbox__"}
    exec(compile(src, "generated.py", "exec"), namespace)
    fn = namespace[name]
    if not callable(fn):
        raise ValueError("Target not callable")
    results = []
    for inp, expected in meta.get("valid_cases", []):
        got = outcome(fn, inp)
        if not acceptable(got, expected, meta.get("allow_multiple_expected", False)):
            raise AssertionError("A valid test did not meet task's expected output")
        results.append(got)
    for inp in meta.get("invalid_cases", []):
        got = outcome(fn, inp)
        if got.get("exception") != meta.get("expected_exception", "ValueError"):
            raise AssertionError("An invalid-case test did not raise expected exception")
        results.append(got)
    if not results:
        raise ValueError("No task tests: cannot certify behavioral equivalence")
    return results


def main():
    try:
        original = Path("/work/original.py").read_text()
        edited = Path("/work/edited.py").read_text()
        meta = json.loads(Path("/work/meta.json").read_text())
        name = meta["function_name"]
        a = verify(original, name, meta)
        b = verify(edited, name, meta)
        if a != b:
            raise AssertionError("Original/edited outputs differ on task tests")
        print(json.dumps({"accepted": True, "tests": len(a)}))
    except BaseException as exc:
        print(json.dumps({"accepted": False, "reason": type(exc).__name__, "message": str(exc)[:180]}))
        sys.exit(2)


if __name__ == "__main__":
    main()
