# DSL Side Quest — plan (2026-11-09)

Standalone, admin-only. Takes the DSL engine to a place where it is robust enough
to build everything on. Outside the v2 build rules. Nothing runs until the
founder says **go**.

Companion files: `STATE.md` (position), `PUBLIC-WRAP.md` (what the main build
takes at the end).

---

## 1. What the DSL engine is for

It is the operator's single place to create and maintain a horse's syndication
deal. The engine holds the **rules**; every public surface — the marketplace,
the term sheet, the PDS, the SA, the sale — derives from what it stores.

The standard we are judged against, in one line:

> An operator can create a horse and its deal without getting lost, and no write
> path can produce an incomplete, illegal or partially-saved listing.

Two halves, both required:
- **Robust** — the rules hold for every write, whatever the source.
- **Usable** — the operator sees the deal before committing and cannot fall into
  a broken state through the UI.

## 2. Are we delivering that?

**The first version of this plan was stronger on rules than on use.** The
hardening items (H1–H3, H6) deliver the first half. The UI was a patch list — tiles,
a field, a banner — with no designed creation path, no review step, and no
horse-only create. That is not enough to call the engine a foundation.

This revision adds the missing half: a designed 3–4 step create flow that ends in
the term sheet for confirmation, the same flow for edit, a horse-only create
path, and a shared form system. The image of today's `/dsl/new` is a wall of
ungrouped fields with no styling; that is the thing this plan replaces.

It also adopts a strict single-source boundary (ruling 2026-11-09): **Records own
entities; the DSL owns the deal.** `/dsl/new` and `/dsl/[id]/edit` never author or
edit a horse, trainer or owner — they attach existing records by id and write to
`dsls` only. That removes the four-table write, the orphan-horse risk and the
image-count clobber by construction.

## 3. The operator experience we are building

### Three stages, one pipeline

| Stage | Routes | Owns | Writes |
|---|---|---|---|
| **1. Records** | `/horses`, `/trainers`, `/owners` | facts, images, slug (S1) | those three tables |
| **2. DSL** | `/dsl`, `/dsl/new`, `/dsl/[id]`, `/edit`, `/legal` | deal assembly (2A), the four narrative slots + PDS/SA sign-off (2B, U14 + U10), readiness, publish gate (2C) | `dsls` only, plus the four soft columns on horse/trainer |
| **3. Ledger** | `/sales` | cap table, investor rows, frozen documents, term close | `dsls.status` only |

The sidebar already follows this order: Records → Listings → Sales.

### View a horse — `/horses/[id]`
Profile: identity and registration, trainer, owner, image count, and the DSLs
attached to the horse. Reached from a tile on `/horses`, which becomes the same
tile grid as trainers and owners.

### Add a horse — `/horses/new`
Horse only: identity, registration, loveracing load, plus an **optional current
trainer** (pick existing or leave unassigned). **No owner** — an
owner is a party to a deal and attaches to the DSL, not the horse (`00015`).
Confirm → atomic save → lands on the new profile. No DSL is created. This closes
the long-standing gap where a horse could only exist as a side-effect of a DSL.

### Create a DSL — `/dsl/new`
A centred panel on its own route (pop-up look, linkable, refresh-safe; not a
fragile modal). Four steps, matching how a deal is actually assembled:

1. **Parties** — select an existing horse and two profiles: one holding the
   trainer role, one the owner role. Records only supplies the candidates. A
   profile may hold both roles, and may be both trainer and owner on one deal.
   Readiness badges say at once whether the horse (<3 images, missing prose,
   unregistered) or the chosen trainer profile (missing bio) is ready, with a
   link to fix it in Records. **No inline creation, no edits** — this step
   attaches, never authors.
2. **Commercials** — payment model, term start and end (they decide payment
   eligibility, so they stay here), price entered as wholesale **or** retail with
   the other derived, investor split, listed stake, minimum, step, stake
   remaining shown as derived.
