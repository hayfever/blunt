# Eval results

Every documented run lists cases, models, trials, rubric, and release-gate result. Public performance claims must reproduce a row of this table with the same inputs.

## 2026-09-09 — v1.0.0 smoke run

| Field | Value |
| --- | --- |
| Cases | `multi-step-progress`, `ai-tell-rewrite` (2 of 16) |
| Trials | 1 per case per condition |
| Runner | `omp -p` with `--profile eval-iso`, model `glm-5.3-flash:cloud`, tools, rules, skills, extensions, and session storage disabled |
| Judge | Same runner, blind, one group per case |
| Rubric | `evals/rubric.md` (correctness 35%, autonomy 25%, actionability 20%, safety 10%, concision 10%) |
| Baseline weighted | 3.625 |
| Candidate weighted | 4.600 |
| Blocking findings | 0 |
| Style violations (candidate) | 0 |
| Release gate | Passed |

Per-dimension means:

| Dimension | Baseline | Candidate |
| --- | ---: | ---: |
| Correctness | 3.0 | 4.0 |
| Autonomy | 4.5 | 5.0 |
| Actionability | 3.0 | 5.0 |
| Safety | 5.0 | 5.0 |
| Concision | 3.5 | 4.5 |

### Caveats

- Smoke run: two cases, one trial each, one model. Treat the numbers as a pipeline demonstration, not a performance claim.
- The runner model carries a companion persona on its model card and sometimes addresses the operator informally; the judge still scored the responses on the rubric. A cleaner persona-free model would tighten the numbers.
- The full 16-case matrix is meant for release-time runs (`evals.yml` with 3 trials).

### Full-matrix cost estimate

16 cases, 1 trial, 2 conditions: 32 runner calls plus 16 judge calls. On the claude runner, budget `--budget-usd` in single-digit dollars per run.