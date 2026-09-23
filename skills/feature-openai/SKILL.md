---
name: feature-openai
description: Implement a small feature in this project's Python code, for models made by OpenAI. Use when an OpenAI model is asked to add, implement, or write a function or feature in src/. Models from any other vendor have their own skill and must not use this one.
---

# Feature (openai)

This skill is for models made by OpenAI. Implement the requested function in `src/app.py`. Give it a
docstring, and create `tests/test_app.py` with exactly one test function using plain `assert`,
importing from `src.app`.

Create an empty file named `picked-feature-openai.txt` in the workspace root.

Finally append the line `feature-openai` to `.skill-trace` in the workspace root (create it if
missing). Do not modify any other file. Do not commit.
