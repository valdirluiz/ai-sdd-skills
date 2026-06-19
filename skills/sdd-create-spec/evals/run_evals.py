#!/usr/bin/env python3
"""
Eval runner for the sdd-create-spec skill validator.

Runs validate_spec.py against each fixture in cases/ and verifies the output
matches the expected.json contract. Exits 0 if all evals pass, 1 otherwise.

Usage:
    python evals/run_evals.py [--verbose]
"""

import json
import subprocess
import sys
from pathlib import Path

VALIDATOR = Path(__file__).parent.parent / "validate_spec.py"
CASES_DIR = Path(__file__).parent / "cases"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run_validator(spec_path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(spec_path)],
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": f"Validator produced non-JSON output: {result.stdout!r}"}


def check_case(case_dir: Path, verbose: bool) -> tuple[bool, str]:
    spec = case_dir / "spec.md"
    expected_file = case_dir / "expected.json"

    if not spec.exists():
        return False, f"Missing spec.md in {case_dir.name}"
    if not expected_file.exists():
        return False, f"Missing expected.json in {case_dir.name}"

    expected = json.loads(expected_file.read_text())
    actual = run_validator(spec)

    if "error" in actual:
        return False, f"Validator error: {actual['error']}"

    failures: list[str] = []

    # Check valid/invalid expectation
    if actual["valid"] != expected["expect_valid"]:
        failures.append(
            f"expected valid={expected['expect_valid']} but got valid={actual['valid']}"
        )

    # Collect fired rule IDs from actual output
    fired_rules = {issue["rule"] for issue in actual.get("issues", [])}

    # Rules that MUST appear
    for rule in expected.get("expect_rules", []):
        if rule not in fired_rules:
            failures.append(f"expected rule '{rule}' to fire but it did not")

    # Rules that MUST NOT appear
    for rule in expected.get("reject_rules", []):
        if rule in fired_rules:
            failures.append(f"rule '{rule}' fired but should not have")

    description = expected.get("description", case_dir.name)

    if failures:
        detail = "\n    ".join(failures)
        if verbose:
            detail += f"\n    actual output: {json.dumps(actual, indent=2)}"
        return False, f"{description}\n    {detail}"

    return True, description


def main() -> None:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if not VALIDATOR.exists():
        print(f"{RED}ERROR:{RESET} Validator not found at {VALIDATOR}", file=sys.stderr)
        sys.exit(1)

    cases = sorted(d for d in CASES_DIR.iterdir() if d.is_dir())
    if not cases:
        print(f"{YELLOW}No eval cases found in {CASES_DIR}{RESET}")
        sys.exit(0)

    passed = 0
    failed = 0

    print(f"\n{BOLD}sdd-create-spec eval suite{RESET}  ({len(cases)} cases)\n")

    for case in cases:
        ok, message = check_case(case, verbose)
        status = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
        label = case.name
        print(f"  {status}  {label}")
        if not ok or verbose:
            for line in message.splitlines():
                print(f"       {line}")
        if ok:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    print(f"\n{BOLD}Results:{RESET} {passed}/{total} passed", end="")
    if failed:
        print(f"  {RED}({failed} failed){RESET}")
    else:
        print(f"  {GREEN}(all passed){RESET}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
