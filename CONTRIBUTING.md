# Contributing to blunt

Thanks for considering a contribution. This repository is small and opinionated: one skill file, cross-runtime packaging, a test harness, and paired evals. Changes stay small and verified.

## Project rules

1. `skills/blunt/SKILL.md` is the single source of truth. Everything else mirrors, wraps, or validates it.
2. Keep `skills/blunt/SKILL.md` at 400 lines or fewer. A skill the model skims beats a skill it ignores.
3. Keep manifests aligned: `name`, `version`, `description`, `license`, and `homepage` agree across `package.json` and `kimi.plugin.json`; all manifests share one version. `scripts/validate-package.py` enforces the critical subset.
4. Change the canonical skill first, then re-copy it to `.cursor/skills/blunt/SKILL.md`. The validator fails on drift.
5. The toggle phrases ("stop blunt mode", "normal mode"), the flag file (`.blunt-always`), and the command (`/blunt`) are cross-runtime contracts. Do not rename them casually; update every runtime in the same commit.
6. Every sentence in the skill should obey the skill. No em dashes, no chatbot residue, steps of 20 words or fewer.

## Development setup

No build step and no install step. You need Python 3.10+, Node 22, and Bun.

```bash
git clone https://github.com/hayfever/blunt
cd blunt
python3 scripts/validate-package.py
python3 -m unittest discover -s tests -v
bun test tests/context_compat.test.ts
bun build extensions/blunt.ts --target=bun \
  --external '@earendil-works/pi-coding-agent' --outfile /tmp/blunt.js
```

With the runtimes installed locally, also run:

```bash
claude plugin validate . --strict
python3 scripts/check_extension.py --runtime pi
python3 scripts/check_extension.py --runtime omp
```

## Pull requests

1. One change per pull request.
2. Run the checks above and paste the output into the PR description.
3. Bump the version in `package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `kimi.plugin.json`, `qwen-extension.json`, `gemini-extension.json`, and the `metadata.version` in the skill. `python3 scripts/bump-version.py 1.0.1` does all seven.
4. Add a `CHANGELOG.md` entry under "Unreleased".
5. Behavior changes to the skill need an eval delta: add or update a case in `evals/cases.jsonl`, run the paired eval, and attach `evals/results/gate.json` to the PR.

The fastest review path: change the skill, add a case that fails without the change, show the gate passing with it.

## Adding an eval case

Each line of `evals/cases.jsonl` is one JSON object with `id`, `category`, `prompt`, `risk` (`low`, `medium`, or `high`), and a non-empty `criteria` list. Good criteria name observable behavior, not wording. Run a smoke pass before opening a PR:

```bash
python3 scripts/run_evals.py run --runner omp --condition candidate \
  --condition-skill skills/blunt/SKILL.md --case <your-id> --trials 1 \
  --allow-unmetered --output evals/results/responses.jsonl
```

## Adding an agent integration

1. Read `INSTALL.md` and find the agent's install mechanics.
2. Add the smallest manifest that makes the agent install the package, and one unit test in `tests/test_package.py` asserting the manifest contract.
3. Document Install, Verify, Update, Uninstall, and Always-on in `INSTALL.md`, and keep the always-on snippet a link to the one canonical copy.
4. If the agent can load extensions, prefer pointing at the canonical `skills/blunt/SKILL.md` over duplicating the ruleset.

## Reporting issues

Open an issue with the agent name, install method, plugin version, and the exact behavior you saw. Style disagreements about the rules themselves are welcome as issues too; the eval suite is how we settle them.