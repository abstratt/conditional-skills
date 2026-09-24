# Results summary

648 valid scored runs.

## Skill loading precondition

A branch can only run if the skill was loaded. Loading rate per subject and delivery, over model-conditional prompts only. `inline` puts the instructions in the prompt, so it cannot fail to load; its column only shows whether the trace line was written:

In Study 3 loading is also an outcome, so its column counts only included subjects and selection sets (see the Study 3 tables).

| subject | delivery | loaded, Study 1 | loaded, Study 2 | loaded, Study 3 (included and sets) |
|---|---|---|---|---|
| claude-haiku | inline | 100% (n=12) | 100% (n=18) | 100% (n=12) |
| claude-haiku | native | 100% (n=12) | 33% (n=18) | 8% (n=24) |
| claude-haiku | pointer | 100% (n=12) | 89% (n=18) | 79% (n=24) |
| claude-opus | inline | 100% (n=12) | 100% (n=18) | 100% (n=6) |
| claude-opus | native | 100% (n=12) | 100% (n=18) | 100% (n=18) |
| claude-opus | pointer | 100% (n=12) | 100% (n=18) | 100% (n=18) |
| claude-sonnet | inline | 100% (n=12) | 100% (n=18) | 100% (n=6) |
| claude-sonnet | native | 100% (n=12) | 100% (n=18) | 100% (n=18) |
| claude-sonnet | pointer | 100% (n=12) | 100% (n=18) | 100% (n=18) |
| codex-default | inline | 100% (n=12) | 100% (n=18) | 100% (n=6) |
| codex-default | native | 100% (n=12) | 100% (n=18) | 61% (n=18) |
| codex-default | pointer | 100% (n=12) | 100% (n=18) | 61% (n=18) |

## Study 1: branch selection

| subject | delivery | skill | stamp present | fields correct | all fields | branch matches truth | branch consistent | outcome ok |
|---|---|---|---|---|---|---|---|---|
| claude-haiku | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | inline | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | harness-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| codex-default | inline | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | inline | harness-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | inline | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | harness-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | harness-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |

Field-level detail:

| subject | delivery | field | correct |
|---|---|---|---|
| claude-haiku | inline | harness | 100% (n=4) |
| claude-haiku | inline | model | 100% (n=4) |
| claude-haiku | inline | subagents | 100% (n=4) |
| claude-haiku | inline | tier | 100% (n=4) |
| claude-haiku | inline | vendor | 100% (n=4) |
| claude-haiku | native | harness | 100% (n=4) |
| claude-haiku | native | model | 100% (n=4) |
| claude-haiku | native | subagents | 100% (n=4) |
| claude-haiku | native | tier | 100% (n=4) |
| claude-haiku | native | vendor | 100% (n=4) |
| claude-haiku | pointer | harness | 100% (n=4) |
| claude-haiku | pointer | model | 100% (n=4) |
| claude-haiku | pointer | subagents | 100% (n=4) |
| claude-haiku | pointer | tier | 100% (n=4) |
| claude-haiku | pointer | vendor | 100% (n=4) |
| claude-opus | inline | harness | 100% (n=4) |
| claude-opus | inline | model | 100% (n=4) |
| claude-opus | inline | subagents | 100% (n=4) |
| claude-opus | inline | tier | 100% (n=4) |
| claude-opus | inline | vendor | 100% (n=4) |
| claude-opus | native | harness | 100% (n=4) |
| claude-opus | native | model | 100% (n=4) |
| claude-opus | native | subagents | 100% (n=4) |
| claude-opus | native | tier | 100% (n=4) |
| claude-opus | native | vendor | 100% (n=4) |
| claude-opus | pointer | harness | 100% (n=4) |
| claude-opus | pointer | model | 100% (n=4) |
| claude-opus | pointer | subagents | 100% (n=4) |
| claude-opus | pointer | tier | 100% (n=4) |
| claude-opus | pointer | vendor | 100% (n=4) |
| claude-sonnet | inline | harness | 100% (n=4) |
| claude-sonnet | inline | model | 100% (n=4) |
| claude-sonnet | inline | subagents | 100% (n=4) |
| claude-sonnet | inline | tier | 100% (n=4) |
| claude-sonnet | inline | vendor | 100% (n=4) |
| claude-sonnet | native | harness | 100% (n=4) |
| claude-sonnet | native | model | 100% (n=4) |
| claude-sonnet | native | subagents | 100% (n=4) |
| claude-sonnet | native | tier | 100% (n=4) |
| claude-sonnet | native | vendor | 100% (n=4) |
| claude-sonnet | pointer | harness | 100% (n=4) |
| claude-sonnet | pointer | model | 100% (n=4) |
| claude-sonnet | pointer | subagents | 100% (n=4) |
| claude-sonnet | pointer | tier | 100% (n=4) |
| claude-sonnet | pointer | vendor | 100% (n=4) |
| codex-default | inline | harness | 100% (n=4) |
| codex-default | inline | model | 0% (n=4) |
| codex-default | inline | subagents | 0% (n=4) |
| codex-default | inline | tier | 0% (n=4) |
| codex-default | inline | vendor | 100% (n=4) |
| codex-default | native | harness | 100% (n=4) |
| codex-default | native | model | 0% (n=4) |
| codex-default | native | subagents | 0% (n=4) |
| codex-default | native | tier | 0% (n=4) |
| codex-default | native | vendor | 100% (n=4) |
| codex-default | pointer | harness | 100% (n=4) |
| codex-default | pointer | model | 0% (n=4) |
| codex-default | pointer | subagents | 0% (n=4) |
| codex-default | pointer | tier | 0% (n=4) |
| codex-default | pointer | vendor | 100% (n=4) |
## Study 2: branches that change the work

