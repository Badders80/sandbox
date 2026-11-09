# DSL Side Quest — execution DoD (2026-11-09)

Status: **Ready** — rulings locked 2026-11-09.
Source of truth for *what* is `PLAN.md`; this file is the *how we run it* contract.

## Done, in one sentence

All four chunks land on `dsl-sidequest`, each gate-green and audited, and the
branch merges to `main` only on the founder's word. The rename/R2 move (S1) and
the public wrap (P1–P3) are a separate follow-on review, not part of this DoD.

## Repo facts verified today (live surface, not the plan's word)

| Check | Result |
|---|---|
| Repo | `/home/evo/evolution/engine_v2/website` (monorepo: `engine/`, `website/`) |
| Branch | `main` @ `0095106`, working tree clean, no `dsl-sidequest` branch yet |
| Gate | `pnpm verify` = typecheck && lint && test && build |
| Migrations | `00019` (profiles) and `00020` (barn name) applied. Next free: `00021` for chunk 2, `00022` for chunk 4; the public review takes the next free after that |
| U13 premise | `engine/src/app/globals.css` is one line: `@import 'tailwindcss'` ✓ |
| H2 premise | `dsl.ts:57-66` `checkStatusTransition` never reads `from` ✓ |
| Pin 5 | `dslStore.ts:70` is `trainerId: string` ✓ |
| Audit seat | `dispatch ask gemma` → `gemma4:31b:cloud`, named diff auditor for engine-v2 ✓ |
| DB | `psql :54422` open; `engine/.env.local` + `website/.env.local` present |
| Baseline | **confirmed green at `0095106`**: engine 339/339, website 54/54, exit 0 (`pnpm verify`, 2026-11-09) |

## Where

- Repo `/home/evo/evolution/engine_v2/website`; branch `dsl-sidequest` off `main`,
  created **in its own command** (branch guard is PreToolUse and kills a
  compound command).
- Stage exact paths only — never `git add <dir>` in a shared checkout.

## Target database — the new Supabase project (added 2026-11-09)

The quest stops being local-only. A **new hosted Supabase project** is the target
engine database; the old project (`ejdenhlpvtldiljxawtd`) stays untouched with the
public website until cutover.

**Ruling — files, never rows.** The new project is built by applying
`supabase/migrations/00001…` **only**. No `pg_dump --data`, no `COPY`, no CSV, no
row export of any kind. Migrations are schema-only today: the three `insert into`
statements in `00012:32`, `00017:50`, `00018:61` live inside function bodies and
never fire during replay. If a future migration ever needs seed rows, it is
declared here first, in the same commit, with the reason.

**Sequence.**
1. Founder mints the project and hands over the DB connection string and
   service-role key. Nothing else starts first.
2. Replay every migration in filename order into the new project.
3. **Zero-rows gate:** `count(*)` on all 7 public tables must be `0`. Recorded.
4. **Parity gate:** tables, columns, triggers, functions, policies and grants must
   match local exactly. Diffs recorded. This is the highest-trust artifact in the
   quest — it proves the engine reproduces from files alone.
5. From then on, `engine/.env.local` points at the new project. 3001 authors
   against it. Local stays as the scratch replay the parity gate compares to.
6. Chunks 2 and 4 each ship a migration (`00021`, `00022`), apply it to both, and
   re-prove parity before the chunk closes.

**Slop cannot travel** because the only channel into the new project is (a) the
migration files and (b) content authored through 3001. Probe rows created during a
walk are deleted before the chunk closes.

## Budget

6 working days / ~48 h; hard stop 9 days. Per chunk ~15 / 9 / 16.5 / 4.5 h, plus
~2 h for the target-database track (replay, zero-rows, parity), run once.
Stop and check in at the end of every chunk.

## Assurance

**Tier A.** Schema migrations, data writes, money path (price/stake). No public
code, schema or asset changes happen in this quest — S1 moved out with the wrap,
so the public surface is genuinely untouched. So: gate + one
`dispatch ask gemma` audit on the mergeable chunk diff, findings folded **before**
the next chunk starts. A chunk that adds a migration also gets a psql parity check
(the SQL actually refuses what the plan says).

## Run mechanics

- **Diff for the audit:** `git diff main...dsl-sidequest > /tmp/chunk-N.diff`, then
  `dispatch ask gemma "<brief with the path>" /home/evo`. One audit per chunk.
- **Triage:** see **Decision policy** below — it decides fix-versus-record, so no
  mid-chunk question is needed.
- **Commit law:** one commit per chunk on `dsl-sidequest`. No push, no merge, no
  deploy until the founder says so. A chunk that cannot reach green reverts to its
  first green commit and stops.
- **Guard:** `border-black` is banned by **extending the existing
  `scripts/assert-design-tokens.sh`** (repo root, already chained into the root
  `pnpm test`), not by adding a ninth script. Its palette rule at `:61` alternates
  over named palettes and **`black` is not in that list**, so loosening the `-NNN`
  suffix there changes nothing — that was checked and is wrong. Add a separate,
  narrow rule:
  `border-(black|white)(/[0-9]+)?` — and do **not** touch `bg-white` / `text-white`
  (the legal sheet is white on purpose). Scan the whole `engine/src` tree, never a
  hardcoded list. Live set on 2026-11-09: 10 files, 34 hits, all of the form
  `border-black/10|20|30|40`; `PLAN.md` names the tenth file wrongly (it is
  `_components/OperatorNav.tsx`). **Prove the new rule RED against the current tree
  before the sweep, GREEN after** — a guard that cannot fail is decorative.

