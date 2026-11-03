"""INSIDE-CONTAINER ONLY: isolated correctness or paired behavioral checks.

Never execute archived source on the host. The host driver mounts a read-only
/work folder with original.py, optional edited.py, meta.json, and this worker.
All cases including explicit_cases are scored; a failure is not conflated with
a source-edit mismatch. Differential probes test observed behavior only.
"""
import contextlib
import copy
import io
import json
import math
import os
import resource
import signal
import sys
from pathlib import Path

if sys.version_info[:2] != (3, 13):
    raise SystemExit("Requires isolated CPython 3.13")
resource.setrlimit(resource.RLIMIT_CPU, (12, 13))
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024**2, 4 * 1024**2))


class CaseTimeout(Exception):
    pass


def alarm_handler(_sig, _frame):
    raise CaseTimeout()


signal.signal(signal.SIGALRM, alarm_handler)


def safe_value(value, depth=0):
    if depth > 7:
        return {"type": type(value).__name__, "repr": repr(value)[:200]}
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, (list, tuple)):
        return [safe_value(v, depth + 1) for v in value[:300]]
    if isinstance(value, dict):
        return {str(k): safe_value(v, depth + 1) for k, v in list(value.items())[:300]}
    if isinstance(value, (set, frozenset)):
        return sorted((safe_value(v, depth + 1) for v in value), key=repr)
    return {"type": type(value).__name__, "repr": repr(value)[:200]}


def build_callable(source, func):
    namespace = {"__name__": "__rq2_sandbox__", "__builtins__": __builtins__}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(compile(source, "generated.py", "exec"), namespace)
    fn = namespace.get(func)
    if not callable(fn):
        raise ValueError("Target function not callable")
    return fn


def execute(fn, argument):
    try:
        signal.setitimer(signal.ITIMER_REAL, 2.0)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            # Keep existing task convention: a list represents positional args.
            result = fn(*copy.deepcopy(argument)) if isinstance(argument, list) else fn(copy.deepcopy(argument))
        return {"kind": "return", "value": safe_value(result)}
    except BaseException as exc:
        return {"kind": "exception", "type": type(exc).__name__}
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def cases(meta):
    ret = []
    for category in ("valid_cases", "explicit_cases", "tests"):
        for index, case in enumerate(meta.get(category, [])):
            if not isinstance(case, list) or len(case) != 2:
                raise ValueError(f"Malformed {category} case {index}")
            ret.append((category, case[0], case[1]))
    for index, value in enumerate(meta.get("invalid_cases", [])):
        ret.append(("invalid_cases", value, meta.get("expected_exception", "ValueError")))
    return ret


def correct(result, category, expected, meta):
    if category == "invalid_cases":
        return result["kind"] == "exception" and result["type"] == expected
    if result["kind"] != "return":
        return False
    actual = result["value"]
    expected_value = safe_value(expected)
    if meta.get("allow_multiple_expected", False) and isinstance(expected, list):
        return any(actual == safe_value(v) for v in expected)
    return actual == expected_value


def generate_probes(meta, cap=40):
    """Deterministic domain-UNVERIFIED probes derived from example arguments.

    They are only for DIFFERENTIAL testing, NEVER correctness. Some may be
    outside the task domain; therefore agreement is evidence not proof.
    """
    seeds = [arg for section, arg, _ in cases(meta) if section != "invalid_cases"]
    existing = {json.dumps(x, sort_keys=True) for x in seeds}
    output = []
    def variants(v):
        if isinstance(v, bool):
            return [not v]
        if isinstance(v, int) and not isinstance(v, bool):
            return list(dict.fromkeys([0, 1, -1, v+1, v-1]))
        if isinstance(v, str):
            return list(dict.fromkeys(["", v + v[-1:] if v else "a", v[:max(0,len(v)//2)]]))
        if isinstance(v, list):
            return [[], v[:max(0,len(v)//2)], v + v[-1:] if v else [0]]
        return []
    for val in seeds:
        if len(output) >= cap:
            break
        if isinstance(val, list):
            for i, arg in enumerate(val):
                for variant in variants(arg):
                    new = copy.deepcopy(val)
                    new[i] = variant
                    key = json.dumps(new, sort_keys=True)
                    if key not in existing:
                        existing.add(key)
                        output.append(new)
                        if len(output) >= cap:
                            break
                if len(output) >= cap:
                    break
        else:
            for variant in variants(val):
                key = json.dumps(variant, sort_keys=True)
                if key not in existing:
                    existing.add(key)
                    output.append(variant)
                    if len(output) >= cap:
                        break
    return output


def evaluate(src, meta):
    provided = cases(meta)
    if not provided:
        raise ValueError("no_executable_task_tests")
    fn = build_callable(src, meta["function_name"])
    rows = []
    for category, argument, expected in provided:
        observed = execute(fn, argument)
        rows.append({"case_category": category, "pass": correct(observed, category, expected, meta),
                     "observed": observed})
    return rows, fn


def main():
    try:
        # Test fixtures may override this directory; production Apptainer
        # uses --cleanenv and the fixed read-only /work mount.
        work = Path(os.environ.get("RQ2_WORK_ROOT", "/work"))
        meta = json.loads((work / "meta.json").read_text())
        original = (work / "original.py").read_text()
        original_results, orig_func = evaluate(original, meta)
        if not original_results:
            raise ValueError("No task tests provided")
        outcome = {
            "ok": True,
            "n_cases": len(original_results),
            "n_pass": sum(r["pass"] for r in original_results),
            "n_failed": sum(not r["pass"] for r in original_results),
            "by_category": {
                kind: {
                    "n": sum(r["case_category"] == kind for r in original_results),
                    "passed": sum(r["pass"] and r["case_category"] == kind for r in original_results)
                } for kind in ("valid_cases", "explicit_cases", "tests", "invalid_cases")
            },
            "all_pass": all(r["pass"] for r in original_results),
        }
        edited_file = work / "edited.py"
        if edited_file.exists():
            edited_results, edited_fn = evaluate(edited_file.read_text(), meta)
            task_matches = all(a["observed"] == b["observed"] for a,b in zip(original_results, edited_results))
            probes = generate_probes(meta)
            differential = [(execute(orig_func, v), execute(edited_fn, v)) for v in probes]
            disagreements = sum(a != b for a,b in differential)
            outcome.update({
                "edit_n_pass": sum(r["pass"] for r in edited_results),
                "edit_all_pass": all(r["pass"] for r in edited_results),
                "task_outputs_match": task_matches,
                "n_probe_cases": len(probes),
                "n_probe_disagreements": disagreements,
                "behavior_matches_on_tests_and_probes": task_matches and disagreements == 0,
                "probes_domain_validated": False,
            })
        print("RQ2_VALIDATION_JSON=" + json.dumps(outcome, allow_nan=False), flush=True)
    except BaseException as exc:
        print("RQ2_VALIDATION_JSON=" + json.dumps({
            "ok": False, "error_type": type(exc).__name__,
            "error": str(exc)[:150],
        }), flush=True)


if __name__ == "__main__":
    main()
