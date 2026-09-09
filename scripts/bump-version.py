#!/usr/bin/env python3
"""Bump the package version across every manifest and the skill frontmatter.

Usage: python3 scripts/bump-version.py 1.0.1 [--from 1.0.0]

Updates metadata.version in skills/blunt/SKILL.md (and the .cursor mirror),
package.json, .claude-plugin/plugin.json, .codex-plugin/plugin.json,
kimi.plugin.json, qwen-extension.json, and gemini-extension.json. Reminds you
about CHANGELOG.md, which stays hand-written.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSIONED_FILES = (
    "package.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "kimi.plugin.json",
    "qwen-extension.json",
    "gemini-extension.json",
)
SKILL_FILES = (
    "skills/blunt/SKILL.md",
    ".cursor/skills/blunt/SKILL.md",
)

def current_version() -> str:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    return str(package["version"])

def replace_in_file(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf'(?<![0-9.]){re.escape(old)}(?![0-9.])', new, text
    )
    if count == 0:
        raise SystemExit(f"{path.relative_to(ROOT)}: no occurrence of {old}")
    path.write_text(updated, encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {count} replacement(s)")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("new_version", help="new version, e.g. 1.0.1")
    parser.add_argument("--from", dest="old_version", default=None)
    args = parser.parse_args()

    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", args.new_version):
        raise SystemExit(f"not a semantic version: {args.new_version}")

    old = args.old_version or current_version()
    if old == args.new_version:
        raise SystemExit(f"version is already {args.new_version}")

    for relative in VERSIONED_FILES:
        replace_in_file(ROOT / relative, old, args.new_version)
    for relative in SKILL_FILES:
        replace_in_file(ROOT / relative, old, args.new_version)

    result = subprocess_ok()
    if not result:
        raise SystemExit("bump applied but validation failed; inspect the diff")

    print()
    print("Next:")
    print(f"1. Add a CHANGELOG.md entry for {args.new_version} (or move the Unreleased block).")
    print(f"2. Commit and tag: git commit -am 'v{args.new_version}' && git tag v{args.new_version}")
    print("3. Push the tag; the release workflow drafts the GitHub release.")
    return 0

def subprocess_ok() -> bool:
    import subprocess
    result = subprocess.run(
        ["python3", str(ROOT / "scripts" / "validate-package.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout + result.stderr, file=sys.stderr)
        return False
    print(result.stdout.strip())
    return True

if __name__ == "__main__":
    raise SystemExit(main())