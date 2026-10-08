# CORPUS-DEEP-DIVE — DoD — 2026-10-08

**Done (one sentence):** A dispatch-run deep audit of the last 60 days of the chat corpus (2026-08-08 → 2026-10-08) delivers pinned antipattern findings + an explicit read on the Hermes-orchestration decay (2026-09-08 → 2026-09-28), with recommendations that either validate or kill the Orca + Ruflo mix.

## Criteria (all must be true)

1. `sandbox/audit/corpus-deep-dive/out/manifest60.json` — machine manifest of the 60-day window per source, no LLM needed.
2. `out/findings.json` — ≥40 sessions scored with the antipattern rubric (correction / redo / scope-drift / rework-loop / frustration / time-sink / other), each signal carrying a verbatim quote.
3. Every quote pin resolves: cited file path exists in `manifest60.json` (script-checked).
4. `out/report.md` — synthesis structured as:
   - Antipattern frequency, 60-day window vs the 04-model 120-file sample (delta table).
   - **Hermes decay narrative:** what degraded across 09-08 → 09-28 with 8–15 pinned verbatim sessions.
   - Execution-layer cost map: where the rework-loop/time-sink/correction clusters actually come from (job type × session shape).
   - Orca/Ruflo validation verdict: which of the 9 rules a worksurface+orchestrator pair can mechanically enforce, which it cannot.
5. Citation spot-check: I open 3 cited files; pins match quotes.

## Out of scope

- No session files are modified. Read-only over the corpus.
- No Orca/Ruflo code written; no install decisions executed — the verdict feeds the install gate, it does not perform it.
- Grok representativeness question stays open (thin sample, per 04-model §4).

## Budget

- ≤75 scoring runs on **local Ollama** `qwen2.5-coder:14b-32k` (founder-amended 2026-10-08: OpenRouter key out of budget; local model replaces it). Turn-aligned chunks of ≤20k chars per run. Concurrency 2 (GPU queues).
- Wall target 60 min (local-token gen). 2× stop → kill the run, report partial.
- Failure ≠ retry-forever: 2 consecutive call failures on one batch → mark batch UNSCORED, continue.