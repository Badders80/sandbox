# Next Session Plan — Marketplace → Horse → Checkout → MyStable

**Status:** ACTIVE
**Created:** 2026-11-13
**Owning code repo:** `/home/evo/evolution/engine_v2/website`
**Owning planning repo:** `/home/evo/sandbox` (`mvp/` is inside this repo)

## Outcome

Rebuild the public commerce path on the V2 shared foundation, in this order:

1. Marketplace initial page.
2. Marketplace horse page.
3. Checkout on the horse page.
4. MyStable after checkout.

Production is the content, hierarchy and trust reference. V2 owns the implementation, tokens, components, motion and data contracts.

## Current Baseline

- Shared V2 page foundation is merged and pushed on `dsl-sidequest` at `ade0cc3`.
- Landing parity is merged at `03ea397` and visually accepted.
- Shared foundation:
  - global scroll-reveal observer;
  - `--duration-reveal: 750ms`;
  - `PageShell`, `PageContainer`, `PageIntro`, `PageSection`;
  - no page-level separator rule (`DESIGN.md` rule 25);
  - Marketplace, horse page and MyStable already consume the primitives.
- Shared gate currently green:
  - engine: 402 passed, 1 skipped;
  - website: 63 passed;
  - both builds pass.
- The current worktree also contains unrelated uncommitted legal/checkout work. Do not stage, discard, reformat or overwrite it.

### Execution checkpoint — 2026-11-14

- Production Marketplace was audited read-only at `1440×1000` and `390×844`.
- V2 `/marketplace` is implemented on isolated branch
  `marketplace-parity-2026-11-14` from `e74b725`, using a local six-card
  visual fixture with Mulan as the available lead card. Nothing was published
  and no Marketplace data was written.
- Evidence, geometry, card anatomy and the carry/adapt/reject decisions are in
  `mvp/audits/marketplace-parity-2026-11-14/EVIDENCE.md`.
- Gate: engine 401 passed / 1 skipped, website 66 passed, both builds. Desktop
  and mobile axe reports show zero violations; filters, keyboard order, 44px
  page controls and reduced motion were walked.
- Session 1 gate: founder approved the Marketplace visual direction and
  desktop/mobile result.

### Session 2 checkpoint — 2026-11-14

- Production Mulan was audited read-only at `1440×1000` and `390×844`, including
  gallery, facts, story, five detail tabs, public offer, legal access and mobile
  conversion behaviour.
- V2 `/marketplace/mulan-the-brave` is implemented on isolated branch
  `horse-page-parity-2026-11-14` from accepted Marketplace commit `ec725c1`.
  Mulan remains a local fixture; no listing, schema or Marketplace data changed.
- Evidence and the carry/adapt/reject decisions are in
  `mvp/audits/horse-page-parity-2026-11-14/EVIDENCE.md`.
- Gate: engine 401 passed / 1 skipped, website 69 passed, both builds. Desktop
  and mobile axe reports show zero violations; gallery, tabs, keyboard, 44px
  controls, reduced motion and the fixed conversion-bar/footer clearance pass.
- Remaining Session 2 gate: founder approval of the horse-page result before
  checkout implementation starts.

## Session 1 — Lock the Marketplace Initial Page

### Goal

Produce one evidence-backed visual contract for `/marketplace`, implement it on the shared V2 foundation, and obtain founder sign-off at 1440px and 390px.

### Required Research

Audit the live production Marketplace page read-only:

- `https://www.evolutionstables.nz/marketplace`
- desktop `1440×1000` and mobile `390×844`;
- hero/header hierarchy;
- spacing between page intro and listing grid;
- card anatomy, image treatment, status placement, CTA placement and empty state;
- published/coming-soon/fully-allocated/completed states;
- what the page exposes publicly versus what belongs only on the horse page;
- touch targets, focus states, keyboard order and reduced-motion behavior.

Save the audit under:

`/home/evo/sandbox/mvp/audits/marketplace-parity-2026-11-14/`

Required evidence:

- paired production/V2 screenshots at both viewports;
- section/geometry table;
- card anatomy table;
- list of content and behavior to carry, adapt or reject;
- one explicit visual direction for the V2 implementation.

### V2 Implementation Rules

