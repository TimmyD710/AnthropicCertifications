# Exercise: Multi-agent orchestration (coordinator + 2 subagents)

**Concepts / exam domain:** coordinator/subagent pattern, explicit context passing, parallel delegation, iterative refinement, too-narrow task decomposition bug
**Started:** 2026-11-05   **Status:** complete (steps 11 and 12 skipped by choice; revisit before the exam)

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
- [x] 9. Parallel execution with threads: (a) refactor dispatcher + benchmark fixed delegations seq vs parallel, (b) wire into the loop - done: 4 delegations in one response run via ThreadPoolExecutor; benchmark noisy (1.06 vs 0.69 s, then 0.65 vs 2.75 s, probably rate-limit retries). TODO: per-round timing line in the real loop.
  - Note step 8: coordinator guessed wrong file names in round 1 (description named no exact files); the error message listing available files let it self-correct in round 2 (4 + 2 = 6 calls).
- [x] 10. (DONE: gaps filled via search after prompt told coordinator not to re-ask the same document; log showed a checker failure `max_tokens` treated as gaps -> add `ERROR:` marker + check, optional `is_error`) Iterative refinement: (a) DONE: check_coverage with closed checklist (needed tightening: first version invented a gap; 3 identical runs after fix), (b) DONE: refactor tool loop into run_tool_loop(messages, result) (per-round timing added; gateway timing noisy: 5.2 s for 4 parallel delegations once), (c) wire into run_agent (gaps -> new user message -> loop again, max 2 refinements) - done when: real gaps (defect detection, training costs) get filled by targeted re-delegation
- [~] 11. (SKIPPED by student choice, concept explained but not reproduced) Reproduce the bug - done when: report is incomplete though all subagents succeed
- [~] 12. (SKIPPED by student choice) Fix at the coordinator - done when: all areas covered without touching subagents
- [x] 13. Wrap-up - check questions + knowledge.md update

## Notes
- Working alias: `code` (gateway models are Qwen/Gemma/GPT-OSS-style, no Claude seen; real models unknown, ask admin).
- Gateway quirks met: embed/rerank aliases return 404/429; empty `response.content` possible (IndexError); set `$env:PYTHONUTF8 = "1"` to avoid print encoding crashes.
- Always check `response.content` is non-empty before `[0]`.
