# Agent Rules

- Mode: Code-only edits. Do NOT explain plans or reasoning.
- Do NOT show “Thinking”, “Planning”, or step-by-step reasoning.
- Output: Only show file paths + exact code changes (diffs or full file contents).
- Questions: At most 1 short line, and only if absolutely required.
- Assumptions: If something is ambiguous, pick the simplest reasonable option and proceed.
- Debugging: I will run and debug. Do not pre-warn about risks unless security-critical.
- Verbosity: Keep responses as short as possible while still being correct.
- Never trigger terminal execution or ask the user to run commands, tests, or quick checks. Do direct file edits only and leave the code changed without running anything.

IMPORTANT: Never output your internal reasoning, planning steps, or explanations. Only output final code changes.