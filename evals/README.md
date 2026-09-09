# Evals

Paired response-quality evaluation: the same case is answered twice, once without the skill (`baseline`) and once with `skills/blunt/SKILL.md` injected into the prompt (`candidate`). A judge model grades blind and a release gate decides.

## Pipeline

```bash
# 1. Generate responses (one row per case, trial, condition).
python3 scripts/run_evals.py run --runner omp --condition baseline \
  --trials 1 --allow-unmetered --output evals/results/responses.jsonl
python3 scripts/run_evals.py run --runner omp --condition candidate \
  --condition-skill skills/blunt/SKILL.md \
  --trials 1 --allow-unmetered --output evals/results/responses.jsonl

# 2. Judge blind: responses get opaque labels, the judge never sees condition names.
python3 scripts/judge.py --responses evals/results/responses.jsonl \
  --runner omp --output evals/results/scores.jsonl

# 3. Aggregate and apply the release gate.
python3 scripts/run_evals.py score evals/results/scores.jsonl

# 4. Deterministic style check on candidate rows only.
python3 scripts/check_style.py evals/results/responses.jsonl \
  --condition candidate --strict
```

The runner is configured in `evals/runners.json`. The default omp runner is unmetered, hence `--allow-unmetered`; the claude runner reports cost through `claude --print --output-format json` and enforces `--budget-usd` per run.

## Runners

| Runner | Cost control | Isolation |
| --- | --- | --- |
| `omp` (local) | none; cap with `--budget-usd` and stop between conditions | `--profile eval-iso`, `--no-session --no-tools --no-rules --no-skills --no-extensions` |
| `claude` (CI default) | `--budget-usd` per invocation | `--setting-sources ""`, no tools, no session persistence |

The omp runner needs its profile seeded once with the main model catalog:

```bash
mkdir -p ~/.omp/profiles/eval-iso/agent
cp ~/.omp/agent/models.yml ~/.omp/profiles/eval-iso/agent/models.yml
```

## Adding cases

Append one JSON line per case to `evals/cases.jsonl` with `id`, `category`, `prompt`, `risk` (`low`, `medium`, `high`), and a non-empty `criteria` list. `python3 scripts/run_evals.py validate` checks the schema. Good criteria name observable behavior ("Restates the current step", "Does not invent a founding date"), not specific wording.

The rubric lives in `evals/rubric.md`. Everything between the `judge:begin` and `judge:end` markers goes verbatim to the grader; release-gate rules live outside that block so the judge stays blind to condition names.

## Style linter

`scripts/check_style.py` grades the mechanical tells without a model: chatbot residue, staged openers, closing pleasantry, dashes as connectors, curly quotes, Latin abbreviations, not-X-but-Y contrasts, and lists longer than five items. Code fences, inline code, and quoted spans are exempt, mirroring the skill's own quoted-text rule. It also works standalone on any text file:

```bash
python3 scripts/check_style.py some-text.md --strict
```

## Interpreting the gate

The release gate passes only when the candidate has no blocking findings, correctness and safety are each within 0.1 points of baseline or better, and the weighted score beats baseline. Documented runs live in `RESULTS.md`.