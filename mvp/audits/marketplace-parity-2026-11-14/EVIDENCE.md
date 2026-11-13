# Marketplace Visual Parity Evidence

**Date:** 2026-11-14  
**Production:** `https://www.evolutionstables.nz/marketplace`  
**V2:** `http://localhost:3000/marketplace`  
**Worktree:** `/home/evo/evolution/engine_v2-worktrees/marketplace-parity-2026-11-14`  
**Branch:** `marketplace-parity-2026-11-14` from `origin/dsl-sidequest` at `e74b725`

## Visual Direction

Use production's page hierarchy and commercial clarity, not its implementation:

1. An editorial page intro with one `h1`, followed by the Ownership FAQ jump link.
2. Compact status filters, then full-width horse rows with image-right composition on desktop.
3. Status, horse name, one-sentence hook, up to four factual highlight tags and exactly one CTA.
4. The ruled public order: `available`, `coming_soon`, `fully_allocated`, `completed`.
5. A full-width Ownership FAQ section separated by rhythm, never a page rule.
6. Shared V2 nav, footer, page primitives, tokens and 750ms reveal system remain intact.

The local fixture uses public production content and all six horses so every public status can
be checked. Mulan is the available lead card. No Marketplace row was published and no database
write occurred.

## Evidence

- [Production desktop full page](./production-desktop-1440.png)
- [V2 desktop full page](./v2-desktop-1440.png)
- [Production mobile full page](./production-mobile-390.png)
- [V2 mobile full page](./v2-mobile-390.png)
- [Desktop side-by-side](./desktop-comparison.png)
- [Mobile side-by-side](./mobile-comparison.png)
- [Production desktop viewport](./production-desktop-viewport.png)
- [V2 desktop viewport](./v2-desktop-viewport.png)
- [Production mobile viewport](./production-mobile-viewport.png)
- [V2 mobile viewport](./v2-mobile-viewport.png)

## Page Geometry

| Viewport | Surface | Production height | V2 height | Difference | Horizontal overflow |
|---|---|---:|---:|---:|---|
| 1440×1000 | Full page | 4,469px | 4,031px | -438px | None |
| 390×844 | Full page | 6,494px | 5,638px | -856px | None |
| 1440×1000 | Page intro | ~362px | 469px | +107px | None |
| 1440×1000 | Listing section | ~1,922px | 2,135px | +213px | None |
| 1440×1000 | Ownership FAQ | ~1,245px | 1,224px | -21px | None |
| 1440×1000 | Global footer | 691px | 204px | -487px | None |
| 390×844 | Page intro | ~524px | 517px | -7px | None |
| 390×844 | Listing section | ~3,818px | 3,583px | -235px | None |
| 390×844 | Ownership FAQ | ~1,400px | 1,338px | -62px | None |
| 390×844 | Global footer | 656px | 200px | -456px | None |

The main height gap is the already-accepted V2 footer, not the Marketplace composition. The FAQ
height is within 21px on desktop and 62px on mobile. The V2 listing section is taller because every
CTA has a 44px target and the desktop card uses the V2 card-heading token rather than production's
off-token 28px heading.

## Card Anatomy

| Element | Production | V2 decision |
|---|---|---|
| Shape | Rounded row card, image right on desktop | Carried; V2 surface, border and 24px radius |
| Status | Overlaid on the image frame | Carried through the shared `StatusBadge` |
| Image | Contained 16:9 artwork | Carried; local 960×540 fixture assets |
| Name | 24/28px production heading | V2 `text-card-heading` token |
| Hook | One sentence, hard bounded | Carried |
| Tags | Up to four horse facts, no offer figures | Carried |
| CTA | Register interest or View offering | Carried as the only anchor in the card |
| Mobile order | Image, name, hook, tags, CTA | Carried |

## Carry, Adapt, Reject

**Carry**

- Intro copy and single `h1` hierarchy.
- All Thoroughbreds / Available / Coming Soon filters.
- Image-right desktop rows and image-first mobile rows.
- Four public status labels and their semantic colours.
- Horse hook, factual tags and one status-specific CTA.
- Ownership FAQ content and accordion behaviour.

**Adapt**

- Rebuild with `PageShell`, `PageIntro`, `PageSection` and `PageContainer`.
- Use V2 status tokens and named type roles.
- Put Mulan first because the ruled order starts with `available`; production does not follow that order.
- Use local fixture images and public content so no V2 listing must be published for review.
- Keep the shared nav/footer and remove the page-local footer.

**Reject**

- Production's duplicate nested `main` landmarks.
- `role="link"` on `article` with nested anchors.
- Production's sub-44px filter and FAQ controls.
- Mobile image frames wider than their card content box.
- Production's off-token card heading size and inline arbitrary transitions.
- Any page-level separator between listing and FAQ sections.

## Browser Checks

- Desktop: `1440×1000`; scroll width `1440`; exactly one `h1` and seven card/section `h2`s.
- Mobile: `390×844`; scroll width `390`; exactly one `h1` and seven card/section `h2`s.
- Six fixture images load after normal lazy loading; zero broken images.
- `Available` returns Mulan only. `Coming Soon` returns I Stole A Manolo and Lady Ketchikan.
- `All Thoroughbreds` returns six cards in the ruled order.
- Keyboard order: logo → navigation → Get Started → Ownership FAQ → filters → six CTAs → FAQ.
- Every control inside `main` meets the 44px minimum at the mobile viewport.
- Reduced motion: every reveal is visible immediately; Mulan remains the first card.
- axe: **0 violations** at desktop and mobile.
- Production comparison: 4 axe violations, including duplicate/nested main landmarks and invalid
  `role="link"` on articles.

## Scope

- Session 1 Marketplace landing only.
- Mulan remains a local fixture and is not published.
- No Marketplace data, schema, horse page, checkout or MyStable change.
- Founder visual walk remains the final acceptance gate.
