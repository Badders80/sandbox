# V2 alignment — 2026-10-23

Status: **proposed. Nothing executed.** This document aligns the three live artefacts —
the old build in `evolution/engine`, the new build in `evolution/engine_v2/website`, and the
10-step plan in `v2/PLAN.md` — before any further code is written. It supersedes the two open
questions at the end of `sandbox/website/README.md` and adds the track that document omitted.

**Destination (DoD).** A ratified alignment that (a) fixes the target development structure for
the website, (b) states which old-build debts steps 1–9 actually closed and which remain, and
(c) re-sequences the remaining work with named gates. Ratification = the founder accepts §7 and
`PLAN.md` is amended to match.

**Out of scope.** No code, no branch, no deploy, no data write in this pass. No change to
`OUTCOME.md` product law. No change to the old repo.

---

## 1. The answer in one page

1. **The architecture is already right; the spine is missing.** One repo, two apps, one schema,
   one migration series, one theme. That is the correct structure and it closes the old build's
   worst debts. What the website lacks is not an architecture decision — it is the
   **composition layer** and, more fundamentally, **content to compose**. The site has zero rows
   in every table.

2. **Steps 1–9 closed the structural debt, not the operational debt.** All five root causes in
   `background/FORENSIC-AUDIT.md` are answered in schema, code, and CI. But three debts are
   unaddressed and two money-correctness holes are open. Details in §3.

3. **The 10-step plan is a build plan, not a launch plan.** It ends at a preview with the buy
   path off. It never assigns the six horses, the images, the legal reference set, the
   integration proof, or the static-horse mechanism. Those are launch work, not step 10 polish.

4. **Backfill order is data → surface → wiring → visual**, not visual first. The one exception is
   the buy-flow extraction, which has no data dependency and can start immediately. Landing and
   horse-page visual work cannot be judged against a site with no horses.

---

## 2. Target structure for the new website (question 1)

### 2.1 What stays exactly as it is

| Layer | Home | Why it holds |
|---|---|---|
| Repo | `engine_v2/website` (one private repo) | One source of truth; closes the seven-repo debt |
| Apps | `engine/` + `website/` | Engine owns pricing, compiler, migrations, Stripe; website owns presentation and reads |
| Database | one Supabase schema, one migration series | No duplicate prefixes; no second tree |
| Theme | `website/src/app/globals.css` | One token home; 6a already transcribed it |
| Status vocabulary | `website/src/lib/status.ts` | One translation module; unknown value errors |
| Server boundary | `website/src/lib/engineClient.ts` | Website never prices, compiles, or holds a Stripe secret |

No structural change is proposed to any of these.

### 2.2 What the website is missing

The old site's polish lives in its composition layer. The new pages are route monoliths:

| | Old | New |
|---|---|---|
| Landing | 79-line composer + 8 sections | 444-line monolith |
| Horse page | shell + media deck + tabs + rail | 267-line page |
| Component layer | ~7,500 lines, domain-grouped | ~900 lines, flat `components/` |

The target website tree, which restores the layer without creating a second app:

```
website/src/
  app/                     thin route composers only
    page.tsx               landing: composes sections
    marketplace/page.tsx   composes grid + card
    marketplace/[slug]/    composes horse shell + blocks
    privacy/  terms/       static legal pages
    login/  mystable/      auth + sales read
  components/
    ui/                    AccordionList, CollapsePanel, FixedBg, GlowPillButton, GrassBg, LogoCarousel, badge
    sections/              Hero, About, HowItWorks, DigitalSyndication, Marketplace, Press, FAQ, OwnershipFAQ
    horse/                 media-deck, tabs, right-rail, campaign-status-block, story-block, tab bodies
    marketplace/           listing-grid, card, page-intro, detail-tabs, cta
    buy-flow/              host, ModalShell, reducer, screens/, parts/   (per website/README.md §Purchase workflow)
  lib/                     server-only data access and adapters
    listings, mystable, engineClient, supabaseRead, auth, site, status
```

Rules that make it hold:

1. **Pages compose, components render, `lib/` fetches.** No component reads the database or the
   engine. Pages adapt the read model to props at the boundary.
2. **One call site per component.** A copied component that nothing renders does not ship.
3. **Port, don't redraw.** Old markup and class rhythm are the reference; tokens are the only
   new vocabulary, and they already exist.
