# Step 6b-ii — The marketplace, the horse page, and the search layer (plan, revision 2)

**Step:** `PLAN.md` § "When you say build" item 6b-ii (`PLAN.md:284`). The third and last slice of Step 6,
split 2026-10-17 (`PLAN.md:272`).
**Scope:** the `website/` app, the repo-root `scripts/`, and one section of `engine/OPERATIONS.md`.
**One commit.** One conventional commit, pushed, CI green.

## 0 · Path convention, declared

Every path in this plan is **repo-root-relative** — `website/src/lib/status.ts`, not
`website/website/src/lib/status.ts`. The repo root is `/home/evo/evolution/engine_v2/website`, which holds
`engine/` and `website/` as its two apps (`PLAN.md:199`). Repo-root-relative is what `PLAN.md:284` uses,
what `git diff` emits, and therefore what a Moment 2 citation resolves against. The auditor is asked to
grade this plan's citations against that base and to hold its own citations to the same form.

## 1 · Deliverables

| # | Path | What it is |
|---|---|---|
| D1 | `website/src/lib/status.ts` | **The status translation module.** The ruled map, and a throw on anything it cannot translate |
| D2 | `website/src/app/marketplace/page.tsx` | The marketplace grid. Dynamic |
| D3 | `website/src/app/marketplace/[slug]/page.tsx` | The horse page, its `generateMetadata`, and its JSON-LD. Dynamic |
| D4 | `website/src/lib/site.ts` | The public host, the OG image, and the image-URL algebra. Pure |
| D5 | `website/src/app/robots.ts` | `robots.txt` |
| D6 | `website/src/app/sitemap.ts` | The sitemap, from the same set the marketplace lists |
| D7 | `website/src/app/layout.tsx`, `website/src/app/page.tsx` | `metadataBase`, the Open Graph image, and the landing page's Organisation + WebSite JSON-LD |
| D8 | `scripts/assert-search-layer.sh` | Fails CI if the search layer drifts or the apex host reappears |
| D9 | `website/tests/status.test.ts`, `website/tests/search.test.ts` | Hermetic tests for the map and the search layer |
| D10 | `website/tests/listings.test.ts` | **Amended, not deleted.** Three 6b-i fences are narrowed by exactly one path each |
| D11 | `website/next.config.ts`, `website/.env.example` | The R2 remote pattern, and one new env **name** |
| D12 | `engine/OPERATIONS.md` | The physical trigger check (`PLAN.md:333`) and the marketplace probe, recorded |
| D13 | `website/src/lib/listings.ts` | **Amended.** `getListingBySlug` becomes `getListingsBySlug`, returning every published DSL on a horse |

`pnpm-lock.yaml` is not expected to change. `PLAN.md:203` excludes it from the audited diff regardless.

## 2 · D1 — the status translation module

**The first deliverable, and the reason for it.** Every listing renders a status, and the database enum and
the design vocabulary do not share names. `PLAN.md:286` rules the map. `website/src/lib/listings.ts` deliberately
carries the enum raw: the header comment at `:10-13` says so and names 6b-ii as the owner of the translation,
and the enum itself is declared at `:21-26`. This file is that translation and nothing else.

**File:** `website/src/lib/status.ts`.

**The ruled map, transcribed exactly (`PLAN.md:286`):**

| DB enum | key | Label | Variant | Token the variant binds to |
|---|---|---|---|---|
| `coming_soon` | `coming_soon` | `COMING SOON` | `active` | `--color-status-active` |
| `available` | `listed` | `AVAILABLE` | `active` | `--color-status-active` |
| `fully_allocated` | `fully_subscribed` | `FULLY ALLOCATED` | `pending` | `--color-status-pending` |
| `completed` | `completed` | `COMPLETED` | `settled` | `--color-status-closed` |

**The variant-to-token binding is the founder's ruling of 2026-10-17:** variant `settled` binds strictly to
`--color-status-closed`. The binding is not an improvisation — the app-root design law states it outright.
`website/DESIGN.md:211` documents `--color-status-closed` as "Terminal — **completed**", and
`website/DESIGN.md:512` lists the status badge's variant enum as `active` · `pending` · `settled`, which is
the enum the theme file transcribes at `website/src/app/globals.css:229`. So the theme file declares three
status colour tokens named `active`, `pending`, `closed` (`website/src/app/globals.css:44-46`) while the
ruled variant enum is `active`, `pending`, `settled`. The variant name and the token name differ, and that
is expected: the variant is the design vocabulary, the token is the colour.
`website/DESIGN.md:684` calls a third colour variant "a ruling", and the founder gave it. **No new token is
created, and no token in `globals.css` is renamed** (`PLAN.md:284`, `:329`).

**The brand folder's copy is not the authority here.** `/home/evo/evolution/engine/brand/DESIGN.md:62`
gives `status-closed` as `#64748b`; the app-root copy at `:211` and the theme file both give `#738396`. 6a
compiled the theme from the app-root copy, which is the design law 6a deployed. Every `DESIGN.md` citation
in this plan is the app-root `website/DESIGN.md` unless the brand path is written out in full.

