#!/usr/bin/env python3
"""Deterministic style check for blunt eval responses.

Catches the mechanical tells without a judge model: chatbot residue, staged
openers and closers, dashes used as connectors, curly quotes, Latin
abbreviations, not-X-but-Y contrasts, and over-long lists. Code fences, inline
code, and commands are exempt; the rules in skills/blunt/SKILL.md exclude them
too.

Input is the responses JSONL written by scripts/run_evals.py, or one file of
plain text. Exit code 1 only with --strict.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Staged openers (tell 4) and chatbot residue (tells 10 and 22).
OPENER_PATTERNS = (
    (r"^\s*(great question|sure!|of course!|certainly!|you'?re absolutely right)",
     "chatbot opener at the start"),
    (r"^\s*(let'?s dive in|let'?s break this down|here'?s what you need to know)",
     "staged run-up opener"),
)
CLOSER_PATTERNS = (
    (r"hope this helps", "closing pleasantry"),
    (r"let me know if", "closing pleasantry"),
    (r"happy to clarify", "closing pleasantry"),
    (r"feel free to ask", "closing pleasantry"),
    (r"anything else\?", "closing offer"),
)
ONE_LINE_CLOSERS = (
    (r"\bread that again\b", "one-line closer"),
    (r"\blet that sink in\b", "one-line closer"),
)
PUNCTUATION_PATTERNS = (
    (r"—|–", "em or en dash used as a connector"),
    (r" -- ", "spaced double hyphen used as a dash"),
    (r"[“”‘’]", "curly quotation mark"),
)
LATIN_PATTERNS = (
    (r"\be\.g\.", "Latin abbreviation"),
    (r"\bi\.e\.", "Latin abbreviation"),
    (r"\betc\.", "Latin abbreviation"),
)
CONTRAST_PATTERNS = (
    (r"\bnot (?:just|only|merely) [^,.;:]{1,60}, (?:but|it'?s) ", "not-X-but-Y contrast"),
    (r"\bit'?s not [^,.;:]{1,60}, it'?s ", "not-X-but-Y contrast"),
    (r"\bthis (?:does not|doesn'?t) mean [^.]{1,80}\. it means ", "split not-X-but-Y contrast"),
)

BULLET_PREFIXES = tuple(f"{number}. " for number in range(1, 10)) + ("- ", "* ")


def strip_code(text: str) -> str:
    """Drop fenced code blocks and inline code spans from the text."""
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lines.append(line)
    clean = "\n".join(lines)
    return clean.replace("`", "")


def check_text(text: str) -> list[str]:
    clean = strip_code(text)
    violations: list[str] = []

    # Curly quotes are a tell even inside quoted spans; every other pattern is
    # exempt inside quotation marks, mirroring the skill's quoted-text rule.
    if re.search(PUNCTUATION_PATTERNS[2][0], clean):
        violations.append(PUNCTUATION_PATTERNS[2][1])

    prose = re.sub(r'"[^"\n]{0,300}"', "", clean)

    start = prose.lstrip()[:160]
    for pattern, label in OPENER_PATTERNS:
        if re.search(pattern, start, re.IGNORECASE):
            violations.append(label)
            break

    for pattern, label in (*CLOSER_PATTERNS, *ONE_LINE_CLOSERS, *LATIN_PATTERNS,
                           *CONTRAST_PATTERNS, *PUNCTUATION_PATTERNS[:2]):
        if re.search(pattern, prose, re.IGNORECASE):
            violations.append(label)

    items = 0
    for line in clean.splitlines():
        if line.lstrip().startswith(BULLET_PREFIXES):
            items += 1
            continue
        if items:
            if items > 5:
                violations.append(f"list of {items} items (cap is 5)")
            items = 0
    if items > 5:
        violations.append(f"list of {items} items (cap is 5)")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="responses JSONL file or plain text file")
    parser.add_argument("--condition", default=None, help="only check rows of this condition")
    parser.add_argument("--report", help="write a JSON report to this path")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any violation")
    args = parser.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8")
    rows: list[dict] = []
    if args.input.endswith(".jsonl"):
        for number, line in enumerate(raw.splitlines(), start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if args.condition and row.get("condition") != args.condition:
                continue
            rows.append(row)
    else:
        rows = [{"case_id": Path(args.input).name, "trial": 0, "response": raw}]

    report: dict[str, list[str]] = {}
    violations = 0
    for row in rows:
        found = check_text(row.get("response", ""))
        report[f"{row.get('case_id', '?')}/trial {row.get('trial', '?')}"] = found
        violations += len(found)
        for item in found:
            print(f"{row.get('case_id', '?')}/trial {row.get('trial', '?')}: {item}")

    if args.report:
        Path(args.report).write_text(
            json.dumps({"violations": violations, "rows": report}, indent=2),
            encoding="utf-8",
        )

    if not rows:
        print("no rows to check")
        return 0

    print(f"checked {len(rows)} row(s): {violations} violation(s)")
    return 1 if args.strict and violations else 0


if __name__ == "__main__":
    raise SystemExit(main())