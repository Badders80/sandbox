# CONTINUE — sandbox (estate work: worksurface test / runbook / census)

## Next action
Open `v2/PLAN.md`. Parent-file slim is agreed and not done (`/home/evo/CLAUDE.md`, `/home/evo/AGENTS.md`, `evolution/CLAUDE.md`). Leave the live website lock in place.

## State
- 2026-10-08 — 60-day corpus deep-dive complete: 73/73 sessions scored (ollama cloud deepseek-v4.1-flash + think:false), report + AMEND verdict at `audit/corpus-deep-dive/out/report.md`. The fix recorded that day was the six-guardrail bundle plus auditor separation. Orca was removed on 2026-10-13.
- 2026-10-08 — RUNBOOK live: `docs/plans/RUNBOOK.md` (61 lines, distilled by local qwen3.8:27b-64k) + pointer wired into 5 boot files (CLAUDE.md, AGENTS.md, website, studio, sandbox). Gate: `audit/runbook-wiring/gate.json` all green.
- 2026-10-08 — Skill library cut 192 → 50 (house method + superpowers + basics); 133 items archived at `~/.agents/skills-archive-2026-10-08/` (restore = mv).
- 2026-10-08 — Census hygiene pass: 63 rulings done (44 DEBRIS + 10 ARCHIVE + 9 CANDIDATE-split → staging). 42 `toss` entries moved to `audit/census/staging-2026-10-08/` (~110 GB). Re-census confirms CANDIDATE bucket = 15 entries, all = our `keep` rulings.
- 2026-10-08 — Dot-dir hygiene (bonus): 138 → 69 dirs in `/home/evo`. 32 dead dirs removed (~26 GB). Runtime cross-checks corrected `.docker`, `.pi`, `.prime`, `.linkedin-mcp` to KEEP (active Supabase containers, Grok/Hermes/OmniRoute services).
- 2026-10-13 — V2 working plan is `v2/README.md` and `v2/PLAN.md`. The brief stays in `evolution/engine_v2/` (`OUTCOME.md`, `CONTINUE.md`, `DoD.md`). Code, after the word build, is `evolution/engine_v2/website`. Do not `git init` the parent. Live website `AGENTS.md` and the branch-law hook stay.
- 2026-10-13 — Orca removed. The Windows app, the `sandbox/audit/orca` checkout, hooks, and the `orca-cli` skill are gone. Do not reinstall.
- 2026-10-08 — Acceptance test still scheduled: re-run deep-dive scorer after 2 weeks; pass = correction/redo/scope-drift/time-sink 88–92% → toward 59–61%.

## Ledger
| date | what | repo | commit | state |
|---|---|---|---|---|
| 2026-10-13 | v2 plan placed in sandbox/v2; Orca removed; live-site lock kept | sandbox | this commit | done |
| 2026-10-08 | corpus deep-dive audit + AMEND verdict | sandbox | (this repo) | done |
| 2026-10-08 | RUNBOOK distilled + wired into 5 boot files | sandbox | (this repo) | done |
| 2026-10-08 | skills archive 192→50; census moves (44+10) | (home root) | n/a | done |
| 2026-10-08 | sandbox/rebuild git-inited + snapshot 89d3271 | rebuild | 89d3271 | done |

## Blocked
- V2 code repo waits for the founder to say build.
- OpenRouter paid lane — key budget exceeded (founder top-up only if needed; free lane works).
- gemma-4-31b:free — persistent 429; alternatives: local qwen3.8:27b-64k (used today) or founder adds Google AI Studio key.
- 2-week re-audit — waits on runbook usage (calendar item ~2026-10-22).