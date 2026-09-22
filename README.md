# Model-conditional skills experiment

Can a skill safely branch on the identity or capability of the model running it, is such a skill
portable across harnesses, and what does it cost? `DESIGN.md` states the questions and how they
are answered; this file says how to read the repository and how to run the experiment.

## Reading order

1. `DESIGN.md`: the questions, the studies, the measures, run validity, ground-truth provenance and
   the report's trust model. It is the only hand-written source of judgement; the report is built
   from it and from the runs.
2. `results/FINDINGS.md`: the answers to the three questions, with caveats and guidance. Written by
   an LLM from the two files below and `DESIGN.md`, then validated: every paragraph cites the claims
   it rests on, and every number comes from `claims.md` or `summary.md`.
3. `results/claims.md`: the checkable verdicts, each with its numbers, evidence kind, status and
   exhibits, plus the corpus it was computed from and a check of `FINDINGS.md` against it.
4. `results/summary.md`: the generated tables, one per study, skill and baseline, plus adherence,
   cost and the runs that missed. Source of truth, with `claims.md`, for every number.
5. `results/runs.csv`: one row per valid run, for your own analysis.

## What is hand-maintained and what is generated

Hand-maintained (edit these; they are the inputs):

| path | what it is |
|---|---|
| `DESIGN.md` | the design, and every judgement the report may make |
| `skills/<name>/SKILL.md` | the six skills under test, unchanged across harnesses |
| `prompts/branch.jsonl`, `prompts/work.jsonl` | the prompts, one per line, with the skill each pairs with |
| `ground_truth.json` | the values stamps and branches are scored against, with each value's source |
| `seed/`, `seed-2/` | the workspaces each run starts from |
| `bin/*.py` | the pipeline scripts |
| `.claude/skills/<step>/SKILL.md` | the pipeline's user interface: one Claude Code skill per step, plus `pipeline` for the whole sequence |

Generated (never edit; rerun the pipeline instead):

| path | produced by |
|---|---|
| `results/runs/<run_id>/` | `run.py`: workspace after the run, transcript, stderr, `meta.json`; then `score.json` and `judge.json` |
| `results/summary.md`, `results/runs.csv`, `results/claims.md`, `results/claims.json` | `report.py` |
| `results/FINDINGS.md` | `findings.py`, from `DESIGN.md`, `claims.md` and `summary.md` |
| `results/run.log`, `results/judge.log` | the console output of steps 1, 3 and 4, appended by the skills (the scripts themselves only print) |

`results/runs/` and the logs are gitignored: a fresh clone has the reports but no run data, so
regenerating the reports means rerunning the experiment. `results/FINDINGS.md` and `claims.json`
are committed: the first so each regeneration is reviewed as a diff, the second so the next refresh
can say which claims changed.

## Running the experiment

Requirements: `claude` and `codex` on PATH and authenticated, Python 3, git. Keep the machine
awake and the lid open: a run interrupted by sleep is detected and marked, but must be redone.

### With the skills (preferred)

The pipeline is driven from Claude Code, opened in this directory. The skills under
`.claude/skills/` are its user interface; each one knows its step's preconditions, flags, cost,
how to tell whether it can be skipped, and how to verify it ran. Ask for the whole thing:

```
/pipeline
```

which works out from the state of `results/` where to resume, runs the steps in order, and
skips the ones with nothing to do. Or ask for one step at a time:

| step | skill | does |
|---|---|---|
| 1 | `/1-run` | run the matrix, or a subset (a study, a subject, a delivery, some prompts); previews the cells first |
| 2 | `/2-score` | score every run deterministically; flags invalid runs |
| 3 | `/3-rerun-invalid` | redo the runs that failed for infrastructure reasons, then score again; skipped when there are none |
| 4 | `/4-judge` | LLM judge (Fable 5.1) for adherence; skips runs already judged |
| 5 | `/5-report` | `summary.md`, `runs.csv`, `claims.md`, `claims.json` |
| 6 | `/6-findings` | `FINDINGS.md`, written by an LLM (Fable 5.1) and validated; skipped when the existing file still validates |

