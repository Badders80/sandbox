# Step 6b-ii — LOCKED CHECKLIST (Moment 1, round 2)

**Verdict: `VERDICT: PASS`.** Locked 2026-10-17 by the independent auditor (`kimi-k2.7-code`, Ollama Cloud,
headless). Audited plan: `/tmp/step6b-ii-plan.md` (**revision 2**). Audit output:
`/tmp/step6b-ii-m1b.out`. Round 2 graded **no items FAIL** — 29 turns, 183 s.

Round 1 audited revision 1 and returned FAIL with seven FAILs (25 turns, 130 s). Six were verified true on
disk and repaired; **the seventh was verified false and rejected**, and round 2 withdrew it in writing. The
repair ledger is the plan's §18.

**This checklist is the Moment 2 rubric.** Moment 2 audits the pre-numbered staged diff against these
items, one at a time, PASS/FAIL with a `file:line` citation. A dummy citation fails the item.

---

## Provenance note — three citation-only edits landed after round 2 was dispatched

Round 2 was dispatched against revision 2 as it stood at that moment. While it ran, the executor re-derived
every one of the plan's ~60 citations with `grep -n` and found three more, which were corrected in the plan
**after** dispatch:

| Found | Repair |
|---|---|
| §2 cited `DESIGN.md:62` — the **brand folder's** copy, which gives `status-closed` as `#64748b`, a different hex from the `#738396` the theme declares | Re-cited to `website/DESIGN.md:211` ("Terminal — **completed**") and `:512` (variant enum `active · pending · settled`) |
| §3 pinned the no-ordering fence at `listings.test.ts:109-113`; it is at `:117-121` | Corrected |
| The §7 D10 table named `src/lib/status.ts` and `globals.css` in a third, app-relative convention | Normalised to repo-root-relative, matching §0 |

**No deliverable, claim, or negative constraint changed** — every edit is a citation or a path form. The
round-2 PASS therefore locks for the plan as it now stands. Item C15 already names the corrected
`:151-160`, `:162-173` and `:117-121` ranges, so the checklist and the plan agree. Disclosed here rather
than left for Moment 2 to discover.

---

## LOCKED CHECKLIST

**C1.** `website/src/lib/status.ts` exists, exports `STATUS_VIEWS: Record<DslStatus, StatusView>` and
`viewForStatus(status: string): StatusView`; `viewForStatus` throws on any value absent from
`DSL_STATUS_VALUES`, with no `??` fallback, no `default:` branch, and no optional chain.

**C2.** `STATUS_VIEWS` maps the four DB enum values exactly as `PLAN.md:286`: `coming_soon` → key
`coming_soon`, label `COMING SOON`, variant `active`; `available` → key `listed`, label `AVAILABLE`, variant
`active`; `fully_allocated` → key `fully_subscribed`, label `FULLY ALLOCATED`, variant `pending`;
`completed` → key `completed`, label `COMPLETED`, variant `settled`.

**C3.** The `settled` variant resolves to a class name built from `--color-status-closed`;
`website/src/app/globals.css` is unchanged and declares no new status token.

**C4.** `website/src/app/marketplace/page.tsx` declares `export const dynamic = 'force-dynamic'`, reads
`listPublishedListings()`, renders one card per published DSL with a link to `/marketplace/[slug]`, applies
no `.order(`, uses no `featured` variant, and exports its own title/description/canonical metadata.

**C5.** `website/src/app/marketplace/[slug]/page.tsx` declares `export const dynamic = 'force-dynamic'`,
reads `getListingsBySlug(slug)`, calls `notFound()` on empty result, renders one `h1` with the horse
`legalName`, renders one block per published DSL with the status badge and the stored commercial terms,
renders no interactive checkout control of any kind, and includes JSON-LD for the horse at
`/marketplace/[slug]` with `name`, `description`, `url`, `image`, no `offers`, no price, and no `/horses/`
path.

**C6.** `website/src/lib/listings.ts` declares `getListingsBySlug(slug): Promise<Listing[]>` and declares no
`getListingBySlug`; the function uses `LISTING_SELECT`, filters `published = true`, embeds `horses!inner`,
and returns every matching row without `.single()`, `.limit(1)`, or `rows[0]`.

**C7.** `website/src/lib/site.ts` exists, is pure, holds `SITE_URL = 'https://www.evolutionstables.nz'`,
holds the site-level `OG_IMAGE = '/og/default.png'`, and mirrors the R2 key shape from
`engine/src/lib/storage.ts`: `imageKey('lady-ketchikan', 1) === 'lady-ketchikan/01'`, no file extension,
files numbered from `01`.

**C8.** `website/src/app/robots.ts` exists and is static; it disallows `/mystable`, `/login`, `/checkout` and
names the sitemap URL using the www host.

**C9.** `website/src/app/sitemap.ts` exists, declares `export const dynamic = 'force-dynamic'`, derives its
URL set from the read layer (`listPublishedListings()`), deduplicates by horse slug, and contains the
landing page, `/marketplace`, and one URL per horse carrying at least one published DSL (Coming Soon
included); it contains no `/horses/`, no `/mystable`, no `/login`, no `/checkout`, and no unpublished DSLs.