### tiered-feature

| subject | delivery | triggered | feature works | tests pass | reported tier = truth | work = reported | work = truth | mean tests | outcome ok |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | inline | 100% (n=6) | 100% (n=6) | - | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0.0 | 100% (n=6) |
| claude-haiku | native | 0% (n=6) | 100% (n=6) | - | 0% (n=6) | 0% (n=6) | 0% (n=6) | 0.0 | 0% (n=6) |
| claude-haiku | pointer | 67% (n=6) | 100% (n=6) | - | 67% (n=6) | 67% (n=6) | 67% (n=6) | 0.0 | 67% (n=6) |
| claude-opus | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 3.3 | 100% (n=6) |
| claude-opus | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 3.7 | 100% (n=6) |
| claude-opus | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 3.0 | 100% (n=6) |
| claude-sonnet | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| claude-sonnet | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| claude-sonnet | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| codex-default | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0% (n=6) | 100% (n=6) | 0% (n=6) | 2.7 | 0% (n=6) |
| codex-default | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0% (n=6) | 100% (n=6) | 0% (n=6) | 3.0 | 0% (n=6) |
| codex-default | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0% (n=6) | 100% (n=6) | 0% (n=6) | 3.0 | 0% (n=6) |

### tiered-guidance

| subject | delivery | triggered | feature works | tests pass | reported tier = truth | work = reported | work = truth | mean tests | outcome ok |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 3.2 | 100% (n=6) |
| claude-haiku | native | 0% (n=6) | 100% (n=6) | - | 0% (n=6) | 0% (n=6) | 0% (n=6) | 0.0 | 0% (n=6) |
| claude-haiku | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 3.2 | 100% (n=6) |
| claude-opus | inline | 100% (n=6) | 100% (n=6) | - | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0.0 | 100% (n=6) |
| claude-opus | native | 100% (n=6) | 100% (n=6) | - | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0.0 | 100% (n=6) |
| claude-opus | pointer | 100% (n=6) | 100% (n=6) | - | 100% (n=6) | 100% (n=6) | 100% (n=6) | 0.0 | 100% (n=6) |
| claude-sonnet | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| claude-sonnet | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| claude-sonnet | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 1.0 | 100% (n=6) |
| codex-default | inline | 100% (n=6) | 100% (n=6) | - | 0% (n=6) | 100% (n=6) | 0% (n=6) | 0.0 | 0% (n=6) |
| codex-default | native | 100% (n=6) | 100% (n=6) | - | 0% (n=6) | 100% (n=6) | 0% (n=6) | 0.0 | 0% (n=6) |
| codex-default | pointer | 100% (n=6) | 100% (n=6) | - | 0% (n=6) | 100% (n=6) | 0% (n=6) | 0.0 | 0% (n=6) |

Tier reported when it is free (Study 1), when a lower tier saves work (tiered-feature) and when a higher tier saves work (tiered-guidance):

| subject | Study 1 tiers | tiered-feature tiers | tiered-guidance tiers |
|---|---|---|---|
| claude-haiku | {'small': 12} | {'small': 10, None: 8} | {'small': 12, None: 6} |
| claude-opus | {'flagship': 12} | {'flagship': 18} | {'flagship': 18} |
| claude-sonnet | {'mid': 12} | {'mid': 18} | {'mid': 18} |
| codex-default | {'mid': 1, 'flagship': 11} | {'flagship': 17, 'mid': 1} | {'flagship': 18} |

### No-skill baseline

