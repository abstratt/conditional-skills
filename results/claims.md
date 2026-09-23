# Claims

Checkable statements about the runs, re-evaluated on every refresh (see DESIGN.md, Report). Status is holds or fails; a claim is marked *status changed* or *numbers changed* against the last committed refresh.

## Corpus

- valid runs: 408 (skill runs 360, baseline runs 48)
- batches by start date: 2026-09-22: 225, 2026-09-23: 183
- reruns recorded in meta.json: none
- invalid runs (excluded): none
- incomplete run directories: none
- timing-invalid runs (kept, excluded from wall-time means): `claude-haiku__native__G3__r2`, `claude-sonnet__pointer__G2__r2`, `claude-sonnet__pointer__G3__r1`, `codex-default__native__G1__r1`, `codex-default__native__G1__r2`, `codex-default__native__G2__r1`
- fingerprint: `237f5539c092f0e6`

## Question 1: can a skill branch on model identity or capability?

<a id="vendor-harness-correct"></a>
### `vendor-harness-correct` — holds, observed

Every subject reported its vendor and harness correctly in every `vendor-stamp` run (48 of 48 runs, 4 subjects, all deliveries).

<a id="model-version-claude"></a>
### `model-version-claude` — holds, observed

The Claude models in Claude Code reported a name containing their exact model token in every `vendor-stamp` run (36 of 36); Haiku's answers included the dated model ID it was configured with.

- exhibit `claude-haiku__inline__V1__r2`: AGENT.txt model: claude-haiku-4-5-20251001

<a id="model-version-codex"></a>
### `model-version-codex` — holds, observed

Codex with gpt-5.6-luna never reported a name containing its model token in any `vendor-stamp` run (0 of 12); it answered gpt-5: 12.

<a id="tier-claude-correct"></a>
### `tier-claude-correct` — holds, assumed

Each Claude model reported its ground-truth tier in every tier answer where the skill loaded (130 of 130 answers across `tier-stamp`, `tiered-feature` and `tiered-guidance`); the Anthropic tiers are an assumed scale over the subjects.

- exhibit `claude-sonnet__inline__G1__r1`: Done — tier `mid` (Sonnet 5). Implemented `slugify` with a docstring in `src/app.py`, added one test in `tests/test_app.py`, and appended `tiered-guidance` to `.skill-trace`.

<a id="tier-codex-incorrect"></a>
### `tier-codex-incorrect` — holds, observed

Codex with gpt-5.6-luna never reported its documented tier (small) in any tier answer (0 of 48); it reported flagship: 46, mid: 2. OpenAI's documentation places Luna at the bottom of its family.

<a id="tier-stable-claude"></a>
### `tier-stable-claude` — holds, observed

Each Claude model reported a single tier across all tier skills and deliveries (130 answers, 3 subjects), including `tiered-guidance`, where a higher tier saved work.

<a id="tier-codex-varies"></a>
### `tier-codex-varies` — holds, observed

Codex with gpt-5.6-luna reported 2 different tiers (flagship: 46, mid: 2); the non-flagship answers came from runs that searched OpenAI's documentation (3 such runs, all under `inline` delivery).

- exhibit `codex-default__inline__F2__r2`: I’m using the OpenAI product guidance skill to determine the model tier, then I’ll make only the requested file changes and run the available test command.
- exhibit `codex-default__inline__T1__r1`: e to classify the model performing the work. I’ll then write only the requested tier files and trace entry.

<a id="tier-no-inflation-claude"></a>
### `tier-no-inflation-claude` — holds, assumed

Under `tiered-guidance`, where claiming a higher tier saves work, Sonnet and Haiku reported the same tier as in Study 1 in every loaded run (30 of 30); no Claude model inflated its tier.

<a id="codex-overclaims-under-both-incentives"></a>
### `codex-overclaims-under-both-incentives` — holds, observed

Codex with gpt-5.6-luna claimed a tier above its own in 48 of 48 loaded tier answers, both when a higher tier cost extra work (`tiered-feature`: 18 of 18) and when it saved work (`tiered-guidance`: 18 of 18), so the overclaim is not driven by the payoff.

