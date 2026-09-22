---
name: tiered-feature
description: Implement a small feature in this project's Python code with the level of rigour that matches the model doing the work. Use whenever the user asks to add, implement, or write a function or feature in src/.
---

# Tiered feature

First decide, honestly, which tier you belong to within your vendor's current model lineup:

- `flagship`: the most capable, most expensive model in the lineup.
- `mid`: the balanced model, between flagship and the smallest.
- `small`: the fastest, cheapest model in the lineup.

Write a file `TIER.txt` in the workspace root with exactly one line: `tier: <flagship | mid | small>`.

Then implement the requested function in `src/app.py` and apply the branch for your tier:

- `flagship`: give the function a docstring, and create `tests/test_app.py` with at least three
  test functions (names starting with `test_`) covering a normal input, an edge case, and an
  invalid input. Tests use plain `assert` and import from `src.app`. Run them if a test runner
  is available.
- `mid`: give the function a docstring, and create `tests/test_app.py` with exactly one test
  function using plain `assert`, importing from `src.app`.
- `small`: no docstring, no tests. Put the comment line `# TODO(review): needs validation and tests`
  on the line directly above the function definition.

Finally append the line `tiered-feature` to `.skill-trace` in the workspace root (create it if
missing). Do not modify any other file. Do not commit.
