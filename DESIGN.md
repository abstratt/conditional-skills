# Model-conditional skills experiment

Goal: understand whether a skill can safely branch on the identity or capability of the
model executing it. Can a skill author write "if you are model X / tier Y / have capability Z,
do A, otherwise do B" and expect the branch to be chosen correctly and carried out?

A second question follows from the first: can a single skill file be portable? Every subject runs
the same `SKILL.md`, unchanged, in one of two harness-and-model pairs (Claude models in Claude Code,
gpt-5.6-luna in Codex CLI) and under every delivery condition. So the experiment should say which
kinds of branch condition behave correctly for both pairs, which only for one, and whether how the
skill is delivered changes that. Harness and model are confounded (see Known asymmetries), so the
answer is stated per pair, never per harness.

A third question is efficiency: what does a model-conditional skill cost to run, in tool
invocations, turns, tokens and wall time (and USD where the harness reports it)? The experiment
should say:

- the overhead of the skill itself, by comparing each Study 2 skill run with the no-skill baseline
  run of the same prompt for the same subject. Baseline prompts carry the same text as the skill
  prompts they pair with (B1..B3 with F1..F3 and G1..G3, BR1..BR3 with R1..R3), and `report.py`
  pairs runs by prompt text;
- how cost differs by branch, within a subject. Each subject always takes the same tier branch, so
  comparing branches across subjects would compare models. Instead, the same prompts under
  `tiered-feature` and `tiered-guidance` give a subject a heavy and a light version of its branch,
  which shows whether the lighter branch is actually cheaper. The contrast exists for flagship
  (three tests against none) and small (a TODO line against three tests) but not for mid, which
  prescribes a docstring and one test in both skills, so a mid subject has no branch-cost
  comparison. For reviews, delegated runs are compared with the same subject's runs that reviewed
  without delegating: its no-skill baseline, and any skill runs that did not delegate;
- whether the delivery condition changes cost, for example because a pointer adds a file read,
  with `inline` as the reference: the same instructions and the same work, with no skill
  mechanism;
- what staying out of a skill costs (Study 3): a run in which the gate held at the description
  should cost about what the no-skill baseline of the same prompt costs, since only the
  description sat in the context, while a run that loaded the skill and then bailed out paid for
  the load. The comparison is per subject, against the baseline run of the same prompt text.

Study 1 has no no-skill baseline, because without the skill the task is not the same; its skill
overhead is measured against `inline` instead. Efficiency is compared within a subject. Tool
invocations are the one step count available in both harnesses; turns exist only for Claude Code
(see Measures).

A fourth question is where the condition can sit. Studies 1 and 2 put it inside the body, so the
skill always loads and the model branches. A skill author has two other places for it, and each
does something a body branch cannot:

