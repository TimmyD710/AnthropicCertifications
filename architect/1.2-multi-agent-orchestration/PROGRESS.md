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
- [x] 6. Coordinator with `delegate` tool emits delegations (inspect only, no execution) - done: 4 delegate calls in ONE response
- [x] 7. Execute delegations + agentic loop, sequential - done: final report written (15 delegations over 3 rounds, all to `search`)
- [x] 8. Tell the coordinator which documents exist (it never used the document agent) - done when: both agent types used, report contains pilot and cost facts
- [ ] 9. Parallel execution with threads: (a) refactor dispatcher + benchmark fixed delegations seq vs parallel x3, (b) wire into the loop - done when: clearly faster than sequential
  - Note step 8: coordinator guessed wrong file names in round 1 (description named no exact files); the error message listing available files let it self-correct in round 2 (4 + 2 = 6 calls).
- [ ] 10. Iterative refinement - done when: planted gap (a topic in neither source) gets filled by targeted re-delegation
- [ ] 11. Reproduce the bug - done when: report is incomplete though all subagents succeed
- [ ] 12. Fix at the coordinator - done when: all areas covered without touching subagents
- [ ] 13. Wrap-up - check questions + knowledge.md update

## Notes
- Working alias: `code` (gateway models are Qwen/Gemma/GPT-OSS-style, no Claude seen; real models unknown, ask admin).
- Gateway quirks met: embed/rerank aliases return 404/429; empty `response.content` possible (IndexError); set `$env:PYTHONUTF8 = "1"` to avoid print encoding crashes.
- Always check `response.content` is non-empty before `[0]`.
