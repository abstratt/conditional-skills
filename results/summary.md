# Results summary

408 valid scored runs.

## Skill loading precondition

A branch can only run if the skill was loaded. Loading rate per subject and delivery, over model-conditional prompts only. `inline` puts the instructions in the prompt, so it cannot fail to load; its column only shows whether the trace line was written:

| subject | delivery | loaded, Study 1 | loaded, Study 2 |
|---|---|---|---|
| claude-haiku | inline | 100% (n=12) | 100% (n=18) |
| claude-haiku | native | 100% (n=12) | 33% (n=18) |
| claude-haiku | pointer | 100% (n=12) | 89% (n=18) |
| claude-opus | inline | 100% (n=12) | 100% (n=18) |
| claude-opus | native | 100% (n=12) | 100% (n=18) |
| claude-opus | pointer | 100% (n=12) | 100% (n=18) |
| claude-sonnet | inline | 100% (n=12) | 100% (n=18) |
| claude-sonnet | native | 100% (n=12) | 100% (n=18) |
| claude-sonnet | pointer | 100% (n=12) | 100% (n=18) |
| codex-default | inline | 100% (n=12) | 100% (n=18) |
| codex-default | native | 100% (n=12) | 100% (n=18) |
| codex-default | pointer | 100% (n=12) | 100% (n=18) |

## Study 1: branch selection

| subject | delivery | skill | stamp present | fields correct | all fields | branch matches truth | branch consistent | outcome ok |
|---|---|---|---|---|---|---|---|---|
| claude-haiku | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | inline | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-haiku | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-opus | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | inline | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | native | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | vendor-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | harness-stamp | 100% (n=4) | 12/12 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| claude-sonnet | pointer | tier-stamp | 100% (n=4) | 4/4 | 100% (n=4) | 100% (n=4) | 100% (n=4) | 100% (n=4) |
| codex-default | inline | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | inline | harness-stamp | 100% (n=4) | 4/12 | 0% (n=4) | 50% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | inline | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | harness-stamp | 100% (n=4) | 2/12 | 0% (n=4) | 25% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | native | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | vendor-stamp | 100% (n=4) | 8/12 | 0% (n=4) | 100% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | harness-stamp | 100% (n=4) | 1/12 | 0% (n=4) | 25% (n=4) | 100% (n=4) | 0% (n=4) |
| codex-default | pointer | tier-stamp | 100% (n=4) | 0/4 | 0% (n=4) | 0% (n=4) | 100% (n=4) | 0% (n=4) |

Field-level detail:

