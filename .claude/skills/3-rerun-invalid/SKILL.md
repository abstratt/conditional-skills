---
name: 3-rerun-invalid
description: Pipeline step 3 of 6. Redo the runs that step 2 marked invalid for infrastructure reasons (bin/run.py --rerun-invalid) and score again. Use when asked to rerun invalid runs, fix failed runs, or clean up the corpus before judging.
---

# Step 3: rerun invalid runs, then score again

Runs that failed for infrastructure reasons (timeout, no final result, error result, failed
turn, non-zero Codex exit) carry `"valid": false` in `score.json` after step 2. They are excluded
from every report and must be redone. This step reruns exactly those cells and rescores.

## Preconditions

Step 2 (`2-score`) has run since the last `run.py` invocation. Same environment requirements as
step 1: `claude` and `codex` authenticated, machine awake.

## Command

```
python3 bin/run.py --rerun-invalid --dry-run                        # lists the cells that would be replaced
python3 bin/run.py --rerun-invalid 2>&1 | tee -a results/run.log
python3 bin/score.py
```

The subset flags of step 1 (`--study`, `--subjects`, `--delivery`, `--prompts`, `--reps`) narrow
which invalid cells are considered; the run flags (`--parallel`, `--timeout`, `--max-turns`) apply
too. Raising `--timeout` is the usual fix for runs invalid with reason `timed out`.

Only cells whose `score.json` says `valid: false` are replaced; every other existing cell is
skipped. The replaced run's `meta.json` records the previous start time and invalid reason under
`rerun`, so the corpus history stays derivable.

## Skipping

Skip this step when step 2 reported no invalid runs:

```
grep -l '"valid": false' results/runs/*/score.json
```

An empty result means nothing to do. Timing-invalid runs (`timing_valid: false`) are not rerun by
this step; their outcomes are kept and only their timings are excluded.

## Verifying

After rescoring, the grep above should print nothing. If a cell is invalid again, look at its
`stderr.txt` and `meta.json` before rerunning; repeated failures usually mean an auth or
network problem, not a flaky run.

## Next

Step 4, `4-judge`.
