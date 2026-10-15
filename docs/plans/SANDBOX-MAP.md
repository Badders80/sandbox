# Sandbox Directory Index

Static. Written 2026-10-15. `/wrap` does not write this file and no session appends to it, so it does not rot. When a folder moves, edit it by hand.

`/home/evo/sandbox` is one git repository (`Badders80/sandbox`) holding several independent workstreams. They share no runtime, no build target, and no lifecycle. `git rev-parse --show-toplevel` resolves to `/home/evo/sandbox` from every folder below except `rebuild/`.

| Workstream | Path | What it is |
|---|---|---|
| V2 product and build law | `v2/` | `PLAN.md` is the build law and the boot path for V2. `OUTCOME.md` is the product law. `README.md` orients. |
| V2 forensic background | `v2/background/` | Pre-build forensics. Reference, not law. |
| V2 R2 setup | `v2/r2-config/` | Bucket configuration notes for the engine. |
| Verification tiers | `docs/plans/VERIFICATION-TIERS.md` | When each verification level runs. Subordinate to `v2/PLAN.md` §Execution Protocol. |
| Estate runbook | `docs/plans/RUNBOOK.md` | The seven guardrails. Wired into boot by `/home/evo/sandbox/AGENTS.md`. |
| Design audit | `audit/design/` | Three-step empirical harvest of the live surfaces, plus `SPEC.md`. Untracked. |
| Corpus deep-dive | `audit/corpus-deep-dive/` | 60-day corpus scoring and its acceptance report. |
| Runbook wiring | `audit/runbook-wiring/` | `gate.json`, one file. |
| `audit/ruflo/` | `audit/ruflo/` | Empty as of 2026-10-15. |
| Business brain | `brain/` | House strategy, audience, and voice. `HOW-TO-USE.md` orients. |
| Rebuild prototype | `rebuild/` | Reference only. **Its own git repo**, with its own `CONTINUE.md`. V2 does not import it. |

## Not law here

`/home/evo/AGENTS.md`, `/home/evo/CLAUDE.md`, and `/home/evo/sandbox/AGENTS.md` describe the old estate. For V2 work they are noise (`v2/README.md` § Do not add instruction files). Root `AGENTS.md` requires `just check`, a venv, and no imports from `evolution/`; this folder is markdown, so none of that binds.

## Where the build is

`/home/evo/evolution/engine_v2/website` is a separate git repo (`Badders80/engine-v2`). It carries its own `CONTINUE.md` brief and its own wrap logs. Nothing in this repository is its boot path, and its `CONTINUE.md` is a boot file — `v2/PLAN.md` reads "`OUTCOME.md`, then `CONTINUE.md`" — so do not delete it while tidying this one.
