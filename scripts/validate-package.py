#!/usr/bin/env python3
"""Check blunt's package files without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILL_PATH = ROOT / "skills" / "blunt" / "SKILL.md"
MIRROR_PATH = ROOT / ".cursor" / "skills" / "blunt" / "SKILL.md"

JSON_MANIFESTS = (
    "package.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "kimi.plugin.json",
    "qwen-extension.json",
    "gemini-extension.json",
    "opencode.json",
    "hooks/hooks.json",
)

JSON_MANIFESTS_WITH_NAME = (
    "package.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "kimi.plugin.json",
    "qwen-extension.json",
    "gemini-extension.json",
)

def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {error}")

def require_match(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match

SKILL = read(SKILL_PATH)

frontmatter = require_match(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "skills/blunt/SKILL.md must begin with YAML metadata",
).group(1)

require_match(
    re.search(r"(?m)^name: blunt$", frontmatter),
    "Frontmatter must declare name: blunt",
)
require_match(
    re.search(r"(?m)^disable-model-invocation: true$", frontmatter),
    "Frontmatter must declare disable-model-invocation: true",
)
for unsupported_field in ("version:", "compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(unsupported_field)}", frontmatter):
        raise SystemExit(f"Remove unsupported YAML field: {unsupported_field[:-1]}")

skill_version = require_match(
    re.search(r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', frontmatter),
    "Add metadata.version to SKILL.md as a three-part version",
).group(1)

if len(SKILL.splitlines()) > 400:
    raise SystemExit("Keep skills/blunt/SKILL.md at 400 lines or fewer")

# Canonical skill and the Cursor mirror must be byte-identical.
if not MIRROR_PATH.exists():
    raise SystemExit(".cursor/skills/blunt/SKILL.md is missing; copy the canonical skill there")
if SKILL != read(MIRROR_PATH):
    raise SystemExit(".cursor/skills/blunt/SKILL.md is out of sync with skills/blunt/SKILL.md")

# Only one skill, and its folder name must match the frontmatter name.
skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if skill_files != {Path("skills/blunt/SKILL.md"), Path(".cursor/skills/blunt/SKILL.md")}:
    raise SystemExit(f"Unexpected SKILL.md locations: {sorted(skill_files)}")

# All manifests parse and agree on name and version.
package_versions = {skill_version}
for relative in JSON_MANIFESTS:
    path = ROOT / relative
    try:
        json.loads(read(path))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Fix the JSON in {relative}: {error}")

for relative in JSON_MANIFESTS_WITH_NAME:
    data = json.loads(read(ROOT / relative))
    name = data.get("name")
    if name != "blunt":
        raise SystemExit(f"{relative} must declare name: blunt (found: {name!r})")
    if isinstance(data.get("version"), str):
        package_versions.add(data["version"])
if len(package_versions) != 1:
    raise SystemExit(
        f"Use one package version in all files: {sorted(package_versions)}"
    )

package = json.loads(read(ROOT / "package.json"))
extension = ["./extensions/blunt.ts"]
if package.get("omp") != {"extensions": extension}:
    raise SystemExit("package.json must declare omp extensions ./extensions/blunt.ts")
if package.get("pi") != {"extensions": extension, "skills": ["./skills"]}:
    raise SystemExit('package.json must declare pi extensions and skills ["./skills"]')
for relative in extension:
    if not (ROOT / relative[2:]).is_file():
        raise SystemExit(f"Declared extension is missing: {relative}")

# Rule numbering: Part 1 has rules 1 to 10, Part 2 has 25 tells, in order.
shape_rules = [
    int(number) for number in re.findall(r"(?m)^## ([0-9]+)\. ", SKILL)
]
if shape_rules != list(range(1, 11)):
    raise SystemExit(f"Number the ten shape rules 1 to 10 in order: {shape_rules}")

tells_section = SKILL.split("## The tells")[1].split("## When not to act")[0]
tells = [
    int(number) for number in re.findall(r"(?m)^([0-9]+)\. \*\*", tells_section)
]
if tells != list(range(1, 26)):
    raise SystemExit(f"Number the tells 1 to 25 without gaps: {tells}")

# Runtime entry points must point at the canonical skill and use blunt phrases.
for relative, marker in (
    ("hooks/always-on.mjs", 'join(scriptDir, "..", "skills", "blunt", "SKILL.md")'),
    ("hooks/always-on.sh", "skills/blunt/SKILL.md"),
    ("hooks/always-on.ps1", "../skills/blunt/SKILL.md"),
    (".opencode/plugins/blunt.mjs", "'blunt', 'SKILL.md'"),
    ("extensions/blunt.ts", '"blunt",'),
    ("GEMINI.md", "@./skills/blunt/SKILL.md"),
):
    if marker not in read(ROOT / relative):
        raise SystemExit(f"{relative} must reference the canonical skill: {marker}")

if not (ROOT / ".opencode/command/blunt.md").is_file():
    raise SystemExit(".opencode/command/blunt.md is missing")

openai_yaml = read(ROOT / "skills" / "blunt" / "agents" / "openai.yaml")
require_match(
    re.search(r"(?m)^  allow_implicit_invocation: false$", openai_yaml),
    "skills/blunt/agents/openai.yaml must set allow_implicit_invocation: false",
)

print(f"blunt package v{skill_version} is valid")