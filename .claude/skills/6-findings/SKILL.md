---
name: 6-findings
description: Pipeline step 6 of 6. Write results/FINDINGS.md with an LLM from DESIGN.md, claims.md and summary.md, then validate it (bin/findings.py); or validate the existing file with --dry-run. Use when asked to regenerate, refresh, or validate the findings.
---

# Step 6: findings

`bin/findings.py` sends `DESIGN.md`, `results/claims.md` and `results/summary.md` to a model
(the one configured in the script, via `claude -p`; the file's header records which) and asks
for a new `results/FINDINGS.md`. The draft is validated:
every paragraph must cite claims that exist and pass, every number must come from `claims.md` or
`summary.md`, and the corpus fingerprint and run count must match. It never replaces the previous
file unless the draft passes every check.

## Preconditions

- `claude` on PATH and authenticated.
- Step 5 has run, so `claims.md` and `summary.md` reflect the current corpus.

## Command

```
python3 bin/findings.py                # draft, validate, retry up to --attempts times (default 3)
python3 bin/findings.py --dry-run      # validate the existing FINDINGS.md only; no model call
```

## Skipping

Run `--dry-run` first. If it prints `FINDINGS.md passes validation`, the existing file is
consistent with the current claims and corpus and this step can be skipped. It fails (exit 1) when
the corpus fingerprint changed, a cited claim changed status or vanished, or a number no longer
matches; then a regeneration is due.

## Outcome

- Success: `wrote results/FINDINGS.md (N words, USD X)`. Review it as a diff (`git diff
  results/FINDINGS.md`) before committing; the file is committed precisely so each regeneration
  is reviewed.
- Failure after all attempts: `FINDINGS.md` is left unchanged and the last draft goes to
  `results/FINDINGS.rejected.md` (gitignored) with the validation errors appended as a comment.
  Read the errors; the usual causes are a claim the draft needs that does not exist yet (add it to
  `bin/claims.py` and redo step 5) or a wording rule in `DESIGN.md`, Rules for claims and findings.

## Next

Nothing. Commit `results/FINDINGS.md`, `claims.json`, `claims.md` and `summary.md` together, so
the committed findings always match the committed claims.
