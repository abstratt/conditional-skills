---
name: 1-run
description: Pipeline step 1 of 6. Run the experiment matrix (or a subset) with bin/run.py, producing results/runs/<run_id>/ per cell. Use when asked to run the experiment, run the matrix, run a study, a subject, a delivery, a prompt, or a few cells.
---

# Step 1: run the matrix

`bin/run.py` runs one headless agent session per (subject, delivery, prompt, rep) cell in a fresh
seeded workspace and writes `results/runs/<run_id>/` (workspace, transcript, stderr, `meta.json`).
Run ids look like `claude-haiku__native__G1__r1`.

## Preconditions

- `claude` and `codex` on PATH and authenticated; Python 3; git.
- The machine must stay awake with the lid open. A run interrupted by sleep is detected and marked
  as timing-invalid by step 2, and must be redone.

## Command

Always preview first, then run, logging console output to `results/run.log`:

```
python3 bin/run.py [subset flags] --dry-run             # lists the cells; "would replace" marks cells that exist
python3 bin/run.py [subset flags] 2>&1 | tee -a results/run.log
```

Subset flags (combine freely):

| flag | meaning |
|---|---|
| `--study branch` / `--study work` | Study 1 (vendor-stamp, harness-stamp, tier-stamp) or Study 2 (tiered-feature, tiered-guidance, tool-gated-review, baselines) |
| `--subjects claude-opus claude-sonnet claude-haiku codex-default` | one or more subjects |
| `--delivery native pointer inline` | one or more delivery conditions |
| `--prompts G1 G2 G3` | prompt ids, listed in `prompts/branch.jsonl` and `prompts/work.jsonl` |
| `--reps N` | repetitions per cell, default 2 |
| `--parallel N` | concurrent runs, default 3 |
| `--timeout S` | per-run timeout in seconds, default 600 |
| `--max-turns N` | Claude Code turn cap, default 30 |

Baseline prompts (B1..B3, BR1..BR3) have no skill, so they get a single `none` delivery cell
regardless of `--delivery`.

## Skipping and redoing

- Cells whose run directory already exists are skipped, so the script can be stopped and resumed,
  and the full matrix can be built up from subsets. A directory without `meta.json` was
  interrupted and is always redone.
- `--force` reruns cells that exist (the old directory is deleted, and `meta.json` records what
  was replaced).
- `--rerun-invalid` only reruns cells whose `score.json` marks them invalid. That is step 3
  (`3-rerun-invalid`), not this step.

## Cost and time

The full matrix is 408 runs. Claude runs cost about USD 0.03 to 0.25 each depending on the model;
Codex reports no cost. Codex runs take one to two minutes each; budget an hour or more for the whole
matrix at the default parallelism. State the cell count from `--dry-run` before starting a large run.

## Verifying

Each finished cell prints `<run_id>: exit=<code> wall=<seconds>s`; `skipped (exists)` means it
was left alone. Afterwards `ls results/runs | wc -l` should match the expected number of cells.
Non-zero exits are not necessarily failures; step 2 decides validity.

## Next

Step 2, `2-score`. Then step 3, `3-rerun-invalid`, if scoring flags invalid runs.