**Shape.** A pure module. One exported lookup and one exported reader:

- `STATUS_VIEWS`: a `Record<DslStatus, StatusView>` where `StatusView` is
  `{ key: DesignStatusKey; label: string; variant: StatusVariant; className: string }`.
- `viewForStatus(status: string): StatusView` — looks the value up and **throws** when it is absent.
  The throw is the whole point: `DESIGN.md` says an unrecognised value is an error rather than a fallback,
  and `PLAN.md:286` repeats it for the website ("a value it cannot translate is an error").
  A default, a `??`, an optional chain, or a `switch` with a `default:` branch is a FAIL.
- `className` is a token utility built from the bound token — e.g. `text-status-active`. No raw colour, no
  stock Tailwind palette (`scripts/assert-design-tokens.sh` enforces this on `website/src/`).
- `draft` and `coming_soon_details` appear nowhere: `PLAN.md:295` rules that neither is emitted by the
  site, and `draft` is `published = false`, an absence from the marketplace rather than a status.

**Labels are uppercase in the module** because `DESIGN.md` renders the component uppercase and keeps source
strings in sentence case. The 6b-i test at `website/tests/listings.test.ts:151-160` asserts these four
uppercase strings do not appear anywhere under `website/src/` — that fence existed to stop 6b-ii inheriting
a half-built map, and §7 narrows it to this one file rather than dropping it.

## 3 · D2 and D3 — the marketplace and the horse page

### D2 — `website/src/app/marketplace/page.tsx`

- Reads `listPublishedListings()` (`website/src/lib/listings.ts:127`). No new query shape is introduced.
- Renders one card per published DSL: the horse's `legalName`, the status badge from `viewForStatus`, and a
  link to `/marketplace/[slug]`.
- **Applies no ordering.** `PLAN.md` and `OUTCOME.md` state no marketplace sort order, so none is invented
  here — the same ruling 6b-i recorded at `CONTINUE.md:57` and pinned at `website/tests/listings.test.ts:117-121`.
  Flagged in §8 for the auditor: if an order is wanted, that is a founder ruling, not an executor choice.
- Uses only `listing-card [standard]`. The `featured` variant exists in the theme's Tier-3 comment
  (`website/src/app/globals.css:229`) but nothing rules which card is featured; inventing that is out of scope.
- `export const dynamic = 'force-dynamic'`. See §10 — this is load-bearing, not stylistic.
- Exports its own `metadata`: a title, a description, and a canonical URL (`PLAN.md:80`).

### D3 — `website/src/app/marketplace/[slug]/page.tsx`

- Reads `getListingsBySlug(slug)` — D13's plural reader, which replaces `getListingBySlug`
  (`website/src/lib/listings.ts:141-154`). It filters `published = true`, matches the horse's slug, and
  returns **every** published DSL on that horse. An empty result calls `notFound()`; an unpublished DSL is a
  404, never an empty page (`PLAN.md:284`, `:297`).
- **One `h1`**, carrying the horse's legal name (`PLAN.md:86`).
- One block per published DSL: the status badge from `viewForStatus`, and that DSL's commercial terms as
  stored — `listedStake`, `minStake`, `step`, `stakeRemaining`, `endDate`, `termStart`, `paymentModel`,
  `closeStyle`, `retailMonthlyPerPercent`, `wholesaleMonthlyTotal`. Every figure is rendered as stored and
  none is recomputed — the website never prices (`PLAN.md:282`).
- **No checkout control of any kind.** Founder's ruling, 2026-10-17: the purchase modal and the buy wiring
  are Step 8 (`PLAN.md:299`), and the buy path stays off until Step 10 (`PLAN.md:301`). An Available
  listing renders the `active` status badge and its commercial terms; it renders no button, no link, and
  no form that begins a purchase. `PLAN.md:284`'s "Available means Buy Now" is read as the meaning of the
  state, not as a control to build in this step. **A disabled or "coming soon" button is also a FAIL** —
  the ruling is no control, not an inert one.
- One sized hero image when `imageCount > 0`, via D4's algebra. When `imageCount` is 0 no image is
  rendered: inventing one is not available, and `imageCount` is the only image fact in the database
  (`OUTCOME.md:68`).
- `generateMetadata` returns that horse's own title, description, and canonical URL (`PLAN.md:80`, `:86`).
  The description is the horse's. **`investor_split` is not in the description and not on the page** —
  `PLAN.md:86` forbids copying one form's 75% across horses, and the 6b-i projection does not select it;
  adding it would be an invented disclosure. Flagged for the auditor in §8.
- **JSON-LD for the horse at `/marketplace/[slug]`**, which is the real page (`PLAN.md:85`). Type
  `Product` with `name`, `description`, `url`, `image`. **No `offers` and no price**: the law does not rule
  which figure is the public price, and `listed_stake` is a percentage (`numeric(5,2)`, ≤ 100), not money.
  Emitting a price here would be the same class of error as the retired `/horses/[slug]` pointer. Flagged
  in §8. The string `/horses/` appears nowhere.
