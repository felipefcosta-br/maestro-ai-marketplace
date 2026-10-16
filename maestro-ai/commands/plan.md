---
description: Turns a goal into a short plan with steps, risks and open questions, without executing it
argument-hint: <goal>
---
Make a plan for the goal below. Do not execute anything. Settle the working language first (section 0 of the `orchestration` skill).

Goal: $ARGUMENTS

Steps:

1. Use only the context you already have. Read at most the few files or documents that decide the plan; do not scan everything.
2. If a missing fact would change the plan, ask up to 3 short questions first. If a decision is big or costly to undo, set out the options with your recommendation and ask the user to choose.
3. Answer in this format, at most ~30 lines:

```
## Goal
<1-2 lines>
## Steps
1. <concrete step> — <result that shows it is done>
## Risks
- <risk> — <mitigation>
## Open questions
- <decision that depends on the user>
## Cheapest way to run it
<what can be done by a simpler/cheaper model or agent, what needs the strongest one>
```

4. Finish by asking whether to start with step 1, or to save the plan with `/maestro-ai:save-context`.
