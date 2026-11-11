# DSL Side Quest — state

**Last updated: 2026-11-11. All four chunks are done, gate-green, audited and
merged on `dsl-sidequest`. The Mulan walk, F1–F5 and the public wrap remain.**

## Position

| Fact | Value |
|---|---|
| Current phase | **post-chunk 4** — re-walk Mulan, then F1–F5 |
| Status | **Chunks 1–4 done**; branch green, unmerged to `main` |
| Branch | `dsl-sidequest` (off `main` @ `0095106`) — `main` untouched, nothing pushed or merged |
| Gate | `pnpm verify` **green 2026-11-11** — engine **393 passed / 1 skipped**, website **54/54**, both builds. SQL gate `just verify-db` **green**: probes **27 + 7 + 2 + 3 + 5**, `check-db` **6/6**. CI enforces both on every PR and branch push |
| Plan | `PLAN.md` — what to build |
| Run contract | `EXECUTION-DOD-2026-11-09.md` — branch, gate, decision policy, tools |
| Target DB | `evolution-engine` (`rkcptsghxovoeaycabah`, Sydney) — **29 migrations (`00001`–`00029`)**; parity re-proved per migration; `engine/.env.local` points at it |
| Public DB | old project `ejdenhlpvtldiljxawtd` — untouched until cutover |
| Public flow-ons | `PUBLIC-WRAP.md` — no new rows from chunks 1–1d (`public-sweep: none`) |
| Soft content | **Manual** (ruling 27) — brief in `evolution/legals/legal-foundation/soft-content-guide.md`; guide + Mulan prose committed in content `0b59d75`; U16 prefill patch parked |
| Execution | Claude Code harness · DeepSeek V4.1 Flash (Ollama Cloud) · agent mode |
| Audit | `kimi-code` (Ollama Cloud), one per chunk diff — the **single** auditor; Gemma is not run in addition (2026-11-10) |
| Public wrap | deferred to its own integration review (`PUBLIC-WRAP.md`) |

## Rulings

1. **Standalone** — outside the v2 build rules; no `OUTCOME.md` / `PLAN.md`
   reconciliation until merge.
2. **Admin only** — profile content is a private store for later use.
3. **H3** — the DB trigger is authoritative, with guards on the referenced tables.
4. **H4 / P1** — wholesale is private; the 100% total is dropped.
5. **U3** — all six profile fields, migration `00019`.
6. **U7** — two-way price entry; retail stays a whole dollar, rounded up.
7. **U11** — create/edit is a 4-step panel ending in the term sheet with
   Confirm / Edit / Close.
8. **U12** — horse-only create is in scope.
9. **U14** — the four PDS soft slots get their own structured editor; the term
   sheet stays hard and locked.
10. **Link model (re-ruled 2026-11-10)** — one **profile** per real-world
    person or company (`parties`), with roles ticked on it (`party_roles`:
    `trainer`, `owner`, extensible). Shared fields live once; the trainer block
    and owner block render by role. The **DSL is the only place a deal links
    them**: `dsls.horse_id`, `dsls.trainer_id`, `dsls.owner_id`, each pointing
    at a horse or a party holding the required role. Records pages show the link
    as a **derived view** and never author it. Horses stay assets, not profiles.
    No `horse_owners` table and no second link table. Trainer may be blank while
    Coming Soon and is required before Available, exactly like the owner.
11. **Strict SSOT** — Records own entities; `/dsl` attaches ids and writes
    `dsls` only.
12. **Three stages** — Records → DSL → Ledger.
13. **Completion is manual** — operator closes a term from the ledger; no cron;
    early close allowed; expired terms surfaced first.
14. **Headless drafting** — copy the brief out, paste suggestions back; the
    engine never calls a model. Approval hash kept as a record, not a lock.
15. **Trainer change** — edit the trainer on the **DSL**; new documents use the
    new trainer; sold documents never change or reissue; investor notice is
    manual. Records shows the new link immediately because it is derived.
16. **Stage 1 edits flow through** — non-empty edits feed live DSLs; locking is
    at the sale. Only blanking a required field (or a bio-less trainer) is refused.
