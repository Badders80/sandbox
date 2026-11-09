# V2 realignment — 2026-11-03

Status: **proposed. No code changed.** This document reconciles what we believe
we have, what is actually on disk, the plan we should execute, and whether that
plan reaches the DoD.

## 1. Truth table

| Area | Claimed / assumed | Actual | Consequence |
|---|---|---|---|
| Steps 1–9 | Built, gated, pushed | Committed through `c3ec894`; `pnpm verify` is green on the current tree | The build spine is real |
| Visual work | Step 10.5 not started | Landing, nav, and footer were partially aligned in `87495a8` / `05df240`; horse page and buy-flow composition are still incomplete | Visual parity is partial, not a blank slate |
| Mulan pilot | Complete | Operator console, `00013`, and the upload-limit change exist only as uncommitted working-tree files; local services are down | The pilot is not reproducible from git |
| Step 10 | Ready to prepare | No preview deployment, no Vercel project link, no Stripe/email env, `WEBSITE_BUY_ENABLED=false` | Step 10 has not started |
| DSL engine | Simple management layer for horse/trainer/owner + commercial terms | Engine DSL page exists, but trainer/owner edits are not persisted; publishing does not require the PDS content; the separate Python operator console is a second writer | Content management is not yet robust |
| Horse model | Horse independent of trainer/owner | `horses` currently owns `trainer_id` and `owner_id` | The stated model and the schema disagree |
| DoD | One real v2 sale end to end | Not met | Everything below is sequencing to that gate |

## 2. DSL engine audit

### What already works

- Horse, trainer, owner, and DSL rows are separate tables.
- One save path writes all four rows and reuses trainer/owner records by stable
  identity.
- Soft prose is limited to the three horse columns the PDS needs.
- Trainer bio, owner entity, commercial terms, and the three soft slots compile
  into the legal pack.
- The retail price is derived, not typed.
- Images are numbered from the slug and `image_count` is the only image fact.
- The availability trigger enforces published, split, price, registered horse,
  and three images.

### Defects that must be fixed before the data spine

1. **Trainer/owner edits are silently ignored on edit.** `resolveTrainer` and
   `resolveOwner` return an existing row without updating `location`, `website`,
   `bio`, `contact`, or `profile`. A changed bio/profile in the DSL form is not
   saved if the trainer/owner already exists.
2. **Publishing does not require legal completeness.** A DSL can be `available`
   and published with missing horse prose, trainer bio, or distribution
   schedule, while the PDS compiler refuses those fields. The availability gate
   and legal compiler disagree.
3. **The website does not consume the content the engine manages.** The public
   `LISTING_SELECT` fetches only id, slug, legal name, registered, image count,
   and commercial terms. Soft prose, trainer, owner, race record, and
   distribution schedule are absent from the website projection.
4. **There are two operator surfaces.** `OUTCOME.md` says the DSL page is the
   only operator screen. The Python console is a second screen with a direct
   service-role write path, no tests, no auth, and a runtime dependency on the
   old engine content directory.
5. **Rename does not move the image folder.** The edit page says a rename moves
   the slug and image folder, but the code only updates `horses.slug`; there is
   no R2 copy/move operation.
6. **Horse save is not transactional.** The four rows are written as separate
   statements. An abandoned save can leave partial rows; the current recovery
   contract only covers the horse/DSL case.
7. **The model is inconsistent.** The schema attaches trainer/owner to the
   horse; the Oct 23 note describes horse, trainer, and owner as independent
   and assembled into the DSL.

## 3. Content contract

The content model should be explicit before visual work or the six-horse
backfill. Every field must have one home and a declared destination.

| Content | Home | Website | PDS/SA | Management note |
|---|---|---|---|---|
| Legal name, slug, sex, colour, breeder, sire, dam, foaling date, microchip | horse | name/slug now; facts later | yes | Horse section of DSL page |
| Three soft horse paragraphs | horse | not yet | PDS only | Required before Available |
| Race record | horse (`jsonb`) | not yet | not yet | Store now; display later |
| Trainer name, stable, location, website, bio | trainer | not yet | name/location/bio in PDS | Must update on edit |
| Owner entity, contact, website, profile | owner | not yet | entity in PDS/SA; profile not used | Must update on edit |
| Commercial terms and distribution schedule | DSL | terms yes; schedule later | yes | DSL section |
| Images | R2 + `image_count` | hero/count yes | no | Rename must move folder |
| Status and published | DSL | yes | sale context | Availability gate |