- `export const dynamic = 'force-dynamic'`. See §10.

## 4 · D4 — `website/src/lib/site.ts`

One pure module holding the three constants the search layer and the pages both need. It reads no file,
opens no connection, and imports nothing from `engine/`.

1. **The public host.** `https://www.evolutionstables.nz` — `PLAN.md:84` rules that the apex
   `https://evolutionstables.nz` is **not** a second canonical, and names the apex as a mistake that stays
   behind. Canonicals, the sitemap, and structured data all use this host.
2. **The Open Graph image.** `/og/default.png`, which 6a already shipped (`website/public/og/default.png`).
   `PLAN.md:78` lists "an Open Graph image" once, at the site level, alongside `robots.txt` — one image for
   the site, not one per horse. 6b-ii adds no per-horse image generator.
3. **The image-URL algebra.** Public images live in one R2 bucket in a folder named from the horse slug,
   files numbered `01` upward, **no file extension** (`engine/src/lib/storage.ts:1-10`, `OUTCOME.md:68`).
   `website/` may not import from `engine/` (`PLAN.md:282`), so this module mirrors that key shape:
   `imageKey(slug, n)` → `{slug}/{NN}` and `publicImageUrl(key, base)` → `{base}/{key}`, reading the origin
   from `WEBSITE_R2_PUBLIC_URL`. Both throw on a malformed slug, a non-integer number, a key carrying a
   dot, or a base that is not an `https://` origin. There is no slug-to-path lookup and no redirect table
   (`PLAN.md:315`).

**The mirror is a duplication, and it is disclosed rather than hidden.** The engine owns the upload side;
the website owns the read side; the shared fact is four lines of string algebra. A hermetic test in D9
pins the exact output (`imageKey('lady-ketchikan', 1) === 'lady-ketchikan/01'`) so the two cannot drift
silently, and the drift is caught in this repo rather than at a 404 in production.

## 5 · D5, D6, D7 — the search layer

`PLAN.md:78-90` is the whole of the requirement. Five parts, each with its deliverable.

| Part | Home | Rule |
|---|---|---|
| Title, description, canonical per page | `layout.tsx`, `marketplace/page.tsx`, `marketplace/[slug]/page.tsx` | Landing page carries the site title; the marketplace and each horse page carry their own (`PLAN.md:80`) |
| Open Graph image | `layout.tsx`, via D4's constant | One site image |
| `robots.txt` | `website/src/app/robots.ts` | Disallows `/mystable`, `/login`, `/checkout`; names the sitemap (`PLAN.md:80`, `:88`) |
| The sitemap | `website/src/app/sitemap.ts` | See below |
| Structured data | `page.tsx` (Organisation, WebSite) and `marketplace/[slug]/page.tsx` (the horse) | `PLAN.md:80`, `:85` |

**The sitemap set, exactly as ruled (`PLAN.md:88`, `:297`).** The landing page, the marketplace, and one URL
per horse that carries at least one published DSL. "Each public horse" and "every published DSL" are the
same set. So `sitemap.ts` calls `listPublishedListings()` and **deduplicates by slug** — a horse may carry
more than one DSL, and the public URL is one page per horse. Unpublished DSLs, unregistered horses, buyer
documents, MyStable, login, and checkout stay out. Coming Soon **is** listed (`PLAN.md:88`).

**The multi-DSL horse page, and the read-layer change it forces.** `PLAN.md:297` states plainly that a horse
may carry more than one DSL, and the schema permits it — `dsls_horse_id_end_date_key unique (horse_id,
end_date)` (`supabase/migrations/00005_dsls.sql`), which is not unique on `horse_id`. The same ruling says the
public URL is one page per horse. This plan therefore has `/marketplace/[slug]` render **every published DSL
on that horse**, because discarding a published offering is the one reading the law does not support, and it
does not choose among them, because choosing would be inventing a rule.

**Revision 1 asserted that and did not deliver it.** The 6b-i read layer returns exactly one row:
`return rows.length > 0 ? toListing(rows[0]) : null` (`website/src/lib/listings.ts:153`). A page cannot render
every DSL through a reader that drops all but the first. **D13 replaces `getListingBySlug` with
`getListingsBySlug(slug): Promise<Listing[]>`** — same `LISTING_SELECT`, same `published = true` filter, same
`horses!inner` embed, same single call site — returning every matching row. The old name goes; leaving both
would strand an uncalled reader, which is the defect 6b-i already flagged once (`CONTINUE.md:54`). The
existing test imports only `toListing` and `ListingRow`, so no 6b-i assertion moves.

**If the auditor reads the law as one DSL per page, it must name which DSL is dropped and the founder
rules.** That alternative drops D13 and nothing else. The split is graded in §8.

**`robots.ts` and `sitemap.ts` are Next metadata routes**, so `robots.txt` and `sitemap.xml` are generated
from code and no static file under `website/public/` is added for either.