17. **Trainer row = company + names** — the form asks Company name and one or more
    Trainer names; the store keeps **one row per company**, names joined `' & '`,
    because a horse attaches to a single `trainer_id` and the PDS prints
    `trainer.name`. Separate rows would drop names from documents.
18. **Links are a raw registry** — one URL per row, stored as given, label is the
    hostname. No fetching, no title reading, no rewriting. Headless drafting is
    the operator's job.
19. **Social renders as a handle** — `socialHandle` (X, Twitter, Instagram,
    Facebook) shows `@handle`; the full URL stays in the link and its title.
20. **Trainer/owner Edit uses the horse pattern** — a top-right Edit link to a
    dedicated `/[id]/edit` route, same breadcrumb and heading; no inline form at
    the foot of the profile.
21. **Dev servers get their own cache** — `NEXT_DIST_DIR` selects the build
    directory so a `next build` cannot rewrite a running `next dev`'s chunks.
22. **Roles are relationships, not permissions** — a role says what a profile is
    to a deal, never what it may do in the app. Auth stays Cloudflare Access.
    Unticking a role that a live DSL references is refused, never cascaded.
23. **A horse may hold several DSLs** (2026-11-10) — different expiries,
    commercials and owners. Pin 3 is retired: `saveDsl` no longer refuses a horse
    with an existing deal. **One dateless draft per horse** (partial unique index
    in `00022`); dated terms are unlimited. The **100%-listed cap is a manual
    operator check owned by the founder**, not a DB constraint, surfaced in the
    wizard step. A deal is identified
    `Horse | Price | Investor Return % | Expiry` (`Mulan The Brave $60 75%
    Jun2028`); the `/dsl` list reads Horse · Price · Investor · Investor Return
    % · Expiry · Status.
24. **Investor vocabulary (2026-11-10)** — admin surfaces speak only of the
    **investor return**; owner retention is assumed and never displayed. A
    **listed** DSL (`available` / `fully_allocated`) always carries a start and
    an expiry; a draft may be dateless, and readiness refuses Available without
    dates. The legal templates keep their full split wording.
25. **One date on the DSL: Expiry (2026-11-10)** — creation asks only for the
    **expiry month**, stored as its last day; the expiry is fixed. The **term
    start is the month the investor buys**, stamped per sale, so the duration
    shortens every month that passes. The investor's initial payment covers five
    months (3-month deposit + the current month + one month in advance), so a
    purchase with **five months or fewer remaining is a one-time payment**. No
    refuse/switch rule: the sale prices the remaining months. `term_start` is not
    a listing property; **readiness requires expiry only**. The **term sheet shows
    Duration** = current month → expiry, recomputed on every view, never stored.
26. **Images never block a listing (2026-11-10)** — images are marketing, not a
    legal precondition; the PDS/SA carry none. Readiness and the Available trigger
    ignore `image_count` (`00023`). Images are authored on the horse's Records page
    and flow through; the public card shows a templated "images coming soon"
    placeholder while the folder is empty. H6 moves to `00024`.
27. **Soft content is manual (2026-11-11)** — the operator writes the three horse
    blocks on the horse's Records page (**Soft content** section) and the trainer
    bio on the trainer's party record. The drafting wizard is a later follow-on.
    The authority is `evolution/legals/legal-foundation/soft-content-guide.md`.
    The v1 prefill remains a draft path until U16 lands.
28. **Break clause (2026-11-11)** — two owner triggers, one per listing: 14-day
    notice (Case B, default) or 3× remaining-lease-value buyout (Case B1). Stored
    as `dsls.close_style`; the PDS and the SA both print the matching block, and
    the SA states the settlement for both payment models. Authority:
    `evolution/legals/legal-foundation/break-clause.md`.
29. **Two SSOTs (2026-11-11)** — the structured investment row is the operational
    SSOT; the executed PDS/SA is the legal SSOT and wins on conflict. Hashes bind
    the two. A DSL is a contract series; the cap table is derived, never stored.
30. **Horse percentage points only (2026-11-11)** — stakes are stored, transmitted,
    contracted and displayed in points of the horse. Contract percentage is
    derived display only: never stored, never printed in the PDS/SA, never used
    in a calculation. Every "100%" names its scope.
31. **Founder owns external capacity (2026-11-11)** — the system is authoritative
    for executed investments and documents; the founder is authoritative for
    horse capacity and external owner terms in v1. Ledger views report **known
    system exposure**, not a complete horse cap table, and say so.