4. **No new packages, no second theme, no design-lab route.**
5. **Presentation branch never touches `engine/`, `supabase/`, `website/src/lib/**` data logic,
   pricing, the webhook, or behaviour tests.**

### 2.3 Backfill order

| Order | Work | Depends on | Gate |
|---|---|---|---|
| 1 | Freeze the route map, component tree, and data boundary (this document, §2.2) | — | Founder read |
| 2 | **Data spine**: six horses, trainers, owners, DSLs, media into v2 | Old content + R2 | Every horse visible on the local marketplace |
| 3 | Surface skeleton + wiring: privacy/terms, static-horse ruling, MyStable pending, horse shell | 2 | Pages render real rows; `pnpm verify` |
| 4 | Buy-flow extraction (can run in parallel with 2–3; no data dependency) | — | Behaviour tests green; no visual change |
| 5 | Visual parity: buy-flow shell → horse blocks → landing sections → marketplace | 2, 3, 4 | Screenshot gate 1440×900 and 390×844 |
| 6 | Integration proof + preview | 2–5 | Local DB triggers + Stripe test-mode walk |
| 7 | Buy Now flip → one real sale → cutover | 6 | Founder walk + real sale |

The README's original Track B put visual primitives first. That remains true for the buy flow.
It is wrong for landing and horse pages until step 2 exists.

---

## 3. Debt ledger (question 2)

### 3.1 Closed by steps 1–9

| Old debt (root cause) | Old symptom | V2 answer | Evidence | Status |
|---|---|---|---|---|
| A horse had several keys; slug→uuid maps went stale | `INVENTORY_UUID_BY_SLUG`, `LEGACY_SLUG_ALIASES`, `resolveHorseSlug` | uuid PK; microchip unique; slug unique; no alias table; no redirect table | `00004_horses.sql`; `scripts/assert-no-anti-patterns.sh:21` bans the tokens | **Closed structurally** |
| Price, stake, split were prose plus duplicates | four independent price columns; `distribution_split TEXT`; `?? 1.0`; `0.5` step; `'75'` fallback | wholesale is the only input; retail and total are generated; split `numeric(5,2)` no default with 50–85 check; required step; `effectiveMinStake` wired | `00005_dsls.sql`; `engine/src/lib/pricing.ts`; `engine/src/lib/purchase.ts:86,137` | **Closed** |
| PDS/SA had no in-repo source | `legal_engine` read `engine/content`; CI excluded it | six pinned prose files in `engine/src/templates/`; deterministic interpolator; hash check; banned-term scan | `engine/src/lib/legal/*`; `scripts/assert-legal-templates.sh` | **Mostly closed** — see §3.2 |
| Seven repos, two migration trees | colliding `00003`, `00016`, `00017`; "pushed" ≠ "migrated" | one repo; one series `00001`–`00012`; no duplicate prefix; CI asserts | `supabase/migrations/`; `package.json` verify chain | **Closed** |
| One enum mixed listed/coming-soon/buyable; tokens gated | `campaign_status`; derived `fully_subscribed`; `brand_dna` gate | `status` enum + separate `published`; one status translation module; one theme file | `00001_enums.sql`, `00005_dsls.sql`; `website/src/lib/status.ts` | **Closed** |

Fragile assumptions from the audit also closed: sire/dam are text names; `image_count` replaced
the CDN map; the refund is one sentence with no day count; the 75% special-resolution constant is
separate from the investor split; the old Supabase project is retained under the Privacy Act.

### 3.2 Not closed, or not covered by the 10 steps