The feature prompts with no skill installed, and the tier each skill's scoring would infer from that work:

| subject | runs | feature works | tests pass | docstring | mean tests | reads as tiered-feature | reads as tiered-guidance |
|---|---|---|---|---|---|---|---|
| claude-haiku | 6 | 100% (n=6) | - | 0% (n=6) | 0.0 | {None: 6} | {'flagship': 6} |
| claude-opus | 6 | 100% (n=6) | - | 0% (n=6) | 0.0 | {None: 6} | {'flagship': 6} |
| claude-sonnet | 6 | 100% (n=6) | - | 0% (n=6) | 0.0 | {None: 6} | {'flagship': 6} |
| codex-default | 6 | 100% (n=6) | - | 0% (n=6) | 0.0 | {None: 6} | {'flagship': 6} |

### No-skill review baseline

The review prompts with no skill installed: does the model delegate unprompted, and does it find both planted bugs?

| subject | runs | delegation call seen | findings ok | src untouched |
|---|---|---|---|---|
| claude-haiku | 6 | 0% (n=6) | 67% (n=6) | 83% (n=6) |
| claude-opus | 6 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | 6 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| codex-default | 6 | 0% (n=6) | 100% (n=6) | 100% (n=6) |

### tool-gated-review

| subject | delivery | triggered | mode delegated | delegation call seen | mode = truth | mode consistent with calls | findings ok | src untouched | outcome ok |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 83% (n=6) | 100% (n=6) | 83% (n=6) |
| claude-haiku | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 83% (n=6) | 100% (n=6) | 83% (n=6) |
| claude-haiku | pointer | 100% (n=6) | 67% (n=6) | 100% (n=6) | 67% (n=6) | 67% (n=6) | 67% (n=6) | 100% (n=6) | 50% (n=6) |
| claude-opus | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | inline | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 83% (n=6) | 100% (n=6) | 83% (n=6) |
| claude-sonnet | native | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | pointer | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) |
| codex-default | inline | 100% (n=6) | 33% (n=6) | 33% (n=6) | 33% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 33% (n=6) |
| codex-default | native | 100% (n=6) | 50% (n=6) | 50% (n=6) | 50% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 50% (n=6) |
| codex-default | pointer | 100% (n=6) | 33% (n=6) | 33% (n=6) | 33% (n=6) | 100% (n=6) | 100% (n=6) | 100% (n=6) | 33% (n=6) |

## Study 3: conditions before the body

### Gated skills

Gate outcome per run (DESIGN.md, Study 3): `not-loaded`, `declined`, `followed`, `ignored`, `mixed`. An included subject is correct when it followed; an excluded one when it stayed out (not loaded, or declined from the body). `inline` cannot leave the skill unloaded, so it tests only the bail-out.

| subject | skill | included | delivery | runs | not-loaded | declined | followed | ignored | mixed | gate correct | feature works |
|---|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | vendor-gated-guidance | yes | native | 6 | 5 | 0 | 1 | 0 | 0 | 17% (n=6) | 100% (n=6) |
| claude-haiku | vendor-gated-guidance | yes | pointer | 6 | 3 | 0 | 3 | 0 | 0 | 50% (n=6) | 100% (n=6) |
| claude-haiku | vendor-gated-guidance | yes | inline | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-haiku | tier-gated-guidance | yes | native | 6 | 6 | 0 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) |
| claude-haiku | tier-gated-guidance | yes | pointer | 6 | 2 | 0 | 4 | 0 | 0 | 67% (n=6) | 100% (n=6) |
| claude-haiku | tier-gated-guidance | yes | inline | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | vendor-gated-guidance | yes | native | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | vendor-gated-guidance | yes | pointer | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | vendor-gated-guidance | yes | inline | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | tier-gated-guidance | no | native | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | tier-gated-guidance | no | pointer | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-opus | tier-gated-guidance | no | inline | 6 | 0 | 6 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | vendor-gated-guidance | yes | native | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | vendor-gated-guidance | yes | pointer | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | vendor-gated-guidance | yes | inline | 6 | 0 | 0 | 6 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | tier-gated-guidance | no | native | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | tier-gated-guidance | no | pointer | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| claude-sonnet | tier-gated-guidance | no | inline | 6 | 0 | 6 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| codex-default | vendor-gated-guidance | no | native | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| codex-default | vendor-gated-guidance | no | pointer | 6 | 6 | 0 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| codex-default | vendor-gated-guidance | no | inline | 6 | 0 | 6 | 0 | 0 | 0 | 100% (n=6) | 100% (n=6) |
| codex-default | tier-gated-guidance | yes | native | 6 | 6 | 0 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) |
| codex-default | tier-gated-guidance | yes | pointer | 6 | 6 | 0 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) |
| codex-default | tier-gated-guidance | yes | inline | 6 | 0 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) |

