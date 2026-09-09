[![Validate](https://github.com/hayfever/blunt/actions/workflows/validate.yml/badge.svg)](https://github.com/hayfever/blunt/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill version](https://img.shields.io/badge/skill-v1.0.0-2563EB)](CHANGELOG.md)

# blunt

Lead with the action. Sound like a person. Write plain English.

Three parts:

- **Shape.** Ten rules that shape every response for an ADHD reader: action first, steps numbered, no "Hope this helps!"
- **Sound human.** 25 patterns that mark text as machine-made, from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Strip them; keep every supported claim; never invent a fact.
- **Stay plain.** Simplified Technical English, the controlled writing standard behind aerospace maintenance docs: active voice, imperative steps, 20-word steps, one term per item, no semicolons.

The standard itself is free to download from ASD; this skill summarizes its Part 1 writing rules and does not reproduce the dictionary.

## Before

> Great question! Let me think about this. It's not just about the middleware, it's about trust. Your auth flow has a few moving pieces: the middleware, the token verification, and the cookie handling. Looking at `src/auth.ts`, the `verifyToken` function (around lines 42-58) seems to be using an older `jsonwebtoken` API — one approach would be to update the package. After making the change, you'd want to run the auth tests to confirm nothing breaks. Hope this helps! Let me know if you want to dig deeper.

## After

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42 to 58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Test fails at `auth.spec.ts:42`: expected 200, got 401. Cause: missing auth header. Fix: add `Authorization: Bearer ${token}`.
>
> Next: run `npm test` and paste the first failing line.

## The rules

**Shape (10 rules).** Lead with the next action. Number multi-step tasks. End with one concrete next action. Suppress tangents. Restate state every turn. Specific time estimates. Make wins visible. Matter-of-fact errors. Cap lists at 5 items. No preamble, no recap, no closers.

**Sound human (25 tells).** Cut the machine habits, strongest first: not-X-but-Y contrasts, one-line closers, sayings that sound deep, staged run-ups, arguing with no one, forced triads, repeated openings, dashes everywhere, stacked qualifiers, hyphenated pairs, passive voice, stock AI words ("delve", "pivotal", "robust"), inflated significance, vague connections, shallow -ing riders, sales language, borrowed authority, avoiding "is/are/has", bold decoration, decorative headings, curly quotes, chatbot residue, knowledge-limit guesses, heading echoes, and writing about the previous version.

**Write plain (STE).** One word, one meaning ("ensure" becomes "make sure", "perform" becomes "do", "shall" becomes "must"). No phrasal verbs. Verbs act; nouns sit. Active voice; imperative steps. 20 words per step, 25 per description. No semicolons. Keep articles, subjects, and "that". No contractions. Conditions first, then the command. One technical term per item. Multi-word nouns of three words or fewer.

## Install

Copy/paste into your CLI prompt:

```text
Install the blunt skill/plugin from https://github.com/hayfever/blunt, refer to the repo's AGENTS.md for instructions.
```

Or read the [installation instructions](INSTALL.md). Every agent that loads agent skills works with no conversion; the same `skills/blunt/SKILL.md` serves Claude Code, Codex, Gemini CLI, GitHub Copilot, Hermes, Kimi, OpenCode, Pi, OMP, Qwen Code, Zed, Cursor, Antigravity, and Amp.

## Activate

Type `/blunt` in any harness. Rules stay on until "stop blunt mode" or "normal mode". In Codex, type `$blunt`. In Pi and OMP, the footer shows `● BLUNT ON` while the mode is active; `pi --blunt` starts with the mode on.

## Always-on

Every agent has a persistent-rules route. Paste the always-on snippet from [INSTALL.md](INSTALL.md#always-on) into your agent's rules file (`CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, Cursor user rules, and so on). Claude Code, Codex, OpenCode, and Pi/OMP also support flag-file always-on; see each agent's section.

## Tune it

Fork, edit `skills/blunt/SKILL.md`, then swap your copy in:

```bash
claude plugin uninstall blunt            # drop the upstream copy first:
claude plugin marketplace remove blunt   # fork and upstream share both names
claude plugin marketplace add <your-username>/blunt
claude plugin install blunt@blunt
```

Restart Claude Code, then re-invoke `/blunt`.

## Credits

- [i-have-adhd](https://github.com/ayghri/i-have-adhd) by Ayoub G. (MIT), based on *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain.
- [humanizer](https://github.com/blader/humanizer) by blader (MIT), patterns from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- [ASD-STE100 Issue 9](https://www.asd-ste100.org) by the ASD Simplified Technical English Maintenance Group (free download; summarized, not reproduced).

## License

MIT.