## Decision policy (binding — never stop mid-chunk to ask)

| Situation | Action |
|---|---|
| Gate red | **Stop.** Baseline is green at `0095106`, so red belongs to this diff. Never fix unrelated tests to unblock. |
| Audit FAIL whose cited `file:line` reads true | Fix it. |
| Audit FAIL the driver believes is wrong | Do **not** fix. Record it in `STATE.md` under *audit disputes* with the evidence, continue, and name it at the chunk stop. |
| WARN that touches a rule | Fix it. |
| Any other WARN | Record in `STATE.md`. No code change. |
| Chunk end | Report and wait. Never start the next chunk. |

**"Touches a rule"** means the finding names a locked fact, a schema or migration, a
status edge, a readiness rule, a money path (price, stake, split), or the public
projection.

**Checkpoint:** update `STATE.md` after each unit inside a chunk; stop only at the
chunk boundary.

## Tools

- Gate: `pnpm verify`.
- App for screenshots: `cd engine && pnpm dev` → `http://localhost:3001`
  (`next dev --port 3001`). The public site is `:3000`. Check with `ss -lntp` first —
  a server was already up on `:3001` on 2026-11-09; do not start a second on the same
  port.
- Audit: `dispatch ask gemma` (`gemma4:31b:cloud`).
- DB parity: `psql :54422`.
- Screenshots: chrome-devtools MCP at `1440×900` and `390×844`.
- **Hover caveat:** the headless browser reports `(hover: none)`, so hover variants
  are inert. Verify a hover by its rule and token, never by pointer.

## Chunk contracts

Each chunk: build → `pnpm verify` green → **public sweep** → gemma audit on the
chunk diff → stop.

**Public sweep (every chunk, no exceptions).** Read the chunk diff against what the
public site actually consumes — `website/src/**` plus the `dslStore` /
`listings` projections in `engine/src/lib/` — and add a `PUBLIC-WRAP.md` row for
every consequence it finds. If there are none, the chunk's commit message ends
with `public-sweep: none`. A row beats a memory; the audit reads the commit
message and the register, not the driver's recollection.

### 1 — Records, Home, forms · ~15 h
`U13 → U8 → U1 → U9 → U12 → U3`, migration `00019`.
Done: theme tokens + form primitives exist; `/` indexes Horses/Trainers/Owners;
`/horses` is a tile grid; `/horses/[id]` profile; `/horses/new` saves horse-only
with optional trainer and lands on the profile; trainer/owner gain the six fields;
zero `border-black` left in engine (guard added).
Proof: gate; screenshots `/`, `/horses`, a profile, add-horse at 1440×900 and 390×844.

### 2 — Harden · ~9 h
`H2 → H1 → H3 (00021) → H4a → U2`.
Done: status edges enforced in TS **and** trigger incl. no-op and null-initial;
`saveDsl` touches `dsls` only; guard triggers refuse blanking a field an Available
DSL depends on; sign-off columns exist and the available trigger requires them.
Proof: gate; status matrix over every `from × to`; a psql insert proving an
unapproved DSL cannot go `available`, and that blanking a horse paragraph is
refused; zero rows left behind by a failed save.

### 3 — Deal assembly · ~16.5 h
`U4 → U7 → U11 → U14 → U10`. No migration.
Done: term sheet one-pager; two-way price round-trips; 4-step panel with
Confirm/Edit/Close and one atomic write; narrative editor with live PDS preview,
copy-brief and sign-off; draft PDS/SA banner.
Proof: gate; a full 2A walk to the term sheet; 2B narration + sign-off; rendered
draft PDS/SA; retail→wholesale→retail equality.

### 4 — Ledger · ~4.5 h
`U15 + H6 (00022)`.
Done: cap table, investor rows with frozen PDS/SA + hashes, manual term close;
`sales` refuses update/delete.
Proof: gate; ledger walk on the existing sale fixture; a refused update and delete.

## Out of scope

Auth/Cloudflare Access; **the rename and its R2 image move (S1), and the public
wrap (P1–P3) — one follow-on review**; public profile pages; v2 doc
reconciliation; any public redesign; the six horses as content.

**After this DoD:** the branch merges to `main` on the founder's word, then the
wrap runs once as a single review pass — S1 and P1–P3 executed, proof written, and
the deferred register plus the v2 docs folded back into the main build
(`PUBLIC-WRAP.md`). This DoD ends at the ledger; it does not close the public gap.

## Rulings

1. **Sign-off invalidation: stay.** Editing a soft slot after approval does not
   clear `narrative_approved_at` — Rulings 14 and 16 already decided it: the hash
   is a record, and locking happens at the sale. Clearing it could strand a live
   DSL. A read-only “changed since approval” flag in the ledger is optional, not
   required.
2. **The wrap is deferred wholesale** (2026-11-09). S1 (the rename and its R2 image
   move) goes with P1–P3 into one follow-on integration review; this DoD ends with
   the ledger in chunk 4.
3. **Budget: 6 days, stop 9.** `PLAN.md` §7, ruling 9 and `STATE.md` agree.
4. **Retired ids:** `U6` and `S2` are gone from `PLAN.md` §4; `PUBLIC-WRAP.md`
   now calls them retired.

## Ready

Say **go** to start chunk 1 at U13.