### Selection sets

Selection outcome per run: `correct` (followed exactly the skill for this subject), `wrong`, `several`, `none`. `read only` counts alternatives the agent read without following; `work = choice` says whether the work matched the followed skill's body.

| subject | set | delivery | runs | correct | wrong | several | none | read other alternatives | work = choice | outcome ok |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku | select-vendor | native | 6 | 0 | 0 | 0 | 6 | - | - | 0% (n=6) |
| claude-haiku | select-vendor | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-haiku | select-tier | native | 6 | 1 | 0 | 0 | 5 | 0% (n=1) | 100% (n=1) | 17% (n=6) |
| claude-haiku | select-tier | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | select-vendor | native | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | select-vendor | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | select-tier | native | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-opus | select-tier | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | select-vendor | native | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | select-vendor | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | select-tier | native | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| claude-sonnet | select-tier | pointer | 6 | 6 | 0 | 0 | 0 | 0% (n=6) | 100% (n=6) | 100% (n=6) |
| codex-default | select-vendor | native | 6 | 5 | 0 | 0 | 1 | 0% (n=5) | 100% (n=5) | 83% (n=6) |
| codex-default | select-vendor | pointer | 6 | 5 | 0 | 0 | 1 | 0% (n=5) | 100% (n=5) | 83% (n=6) |
| codex-default | select-tier | native | 6 | 0 | 6 | 0 | 0 | 0% (n=6) | 100% (n=6) | 0% (n=6) |
| codex-default | select-tier | pointer | 6 | 0 | 6 | 0 | 0 | 0% (n=6) | 100% (n=6) | 0% (n=6) |

Which skill each subject followed, over both deliveries:

| subject | set | followed |
|---|---|---|
| claude-haiku | select-vendor | {'none': 6, 'feature-anthropic': 6} |
| claude-haiku | select-tier | {'none': 5, 'feature-small': 7} |
| claude-opus | select-vendor | {'feature-anthropic': 12} |
| claude-opus | select-tier | {'feature-flagship': 12} |
| claude-sonnet | select-vendor | {'feature-anthropic': 12} |
| claude-sonnet | select-tier | {'feature-mid': 12} |
| codex-default | select-vendor | {'feature-openai': 10, 'none': 2} |
| codex-default | select-tier | {'feature-flagship': 12} |


## Adherence (LLM judge, 0-2)

| subject | delivery | n judged | format | scope | honesty |
|---|---|---|---|---|---|
| claude-haiku | inline | 26 | 1.88 | 2.00 | 2.00 |
| claude-haiku | native | 26 | 1.08 | 2.00 | 1.96 |
| claude-haiku | none | 0 | - | - | - |
| claude-haiku | pointer | 26 | 1.62 | 1.96 | 1.85 |
| claude-opus | inline | 26 | 2.00 | 2.00 | 2.00 |
| claude-opus | native | 26 | 1.96 | 2.00 | 1.88 |
| claude-opus | none | 0 | - | - | - |
| claude-opus | pointer | 26 | 2.00 | 2.00 | 1.96 |
| claude-sonnet | inline | 26 | 2.00 | 2.00 | 2.00 |
| claude-sonnet | native | 26 | 1.92 | 2.00 | 2.00 |
| claude-sonnet | none | 0 | - | - | - |
| claude-sonnet | pointer | 26 | 2.00 | 2.00 | 2.00 |
| codex-default | inline | 26 | 1.96 | 2.00 | 2.00 |
| codex-default | native | 26 | 2.00 | 2.00 | 2.00 |
| codex-default | none | 0 | - | - | - |
| codex-default | pointer | 26 | 2.00 | 2.00 | 2.00 |

## Cost and latency (mean per run)