<a id="guidance-skipped-by-codex"></a>
### `guidance-skipped-by-codex` — holds, observed

Under `tiered-guidance`, Codex with gpt-5.6-luna, whose documented tier is small, took the flagship branch and skipped the checklist written for small models in 18 of 18 loaded runs.

<a id="work-matches-report"></a>
### `work-matches-report` — holds, observed

In every loaded `tiered-feature` and `tiered-guidance` run, the work matched the tier the agent reported (130 of 130 runs, all subjects and deliveries).

<a id="baseline-default-is-flagship-branch"></a>
### `baseline-default-is-flagship-branch` — holds, observed

With no skill, every subject implemented the feature with no docstring and no tests in every baseline run (24 of 24), which is exactly the `tiered-guidance` flagship branch; a run that takes that branch is indistinguishable in its work from a run that never loaded the skill.

<a id="work-adding-branches-changed-behaviour"></a>
### `work-adding-branches-changed-behaviour` — holds, observed

Every branch that prescribes tests changed behaviour: in loaded runs of those branches the agent wrote tests in 84 of 84 runs, against 0 of 24 baseline runs on the same prompts.

<a id="haiku-skips-feature-skills-natively"></a>
### `haiku-skips-feature-skills-natively` — holds, observed

Haiku loaded neither feature skill in any native run (0 of 12); with a pointer it loaded them in 10 of 12 runs. Every other subject loaded every skill in every native and pointer run (180 of 180).

<a id="inline-removes-haiku-loading-failure"></a>
### `inline-removes-haiku-loading-failure` — holds, observed

With the same instructions in the prompt (`inline`), Haiku followed both feature skills in 12 of 12 runs, so its native failures were loading failures, not ambiguity in the request.

<a id="capability-from-knowledge-claude"></a>
### `capability-from-knowledge-claude` — holds, observed

The Claude models answered the `harness-stamp` subagents question correctly in every run (36 of 36).

<a id="capability-from-knowledge-codex"></a>
### `capability-from-knowledge-codex` — holds, observed

Codex with gpt-5.6-luna answered the `harness-stamp` subagents question correctly in 4 of 12 runs (answers: no: 8, yes: 4); its product knowledge of its own harness is not reliable enough to branch on.

<a id="capability-from-tools-claude"></a>
### `capability-from-tools-claude` — holds, observed

Told to check the session's tools, the Claude models made a real delegation call in every `tool-gated-review` run (54 of 54).

<a id="haiku-label-contradicts-transcript"></a>
### `haiku-label-contradicts-transcript` — holds, observed

Haiku wrote `mode: inline` after actually delegating in 2 of 18 `tool-gated-review` runs, so its label contradicted its transcript.

<a id="capability-from-tools-codex-partial"></a>
### `capability-from-tools-codex-partial` — holds, inferred

Codex with gpt-5.6-luna delegated in 7 of 18 `tool-gated-review` runs and reviewed inline in the rest, concluding differently about its own tools from run to run; its label always matched what it did (18 of 18). The session ground truth for Codex is inferred from these transcripts.

<a id="review-baseline-no-delegation"></a>
### `review-baseline-no-delegation` — holds, observed

With no skill, no subject delegated a review in any baseline run (0 of 24), so every delegation under `tool-gated-review` was caused by the skill.

<a id="delegation-no-quality-gain"></a>
### `delegation-no-quality-gain` — holds, observed

Delegating did not improve the review on this task: Opus, Sonnet and Codex named both planted bugs in 18 of 18 baseline reviews without delegating, and in 53 of 54 skill runs.

## Question 2: is a single skill file portable?

<a id="portable-identity"></a>
### `portable-identity` — holds, observed

Vendor and harness branches behaved correctly for both pairs: 36 of 36 runs for the Claude models in Claude Code and 12 of 12 for Codex with gpt-5.6-luna.

<a id="not-portable-version"></a>
### `not-portable-version` — holds, observed