3. **Conditions** — break and exit terms (close style: 14-day notice or 3×
   remaining buyout), distribution schedule, status and published, plus the
   readiness checklist naming anything still missing before Available.
4. **Review** — **the term sheet pops up**: the internal one-pager, with
   **Confirm · Edit · Close**. Confirm performs the single atomic save and lands
   on `/dsl/[id]`; it is allowed for a Coming Soon draft with gaps, and blocked
   only where the chosen status is illegal. Edit returns to the step that owns
   the field. Close discards; no draft row is written mid-flow.

Same four steps for edit, prefilled, with Review saying “Save changes”.

Step rules: client-side checks per step for speed, the server and DB remain
authoritative; a step cannot advance while a blocking field is invalid; the
progress shows where the operator is.

### Step 2B — the soft content and the legal sign-off
The term sheet holds the hard content and stays clean and locked. Step 2B is the
second half of Stage 2: it fills the four cells the PDS reads, shows the compiled
pack, and records the sign-off. It is reached from the 2A term sheet right after
Confirm, and it is the only place the four soft paragraphs are written.

There are exactly **four soft slots**, fixed by the legal corpus
(`engine/src/lib/legal/tokens.ts:103-108`):

| Slot | Lives on | Appears in |
|---|---|---|
| About the horse | horse | PDS §Asset Specifics |
| Racing outlook and pedigree | horse | PDS §Asset Specifics |
| Race expectation | horse | PDS §Summary and §Asset Specifics |
| Trainer bio | trainer | PDS §2.1 About Horse & Trainer |

The editor: one page per horse, four labelled slots with plain-text guidance, a
live PDS preview beside or below so the operator sees where each paragraph lands,
and a count of characters — no HTML, no formatting that the compiler cannot carry.
Empty slots are allowed while the DSL is Coming Soon and are named by the
readiness checklist; all four must be non-empty before Available, which the DB
trigger will enforce (H3).

2B writes the four columns on the horse and trainer — the one named cross-stage
write. The DSL owns none of the content, so it is reused across every DSL on that
horse. The approval is a DSL row, because it is a sign-off on that deal.

The sign-off approves **the prose, not the numbers** — prices and stakes come from
the 2A term sheet and are already fixed. The preview compiles with a preview buyer
and the listing's minimum stake, purely to render the sale lines.

**Headless drafting (ruled 2026-11-09).** The engine never calls a model. The
editor offers **Copy the drafting brief**: plain text holding the locked Stage 1
facts (identity, race record, trainer details), the four slot definitions, and the
voice constraints — no invented facts, no projections, no promises. The operator
pastes it into any chat, pastes the suggestions back into the slots, edits, and
approves. No backend, no keys, and no prose written by the engine. The approval
hash is kept as a **record** of the exact text approved, never as a lock: Stage 1
edits still flow through to live DSLs (Ruling 16), while the record still proves
what was signed off at the moment of approval.

Sign-off storage, on `dsls`: `narrative_signoff jsonb` (the four slot states),
`narrative_approved_at timestamptz`, and `narrative_approved_hash text` (audit
record only). The `available` trigger requires `narrative_approved_at` set and all
four slots approved; it does not compare the hash.

### Sales — the ledger — `/sales`
Stage 3. Today it is a flat dump: DSL id, stake, amount, date. Build three things:

- **Cap table per DSL** — listed, sold, remaining, active holds that have not
  expired, revenue to date, term end.
- **Investor rows** — name, stake, amount, Stripe id, and one-click view of the
  frozen PDS and SA with their SHA-256 hashes.
- **Term close** — an explicit operator action to `completed`, with a confirmation.
  Terms whose end date has passed are surfaced first; early close is allowed.

It reads `sales` and `checkout_sessions`; it writes nothing except the DSL status.

### The form system
One set of primitives used by all three flows: step shell, field group, label and
help text, error slot, stepper, summary row. Styled, keyboard-navigable, 44px
targets, works at 390px.