| subject | delivery | field | correct |
|---|---|---|---|
| claude-haiku | inline | harness | 100% (n=4) |
| claude-haiku | inline | hooks | 100% (n=4) |
| claude-haiku | inline | image_generation | 100% (n=4) |
| claude-haiku | inline | model | 100% (n=4) |
| claude-haiku | inline | subagents | 100% (n=4) |
| claude-haiku | inline | tier | 100% (n=4) |
| claude-haiku | inline | vendor | 100% (n=4) |
| claude-haiku | native | harness | 100% (n=4) |
| claude-haiku | native | hooks | 100% (n=4) |
| claude-haiku | native | image_generation | 100% (n=4) |
| claude-haiku | native | model | 100% (n=4) |
| claude-haiku | native | subagents | 100% (n=4) |
| claude-haiku | native | tier | 100% (n=4) |
| claude-haiku | native | vendor | 100% (n=4) |
| claude-haiku | pointer | harness | 100% (n=4) |
| claude-haiku | pointer | hooks | 100% (n=4) |
| claude-haiku | pointer | image_generation | 100% (n=4) |
| claude-haiku | pointer | model | 100% (n=4) |
| claude-haiku | pointer | subagents | 100% (n=4) |
| claude-haiku | pointer | tier | 100% (n=4) |
| claude-haiku | pointer | vendor | 100% (n=4) |
| claude-opus | inline | harness | 100% (n=4) |
| claude-opus | inline | hooks | 100% (n=4) |
| claude-opus | inline | image_generation | 100% (n=4) |
| claude-opus | inline | model | 100% (n=4) |
| claude-opus | inline | subagents | 100% (n=4) |
| claude-opus | inline | tier | 100% (n=4) |
| claude-opus | inline | vendor | 100% (n=4) |
| claude-opus | native | harness | 100% (n=4) |
| claude-opus | native | hooks | 100% (n=4) |
| claude-opus | native | image_generation | 100% (n=4) |
| claude-opus | native | model | 100% (n=4) |
| claude-opus | native | subagents | 100% (n=4) |
| claude-opus | native | tier | 100% (n=4) |
| claude-opus | native | vendor | 100% (n=4) |
| claude-opus | pointer | harness | 100% (n=4) |
| claude-opus | pointer | hooks | 100% (n=4) |
| claude-opus | pointer | image_generation | 100% (n=4) |
| claude-opus | pointer | model | 100% (n=4) |
| claude-opus | pointer | subagents | 100% (n=4) |
| claude-opus | pointer | tier | 100% (n=4) |
| claude-opus | pointer | vendor | 100% (n=4) |
| claude-sonnet | inline | harness | 100% (n=4) |
| claude-sonnet | inline | hooks | 100% (n=4) |
| claude-sonnet | inline | image_generation | 100% (n=4) |
| claude-sonnet | inline | model | 100% (n=4) |
| claude-sonnet | inline | subagents | 100% (n=4) |
| claude-sonnet | inline | tier | 100% (n=4) |
| claude-sonnet | inline | vendor | 100% (n=4) |
| claude-sonnet | native | harness | 100% (n=4) |
| claude-sonnet | native | hooks | 100% (n=4) |
| claude-sonnet | native | image_generation | 100% (n=4) |
| claude-sonnet | native | model | 100% (n=4) |
| claude-sonnet | native | subagents | 100% (n=4) |
| claude-sonnet | native | tier | 100% (n=4) |
| claude-sonnet | native | vendor | 100% (n=4) |
| claude-sonnet | pointer | harness | 100% (n=4) |
| claude-sonnet | pointer | hooks | 100% (n=4) |
| claude-sonnet | pointer | image_generation | 100% (n=4) |
| claude-sonnet | pointer | model | 100% (n=4) |
| claude-sonnet | pointer | subagents | 100% (n=4) |
| claude-sonnet | pointer | tier | 100% (n=4) |
| claude-sonnet | pointer | vendor | 100% (n=4) |
| codex-default | inline | harness | 100% (n=4) |
| codex-default | inline | hooks | 25% (n=4) |
| codex-default | inline | image_generation | 25% (n=4) |
| codex-default | inline | model | 0% (n=4) |
| codex-default | inline | subagents | 50% (n=4) |
| codex-default | inline | tier | 0% (n=4) |
| codex-default | inline | vendor | 100% (n=4) |
| codex-default | native | harness | 100% (n=4) |
| codex-default | native | hooks | 0% (n=4) |
| codex-default | native | image_generation | 25% (n=4) |
| codex-default | native | model | 0% (n=4) |
| codex-default | native | subagents | 25% (n=4) |
| codex-default | native | tier | 0% (n=4) |
| codex-default | native | vendor | 100% (n=4) |
| codex-default | pointer | harness | 100% (n=4) |
| codex-default | pointer | hooks | 0% (n=4) |
| codex-default | pointer | image_generation | 0% (n=4) |
| codex-default | pointer | model | 0% (n=4) |
| codex-default | pointer | subagents | 25% (n=4) |
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


## Adherence (LLM judge, 0-2)

| subject | delivery | n judged | format | scope | honesty |
|---|---|---|---|---|---|
| claude-haiku | inline | 30 | 1.90 | 2.00 | 2.00 |
| claude-haiku | native | 30 | 1.20 | 2.00 | 1.97 |
| claude-haiku | none | 0 | - | - | - |
| claude-haiku | pointer | 30 | 1.67 | 1.97 | 1.87 |
| claude-opus | inline | 30 | 2.00 | 2.00 | 2.00 |
| claude-opus | native | 30 | 1.97 | 2.00 | 1.90 |
| claude-opus | none | 0 | - | - | - |
| claude-opus | pointer | 30 | 2.00 | 2.00 | 1.97 |
| claude-sonnet | inline | 30 | 2.00 | 2.00 | 2.00 |
| claude-sonnet | native | 30 | 1.93 | 2.00 | 2.00 |
| claude-sonnet | none | 0 | - | - | - |
| claude-sonnet | pointer | 30 | 2.00 | 2.00 | 2.00 |
| codex-default | inline | 30 | 1.97 | 2.00 | 2.00 |
| codex-default | native | 30 | 2.00 | 2.00 | 2.00 |
| codex-default | none | 0 | - | - | - |
| codex-default | pointer | 30 | 2.00 | 2.00 | 2.00 |