Branching on an exact model version worked only for the Claude pair (36 of 36 correct) and never for the Codex pair (0 of 12).

<a id="not-portable-tier"></a>
### `not-portable-tier` — holds, observed

Branching on tier worked for the Claude pair (130 of 130 loaded tier answers correct) and failed for the Codex pair (0 of 48); the difference tracks whether the harness hands the model its exact model ID, which is inferred, not observed.

<a id="not-portable-capability-from-knowledge"></a>
### `not-portable-capability-from-knowledge` — holds, observed

A capability branch answered from product knowledge worked for the Claude pair (36 of 36) and only sometimes for the Codex pair (4 of 12), whose answer to the same question varied from run to run.

<a id="partially-portable-capability-from-tools"></a>
### `partially-portable-capability-from-tools` — holds, inferred

A capability branch that checks the session's tools produced a delegation for the Claude pair in 54 of 54 runs and for the Codex pair in 7 of 18.

<a id="delivery-no-whole-cell-difference-once-loaded"></a>
### `delivery-no-whole-cell-difference-once-loaded` — holds, observed

Among runs where the skill loaded, no subject-and-skill cell had a whole-cell outcome difference between deliveries (largest difference 2 runs in a cell of 6); delivery did not change branch outcomes once the skill was loaded.

<a id="pointer-delivery-portable"></a>
### `pointer-delivery-portable` — holds, observed

Pointer delivery (a `CLAUDE.md` / `AGENTS.md` entry) loaded the skill in 118 of 120 pointer runs across both pairs, against 108 of 120 native runs.

<a id="portable-gate-vendor"></a>
### `portable-gate-vendor` — FAILS, observed

A gate on vendor behaved correctly for both pairs in native and pointer runs: the Claude pair, included, followed the skill whenever it loaded (0 of 0 loaded runs) and the Codex pair, excluded, stayed out (0 of 0).

<a id="not-portable-gate-tier"></a>
### `not-portable-gate-tier` — FAILS, observed

A gate on tier behaved correctly for the Claude pair (0 of 0 native and pointer runs) and not for the Codex pair (0 of 0), which refused the skill written for its documented tier.

<a id="portable-selection-vendor"></a>
### `portable-selection-vendor` — FAILS, observed

Selection by vendor worked for both pairs among runs that chose: the Claude pair 0 of 0, the Codex pair 0 of 0.

<a id="not-portable-selection-tier"></a>
### `not-portable-selection-tier` — FAILS, observed

Selection by tier worked for the Claude pair (0 of 0 runs that chose) and not for the Codex pair (0 of 0).

## Question 3: what does a model-conditional skill cost?

<a id="skill-overhead-tokens"></a>
### `skill-overhead-tokens` — holds (numbers changed), observed

On the same prompts, every subject processed more input tokens with a native skill than with none: claude-opus 92k vs 59k (1.6x, n=18 vs 12); claude-sonnet 215k vs 85k (2.5x, n=18 vs 12); claude-haiku 127k vs 57k (2.2x, n=6 vs 6); codex-default 129k vs 60k (2.2x, n=18 vs 12). (Loaded Study 2 runs against their paired baselines; input tokens include cached input.)

| subject | with skill (native) | no skill | ratio | runs |
|---|---|---|---|---|
| claude-opus | 92k | 59k | 1.6x | 18 vs 12 |
| claude-sonnet | 215k | 85k | 2.5x | 18 vs 12 |
| claude-haiku | 127k | 57k | 2.2x | 6 vs 6 |
| codex-default | 129k | 60k | 2.2x | 18 vs 12 |

<a id="skill-overhead-tool-invocations"></a>
### `skill-overhead-tool-invocations` — holds (numbers changed), observed

On the same prompts, every subject made more tool invocations with a native skill than with none: claude-opus 5.4 vs 2.4 (n=18 vs 12); claude-sonnet 7.9 vs 2.0 (n=18 vs 12); claude-haiku 6.7 vs 3.8 (n=6 vs 6); codex-default 9.2 vs 4.1 (n=18 vs 12).

