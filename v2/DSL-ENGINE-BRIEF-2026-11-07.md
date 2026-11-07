# DSL Engine — deep-dive brief (prepared 2026-11-07)

For the session when the founder returns. **Planning only; no code changed.**
Sources: `engine_v2/website` at `05df240`, `sandbox/v2/OUTCOME.md`, `PLAN.md`, `ALIGNMENT-2026-11-03.md`.

---

## 1. What the engine actually is

The only surface where a horse becomes investible. Four rows go in, one legal pack comes out, one public listing appears.

```
horse (facts + 3 soft paragraphs + race record + image_count)
trainer (name, stable, location, website, bio)
owner   (entity, contact, website, profile)
        ↓  assembled by the operator on the DSL page
DSL     (horse + trainer + owner + commercial terms + status + published)
        ↓  deterministic interpolation
PDS.md + SA.md  (frozen with SHA-256 at sale)
        ↓  projection
website listing
```

## 2. What exists today (verified)

| Layer | State |
|---|---|
| `saveDsl` | Writes all four rows from one call, **non-transactionally**, with an adopt-orphan recovery rule for the horse row |
| Trainer/owner reuse | Found by `(name, stable)` / `entity`; **an existing row is returned unchanged** — edits to bio, profile, location, website, contact are silently dropped (`dsl.ts:213`, `:227`) |
| Model | Trainer and owner hang off the **horse** (`00004_horses.sql:24-25`). `dsls` holds neither |
| Availability gate | Postgres trigger checks 5 things: published, split, price, registered, `image_count >= 3` |
| Compiler gate | Requires 3 horse paragraphs **+ trainer bio + distribution schedule** — a superset of the trigger |
| Website projection | Commercial terms + `slug, legal_name, registered, image_count`. No soft prose, no trainer, no owner, no race record |
| Status machine | `checkStatusTransition` takes `from` and **never reads it** — any status can jump to any other |

**The one sentence that matters:** a DSL can pass the database gate, publish, appear on the marketplace, and take money, while its PDS cannot compile. The two definitions of "ready" disagree by three fields.

## 3. Decisions the deep-dive must close

**Locked so far (2026-11-07):**

- **Model:** horse, trainer, owner are static records authored independently. **Trainer attaches to the horse** (one at a time, change propagates to live DSLs). **Owner attaches to the DSL** (a horse can have several owners, each listing their own stake).
- **No cross-DSL 100% ceiling.** The operator is trusted to list a valid stake. The 50% policy is out of scope.
- **No oversell inside a DSL.** Reserve at Checkout (decrement `stake_remaining` on session creation), 5-minute hold, cron expires overdue sessions, atomic conditional decrement at the webhook as backstop. This is purchase-workflow work, not DSL-engine work.
- **A refused buyer is told on screen**, never silently refunded: *"No stock available right now. Evolution Stables will be in touch with a new offer."* No fifth email kind.
- **Trainer change:** no system action. Sold documents stay frozen and the founder tells investors by hand. Live listings read the current trainer; new buyers compile from it.
- **One publication object:** the DSL. No horse-level `listed` flag.
- **Four visible states** = `published` × `status` × derived completeness:
  not listed · coming soon (no commercials) · coming soon (with commercials) · live.
- **Nine commercial/date columns become nullable.** Completeness is computed, never stored.
- **One readiness function** used by the `available` trigger, the save action, and the compiler. Ready = complete commercials **and** the pack compiles.
- **Edit semantics:** create resolves by natural key; edit updates by id. The DSL form needs an existing-entity picker as well as create-new fields.
- **One write surface:** the engine DSL page. The Python console is retired (moved to `_archive/engine-v2-operator-console-2026-11-07/`). No Streamlit.
- **`distribution_schedule` is free text** for MVP. The compiler prints it verbatim; nothing validates its shape. Structured comes later.
- **Rename moves the image folder.** Copy every object to the new slug prefix, delete the old, then update the slug. The claim in `OUTCOME.md` is implemented, not deleted.
- **Operator UI:** sidebar with three sections — **Records** (Horse/Trainer/Owner tiles + New), **Listings** (DSLs by row, term sheet + pre-execution PDS/SA preview), **Sales** (one row per sale, grouped by DSL, read-only). `saveDsl` takes ids; it no longer creates trainers or owners.

Each is one-word answerable. Ordered by what blocks what.