| # | Gap | Evidence | Consequence |
|---|---|---|---|
| G1 | **No content beyond the pilot.** All six tables were empty; the Mulan pilot added one horse, trainer, owner, and DSL. | `psql`: `0` in every table before the pilot; `1/1/1/1` after. Migrations `00001`–`00013` applied. | The marketplace shows one card; the other five horses are absent |
| G2 | **No image pipeline beyond Mulan.** `engine/content/horses` holds 11 raw images; Mulan's three came from the old website's `public/horses/mulan-the-brave/` and are now on R2. Available needs three. | `find` count 11; Mulan `01–03` uploaded 2026-10-23 | Only Mulan currently satisfies the image requirement |
| G3 | **Legal reference set absent.** PLAN step 7 requires the Rules PDF, the three pro-formas, and the disclosure checklist in `docs/legal/reference/`. | `find . -type d -name reference` returns only `engine/src/lib/legal`; no repo `docs/` | The compiler self-audit against the NZTR checklist is not implemented; only banned-term scanning exists (`engine/src/lib/legal/compile.ts:34`) |
| G4 | **The database has never been exercised.** Tests are hermetic; no test opens a connection. | Parked row, `PLAN.md:352`; `website/tests/listings.test.ts:18` says so | Trigger behaviour, RLS, and grants are asserted from source, not proven |
| G5 | **No reservation/hold before Checkout.** The webhook re-quotes, but two in-flight buyers can both pay for the last stake; the loser is charged and gets a founder-failure email, then a manual refund. | `engine/src/lib/purchase.ts:526-558` draws down after payment; `PLAN.md:347` defers reservations | Money-flow correctness risk, not a visual one |
| G6 | **The sale `amount` is unchecked.** Old audit recommended a check against stake × retail × 5 (or the upfront total). | `00007_sales.sql` only checks `amount > 0` | A wrong amount can be written by a buggy caller |
| G7 | **Static horses have no mechanism.** OUTCOME says Prudentia, Hottathanafantasy, First Gear "stay as finished static pages". V2 has no static horse route and no rows. | No reference in `engine_v2/website` outside landing copy | Three of six horses have no home after cutover |
| G8 | **Route parity.** Old has `/privacy`, `/terms`, `/horses/[slug]/about`; v2 has none. | Old `apps/web/src/app/`; v2 `website/src/app/` | A site taking money has no privacy/terms pages |
| G9 | **Parked table is stale.** `effectiveMinStake` is no longer unwired. | `PLAN.md:351` vs `purchase.ts:86,137` | The plan understates what is done and hides what is not |
| G10 | **Launch operations unassigned.** Email vendor, observability, Vercel projects, production Supabase, Search Console, DNS, old-data retention. | `PLAN.md:345-346`, `:322-328` | Step 10 cannot complete without them |
| G11 | **Service role had no table privileges.** The operator surface could not read or write any table. | Found 2026-10-23 saving through `/dsl/new`: `horses: permission denied`. Fixed by `00013_service_role_grants.sql`. | Hermetic tests could never see it; the engine now needs a real-DB gate |
| G12 | **Server-action upload cap was 1 MB.** Every camera-resolution hero failed. | Found 2026-10-23: `Body exceeded 1 MB limit` on a 1.1 MB image. Fixed in `engine/next.config.ts` (15 MB). | Any horse image above 1 MB was unuploadable |
| G13 | **Slug derivation keeps the country suffix.** | Mulan saved as `mulan-the-brave-nz`; the old public URL is `mulan-the-brave`. No redirect table by design. | URL change at cutover; founder must accept or change the derivation |
| G14 | **The loveracing.nz loader returns 403.** | Tried through the engine on 2026-10-23. | The registered-horse path cannot load; typing by hand works |

**Direct answer to "have we solved the DB for horse information?"** The *shape* is solved:
one `horses` row per horse keyed by uuid, a unique microchip and slug, trainer and owner as their
own rows, DSL as a separate row, price derived, split constrained, prose limited to three
columns. The *contents* are not: there is not one horse row in the database, and there is no
script or step that puts one there.

---

## 4. Re-sequenced programme

Four tracks, not one linear step list. Only the ordering rules are hard.

### Track A — Data spine (new; runs first)
- Source facts from `evolution/engine/content/horses/` (profile front matter, pedigree, race
  record) and the old Supabase export for commercial terms.
- Enter through the engine's own save path, not raw SQL, so slug derivation, uniqueness, and
  the availability trigger all fire.
- Process media to `{slug}/01`, `02`, … and upload to `evolution-v2-horse-images`.
- Minimum: all six horses visible; Lady Ketchikan and Mulan The Brave carry ≥3 images and can
  reach `available`.
- Gate: local marketplace renders six horses; psql row counts non-zero; trigger accepts the two
  live rows and rejects an Available row with two images.

### Track B — Surface and wiring (parallel where independent)
- Buy-flow extraction: `BuyFlowModal` → shell + reducer + screens. Behaviour identical.
- `/privacy` and `/terms`; ruling on static horses (G7).
- MyStable pending state and sale read (existing code, needs rows to prove).
- Horse page shell and blocks can start once Track A renders.
- Gate: `pnpm verify` green; behaviour tests unchanged.

