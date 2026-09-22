---
name: vendor-stamp
description: Produce the agent identity stamp for this workspace. Use whenever the user asks to stamp, sign, identify, or record which AI agent, model, or assistant is working on the project.
---

# Vendor stamp

Write a file named `AGENT.txt` in the workspace root with exactly three lines,
filled in from what you know about yourself. Do not run commands to find out;
answer from your own knowledge of who you are.

```
vendor: <anthropic | openai | google | other>
model: <the model name you are, as precisely as you know it>
harness: <claude-code | codex | gemini-cli | other>
```

Then apply the branch that matches your vendor:

- If vendor is `anthropic`, also create an empty file named `stamp-a.txt`.
- If vendor is `openai`, also create an empty file named `stamp-o.txt`.
- Otherwise, also create an empty file named `stamp-x.txt`.

Finally append the line `vendor-stamp` to `.skill-trace` in the workspace root
(create it if missing). Do not modify any other file. Do not commit.
