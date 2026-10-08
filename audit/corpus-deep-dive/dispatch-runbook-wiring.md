# DISPATCH BRIEF — Runbook wiring — 2026-10-08

Executor: ollama cloud `deepseek-v4.1-flash:cloud`, think:false. Read-only except where named. Gate at end. DoD: `../docs/plans/GUARDRAIL-RUNBOOK-DOD-2026-10-08.md`.

## Task

1. **Produce the operator contract** — read the full DoD below, distill into `/home/evo/sandbox/docs/plans/RUNBOOK.md` (≤120 lines, markdown). Sections: Boot order (the 7 rules in session order with each rule's enforcer + trigger) · Auditor law (executor never audits own work; kimi-k2.7-code:cloud pinned) · Acceptance test (2-week re-audit, targets from the report) · Scope fence wording · Root hygiene rules. No new content beyond the DoD and audit report — this is a distillation, not an invention.
2. **Wire the pointer** — append this exact block to each existing boot file (only the ones listed EXIST below; create nothing):

```markdown
## Runbook (default execution law)
Every execution session runs the seven guardrails: /home/evo/sandbox/docs/plans/RUNBOOK.md
Acceptance re-audit: /home/evo/sandbox/audit/corpus-deep-dive/out/report.md
```

Boot files to wire (verified existing):
- /home/evo/CLAUDE.md
- /home/evo/AGENTS.md
- /home/evo/evolution/engine/website/AGENTS.md
- /home/evo/studio/AGENTS.md
- /home/evo/sandbox/AGENTS.md
Do NOT touch any other file (incl. census, corpus, audit outputs).

## Gate (write to /home/evo/sandbox/audit/runbook-wiring/gate.json)

- RUNBOOK.md exists, ≤120 lines, contains all 7 rule names
- pointer greppable in all 5 wired files
- zero other files modified (git-less check: report new/changed files it touched)

## Source DoD (verbatim — the substance the model distills)

### The runbook (seven guardrails, one order)

1. **Boot:** quote last 2 lines of `CONTINUE.md`/`STATE.md` + blockers count on turn 1. *(enforcer: agent-mode intake)*
2. **Binary ruling** before any A/B/exploration; parked items go to a parking file, agent cannot re-ask. *(enforcer: /yes-no + parking-lot rule in agent-mode)*
3. **Budget:** 150 tool calls OR 2h per chunk → write state, flush, restart. Subagent cap 25 calls/child; failures write summaries, never partial work. *(enforcer: agent-mode policy 2/6)*
4. **Verification:** no "fixed" claim without file:line evidence pasted in-session. *(enforcer: verify-before-complete + coding-loop gate)*
5. **Auditor separation:** executor model NEVER audits own work; auditor = `kimi-k2.7-code:cloud` pinned; audit runs pre-execution (plan) and post (diff) where founder asks. *(enforcer: dispatch brief structure)*
6. **Scope fence:** new surface/tool/file asks mid-run → `Deferring to <parking file>. Continue current scope? (Y/N)` — no auto-expand. *(enforcer: agent-mode policy 1/4)*
7. **Root hygiene:** artifacts land in a named workspace, never `$HOME` root; backups are dated archives under `_archive/`. Gate: census re-run weekly (DEBRIS must stay 0). *(enforcer: census instrument + agent-mode close)*

### Acceptance test

Re-run the deep-dive scorer after 2 weeks. Pass = correction/redo/scope-drift/time-sink fall from 88–92% toward 59–61%; rework-loop (42%) and frustration (53%) hold or improve.