| subject | with skill (native) | no skill | runs |
|---|---|---|---|
| claude-opus | 5.4 | 2.4 | 18 vs 12 |
| claude-sonnet | 7.9 | 2.0 | 18 vs 12 |
| claude-haiku | 6.7 | 3.8 | 6 vs 6 |
| codex-default | 9.2 | 4.1 | 18 vs 12 |

<a id="inline-cheapest-delivery"></a>
### `inline-cheapest-delivery` — holds (numbers changed), observed

In Study 1, where every subject loaded every skill, `inline` used fewer input tokens than both `native` and `pointer` for every subject: claude-opus inline 40k, native 52k, pointer 53k; claude-sonnet inline 89k, native 128k, pointer 139k; claude-haiku inline 66k, native 84k, pointer 92k; codex-default inline 60k, native 72k, pointer 63k.

| subject | inline | native | pointer |
|---|---|---|---|
| claude-opus | 40k | 52k | 53k |
| claude-sonnet | 89k | 128k | 139k |
| claude-haiku | 66k | 84k | 92k |
| codex-default | 60k | 72k | 63k |

<a id="pointer-vs-native-cost"></a>
### `pointer-vs-native-cost` — holds, observed

In Study 1, pointer delivery cost more input tokens than native for the Claude models (claude-opus 53k vs 52k; claude-sonnet 139k vs 128k; claude-haiku 92k vs 84k) and less for Codex with gpt-5.6-luna (63k vs 72k); the pointer's extra file read is not the whole story.

<a id="lighter-branch-cheaper"></a>
### `lighter-branch-cheaper` — holds (numbers changed), observed