### The look — the operator console
**Ruled 2026-11-09: no gold anywhere.** The canonical source is
`dsl-sidequest/DESIGN.md` — Altitude, “midnight financial editorial”: near-black
canvas, bone-white serif titles, razor-thin Inter, one blue. The engine app has
**no theme at all today** — `engine/src/app/globals.css` is a single
`@import 'tailwindcss'`. U13 adds the tokens.

- **Surface stack:** `#111` rail · `#181818` canvas · `#1F1F1F` panels · `#262626`
  hover and alternate rows · `#323232` borders; `#4B4B4B` for deep separators.
  Text `#EEEEEE`; muted `#A4A19B`; low-emphasis `#5E5D59`. Hairlines do the
  structure, never shadows. The legal sheet stays pure white — the one light block.
- **Accent:** Voltage Blue `#2B7FFF` only — focus rings, the active step, the
  primary action, a selected row. Mid Navy `#1A365D` only if a heading needs
  depth. Status is a neutral badge with weight and tracking, never a coloured fill.
- **Type:** Inter for all UI, 10–28px; small uppercase labels get +0.025–0.05em.
  Fira Code for every number, date, id, hash and price — +0.1em only on code
  labels, 0 on figures. Libre Baskerville 400 for page titles and the term-sheet
  title; never bold, never italic, never body.
- **Type scale:** caption 10 · body 14 · heading-sm 18 · heading 28 · heading-lg
  36. Tracking straight from the kit: +0.5px at 10, 0 at 14, −0.45 at 18, −0.7 at
  28, −0.9 at 36.
- **Spacing:** 4px base. Console overrides on the landing values: element gap
  **12** (not 8), card padding **20** (not 12), section gap **32** (not 80),
  rail 224, content max 1200.
- **Radii:** inputs, buttons and badges **4**; cards **8**; the pop-up **16**.
- **Not carried over:** mountain imagery, the hero, the 80px section rhythm, the
  72px display, the feature splits. We take the kit, not the landing page.
- **The pop-up:** an 800px centred panel, 16 radius, hairline border, over a
  dimmed backdrop; fixed step header, scrolling body, fixed footer (Back ·
  Continue). Review renders the term sheet as an A4-ish white sheet in the same
  panel.

## 4. Work items

### Hardening

**H1 — The DSL writes one table (HIGH).** Retired by the SSOT boundary: `saveDsl`
no longer inserts a horse, trainer or owner, so a single `dsls` insert/update is
atomic by construction and no four-table RPC is needed. Fix: delete the multi-table
path (`resolveTrainer`, `resolveOwner`, the horse insert, `dsl.ts:400-473`); accept
`horseId` and `ownerId`; prove the save touches `dsls` only and a failure leaves
zero rows. No migration.

**H2 — Status is a machine (HIGH).** `checkStatusTransition` ignores `from`
(`dsl.ts:57-66`). Encode the edges `coming_soon → available`,
`available → fully_allocated`, `available → coming_soon`,
`fully_allocated → completed`, plus two non-transitions that must not be refused:
**no-op** (`from === to`, an ordinary edit) and **initial** (`null → coming_soon`
or `null → available` on insert). Refuse the rest in TS and in a trigger. Proves:
a table test over all `from × to` pairs, including the no-op and null rows.

**Ruled 2026-11-09: completion is manual.** Both `available → completed` and
`fully_allocated → completed` are legal edges. There is no cron and no auto-sweep —
the operator closes a term from the ledger, with a confirmation. Early completion is
allowed (a lease can end early); the UI surfaces terms whose `end_date` has passed
first. The `ENGINE_EXPIRE_*` secrets stay a checkout-hold concern only.

