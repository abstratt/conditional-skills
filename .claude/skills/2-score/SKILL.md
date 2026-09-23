---
name: 2-score
description: Pipeline step 2 of 6. Deterministically score every run with bin/score.py, writing score.json per run and flagging invalid runs. Use when asked to score runs, rescore, check which runs are invalid, or after any run.py invocation.
---

# Step 2: score every run

`bin/score.py` reads every `results/runs/<run_id>/` that has a `meta.json` and writes
`score.json` next to it: trigger evidence (did the skill load and was it expected to), outcome
checks against `ground_truth.json`, stamp values, cost and tokens, and the validity flags.

## Command

```
python3 bin/score.py
```

No flags. It is cheap, deterministic and idempotent: it rescores everything each time, so rerun
it freely after any change to runs or to `bin/score.py` itself. It must run after every
`run.py` invocation, because `judge.py`, `report.py` and `run.py --rerun-invalid` all read
`score.json`.

## Validity flags

Each `score.json` carries two flags, defined in `DESIGN.md`, Run validity:

- `valid: false` with `invalid_reason` marks an infrastructure failure (timed out, no final
  result, error result, failed turn, non-zero exit for Codex). The run's outcome is unusable;
  it is excluded from every report and should be rerun with step 3.
- `timing_valid: false` with `timing_invalid_reason` marks a run whose outcome is usable but whose
  timing is not (the machine slept, or the network reconnected). It stays in the reports but is
  left out of time comparisons.

## Verifying

The script prints one line per run and ends with `scored N runs` on stderr. To list invalid runs:

```
grep -l '"valid": false' results/runs/*/score.json
```

## Next

If any run is invalid, step 3, `3-rerun-invalid`. Otherwise step 5, `5-report` (step 4, the
judge, is optional and only run when asked).