The rule: no field is copied into a template by hand, and no website page reads
a table directly. The engine owns writes; the website reads one published
projection.

### Recommended content gate

Before a DSL may become `available`:

- all three horse soft prose fields are non-empty;
- trainer bio is non-empty;
- distribution schedule is non-empty;
- investor split, price, registered horse, published, and at least three images
  are present;
- the legal pack compiles successfully from the same row.

The same check should run in the pure save path and in Postgres where practical.
This prevents a listing that can be bought but cannot produce its PDS.

### Recommended management surface

Keep one operator surface: the engine DSL page. Add a compact content matrix on
that page showing each field and whether it appears on the website, PDS, SA, or
nowhere. That gives the operator a truthful view without creating a second admin
app.

The Python operator console should be either retired or treated as a throwaway
local tool. It must not remain a parallel production write path.

## 4. The one model decision

**Option A — current schema:** horse owns `trainer_id` and `owner_id`; all DSLs
for a horse share the same trainer/owner.

**Option B — stated model:** horse is independent; each DSL references the
trainer and owner for that lease.

Recommendation: choose **Option B** if a horse can ever have more than one deal,
owner, or trainer during its life. The DSL is the legal/commercial object, so
the parties belong on the DSL. Choose Option A only if one trainer/owner per
horse is a permanent product rule.

This must be decided before backfill. Changing it after six horses and live
sales is much more expensive.

## 5. Plan to the DoD

### Phase 0 — lock the control plane

- Ratify this alignment and amend `PLAN.md` / `CONTINUE.md`.
- Decide the horse/trainer/owner model.
- Decide the operator-console disposition.
- Commit or discard the pilot slice; no uncommitted production path.

### Phase 1 — content contract and DSL hardening

- Fix trainer/owner update persistence.
- Add the content readiness gate and tests.
- Add the explicit public listing projection for the fields the website will
  render.
- Make rename image handling real or remove the claim.
- Add a transactional or compensating save path.
- Add the content matrix to the DSL page.

### Phase 2 — data spine

- Enter all six horses through the DSL page.
- Enter trainers, owners, commercial terms, three soft slots, and images.
- Prove the two live horses can reach `available`; prove the trigger rejects an
  incomplete one.

### Phase 3 — local proof

- Exercise migrations 00001–00013 against the local stack.
- Prove grants, RLS, availability trigger, legal compile, and rollback.
- Record `file:line` and database evidence.

### Phase 4 — Step 10 preview

- Two new Vercel projects, one per app.
- Preview only, `WEBSITE_BUY_ENABLED=false`.
- Render the six-horse marketplace and horse pages.
- Screenshot gate at 1440×900 and 390×844.

### Phase 5 — money rail

- Configure Stripe test keys and webhook secret.
- Configure the email sender.
- Walk quote → documents → identity → checkout → webhook → sale → emails →
  MyStable.
- Test KYC failure, checkout cancellation, webhook failure, and duplicate
  webhook replay.

### Phase 6 — bounded visual parity

- Copy the old site’s specific layout and components; do not redesign.
- Order: buy-flow shell, horse blocks, landing sections, marketplace.
- Keep the purchase path green throughout.

### Phase 7 — cutover and DoD

- Flip `WEBSITE_BUY_ENABLED` only after preview proof.
- Point the domain at the new website.
- Make one real sale.
- Verify frozen PDS/SA hashes, correct amount, MyStable visibility, and emails.
- Archive the old app; do not delete old data.

## 6. Does this reach the DoD?

Yes, but not with the current Step 10 alone.

The current plan reaches the **preview** gate. It does not yet cover:

- the six-horse data spine;
- the content readiness gate;
- trainer/owner update correctness;
- the website content projection;
- the legal reference set;
- oversell/hold protection;
- the sale amount invariant;
- the real-sale cutover proof.

With Phases 0–7 above, the path reaches the DoD. The critical ordering is:

**lock model → fix content writes and gates → populate six horses → prove local
DB → preview → Stripe test walk → visual copy → cut over → one real sale.**

## 7. Execution guardrails from the audit

- One writer, one repo, one session at a time.
- Fresh session on turn 1; quote `CONTINUE.md` and blockers.
- Binary decisions only; park everything else.
- Stage explicit paths; never broad-add a dirty tree.
- One gate command per chunk; evidence before "done".
- Executor never audits its own work; pinned auditor before and after.
- No long background audits or subagent fan-out for the critical path.
- Visual work is a bounded copy task, not an open design exploration.
- Do not strip or rewire the live site; do not mix old and new backends.