**H3 — One readiness rule (HIGH).** `00015_owner_moves_to_dsl.sql` has already
rewritten `assert_dsl_available` to check the full 17-field set on `dsls` —
`00008` is superseded, not the live rule. The remaining hole is the child tables:
blanking a horse paragraph, the image count, or a trainer bio *after* a DSL went
Available is not caught. Neither is moving a horse to a trainer with no bio. Add
guard triggers on `horses`, `trainers` and `owners` that re-check every dependent
Available DSL — including `horses.trainer_id` changes. Non-empty edits flow
through, by ruling (see Ruling 16). Migration `00021` also adds the 2B sign-off
columns to `dsls` — `narrative_signoff jsonb`, `narrative_approved_at`,
`narrative_approved_hash` — and the `available` trigger requires an approval with
all four slots approved. Keep TS as the
friendly-message layer, not a second authority. Proves: a later blanking is
refused while an Available DSL depends on it; trigger and `readiness.ts` agree on
one fixture set.

**H4 — Wholesale is private; the 100% total is dead (MEDIUM).** Ruled 2026-11-09.
Admin surfaces stop quoting it now. The column drop and the public removal happen
together in P1, which is deferred to the public integration review — so the column
stays until then.

**H5 — Concurrent edits (RETIRED).** The DSL no longer updates the full horse row,
so the image-count clobber cannot happen. It disappears with H1.

**H6 — Sales are append-only in fact, not just in comment (MEDIUM).** `00007`
calls the table read-only, but there is no policy or trigger, and `00013` grants
the service role `update, delete`. Add a trigger refusing update and delete on
`sales`. Migration `00022`.

### Pins — defects to fix inside the named items

**Pin 1 — `stake_remaining` never initialises on a draft priced later.** `saveDsl`
sets it from `listedStake` on insert (`dsl.ts:469`), but `updateDsl` omits it
(`dsl.ts:610-615`). A draft created with no stake (`00014` allows null) can never
reach Available. Fix in H1/U11: set it when it is null; never reset it once
non-null, because buyers have drawn it down.

**Pin 2 — the DB allows a null owner, the code does not.** `00015` makes
`dsls.owner_id` nullable on purpose; `resolveOwner` refuses to save without one.
Fix in U11: a Coming Soon draft may have no owner; the Available gate still
requires one.

**Pin 3 — `saveDsl` must accept existing ids.** Now the core of H1, not a side
note: Step 1 hands over `horseId` and `ownerId`; keep the rule that a horse already
holding a DSL is refused — multiple concurrent DSLs per horse is out of scope.

**Pin 4 — no-op and initial transitions.** Part of H2; called out here so the
matrix test includes them.

**Pin 5 — one TS line for an optional trainer.** `NewHorse.trainerId: string`
(`dslStore.ts:70`) becomes `string | null`. Part of U12.

### Operator surfaces

**U1 — `/horses` tile grid.** Same pattern as trainers/owners: image, name,
status, trainer; links to the profile. ~1 h

**U2 — `/dsl` list shows the horse name.** Page-side join against `listHorses`.
~30 min

**U3 — Trainer/owner: three sections + socials + links (schema `00019`).**
Confirmed 2026-11-09; folded into `parties` by P0 (2026-11-10) and carried over
by `00021`. Both tables gain `achievements`, `other`, `x_url`,
`facebook_url`, `instagram_url`, `links` jsonb. Fixed order: Profile →
Achievements → Other → Social → Links. Optional, so readiness and legal templates
are untouched. Admin-only private store. ~3 h

**U4 — DSL term sheet as the internal one-pager.** Same numbers; better hierarchy;
adds the operational facts already in the rows (owner contact, trainer stable,
horse facts, image count, slug, readiness gaps). ~3 h

**U7 — Two-way price entry.** Enter wholesale or retail; the other is derived.
Retail stays a whole dollar rounded up. Retail entry snaps to the whole-dollar
wholesale that reproduces it, falls back to 2dp, and refuses if none. Shows both
before saving. ~2 h