32. **Chunk 4 is locked tight (2026-11-11)** — the ledger, the sale snapshot, the
    sale-time start, the close guard, the cap-table identity and append-only sales
    land now. Contract
    ID, the post-sale term freeze, the external legal archive, offsite backups and
    the recovery drill are **F1–F5**, after the chunk. The email is a link, not a
    copy: recovery is database-only until F3.
33. **Closed means inactive (2026-11-11)** — a row with `closed_at` set is
    inactive whatever its status. Every active-row predicate excludes it: the
    dateless-draft index (`00028`), readiness and listing queries. A draft closes
    in place (`00027`).
34. **A closed row is immutable (2026-11-11)** — the `dsls_closed_immutable`
    trigger refuses every update to a row with `closed_at` set. Resuming an
    archived draft means creating a new one; `00028` allows it. `updateDsl`
    returns a readable reason before the database.
35. **The horse-level 100-point cap is dropped in v1 (2026-11-11)** — no
    system-enforced ceiling. The founder manages the sum externally alongside
    owner terms and inventory, because the system cannot see external deals.
    The ledger reports known system exposure. Follow-on: remove the wizard's cap
    copy (`DslWizard.tsx:530`) and the operator-check wording (`dsl.ts:362`).

## Chunks

Done: **1** (`8b6baf4`) · **1b** (`e30e50c`, audit PASS) · **1c** (`82a702d`,
audit PASS) · **1d** (`2bccb1b → d387225`, gate-green) · **2** (`e1f12f9`,
audit PASS) · **3** (`73f65bb`, merged `3dfdac6`, audit PASS).

The remaining chunks are **LOCKED 2026-11-10**. Their contents do not change
without a ruling; work lands in this order, one chunk at a time.

### Chunk 2 — Harden the engine · DONE 2026-11-10 (`e1f12f9`, audit PASS)

DoD: **no write path can produce an incomplete, illegal or partially-saved
listing.** The rules hold whatever the source, in TS *and* in SQL.

1. **P0 — one profile, roles.** Merge `trainers` and `owners` into `parties` +
   `party_roles` (`trainer`, `owner`, extensible). Shared fields live once —
   name/entity, contact, location, website, bio, achievements, other, socials,
   links; the trainer block (company + people names) and owner block render only
   when that role is ticked. `/trainers` and `/owners` become filtered views;
   each profile's edit page ticks roles ("Add as an owner" / "Add as a
   trainer"). `dsls.trainer_id` and `dsls.owner_id` become FKs to
   `parties(id)`; a write is refused unless the party holds that role.
   `00021` copies existing rows into `parties` with the matching role, then
   drops the old tables. No compatibility views, no dead columns.
2. **H2 — status is a machine.** Encode `coming_soon → available`,
   `available → fully_allocated`, `available → coming_soon`,
   `fully_allocated → completed`, `available → completed`, plus the two legal
   non-transitions: no-op (`from === to`) and initial (`null → coming_soon |
   available`). Refuse the rest. TS `checkStatusTransition` and the `00021`
   trigger must agree. Completion stays manual (ruling 13).
3. **H1 — the DSL writes one table.** `saveDsl`/`updateDsl` accept `horseId`,
   `trainerId` and `ownerId`; delete `resolveTrainer`, `resolveOwner`, the horse
   insert and the four-table path. One `dsls` write at Confirm. A failure leaves
   zero rows.
4. **H3 — readiness cannot be cheated.** Guard triggers on `parties`,
   `party_roles`, `horses` and `dsls` re-check every dependent Available DSL,
   including a role untick (refused, never cascaded) and a `dsls.trainer_id`
   change. Non-empty edits flow (ruling 16). The same `00021` adds
   `narrative_signoff jsonb`, `narrative_approved_at`,
   `narrative_approved_hash`; the Available trigger requires all four slots
   approved.
5. **H4a — wholesale is private.** Admin surfaces stop quoting the 100% total;
   the column drop waits for P1.
