# DSL Side Quest — state

**Last updated: 2026-11-09. Chunk 1 is built, gate-green, committed and audited.**

## Position

| Fact | Value |
|---|---|
| Current chunk | **1c — horse edit** — committed `82a702d`, gate-green, audited PASS |
| Status | **Chunk 1b done; chunk 2 not started** — awaiting the founder's go |
| Branch | `dsl-sidequest` (off `main` @ `0095106`), one commit, not pushed, not merged |
| Gate | `pnpm verify` — **green**, engine **340/340**, website **54/54**, exit 0 |
| Plan | `PLAN.md` — what to build |
| Run contract | `EXECUTION-DOD-2026-11-09.md` — branch, gate, decision policy, tools |
| Target DB | `evolution-engine` (`rkcptsghxovoeaycabah`, Sydney) — **19 migrations replayed, zero rows, parity 171/171, `engine/.env.local` now points at it** |
| Public DB | old project `ejdenhlpvtldiljxawtd` — untouched until cutover |
| Public flow-ons | `PUBLIC-WRAP.md` — no new rows from chunk 1 (`public-sweep: none`) |
| Execution | Claude Code harness · DeepSeek V4.1 Flash (Ollama Cloud) · agent mode |
| Audit | Gemma 4 31B (Ollama Cloud), one per chunk diff |
| Budget | 6 working days, hard stop 9 |
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
10. **Link model** — independent records; horse has 0..1 nullable trainer; owner
    attaches per DSL; owner↔trainer derived; no `horse_owners` table.
11. **Strict SSOT** — Records own entities; `/dsl` attaches ids and writes
    `dsls` only.
12. **Three stages** — Records → DSL → Ledger.
13. **Completion is manual** — operator closes a term from the ledger; no cron;
    early close allowed; expired terms surfaced first.
14. **Headless drafting** — copy the brief out, paste suggestions back; the
    engine never calls a model. Approval hash kept as a record, not a lock.
15. **Trainer change** — edit on the horse; new documents use the new trainer;
    sold documents never change or reissue; investor notice is manual.
16. **Stage 1 edits flow through** — non-empty edits feed live DSLs; locking is
    at the sale. Only blanking a required field (or a bio-less trainer) is refused.

## Chunks

- [x] 1 — Records, Home and the form system (U13, U8, U1, U9, U12, U3) · done `8b6baf4`
- [x] 1b — loveracing load, barn name, slug law · done `e30e50c`, audit PASS
- [x] 1c — horse edit + trainer assignment · done `82a702d`, audit PASS
- [ ] 2 — Harden the engine (H2, H1, H3, H4a, U2) · ~9 h
- [ ] 3 — Deal assembly (U4, U7, U11, U14, U10) · ~16.5 h
- [ ] 4 — Ledger (U15, H6) · ~4.5 h

The rename and its R2 image move (S1), and the public wrap (P1–P3), are **not** in
this quest. They are one separate follow-on integration review.

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
4. **No sale fixture.** `sales` is empty, and chunk 4's proof is a ledger walk over
   one. It has to be created deliberately at chunk 4, before the proof.
5. **Service-role JWT was pasted into chat.** Founders' ruling: all keys rotate in
   one batch at cutover — no revocation now.
6. **Unnamed-horse form path.** `slugFromUnnamed` is implemented and tested; the
   form still requires a legal name. Deferred until a horse without a name exists.
7. **Mumbai project** (`umxljalfbmvrocaopao`) — confirm it is deleted.

## Next action

Say **go** to start chunk 2 at H2 (status is a machine).