**U8 — Sidebar Home + index page.** Home first; `/` lists Horses → Trainers →
Owners, each with a small header. ~1 h

**U9 — `/horses/[id]` profile.** Identity, registration, trainer, owner, images,
its DSLs. ~2 h

**U10 — Draft PDS/SA.** Already at `/dsl/[id]/legal`; add a **DRAFT — not
executed** banner and the blocking-field list on failure. ~1 h

**U11 — The create/edit flow.** The four-step panel described in §3, reusing the
form system. Step 1 selects a horse and two role-holding profiles from existing
records only; one atomic `dsls` write at Confirm. ~7 h

**U12 — `/horses/new`.** Horse-only flow. **No trainer and no owner** — the
horse/trainer/owner link happens at DSL creation (ruling 10). Lands on the
profile. ~3 h

**U13 — Form system and admin theme.** The engine theme tokens (the app has none
today), shared primitives, validation display, keyboard and mobile behaviour, used
by U11 and U12.

Also a full light-class sweep: **10 engine files** carry `border-black/10-40`
from the old white theme (`trainers/[id]`, `trainers/new`, `trainers/page`,
`owners/[id]`, `owners/new`, `owners/page`, `horses/page`, `dsl/page`,
`sales/page` and the DSL detail). On `#090909` those borders vanish. Replace every
one with the token hairline, and add a source guard so `border-black` cannot
reappear. ~5 h

**U14 — Narrative editor.** The four PDS soft slots on one page per horse, with a
live PDS preview, a readiness count and **Copy the drafting brief**; reached from
the 2A term sheet and the DSL page. Sign-off writes the three columns above. ~3.5 h

**U15 — Sales ledger.** Cap table per DSL (listed, sold, remaining, live holds,
revenue, term end), investor rows with the frozen PDS/SA and hashes, and the term
close action. ~4 h

### Step-10 leftovers

**S1 — Rename moves the R2 image folder.** **Deferred 2026-11-09 to the public
integration review** — no R2 or image work happens in this quest. The public
consequence is why: the marketplace builds image URLs from the slug (`site.ts`
`heroImageUrl` → `imageKey(slug, 1)`), so a naive move opens a 404 window. When it
runs, order it **copy → update the slug → verify the new keys serve → delete the
old ones**. No window, no broken card. ~3 h

### Public flow-ons — deferred to the integration review

**P1** wholesale off the public page + drop `wholesale_monthly_total` (takes the
next free migration at review time). **P2** buy
flow defaults to 1%. **P3** public projection proof with screenshots. Detail in
`PUBLIC-WRAP.md`.

## 5. Chunks — rebalanced 2026-11-09

Each chunk ends gate-green, gets one Gemma audit on the chunk diff, and stops for
the founder's eye before the next begins. Sizes are balanced at roughly one to two
working days; the old single DSL chunk was 28.5 h and is now split.

**Chunk 1 — Records, Home and the form system** · ~15 h
U13 → U8 → U1 → U9 → U12 → U3. Migration `00019`.
Gate: `pnpm verify`; screenshots of `/`, `/horses`, a profile, and the add-horse
flow.

**Chunk 1b — loveracing load, barn name, slug law** · ~4.5 h — **DONE `e30e50c`**
L1 + B1: fetch through `curl_cffi`, parse the real Stud Book markup, accept
`/Breeding/` and `/stud-book/`, optional `barn_name` (`00020`), slug drops the
`(NZ)` suffix, unnamed `sire-x-dam-yr` rule. Gate green 343/54; audit PASS.

**Chunk 1c — horse edit** · ~2 h — **DONE `82a702d`**
`/horses/[id]/edit` with `updateHorseAction`, shared `HorseForm`, trainer
assignment, Edit link on the profile. Slug fixed on edit. Gate green; audit PASS.

