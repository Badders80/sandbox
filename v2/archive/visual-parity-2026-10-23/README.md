# Visual Parity Pass — Decision Record

Written 2026-10-22. Updated 2026-10-23.
Status: **Data backfill & operator console complete; Money Test (Step 10b) ready; visual parity pass scoped for Step 10.5.**
See latest handoff: [`../v2/SESSION-NOTE-2026-10-23.md`](file:///home/evo/sandbox/v2/SESSION-NOTE-2026-10-23.md).

This folder is **not the build**. It holds the decision and the scope for the visual pass that
brings the v2 website up to the old site's polish. The build stays in
`/home/evo/evolution/engine_v2/website/website`. `sandbox/v2/PLAN.md` remains build law;
`sandbox/v2/OUTCOME.md` remains product law. This README sits under both and does not replace either.

---

## Where v2 stands

| | Path |
|---|---|
| Plan / build law | `/home/evo/sandbox/v2/PLAN.md` |
| Product law | `/home/evo/sandbox/v2/OUTCOME.md` |
| v2 build (engine + website) | `/home/evo/evolution/engine_v2/website` |
| Old live site (visual reference) | `/home/evo/evolution/engine/website/apps/web` |
| Earlier visual prototype (reference only) | `/home/evo/sandbox/rebuild` |

- Steps 1–9 are executed and pushed. Last v2 commit: `05df240` (2026-10-21).
- Step 10 is preview/deploy with the buy path off, then one real sale after the Buy Now flip.
- The new backend has **not** been tested end to end against Stripe yet.
- The visual rebuild has **not** started.

---

## The gap

This is not a colour or spacing problem. It is an architectural one.

| | Old live | New v2 |
|---|---|---|
| Landing page | 79 lines, composes 8 section components | 444-line monolith |
| Component layer | ~7,500 lines across `sections/`, `horse/`, `marketplace/`, `ui/` | ~900 lines, 6 components |
| Horse page | shell + media deck + tabs + right rail + pedigree | one 267-line page |
| Theme | `globals.css` + `benedict.css` | `globals.css` (tokens already close) |

The old polish lives in its **composition layer**: `HeroSection`, `AboutSection`,
`HowItWorksSection`, `DigitalSyndicationSection`, `MarketplaceSection`, `PressShowcaseSection`,
`FAQSection`, plus the `ui/` primitives (`GlowPillButton`, `LogoCarousel`, `FixedBg`, `GrassBg`,
accordion), and the horse components (`media-deck`, `tabs`, `right-rail`,
`campaign-status-block`). The new site removed that layer and inlined everything into pages.
Restyling the monolith will never close the gap; restoring the layer will.

---

## The decision: no clean room

A separate app in `sandbox/website` looks clean but creates a second source of truth, a port
step, and merge drift. That experiment has already been run: `sandbox/rebuild` became a third
prototype with its own token package and purchase flow, and it is now parked. Do not repeat it.

**Instead: one branch in `engine_v2/website/website`, presentation-only.**
The clean room is a git branch, not a folder.

### Branch

Suggested name: `visual-parity`. Branch from `main`, rebase before merge, one merge commit.

---

## What gets ported

Copy from the old components, strip their old data coupling, and compose v2 pages from them.
`OUTCOME.md` already permits the old engine as "a source of pieces". Do not import the old repo
at build time; copy and adapt.

### Landing — port all

| Component | Lines |
|---|---|
| `sections/HeroSection.tsx` | 107 |
| `sections/AboutSection.tsx` | 49 |
| `sections/HowItWorksSection.tsx` | 134 |
| `sections/DigitalSyndicationSection.tsx` | 143 |
| `sections/MarketplaceSection.tsx` | 196 |
| `sections/PressShowcaseSection.tsx` | 393 |
| `sections/FAQSection.tsx` | 140 |
| `sections/OwnershipFAQSection.tsx` | 140 |

### UI primitives — port the ones with a call site

`AccordionList` (112), `CollapsePanel` (48), `FixedBg` (16), `GlowPillButton` (50),
`GrassBg` (15), `LogoCarousel` (64), `badge` (40).

### Horse page — port the shell and visual blocks

`media-deck` (270), `tabs` (76), `right-rail` (585), `campaign-status-block` (78),
`story-block` (143), `overview-tab` (69), `race-tab` (206), `pedigree-tab` (616),
`trainer-tab` (126), `documents-tab` (196), `documents-gate` (43).

Adapt props to the v2 read model at the page boundary. Do not move data fetching into components.

### Marketplace / MyStable — evaluate, port what earns its place

`horse-page-shell` (80), `campaign-status-badge` (37), `collapsible-page-intro` (79),
`detail-tabs` (274), `marketplace-cta` (57), `marketplace-listing-grid.tsx`,
plus `cap-table-card.tsx`, `data-room-card.tsx`, `mystable-dashboard.tsx` if the v2 MyStable
needs their visual density.

### Do NOT port

- `horse/purchase-flow-modal.tsx` (2,061 lines). Step 8's `BuyFlowModal` is the sanctioned flow.
  Copy visual shell only if a piece is reusable; never its business logic.
- `marketplace/purchase-flow-host.tsx` unless it is pure presentation.
- `design-lab/`. Do not ship it. Use screenshot snapshots instead.
- `packages/brand_dna`, any old token package, any old alias map.
- `NavBar` / `footer` wholesale — compare against v2's existing versions first; replace only if
  the old ones are meaningfully better.

---

## Purchase workflow

Three artefacts exist. Only one is the implementation.

| Artefact | What it is | Role |
|---|---|---|
| Old `purchase-flow-modal.tsx` (2,061 lines) | Live flow: `terms → accept → kyc → checkout → confirm` | Visual and interaction reference. Not code. Its confirm step claims ownership before the sale exists; never port it. |
| `sandbox/rebuild/purchase-flow-v2.html` | Static prototype, six review steps with branches | Screen words and layout reference only. No in-modal payment, no celebration seal, no review rail. |
| v2 `BuyFlowModal.tsx` (595 lines) | Step 8's five-screen flow: `Terms → Documents → Identity → Pay → Return` | **The implementation.** Functional, tested, visually wireframe. Refactor this. |

Do not write a fourth flow.

### Shape

```
src/components/buy-flow/
  BuyFlowModal.tsx        host only: mount, open, dispatch, redirect
  ModalShell.tsx          responsive frame + progress rail
  reducer.ts              pure transitions and guards
  screens/
    TermsScreen.tsx
    DocumentsScreen.tsx
    IdentityScreen.tsx
    PayScreen.tsx
    ReturnScreen.tsx      pending only; never says "you own"
  parts/
    StakeStepper.tsx
    QuoteRows.tsx
    LegalDocAccordion.tsx
    DeclarationChecklist.tsx
    FlowError.tsx
```

The reducer lives under `components/buy-flow/`, not `src/lib/`, so the scope fence stays
intact. `src/lib/engineClient.ts` is unchanged and remains the only server boundary.

### Rules

- Screens are presentational. The reducer owns transitions. `engineClient` owns every server
  fact: quote, compiled documents, identity outcome, checkout URL, sale state.
- No pricing, no document compilation, no Stripe secret in the website.
- Copy constants stay in `engineClient`; no duplicated strings.
- `Return` is a MyStable pending state. It never asserts ownership.

### Port from the old flow

- Pinned shell header and progress rail — not the fixed `h-[900px]` never-scrolls lock. Use
  `max-h-[100dvh]`, shell pinned, each screen scrolls internally, full-width sheet on mobile.
- Four-row term summary, stepper with direct entry and step validation, green distribution row.
- PDS→SA accordion with scroll-gated ticks, auto-collapse on complete, four declarations.
- Identity verified/unverified split, with no "NZTR-verified member" claim.
- Payment summary and hosted Checkout handoff.

### Do not port

- Old `confirm` step and the prototype's celebration seal.
- In-modal payment.
- Prototype review rail and pass/fail toggles.
- `marked`, `pricingForUnits`, `useAuth`, `@evo/ui`, `legal_engine`.

### Commit sequence

1. `refactor(website): split BuyFlowModal into shell, reducer, screens` — behaviour identical,
   tests green, no visual change.
2. `feat(website): port purchase-flow visual shell` — old markup and class rhythm, existing
   tokens, behaviour untouched.
3. `test(website): cover buyFlow reducer transitions` — Terms → Documents → Identity → Pay,
   plus the gates.
4. Horse page mounts the modal; MyStable owns the return.

Steps 1 and 2 stay separate so a break is attributable to extraction or paint, never both.

### Gate

Existing hermetic tests stay green. Add reducer transition tests and the copy invariants
(verbatim refund sentence, four declarations, no day counts, no NZTR-verified claim, no
ownership before the sale). Manual or Playwright: happy path, KYC failure, Checkout cancel,
in Stripe test mode.

### Decision

Progress rail: render four steps plus a handoff marker, while keeping `BUY_FLOW_SCREENS` as the
state enum so the existing tests stay valid.

---

## Zero-debt rules

1. **Port, don't redraw.** Reuse the old components; do not hand-write comparable markup.
2. **Move, don't duplicate.** A copied component replaces the page-local markup in the same
   commit. No dead components, no unused files.
3. **No new packages.** No animation library, no component library, no second theme.
4. **One theme file.** Every value goes into `website/src/app/globals.css`. A new token is a
   rejected change unless it is added there and justified.
5. **Parity is the baseline; improvements are a named list.** An unnamed visual change is drift.
6. **Every copied component must have a call site.** If nothing renders it, it does not ship.
7. **Do not touch data or money.** Visual branch never edits `engine/`, `supabase/`, `src/lib/**`,
   pricing, the webhook, or tests that assert behaviour.
8. **Delete after copy.** The old app is archived, not maintained. Do not leave two copies in
   play or import across repos.

---

## Scope fence

Visual branch **owns**:

- `website/src/app/page.tsx`
- `website/src/app/marketplace/**` (presentational markup only)
- `website/src/components/**`
- `website/src/app/globals.css`

Visual branch **never touches**:

- `engine/**`, `supabase/**`, `website/src/lib/**`, `website/src/app/mystable/**` data logic
- pricing, compiler, webhook, migrations, Stripe
- `PLAN.md` / `OUTCOME.md` beyond the one-line amendment below

---

## Gates

- `pnpm verify` green at repo root (`/home/evo/evolution/engine_v2/website`), `--max-warnings=0`.
- Behaviour tests unchanged and green.
- Screenshot snapshots per route at **1440×900** and **390×844**, old vs new, kept as the
  acceptance record.
- Definition of done: landing, marketplace, horse page, purchase flow, MyStable and login match
  the old site's density and rhythm; all v2 functionality preserved; buy-flow behaviour
  unchanged; no new dependencies; no tokens beyond `globals.css`.

---

## Timing with the backend and cutover

Visual and backend do not share files, so run them concurrently.

- **Track A — backend (step 10).** Preview deploy with the buy path off. Stripe test-mode
  purchase, KYC, webhook sale write, hashes, four emails, MyStable. This does not need the pretty UI.
- **Track B — visual.** Port primitives → extract and port the buy flow → horse page → landing
  sections → marketplace. Screenshot gate per route. The flow comes first because the horse
  page mounts it and because it is the only visual surface that touches money.

Only ordering that matters:

1. Backend code frozen (steps 1–9 done; only fixes).
2. Visual branch merges to `main`.
3. Preview redeploy → founder reviews **once**, on the final look.
4. Re-run backend smoke on the merged build.
5. One real sale after the Buy Now flip — the actual roll gate.
6. Domain flip; old site keeps serving until DNS/TLS confirm; then archive old app and keep the
   data export.

**Rule:** visuals never block the money test; the money test never waits for polish. The only
hard order is visual merge → founder preview → real sale → cutover.

---

## Plan amendment (one line)

`PLAN.md` §7 currently says there is no separate design pass, and the Parked table defers
per-page styling. Activate it rather than working outside the plan:

> **Step 10.5 — Visual parity pass.** Activated 2026-10-22. Scope `website/` only. Reuses the 6a
> theme file; no new tokens, no new packages. Ports the old presentational component layer and
> recomposes pages. Does not touch `engine/`, `supabase/`, pricing, or the buy flow.
> Decision record: `sandbox/website/README.md`.

---

## Open decisions — blocking

1. **Parity depth.** Pixel-level match of the old pages, or brand-level match with the old
   sections re-composed?
   *Recommendation: brand-level.* The old components carry density and rhythm; exact pixel
   parity also imports old content mistakes.
2. **Route parity.** Old site has `/privacy`, `/terms`, and `/horses/[slug]/about`; v2 has none.
   *Recommendation: add `/privacy` and `/terms` (a site taking money needs them); skip
   `/horses/[slug]/about` unless its content is genuinely missing from the new horse page.*

Record the answers here before branching.

---

## Tomorrow's first move (< 2 minutes)

Answer the two decisions above. Then activate the Parked row with the amendment text, and cut
`visual-parity` from `main` in `engine_v2/website`. First commit on that branch is the buy-flow
extraction (commit 1 in **Purchase workflow**), not the landing page.
