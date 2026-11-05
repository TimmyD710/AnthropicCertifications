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
- [ ] 4. Build the two subagents (fake search + document), test each alone - done when: each answers from its own source
- [ ] 5. Run both sequentially from plain code, synthesise, time it - done when: combined report + measured time
- [ ] 6. Coordinator with delegate tool, parallel delegation - done when: two tool calls in one response, time clearly lower
- [ ] 7. Iterative refinement - done when: planted gap gets filled by targeted re-delegation
- [ ] 8. Reproduce the bug - done when: report is incomplete though all subagents succeed
- [ ] 9. Fix at the coordinator - done when: all areas covered without touching subagents
- [ ] 10. Wrap-up - check questions + knowledge.md update

## Notes
- Working alias: `code` (gateway models are Qwen/Gemma/GPT-OSS-style, no Claude seen; real models unknown, ask admin).
- Gateway quirks met: embed/rerank aliases return 404/429; empty `response.content` possible (IndexError); set `$env:PYTHONUTF8 = "1"` to avoid print encoding crashes.
- Always check `response.content` is non-empty before `[0]`.