**Chunk 1d — profile polish found necessary in use** · **DONE 2026-11-10**
(head `d387225`; no separate audit — the chunk-2 audit covers the diff)
Deduplicated profile headings; trainer = Company name + one or more Trainer names
joined `' & '` (rulings 17); links as a raw registry with add/remove, title
fetching removed (ruling 18); social URLs render as handles (ruling 19);
`/trainers/[id]/edit` and `/owners/[id]/edit` use the horse Edit pattern
(ruling 20); `NEXT_DIST_DIR` isolates a dev server from a build (ruling 21).
Gate: typecheck + lint + test green, engine 346/346, website 54/54.

**Chunks 2–4 are LOCKED (2026-11-10).** Contents change only by ruling.

**Chunk 2 — Harden the engine** · LOCKED
P0 (profiles + roles) → H2 → H1 (no migration) → H3 (`00021`, shared with P0) →
H4a → U2 → R1.
Gate: `pnpm verify`; psql parity; an unapproved DSL refused `available` by SQL;
the status matrix test over all `from × to` pairs; `/trainers` and `/owners`
are role-filtered views of one profile table; `horses` stores no trainer.

**Chunk 3 — Deal assembly (2A → 2B → 2C)** · LOCKED
U4 → U7 → U11 → U14 → U10. No migration — the sign-off columns ride in `00021`.
The pieces land before the wizard that uses them, so the review step is built
against the final term sheet and price entry.
Gate: `pnpm verify`; a full 2A walk ending in the term sheet review; 2B narration
and sign-off; a rendered draft PDS/SA; two-way price round-trip.

**Chunk 4 — Ledger** · LOCKED
U15 + H6 (`00022`). Gate: `pnpm verify`; a ledger walk over the existing sale
fixture; an update/delete on `sales` refused.

### After this quest — the public integration review

The rename and its R2 image move (S1), plus P1, P2 and P3, are **not part of this
DoD**. They stay registered in
`PUBLIC-WRAP.md` and get their own review once the engine is locked: what the
public site needs from it, how it integrates, and in what order. This quest is the
engine, not the shopfront.

One live consequence to keep in view: until that review, the public marketplace
still shows the wholesale total.

## 6. Out of scope

- Auth / Cloudflare Access — cutover batch.
- **The rename and its R2 image move (S1), and the public wrap (P1–P3)** — one
  follow-on review; see `PUBLIC-WRAP.md`.
- Public profile pages — the content is a private store.
- v2 doc reconciliation — see `PUBLIC-WRAP.md`.
- Any public redesign.
- The six horses as content; two exist, one is buyable.

## 7. Budget

**6 working days** (planning estimate, ~48 h), hard stop **9 days**.

Breakdown: records, Home and forms 15 h; hardening 9 h; deal assembly 16.5 h;
ledger 4.5 h; audits and rework ~3 h. The rename (S1) and the public review are
separate and not counted here.

## 8. How the work runs

**Ruled 2026-11-09.**

- **Driver:** the Claude Code harness running **DeepSeek V4.1 Flash** (Ollama
  Cloud), in agent mode. It owns the DoD, the branch, every gate and every stop
  point.
- **Execution:** in-session, not dispatched. If a bounded job is ever handed to a
  dispatch exec seat, the driver still runs the gate itself — dispatch's
  `just check` reports **SKIP** here because the repo has no Justfile.
- **Audit:** **Gemma 4 31B** (Ollama Cloud) on each chunk diff, one audit per
  chunk, via `~/bin/dispatch ask gemma`. Findings are folded before the next chunk.
- **Branch:** `dsl-sidequest` off `main`, created in its own command.
- **Stop:** each chunk ends gate-green and waits for the founder's eye.

## 8.1 Gate, assurance, tools

- **Gate:** `cd /home/evo/evolution/engine_v2/website && pnpm verify`
  (baseline 339 engine / 54 website).
- **Assurance: Tier A.** Money path, data writes, schema migrations, public
  surface. Never ship on the implementer's word.
