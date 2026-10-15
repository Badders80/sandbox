# CONTINUE — sandbox

Scoped to this git root (`Badders80/sandbox`). Work in another repo belongs to that repo's `CONTINUE.md`. The folder map is `docs/plans/SANDBOX-MAP.md`, which `/wrap` does not write.

## Next action
Open `audit/design/STEP1-LANDING-PAGE.md` and answer Question 2 (elevation model), then Q3–Q8, before drafting `DESIGN.md`.

## State
- 2026-10-15 — Pruned to wrap's four slots and scoped to this root. The folder map moved out to `docs/plans/SANDBOX-MAP.md`.
- 2026-10-15 — `docs/plans/VERIFICATION-TIERS.md` filed. `v2/PLAN.md` §5 and §8.5 now codify the pre-numbered diff audit, with a pointer to that file.
- 2026-10-15 — Design audit harvest complete across all three surfaces (`/`, `/marketplace`, `/mystable`). Q1 answered (tagline style); 7 open. `audit/design/` is untracked.
- 2026-10-13 — V2 working plan is `v2/README.md` and `v2/PLAN.md`. The brief stays in `evolution/engine_v2/` (`OUTCOME.md`, `CONTINUE.md`, `DoD.md`). Do not `git init` the parent.
- 2026-10-13 — Orca removed. Do not reinstall.
- 2026-10-08 — `docs/plans/RUNBOOK.md` live, wired into boot by `/home/evo/sandbox/AGENTS.md`.
- 2026-10-08 — Corpus deep-dive complete, 73/73 sessions scored. Acceptance re-audit ~2026-10-22.

Closed or out-of-scope, dropped 2026-10-15 so they are not re-added: the gemma-4-31b 429 row, the R2/Cloudflare token row (all five `R2_*` keys are set in `engine/.env.local`), the first-commit gate (steps 1–5 are pushed), and the 2026-10-14 refund row (that rule lives in `OUTCOME.md`).

## Ledger
| date | what | repo | commit | state |
|---|---|---|---|---|
| 2026-10-15 | Verification tiers filed; pre-numbered diff audit codified in PLAN.md §5/§8.5 | sandbox | ae34ac9 | done |
| 2026-10-15 | Wrap | sandbox | 5e6d0c8 | done |
| 2026-10-15 | Three verification gaps parked in `v2/PLAN.md` §Parked | sandbox | ef071f4 | done |
| 2026-10-15 | Design audit: harvest complete, Q1 answered, 7 open | sandbox | no commit | in progress |

## Blocked
- Design review: 7 of 8 quick-fire questions open — elevation, motion tokens, CollapsePanel, 64px heading, label roles, gold viewport cap, system sans stack.
- `audit/design/DESIGN.md` not drafted. Waits on Q1–Q8.
- `audit/design/` untracked, so none of it is in git history yet.
- 2-week re-audit — waits on runbook usage (~2026-10-22).