- **A gate in the description.** The description is what the harness shows the model before any
  skill is loaded. A condition there ("only for small models; flagship models must not invoke this
  skill") could keep a model that the skill is not for from ever loading it, which is the only way
  to *avoid* a skill rather than take an empty branch of it. Can a model tell from the description
  alone that the skill is not for it, and leave it unloaded? And does a model the description
  includes still load it?
- **Selection among alternatives.** Several skills whose descriptions differ only in which model
  each is for ("skill A for Sonnet, skill A' for Opus"). Does the model load the one meant for it,
  and only that one?
- **A bail-out in the body.** A loaded skill whose first lines tell a model that it is not for it.
  Does the model stop following the skill and do the request as it would have without it?

The motivating case, and the one the tier gate in Study 3 is built for, is a skill written only
for weaker models: guidance that a small model should follow in full and a frontier model, which
gains little from it, should avoid altogether. Study 2 showed the body-level half of this (a
flagship branch that skips the checklist); Study 3 asks whether the frontier model can be kept
out of the skill entirely, and whether a weaker model still comes in. Study 3 answers this
fourth question, and its cost is part of the third.

The report answers all four questions. Restated as the questions a skill author asks, they are:

| question | where it is answered |
|---|---|
| Can a model report what model and harness it is running in? | Study 1, `vendor-stamp` and `harness-stamp` |
| Can a model, running a skill, take a different workflow depending on model or capability? | Studies 1 and 2 |
| Can a model tell from the description alone that it should not run the skill, and never call it? | Study 3, gated skills |
| Can a model pick one skill from alternatives by model type? | Study 3, selection sets |
| Can a model bail out of a skill from its body? | Study 3, gated skills, `inline` and loaded runs |
| Can a skill be reserved for weaker models and avoided by frontier models? | Study 3, `tier-gated-guidance`, with Study 2's `tiered-guidance` |

## Subjects

| id            | harness     | model                       |
|---------------|-------------|-----------------------------|
| claude-opus   | Claude Code | claude-opus-5               |
| claude-sonnet | Claude Code | claude-sonnet-5             |
| claude-haiku  | Claude Code | claude-haiku-4-5-20251001   |
| codex-default | Codex CLI   | gpt-5.6-luna (pinned per run in `config.toml`) |

Every run is headless (`claude -p`, `codex exec`), in a fresh git-initialised workspace,
with exactly one skill available (none for the baseline; a set of two or three alternatives in
Study 3's selection cells). The prompts are written as unambiguous
requests for what the skill does, so that a run in which the skill was not loaded counts as a
loading failure rather than a triggering ambiguity. That is an assumption, and the `inline`
condition tests it: a model that follows the same instructions when they are in the prompt was
not confused by the request. Loading is measured as a precondition (Measures, 1) and the branch
results are read over runs where it succeeded.

## Delivery conditions

- `native`: the skill lives where the harness discovers it natively
  (`<ws>/.claude/skills/<name>/SKILL.md`, or `$CODEX_HOME/skills/<name>/SKILL.md`
  with an isolated per-run `CODEX_HOME`).
- `pointer`: the harness's instructions file (`CLAUDE.md` / `AGENTS.md`) lists the
  skill's name and description and points at `skills/<name>/SKILL.md`.
- `inline`: no skill is installed and there is no pointer. The body of `SKILL.md`,
  without its frontmatter, is placed in the prompt ahead of the user's request, introduced as
  instructions that apply to it. Same task, same branches, same output files; only the delivery
  differs.

Comparing `native` and `pointer` separates the skill discovery mechanism from instruction
following; `inline` is the control for both. It cannot fail to load, so it gives an upper bound on
how well a model follows the branch once it has the instructions, and a gap between `inline` and
the skill conditions is the cost of loading: a model may not load a skill on a plain coding
request, and `inline` shows whether it follows the same instructions when loading is not in
question. It also measures the skill mechanism's efficiency on identical work, since an `inline`
run and a `native` run of the same prompt differ only in discovering, loading and reading the
skill. `inline` is not free either, since the skill body sits in the context on every turn, so the
comparison is against instructions in the prompt, not against nothing. That makes it the
like-for-like efficiency comparison for Study 1, which has no no-skill baseline: a no-skill Study 1
run would invent its own stamp format, so it would not be the same task. And it depends on neither
harness's skill support, which matters for portability. If the optional judge is run, `inline`
runs are judged like the others.
For them the skill-loaded measure is forced true by the scorer, because the instructions are in the
prompt; the trace line is still recorded, but not as loading.

In Study 3 the delivery conditions carry a different meaning, because the condition sits before
the body. Under `native` and `pointer` the model sees the description (in the harness's skill
listing, or in the instructions file) before deciding to load, so those two deliveries are where a
gate or a selection can hold. `inline` puts the body in the prompt, so it cannot test a gate at
the description; for the gated skills it tests the bail-out in the body alone, and for the
selection sets it is not run, since putting every alternative's body in the prompt is a body-level
branch, which Study 2 already tests.

## Study 1: branch selection (skills `vendor-stamp`, `harness-stamp`, `tier-stamp`)

Workspace seeded from `seed/`. Each skill asks the agent to write a small key/value file whose
values depend on the agent, then to apply a branch whose visible effect is a differently named file:

- `vendor-stamp`: self-reported vendor, model, harness.
- `harness-stamp`: whether the harness supports subagents, answered from product knowledge.
- `tier-stamp`: self-placed tier (flagship / mid / small).

Two prompts per skill (`prompts/branch.jsonl`). Ground truth per subject is in
`ground_truth.json` and is editable.

`harness-stamp` asked three questions in the first corpus: hooks, subagents and image
generation. The first and last were dropped in September 2026 (see Scope decisions): neither is
observable from inside a session, no branch depended on them, and their only effect on the
measure was to dilute the all-correct rate with answers the runs could not verify. The `harness-stamp`
cells are rerun with the one-question skill in the same batch as Study 3.

## Study 2: branches that change the work (skills `tiered-feature`, `tiered-guidance`, `tool-gated-review`)

### Why a second study

Study 1 tests whether an agent can pick a branch, but its branches are trivial by construction:
creating an empty file named after the answer costs nothing and says nothing about whether a real
skill would behave differently per model. A skill author writes a model-conditional skill because they
want different behaviour, for example a stronger model skipping guidance it does not need and a
weaker one following it in full. Study 2 closes two gaps Study 1 cannot:

1. **The branch must have consequences.** Here the branch decides the actual work. Scoring
   infers the branch from the work itself, independently of what the agent wrote down, and
   checks that the two agree.
2. **Self-reports must survive an incentive.** In Study 1 nothing hung on the answer. If a
   model's self-placement changes when some answer means less work, self-placement cannot be
   trusted as a branch condition. The report compares the tiers claimed in Study 1 (free) and
   Study 2 (costly) side by side.

Each skill isolates one kind of condition: identity for `tiered-feature` and `tiered-guidance`,
capability for `tool-gated-review`.

### Setup

Workspace seeded from `seed-2/`, whose `src/app.py` has two planted bugs (division by zero on an
empty list, off-by-one index). The bugs give the review a right answer, so a delegated review is
not scored as a success merely because its mode label was correct: both bugs must be named.

### `tiered-feature` (F1..F3): identity, with a cost

The use of an identity branch that motivates this experiment is a skill that matters less the
stronger the model is: a strong model gets little from detailed guidance and can skip most of
it, while a weaker one should follow it in full. That only works if a model places itself in its
lineup correctly, and keeps doing so when the placement decides how much work it has to do.
Study 1 tests the placement when nothing hangs on it. This skill asks whether it survives a
payoff.

The lever is tests. Tier decides whether the agent writes three or more tests, one, or none:
flagship must add a docstring and at least three tests, mid a docstring and one test, small no
tests and a TODO comment. Note that this payoff runs opposite to the motivating use: here the
flagship does the most work, so claiming a lower tier is the easy way out and claiming a higher
one costs extra work. `tiered-feature` therefore tests only the downward pull. It cannot show
whether a weak model would claim a higher tier to skip guidance it needs, which is the risk that
matters when a skill steps back for strong models. `tiered-guidance` below inverts the payoff to
test that.

The skill also makes the branch observable without trusting the agent. The tier is written to
`TIER.txt`, but scoring infers the tier from the work itself (test count, docstring, TODO) and
compares three things: reported tier against ground truth, the work against the reported tier,
and the work against ground truth. The feature is executed and the tests are run with an
inline runner, so a branch that produced broken tests does not count as followed.

### `tiered-guidance` (G1..G3): identity, with the payoff inverted

Same tiers, prompt texts and lever as `tiered-feature`, with the branches swapped to match the
motivating use. The skill presents itself as a quality checklist that stronger models do not
need: flagship skips it (implement only, no docstring, no tests), mid follows part of it (a
docstring and one test), small follows all of it (a docstring and at least three tests). Claiming
a higher tier is now the easy way out.

Scoring infers the tier from the work as before, with the mapping reversed: no docstring and no
tests implies flagship, a docstring and one test mid, a docstring and three or more tests small.
There is no TODO marker. Read together with `tiered-feature`, the report can show whether
self-placement holds under both pulls: a tier that rises here but not there means models inflate
their tier to skip work, which would make a skill that steps back for strong models unsafe.

### No-skill baseline (B1..B3): what the model does unprompted

The feature prompts F1..F3 again, with no skill installed and no pointer, so there is a single
`none` delivery cell per subject. It answers a question the tiered skills cannot: did the branch
change anything? A branch that prescribes more work than the model would do anyway is visible in
the work. A branch that prescribes the model's default is not: if a model implements a one-line
request with no docstring and no tests when nothing asks for them, then the `tiered-guidance`
flagship branch (implement only, no docstring, no tests) is its default, and "work matches the
reported tier" is no evidence that the branch was followed. The baseline shows, per subject,
which branches prescribe more than the default and which prescribe exactly the default. The same
question applies to the `tiered-feature` small branch, apart from its TODO line.

Scoring records test count, docstring and feature check, and which tier each tiered skill's
scoring would infer from the same work. The runs are not judged, since there is no skill to grade
adherence to.

### No-skill review baseline (BR1..BR3): does the model delegate unprompted?

The review prompts R1..R3 again, with no skill installed. A perfect score on `tool-gated-review`
only shows the branch mattered if the model would not have delegated anyway. If a model delegates a
one-file review unprompted, its delegated branch is its default, just like the `tiered-guidance`
flagship branch, and following it proves nothing. Conversely, for a model that never delegates
unprompted, every delegation under the skill is the branch's doing, and a partial delegation rate
shows the branch pulling it partway.

Without the skill there is no required `REVIEW.md`, so scoring checks the final message and any
file written outside `src/` for both planted bugs. It also records whether a delegation call
appears in the transcript, and whether `src/` was left untouched, since nothing tells the model not
to fix the bugs. The runs are not judged.

### `tool-gated-review` (R1..R3): capability, verified in the moment

Review the buggy file. If the session exposes a delegation tool the agent must delegate and
mark the review `mode: delegated`, else review inline. The skill tells the agent to decide from
the tools it can actually call, not from product knowledge, because a model's product knowledge
of its own harness may be wrong (`harness-stamp` tests exactly that) and a branch should not
depend on it. This makes the condition checkable: the transcript shows whether a delegation call
really happened, so the label can be scored against the action, not just against ground truth.
Ground truth is session-level (`subagents_session`), with its source stated per pair in
`ground_truth.json` (see Ground truth below). Scoring checks the mode line, whether a delegation
call appears in the transcript, that both planted bugs are named, and that `src/` is untouched.

Three prompts per skill (`prompts/work.jsonl`).

## Study 3: conditions before the body (skills `vendor-gated-guidance`, `tier-gated-guidance`; sets `select-vendor`, `select-tier`)

### Why a third study

Studies 1 and 2 test a condition that the model meets after the skill has loaded. Study 3 tests
the two places a condition can sit before that, and the bail-out that lets a loaded skill send the
model away. It uses the feature task of Study 2 throughout, so the no-skill baselines B1..B3 say
what each subject does when it stays out of the skill, and the checklist from `tiered-guidance`
says what following it looks like. A condition in the description depends on the harness showing
descriptions before loading, which both do (see Known asymmetries), and on the model reading them
against what it knows about itself, which Study 1 measured per condition kind: vendor is reliable
for both pairs, tier only for the Claude pair. Study 3 uses both kinds, so it can tell a failure
of the mechanism from a failure of self-knowledge.

### Gated skills (`vendor-gated-guidance`, `tier-gated-guidance`): a skill that is not for everyone

Both skills carry the full checklist of the `tiered-guidance` small branch as their body: give
the function a docstring and create `tests/test_app.py` with at least three tests, run them if a
runner is available. The description says who the skill is for and that other models must not
invoke it. The body opens by restating the condition and giving the bail-out: a model the
condition excludes appends `<skill>: declined` to `.skill-trace`, then implements the request as
it would without the skill and ignores the rest of the file. A model the condition includes
follows the checklist and appends the plain skill name, as every skill does.

- `vendor-gated-guidance` is for models made by Anthropic. Included: the Claude pair. Excluded:
  the Codex pair. Vendor is the condition both pairs reported correctly in every Study 1 run, so
  this gate tests the mechanism with a condition the model can be trusted to know.
- `tier-gated-guidance` is for the small tier, the fastest and cheapest model in its vendor's
  lineup. Included: Haiku (assumed, see Tier scale) and the Codex pair (documented). Excluded:
  Opus and Sonnet. This is the motivating case, a skill reserved for weaker models. The Codex
  pair placed itself at flagship in every Study 2 tier answer, so it is expected to refuse a skill
  written for it; that is a result about whether the case can rest on self-placement, not a defect
  of the study.

Prompts: the feature prompt texts F1..F3, under the ids GV1..GV3 and GT1..GT3
(`prompts/gate.jsonl`), so the baselines B1..B3 pair with them by text as they do with F and G.
All three deliveries are run; `inline` tests only the bail-out (see Delivery conditions).

Each run gets a **gate outcome**, from the loading evidence, the trace line and the work:

| outcome | loaded | trace line | work |
|---|---|---|---|
| `not-loaded` | no | none | any |
| `declined` | yes | `<skill>: declined` | not the checklist |
| `followed` | yes | `<skill>` | the checklist: docstring, three or more passing tests |
| `ignored` | yes | none | not the checklist |
| `mixed` | anything else | | |

The correct outcome for an included subject is `followed`. For an excluded subject it is either
`not-loaded` or `declined`; both keep the skill's work off the model, and which one occurred says
where the gate held. `not-loaded` under `native` or `pointer` is the description doing its job, the
answer to whether a model can tell from the description alone. `declined` is the body doing it,
the answer to whether a model can bail out. The report gives both rates, per subject and
delivery, and treats `inline` `declined` rates as the upper bound on bail-out, since there the
skill cannot fail to be in front of the model. `followed` by an excluded subject is the failure
that matters: the skill imposed its work on a model it was not written for. `ignored` is a loaded
skill that left no trace, which is safe in effect but says nothing about why.

Whether a subject is included under the tier gate rests on the tier scale, so claims about the
tier gate carry the ground truth's evidence kind (assumed for the Anthropic subjects, observed
against documentation for the OpenAI subject), as every tier claim does.

Two things the gated skills cannot show. The Codex pair is included only under the tier gate,
where its self-placement is already known to fail, so its ability to load a gated skill it is
meant for is not cleanly tested here; that it loads an unconditional skill is established by
Studies 1 and 2. And a gate that holds at the description is a harness feature as much as a model
one: the model can only refuse what it was shown, so a harness that did not list descriptions
before loading could not gate at all. Both harnesses tested do.

### Selection sets (`select-vendor`, `select-tier`): one skill among alternatives

A set is two or three skills installed together in the same run, whose descriptions say the same
thing except which model each is for, so that choosing is reading the descriptions against
oneself and nothing else. Each skill's body writes a marker file named after the skill
(`picked-<name>.txt`), appends its trace line, and does its work.

- `select-vendor`: `feature-anthropic` and `feature-openai`. Both bodies prescribe the same work,
  a docstring and one test, so the work is neutral and only the marker and the trace show the
  choice. This is the control: selection with a condition both pairs know.
- `select-tier`: `feature-flagship`, `feature-mid` and `feature-small`, one per tier. Their bodies
  are the three `tiered-feature` branches (a docstring and at least three tests; a docstring and
  one test; a TODO line and no tests), so scoring infers the tier from the work as it does there,
  and the work shows which skill was followed independently of the marker. The payoff is the
  downward pull of `tiered-feature`: the flagship skill costs the most, so a model claiming a lower
  tier saves work. The three skills sit beside the harness's own skills as everywhere else.

Prompts: the same F1..F3 texts, ids SV1..SV3 and ST1..ST3 (`prompts/gate.jsonl`). Deliveries:
`native` and `pointer`, where the pointer file lists every skill in the set with its description
and path.

Each run gets a **selection outcome** from which skills of the set were followed, meaning their
trace line or marker file was written: `correct` (exactly the expected skill), `wrong` (exactly
one other), `several` (more than one), `none`. The expected skill follows from the subject's
vendor or tier in `ground_truth.json`. Scoring also records whether the work matches the skill
that was followed, so a model that picked correctly and then did another skill's work is visible.
Reading is recorded separately from following: a skill that was invoked or read but left no trace
or marker counts as read only, since reading the alternatives to decide is reasonable and following
more than one is not, and the report gives the read-only rate beside the outcome.

## Ground truth

`ground_truth.json` holds, per subject, the values the stamps and branches are scored against, and
a `sources` map saying where each value comes from. A source must be independent of the runs it
scores: experiment configuration (harness, model, vendor), a harness's own feature listing
(`codex features list`), the tool list a harness prints when a session starts (Claude Code's
init event), product documentation (hooks; the OpenAI model's tier), or a stated assumption (the
Anthropic models' tiers). A value that could only be established from the scored
runs themselves is marked `from_runs: true`, and every claim that scores against it is evidence
kind *inferred* with the circularity named: the runs are being checked against a fact learned
from the runs. At present that applies to `subagents_session` for the Codex pair, which has no
session tool listing; establishing it independently needs a probe outside the corpus.

Study 3 adds no values. Whether a subject is included under a gate, and which skill of a set it
is expected to pick, follow from its `vendor` and `tier`, so a gate or selection claim carries the
evidence kind of the value it derives from: observed for vendor, and for tier the same split as
every tier claim.

## Measures

1. **Skill loaded**: transcript shows the skill being invoked or `SKILL.md` being read, or
   `.skill-trace` contains the skill name (every skill asks for that line). A branch can only
   run if the skill was loaded, so this is reported as a precondition. In Study 3 loading is an
   outcome as well: a gated skill left unloaded by an excluded subject is the gate holding, and
   the loads in a selection set say which alternative was chosen. A `declined` trace line counts
   as loaded, since the body was read.
2. **Deterministic outcome**: files on disk after the run, stamp values against ground truth,
   branch file present, feature and tests executed, delegation call seen in the transcript. For
   Study 3, the gate outcome and the selection outcome defined there, and whether the work matches
   the skill that was loaded.
3. **Adherence (LLM judge), optional**: Fable 5.1 grades a valid skill run on format followed,
   no unrequested actions, claims match actions, 0 to 2 each. No claim rests on these scores, and
   the findings never cited one, so the judge is not part of a refresh (see Scope decisions). The
   step remains for anyone who wants the scores; `report.py` shows them where a `judge.json`
   exists and leaves the columns empty otherwise. Baseline runs are never judged, since there is
   no skill to grade against.
4. **Efficiency**, per run:
   - **Tool invocations**: every tool call the agent makes. In Claude Code, each `tool_use` block
     (Bash, Read, Write, Edit, Skill, Agent, WebSearch, ...). In Codex, every transcript item
     that is not a message, reasoning or error (`command_execution`, `file_change`,
     `collab_tool_call`, `web_search`, ...). This is the step count both harnesses expose, but
     the harnesses offer different tool sets, so the same piece of work can take a different number
     of invocations in each. Treat cross-harness differences as indicative; how the granularity
     actually differs is a claim, computed from the transcripts, not a design assumption.
   - **Turns**: Claude Code's reported `num_turns`, Claude Code only. Codex reports no turn count.
   - **Tokens**: input and output, summed over the session. Input includes cached input for both
     harnesses, so it measures context processed, not tokens billed.
   - **Wall time**: from launching the agent to its exit. Runs interrupted by the machine sleeping
     are left out of time comparisons.
   - **USD**: as reported by Claude Code. Codex reports none.

## Run validity

A run can fail for reasons that have nothing to do with the agent, such as a lost network or the
machine sleeping. Those runs must not be scored as agent behaviour. `bin/score.py` classifies every
run on two independent flags.

**Invalid**: the outcome is unusable. A run is invalid if it timed out; for Claude Code, if the
transcript has no final result, or the final result is an error other than reaching the turn
limit (an API error exits 0 or 1 with `is_error` set); for Codex, if a turn failed, no turn
completed, or the exit code is not 0. Invalid runs are excluded from every table and from judging,
listed at the top of `summary.md`, and rerun with `bin/run.py --rerun-invalid`. A run directory
without `meta.json` was interrupted before it finished; it is listed as incomplete and a plain
rerun redoes it.

**Timing invalid**: the outcome stands but time measurements do not. `bin/run.py` records both wall
time and active time (a monotonic clock that stops while the machine sleeps); a gap of more than
30 s means the machine slept. Runs recorded before active time was added are timing invalid when
their wall time exceeds the run timeout, which the timeout's own sleep-stopping clock makes
impossible otherwise. A Codex run that logged network reconnects is also timing invalid. These
runs stay in every outcome table and are left out of wall-time means.

Reaching the turn limit is agent behaviour, not a failure: such a run is valid and scored on what
it produced.

## Scale

Studies 1 and 2: 4 subjects x 3 delivery x (6 + 9 prompts) x 2 reps = 360 skill runs, plus 4
subjects x 6 baseline prompts x 2 reps = 48 baseline runs, 408 in total. Study 3: the gated skills
are 4 subjects x 3 delivery x 6 prompts x 2 reps = 144 runs, and the selection sets 4 subjects x 2
delivery x 6 prompts x 2 reps = 96, so 240 more and 648 in all. Study 3 reuses the Study 2
baselines and adds none. `bin/run.py` accepts filters so a subset can be
run first: `--delivery inline` for the inline control, `--prompts G1 G2 G3` for one skill,
`--prompts B1 B2 B3` or `--prompts BR1 BR2 BR3` for a baseline, `--study gate` for Study 3. Which runs were made when is
corpus history and is recorded in `claims.md`, not here; `report.py` derives it from each run's
`meta.json` (its `started` timestamp and rerun status), so history is never typed by hand and
cannot be lost when `FINDINGS.md` is regenerated.

## Pipeline

```
bin/run.py    --subjects ... --delivery ... --prompts ... --reps N   # results/runs/<id>/
bin/score.py                                                        # score.json per run
bin/run.py    --rerun-invalid, then bin/score.py again               # redo runs score.py marked invalid
bin/judge.py                                                        # optional: judge.json per run; not part of a refresh
bin/report.py                                                       # summary.md, runs.csv, claims.md, claims.json
bin/findings.py                                                     # FINDINGS.md, written by an LLM and validated
```

## Report

The whole report is generated. The only hand-written input is this document: its questions,
rules and caveats carry every judgement the report makes. Anything else a finding needs must come
from the runs, so a finding that seems to need hand-written input means this document is missing
something, and it is added here.

The report holds three kinds of content, trusted for different reasons:

| kind | example | file | why it can be trusted |
|---|---|---|---|
| numbers | a subject loaded the skill in k of n pointer runs | `summary.md`, `runs.csv`, `claims.md` | computed from the runs |
| checkable verdicts | no subject changed its reported tier across the tier skills | `claims.md` | re-evaluated on every refresh |
| interpretation | a branch that equals the default proves nothing | `FINDINGS.md` | written from the two above and this document, then validated |

### Claims

A claim is a checkable statement about the runs. Claims live in `bin/claims.py`. Each has:

- an **ID**, stable across refreshes, such as `tier-stable` or `review-baseline-no-delegation`;
- the **question** it answers: branching, portability, efficiency or placement, meaning where the
  condition sits (see Goal);
- a **statement** with placeholders for its numbers, including the n behind every rate, such as
  "No subject changed its reported tier across Study 1, `tiered-feature` and `tiered-guidance`
  ({subjects} subjects, {runs} runs).";
- a **check**: a function of the valid scored runs that returns whether the claim holds and the
  values for its placeholders;
- its **evidence kind**: observed (seen in files or transcripts), inferred (reasoned from indirect
  evidence, named in the statement), or assumed (resting on ground truth the runs do not verify,
  such as a model's tier);
- optional **exhibits**: short excerpts pulled from run transcripts or files by a deterministic
  rule, such as a model's explanation of its tier or a review that missed a planted bug, each with
  its run ID. They let a finding quote the runs without anyone reading transcripts.

Negative results are claims too, such as a claim that a subject never reported its exact model
version, so a failure is as visible as a success. Claims are written to hold on the
current corpus; a claim that stops holding is news.

On every refresh `bin/report.py` evaluates all claims and writes:

- `results/claims.md`, grouped by question: each claim's filled-in statement, evidence kind,
  exhibits and status, **holds** or **fails**, plus two change marks against the last refresh:
  *status changed* (holds became fails or the reverse) and *numbers changed* (the same status with
  different values, which happens to nearly every claim when runs are added). Only a status change
  flags a `FINDINGS.md` paragraph;
- `results/claims.json`, the claim values from this refresh, committed so the next refresh can tell
  what changed.

`claims.md` opens with the corpus it was computed from: the number of valid runs, the dates of each
batch, reruns, the invalid and timing-invalid runs, and a fingerprint: a hash over the valid runs'
`run_id` and outcome fields only (`valid`, `triggered`, `outcome_ok`, `stamp`, `fields`,
`reported_tier`, `implied_tier`, `mode`, `delegated_call`, `findings_ok`, `gate_outcome`,
`selection_outcome`), so timing, tokens and free text such as error messages cannot change it.

### FINDINGS.md

`bin/findings.py` writes `FINDINGS.md` with an LLM, then validates it.

**Inputs**: this document, `claims.md` and `summary.md`. Not the raw runs: the model must not
compute numbers or verdicts itself, and whatever it needs from the runs reaches it as a claim or
an exhibit.

**Output**: one section per question in the Goal, each answering the question first and then giving
the evidence; the caveats that bound the answers; and guidance for skill authors. It opens with a
number-free summary of the four answers, followed by a section "Answers to the six questions": a
table with one row per question in the Goal's six-question table, in that order, giving the
question, its answer in one or two sentences stated per pair where the pairs differ, and the
section of the file that carries the evidence. The file's four question sections follow the
design's mechanisms, not the six use cases, and this table is where a reader who arrived with
the six questions finds each answer without learning the mapping. It uses subheadings and bullet
lists, may carry one small table per question copied from a claim, and may quote a claim's
exhibits verbatim. Guidance is
derived, not invented: one item per kind of branch condition (vendor, harness, exact version, tier,
capability from knowledge, capability from the session's tools), one per place a condition can sit
(a gate in the description, selection among alternatives, a bail-out in the body) and one per
delivery condition, each saying use, do not use, or use with a stated caveat, decided only by
which claims hold. The placement items say for which condition kinds the placement worked, since a
gate on vendor and a gate on tier may not behave alike. It
recommends nothing the claims do not cover. Every paragraph, bullet and table ends with a citation
line naming the claims it rests on, each linked to its entry in `claims.md`
(`*Claims: [tier-stable-claude](claims.md#tier-stable-claude)*`). The header records the corpus
fingerprint and the generator's model.

**Validation**, deterministic, before the file is written:

- every numeral in the body appears in `claims.md` or `summary.md`; a derived figure such as a
  ratio or a difference must therefore be a claim of its own, since the prose may not do arithmetic.
  The header (fingerprint, dates, generator model) is exempt and checked separately;
- every paragraph, bullet and table has a citation line, every cited claim exists, and a claim
  cited as support holds;
- every section is present, the summary contains no numbers, and the six-question table has six rows;
- every passage in quotation marks is a verbatim exhibit from `claims.md`;
- no harness is named as the subject of a result without its model (see the rules below);
- the fingerprint matches the current corpus.

A failed check is returned to the model as an error to fix. If the draft still fails after three
attempts, `findings.py` exits with an error and leaves the previous `FINDINGS.md` in place.

The model and prompt are fixed in `bin/findings.py`, and `FINDINGS.md` is committed, so every
regeneration is reviewed as a diff. Validation limits what the model can get wrong to wording;
numbers and verdicts cannot drift. Because the writer is a Claude model reporting on Claude models,
the generator's model is named in the file header.

`FINDINGS.md` was written by hand before this mechanism existed; the generated version replaced it,
and the hand-written one is not kept. A draft that fails every attempt is saved as
`results/FINDINGS.rejected.md` (gitignored) for inspection.

### Rules for claims and findings

- **Name the pair, not the harness.** Harness and model are confounded (see Known asymmetries), so
  a claim or finding is stated for a subject, such as "the Claude models in Claude Code" or "Codex
  with gpt-5.6-luna", never as a property of a harness alone.
- **Say how a claim is known,** using the evidence kinds above.
- **Give n with every rate.** Cells are small (2 reps), so a rate without its count misleads.
- **Check a branch against its baseline before crediting it.** A branch whose prescribed work is
  what the model does without the skill is not evidence the branch was followed. Claims that credit
  a branch are paired with a baseline claim, and a finding says when a branch equals the default.
- **Date the corpus.** Runs are made in batches; `claims.md` records them, and a finding flags any
  comparison between batches run on different days.
- **Report exclusions,** as in Run validity; `claims.md` lists them.
- **Tier claims carry the ground truth's evidence kind.** The tier scale is a construct; where a
  subject's placement on it is an assumption (the Anthropic subjects, see Known asymmetries) a
  claim about its tier correctness is *assumed*, and where it is taken from the vendor's
  documentation (the OpenAI subject) the claim is *observed* against that source.
- **A difference smaller than a whole cell is not a difference.** With two reps, one run flips a
  cell's rate by half; a claim may only report a difference between conditions that holds across
  entire cells.

## Known asymmetries and caveats

- **Harness and model are confounded.** Claude models run only in Claude Code and the GPT model
  only in Codex, so any difference between the two subjects' behaviour may come from the harness,
  the model, or both. Separating them needs a model run in both harnesses.
- **Neither harness sees only the target skill.** In Claude Code, `--setting-sources project`
  drops user skills and plugins, but the built-in skills (code-review, simplify, loop, ...) are
  still listed next to the target; an isolated `CLAUDE_CONFIG_DIR` loses authentication on macOS
  (keychain), so this was left as is. Codex installs its own system skills into every `CODEX_HOME`
  on startup (`skills/.system/`: review-agent, skill-creator, plugin-creator, skill-installer,
  openai-docs, imagegen), so the isolated home holds those beside the target too. The two
  catalogs differ, and a model may consult a system skill during a run; `openai-docs` in
  particular can send Codex to OpenAI's documentation when a prompt concerns OpenAI models.
- **Web access.** Both harnesses expose a web search tool (Claude Code: `WebSearch`/`WebFetch`;
  Codex: `web_search` items), so an identity or capability answer may come from a lookup rather
  than from the model's own knowledge. Whether a run searched is visible in the transcript and is
  counted among its tool invocations; a claim about self-knowledge must separate runs that looked
  something up from runs that did not.
- **Codex binary**: `~/.local/bin/codex` is a symlink into ChatGPT.app, and Codex looks for
  `codex-code-mode-host` next to argv[0], so `codex exec` fails with the symlink. The driver
  resolves the real path and calls that. Nothing on the machine was changed.
- **Codex isolation**: each run gets its own `CODEX_HOME` with a symlinked `auth.json`, a
  minimal `config.toml` (model, high reasoning, approval never, workspace-write sandbox,
  workspace trusted) and the skill under `skills/`. Your plugins and MCP servers are not loaded.
- **Judge, if run**: about USD 0.10 to 0.22 per judged run with Fable 5.1, a Claude model grading
  Claude models alongside Codex, never checked against human grading. Its scores are evidence of
  adherence to the skill text, not of correctness, and a vendor bias in either direction cannot be
  ruled out. The findings generator is a Claude model too (its model is named in the `FINDINGS.md`
  header).
- **Two reps per cell.** A difference smaller than one whole cell cannot be resolved: a single
  run changes a cell's rate by half, so cell-level numbers are noise bounds, not trends.
- **One skill per run, except in Study 3's selection sets,** whose alternatives are written to be
  disjoint: same task, same wording, different model condition. Competition between overlapping
  skills, and selection among a large catalogue, are untested.
- **Descriptions are shown before loading in both harnesses.** Claude Code lists each installed
  skill's name and description in the model's context and loads the body on invocation; Codex
  lists the skills under `$CODEX_HOME/skills` the same way. A gate in the description can only
  hold where this is true, so Study 3's gate results are about these two harnesses' listings as
  much as about the models. In `pointer` delivery the instructions file plays the listing's role.
- **Capability scope.** Capability branches cover harness tools only; model-level properties such
  as image input or context size are not tested.
- **Tier is a supplied name, not measured capability.** A model's tier answer rests on what it is
  told or knows about its own name, or on a guess; no run measures whether its tier matches its
  capability on the task.
- **Model field** in `vendor-stamp` is strict: the answer must contain a token unique to the
  actual model (opus, sonnet, haiku, luna), so Opus, Sonnet and Haiku are never interchangeable
  and a family name alone is wrong. Tokens live in `model_tokens` in `ground_truth.json`.
- **Tier scale**: three labels over each vendor's lineup. The skills ask a model to place itself
  in its vendor's *current* lineup, which for Anthropic includes Fable, yet the ground truth scores
  Opus as flagship because the scale is defined over the subjects, not the vendor's lineup. So the
  skill's question and the ground truth disagree in scope, an Opus answer of "flagship" would hold
  by construction, and a tier result means "consistent with the chosen scale", not "knows its
  rank". The OpenAI subject's tier comes from OpenAI's model documentation, which places
  gpt-5.6-luna at the bottom of its family, so for that pair the scale and the vendor's lineup
  agree and the tier is documented rather than assumed; it was recorded as an assumption of
  "flagship" until checked. Tier-correctness claims about the Anthropic subjects are evidence kind
  *assumed*; about the OpenAI subject, *observed* against documentation (see Rules for claims and
  findings). With Fable added as a subject the scale needs a fourth label or Opus moves to mid.
- **Product-level vs session-level ground truth** for `harness-stamp`. The ground truth encodes
  the product feature (`codex features list`: multi_agent enabled), which need not match what a
  given session exposes. The session-level value for subagents has a different provenance per
  pair; see Ground truth. The hooks and image-generation values stay in `ground_truth.json` for
  the first corpus's record but are no longer asked or scored.
- **Judge input excludes bytecode caches,** if the judge is run. The scorer imports `src.app` and
  runs the agent's tests, which creates `__pycache__` directories in the workspace before the
  judge sees it, so the judge's diff excludes them; otherwise scope discipline would be docked for
  files the agent never wrote.

## Scope decisions

Parts of the design that were cut or narrowed after the first corpus (408 runs, September 2026),
with the reason, so a reader of an older `FINDINGS.md` can see what changed and why.

- **The LLM judge is optional (September 2026).** Every claim in the first corpus was
  deterministic; none used an adherence score and the findings cited none, so the judge was the
  most expensive step per run after the runs themselves with no bearing on the answers. It stays
  in `bin/` and in the report's columns, and is left out of a refresh.
- **`harness-stamp` asks only about subagents (September 2026).** Hooks and image generation
  cannot be observed from inside a session, no branch depended on them, and the review skill tests
  the subagents capability better, from the session's tools. The two questions were dropped and
  the cells rerun with the one-question skill, so the first corpus's three-question answers are
  replaced rather than compared.
- **Kept, deliberately.** `tiered-feature` tests the pull opposite to the motivating case and found
  nothing moved; it stays for the incentive contrast and the light-versus-heavy cost comparison,
  but is not extended. `tool-gated-review` answers a capability question the placement questions
  do not ask; it stays for its guidance item and its delegation cost comparison.
