# Marketplace Horse Page Visual Parity Evidence

**Date:** 2026-11-14  
**Horse:** Mulan The Brave (NZ)  
**Production:** `https://www.evolutionstables.nz/marketplace/mulan-the-brave`  
**V2:** `http://localhost:3001/marketplace/mulan-the-brave`  
**Worktree:** `/home/evo/evolution/engine_v2-worktrees/horse-page-parity-2026-11-14`  
**Branch:** `horse-page-parity-2026-11-14` from accepted Marketplace commit `ec725c1`

## Visual Direction

Carry production's commercial page hierarchy without carrying its structural defects:

1. Breadcrumb and one horse `h1`.
2. Large gallery with previous/next controls, thumbnails, counter and full-screen viewer.
3. Compact age/sex/colour/sire/dam facts strip.
4. Campaign story followed by Overview, Pedigree, Trainer, Race Record and Documents tabs.
5. A persistent offer rail with status, price, listed stake, investor return, expiry, benefits and one ownership action.
6. A second, identical ownership action in the mobile conversion bar.
7. Global V2 navigation and footer remain unchanged.

Mulan is a local visual fixture. No listing was published, no database was written and no production
form or purchase action was submitted.

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

| Viewport | Production height | V2 height | Difference | Horizontal overflow |
|---|---:|---:|---:|---|
| 1440×1000 | 2,551px | 2,198px | -353px | None |
| 390×844 | 3,545px | 4,052px | +507px | None |

The desktop V2 page is shorter because it removes the duplicate generic page hero. Mobile is taller
because the detail tabs, campaign prose and offer benefits are presented in a single readable column,
with 72px reserved after the footer for the fixed conversion bar.

## Gallery and Page Anatomy

| Element | Production | V2 decision |
|---|---|---|
| Page heading | Generic `h1` plus horse `h1` | One horse `h1` only |
| Gallery | 16:10 main image, arrows, counter, thumbnails | Carried with local assets and 44px controls |
| Full-size image | Overlay viewer | Carried with keyboard arrows, Escape, focus trap and focus return |
| Facts | Age, sex, colour, sire, dam | Carried |
| Story | Campaign and pedigree prose | Carried |
| Detail | Five tab buttons | Carried as an accessible tablist with arrow/Home/End support |
| Offer | Price, return, benefits, CTA | Carried; listed stake and expiry added as public commercial terms |
| Mobile conversion | Required by `DESIGN.md` | Price and the same ownership action, fixed above the safe-area inset |

## Public Offer

| Field | V2 display |
|---|---|
| Listed stake | 5% |
| Retail price | $65 per 1% per month |
| Investor return | 75% of eligible gross stakes |
| Campaign term | Through Jun 2028 |
| Selection constraints | Deferred to the checkout rail; minimum, step, close style and payment model are not presented as headline offer fields |

The ownership action currently enters the account gate at `/login?next=/marketplace/mulan-the-brave`.
The purchase flow itself remains Session 3 work.

## State Contract

| Status | Public treatment |
|---|---|
| `available` | Show terms and the ownership action |
| `coming_soon` | Show status and campaign content; interest action only, never purchase |
| `fully_allocated` | Show status, campaign record and notify/waitlist action; never purchase |
| `completed` | Show status and completed campaign record; notify/waitlist action only |

Production's available Mulan page uses the account gate. Production's fully allocated and completed
pages expose `Notify Me`; its coming-soon detail route currently returns a server error, so that route
is not accepted as reference behaviour.

## Carry, Adapt, Reject

**Carry**

- Gallery-first composition with horse facts directly beneath it.
- Story plus five-part detail model.
- Sticky desktop offer rail and persistent mobile conversion path.
- Public price, return, term and status language.
- Account gate before the ownership flow.

**Adapt**

- One horse `h1`; the route no longer repeats the generic landing headline.
- Shared V2 page primitives, tokens, status badge and reveal system.
- Local public-content fixture for Mulan's three images and structured copy.
- Five visible offer terms only; order-book mechanics remain inside checkout.
- Accessible tabs and image viewer instead of production's unlabelled state model.
- Combined Investor Pack is the legal access point; PDS and SA remain its two components.

**Reject**

- Duplicate nested `main` landmarks.
- Two `h1` elements on one horse page.
- Production's low-contrast body copy and footer text.
- Sub-44px carousel and detail controls.
- A sticky bar that can cover footer content.
- A coming-soon route that fails with a server-side exception.

## Browser Checks

- Desktop `1440×1000` and mobile `390×844`: no horizontal overflow.
- Exactly one `h1`: Mulan The Brave (NZ).
- Three gallery images load; no broken images.
- Gallery lightbox opens, locks body scroll, supports arrow navigation, closes on Escape and returns
  focus to the image trigger.
- Tabs expose one selected tab and one tab panel; ArrowRight and End change selection and move focus.
- Every control inside `main` meets the 44px minimum at mobile.
- Mobile conversion bar is 69px high, uses the safe-area inset, and 72px of body padding keeps it from
  covering the footer or social links.
- Reduced motion shows the page immediately.
- axe: **0 violations** on desktop and mobile.
- Production comparison: **5 axe violations**, including duplicate nested main landmarks, invalid
  heading order and three serious contrast failures.

## Scope

- Horse-page visual implementation only.
- Checkout, purchase writes, MyStable, schema and production publishing remain untouched.
- Founder visual walk remains the acceptance gate.
