---
name: 4-judge
description: Pipeline step 4 of 6, optional. Run the LLM judge (bin/judge.py) for adherence on runs where the skill was expected or used, writing judge.json per run. Use when asked to judge runs, grade adherence, rejudge, or judge specific run ids.
---

# Step 4: LLM judge (optional)

No claim uses adherence scores and a refresh skips this step (`DESIGN.md`, Scope decisions).
Run it only when asked for adherence scores.

`bin/judge.py` asks a judge model (the one configured in the script, via `claude -p` with no tools) to grade each
eligible run's adherence to its skill: format adherence, scope discipline and honesty, with a
rationale. It writes `results/runs/<run_id>/judge.json`.

## Preconditions

- `claude` on PATH and authenticated.
- Step 2 has run: the judge reads `score.json` to decide eligibility and to build the packet
  (tool calls, workspace diff, final message).
- Step 3 is done, or accepted as skipped, since invalid runs are never judged and a rerun
  produces a new run that needs judging.

## Command

```
python3 bin/judge.py 2>&1 | tee -a results/judge.log
```

| flag | meaning |
|---|---|
| `--only <run_id> ...` | judge only these run ids |
| `--force` | rejudge runs that already have `judge.json` |
| `--parallel N` | concurrent judge calls, default 4 |

## Which runs get judged

A run is judged only when the skill was expected to apply or was actually triggered, and the run
is valid. Baseline runs without a skill, and runs where an unexpected skill did not fire, are
skipped silently and have no `judge.json`. Runs that already have `judge.json` are skipped
without `--force`, so the step is resumable and only new runs cost anything on a refresh.

## Cost

About USD 0.10 to 0.22 per judged run. `--force` over the whole corpus rejudges everything;
prefer `--only` when a few runs changed.

## Verifying

Each judged run prints `<run_id>: {...verdict...}`. A verdict containing an `error` key means the
judge call failed; rerun those ids with `--only ... --force`. To find them:

```
grep -l '"error"' results/runs/*/judge.json
```

## Next

Step 5, `5-report`.
