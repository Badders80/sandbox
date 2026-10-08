# GUARDRAIL-RUNBOOK — DoD — 2026-10-08

**Done (one sentence):** One default runbook (~60 lines max) that fires the six guardrails mechanically in every execution session, with auditor separation enforced by model identity, tested against the 60-day baseline.

## The runbook (six guardrails, one order)

1. **Boot:** quote last 2 lines of `CONTINUE.md`/`STATE.md` + blockers count on turn 1. *(enforcer: agent-mode intake)*
2. **Binary ruling** before any A/B/exploration; parked items go to a parking file, agent cannot re-ask. *(enforcer: /yes-no + parking-lot rule in agent-mode)*
3. **Budget:** 150 tool calls OR 2h per chunk → write state, flush, restart. Subagent cap 25 calls/child; failures write summaries, never partial work. *(enforcer: agent-mode policy 2/6)*
4. **Verification:** no "fixed" claim without file:line evidence pasted in-session. *(enforcer: verify-before-complete + coding-loop gate)*
5. **Auditor separation:** executor model NEVER audits own work; auditor = `kimi-k2.7-code:cloud` pinned; audit runs pre-execution (plan) and post (diff) where founder asks. *(enforcer: dispatch brief structure)*
6. **Scope fence:** new surface/tool/file asks mid-run → `Deferring to <parking file>. Continue current scope? (Y/N)` — no auto-expand. *(enforcer: agent-mode policy 1/4)*
7. **Root hygiene:** artifacts land in a named workspace, never `$HOME` root. Screenshots/scratch/one-off scripts die at end of run or move to `work/`; backups are dated archives under `_archive/`. Gate: `/home/evo/audit/census/` census re-run weekly — the instrument-first finder (DEBRIS must stay 0). *(enforcer: census instrument + agent-mode close)*

## Acceptance test (from the 60-day audit, `audit/corpus-deep-dive/out/report.md` §2)

Re-run the deep-dive scorer after 2 weeks of runbook use. Pass = correction/redo/scope-drift/time-sink fall from 88–92% toward the 59–61% baseline; rework-loop (42%) and frustration (53%) hold or improve.

## Out of scope

- No Orca reconfiguration in this job (Orca is the container, already validated).
- No new skills installed — the runbook is rules over the kept 50, not additions.
- Ruflo not installed; only if the runbook leaves an un-enforceable gap.

## Budget

- Half a session to write + wire (this file + a pointer in each active island's AGENTS.md/CONTINUE.md).
- No model runs required beyond the 2-week re-audit.