6. **U2 — `/dsl` list reads as a contract:** Horse · Price · Investor · Return
   % · Expiry · Status. Horse joins page-side; Price is retail per 1%/month;
   Investor is the **buyer** (blank until a sale exists — the ledger joins it in
   chunk 4); Return % is the investor split; status in plain words
   (done 2026-11-10, `0d912d9`).
7. **R1 — Records shows the link, never authors it.** Remove the trainer from
   `HorseForm`, `/horses/new`, `/horses/[id]/edit` and `updateHorseAction`; the
   horse profile and `/horses` derive the trainer through its DSL; `/trainers`
   and `/owners` are role-filtered views of `parties`. Zero writes here.

Pins inside this chunk: Pin 1 (`stake_remaining` set when null, never reset),
Pin 3 (existing ids accepted), Pin 4 (matrix includes no-op and initial).

Gate: `pnpm verify`; psql parity local ↔ hosted; an unapproved DSL is refused
`available` **by SQL**; the status-matrix test over every `from × to` pair;
Records pages show the DSL's trainer while `horses` no longer stores one.

**Delivered 2026-11-10 (`e1f12f9`, audit PASS).** `parties` + `party_roles`
replace `trainers`/`owners`; status matrix in TS and the `00021` trigger agree;
one `dsls` write; four readiness guards; narrative sign-off columns; horse
authoring loses the trainer; admin stops quoting the wholesale total. Gate
345/54 with both builds; **18 SQL probes**; parity **326/326**; hosted DB
migrated to `00021`; dead `TrainerNames.tsx` removed. The break clause is
`dsls.close_style` (ruling 28): it **has** a column, the PDS prints the matching
block, and the SA still lacks the branch.

### Chunk 3 — Deal assembly · DONE 2026-11-10 (`73f65bb`, merged `3dfdac6`, audit PASS)

DoD: **an operator can create and edit a deal without getting lost, sees it
before committing, and the documents derive from what was stored.**

1. **U4 — term sheet one-pager.** The internal term sheet: existing numbers,
   better hierarchy, plus owner contact, trainer stable, horse facts, image
   count, slug and readiness gaps.
2. **U7 — two-way price entry.** Wholesale or retail; the other derived; retail
   stays a whole dollar, rounded up; refuses where no whole-dollar wholesale
   reproduces the retail.
3. **U11 — the four-step create/edit panel.** Parties → Commercials → Terms →
   Narrative, ending in the term-sheet **Review** (the Review is the popup, not a
   step). Step 1 selects horse, trainer and owner from existing records; one
   atomic `dsls` write at Confirm; Confirm / Edit / Close. No entity authoring.
4. **U14 — soft content, re-ruled 2026-11-10.** Records own the base text: the
   horse profile gains one **Soft content** section with three horse slots
   editable in place; the trainer bio shows read-only with a link to its edit
   page. The wizard's Narrative step prefills all four; **only the three horse
   slots are overridable**, kept as deal-local text on `dsls`, never written back.
   The trainer bio always resolves from the party. Untouched slots follow Records
   live; an overridden slot shows one dismissible warning when its source changes.
   **One resolver** (`resolveNarrative`) is imported by readiness, the compiler,
   the term-sheet preview and the editor; SQL mirrors the fallback. *Copy the
   drafting brief*; sign-off lives on the deal and hashes the resolved texts.
5. **U10 — draft PDS/SA.** The existing `/dsl/[id]/legal` gains the
   **DRAFT — not executed** banner and the blocking-field list on refusal.
6. **Migration `00022`.** Three text columns on `dsls` + `narrative_override_meta
   jsonb` (source/dismissed hashes, keys constrained to the three) + the
   `party_roles.role` check. **H6 moves to `00024`.**

Pins inside this chunk: Pin 1, Pin 2 (Coming Soon may have no owner; Available
still requires one).

Gate: `pnpm verify`; a full step-1→Narrative walk ending in the term-sheet
review; an override that survives a Records edit plus its one-time warning; a
rendered draft PDS/SA; a two-way price round-trip; parity for `00022`.

### Chunk 4 — Ledger · DONE 2026-11-11 (`be5b3d4`, merged `72d7335`, audit 12/12 PASS)

DoD: **a sold term is visible, closable and immutable.**

1. **U15 — ledger.** Upgrade the read-only `/sales` page: per-DSL cap table
   (listed, sold, open holds, remaining, revenue, term end), investor rows with
   the frozen PDS/SA and hashes, manual close.
