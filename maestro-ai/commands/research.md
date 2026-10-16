---
description: Researches a question with current sources and returns a short, checkable answer
argument-hint: <question or topic>
---
Research the question below. Settle the working language first (section 0 of the `orchestration` skill).

Question: $ARGUMENTS

Steps:

1. State in one line what you will find out and what is out of scope. If the question is ambiguous and a wrong guess would waste effort, ask one short question first.
2. Search current sources for anything that can change over time; do not answer from memory. In Claude Code, delegate broad searches to the `researcher` agent with a briefing; in chat, search yourself.
3. Cross-check important claims in at least two sources and say when sources disagree.
4. Answer in this format, at most ~25 lines:

```
## Answer
<2-5 lines, direct>
## Findings
- <finding> (source)
## Uncertainty
- <what is unconfirmed, outdated or disputed>
## Sources
- [Title](URL)
```

Never include secrets or confidential data in searches.
