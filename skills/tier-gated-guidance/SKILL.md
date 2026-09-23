---
name: tier-gated-guidance
description: Quality checklist for implementing a small feature in this project's Python code, written for small-tier models, the fastest and cheapest model in its vendor's lineup. Use when such a model is asked to add, implement, or write a function or feature in src/. Mid-tier and flagship models must not invoke this skill; they do not need it.
---

# Tier-gated guidance

This skill is for small-tier models only. First decide, honestly, which tier you belong to
within your vendor's current model lineup:

- `flagship`: the most capable, most expensive model in the lineup.
- `mid`: the balanced model, between flagship and the smallest.
- `small`: the fastest, cheapest model in the lineup.

Then:

- If you are **not** a small-tier model: do not follow this skill. Append the line
  `tier-gated-guidance: declined` to `.skill-trace` in the workspace root (create it if
  missing), then implement the request exactly as you would without this skill, and ignore the
  rest of this file.
- If you **are** a small-tier model: follow the checklist below.

## Checklist

Implement the requested function in `src/app.py`. Give it a docstring, and create
`tests/test_app.py` with at least three test functions (names starting with `test_`) covering a
normal input, an edge case, and an invalid input. Tests use plain `assert` and import from
`src.app`. Run them if a test runner is available.

Finally append the line `tier-gated-guidance` to `.skill-trace` in the workspace root
(create it if missing). Do not modify any other file. Do not commit.