**Two live founder rulings are respected, not re-raised.** All nine partner marks stay on the landing page,
and the five landing dividers at `website/public/images/landing/` stay committed. 6b-ii touches neither.

## 6 · D8 — `scripts/assert-search-layer.sh`

A fifth repo-root assertion script, wired into the root `test` chain beside the four that exist
(`package.json:13`), so it blocks the gate and CI before the commit rather than after. It is a shell
script reading text. It asserts:

1. `website/src/app/robots.ts` and `website/src/app/sitemap.ts` both exist.
2. The canonical host literal is `https://www.evolutionstables.nz`, and the apex `https://evolutionstables.nz`
   appears as a canonical, a sitemap entry, or a structured-data `url` **nowhere** under `website/src/`
   (`PLAN.md:84`). A bare mention of the apex in prose is not a failure; using it as a URL is.
3. `robots.ts` disallows `/mystable`, `/login`, `/checkout`.
4. `sitemap.ts` reads its set through the read layer rather than composing URLs from anything else, and
   carries no `/horses/` path.
5. `/horses/` appears nowhere under `website/src/` (`PLAN.md:85`).
6. The marketplace and horse page both declare `dynamic = 'force-dynamic'` (§10), and `sitemap.ts` does too.
7. **An asset-path sweep.** Every `'/images/…'` and `'/brand/…'` string literal under `website/src/`
   resolves to a file under `website/public/`. 6a shipped a `.png` reference to a `.jpg` on disk and
   `next/image` takes a runtime string, so typecheck, lint and build all passed while the mark would have
   404'd (`CONTINUE.md:91-95`). All eleven references in the app resolve today; the sweep makes the twelfth
   fail here rather than in a browser.

The script is `set -euo pipefail`, prints PASS/FAIL with the offending line, and is added to
`package.json` as `test:search-layer`, appended to the `test` chain. Mirroring 6b-i's
`scripts/assert-read-policies.sh`, it is falsified at least once before it is trusted — by breaking each
assertion in turn, watching it fail, and restoring.

## 7 · D9 and D10 — the hermetic tests

**No test opens a database connection.** CI runs `pnpm run test` with no database service
(`.github/workflows/ci.yml`), so every assertion below is a pure function, a text scan, or a source fence.

**D9 — `website/tests/status.test.ts`.**
- Each of the four enum values maps to the ruled key, label, and variant, asserted as literals.
- `viewForStatus('something_else')` **throws**, and does not return a fallback. This is the item the
  `DESIGN.md` no-fallback rule turns on.
- Variant `settled` resolves to a class name built from `status-closed`, and variant `active` from
  `status-active` — the binding is a literal assertion, not a comment.
- The four uppercase labels and the four variant names appear **only** in `website/src/lib/status.ts`
  across all of `website/src/`.

**D9 — `website/tests/search.test.ts`.**
- `imageKey('lady-ketchikan', 1) === 'lady-ketchikan/01'`; `imageKey(slug, 10) === '{slug}/10'`.
- `publicImageUrl` joins an origin and a key and strips a trailing slash from the base.
- `imageKey` and `publicImageUrl` throw on: a key carrying a dot, a reserved private prefix, a
  non-integer number, and a non-`https` base.
- The sitemap set is derived from the read layer and deduplicated by slug: given two published DSLs on one
  horse, the resulting URL list holds that horse once.
- **The plurality fence.** `website/src/lib/listings.ts` declares `getListingsBySlug` and declares no
  `getListingBySlug`, and contains no `rows[0]`, no `.single()`, and no `.limit(1)`. This is the assertion
  that would have caught revision 1's defect — a plan claiming the horse page renders every published DSL
  while the reader it named dropped all but the first (`website/src/lib/listings.ts:153`).
- `SITE_URL` is the `www` host and is not the apex, asserted as a literal.

**D10 — `website/tests/listings.test.ts` is amended, not deleted.** Three 6b-i fences exist precisely so
6b-ii could not inherit a half-built map, and 6b-ii is what builds the map. Each is **narrowed to one
path**, never removed:

| 6b-i fence | 6b-ii change |
|---|---|
| `renders no status label, leaving that to 6b-ii` (`:151-160`) | Exempt `website/src/lib/status.ts`, with a comment naming 6b-ii as the owner the fence deferred to |
| `carries no status colour or design status key outside the theme file` (`:162-173`) | Exempt `website/src/lib/status.ts` alongside `website/src/app/globals.css`, for the same reason |
| `applies no ordering, because no ordering rule exists` (`:117-121`) | **Unchanged.** No ordering is added, so the fence stays true as written |

The exemption list grows from one path to two, and both exemptions carry the reason inline. **Deleting a
fence, or widening one beyond a single named path, is a FAIL.**

## 8 · What this plan does not decide, flagged for the auditor

Six points where the law is silent or a reading is being taken. Each is named here rather than settled
silently in a diff, per the step brief's instruction.

1. **Marketplace order.** No ordering is applied, because none is ruled. If an order is wanted, the founder
   rules.
