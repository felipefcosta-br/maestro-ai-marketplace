# maestro-ai-clear

Optional companion mod for the `maestro-ai` plugin. It makes "save the context and start clean" a single step:

1. A band above the prompt (after 15 turns) offers **Save context and clear**. The `clear_conversation` tool does the same when Claude calls it after the long-conversation warning.
2. It runs `/maestro-ai:save-context` and checks that the save finished (the `/maestro-ai:resume <name>` closing line).
3. It runs `/clear`, then `/maestro-ai:resume <name>`, so the work continues from the saved context with nothing to type.

Requires `maestro-ai` 0.5.0 or later. Without this mod everything still works: you type `/clear` and the start-of-session hook of `maestro-ai` resumes the saved context on your first message.

If the save is not confirmed, the conversation is not cleared. If `/clear` or the resume cannot run, a message tells you the command to type.
