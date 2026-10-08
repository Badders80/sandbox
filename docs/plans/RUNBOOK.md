# RUNBOOK — seven guardrails (default execution law)

## Boot order
Seven rules enforced in strict session order:

1. **Boot**
   - Trigger: Turn 1 of any execution session.
   - Enforcer: agent-mode intake.
   - Action: Quote last 2 lines of `CONTINUE.md`/`STATE.md` + blockers count.

2. **Binary ruling**
   - Trigger: Before any A/B test or exploration.
   - Enforcer: /yes-no + parking-lot rule in agent-mode.
   - Action: Issue binary ruling; parked items go to parking file (agent cannot re-ask).

3. **Budget**
   - Trigger: 150 tool calls OR 2h per chunk.
   - Enforcer: agent-mode policy 2/6.
   - Action: Write state, flush, restart. Subagent cap 25 calls/child; failures write summaries, never partial work.

4. **Verification**
   - Trigger: Before claiming "fixed".
   - Enforcer: verify-before-complete + coding-loop gate.
   - Action: Paste `file:line` evidence in-session. No claim without evidence.

5. **Auditor separation**
   - Trigger: Pre-execution (plan) and post (diff) where founder asks.
   - Enforcer: dispatch brief structure.
   - Action: Executor never audits own work. Auditor is `kimi-k2.7-code:cloud` (pinned).

6. **Scope fence**
   - Trigger: New surface/tool/file request mid-run.
   - Enforcer: agent-mode policy 1/4.
   - Action: Prompt: `Deferring to <parking file>. Continue current scope? (Y/N)`. No auto-expand.

7. **Root hygiene**
   - Trigger: Session end / weekly gate.
   - Enforcer: census instrument + agent-mode close.
   - Action: Artifacts land in named workspace (never `$HOME` root). Backups are dated archives under `_archive/`. Census re-run weekly; DEBRIS must stay 0.

## Auditor law
- Executor model NEVER audits own work.
- Auditor identity is pinned: `kimi-k2.7-code:cloud`.
- Audit runs are pre-execution (plan) and post-execution (diff), triggered only when founder asks.

## Acceptance test
- Re-run deep-dive scorer after 2 weeks of runbook use.
- **Pass criteria:**
  - Correction/redo/scope-drift/time-sink fall from 88–92% toward 59–61% baseline.
  - Rework-loop (42%) and frustration (53%) hold or improve.

## Scope fence wording
- **Trigger:** Any mid-run request for new surface, tool, or file.
- **Response:** `Deferring to <parking file>. Continue current scope? (Y/N)`
- **Constraint:** No auto-expand. Agent must wait for explicit user confirmation.

## Root hygiene
- **Placement:** Artifacts land in a named workspace, never `$HOME` root.
- **Lifecycle:** Screenshots/scratch/one-off scripts die at end of run or move to `work/`.
- **Backups:** Dated archives under `_archive/`.
- **Gate:** Census re-run weekly at `/home/evo/audit/census/`. Instrument-first finder (DEBRIS must stay 0).