2. **The multi-DSL horse page.** Renders every published DSL on that horse, per §5, which required
   extending the read layer (D13). If the auditor reads the law as one DSL per page, it names which is
   dropped and the founder rules; that alternative drops D13 and nothing else.
3. **`investor_split` is omitted.** Not selected by 6b-i, not ruled public, and `PLAN.md:86` forbids
   generalising one form's split. `effectiveMinStake` (`PLAN.md:332`) is likewise uncalled: it belongs to
   the buy path in Step 8.
4. **No price in the horse JSON-LD.** The law does not rule which stored figure is the public price.
5. **`listing-card` renders `standard` only.** `featured` exists in the theme's Tier-3 comment and nothing
   rules which listing is featured.
6. **The R2 image algebra is mirrored into `website/`**, because `website/` may not import `engine/`, with
   a drift test in D9 (§4).

## 9 · Negative constraints (each falsifiable against a diff)

- **N1** No `.from('horses')`, `.from('trainers')`, or `.from('owners')` anywhere under `website/src/`.
  Every read originates at `dsls` and embeds outward. Grep on the diff. (`PLAN.md:282`)
- **N2** Every `.from('…')` under `website/src/` names `dsls` and only `dsls`. The 6b-i test at
  `website/tests/listings.test.ts:95-111` already asserts this over all sources and stays as it is.
- **N3** No service-role key, no `SERVICE_ROLE`, no `sb_secret_`, no Stripe key or secret under `website/`.
- **N4** No new design token, no palette addition, and no edit to `website/src/app/globals.css`. 6b-ii
  reuses the 6a theme file unchanged (`PLAN.md:284`, `:329`). The variant-to-token binding of §2 consumes
  three tokens that already exist and declares none.
- **N5** No raw colour literal, no stock Tailwind palette utility, no `font-sans`/`font-serif`, no
  `text-muted`, and no arbitrary `rounded-[…]`/`z-[…]`/`duration-[…]` outside the theme file. The existing
  `scripts/assert-design-tokens.sh` scans `website/src/` and already fails on each.
