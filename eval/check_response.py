#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_CASES_DIR = Path(__file__).with_name("cases")
REGEX_FLAGS = re.IGNORECASE | re.MULTILINE | re.DOTALL


def load_case(case_path: Path) -> dict:
    with case_path.open("r", encoding="utf-8") as handle:
        case = json.load(handle)
    case.setdefault("required_patterns", [])
    case.setdefault("forbidden_patterns", [])
    return case


def evaluate_case(case: dict, response_text: str) -> list[tuple[bool, str]]:
    results: list[tuple[bool, str]] = []

    for rule in case["required_patterns"]:
        matched = re.search(rule["pattern"], response_text, REGEX_FLAGS) is not None
        results.append((matched, f"required: {rule['description']}"))

    for rule in case["forbidden_patterns"]:
        matched = re.search(rule["pattern"], response_text, REGEX_FLAGS) is None
        results.append((matched, f"forbidden: {rule['description']}"))

    return results


def render_report(case_name: str, response_path: Path, results: list[tuple[bool, str]]) -> bool:
    passed = all(ok for ok, _ in results)
    status = "PASS" if passed else "FAIL"
    print(f"{status}  {case_name}  {response_path}")
    for ok, message in results:
        marker = "ok " if ok else "bad"
        print(f"  [{marker}] {message}")
    return passed


def find_case_path(case_name: str, cases_dir: Path) -> Path:
    case_path = cases_dir / f"{case_name}.json"
    if not case_path.exists():
        raise FileNotFoundError(f"Unknown case: {case_name}")
    return case_path


def run_single(case_name: str, response_path: Path, cases_dir: Path) -> bool:
    case = load_case(find_case_path(case_name, cases_dir))
    response_text = response_path.read_text(encoding="utf-8")
    results = evaluate_case(case, response_text)
    return render_report(case["name"], response_path, results)


def run_directory(responses_dir: Path, cases_dir: Path) -> bool:
    all_passed = True
    for case_path in sorted(cases_dir.glob("*.json")):
        case = load_case(case_path)
        response_path = responses_dir / f"{case['name']}.md"
        if not response_path.exists():
            print(f"FAIL  {case['name']}  missing response file {response_path}")
            all_passed = False
            continue

        response_text = response_path.read_text(encoding="utf-8")
        results = evaluate_case(case, response_text)
        all_passed &= render_report(case["name"], response_path, results)
    return all_passed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lightweight response checker for canonical clean-viz prompts."
    )
    parser.add_argument(
        "response",
        nargs="?",
        type=Path,
        help="Path to a saved markdown response for single-case evaluation.",
    )
    parser.add_argument(
        "--case",
        help="Case name from eval/cases (required for single-response mode).",
    )
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=DEFAULT_CASES_DIR,
        help="Directory containing JSON case specifications.",
    )
    parser.add_argument(
        "--responses-dir",
        type=Path,
        help="Directory containing one markdown file per case, named <case>.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.responses_dir:
        passed = run_directory(args.responses_dir, args.cases_dir)
        return 0 if passed else 1

    if not args.case or not args.response:
        print("Single-response mode requires both --case and a response path.", file=sys.stderr)
        return 2

    passed = run_single(args.case, args.response, args.cases_dir)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
