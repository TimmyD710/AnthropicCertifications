# Exercise: Multi-agent orchestration (coordinator + 2 subagents)

**Concepts / exam domain:** coordinator/subagent pattern, explicit context passing, parallel delegation, iterative refinement, too-narrow task decomposition bug
**Started:** 2026-11-05   **Status:** in progress

## Goal
Build a coordinator that delegates to a web-search subagent (fake canned search function) and a document-analysis subagent (local .txt files), runs them in parallel, refines for coverage gaps, then reproduce and fix the narrow-decomposition bug at the coordinator.

## Prerequisites
- [x] `anthropic` installed in this folder's uv project (`uv add anthropic`)
- [x] API key + base URL set as environment variables in the terminal (never in chat or files)
- [x] Output logged with `| Tee-Object -FilePath run.log`

## Steps
- [x] 1. Setup check - done when: tiny test call reply appears in run.log
- [ ] 2. One subagent with explicit brief - done when: it answers using only facts in the brief
- [x] 3. Prove no inherited context - done when: subagent doesn't know an unshared fact, then does once it is in the brief
- [x] 4. Build the two subagents (fake search + document), test each alone - done when: each answers from its own source
- [x] 5. Run both sequentially from plain code, synthesise, time it - done when: combined report + measured time (baseline: ~0.45 s search, ~0.14 s doc, ~0.12 s synthesis, total ~0.71 s; runs are noisy)
- [ ] 6. Coordinator with `delegate` tool emits delegations (inspect only, no execution) - done when: log shows tool_use blocks per response
- [ ] 7. Execute delegations + agentic loop, sequential, timed - done when: coordinator writes final report
- [ ] 8. Parallel execution with threads, timed over several runs - done when: clearly faster than step 7
- [ ] 9. Iterative refinement - done when: planted gap (costs doc) gets filled by targeted re-delegation
- [ ] 10. Reproduce the bug - done when: report is incomplete though all subagents succeed
- [ ] 11. Fix at the coordinator - done when: all areas covered without touching subagents
- [ ] 12. Wrap-up - check questions + knowledge.md update

## Notes
- Working alias: `code` (gateway models are Qwen/Gemma/GPT-OSS-style, no Claude seen; real models unknown, ask admin).
- Gateway quirks met: embed/rerank aliases return 404/429; empty `response.content` possible (IndexError); set `$env:PYTHONUTF8 = "1"` to avoid print encoding crashes.
- Always check `response.content` is non-empty before `[0]`.