- **N6** No new directory named `theme/`, `tokens/`, or `design/`, and no lookbook.
- **N7** No `AGENTS.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, or other meta-rule file created anywhere.
- **N8** No import specifier resolving into `engine/`, and no new package in `pnpm-workspace.yaml`
  bridging the apps.
- **N9** No pricing and no compilation in `website/`: `retail_monthly_per_percent` and
  `wholesale_monthly_total` are read as stored and never recomputed, and `pricing.ts` is not mirrored.
- **N10** No interactive checkout control on any page: no purchase button, no buy form, no checkout link,
  and no inert or disabled stand-in for one. Founder's ruling, 2026-10-17. (`PLAN.md:299`, `:301`)
- **N11** No status label, status key, or status colour outside `website/src/lib/status.ts` and
  `website/src/app/globals.css`, and no `??`, `default:` branch, or optional chain in `viewForStatus`.
- **N12** No `/horses/` path and no sitemap or canonical entry on the apex host. (`PLAN.md:84`, `:85`)
- **N13** No slug-to-id table and no slug-to-id lookup anywhere. (`PLAN.md:315`)
- **N14** No credential value in any tracked file. `website/.env.local` stays ignored and
  `website/.env.example` carries names only.
- **N15** No test opens a database connection and no test imports a database driver. CI has no database
  service. Database behaviour is proven by D12's recorded probe.
- **N16** `draft` and `coming_soon_details` appear nowhere in the app. (`PLAN.md:295`)
- **N17** One step, one commit, pushed once. No multi-step execution across a prompt boundary.
  (`PLAN.md:117`)

## 10 · The CI-without-environment trap, named

**This is the load-bearing technical risk in 6b-ii and it is stated here rather than discovered at the
gate.**

`.github/workflows/ci.yml` runs `pnpm run build` with **no environment variables set**, and
`website/src/lib/supabaseRead.ts:30-36` deliberately **throws** when `WEBSITE_SUPABASE_URL` or
`WEBSITE_SUPABASE_ANON_KEY` are absent. That throw is correct and must not be softened.

In 6b-ii the website stops rendering zero rows: the marketplace, the horse page, and the sitemap all read
data. Next prerenders static pages and metadata routes **at build time**, so a read during prerender would
throw in CI and take `pnpm verify` to a non-zero exit for a reason that has nothing to do with the change.
The correct answer is not to weaken the client:

- `website/src/app/marketplace/page.tsx` declares `export const dynamic = 'force-dynamic'`.
- `website/src/app/marketplace/[slug]/page.tsx` declares the same.
- `website/src/app/sitemap.ts` declares the same, because a metadata route is prerendered by default.

Each page is then server-rendered per request, which still satisfies `PLAN.md:90` — the first response
contains the horse name, the status, and the sized hero image as HTML — while the build never touches the
database. `robots.ts` reads nothing and stays static.

**D8's assertion script checks all three declarations are present.** A future edit that removes one is a
build break in CI, which is where it should be found.

**The verification is falsification, not inspection:** delete one declaration, run `pnpm build`, watch it
fail, restore it, run `pnpm build`, watch it pass. The falsification is recorded in §13.

## 11 · D12 — the physical trigger check (`PLAN.md:333`), which is this step's gate

`engine/src` references `00008_dsl_availability_trigger.sql` in prose only. No test imports a database
driver and no test opens a connection, so **nothing in this repo has ever executed that trigger**, and the
`image_count` write is wired and source-asserted rather than proven to satisfy the constraint it exists for.

`PLAN.md:333` parks the check against the local stack "before the first listing goes live", and 6b-ii ships
the first listing. **So this is 6b-ii's gate, and it is the only part of this step that touches a database.**

- Against the local stack on 544xx, with migrations `00001`–`00009` applied.
- **A fixture is seeded first, and removed last.** The database is empty, and a probe against an empty
  database returns `[]` to every question and proves nothing — the vacuous green that let the missing
  `GRANT` survive 6b-i's first draft (`CONTINUE.md:37-41`). One horse with fewer than three images and a
  DSL attempting `available`, then the same horse with three, is the shape that exercises the trigger
  both ways.
- Both directions are recorded: the write that must be **refused**, and the write that must be
  **accepted**. Only the second one is the easy half.
- The recorded output goes into `engine/OPERATIONS.md` — command, fixture, observed result, and the
  teardown that removed the fixture.
- **It stays out of `engine/tests/`.** CI runs `pnpm run test` with no database service.
- `PLAN.md:203` carries the explicit exemption for `engine/OPERATIONS.md` prose within scope-leakage
  checks.

The same recorded section re-runs 6b-i's anon probe through the marketplace's own query — that the four
public tables answer as `00009` intends — so the step's recorded evidence covers both what it added and
what it now renders.

## 12 · Non-orphan consumer wiring

Every deliverable has a consumer, and nothing is pinned ahead of need.

| Introduced | Consumer |
|---|---|
| `website/src/lib/status.ts` | Both pages, via `viewForStatus` |
| `marketplace/page.tsx` | Linked from the landing page's navigation |
| `marketplace/[slug]/page.tsx` | Linked from every marketplace card |
| `getListingsBySlug` (D13) | `marketplace/[slug]/page.tsx`, and the multi-DSL assertion in D9 |
| `website/src/lib/site.ts` | Both pages, `robots.ts`, `sitemap.ts`, `layout.tsx` |
| `robots.ts`, `sitemap.ts` | Next's metadata routes; `sitemap.ts` also named from `robots.ts` |
| `scripts/assert-search-layer.sh` | The root `test` chain, hence CI |
| `website/.env.example`'s third name | The operator, and the horse page's hero image |
| `engine/OPERATIONS.md`'s section | The operator |

**Flagged for the auditor.** `viewForStatus` throwing on an untranslatable value is unreachable from the
pages with today's data, because the database is empty and the enum has four members. It is tested
directly in D9 rather than exercised through a page. The alternative — a page-level test with a fabricated
row — would need the pages to accept injected data, which is more surface than the rule is worth. If the
auditor rejects the direct test, name the shape it wants.

## 13 · Local verification protocol

`pnpm verify` from the repo root — exit code 0, `--max-warnings=0` (`PLAN.md:202`). It runs typecheck, lint
in both workspaces, the five assertion scripts, both workspaces' vitest suites, and both builds.

Three falsifications are run and recorded before the diff is staged, each broken, watched failing, and
restored:

1. `scripts/assert-search-layer.sh` — break each assertion in turn, watch each fail.
2. The `force-dynamic` declarations of §10 — remove one, watch `pnpm build` fail, restore it.
3. The `viewForStatus` throw — replace it with a `??` fallback, watch `status.test.ts` fail, restore it.
4. D13's plurality — restore `rows[0]` in the reader, watch the plurality fence in `search.test.ts` fail,
   restore the plural return. This one is new in revision 2 and it falsifies the exact defect Moment 1
   round 1 found.

Then §11's probe against the local stack with its fixture, recorded in `engine/OPERATIONS.md`. It is a
logged manual procedure, not a CI test, and it is the only evidence in this step that touches a database.

## 14 · Audit and push gate

**Moment 1 — this plan, before a line is written.** `kimi-k2.7-code` via Ollama Cloud, headless,
stdout/stderr split, blocking wait under `timeout 900`, timeout = FAIL, verdict read from the **last
non-empty line** of `.result`, parsed as JSON and tested for equality. **Never by substring**: the returned
checklist legitimately quotes the pass phrase when it specifies the gate, and on 2026-10-17 that is exactly
how a FAIL was nearly committed as a PASS (`CONTINUE.md:75-79`). It returns the numbered checklist that
Moment 2 then grades against.

**Moment 2 — the staged diff, after `pnpm verify` exits 0.**
`git diff --cached -- . ':(exclude)pnpm-lock.yaml' | nl -ba > /tmp/step6b-ii-diff.txt`, **pre-numbered
before dispatch**, same model and protocol. Every item graded PASS or FAIL with a non-dummy `file:line`
citation; a citation that does not say what it claims fails its item. `PLAN.md:203` carries the explicit
exemption for `engine/OPERATIONS.md` prose within scope-leakage checks.

**Then:** one conventional commit, `git push origin main` from `/home/evo/evolution/engine_v2/website`
(`origin` is `Badders80/engine-v2`, never the sandbox planning repo), then `gh run watch --exit-status`.
(`PLAN.md:204`)

## 15 · Scope fence, resolved

`PLAN.md:284-297` defines 6b-ii, and this plan touches four locations:

1. `website/` — the app, its lib, its routes, its tests, its env example, its Next config.
2. `scripts/` at the repo root — where the four existing assertion scripts live and where the root `test`
   chain already looks.
3. `package.json` at the repo root — one new script and one line on the `test` chain.
4. `engine/OPERATIONS.md` — **the one location that can be read as leaking into `engine/`**, and this
   step's parked gate makes it mandatory rather than optional.

The fourth is deliberate. `PLAN.md:236` names `engine/OPERATIONS.md` as the single operator guide and
requires each step to add the click-path for what it built; `PLAN.md:203` exempts that file's prose from
scope-leakage checks; and `PLAN.md:333` parks a database check that must be recorded somewhere other than
`engine/tests/`. It is documentation, not code, and no `website/` file imports from it. **If the auditor
reads the fence as `website/`-and-scripts only, D12 drops and that is the only change** — but the trigger
check then has no home and stays parked past the first listing, which is the one thing `PLAN.md:333`
forbids.

No branch other than `main`. No `AGENTS.md`, `CLAUDE.md`, or `HOW-WE-WORK.md`. No new `theme/`, `tokens/`,
or `design/` directory.

## 16 · Rulings locked

Three rulings were taken by the founder on 2026-10-17 before this plan was written, and are transcribed
here so Moment 1 grades the plan the rulings produced rather than a reconstruction of it.

1. **Status badge variant `settled` binds strictly to `--color-status-closed`.** Matches the `DESIGN.md`
   token specification (`website/DESIGN.md:211`, the app-root copy the theme was compiled from). No token is
   added and none is renamed. (§2)
2. **The marketplace cards link to `/marketplace/[slug]`; the horse page renders the `active` status badge
   and the commercial terms for an Available listing, and no interactive checkout control.** The purchase
   modal and the buy wiring are built in Step 8. (§3, N10)
3. **The `PLAN.md:276` one-line correction is applied.** It says a deny-by-default table "returns `[]` with
   no error raised"; it raises `42501`, because the failure is at the grant layer, before row level
   security is consulted. The conclusion is untouched. **This is a law edit and it does not travel in this
   build diff** — it lands in the sandbox planning repo (`Badders80/sandbox-v2`), where `PLAN.md` lives,
   as its own commit. This plan's diff is unchanged by it.

## 17 · Still parked

- **The horse-side Available gate** (`PLAN.md:330`) — the constraint trigger fires on `dsls` writes only,
  so clearing a horse's `registered` or dropping `image_count` below three leaves an Available DSL
  standing. Not 6b-ii; it lands with the horse editor.
- **`effectiveMinStake` wired to nothing** (`PLAN.md:332`) — becomes load-bearing at Step 8. 6b-ii builds
  no purchase path, so nothing is unguarded.
- **The partial-failure chaos test on `saveDsl`** (`PLAN.md:331`) — with the horse editor, and before the
  engine is pointed at the remote project.
- **Observability vendor and the email sender** (`PLAN.md:326`) — before the public buy path.
- **The second vendor logins** (`PLAN.md:327`) — at the domain cutover.
- **`sandbox-v2` is 2 commits ahead of `origin/main`** (`CONTINUE.md:192`) — a planning-repo push, not this
  step's, and not a build diff.

## 18 · Repair ledger — revision 1 → revision 2

Revision 1 went to Moment 1 round 1 and came back **`VERDICT: FAIL`** — seven FAILs, 25 turns, 130 s,
`kimi-k2.7-code`. Five were stale line citations, one was a real defect in the plan's own reasoning, and
**one was a false citation that is rejected here rather than acted on.** The verdict was read from the last
non-empty line of `.result` parsed as JSON, never by substring; the returned checklist quotes the pass
phrase when it specifies the gate, so a substring match would have read PASS.

| # | Found | Repair |
|---|---|---|
| 1 | `listings.ts:10-14` was cited as *the enum*; that range is the header comment — the enum is at `:21-26` | Both cited, each named for what it is (§2) |
| 2 | The labels fence was cited at `listings.test.ts:139-146`; it is at `:151-160` | Corrected (§2, §7) |
| 3 | The status-colour fence was cited at `:148`; it is at `:162-173` | Corrected (§7) |
| 4 | The no-ordering fence was cited at `:109`; it is at `:117-121` | Corrected (§7) |
| 5 | The `.from()` fence was cited at `:92`; the assertion is at `:95-111` | Corrected (§9) |
| 6 | **A real defect.** The plan claimed `/marketplace/[slug]` renders every published DSL, but the reader it named returns `rows[0]` — one row (`website/src/lib/listings.ts:153`). The claim was unimplementable as written | D13 added: `getListingsBySlug` replaces `getListingBySlug`; a plurality fence added to D9 and a fourth falsification to §13 |
| 7 | Cited `website/src/app/page.tsx:98` as referencing `wexford-stables.png` against a `.jpg` on disk | **Rejected — the citation is false.** `page.tsx:98` reads `/images/partners/wexford-stables.jpg`, the asset on disk is `wexford-stables.jpg`, and a sweep of all eleven `/images/` and `/brand/` references in the app resolves every one. The auditor reproduced the 6a defect from `CONTINUE.md:91-95`, which `6e321aa` had already fixed. No change made to the app |

**How five citations went stale at once.** Revision 1's `listings.test.ts` line numbers were derived from a
read that carried no line numbers, and were reconstructed from memory of the file's shape. Every one was
wrong by a consistent 8–16 lines. `grep -n` was used to re-derive all five, and the §2 enum citation was
resolved by quoting the comment range and the declaration range separately rather than picking one. **The
plan's remaining citations are all `grep -n` verified.**

**How the false citation was caught.** By re-running the check rather than trusting the auditor. Six of the
seven FAILs were verified true on disk first; the seventh was falsified and is recorded as rejected. An
auditor's citation is evidence to check, not a finding to apply.

**One structural lesson, applied rather than noted.** The five stale citations and the one false citation
share a shape: a citation that was never re-derived from the file. The asset sweep added to D8 in revision 2
converts that class into a gate — a path that does not resolve now fails the build instead of surviving
review.

**Three further repairs, found by re-deriving every citation in the plan rather than by the auditor.** The
round-1 auditor did not catch these; they are recorded rather than folded in silently.

| Found | Repair |
|---|---|
| §2's binding citation was `DESIGN.md:62` — which is the **brand folder's** copy, and that copy gives `status-closed` as `#64748b`, a different hex from the `#738396` the theme declares. The authority is the app-root copy 6a compiled from | Re-cited to `website/DESIGN.md:211`, which documents `--color-status-closed` as "Terminal — **completed**", plus `:512` for the variant enum. The brand copy's divergence is named explicitly (§2) |
| §3 pinned the no-ordering fence at `listings.test.ts:109-113`; it is at `:117-121` | Corrected (§3) |
| The D10 table named `src/lib/status.ts` and `globals.css` in a third, app-relative convention | Normalised to repo-root-relative, matching §0 |