## Cost and latency (mean per run)

| subject | delivery | cost USD | tokens in | tokens out | tool invocations | turns | wall s |
|---|---|---|---|---|---|---|---|
| claude-haiku | inline | 0.044 | 135292 | 1772 | 6.2 | 7.0 | 24 |
| claude-haiku | native | 0.035 | 86078 | 1005 | 4.1 | 5.4 | 18 |
| claude-haiku | none | 0.031 | 62525 | 706 | 3.0 | 2.9 | 14 |
| claude-haiku | pointer | 0.048 | 128300 | 1560 | 6.8 | 6.9 | 52 |
| claude-opus | inline | 0.158 | 66479 | 1199 | 3.0 | 3.7 | 22 |
| claude-opus | native | 0.212 | 76081 | 1116 | 4.1 | 5.3 | 34 |
| claude-opus | none | 0.125 | 58879 | 938 | 2.4 | 3.4 | 15 |
| claude-opus | pointer | 0.201 | 80707 | 1345 | 4.5 | 4.8 | 27 |
| claude-sonnet | inline | 0.096 | 156405 | 1235 | 5.4 | 6.2 | 20 |
| claude-sonnet | native | 0.106 | 180310 | 1391 | 6.5 | 8.1 | 23 |
| claude-sonnet | none | 0.060 | 84949 | 497 | 2.0 | 3.0 | 8 |
| claude-sonnet | pointer | 0.133 | 195314 | 1552 | 7.2 | 7.2 | 37 |
| codex-default | inline | - | 79652 | 1568 | 4.4 | - | 45 |
| codex-default | native | - | 106140 | 2024 | 7.2 | - | 91 |
| codex-default | none | - | 59772 | 1060 | 4.1 | - | 29 |
| codex-default | pointer | - | 98767 | 1746 | 5.7 | - | 92 |

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
- `claude-haiku__native__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=delegated call=True findings=False
- `claude-haiku__none__BR1__r1`: triggered=False (expected False), outcome_ok=False, changed=[]
- `claude-haiku__none__BR3__r1`: triggered=False (expected False), outcome_ok=False, changed=[]
- `claude-haiku__pointer__F1__r1`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
- `claude-haiku__pointer__F3__r2`: triggered=False (expected True), outcome_ok=False, changed=['src/app.py'], reported=None implied=None feature_ok=True
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
- `codex-default__inline__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'yes', 'subagents': 'no', 'image_generation': 'yes'}
- `codex-default__inline__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'delegates.txt'], stamp={'hooks': 'no', 'subagents': 'yes', 'image_generation': 'no'}
- `codex-default__inline__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'delegates.txt'], stamp={'hooks': 'no', 'subagents': 'yes', 'image_generation': 'no'}
- `codex-default__inline__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
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
- `codex-default__native__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__native__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__native__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'delegates.txt'], stamp={'hooks': 'no', 'subagents': 'yes', 'image_generation': 'yes'}
- `codex-default__native__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__native__R1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__native__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__native__R2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
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
- `codex-default__pointer__H1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__pointer__H1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'delegates.txt'], stamp={'hooks': 'no', 'subagents': 'yes', 'image_generation': 'no'}
- `codex-default__pointer__H2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__pointer__H2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'HARNESS.txt', 'solo.txt'], stamp={'hooks': 'no', 'subagents': 'no', 'image_generation': 'no'}
- `codex-default__pointer__R1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R3__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__R3__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'REVIEW.md'], mode=inline call=False findings=True
- `codex-default__pointer__T1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__T2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'TIER.txt', 'deep.txt'], stamp={'tier': 'flagship'}
- `codex-default__pointer__V1__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V1__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V2__r1`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
- `codex-default__pointer__V2__r2`: triggered=True (expected True), outcome_ok=False, changed=['.skill-trace', 'AGENT.txt', 'stamp-o.txt'], stamp={'vendor': 'openai', 'model': 'gpt-5', 'harness': 'codex'}
