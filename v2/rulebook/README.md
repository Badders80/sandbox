# Ownership and Commercial Rulebook

Working canonical v0.1, started 2026-11-11.

This folder is the home for the rules that govern the DSL ownership and
commercial model. It is an index of authority, not a second runtime and not a
replacement for the code, migrations, legal templates or tests.

## What it answers

For every rule:

- what must always be true;
- where it is enforced;
- how it is proven;
- where it sits in the status flow, and who is the primary authority.

## Scope

In scope:

- parties, roles and the ownership model;
- the DSL as a contract series;
- horse percentage points and contract sizing;
- pricing, term and payment model;
- readiness and publication;
- allocation, holds, sales and the register;
- PDS/SA as executed legal records;
- explicit external controls.

Out of scope:

- UI copy and visual design;
- marketing claims;
- public-site flow-ons already registered in `dsl-sidequest/PUBLIC-WRAP.md`;
- restating legal prose from the templates.

## Authority model

- **DB**: invariants that must never be bypassed by any writer.
- **TS**: calculations, orchestration and operator-facing messages.
- **Legal template**: fixed legal prose; only declared tokens are data.
- **Manual/external**: founder-controlled capacity, owner relationships and
  archive/backup controls.
- **Evidence**: tests, SQL probes, ledger walks and written audit records.

One rule has one primary authority. A mirror is allowed only when a conformance
test or probe binds it to the primary authority.

## Worked unit example

A DSL listed at 5.0% of the horse is a 5.0-point contract. An investor buying
1.0% of the horse holds 1.0 point. The derived contract share is 20% and is
display-only. The system never stores or contracts the 20%.

Display convention: money is quoted in whole NZD; percentages keep their exact
stored precision with trailing zeros removed. A 0.1% stake is never displayed
as 1%.

Rule IDs are stable. Do not renumber them; retire a rule and add a new one when
the meaning changes.

## Status vocabulary

The flow is `proposed → locked → enforced`. `external` branches off `locked`
when the rule is deliberately not code-enforceable in v1. `retired` is
terminal from any state.

| Status | Meaning |
|---|---|
| `proposed` | A candidate rule under discussion. Not yet binding. |
| `locked` | Wording is final and an enforcement site plus proof are named. Implementation may still be pending. |
| `enforced` | Implemented and evidenced in the current branch. |
| `enforced (mirrored)` | Enforced in more than one place, bound by a named test or probe. |
| `external` | Deliberately controlled outside the system in v1. |
| `retired` | No longer current; kept for history. |

## Update protocol

- New rules enter as `proposed`. A rule moves to `locked` only when the
  wording is final and an enforcement site and proof are named. A rule moves
  to `enforced` only when that proof exists and has run.
- At chunk start, add or update the rules the chunk will touch.
- During the chunk, cite rule IDs in migration comments and test names where
  practical.
- At chunk close, update evidence and status; add unresolved items to
  `OPEN.md`.
- A ruling changes the rulebook, the enforcement point and the evidence
  together. Do not change code silently.
- Backfill older chunks only when a later change touches them.

## Canonical location

This folder is the working canonical until the sidequest merges. At merge, move
the rulebook into `engine_v2/website/docs/rulebook/` and leave a pointer here.
Do not maintain two live copies.

## Files

| File | Role |
|---|---|
| `RULES.md` | Normative register and enforcement map. |
| `OPEN.md` | Conflicts, gaps, external controls and follow-ups. |