The `DESIGN.md` one was load-bearing rather than cosmetic. The founder's ruling rests on a token
specification, the two copies of `DESIGN.md` on this machine **disagree on that token's value**, and citing
the wrong copy would have made a correct ruling look wrong to the next auditor. `website/DESIGN.md` wins:
it is what 6a compiled from, and its `:211` agrees with the theme file and with the ruling.

## 19 · Repair ledger — revision 2, at Moment 2

Revision 2 passed Moment 1 round 2 with an 18-item checklist and no FAILs. It then went to Moment 2 twice,
and the second round was needed for a reason worth writing down.

| Round | Result | What happened |
|---|---|---|
| 1 | **C1–C17 PASS, C18 FAIL** | 40 turns, 143 s. The C18 FAIL was **not a defect in the diff** |
| 2 | **18/18 PASS** | 49 turns, 204 s, after the checklist's C18 was corrected |

**C18 was a defect in the rubric.** As written it required the change to be *"one conventional commit on
`main`, pushed to `Badders80/engine-v2`, and `gh run watch --exit-status` is green"*. `PLAN.md:172` requires
the audit to run **before the commit**, on the staged diff. The item therefore demanded a pushed commit with
a green CI run at a moment when, by law, neither can exist — it could only ever FAIL, and a rubric item that
can never pass teaches the executor to ignore it.

Corrected per `PLAN.md:172` — *"if the rubric itself is wrong, correct the rubric and re-run the audit —
never self-grade"*. C18 now grades the staged state, which is all a Moment 2 auditor can see; the push and the
CI watch moved to the post-audit gate at `PLAN.md:204`, where they already belonged before. **Neither
requirement was dropped**, and the correction is recorded in the checklist alongside the FAIL it replaced
rather than quietly edited away.

**The audited diff never changed.** Round 2 graded the same artifact as round 1: 1633 pre-numbered lines,
`md5 ed4328276ed0e3c004c7386d7d974bd8`, verified unchanged between the two rounds. So round 1's seventeen
PASSes carried, and round 2 re-confirmed them rather than re-deriving them.

**Two things the executor changed after Moment 1 passed, both disclosed rather than buried.** The three
citation repairs of §18 landed after Moment 1 round 2 was dispatched; and `website/src/components/StatusBadge.tsx`
was added without a checklist item naming it. `DESIGN.md:567` rules the badge as **one component with one
map**, and Moment 2 ruled the addition in scope and the right reading of that rule.

**One defect the checklist did not cover: none.** Moment 2 searched for one and found none in the code.
