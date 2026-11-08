# V2 working notes

This folder is the plan. It is the canonical planning repository (Badders80/sandbox).

**Where we are — verified 2026-11-09.** Code is built and green at `0095106`: `pnpm verify` exit 0, 339 engine / 54 website tests, both builds, CI green, tree clean. Nothing has shipped since the 2026-11-07 push. The DoD — one horse sells end to end, real money, real investor — is **not** met. Head of the critical path is **10.3 (data spine)**, blocked on a hosted Supabase project: `SUPABASE_URL` is still `http://127.0.0.1:54421`. Two decisions sit in front of it: build `/horses/new` or seed by script, and which hosted project.

Facts as they actually are (2026-11-09), not as the older notes assumed:

- The local DB (`:54422`) holds **2 horses and 2 DSLs** — Mulan `available` + published, Hottathanafantasy `coming_soon` + draft. That is already one sellable horse; the DoD does not need six.
- The six-horse content lives in the **old** engine at `/home/evo/evolution/engine/content/horses/` (profile.md, pedigree.json, race-record.json, images). `engine_v2` has no content folder — the spine is empty.
- There is **no `/horses/new` route**. `insertHorse` has one call site, `dsl.ts:460` inside `saveDsl`. Trainers and owners both have `new/` pages.
- `WEBSITE_BUY_ENABLED=false`; `ENGINE_EXPIRE_URL`/`ENGINE_EXPIRE_TOKEN` unset, so the scheduled expiry workflow runs green and does nothing.
- Git hygiene: `STEP10-PLAN-2026-11-07.md` is modified-but-uncommitted, and `ALIGNMENT-*`, `PILOT-MULAN`, `SESSION-NOTE-2026-10-23` are untracked. Commit these before handing the folder to a clean clone.

Read `STEP10-PLAN-2026-11-07.md` §4–§6 for the status table and critical path; `engine_v2/CONTINUE.md` for the build log and evidence.

| Role | Path |
|---|---|
| Working plan | `/home/evo/sandbox/v2/PLAN.md` (this folder) |
| Locked brief | `/home/evo/sandbox/v2/OUTCOME.md`, then `/home/evo/evolution/engine_v2/CONTINUE.md` |
| Step-10 plan + status | `/home/evo/sandbox/v2/STEP10-PLAN-2026-11-07.md` |
| Old brief, audit only | `/home/evo/evolution/engine_v2/DoD.md` (not present; `OUTCOME.md` wins) |
| Forensic background | `/home/evo/sandbox/v2/background/` |
| Code, after the word **build** | `/home/evo/evolution/engine_v2/website` |

`engine_v2/` itself is not the repo. Do not `git init` it. Only `CONTINUE.md` lives there now; `OUTCOME.md` is in this folder and `DoD.md` no longer exists.

## What to open

Planning: this folder.

Building, only after you say build: `evolution/engine_v2/website`, once that repo exists.

## Do not add instruction files

Do not add `CLAUDE.md`, `AGENTS.md`, or a skill file in this folder or in `engine_v2/`. The brief and `PLAN.md` are the instructions.

Parent files already on disk will still load, and they describe the old estate. For this work they are noise:

- `/home/evo/AGENTS.md` tells every session to block React until design tokens are locked, and to load `engine/SSOT/doc/CANONICAL_FACTS.md` on turn 1. The v2 outcome says tokens are not a gate, and the product numbers are in `OUTCOME.md`.
- `/home/evo/CLAUDE.md` and `/home/evo/evolution/CLAUDE.md` boot `evolution/engine/website`. That is the current live app.
- `/home/evo/sandbox/AGENTS.md` requires `just check`, a venv, and no imports from `evolution/`. This folder is markdown. Reading the brief is the work. Copying engine source into this folder is not.
- `/home/evo/evolution/docs/superpowers/plans/2026-10-09-v2-repo-setup-streamlining.md` is a different job: infra fixes on the old seven-repo engine. Leave it. Do not follow it.
- Orca was removed on 2026-10-13. Do not reinstall it, and do not follow any leftover note that says to.

`DoD.md` says the plan is `OUTCOME.md`. Where those two disagree, `OUTCOME.md` wins. The rulings are in `PLAN.md`.
