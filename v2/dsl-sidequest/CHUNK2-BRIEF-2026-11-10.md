# Chunk 2 brief — harden the engine, one profile with roles

Repo: `/home/evo/evolution/engine_v2/website` (branch `dsl-sidequest`).
Contract of record: `/home/evo/sandbox/v2/dsl-sidequest/STATE.md` § **Chunk 2 —
Harden the engine · LOCKED**. Rulings 10, 11, 13, 15, 16, 22 bind.
Gate: `just check` (Justfile) = `pnpm verify`.

## Deliver, in this order

1. **P0 — one profile, roles.** Merge `trainers` and `owners` into `parties` +
   `party_roles` (`trainer`, `owner`, extensible). Shared fields live once.
   `/trainers` and `/owners` become role-filtered views. Each profile's edit page
   ticks roles ("Add as an owner" / "Add as a trainer"). `dsls.trainer_id` and
   `dsls.owner_id` become FKs to `parties(id)`.
2. **H2 — status is a machine.** Encode `coming_soon → available`,
   `available → fully_allocated`, `available → coming_soon`,
   `fully_allocated → completed`, `available → completed`, plus no-op
   (`from === to`) and initial (`null → coming_soon | available`). Refuse the
   rest in TS and in a `00021` trigger. Completion stays manual.
3. **H1 — the DSL writes one table.** `saveDsl`/`updateDsl` take `horseId`,
   `trainerId`, `ownerId`; delete `resolveTrainer`, `resolveOwner`, the horse
   insert and the four-table path. One `dsls` write; a failure leaves zero rows.
4. **H3 — readiness cannot be cheated.** Guard triggers on `parties`,
   `party_roles`, `horses` and `dsls`: a role untick or a blanked required field
   while an Available DSL depends on it is refused; non-empty edits flow. Same
   `00021` adds `narrative_signoff jsonb`, `narrative_approved_at`,
   `narrative_approved_hash`; the Available trigger requires all four slots
   approved.
5. **H4a — wholesale is private.** Admin surfaces stop quoting the 100% total.
   Do not drop the column (P1, deferred).
6. **R1 — Records shows the link, never authors it.** Remove the trainer from
   `HorseForm`, `/horses/new`, `/horses/[id]/edit` and `updateHorseAction`. The
   horse profile and `/horses` derive the trainer through its DSL.

**U2 is already done** (`0f4a13a`): the `/dsl` list shows Horse and Expiry. Do not
redo it.

## Verified starting facts (checked 2026-11-10, this machine)

- `checkStatusTransition` at `engine/src/lib/dsl.ts:57-67` enforces only the
  registration gate and **ignores `from`**.
- `resolveTrainer` `engine/src/lib/dsl.ts:334`, `resolveOwner` `:384`,
  `saveDsl` `:444`, `SaveDslInput` `:117` — the multi-table path still exists.
- `engine/src/app/dsl/DslForm.tsx` is 372 lines and authors horse identity
  (`legalName:78`, `sireName:103`, `damName:108`), trainer creation `:170`,
  owner creation `:218`, Branding `:346`.
- Migrations live at `supabase/migrations` (repo root), latest
  `00020_barn_name.sql`. **No** `narrative_signoff` / `narrative_approved_*`
  columns exist anywhere.
- `horses.trainer_id` is read in ~13 engine files; `website/src` never reads a
  horse trainer.
- `engine/src/lib/termSheet.ts` exists (215 lines) and `/dsl/[id]` calls
  `buildTermSheet`; `engine/src/lib/term.ts` has `termMonthsBetween` and
  `paymentModelAllowed` (`FLOAT_MIN_TERM_MONTHS = 6`); `pricing.ts` retail =
  `ceil(wholesale * 1.05 * 1.03)`.
- Target DB: hosted `evolution-engine` (`rkcptsghxovoeaycabah`, Sydney);
  `engine/.env.local` points at it.

## Rules

- **One migration only: `00021`.** It creates `parties` + `party_roles`, copies
  every `trainers` row with the trainer role and every `owners` row with the
  owner role, drops the old tables; adds `dsls.trainer_id` and drops
  `horses.trainer_id`; adds the three narrative columns.
- No compatibility views, no dead columns, no new link table.
- Roles are relationships, not permissions. Auth is out of scope.
- Do not touch `website/`, pricing or legal templates, the sales ledger, or PDS
  rendering.
- Never push and never merge. Work only in the worktree.
- Every claim in the final report needs a command output behind it.

## Gate and proof

- `cp /home/evo/evolution/engine_v2/website/engine/.env.local engine/.env.local`
  in the worktree first — it is gitignored, and its absence is not a code result.
- `pnpm verify` green.
- Status-matrix test over every `from × to`, including the no-op and null rows.
- SQL refuses `available` for a DSL whose narrative is unapproved.
- A `dsls` write is refused unless the party holds the role; a role untick is
  refused while a live DSL references it.
- psql parity local ↔ hosted for `00021`.
- `/trainers` and `/owners` render as role-filtered views; horse pages show the
  trainer through the DSL; `horses` has no trainer column.
- Report: diff stat, migration file, test evidence, and any open question.

## Report, do not resolve

- The **break clause** has no column. Do not invent one and do not add a
  migration for it. Name it as an open decision.
