# DSL Side Quest

A standalone, admin-only push to make the DSL engine robust and finish the
operator pages. Outside the v2 build rules; it keeps its own plan and state.

**Read `STATE.md` first. It is the current position. `PLAN.md` is the detailed
plan and does not change without a ruling.**

| File | Role |
|---|---|
| `STATE.md` | current chunk, rulings, next action — read first |
| `PLAN.md` | items H1–H4, H6, U1–U15, S1, P1–P3, chunks, budget, assurance |
| `PUBLIC-WRAP.md` | the register of public flow-ons and what the main build takes at the end |
| `DESIGN.md` | the source design kit — a resource, not a mandate |

## How DESIGN.md is used

`DESIGN.md` is the Altitude kit, downloaded 2026-11-09 and kept **verbatim**.
It is a resource, not a brief: we take its tokens, not its page composition.

- **Take:** the five-step surface stack, Voltage Blue rationing, the type scale and
  tracking, 4px spacing base, 4/8/16 radii, hairline structure, restrained shadows.
- **Leave:** mountain imagery, the hero, the 80px section rhythm, the 72px display,
  feature splits, the marketing composition.
- **Overrides for a console** live in `PLAN.md` §3: element gap 12 (not 8), card
  padding 20 (not 12), section gap 32 (not 80); Libre Baskerville on page titles
  only, Inter for UI, Fira Code for figures.
- **No new tokens.** If the console needs something the kit does not have, it is
  added to `PLAN.md` §3 first and only then to the theme.

## Shape

Four chunks, one at a time, each ending gate-green and audited:

1. Records, Home and the form system — **done** (1, 1b, 1c, 1d)
2. Harden the engine — **LOCKED, next**
3. Deal assembly (2A → 2B → 2C) — **LOCKED**
4. Ledger — **LOCKED**

Chunk contents are in `STATE.md`; they change only by ruling.

The rename with its R2 image move (S1), and the public wrap (P1–P3), are **not**
chunks of this quest. They are a separate follow-on integration review,
registered in `PUBLIC-WRAP.md`.

## Where it happens

Repo `/home/evo/evolution/engine_v2/website`, branch `dsl-sidequest`.
Gate: `pnpm verify`.

## Rules

- Admin only. The public site is not touched until the wrap.
- Every public consequence is written into `PUBLIC-WRAP.md` as it is found, then
  executed once at the end (`PLAN.md` §4, Public flow-ons).
- Nothing runs until the founder says **go**.