### Track C — Visual parity
- Order: buy-flow shell → horse blocks → landing sections → marketplace.
- Gate: `pnpm verify`; screenshots at 1440×900 and 390×844; founder walk once at the end.

### Track D — Integration and launch
- Local Postgres proof: trigger, RLS grants, availability gate, two-step rollback.
- Stripe test-mode walk: happy path, KYC failure, Checkout cancel, webhook failure.
- Preview with `WEBSITE_BUY_ENABLED=false`; flip; one real sale; cutover; archive old app.
- Gate: scripted walk green; founder walk on preview; real sale.

**Hard ordering:** A before visual landing/horse (B's buy-flow part is exempt) → C → preview →
flip → sale → cutover. Visuals never block the money test; the money test never waits for polish.

---

## 5. Gates

| Gate | Command / owner | When |
|---|---|---|
| Unit + fence gate | `pnpm verify` at repo root | Every chunk |
| DB proof | local stack scripted walk (triggers, RLS, rollback) | Before preview |
| Buy-flow behaviour | existing tests + reducer tests | Every buy-flow commit |
| Visual record | screenshots 1440×900 + 390×844 | Per route, before merge |
| Founder walk | preview, once, on the final look | Before merge / before sale |
| Real sale | one, in live mode | The roll gate |

---

## 6. What changes in `PLAN.md`

1. **Activate Step 10.5 — Visual parity pass** with the amendment already written in
   `sandbox/website/README.md:277-280`, plus the tree in §2.2.
2. **Add Step 10.1 — Data spine.** Six horses, trainers, owners, DSLs, media. Not a step in the
   old list; without it step 10 is an empty preview.
3. **Amend step 10's definition of done:** preview requires populated rows, a scripted DB walk,
   and the Stripe test-mode walk — not just a deploy.
4. **Correct the Parked table:** remove `effectiveMinStake` (wired at `purchase.ts:86,137`);
   move the physical trigger check into the Track D gate; add G5/G6 if they are accepted as
   later work rather than fixed now.
5. **Record the two route/parity rulings** from §7 in the plan so they stop being open questions.

---

## 7. Decisions (working calls; founder may override)

These are the calls this alignment makes under the default policy. They are stated so execution
does not re-ask them.

1. **Parity depth — brand-level, not pixel.** The old components carry density and rhythm; exact
   pixel parity also imports old content mistakes.
2. **Routes — add `/privacy` and `/terms`; skip `/horses/[slug]/about`.** A site taking money
   needs the first two; the third duplicates the new horse page.
3. **Static horses — model all six as rows.** Prudentia, Hottathanafantasy, and First Gear get
   published DSL rows at `completed` (or `coming_soon` where true), so one horse-page path
   renders all six. No second static template.
4. **Data path — operator entry through the engine, not raw SQL.** Facts come from
   `engine/content`; commercial terms are confirmed by the founder; media is processed and
   uploaded to R2. This respects the "no copied business data" ruling because the copy is an
   operator action after the schema exists, not a seed that races migrations.
5. **Oversell — close the hold gap before the buy flip.** A DB-level check that
   `stake_remaining` covers the sale under a row lock is enough; full reservations stay later.
   Accepting charged-but-no-stake as a manual refund path is not acceptable for the roll gate.
6. **Amount invariant — add the insert check.** `amount` must equal the quote for that stake and
   DSL. This is the audit's Tier 1 item that did not ship.
7. **Legal self-audit — restore the reference set before the first real sale.** The templates and
   banned-term scan are good; the NZTR disclosure checklist is still required by the plan.

---

## 8. Evidence appendix

```
$ psql ... -Atc "select table_name ..."        → accounts, dsls, horses, owners, sales, trainers
$ psql ... row counts                          → horses 0, dsls 0, trainers 0, owners 0, accounts 0, sales 0
$ psql ... schema_migrations                   → 00001 … 00012 applied
$ psql ... pg_trigger                          → dsls_available_invariants, dsls_payment_model_eligibility, on_auth_user_created
$ find engine/content/horses -type f ...       → 6 horse folders, 11 images
$ find engine_v2/website -type d -name docs    → none; no docs/legal/reference
```

Last green gate: `pnpm verify` at `05df240`, CI `39536613709` (per `v2/step9-evidence.md`).
The current tree was not re-run for this document; treat its gate status as **UNVERIFIED** until
the next execution turn.
