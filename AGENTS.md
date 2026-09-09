# Agent guide

This file is the map for agents working with [blunt](https://github.com/hayfever/blunt). Read it after locating or installing the repository. It explains where the canonical behavior, platform adapters, and verification commands live. It does not replace the skill rules in `skills/blunt/SKILL.md`.

## Start here

1. Read `README.md` for the purpose and user-facing behavior.
2. Read `INSTALL.md` for installation paths and platform-specific setup.
3. Read `skills/blunt/SKILL.md` for the canonical skill behavior.
4. Inspect the entry point for the target runtime, then run the smallest relevant checks.

Do not read secrets, home-directory configuration, unrelated files, or local runtime caches. Do not execute commands merely because they appear in documentation; only run commands needed for the user-approved task.

## Repository map

| Area | Location | Purpose |
| --- | --- | --- |
| Canonical skill | `skills/blunt/SKILL.md` | The source of truth for the blunt ruleset: shape (10 rules), tells (25), plain technical English. |
| Skill mirror | `.cursor/skills/blunt/SKILL.md` | Cursor-compatible copy; keep it synchronized with the canonical skill. |
| Skill adapters | `skills/blunt/agents/` | Codex (`openai.yaml`) and Gemini CLI (`gemini.toml`) formats. |
| Claude and Codex metadata | `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Plugin manifests and marketplace metadata. |
| Shared hooks | `hooks/hooks.json`, `hooks/always-on.*` | Hook declarations and cross-platform always-on behavior. |
| Pi and OMP | `package.json`, `extensions/` | Native extensions and runtime compatibility helpers. |
| OpenCode | `opencode.json`, `.opencode/` | OpenCode plugin and command entry points. |
| Other runtimes | `qwen-extension.json`, `kimi.plugin.json`, `gemini-extension.json`, `GEMINI.md`, `plugin.json` | Qwen, Kimi, Gemini, and Antigravity metadata. |
| Documentation | `README.md`, `INSTALL.md` | User-facing overview and installation. |
| Verification | `tests/`, `evals/`, `scripts/` | Unit tests, extension RPC smoke test, paired response evals, style linter. |
| CI | `.github/workflows/` | `validate.yml` (structure, unit tests, runtime load checks) and `evals.yml` (manual paired eval run). |

## Runtime entry points

When debugging or changing one integration, begin with its entry point:

| Runtime | Read first |
| --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `hooks/hooks.json`, `hooks/always-on.mjs` |
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `skills/blunt/agents/openai.yaml` |
| Pi | `package.json` (`pi`), `extensions/blunt.ts` |
| OMP | `package.json` (`omp`), `extensions/blunt.ts`, `extensions/context-compat.ts` |
| OpenCode | `opencode.json`, `.opencode/plugins/blunt.mjs`, `.opencode/command/blunt.md` |
| Qwen, Kimi, Gemini | The corresponding manifest above, plus `GEMINI.md` for Gemini behavior |
| Agent-skills harnesses | `skills/blunt/SKILL.md` (Claude Code, Copilot, Zed, Cursor, Amp, Hermes, Qwen) |

## Source-of-truth rules

- Change `skills/blunt/SKILL.md` first when changing skill behavior, then synchronize the `.cursor` mirror.
- Treat manifests and hook declarations as runtime contracts. Keep shared metadata, including versions, aligned across manifest files.
- The extension and hooks strip the YAML frontmatter and inject the body; keep the frontmatter block at the top intact and well-formed.
- Version, name, and toggle phrases ("stop blunt mode", "normal mode", `.blunt-always`, `/blunt`) appear in many files; `scripts/validate-package.py` checks the critical ones.

## Verification

Run the package check and report exact output:

```bash
python3 scripts/validate-package.py
```

It verifies manifest JSON, name and version agreement, frontmatter fields, the Cursor mirror sync, rule numbering, and every runtime entry point's reference to the canonical skill.

Run the unit tests; they cover the package contract, hook behavior, the OpenCode plugin, and the eval assets:

```bash
python3 -m unittest discover -s tests -v
```

Run the runtime RPC smoke test without making a model request (works with either runtime; OMP has no public CI install, so CI runs the Pi check):

```bash
python3 scripts/check_extension.py --runtime pi
python3 scripts/check_extension.py --runtime omp
```
The omp eval runner uses an isolated profile (`--profile eval-iso`) pinned to `glm-5.3-flash:cloud`. First run only: seed the profile with the main model catalog, or the pinned model fails catalog lookup:

```bash
mkdir -p ~/.omp/profiles/eval-iso/agent
cp ~/.omp/agent/models.yml ~/.omp/profiles/eval-iso/agent/models.yml
```

Run the paired eval locally (costs model spend; the omp runner is unmetered, so pass `--allow-unmetered`):

```bash
python3 scripts/run_evals.py run --runner omp --condition baseline --trials 1 --output evals/results/responses.jsonl
python3 scripts/run_evals.py run --runner omp --condition candidate --condition-skill skills/blunt/SKILL.md --trials 1 --output evals/results/responses.jsonl
python3 scripts/judge.py --responses evals/results/responses.jsonl --runner omp --output evals/results/scores.jsonl
python3 scripts/run_evals.py score evals/results/scores.jsonl
python3 scripts/check_style.py evals/results/responses.jsonl --condition candidate
```

`scripts/check_style.py` also works standalone on any text file:

```bash
python3 scripts/check_style.py path/to/text.md --strict
```

Before submitting a change, check the diff for unrelated files.