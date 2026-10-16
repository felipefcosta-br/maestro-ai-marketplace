---
name: orchestration
description: Subagent orchestration rules (maestro-ai). Use when planning any development task that can be delegated to researcher, analyst, implementer, tester, specialist, architect or reviewer; when writing briefings; when deciding model escalation or review.
---

# Agent orchestration

The main session is the orchestrator: it understands the task, splits it into steps, writes each agent's briefing and integrates the results. Every agent starts with no context, so the quality of the briefing decides the quality of the result.

> Subagents and hooks exist only in Claude Code and Cowork. In chat, do the same steps yourself: keep the briefing discipline (goal, minimal context, definition of done), ask before big decisions and review your own result before delivering.

## 0. Language

Decide the working language before anything else:

1. If a language is already recorded (a `Language:` line in `AGENTS.md`, or in `.maestro-ai/context.md`), use it.
2. Otherwise, if the user is writing in English, use English and do not ask.
3. Otherwise (the user writes in another language and nothing is recorded), ask once, before starting the work: which language they want for replies, briefings, agent reports and saved context. Offer their current language as the recommended option. Do not ask again in the same project; suggest recording the answer as a `Language:` line in `AGENTS.md` (and `save-context` records it in `context.md`).

Use the chosen language for every reply to the user, every briefing and the saved context. Keep code, identifiers, commands and commit messages in the language the project already uses. If the user later switches language on their own, follow them without asking again.

## 1. Delegate or do it directly

**Do it directly:** simple questions, small tasks (1-2 files), anything where the context is already in the conversation.

**Delegate when:**
- the search is broad or produces a lot of intermediate noise (logs, long documentation);
- more than 3 files are involved;
- tasks are independent and can run in parallel.

Rule of thumb: delegate when the path is long and the result is short. If the briefing would be longer than the task, do it directly. These rules should evolve with usage data.

## 2. Who does what

| Situation | Agent | Model |
|---|---|---|
| Map code, research docs/APIs | `researcher` | haiku |
| Understand code, a log or data (explanation) | `analyst` | sonnet |
| Small, well-specified change | `implementer` | sonnet |
| Write/run tests | `tester` | sonnet |
| Subtle bug, risky refactor, repeated failure | `specialist` | opus |
| Architecture decision, hardest problems | `architect` | opus (fable if the user approves) |
| Review a diff | `reviewer` | sonnet |

## 3. Briefing

Every briefing follows `templates/briefing.md`: goal, minimal context, files/areas, constraints, definition of done and output mode. Include only what is needed and never put secrets, credentials or customer data in it. Write the briefing in the working language (section 0); agents answer in the language of the briefing.

Output modes (`templates/output.md`): `summary` (short, up to 15 lines) or `didactic` (step-by-step explanation). Always ask for a format; agents that return long texts cancel the savings.

## 4. Escalation

- An agent failed twice: **ask the user** whether to move up to the `specialist`.
- The `specialist` did not solve it: **ask the user** whether to call the `architect`.
- Do not move up to a stronger model on your own without asking.

## 5. Architect: mandatory question, with a recommendation

Before ANY call to the `architect`, ask the user (AskUserQuestion) whether they want **Fable** (more expensive) or **Opus**. Never call it without asking and never assume the answer; if there is no answer, wait.

The question carries your recommendation: the recommended option comes first, marked "(Recommended)", plus one line with the reason.

- Recommend **Fable** when: an architecture decision has high impact or is hard to reverse; the `specialist` already tried and did not solve it; many interdependent parts; high risk (security, data, concurrency).
- Recommend **Opus** when: a complex but bounded problem; a plan that touches few files; the expected gain from Fable does not justify the cost.
- Example reason: "I recommend Fable: the decision affects 4 modules and the specialist already failed once; the extra cost is worth the risk of rework."

If the user chooses Fable, call the agent with `model: "fable"`. If they choose Opus, call it without overriding the model (the agent already uses Opus). A hook asks for an extra confirmation whenever a call uses Fable; if the user denies it there, redo the call with Opus.

## 6. Review

Use the `reviewer` for complex problems and for all non-trivial implemented code. Pass the original goal and how to get the diff. Complex changes may call for the `reviewer` on Opus (override the model in the call, after informing the user).

## 7. Parallelism and conflicts

- Research and analysis (read-only) can run in parallel.
- Agents that edit files run in series, or in separate worktrees.
- Subagents do not create subagents: only the main session delegates.

## 8. Security

- Only the `researcher` can use the web. Agents that write files do not use the network or install packages.
- No secrets in briefings, AGENTS.md or logs. Do not read `.env`, keys or credentials.
- Ask for confirmation before installing packages, using the network, `git commit` and `git push`.
- When an agent returns, check that it met the definition of done before calling the task finished.

## 9. Fixed workflows

For repeatable sequences use the plugin commands:
- `/maestro-ai:implement-test-review <task>`
- `/maestro-ai:pre-commit-review`

## 10. Long conversations and continuity

Every reply resends the history, so long conversations get expensive and lose focus. When the conversation is long (the hook warns once), or when a big step is done:
- Suggest `/maestro-ai:save-context` to the user. It writes the state to `.maestro-ai/context.md` (goal, decisions, next steps, key files, pitfalls).
- Then continue in a clean session with `/maestro-ai:resume`, which reads only that file, checks the repository state and picks up from the next step.
- The context file never contains secrets; `.maestro-ai/` should stay out of Git unless the user decides otherwise.
- This complements the built-in `/compact`: the file is curated, persists across sessions, can be edited by you and works as a briefing for agents.
