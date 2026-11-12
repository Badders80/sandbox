# V2 Website Design Review

**Date:** 2026-11-11  
**Status:** reference audit, not an MVP completion gate  
**Target:** proposed v2 public website at `/home/evo/evolution/engine_v2/website/website`  
**Method:** dual-agent design review plus deterministic scan and browser evidence

## Scope

Reviewed the locally rendered proposed v2 website:

- `/`
- `/marketplace`
- desktop at 1440px and mobile at 390px
- source-level review of horse detail, checkout, navigation, footer and design tokens

The live production website at `https://evolutionstables.nz/` was **not** part of
this review. A side-by-side production comparison remains queued below.

## Verdict

**Strong visual foundation, partially modular implementation, not yet a credible
live marketplace.** Design health score: **23/40 — acceptable**.

The visual identity is coherent and specific: near-black surfaces, restrained
gold, editorial typography, horse photography and mono financial figures. The
information architecture is more generic and does not yet carry the product's
marketplace specificity.

## What Works

- The tokenized visual identity is distinct and consistent.
- Desktop and mobile render without horizontal overflow.
- One H1 is present on reviewed pages; images load and headings form a usable
  outline.
- The source includes a deliberate multi-step purchase modal with progress,
  close and error states.

## Priority Issues

**[P0] Marketing promises unavailable inventory.**  
Multiple offering CTAs lead to a marketplace that says no offers are published.
Publish one real offer for the walk or present an explicit pre-launch state with
a notification action.

**[P1] The first viewport explains atmosphere, not the product.**  
The hero contains the wordmark and an abstract tagline, but no horse, offer,
term, return or next action.

**[P1] Accessibility drifts from the written system.**  
Several mobile controls are below 44px, focus treatment is inconsistent,
Escape does not close the mobile drawer and the partner marquee ignores reduced
motion.

**[P1] Trust links are unresolved.**  
Privacy Policy and Terms of Service appear globally but have no public routes.

**[P2] The homepage is longer than its information yield.**  
It is approximately 8,570px tall on desktop and 10,576px on mobile. The first
offering CTA begins about 6,101px down on mobile.

## Modularity

- **Tokens:** strong central theme and useful semantic names.
- **Components:** partial. Core chrome exists, but marketplace cards remain
  page-local and the purchase modal is large and monolithic.
- **Consistency:** mostly coherent, but manual review found undeclared spacing,
  hero type oversized against the documented scale, gold-filled primary CTAs
  against the written white-primary rule, and missing focus rings.

## Evidence Limits

- No published marketplace listing exists in the v2 environment.
- `/marketplace/mulan-the-brave` returns 404 because Mulan remains unpublished.
- Horse detail and rendered checkout could not be visually walked.
- The deterministic detector returned zero findings; the higher-risk issues
  were found through browser geometry, accessibility inspection and source
  review.
- No Impeccable visual overlay was available.

## Detailed Snapshot

The full critique snapshot is stored at:

`/home/evo/evolution/engine_v2/website/website/.impeccable/critique/2026-11-11T09-38-27Z__src-app-page-tsx.md`

## Production Comparison — QUEUED

Do not treat this review as evidence that v2 is better or worse than production.
Once one v2 listing is published, compare:

1. Homepage first viewport and proposition.
2. Marketplace inventory and empty state.
3. Horse detail hierarchy and purchase path.
4. Mobile navigation, tap targets and accessibility.
5. Legal links, trust signals and document access.

Production reference: `https://evolutionstables.nz/`.
