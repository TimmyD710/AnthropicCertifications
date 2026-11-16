# Exercise: 1.3.7 Build a Context-Passing Pipeline (45 min)

**Concepts / exam domain:** Domain 1 - subagent invocation, brief as the only channel, structured findings with source metadata, parallel delegation, least-privilege subagent definitions
**Started:** 2026-11-16   **Status:** in progress

## Goal
A coordinator delegates to a search and an analysis subagent in parallel. Their JSON findings (with source_url / document_name / page_number) are passed into a synthesis subagent's brief. The report cites every claim; stripping the metadata from the brief makes the citations disappear, showing the failure is in context passing.

## Prerequisites
- [ ] `uv` installed, gateway environment variables set (as in 1.2)
- [ ] Log runs with `uv run python main.py 2>&1 | Tee-Object -FilePath run.log`

## Steps
- [ ] 1. Setup: main.py, `uv add anthropic`, one test call - done when it prints a reply
- [ ] 2. Fixed source data (two lists with text + metadata) - done when both print
- [ ] 3. Subagent definitions (description, prompt, tools) + run_subagent - done when one answers a hand-written brief
- [ ] 4. Coordinator with `delegate` tool, two calls in one response, run in parallel - done when the log shows both running together
- [ ] 5. Structured findings: JSON claims parsed, parse failure becomes ERROR - done when you get claims with metadata
- [ ] 6. Synthesis brief with complete findings; check every claim is cited - done when the check passes
- [ ] 7. Break it: strip metadata, rerun, compare - done when citations vanish and you can explain why
- [ ] 8. Wrap-up: 3 check questions, knowledge update

## Notes
- Interpretation: search and analysis are two independent sources (web-style snippets vs local document) so they can truly run in parallel; synthesis combines both.
- Built with the plain anthropic client and a `delegate` tool, not the Agent SDK. Agent tool gate, allowed_tools, AgentDefinition covered by check questions only.
- Planned ~50 min; shorten steps 5/6 first if running long.