2. **U18 — sale snapshot (snapshot only).** `sales` stores the executed terms:
   both price columns, `investor_split`, `listed_stake`, `min_stake`, `step`,
   `end_date`, `payment_model`, `close_style`, `distribution_schedule`, and the
   parties at sale. **The ledger reads the snapshot.** The live DSL may drift
   until F2; no post-sale guard in chunk 4; ruling 15 governs edits.
3. **U19 — close guard.** `closed_at`, `closed_reason`, `closed_by`; sweep stale
   holds, then refuse close while any `open` or `paid_unfulfilled` checkout
   exists — held **or** returned, because money was taken without a sale.
4. **U20 — invariant and fixture.** `listed = sold + open holds + held
   paid_unfulfilled + remaining` in horse points. **`00024` adds**
   `checkout_sessions.stake_returned_at timestamptz`: null = stake still held;
   set = release or expiry returned it; a `paid_unfulfilled` row counts only when
   null. Synthetic fixture through the real reserve → sale path.
5. **U21 — sale-time start.** Start = first day of the buyer's month;
   `remaining = termMonthsBetween(start, end)`; effective model is `upfront` when
   the listing is upfront or `remaining <= 5`, else `subscription_float`; price
   the remaining months, compile with that start, store `term_start`, `term_end`,
   `term_months`, `payment_model_at_sale` on `sales`. `dsls.term_start` stays
   unwritten; add `isListableDsl`.
6. **H6 — append-only.** `00024` adds `record_sale_atomically`: idempotent by
   `stripe_session_id`, row locks, amount/currency/hold validation, snapshot,
   hold claim, DSL update and checkout completion in one transaction; expired or
   short → no sale, `paid_unfulfilled`, founder alert. No delete path. Then
   refuses update/delete/truncate and revokes `UPDATE/DELETE/TRUNCATE`.
7. **Verification — buyer email.** Confirm MyStable serves the stored frozen
   bytes, not a recompile. Fix is a follow-up if not.

Gate: `pnpm verify`; a ledger walk over the fixture; the cap-table identity in
horse points; update, delete and truncate on `sales` refused; close refused with
an open or paid-unfulfilled hold; a dateless listing sells with the correct start
and remaining months; the email served the frozen bytes. ~10–12 h.

**Delivered 2026-11-11.** `00024` (sale snapshot, sale-time start, close columns,
`stake_returned_at`, `record_sale_atomically`, append-only guards) and `00025`
(checkout-session grants), applied local and hosted. Gate 390/54; probes 27/27; the
local fixture sold a dateless listing (`termStart 2026-11-01`, 20 months,
`subscription_float`). `deleteSaleById` is gone. Audit 12/12 PASS. **One
verification is open:** MyStable's frozen-byte rendering.

**Images, sale path included (2026-11-11, `81b5f5d`).** The checkout bucket
check is removed — ruling 26 now holds end to end. No generic placeholder: the
gallery shows only real images and stays blank until they are added.

**P0 follow-up fixed 2026-11-11 (`014ad4b`).** `00026` adds
`resolve_paid_unfulfilled`; `close_dsl` counts only **unresolved** exceptions;
the ledger shows each one with a Resolve form and hides Close until it is clear.
Resolution returns any held stake and records who, when and why. Probe **7/7**;
gate **393/54**.

**Follow-up register (F1–F5):** contract ID printed/indexed; post-sale term
freeze; external legal archive + manifest; offsite backup + restore drill;
recovery test. **D1 is deferred, not resolved:** the email is a link, not a copy,
so recovery is **database-only until F3**.

### Not chunks of this quest

The rename and its R2 image move (S1), and the public wrap (P1–P3), are one
separate follow-on integration review. So are auth, public pages and any v2 doc
reconciliation.

## Target DB — evidence (2026-11-09)

