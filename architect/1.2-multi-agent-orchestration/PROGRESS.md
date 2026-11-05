# Exercise: Multi-agent orchestration (coordinator + 2 subagents)

**Concepts / exam domain:** coordinator/subagent pattern, explicit context passing, parallel delegation, iterative refinement, too-narrow task decomposition bug
**Started:** 2026-11-05   **Status:** in progress

## Goal
Build a coordinator that delegates to a web-search subagent (fake canned search function) and a document-analysis subagent (local .txt files), runs them in parallel, refines for coverage gaps, then reproduce and fix the narrow-decomposition bug at the coordinator.

## Prerequisites
- [ ] `anthropic` installed in this folder's uv project (`uv add anthropic`)
- [ ] API key + base URL set as environment variables in the terminal (never in chat or files)
- [ ] Output logged with `| Tee-Object -FilePath run.log`

## Steps
- [ ] 1. Setup check - done when: tiny test call reply appears in run.log
- [ ] 2. One subagent with explicit brief - done when: it answers using only facts in the brief
- [ ] 3. Prove no inherited context - done when: subagent doesn't know an unshared fact, then does once it is in the brief
- [ ] 4. Two subagents, sequential - done when: combined report + measured time
- [ ] 5. Parallel delegation - done when: two tool calls in one response, time clearly lower
- [ ] 6. Iterative refinement - done when: planted gap gets filled by targeted re-delegation
- [ ] 7. Reproduce the bug - done when: report is incomplete though all subagents succeed
- [ ] 8. Fix at the coordinator - done when: all areas covered without touching subagents
- [ ] 9. Wrap-up - check questions + knowledge.md update

## Notes
