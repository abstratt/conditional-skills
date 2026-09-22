---
name: tool-gated-review
description: Review this project's Python code for bugs and write the findings to REVIEW.md. Use whenever the user asks to review, audit, or check code in src/ for bugs, defects, or correctness problems.
---

# Tool-gated review

Check whether this session gives you a tool that delegates a task to a subagent (for example a
tool named Task, Agent, or spawn_agent). Decide from the tools you can actually call right now,
not from what your product supports in general.

- If you have such a tool: delegate the review of `src/app.py` to one subagent, wait for its
  result, and write `REVIEW.md` whose first line is `mode: delegated`.
- If you do not: review `src/app.py` yourself and write `REVIEW.md` whose first line is `mode: inline`.

After the first line, list every bug you found, one bullet per bug in the form
`- <function name>: <what is wrong>`.

Finally append the line `tool-gated-review` to `.skill-trace` in the workspace root (create it if
missing). Do not modify anything under `src/`. Do not commit.