| Check | Result |
|---|---|
| Project | `evolution-engine`, ref `rkcptsghxovoeaycabah`, **Oceania (Sydney) `ap-southeast-2`** |
| Engine DB | PostgreSQL 17.11, direct IPv6 `:5432` reachable from WSL |
| Replay | `00001`–`00019` applied in filename order, all ok, no errors |
| Zero rows | `dsls` 0 · `horses` 0 · `trainers` 0 · `owners` 0 · `accounts` 0 · `sales` 0 · `checkout_sessions` 0 |
| Parity | 171/171 manifest lines identical vs local — tables, columns, triggers, functions (md5 of definition), policies, anon/authenticated/service_role grants, indexes, enums |
| Credentials | `~/.secrets/new-supabase.txt` (mode 600) — **not** in any repo; pre-cutover env backed up to `~/.secrets/engine-env-local.precutover.bak` |
| Cutover | `engine/.env.local` → new project (legacy JWT `service_role`, not the new `sb_secret_` format) |
| API check | PostgREST `GET /rest/v1/horses` with `service_role` → `200 []`; `dsls` → `200 []` |
| Migration history | **recorded 2026-11-09** via `supabase migration repair --status applied 00001…00020`; `supabase db push --dry-run` → *Remote database is up to date* |
| RLS | on for all 7 tables; 6 SELECT policies (horses/dsls/owners/trainers public, accounts/sales read-own); `checkout_sessions` has none → service_role only |
| Function grants | the 5 SECURITY DEFINER functions are not executable by `anon`; only the 3 SECURITY INVOKER validators are |
| Open | no backups (free tier); `TRUNCATE,TRIGGER,REFERENCES` remain granted to anon/authenticated by Supabase default |

The first parity run reported "IDENTICAL" on two **empty** manifests (an `oid`
ambiguity, then a `UNION`/`GROUP BY` error). Both were caught and fixed; the
recorded result is from a run with 171 real lines on each side.

## Chunk 1 — what landed

- **U13** — console theme tokens (`engine/src/app/globals.css`), Inter / Fira Code /
  Libre Baskerville roles, shared form primitives (`_components/forms.tsx`), light
  sweep: `border-black` 10 files / **34** hits → token hairlines. Guard rule added
  to `scripts/assert-design-tokens.sh`, proven RED against a probe file and GREEN
  after the sweep. (34 is the correct baseline count — `git grep -c border-black
  0095106 -- engine/src` = 10 files / 34 hits; an earlier note here said 36 — most
  likely a mid-sweep count that included the probe file.)
- **U8** — Home first in the sidebar; `/` indexes Horses → Trainers → Owners.
- **U1** — `/horses` tile grid: image or image count, name, registration badge,
  slug, trainer, link to the profile.
- **U9** — `/horses/[id]`: identity, registration, trainer, owner derived through
  the DSL, image count/gallery, attached DSLs.
- **U12** — `/horses/new`: horse-only create, optional existing trainer, loveracing
  load, race-record JSON; lands on the profile. `NewHorse.trainerId` widened to
  `string | null`; `toHorse` now maps null correctly (`strOrNull`).
- **U3** — migration `00019_trainer_owner_profiles.sql` adds `achievements`,
  `other`, `x_url`, `facebook_url`, `instagram_url`, `links jsonb` to `trainers`
  and `owners`; types, Supabase mappers/columns, create/edit forms and profiles
  use the fixed order Profile → Achievements → Other → Social → Links.
  Applied locally with `supabase migration up --local`; psql parity confirmed both
  tables carry the six columns, `links` defaults to `'[]'::jsonb`.
- **Functional proof** — a browser walk created a probe horse (slug derived,
  trainer null, image 0) and a probe trainer with all six fields stored, including
  `links` as a jsonb array; both probe rows deleted afterwards.
- **Screenshots** — `/`, `/horses`, a profile and `/horses/new` at 1440×900 and
  390×844. Fixed a mobile grid blowout on `/` found during that pass
  (`min-w-0` / `overflow-hidden` on the card grid and cards).
- **Public sweep: none** — `website/src` untouched; the public site reads neither
  `trainers` nor `owners`, and the migration adds no projected column.

## Audit disputes (chunk 1)

Gemma 4 31B returned **FAIL**, with one FAIL and two WARNs. Both substantive
findings were checked against the code and are false; no code change was made, per
the decision policy (a FAIL the driver believes is wrong is recorded, not fixed).