Plain language works as well as the slash form: "run study 1 for haiku", "score the runs",
"regenerate the report", "refresh the results". The skills state what a step will run and what
it costs before launching anything that calls an agent (steps 1, 3, 4 and 6), so answer that
prompt rather than assuming it started. They also append the console output of steps 1, 3 and
4 to `results/run.log` and `results/judge.log`.

After a change, `/pipeline` also knows which steps a refresh needs: a changed skill, prompt or
seed means rerunning the affected cells and then steps 2 to 6; a changed `bin/score.py` means
steps 2, 5 and 6; a changed `bin/claims.py` or `DESIGN.md` means steps 5 and 6.

### With the scripts

Every skill runs a script in `bin/`, and nothing else; the scripts are the whole pipeline and
can be run by hand from any shell, without Claude Code. In order:

```
python3 bin/run.py                  # 1. run the matrix; results/runs/<run_id>/ per cell
python3 bin/score.py                # 2. score every run; writes score.json, flags invalid runs
python3 bin/run.py --rerun-invalid  # 3. redo runs that failed for infrastructure reasons...
python3 bin/score.py                #    ...and score again
python3 bin/judge.py                # 4. LLM judge (Fable 5.1); writes judge.json, skips runs already judged
python3 bin/report.py               # 5. summary.md, runs.csv, claims.md, claims.json
python3 bin/findings.py             # 6. FINDINGS.md, written by an LLM (Fable 5.1) and validated; fails rather than write a bad draft
```

The scripts only print; to keep the logs the skills keep, pipe steps 1, 3 and 4 through
`2>&1 | tee -a results/run.log` (or `judge.log`). The rest of this section is what the skills
encode, for running by hand.

Step 3 is conditional. `score.py` writes `"valid": false` and a reason into the `score.json` of
a run that failed for infrastructure reasons (timeout, no final result, failed turn), and
`run.py --rerun-invalid` replaces only those cells, so it is a no-op when the corpus is clean.
To see whether there is anything to redo, after scoring:

```
grep -l '"valid": false' results/runs/*/score.json   # the invalid runs, or nothing
python3 bin/run.py --rerun-invalid --dry-run          # the cells step 3 would replace
```

Skip step 3 when both print nothing. `summary.md` also lists invalid and incomplete runs, with
reasons, in an "Excluded runs" section at the top that appears only when there are some. A run whose
timing is invalid (the machine slept) keeps its outcome and is not rerun; it is only left out of
time comparisons.

`findings.py --dry-run` validates the existing `FINDINGS.md` without calling the model. Claims live in
`bin/claims.py`; add one there when a finding needs a number or verdict the report does not provide.

`run.py` skips cells whose run directory already exists, so it can be stopped and resumed, and a
subset can be run first. A directory left without `meta.json` by an interrupted run is always
redone. `--force` reruns cells that exist. `--dry-run` prints the cells and touches nothing.

Subsets:

```
python3 bin/run.py --study branch                      # Study 1: vendor-stamp, harness-stamp, tier-stamp
python3 bin/run.py --study work                        # Study 2: tiered-feature, tiered-guidance, tool-gated-review, baselines
python3 bin/run.py --delivery inline                   # the inline-instructions control only
python3 bin/run.py --prompts G1 G2 G3                  # one skill (prompt ids are in prompts/*.jsonl)
python3 bin/run.py --prompts B1 B2 B3 BR1 BR2 BR3      # the no-skill baselines
python3 bin/run.py --subjects claude-haiku --reps 1    # one subject, one rep
```

The full matrix is 408 runs (see `DESIGN.md`, Scale). Claude runs cost about USD 0.03 to 0.25 each
depending on the model, Codex reports no cost, and judging costs about USD 0.10 to 0.22 per run.
Codex runs are the slowest at one to two minutes each; with the default parallelism of 3, budget
an hour or more for the whole matrix.

## Interpreting a run directory

`results/runs/<subject>__<delivery>__<prompt>__r<rep>/` holds `workspace/` (the files after the
run, as a git repo whose last commit is the state before the agent started, so `git status` shows
what the agent changed), `stdout.jsonl` (the harness's JSON transcript), `stderr.txt`, `meta.json` (the cell,
command, timing, and what a rerun replaced), `score.json` (every deterministic measure, plus the
validity flags) and `judge.json` (adherence scores and the judge's rationale).
