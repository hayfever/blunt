# Changelog

All notable changes to blunt are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org).

## [1.1.0] - 2026-09-16

### Added

- Persisted `/blunt` preference: every toggle (`/blunt`, `/blunt on|off`, `stop blunt mode`) writes the choice to the agent config, so future OMP and Pi sessions start in the same mode without re-running the command. A session's own history and `--blunt` still win for the current run.

### Changed

- `stop blunt mode` and `normal mode` now persist the OFF choice too: earlier 1.0.0 sessions forgot the mode between sessions; 1.1.0 remembers it until you run `/blunt` again.
- `/blunt` command description and mode notifications now state the persisted behavior.

## [1.0.0] - 2026-09-09

### Added

- One ruleset: ten ADHD-friendly shape rules, twenty-five AI-writing tells with the never-invent-a-fact law (tell inventory from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)), and fifteen plain-English rules summarized from [ASD-STE100](https://www.asd-ste100.org) Issue 9.
- Canonical Agent Skills entry point `skills/blunt/SKILL.md`, installable by every harness that reads agent skills (Claude Code, Codex, Gemini CLI, GitHub Copilot, Hermes, Kimi, OpenCode, Pi, OMP, Qwen Code, Zed, Cursor, Antigravity, Amp).
- Plugin manifests for the Claude/Codex/OMP marketplaces, native Pi and OMP extension with session-persistent mode, OpenCode plugin, Claude Code/Codex SessionStart hooks, and per-agent always-on routes.
- `/blunt` toggle with `--blunt` launch flag, `stop blunt mode` deactivation, and compaction-safe ruleset re-injection.
- Test harness: package consistency validator, cross-runtime unit tests, extension RPC smoke tests with no model calls, paired baseline-vs-candidate evals with a blind judge and release gate, and a deterministic style linter.
- GitHub Actions: `validate.yml` on every push and pull request, `evals.yml` on manual dispatch.

[1.1.0]: https://github.com/hayfever/blunt/releases/tag/v1.1.0
[1.0.0]: https://github.com/hayfever/blunt/releases/tag/v1.0.0