**D1 — Where do trainer and owner live?**
- On the DSL (`dsl.trainer_id`, `dsl.owner_id`) — the deal is the legal object; one horse can change trainer between deals; history preserved. Matches the stated intent.
- On the horse — one trainer and one owner for the horse's life; simplest schema; loses history; a second deal silently rewrites the first.

Founder has said: mix and match, one trainer at a time. That is the DSL option. **Consequence:** `OUTCOME.md` says the opposite ("Owner and trainer come from that horse") and must be amended, or the model reverts.

**D2 — Owner: mix-and-match or one-owner-per-horse?** Still open.

**D3 — How is "one trainer at a time" enforced?**
Two DSLs for one horse with overlapping term dates must not carry different `trainer_id`. Postgres exclusion constraint on a daterange, or a save-path check, or both.

**D4 — Two gates or one?**
Publish and Available are separate today. Proposal: **one readiness function**, called by the save path, the publish action, and the compiler. It returns the list of missing fields. Postgres enforces the subset it can see.

**D5 — What may a Coming Soon DSL omit?**
Today: everything. The horse row still needs legal name, foaling date, sex, colour, sire, dam. Proposal: those are the only hard fields before save.

**D6 — Does the operator console survive?**
`OUTCOME.md`: the DSL page is the only operator screen. The Python console is a second writer with no auth, no tests, and a dependency on `evolution/engine/content/horses`. Retire it, or declare it throwaway and forbid it on real data.

**D7 — Rename and images.**
`OUTCOME.md` says a rename moves the image folder. No code does. Either implement `CopyObject` + `DeleteObject`, or delete the claim from the outcome.

**D8 — Website content source.**
One published projection (a view or an engine endpoint) or direct table reads. Today the site reads `dsls` joined to a thin horse projection. Whatever is chosen, no page reads a table directly and no field is copied into a template by hand.

## 4. Content contract — one home per field

| Field | Home | PDS | SA | Website | Required before Available |
|---|---|---|---|---|---|
| legal_name, slug, sex, colour, breeder, foaling_date, microchip, life_number, loveracing_id | horse | yes | no | name + slug now | yes |
| sire_name, dam_name | horse | yes | no | no | yes |
| about_horse, racing_outlook_and_pedigree, race_expectation | horse | yes | **no** | no | **yes — not enforced** |
| race_record (jsonb) | horse | no | no | no | no |
| trainer name, location, bio | trainer | yes | no | no | bio **yes — not enforced** |
| trainer stable, website | trainer | no | no | no | no |
| owner entity | owner | yes | yes | no | yes |
| owner contact, website, profile | owner | no | no | no | no |
| commercial terms, investor split | DSL | yes | yes | yes | yes (enforced) |
| distribution_schedule | DSL | yes | no | no | **yes — not enforced** |
| images (`image_count`) | horse + R2 | no | no | hero + count | yes (enforced, but editable by hand) |
| status, published | DSL | context | context | yes | — |

Rule: every field has exactly one home. Nothing is retyped into a template. The website reads one projection.

## 5. What "seamless PDS/SA" requires

1. **One assembler.** `LegalPackInput` is built in exactly one function from a DSL id. Nothing else constructs it.
2. **One readiness gate.** Same function decides save, publish, and compile. Its output is a field list, not a boolean, so the operator sees what is missing.
3. **Templates are the only prose.** The compiler is an interpolator. No generation, no paraphrase, no filesystem scan.
4. **Preview before publish.** The operator sees the rendered PDS and SA, and the hash, before the listing can go Available.
5. **Frozen at sale.** The sale row stores both documents and both hashes; later edits do not touch them. Already true.
6. **A failed compile is a blocked publish, never a runtime 500.** Today the compiler can refuse at purchase time.

## 6. Build order for the DSL session

1. Decide D1–D8. Amend `OUTCOME.md` first — it is the product law and it currently contradicts D1.
2. Migration: move `trainer_id`/`owner_id` to `dsls`; add the overlap exclusion; grant `service_role` (commit `00013`).
3. One readiness function, used by save / publish / compile.
4. Fix trainer/owner update-on-edit.
5. Publish the full projection; make the website consume it.
6. Retire or fence the Python console.
7. Rename images: implement or delete the claim.

## 7. Open questions I could not close from the documents

- Is a DSL allowed to change trainer mid-term? (D3 assumes no overlap, but a mid-term change is a different rule.)
- Is `distribution_schedule` free text or structured? The compiler prints it verbatim; nothing validates it.
- When a trainer's bio is edited, an unpublished listing's PDS changes silently. Is that intended, and should the operator be warned?
