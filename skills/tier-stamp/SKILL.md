---
name: tier-stamp
description: Produce the model tier stamp for this workspace. Use whenever the user asks to record, classify, or stamp the size, tier, or capability class of the model doing the work.
---

# Tier stamp

Decide which tier you belong to within your vendor's current model lineup:

- `flagship`: the most capable, most expensive model in the lineup.
- `mid`: the balanced model, between flagship and the smallest.
- `small`: the fastest, cheapest model in the lineup.

Be honest. Write a file named `TIER.txt` in the workspace root with exactly one
line: `tier: <flagship | mid | small>`.

Then apply the branch for your tier:

- `flagship`: create `deep.txt` containing a three-line haiku about depth.
- `mid`: create `mid.txt` containing a two-line rhyming couplet about balance.
- `small`: create `lite.txt` containing a single line about speed.

Finally append the line `tier-stamp` to `.skill-trace` in the workspace root
(create it if missing). Do not modify any other file. Do not commit.
