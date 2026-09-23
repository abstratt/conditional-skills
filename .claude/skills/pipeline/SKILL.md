---
name: pipeline
description: Run the whole experiment pipeline end to end, or resume it from wherever it stopped: run the matrix, score, rerun invalid runs, judge, report, findings. Use when asked to run the pipeline, run everything, refresh the results, or when unsure which step comes next.
---

# The pipeline

Six steps, each its own skill and its own script in `bin/`, each reading what the previous ones
left in `results/`. There is no orchestrator; run the scripts in order. Every step is resumable
and idempotent, so the pipeline can be stopped at any point and continued.

| step | skill | command | writes | cost |
|---|---|---|---|---|
| 1 | `1-run` | `python3 bin/run.py [subset]` | `results/runs/<run_id>/` | agent runs; slow |
| 2 | `2-score` | `python3 bin/score.py` | `score.json` per run | free |
| 3 | `3-rerun-invalid` | `python3 bin/run.py --rerun-invalid` then `python3 bin/score.py` | replaced runs | agent runs |
| 4 | `4-judge` | `python3 bin/judge.py` | `judge.json` per eligible run | optional; USD 0.10 to 0.22 per run |
| 5 | `5-report` | `python3 bin/report.py` | `summary.md`, `runs.csv`, `claims.md`, `claims.json` | free |
| 6 | `6-findings` | `python3 bin/findings.py` | `FINDINGS.md` | one to three model calls |

Read the step's skill before running it; each states preconditions, flags, how to skip and how
to verify.

## Before starting

- `claude` and `codex` on PATH and authenticated; Python 3; git.
- The machine stays awake for steps 1, 3 and 4.
- Say what will run and roughly what it costs before launching steps 1, 3, 4 or 6. Use
  `bin/run.py --dry-run` to count cells.

## Full run

```
python3 bin/run.py 2>&1 | tee -a results/run.log
python3 bin/score.py
python3 bin/run.py --rerun-invalid 2>&1 | tee -a results/run.log && python3 bin/score.py
python3 bin/judge.py 2>&1 | tee -a results/judge.log    # optional; only when asked for adherence scores
python3 bin/report.py
python3 bin/findings.py
```

## Where to resume

Decide from the state of `results/`:

1. No `results/runs/`, or fewer run directories than cells: step 1. A fresh clone has no run
   data at all (it is gitignored), so regenerating the reports means rerunning the experiment.
2. Run directories without `score.json`, or any `run.py` invocation since the last scoring: step 2.
3. `grep -l '"valid": false' results/runs/*/score.json` prints anything: step 3.
4. Step 4 only when the user asks for adherence scores; no claim uses them (`DESIGN.md`, Scope
   decisions). Plain `judge.py` finds the unjudged runs itself.
5. Anything changed since `summary.md` was written, including edits to `bin/claims.py`: step 5.
6. `python3 bin/findings.py --dry-run` fails: step 6.

## Skipping a step

- Steps 2 and 5 are free; never skip them, just rerun.
- Step 3 is skipped when step 2 flags no invalid runs.
- Step 4 is optional and skipped by default; when run, it skips already-judged runs on its own.
- Step 6 is skipped when `--dry-run` passes.
- Step 1 is skipped when the corpus is complete; `run.py` with no flags reports every cell as
  `skipped (exists)` in that case, which is a cheap way to confirm.

## Refreshing after a change

- Changed a skill under `skills/`, a prompt, or a seed: rerun the affected cells with
  `run.py --force [subset]`, then steps 2 to 6.
- Changed `bin/score.py`: steps 2, 5, 6 (rejudge with `judge.py --force` only if the judge
  packet depends on what changed).
- Changed `bin/claims.py` or `DESIGN.md`: steps 5 and 6.
- Changed nothing but want the report: steps 5 and `findings.py --dry-run`.

## Finishing

Commit `results/FINDINGS.md`, `claims.json`, `claims.md` and `summary.md` together. Review
`FINDINGS.md` as a diff before committing; that is why it is committed.