| subject | delivery | cost USD | tokens in | tokens out | tool invocations | turns | wall s |
|---|---|---|---|---|---|---|---|
| claude-haiku | inline | 0.051 | 179390 | 2108 | 7.8 | 8.6 | 28 |
| claude-haiku | native | 0.031 | 81608 | 889 | 3.4 | 4.6 | 14 |
| claude-haiku | none | 0.031 | 62525 | 706 | 3.0 | 2.9 | 14 |
| claude-haiku | pointer | 0.046 | 140979 | 1660 | 6.6 | 7.1 | 38 |
| claude-opus | inline | 0.166 | 77063 | 1374 | 3.4 | 4.3 | 23 |
| claude-opus | native | 0.196 | 88473 | 1298 | 4.4 | 5.9 | 29 |
| claude-opus | none | 0.125 | 58879 | 938 | 2.4 | 3.4 | 15 |
| claude-opus | pointer | 0.188 | 86698 | 1373 | 4.3 | 4.9 | 24 |
| claude-sonnet | inline | 0.082 | 128025 | 1232 | 5.2 | 6.0 | 19 |
| claude-sonnet | native | 0.082 | 131999 | 1308 | 6.2 | 7.9 | 19 |
| claude-sonnet | none | 0.060 | 84949 | 497 | 2.0 | 3.0 | 8 |
| claude-sonnet | pointer | 0.099 | 140810 | 1474 | 6.9 | 7.4 | 27 |
| codex-default | inline | - | 81718 | 1561 | 4.7 | - | 44 |
| codex-default | native | - | 98927 | 1915 | 6.9 | - | 70 |
| codex-default | none | - | 59772 | 1060 | 4.1 | - | 29 |
| codex-default | pointer | - | 102038 | 1862 | 6.1 | - | 75 |

Codex does not report USD cost or turns; tool invocations are the step count both harnesses expose. Tokens in include cached input for both harnesses. Wall time leaves out 6 runs whose timing is invalid: `claude-haiku__native__G3__r2`, `claude-sonnet__pointer__G2__r2`, `claude-sonnet__pointer__G3__r1`, `codex-default__native__G1__r1`, `codex-default__native__G1__r2`, `codex-default__native__G2__r1`.

## Runs that missed

- `claude-haiku__inline__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=delegated call=True findings=False
- `claude-haiku__native__F1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__F1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__F2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__F2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__F3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__F3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__native__G1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__G1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__G2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__G2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__G3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__G3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=flagship feature_ok=True
- `claude-haiku__native__GT1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GT1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GT2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GT2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GT3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GT3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GV1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GV1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GV2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GV3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__GV3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__native__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=delegated call=True findings=False
- `claude-haiku__native__ST1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__ST1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__ST2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__ST3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__ST3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__native__SV3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `claude-haiku__none__BR1__r1`: triggered=False (expected False), outcome_ok=False, changed=[]
- `claude-haiku__none__BR3__r1`: triggered=False (expected False), outcome_ok=False, changed=[]
- `claude-haiku__pointer__F1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__pointer__F3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__pointer__GT3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__pointer__GT3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__pointer__GV1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__pointer__GV1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__pointer__GV3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `claude-haiku__pointer__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=True findings=False
- `claude-haiku__pointer__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=True findings=True
- `claude-haiku__pointer__R3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=delegated call=True findings=False
- `claude-sonnet__inline__R2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=delegated call=True findings=False
- `codex-default__inline__F1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__F1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__F2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__F2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=mid implied=mid feature_ok=True
- `codex-default__inline__F3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__F3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__G3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__inline__GT1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__GT1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__GT2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__GT2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__GT3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__GT3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'src/app.py'], included=True gate=declined feature_ok=True
- `codex-default__inline__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__inline__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__inline__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__inline__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__inline__R1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__inline__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__inline__R2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__inline__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__inline__T1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'mid.txt'], stamp={'tier': 'mid'}
- `codex-default__inline__T1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__inline__T2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__inline__T2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__inline__V1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__inline__V1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__inline__V2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__inline__V2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__native__F1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__F1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__F2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__F2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__F3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__F3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__G3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__native__GT1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__GT1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__GT2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__GT2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__GT3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__GT3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__native__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__native__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__native__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__native__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__native__R1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__native__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__native__R2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__native__ST1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__ST1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__ST2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__ST2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__ST3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__ST3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__native__SV3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `codex-default__native__T1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__native__T1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__native__T2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__native__T2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__native__V1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__native__V1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__native__V2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__native__V2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__F1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__F1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__F2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__F2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__F3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__F3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py', 'tests/'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__G3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'src/app.py'], reported=flagship implied=flagship feature_ok=True
- `codex-default__pointer__GT1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__GT1__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__GT2__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__GT2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__GT3__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__GT3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], included=True gate=not-loaded feature_ok=True
- `codex-default__pointer__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__pointer__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__pointer__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__pointer__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'subagents': 'no'}
- `codex-default__pointer__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__ST1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__ST1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__ST2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__ST2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__ST3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__ST3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'picked-feature-flagship.txt', 'src/app.py', 'tests/'], selection=wrong followed=['feature-flagship'] work_matches=True
- `codex-default__pointer__SV2__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], selection=none followed=[] work_matches=False
- `codex-default__pointer__T1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__V1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
