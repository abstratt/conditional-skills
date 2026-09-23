---
name: vendor-gated-guidance
description: Quality checklist for implementing a small feature in this project's Python code, written for models made by Anthropic. Use when an Anthropic model is asked to add, implement, or write a function or feature in src/. Models from any other vendor must not invoke this skill.
---

# Vendor-gated guidance

This skill is for models made by Anthropic only. First decide, honestly, which vendor made you.

- If you are **not** an Anthropic model: do not follow this skill. Append the line
  `vendor-gated-guidance: declined` to `.skill-trace` in the workspace root (create it if
  missing), then implement the request exactly as you would without this skill, and ignore the
  rest of this file.
- If you **are** an Anthropic model: follow the checklist below.

## Checklist

Implement the requested function in `src/app.py`. Give it a docstring, and create
`tests/test_app.py` with at least three test functions (names starting with `test_`) covering a
normal input, an edge case, and an invalid input. Tests use plain `assert` and import from
`src.app`. Run them if a test runner is available.

Finally append the line `vendor-gated-guidance` to `.skill-trace` in the workspace root
(create it if missing). Do not modify any other file. Do not commit.
