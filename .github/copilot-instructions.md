# Copilot Instructions — AgroEye

## Project Overview
This repo is a capstone project of acting as a pipeline for crop disease monitoring and detection which acts as a pipeline for capturing images from the drone and store it in the streams folder and then show it in the frontend interface along with the type of crop disease present

## Agent Rules
- Mode: code edits only.
- Keep edits minimal and scoped to the actual issue.
- Preserve the existing code patterns and naming used by the repo.
- Do not add speculative architecture or unrelated template features.
- Do not output internal reasoning, step-by-step plans, or commentary about how you think.
- Prefer direct code changes that fit the existing project structure.
- Be consistent with the current backend/frontend conventions already present in the repo.
- No explanations, no planning, no reasoning steps.
- Output only: file paths + exact code changes (diff or full file).
- Keep responses ultra-short and token-efficient: prefer direct patches over long descriptions.
- Do not ask the user to run commands, open terminals, or perform local verification unless strictly required by the task.
- Never trigger terminal execution, code-running requests, or quick checks; do direct edits only and leave the repo changed without running commands.
- Do not ask for clarification unless absolutely necessary; if ambiguous, choose the simplest consistent repo-native implementation.
- Do not ask broad follow-up questions; minimize back-and-forth and avoid unnecessary conversational overhead.
- At most one short clarifying question if strictly needed.
- I will run and debug.
- IMPORTANT: Never output your internal reasoning, planning steps, or explanations. Only output final code changes.
- IMPORTANT: Save tokens aggressively; avoid repeating context, avoid long summaries, avoid explanations, and keep every response focused on the code change itself.