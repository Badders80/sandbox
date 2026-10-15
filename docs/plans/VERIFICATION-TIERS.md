# Engine V2 Verification Tiers & Audit Runbook

Drafted 2026-10-15. Subordinate to `sandbox/v2/PLAN.md` §Execution Protocol, which is the sole operational law for any session driving this build. Where this file and PLAN.md disagree, PLAN.md wins and this file is corrected.

This document says when each verification level runs and what it can and cannot see. It does not restate the build law.

## Tier 1 — Hermetic Code Gate

- **When**: Every code edit, every step completion, and GitHub Actions on `ubuntu-24.04`.
- **Command**: `pnpm verify` — lint at `--max-warnings=0`, typecheck, test, build, then `scripts/assert-no-anti-patterns.sh`.
- **Environment**: Node and in-memory seams only (`InMemoryDslStore`). No network. No database service.
- **Pass**: exit code 0.
- **Catches**: broken types, failed assertions, lint drift, banned legacy tokens.
- **Misses**: untested edges, and any surface that is wired in source but not called at runtime.

## Tier 2 — Pre-Commit Adversarial Diff Audit

- **When**: after Tier 1 passes, before `git commit`, on every numbered step.
- **Auditor**: `gemma4:31b` on Ollama Cloud via `$OLLAMA_API_KEY`. If unavailable, stop and ask the founder which model to use (PLAN.md §5).
- **Target**: staged diff, `git diff --cached -- . ':(exclude)pnpm-lock.yaml'`.
- **Rules**:
  - Hunk lines are **pre-numbered** before dispatch. Gemma cannot do unified-diff header arithmetic (`@@ -95,7 +99,12 @@`) and eyeballs 3–6 lines off when forced to. Pre-numbering removes the calculation, so it copies a literal line number. Proven 2026-10-15: 4/4 exact citations after pre-numbering, against 8 dummy citations before.
  - Every rubric item carries a real `file:line` citation. Citations to file headers, import blocks, comments, or blank lines are hallucinated evidence and fail the item (PLAN.md §5).
  - Rubrics carry self-contained literal expected values. No relative doc citations.
  - Reply ends strictly with `VERDICT: PASS` or `VERDICT: FAIL`. The executor never overrides a verdict; a wrong rubric is fixed and the audit re-run.
  - Scope-leakage checks cover code and configuration. Prose in `engine/OPERATIONS.md` is exempt.
- **Catches**: skipped deliverables, negative-constraint violations, banned tokens, prompt evasion.
- **Misses**: anything requiring a second file. Gemma sees one diff and no repository AST. It approved steps 3–5 while a float-modulo bug and an unwired upload button were both live. A PASS here is not evidence of integration.

## Tier 3 — Physical State, Chaos & Deep Stress

Milestone-gated. Never added to step CI, which runs with no database service.

1. **Physical Postgres trigger verification** — before the first live listing. Connect as service-role to local Supabase on `544xx` and assert error `23514` on the forbidden transitions: `image_count < 3`, and an unregistered horse on `available`. Per PLAN.md §Parked, keep this out of `engine/tests/`.
2. **Partial-failure chaos on `saveDsl`** — with the horse editor, and before the engine is pointed at the remote project. Inject failures between the four sequential store writes; assert no stranded row, and assert a retry neither duplicates the trainer nor the owner.
3. **Financial and stake property sweeps** — before Step 8. Sweep modulo and stake math across every valid `step` increment, and prove runtime pricing equals the Postgres generated columns.

Item 2 is **hermetic and belongs in `engine/tests/`**, against `InMemoryDslStore`, so it runs in Tier 1 like any other test. It is listed here because it is milestone-*scheduled*, not because it is non-hermetic. The distinction matters: `dsl-chaos.test.ts` is a `*.test.ts` and CI will collect it.

The numeric domain is `numeric(5,2)`, not integer basis points. The known failure is JS float modulo — `0.3 % 0.1 === 0.09999999999999998` — so the sweep must run in the float domain the code actually uses. A basis-point sweep would pass while the bug ships.

## The supervisory seat — not a tier

Tiers 1–3 are mechanical. They are commands with exit codes, and each one is blind in a documented way. The adversarial supervisory pass is not a fourth tier in that list, because it is not a command; it is the seat that reads cross-file execution paths, physical constraints, and arithmetic traps that no single diff exposes.

It does not replace Tier 2, and Tier 2 does not replace it. Gemma is a tripwire on the diff; it was never an architect. Anything a tier cannot see has to land somewhere, and this is that place.

## Milestone queue

The three unproven items from the steps 1–5 hardening pass are already parked, dated, and scoped in `sandbox/v2/PLAN.md` §Parked. This document points at them rather than copying them, so the two cannot drift:

| Tier 3 item | Parked row |
|---|---|
| 1. Physical trigger check | "Physical trigger check against Postgres" |
| 2. Chaos test on `saveDsl` | "Partial-failure chaos test on `saveDsl`" |
| 3. Property sweeps | "`effectiveMinStake` is wired to nothing" |

None of the three blocks 6a, which reads zero rows.

## Deviations from the 2026-10-15 chat draft

- Filed at `docs/plans/` beside `RUNBOOK.md`, not at the `docs/` root. `AGENTS.md` wires exactly one file from `docs/plans/` into boot; a runbook no boot path references does not exist for the next session.
- Chaos test moved out of the "never in CI" bucket. The draft put it in a milestone tier while naming it `dsl-chaos.test.ts`; PLAN.md §Parked says it stays hermetic in `engine/tests/`.
- "Integer basis-point" corrected to the `numeric(5,2)` float domain.
- The supervisory pass is described as a seat rather than numbered as a third mechanical tier, so "Tier 3" means one thing in this repo. `v2/background/FORENSIC-AUDIT.md` uses Tier 1/2/3 for Postgres constraints, pricing contracts, and legal baselines — a different axis, deliberately not merged.