1. **FAIL — “DSL save blanks Records profile fields”** (`dsl.ts`, diff lines
   2475 / 2498). False. `resolveTrainer` / `resolveOwner` pass a five-field patch
   (`name, stable, location, website, bio`) that contains **no** profile keys.
   Both stores treat the patch as partial: the Supabase path builds columns through
   `defined()`, which drops `undefined` keys, and the in-memory path spreads the
   patch over the existing row. Proof added as a regression test in
   `engine/tests/dsl-save.test.ts` (“the Records profile fields survive a DSL
   save”): all six fields on a matched trainer and owner survive `saveDsl`.
2. **WARN — “createHorseAction allows blank required fields (regex gap)”**
   (`records/actions.ts`). False. The guard is
   `if (sex === '' || colour === '' || sireName === '' || damName === '')`, so
   **any** blank field fails, not only all four.
3. **WARN — `trainerId` empty string mapped to null** — the audit itself marks
   this correct; it only calls the mapping implicit. No change.

## Chunk 1b — what landed (2026-11-09)

- **Barn name** — migration `00020_barn_name.sql`: `horses.barn_name text`, optional,
  display-only, applied to local **and** the Sydney project (columns parity 101/101).
  Form field on `/horses/new` with the law's warning; a value equal to the legal name
  (case-insensitive) is stored as null, never refused.
- **loveracing load works** — the parser was rewritten against the real markup
  (`<h2 class="horse-name">`, `<strong>Label:</strong>`, the unlabelled `Bay Filly`
  line). The fetch no longer uses `fetch`: `engine/scripts/loveracing-fetch.py`
  fetches through `curl_cffi` TLS impersonation and the loader reads it back over
  stdout. Both URL shapes work — `/Breeding/{id}/…` and `/stud-book/{id}/…` return
  the same bytes; the loveracing id is read from the URL; a life number marks the
  horse registered; the race record comes back empty rather than guessed.
- **Naming law** — `slugFromLegalName` now drops the parenthetical country suffix
  (`Mulan The Brave (NZ)` → `mulan-the-brave`), and `slugFromUnnamed` implements
  `sire-x-dam-yr` with the year required.
- **Evidence** — gate green: engine **343/343**, website **54/54**; 36 tests across
  the parser, the guard and the slug; live load through 3001 with a `/stud-book/`
  link prepopulated every field on the form.
- **Audit** — gemma PASS, no FAIL and no WARN (diff `/tmp/chunk-1b.diff`).
- **Not done** — the performance/race content (Performance Profile page); the
  unnamed-horse path is implemented and tested but the form still requires a legal
  name.

## Chunk 1c — what landed (2026-11-09)

- `/horses/[id]/edit`, prefilled, with `updateHorseAction`; Edit link on the profile
  header. The trainer and barn name are now authorable after creation (ruling 15).
- The horse form is extracted to `horses/_components/HorseForm.tsx`, shared by add
  and edit, so the two cannot drift.
- The slug is fixed on edit — a rename is a migration, not an edit (naming law §7).
- Evidence: gate green engine **343/343**, website **54/54**; `/horses/[id]` and
  `/horses/[id]/edit` both `200` with Mulan's fields prefilled.

## Chunk 1d — what landed because it was needed (2026-11-10)

Work found necessary while exercising the Records screens after 1c. It is on the
same branch, gate-green, and **has no separate audit pass** — the next audit
(chunk 2 diff) reviews it too.

1. **Profile headings deduplicated** — Profile, Achievements, Other and Links
   rendered a group legend and a field label with the same text. Social keeps its
   group heading because its three fields have distinct labels.
2. **Trainer = company + one or more names** (`TrainerNames.tsx`, ruling 17) —
   Company name plus Trainer name rows with **+ Add another trainer**; stored as
   one row with names joined `' & '`, split back into boxes on edit. Verified
   against the hosted DB with a probe row, then deleted.
3. **Links are a plain registry** (`LinkRows.tsx`, ruling 18) — one Link input,
   **+ Add another link**, Remove; raw URL stored as given; `label` is the
   hostname. The title-reading route was removed with its feature.
4. **Social handles + locked Edit pattern** (`lib/social.ts`, ruling 19/20) —
   X/Twitter/Instagram/Facebook URLs render as `@handle`, full URL kept in the
   link and title; `/trainers/[id]/edit` and `/owners/[id]/edit` are dedicated
   routes with the horse profile's top-right Edit link, breadcrumb and error slot.
