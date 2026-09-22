---
name: 5-report
description: Pipeline step 5 of 6. Aggregate score.json and judge.json into results/summary.md, runs.csv, claims.md and claims.json with bin/report.py. Use when asked to regenerate the report, the summary tables, the claims, or the CSV.
---

# Step 5: report

`bin/report.py` aggregates every valid run into the generated report files:

| file | contents |
|---|---|
| `results/summary.md` | tables per study, skill and baseline, plus adherence, cost and the runs that missed |
| `results/runs.csv` | one row per valid run, with judge scores where present |
| `results/claims.md` | every claim from `bin/claims.py` evaluated against the corpus, with numbers, evidence, status and exhibits; the corpus fingerprint; a check of `FINDINGS.md` against the claims |
| `results/claims.json` | the same claims, machine-readable, committed so the next refresh can say which changed |

Invalid runs are excluded everywhere and listed; incomplete run directories (no `meta.json`) are
listed too.

## Preconditions

Steps 2 and 4 have run. Missing `judge.json` files do not fail the report; the adherence columns
are just empty for those runs.

## Command

```
python3 bin/report.py
```

No flags. Cheap, deterministic and idempotent: rerun after any scoring, judging or edit to
`bin/claims.py` or `bin/report.py`. It prints the summary to stdout and ends with
`claims: N evaluated, M failing` on stderr.

## Claims

Claims live in `bin/claims.py`. When a finding needs a number or verdict the report does not
provide, add a claim there and rerun this step; never compute the number by hand for
`FINDINGS.md`. A failing claim is not an error in the pipeline; it is a verdict that the corpus
does not support, and `claims.md` says so.

## Verifying

- `git diff --stat results/claims.json` shows which claims changed since the last commit.
- The tail of `results/claims.md` reports whether the existing `FINDINGS.md` still cites valid,
  passing claims and a current fingerprint. A stale fingerprint means step 6 must run.

## Next

Step 6, `6-findings`.
