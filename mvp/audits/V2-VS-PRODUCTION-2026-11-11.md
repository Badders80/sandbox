# V2 vs Production Website Review

**Date:** 2026-11-11  
**Status:** complete read-only comparison  
**V2:** `http://localhost:3000`  
**Production:** `https://www.evolutionstables.nz/`  
**Viewports:** 1440×1000 desktop and 390×844 mobile

## Verdict

**V2 is not yet the better website. It is the cleaner foundation.**

Production is the more complete commercial product: it has live listings, richer
horse pages, visible pricing and returns, legal-document access, a purchase CTA
and populated trust content. V2 is more tokenized, more restrained, semantically
cleaner and about 17–18% shorter, but its primary marketplace currently has no
published offer and its horse page cannot be reached.

## Route Comparison

| Surface | V2 | Production | Result |
|---|---|---|---|
| Homepage | Coherent dark/editorial system; abstract wordmark hero; 8,570px desktop, 10,577px mobile | Same visual family; longer and more content-rich; 10,350px desktop, 12,950px mobile | V2 is cleaner and shorter; production gives more evidence and context |
| First proposition | Wordmark and tagline; no named horse or offer | Explicit digital racehorse ownership proposition plus press/trust material | Production communicates the product more quickly |
| Marketplace | Clear empty state; zero listings | Six status-grouped listings with summaries, statuses and actions | Production is decisively stronger |
| Horse detail | Unavailable: `/marketplace/mulan-the-brave` returns 404 | Rich gallery, story, tabs, price, return, benefits, CTA and legal documents | Production is the only end-to-end reference currently available |
| Mobile behavior | No horizontal overflow; 13 undersized interactive targets detected | No horizontal overflow; 17 undersized interactive targets detected | Neither meets the written touch-target floor; V2 has fewer failures |
| Legal links | Privacy/Terms links exist but their routes return 404 | Privacy/Terms and PDS/SA links resolve | Production wins on visible trust |
| Structure | Route-specific marketplace H1; source enforces one H1 on horse pages | Horse page contains two H1s (`Ownership, evolved.` and the horse name) | V2 is semantically cleaner |

## What V2 Does Better

- The design token system is explicit and central.
- Route-specific headings and metadata are cleaner.
- The page is shorter and less overloaded than production.
- The layout is responsive with no horizontal overflow at 390px.
- The marketplace empty state is honest and well-written.
- The source has deliberate loading, error and multi-step purchase states.

## What Production Does Better

- Users can browse real horses and understand status immediately.
- Horse pages provide the story, pedigree, trainer, race record, documents,
  price, investor return and a clear ownership action in one place.
- Legal trust links are live.
- The homepage carries more social proof, press and racing specificity.
- The commercial path is visible and testable.

## Shared Weaknesses

- Both homepages are very long before a concrete offer is reached.
- Both fail the 44px touch-target floor in several places.
- Both retain a generic luxury-site structure beneath the strong visual skin.
- Both could make the actual stake, term and return easier to understand before
  the horse page.

## Important V2 Source Risks

The V2 horse-page source exposes `minimum stake`, `step`, `remaining`, `payment
model` and `close style` as prominent customer-facing figures. That conflicts
with the locked model's treatment of minimum and increment as order-book
controls rather than the core public offer. Checkout also exposes minimum/step
wording.

This should be reconciled before the detailed horse-page walk:

- public: total DSL stake, price per 1% per month, term/expiry, investor split;
- purchase control: selected quantity constrained by the order book;
- internal: step size, close style and operator mechanics unless required for
  disclosure.

## Recommendation

Do not replace V2 with production or port production wholesale. Use production as
the content and conversion reference, retain V2's token system and cleaner
structure, and close these gaps first:

1. Publish one real V2 listing.
2. Make the homepage's primary CTA truthful for the current inventory state.
3. Bring the horse page to commercial parity without copying production's
   information density or duplicate H1 structure.
4. Align visible offer fields with `MODEL.md`.
5. Fix touch targets, focus treatment and legal routes.

## Evidence Limits

- V2 horse detail and checkout were not rendered because no listing is
  published.
- No performance benchmark was run.
- Comparison used live accessibility trees, page text, DOM measurements and
  full-page screenshots.
- Production was inspected read-only; no forms, purchases or account actions
  were submitted.
