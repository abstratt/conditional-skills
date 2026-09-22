---
name: harness-stamp
description: Produce the harness capability stamp for this workspace. Use whenever the user asks to record, declare, or stamp what the agent's harness, runtime, or tooling can do.
---

# Harness stamp

Write a file named `HARNESS.txt` in the workspace root with exactly three lines.
Answer from your knowledge of the harness (the agent product) you are running in
right now, not from what a model could do in general.

```
hooks: <yes | no>              # can users configure hooks that run around tool calls?
subagents: <yes | no>          # can you spawn subagents / delegate to other agents?
image_generation: <yes | no>   # do you have a tool that generates images?
```

Then apply the branch that matches the `subagents` answer:

- If `subagents` is `yes`, also create an empty file named `delegates.txt`.
- If `subagents` is `no`, also create an empty file named `solo.txt`.

Finally append the line `harness-stamp` to `.skill-trace` in the workspace root
(create it if missing). Do not modify any other file. Do not commit.
