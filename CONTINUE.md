# CONTINUE — sandbox (estate work: worksurface test / runbook / census)

## Next action
Continue quick-fire review of `audit/design/STEP1-LANDING-PAGE.md` — Question 2 (elevation model). Then complete questions 3–8, then resolve gaps across all three steps before drafting `DESIGN.md`.

## State
- 2026-10-15 — Design audit begun: three-step empirical harvest of live surfaces (`/`, `/marketplace`, `/mystable`). Reference docs copied from `audit/website/` into `audit/design/`. Full source read: all landing page sections, marketplace components, MyStable dashboard, brand token source (`tokens.ts` + `theme.generated.css`). Findings written to `audit/design/STEP1-LANDING-PAGE.md`, `STEP2-MARKETPLACE.md`, `STEP3-MYSTABLE.md`. Quick-fire review in progress (8 questions posed, 1 answered).
- 2026-10-14 — Refund rule written once, in the Refund section of `/home/evo/sandbox/v2/OUTCOME.md` and `evolution/engine_v2/OUTCOME.md` (copies match). `PLAN.md` and `OPERATIONS.md` point at it. No day count. A rule stays in the spec; the plan and the guide do not restate it. Execution protocol was discussed and not locked.
- 2026-10-13 — V2 working plan is `/home/evo/sandbox/v2/README.md` and `/home/evo/sandbox/v2/PLAN.md`. The brief stays in `evolution/engine_v2/` (`OUTCOME.md`, `CONTINUE.md`, `DoD.md`). Code, after the word build, is `evolution/engine_v2/website`. Do not `git init` the parent. Live website `AGENTS.md` and the branch-law hook stay.
- 2026-10-13 — Orca removed. The Windows app, the `sandbox/audit/orca` checkout, hooks, and the `orca-cli` skill are gone. Do not reinstall.
- 2026-10-08 — 60-day corpus deep-dive complete: 73/73 sessions scored. Fix: six-guardrail bundle + auditor separation. Acceptance test still scheduled ~2026-10-22.
- 2026-10-08 — RUNBOOK live: wired into 5 boot files. Gate all green.
- 2026-10-08 — Skill library cut 192 → 50; census hygiene pass; dot-dir hygiene.

## Ledger
| date | what | repo | commit | state |
|---|---|---|---|---|
| 2026-10-15 | Design audit: 3-step harvest complete; Q1 answered (tagline style); 7 questions remain | sandbox | no commit | in progress |
| 2026-10-14 | 14-day refund line removed; Refund section is the only copy | sandbox + engine_v2 | no commit | done |
| 2026-10-13 | v2 plan, OPERATIONS.md, and engine-v2 remote locked | sandbox | no commit | done |
| 2026-10-13 | v2 plan placed in sandbox/v2; Orca removed; live-site lock kept | sandbox | this commit | done |
| 2026-10-08 | corpus deep-dive audit + AMEND verdict | sandbox | (this repo) | done |
| 2026-10-08 | RUNBOOK distilled + wired into 5 boot files | sandbox | (this repo) | done |
| 2026-10-08 | skills archive 192→50; census moves (44+10) | (home root) | n/a | done |
| 2026-10-08 | sandbox/rebuild git-inited + snapshot 89d3271 | rebuild | 89d3271 | done |

## Blocked
- V2 first commit waits for the founder to say build. The remote `Badders80/engine-v2` already exists, private and empty. Image upload still waits on a Cloudflare token.
- OpenRouter paid lane — key budget exceeded (founder top-up only if needed; free lane works).
- gemma-4-31b:free — persistent 429; alternatives: local qwen3.8:27b-27b-64k or founder adds Google AI Studio key.
- Design review: 7 of 8 quick-fire questions still open (elevation, motion tokens, CollapsePanel, 64px heading, label roles, gold viewport cap, system sans stack).
- `audit/design/DESIGN.md` not yet drafted — waiting on Q1–Q8 resolution.
- 2-week re-audit — waits on runbook usage (~2026-10-22).