**C10.** `website/src/app/layout.tsx` and `website/src/app/page.tsx` set `metadataBase` to
`https://www.evolutionstables.nz`, carry the site-level OG image, and add Organisation + WebSite JSON-LD on
the landing page; the apex host `https://evolutionstables.nz` appears as a URL nowhere under
`website/src/`.

**C11.** `website/next.config.ts` adds the R2 public origin to `images.remotePatterns`, and
`website/.env.example` names `WEBSITE_R2_PUBLIC_URL` as the third env name with no value; no tracked file
contains a credential.

**C12.** `scripts/assert-search-layer.sh` exists, is `set -euo pipefail`, asserts the three metadata routes
exist, the canonical host, the disallow list, the sitemap source, no `/horses/`, the three `force-dynamic`
declarations, and the asset-path sweep for every `'/images/'` and `'/brand/'` string literal under
`website/src/`; it is wired into root `package.json` `test` chain as `test:search-layer`.

**C13.** `website/tests/status.test.ts` exists and hermetically asserts the four enum mappings, the throw on
an unknown value, the `settled`→`status-closed` and `active`→`status-active` class bindings, and that the
four uppercase labels and the four variant names appear only in `website/src/lib/status.ts` and
`website/src/app/globals.css`.

**C14.** `website/tests/search.test.ts` exists and hermetically asserts `imageKey`, `publicImageUrl`
(including dot/rejected-private-prefix/non-integer/non-https failures), sitemap deduplication by slug, the
plurality fence (`getListingsBySlug` present, `getListingBySlug` absent, no
`rows[0]`/`.single()`/`.limit(1)`), and `SITE_URL` is the www host.

**C15.** `website/tests/listings.test.ts` is amended, not deleted: the labels fence (`:151-160`) and the
status-colour fence (`:162-173`) exempt only `website/src/lib/status.ts` alongside
`website/src/app/globals.css`; the no-ordering fence (`:117-121`) remains unchanged.

**C16.** `engine/OPERATIONS.md` records the physical trigger check from `PLAN.md:333`: against the local
544xx stack, a fixture horse with fewer than three images refuses a DSL write to `available`, and with
three images accepts it; the fixture is removed afterwards and no test in `engine/tests/` opens a database
connection.

**C17.** No `.from('horses')`, `.from('trainers')` or `.from('owners')` under `website/src/`; every
`.from('…')` names `dsls`; no import specifier resolves into `engine/`; no service-role key, Stripe secret,
or `sb_secret_`; no pricing recompute; no checkout button/link/form/inert stand-in; no `/horses/` path; no
new token, palette edit, `theme/`/`tokens/`/`design/` directory, or
`AGENTS.md`/`CLAUDE.md`/`HOW-WE-WORK.md`.

**C18.** The change is **one conventional commit's worth of change, staged as a single commit on `main` of
`Badders80/engine-v2`**: every staged path is inside the agreed scope, no unrelated file is staged, and
`pnpm-lock.yaml` is unchanged. The commit message is conventional and carries the `Co-Authored-By: Claude
Code <noreply@anthropic.com>` attribution line. The push (`git push origin main`, where `origin` is
`Badders80/engine-v2`) and the green `gh run watch --exit-status` are the **post-audit gate** ruled at
`PLAN.md:204`; they are verified outside this checklist and recorded in `CONTINUE.md`, not graded here.

---

## FAILs

None.

---

## Rubric correction, 2026-10-17 — C18, after Moment 2 round 1

Moment 2 round 1 graded **C1–C17 PASS, no FAILs, and C18 FAIL** — 40 turns, 143 s. The C18 FAIL was not a
defect in the diff. It was a defect in this checklist.

C18 as first written required the change to be *"one conventional commit on `main`, pushed to
`Badders80/engine-v2`, and `gh run watch --exit-status` is green"*. `PLAN.md:172` requires the audit to run
**before the commit**, on the staged diff. So the item demanded a pushed commit with a green CI run at a
moment when, by law, neither can exist yet. It was unfalsifiable in the only direction that mattered: it
could only ever FAIL, and a rubric item that can never pass teaches the executor to ignore it.

Corrected per `PLAN.md:172` — *"if the rubric itself is wrong, correct the rubric and re-run the audit —
never self-grade"*. C18 now grades the staged state, which is what a Moment 2 auditor can actually see, and
the push and CI watch move to the post-audit gate at `PLAN.md:204` where they already belonged. **Neither
requirement was dropped.** The push and the green run remain mandatory; they are verified against
`gh run watch` output and recorded in `CONTINUE.md`.

**Nothing else changed.** The audited diff is the same artifact: 1633 pre-numbered lines, unchanged since
it was staged, `md5 ed4328276ed0e3c004c7386d7d974bd8`. Round 2 re-grades the same diff against the same
C1–C17, which round 1 already passed.