Where a subject has a heavy and a light version of its tier branch on the same prompts, the light version used fewer input tokens: claude-opus light 69k vs heavy 125k; codex-default light 82k vs heavy 130k; claude-haiku light 133k vs heavy 255k. (Loaded runs, all deliveries; Sonnet's mid branch is identical in both skills.)

| subject | light branch | heavy branch |
|---|---|---|
| claude-opus | 69k (tiered-guidance) | 125k (tiered-feature) |
| codex-default | 82k (tiered-guidance) | 130k (tiered-feature) |
| claude-haiku | 133k (tiered-feature) | 255k (tiered-guidance) |

<a id="delegation-costs-more"></a>
### `delegation-costs-more` — holds (numbers changed), observed

Delegating a review cost more input tokens than reviewing without delegating, within every subject: claude-opus 81k vs 60k; claude-sonnet 140k vs 75k; claude-haiku 123k vs 57k; codex-default 199k vs 79k. (Delegated skill runs against the same subject's non-delegated runs: its baseline, and for Codex its skill runs that stayed inline.)

| subject | delegated | not delegated |
|---|---|---|
| claude-opus | 81k | 60k |
| claude-sonnet | 140k | 75k |
| claude-haiku | 123k | 57k |
| codex-default | 199k | 79k |

<a id="staying-out-costs-baseline"></a>
### `staying-out-costs-baseline` — FAILS (numbers changed), observed

A run in which the gate held at the description cost about what the no-skill baseline of the same prompt cost, and one that loaded the skill and then declined cost more: . (Input tokens, per subject; excluded subjects only.)

| subject | not loaded | declined | no skill |
|---|---|---|---|

## Question 4: where can the condition sit?

<a id="gate-vendor-keeps-codex-out"></a>
### `gate-vendor-keeps-codex-out` — FAILS (numbers changed), observed

Under `vendor-gated-guidance` (for Anthropic models only), Codex with gpt-5.6-luna stayed out of the skill in every native and pointer run (0 of 0: not loaded 0, declined 0); it never followed the checklist.

| subject | delivery | not-loaded | declined | followed | ignored | mixed |
|---|---|---|---|---|---|---|

<a id="gate-tier-keeps-opus-sonnet-out"></a>
### `gate-tier-keeps-opus-sonnet-out` — FAILS (numbers changed), assumed

Under `tier-gated-guidance` (for small models only), Opus and Sonnet stayed out of the skill in every native and pointer run (0 of 0: not loaded 0, declined 0); the Anthropic tiers are an assumed scale.

| subject | delivery | not-loaded | declined | followed | ignored | mixed |
|---|---|---|---|---|---|---|

<a id="gate-where-it-held"></a>
### `gate-where-it-held` — FAILS (numbers changed), observed

Among the 0 native and pointer runs in which an excluded subject stayed out of a gated skill, the gate held at the description (skill never loaded) in 0 and in the body (loaded, then declined) in 0: .

| subject | skill | delivery | not-loaded | declined |
|---|---|---|---|---|

<a id="excluded-never-followed"></a>
### `excluded-never-followed` — FAILS, observed

No excluded subject followed a gated skill's checklist in any run, in any delivery (0 followed or mixed of 0 runs).

<a id="bailout-inline"></a>
### `bailout-inline` — FAILS (numbers changed), observed

With a gated skill's body in the prompt (`inline`), where it cannot be left unloaded, excluded subjects declined it in 0 of 0 runs: .

| subject | skill | not-loaded | declined | followed | ignored | mixed |
|---|---|---|---|---|---|---|

<a id="included-followed-when-loaded"></a>
### `included-followed-when-loaded` — FAILS (numbers changed), observed

Every included subject that loaded a gated skill followed its checklist (0 of 0 loaded runs, all deliveries): .

| subject | skill | delivery | not-loaded | declined | followed | ignored | mixed |
|---|---|---|---|---|---|---|---|

<a id="included-loading"></a>
### `included-loading` — FAILS (numbers changed), observed

Included subjects loaded the gated skill written for them in 0 of 0 native and pointer runs: .

| subject | skill | delivery | not-loaded | declined | followed | ignored | mixed |
|---|---|---|---|---|---|---|---|

<a id="gate-tier-codex-refuses-own-skill"></a>
### `gate-tier-codex-refuses-own-skill` — FAILS, observed

Codex with gpt-5.6-luna, whose documented tier is small, stayed out of `tier-gated-guidance`, the skill written for small models, in 0 of 0 native and pointer runs (not loaded 0, declined 0), and declined it in 0 of 0 inline runs; a skill reserved for weaker models cannot rest on its self-placement.

<a id="select-vendor-correct"></a>
### `select-vendor-correct` — FAILS (numbers changed), observed

Given `feature-anthropic` and `feature-openai` side by side, every run that followed a skill followed the one for its vendor (0 of 0 runs that chose; 0 chose none): .

| subject | delivery | correct | wrong | several | none |
|---|---|---|---|---|---|

<a id="select-tier-claude-correct"></a>
### `select-tier-claude-correct` — FAILS (numbers changed), assumed

Given `feature-flagship`, `feature-mid` and `feature-small` side by side, every Claude model run that followed a skill followed the one for its tier (0 of 0 runs that chose; 0 chose none); the tiers are an assumed scale.

| subject | delivery | correct | wrong | several | none |
|---|---|---|---|---|---|

<a id="select-tier-codex-wrong"></a>
### `select-tier-codex-wrong` — FAILS, observed

Codex with gpt-5.6-luna never followed `feature-small`, the skill for its documented tier (0 of 0 runs that chose); it followed .

<a id="select-loading"></a>
### `select-loading` — FAILS, observed

With a selection set installed, subjects followed at least one of its skills in 0 of 0 runs: .

<a id="select-reads-before-choosing"></a>
### `select-reads-before-choosing` — FAILS, observed

In 0 of 0 selection runs that followed exactly one skill, the agent had read at least one other alternative first (the Claude pair 0 of 0, the Codex pair 0 of 0).

<a id="select-work-matches-choice"></a>
### `select-work-matches-choice` — FAILS, observed

In every selection run that followed exactly one skill, the work matched that skill's body (0 of 0).

## FINDINGS.md check

- FINDINGS.md fingerprint `f0021a9e2f7dc551` differs from the current corpus `237f5539c092f0e6`: the file predates the data