- **Tools:** `dispatch ask gemma`; `psql :54422`; browser screenshots at 1440×900
  and 390×844.
- **Where:** repo `/home/evo/evolution/engine_v2/website`.

## 9. Rulings recorded

1. Standalone, admin only; no v2 doc edits until merge.
2. DB trigger authoritative; guards on the referenced tables.
3. Six profile fields, migration `00019`.
4. Wholesale private; 100% total dropped (P1).
5. Retail is a whole dollar, rounded up; two-way entry.
6. **Create flow is a 4-step panel — Parties · Commercials · Conditions ·
   Review — ending in the term sheet with Confirm / Edit / Close**
   (2026-11-09).
7. **Horse-only create path is in scope** (2026-11-09).
8. **Soft content is a separate structured editor** — the four fixed PDS slots,
   with a live preview; the term sheet stays hard, clean and locked
   (2026-11-09).
9. Budget 6 days, stop 9 (locked 2026-11-09).
10. **Link model (re-ruled 2026-11-10)** — one **profile** per real-world person
    or company (`parties`), with roles ticked on it (`party_roles`: `trainer`,
    `owner`, extensible). Shared fields live once; the trainer block and owner
    block render by role, so one profile serves both surfaces with no duplicate to
    drift. The **DSL is the only place a deal links them**: `dsls.horse_id`,
    `dsls.trainer_id`, `dsls.owner_id`, each pointing at a horse or a party
    holding the required role. Records pages show the link as a **derived view**
    and never author it. Horses stay assets, not profiles. **No `horse_owners`
    table and no second link table.** Trainer may be blank while Coming Soon and
    is required before Available, like owner.
11. **Strict SSOT boundary** — Records own entities; the DSL attaches ids and
    writes `dsls` only. No inline creation or editing in `/dsl`.
12. **Three-stage pipeline** — Records → DSL → Ledger, matching the sidebar.
13. **Completion is manual** — `available → completed` and
    `fully_allocated → completed`, set by the operator from the ledger; no cron,
    no auto-sweep. Early close allowed; expired terms surfaced first.
15. **Trainer change** — edit the trainer on the **DSL**; every **new** document
    uses the new trainer; sold documents are never changed or reissued; investor
    notification is manual. Records shows the new link immediately because it is
    derived.
16. **Stage 1 edits flow through** — a non-empty edit to horse, trainer or owner
    feeds every live DSL and the next compilation; locking happens at the sale,
    which freezes the PDS/SA and hashes. Only blanking a required field (or
    pointing a horse at a bio-less trainer) is refused while a DSL is Available.
14. **Headless drafting** — the narrative editor copies a brief out and pastes
    suggestions back; the engine never calls a model and never writes prose.
    Approval is recorded against the text by hash, never enforced.
17. **Trainer row = company + names** (2026-11-10) — Company name plus one or
    more Trainer names; one row per company, names joined `' & '`, because a
    horse attaches to a single `trainer_id` and the PDS prints `trainer.name`.
18. **Links are a raw registry** (2026-11-10) — one URL per row, stored as given,
    label is the hostname; no fetching, title reading or rewriting.
19. **Social renders as a handle** (2026-11-10) — X, Twitter, Instagram and
    Facebook URLs show `@handle`; the full URL stays in the link and its title.
20. **Trainer/owner Edit uses the horse pattern** (2026-11-10) — a top-right Edit
    link to a dedicated `/[id]/edit` route, same breadcrumb and heading.
21. **Dev servers get their own cache** (2026-11-10) — `NEXT_DIST_DIR` selects the
    build directory so a build cannot rewrite a running dev server's chunks.
22. **Roles are relationships, not permissions** (2026-11-10) — a role says what
    a profile is to a deal, never what it may do in the app; auth stays
    Cloudflare Access. Unticking a role a live DSL references is refused, never
    cascaded.

## Ready

Chunks 1–1d are done. The next action is **`go chunk 2`** — H2 first.