5. **Dev/build cache isolation** (`NEXT_DIST_DIR`, ruling 21) — a `next build`
   no longer rewrites a running `next dev`'s chunks; `.next-*/` is ignored.

## Known defects (open)

1. ~~loveracing loader cannot fetch~~ — **fixed in chunk 1b** via `curl_cffi`. The
   race content is still outstanding: the Performance Profile
   (`/Common/SystemTemplates/Modal/EntryDetail.aspx?HorseID={id}&DisplayContext=Modal01`)
   is where race record and reviews come from; the old parser is
   `evolution/engine/website/scripts/scrape-race-log.py` (`table-indepth` rows).
   Sample page: `scratch/mulan-perf.html`.
2. **No backups.** The free tier has none and this project is now the target
   authority. Needs a decision: Pro plan, or a scheduled `pg_dump` to disk/R2.
3. **Supabase default grants.** `TRUNCATE, TRIGGER, REFERENCES` are granted to
   `anon`/`authenticated` on every table. Not reachable through PostgREST, but a
   one-line `revoke` migration would close it. Optional hardening.
4. ~~**No sale fixture.**~~ — **U20 delivered it** through the real reserve → sale
   path on the local stack, labelled synthetic. Hosted stays row-free.
5. **Service-role JWT was pasted into chat.** Founders' ruling: all keys rotate in
   one batch at cutover — no revocation now.
6. **Unnamed-horse form path.** `slugFromUnnamed` is implemented and tested; the
   form still requires a legal name. Deferred until a horse without a name exists.
7. **Mumbai project** (`umxljalfbmvrocaopao`) — confirm it is deleted.
8. **Soft prefill reads registry sections, not Soft content** (U16, parked) — v1
   `engine/website/packages/legal_engine/src/soft-prefill.ts` reads `## Profile` /
   `## Pedigree`, so a generator draft cannot see the `## Soft content` blocks the
   guide writes. Manual entry is unaffected. ~15 min, v1 tree, not chunk 4.
9. ~~**SA §15 does not branch on the break clause**~~ — **fixed 2026-11-11**
   (ruling 28, `0ce9cef`). The SA now selects `sa-break-clause.<close_style>.md`
   and states both payment-model settlements. Gate green: engine 375/375,
   website 54/54; legal pack version `1.0.1`.
10. **MyStable frozen-byte rendering unverified** (O-10) — the buyer email links to
    MyStable; its artifact route serves the **v1 acceptance record** bytes
    (`/api/legal/artifact`), not the v2 `sales.pds_markdown`. Confirm the v2 copy is
    served after cutover.
11. ~~**SQL probes are not in the gate**~~ — **fixed 2026-11-11** (`221e25f`).
    `just verify-db` runs every probe against localhost only, asserts the schema
    version, takes an advisory lock, and fails on any probe row. CI runs it as
    its own job; `pnpm verify` stays DB-free.
12. ~~**`00024`/`00025` carry no rule IDs**~~ — **fixed 2026-11-11** (`221e25f`).
    Both cite their rulebook IDs; `00026` did from the start.
13. ~~**A `coming_soon` listing cannot be closed**~~ — **fixed 2026-11-11**
    (`bae753f`). `00027` closes a draft in place (status stays `coming_soon`);
    the ledger labels a closed zero-sale listing **archived**.
14. **`/sales` has no in-app auth** (deployment gate) — Cloudflare Access is the
    control. Do not expose the engine host without it.
15. ~~**`verify-db` has no CI job yet**~~ — **fixed 2026-11-11**. `ci.yml` runs
    `pnpm verify` then `supabase start` + `supabase db reset` + `just verify-db`
    on every PR and branch push, no secrets. Validated by a full local replay of
    all 29 migrations, then `verify-db: PASS`.

## Next action

Chunk 4 is merged; the sidequest's four chunks are complete. Hosted
`evolution-engine` is **0 `dsls`, 0 `sales`, 0 holds**; the Mulan horse and the
Gray party records stay.

Next: **re-walk Mulan on `:3001`** — create the DSL, approve the narrative,
publish, then sell one stake through the real path. Then **F1–F5**. Merging
`dsl-sidequest` to `main` is the founder's call.
