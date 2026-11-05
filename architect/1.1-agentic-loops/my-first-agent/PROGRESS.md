# Exercise: Minimal multi-tool agent

**Concepts / exam domain:** agentic loops, tool definitions, stop_reason handling, conversation history, iteration safety net
**Started:** 2026-11-03   **Status:** complete (2026-11-04)

## Goal
Build an agent with two tools (calculator, web-search stub). It calls messages.create() in a loop, branches on stop_reason (tool_use -> run tool and append assistant message + tool result; end_turn -> return final answer), with MAX_ITERATIONS = 20 as a safety net only.

## Prerequisites
- [x] Anthropic API key set as an environment variable (never in code or chat)
- [x] `anthropic` package installed via `uv add anthropic`
- [ ] Current model name checked in the docs

## Steps
- [x] 1. Set up - done when: `uv run python -c "import anthropic"` runs without error
- [x] 2. First plain API call - done when: a text answer prints in the terminal
- [x] 3. Define the two tools - done when: list of two tool dicts exists and file still runs
- [x] 4. Write tool functions + dispatcher - done when: direct calls return a calculation and fake search text
- [x] 5. Pass tools to Claude, inspect stop_reason - done when: stop_reason == "tool_use" and a tool_use block is printed
- [x] 6. Build the loop - done when: a question needing both tools gets a final answer
- [x] 7. Add MAX_ITERATIONS = 20 - done when: you can explain it and a tiny value (1) triggers the guard
- [x] 8. Test and wrap-up - done when: 3 different questions run and check questions are answered

## Notes
- Gateway: model names are aliases (company gateway, ANTHROPIC_BASE_URL). `model="code"` works; list names via `client.models.list()`.
- Step 2: needed a hint to also print stop_reason.
- Step 3: first wrote "required" as a string instead of a list (fixed). Remember to save (Ctrl+S) before running.
- Step 6: needed hints for "type:" typo, dict["key"] vs object.attr, return inside the while loop, one user message for all tool results. Tool named "web_search" was ignored by the gateway/model; renamed to "search_stub" and it worked (likely a reserved name; unconfirmed). A stub that always says "no results" made Claude retry 3 rounds.
- Step 8: 3 test runs matched. Gateway alias `code` self-reported as Qwen (not Claude); ask admin. Check Q1 (why one message for all tool_results) only partly right; Q2 and Q3 correct.
- Step 7: used `&&` instead of `and`; first version checked the counter after the loop (off by one) instead of stop_reason. Fixed. Cap tested with 1 and 20.