- Use `PageShell`, `PageIntro`, `PageSection`, `PageContainer`.
- Use existing design tokens only. Do not add a second visual language.
- No page-level `border-t` separators.
- Keep the shared nav, footer and reveal system.
- Use a local visual fixture for card-layout proof; do not publish Mulan or write Marketplace data during this phase.
- No figures inside cards unless the production audit and locked model justify them.
- Public page order remains `available`, `coming_soon`, `fully_allocated`, `completed`; within rank, soonest close first.
- Empty state must remain honest and usable.
- Motion is reveal-only; do not add parallax, GSAP or production motion code.

### Session 1 Definition of Done

1. Production audit evidence exists and is linked from `mvp/CONTINUE.md`.
2. Founder approves one Marketplace visual direction.
3. V2 `/marketplace` implements that direction on the shared foundation.
4. `just check` passes.
5. Browser walk passes at `1440×1000` and `390×844`:
   - zero horizontal overflow;
   - one `h1`;
   - keyboard focus order works;
   - touch targets meet the 44px floor;
   - reduced-motion shows content immediately;
   - cards and empty state render honestly.
6. Founder visual walk approves the V2 result.
7. Work is committed on an isolated Marketplace branch from `origin/dsl-sidequest` and pushed; do not merge until the founder walk passes.

### Session 1 Out of Scope

- no Mulan publish;
- no horse-page rebuild;
- no checkout changes;
- no MyStable redesign;
- no schema or data changes;
- no production-site writes.

## Session 2 — Marketplace Horse Page

Audit production `/marketplace/<horse>` and rebuild the V2 horse page after Session 1 approval.

Lock these areas first:

- hero image/gallery;
- horse identity and single `h1`;
- offer terms and public versus operator-only fields;
- price, split, term and remaining inventory presentation;
- legal/investor-pack access points;
- the mobile conversion path;
- state behavior for available, coming-soon, fully allocated and completed.

Do not copy production markup or motion. Use the shared V2 page primitives and current status vocabulary.

## Session 3 — Checkout on the Horse Page

Use `/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html` as an interaction-logic reference only. Do not import its HTML, CSS, fonts, tokens or assets.

Required five-step sequence:

1. Terms.
2. Documents.
3. Identity.
4. Pay.
5. Return / confirmation.

Locked interaction direction:

- one modal, one stable outer footprint across all steps;
- only the step body scrolls when required;
- progress chrome remains stable;
- desktop is the design reference, but mobile is the primary validation target;
- design first at 390px, then confirm at 1440px;
- no artificial elapsed-time holds;
- state transitions use the V2 motion tokens and remain interruptible;
- documents, declarations, KYC and payment gates preserve the locked legal/sale sequence;
- use the current engine/API contracts; do not revive sandbox implementation code.

Assurance: this phase touches auth, documents, payment and sale writes. Tier A applies. A `kimi-k2.7-code:cloud` audit of the mergeable diff is required before merge unless the founder explicitly waives it.

## Session 4 — MyStable

Audit production MyStable and rebuild the V2 investor view after checkout is accepted.

Required states:

- signed out;
- signed in with no stake;
- checkout return pending;
- recorded sale;
- frozen Investor Pack (PDS + SA) display;
- proof-of-address status;
- future distribution/term information only when backed by stored data.

MyStable must never present a pending checkout as owned. Frozen document hashes and acceptance evidence must remain visible and verifiable.

## Shared Invariants

- Do not bring old-build debt into V2.
- Do not duplicate page shells or section headers.
- Do not introduce raw design values.
- Do not add page-level separator rules.
- Do not use production as a code source.
- Do not publish or mutate production data without an explicit founder ruling.
- Preserve unrelated dirty work in the shared checkout.
- One surface or checkpoint in progress at a time.
- Evidence before merge; founder walk before acceptance.

## Working Location

Start the next session from a clean worktree based on:

`origin/dsl-sidequest` at `e74b725` (wrap commit; foundation code is `ade0cc3`)

Suggested worktree:

`/home/evo/evolution/engine_v2-worktrees/marketplace-parity-2026-11-14`

Suggested branch:

`marketplace-parity-2026-11-14`

Do not work directly in the shared checkout that contains unrelated legal/checkout changes.

## Verification Commands

- `just check`
- `git diff --check`
- browser walk at `1440×1000` and `390×844`
- reduced-motion browser pass
- keyboard/focus pass
- screenshot comparison and visual founder walk

## Stop Conditions

Stop and request a ruling if:

- the production Marketplace content contradicts the locked MVP model;
- a card requires data not present in the read layer;
- the visual direction requires a new token or component family;
- publishing Mulan is required to test the design;
- Session 1 scope expands into the horse page or checkout.
