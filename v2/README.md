# V2 working notes

This folder is the plan. It is the canonical planning repository (Badders80/sandbox).

**Start here: `STATE.md`.** It is the one-page, dated, verified state and the recap protocol. If a session is asked "where are we at on sandbox/v2", it reads `STATE.md` first and runs the fast checks it lists. Do not re-derive from dated session notes; they are history.

Verified 2026-11-09, in one line: code green at `0095106` (339 engine / 54 website, exit 0), DoD not met, head of the critical path is 10.3 blocked on a hosted Supabase project. Details, blockers, decisions and the ordered "go" list are in `STATE.md`.

| Role | Path |
|---|---|
| **Current state + recap protocol** | `/home/evo/sandbox/v2/STATE.md` |
| Working plan | `/home/evo/sandbox/v2/PLAN.md` (this folder) |
| Locked brief | `/home/evo/sandbox/v2/OUTCOME.md`, then `/home/evo/evolution/engine_v2/CONTINUE.md` |
| Step-10 plan + status | `/home/evo/sandbox/v2/STEP10-PLAN-2026-11-07.md` |
| Old brief, audit only | `/home/evo/evolution/engine_v2/DoD.md` (not present; `OUTCOME.md` wins) |
| Forensic background | `/home/evo/sandbox/v2/background/` |
| Code, after the word **build** | `/home/evo/evolution/engine_v2/website` |

`engine_v2/` itself is not the repo. Do not `git init` it. Only `CONTINUE.md` lives there now; `OUTCOME.md` is in this folder and `DoD.md` no longer exists.

## What to open

Planning: this folder, starting at `STATE.md`.

Building, only after you say build: `/home/evo/evolution/engine_v2/website` (the repo already exists; it is `Badders80/engine-v2`).

## Do not add instruction files

Do not add `CLAUDE.md`, `AGENTS.md`, or a skill file in this folder or in `engine_v2/`. The brief and `PLAN.md` are the instructions.

Parent files already on disk will still load, and they describe the old estate. For this work they are noise:

- `/home/evo/AGENTS.md` tells every session to block React until design tokens are locked, and to load `engine/SSOT/doc/CANONICAL_FACTS.md` on turn 1. The v2 outcome says tokens are not a gate, and the product numbers are in `OUTCOME.md`.
- `/home/evo/CLAUDE.md` and `/home/evo/evolution/CLAUDE.md` boot `evolution/engine/website`. That is the current live app.
- `/home/evo/sandbox/AGENTS.md` requires `just check`, a venv, and no imports from `evolution/`. This folder is markdown. Reading the brief is the work. Copying engine source into this folder is not.
- `/home/evo/evolution/docs/superpowers/plans/2026-10-09-v2-repo-setup-streamlining.md` is a different job: infra fixes on the old seven-repo engine. Leave it. Do not follow it.
- Orca was removed on 2026-10-13. Do not reinstall it, and do not follow any leftover note that says to.

`OUTCOME.md` is the plan. Where any older brief disagrees with it, `OUTCOME.md` wins. The rulings are in `PLAN.md`; current status is `STATE.md`.
