# Output modes

## `summary` (default for execution)
At most 15 lines:
1. What was done or concluded
2. Files touched (paths)
3. Test results (passed/failed, counts)
4. Risks or pending items

## `didactic` (default for analysis, and when the user wants to understand)
Step-by-step explanation:
1. Context: what is being analyzed and why
2. Reasoning in short steps, with small examples
3. Evidence (file:line), separating facts from hypotheses
4. Conclusion and suggested next steps

## Common rules
- Do not paste large code excerpts: point to path and lines.
- No secrets in the answer, even if they appear in logs.
- Say clearly what was not verified.
