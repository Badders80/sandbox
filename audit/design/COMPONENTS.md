# Workstream C — pattern locks

The component half of the V2 `DESIGN.md`. Each component is locked at **decision level**: what it
is for, what it is made of, a CLOSED variant list, its states, the tokens it may consume, its
content rules, and its do-nots — each do-not naming the drift it caused.

**This is a working file.** It does not leave this folder. Its content is collated into
`DESIGN.md` §8 when that document is written (README §9, §13).

**Locked decisions, not markup.** Nothing below names a component file or a class string as a
rule. Live code is cited only as evidence — for what exists, and for what went wrong.

**Two markers used throughout.**

- **`adopted`** — the value is the live build's, taken as-is. Live is evidence, so this needs no
  argument.
- **`departs`** — the value differs from the live build on purpose. One line says why. §5 makes
  the live page the winner on values, so a departure is a ruling, and it has to be argued.

**Status: 6 locked** — listing card, status badge, navigation, footer, mobile conversion bar,
mobile menu drawer. Remaining: button hierarchy, figure row, form field (§9).

---

## 0 · The evidence base

Everything below is ruled from the live build at `evolution/engine/website`, read 2026-10-16, plus
`DEFECT-HISTORY-2026-10-16.md`. Verify against `evolution/engine/website`; a value found only under
`/home/evo/audit/website/` is a proposal (README §5).

Three status maps are live, and they disagree — which is why the badge is locked before the card:

| Where | Shape |
|---|---|
| `asset-lock.ts:45` | `ListingStatus` — 4 public values |
| `database.types.ts:71` | `CampaignStatus` — the Postgres type, 6 values |
| `lib/campaign-status.ts` | `CampaignStatus` **again**, 6 values, plus 5 deprecated legacy aliases |

---

## 1 · Listing card

### Name and job
The marketplace unit. One offering, presented as something a buyer can scan and open. The highest
drift exposure in the system and the one most likely to grow a second look.

### Anatomy

| Slot | Requirement |
|---|---|
| Status badge | **Required.** Top-right of the image frame (§2) |
| Image frame | **Required.** Fixed aspect, contains the badge |
| Name | **Required.** One line |
| Hook | **Required.** One short paragraph |
| CTA link | **Required.** Exactly one |
| Highlight tags | Optional. Zero to three |
| No-photo placeholder | Rendered in place of the image when there is none |

### Variants — a CLOSED list

| Variant | Difference |
|---|---|
| `standard` | The default |
| `featured` | Larger **gap** and larger image column. One per grid, at most |

**Adding a third is a ruling.**

### States
`default` · `hover` · `focus-visible` · `active` · `loading` (skeleton, same footprint) ·
`image-error` (falls back to the placeholder, never a broken frame). There is no `disabled` card:
an unsellable offering is a *status*, not an absent card.

### Tokens consumed — and only these
Surfaces: `canvas`, `surface`, `raised`. Structure: `border` at one of the three opacity steps.
Text: `heading`, `muted-foreground`, `micro`, the card-heading role, the body role. Accent: `gold`
for the CTA's hover only. Status: the badge's own three (§2). Shape: `radius-lg` outer,
`radius-md` for the image frame. Depth: `shadow-card-hover`, and nothing else. Motion: the hover
duration, hover-guarded.

### Content rules
- The name is one line. It never wraps and never truncates with an ellipsis — a horse name that
  does not fit is a name the card is wrong for.
- The hook has a fixed maximum with a hard truncation. It never expands the card's height.
- Tags are uppercase, three at most, and describe the *horse* — never the offer's terms.
- **No price, no percentage, no figures inside the card.** Financials belong to the horse page,
  where Geist Mono is the ruled face for them.
- Exactly one CTA. Its words change with intent (`View Offering`, or `Register Interest` where
  there is nothing to buy) but there is never a second action competing with it.

### Do-not
1. **Do not let siblings differ in padding.** The live build runs `p-5`, `md:p-6` and `p-8` on one
   surface. Featured differs by gap and image width. *Drift:* it makes "what is our card padding"
   unanswerable, which is how a spacing scale stops existing.
2. **Do not use Tailwind's numeric radius names.** Live uses `rounded-3xl` and `rounded-2xl` while
   the theme defines five named tiers. `DEFECT-HISTORY` #2 banned bare `rounded` for exactly this
   reason; the named tiers are the same fix, completed.
3. **Do not write the hover shadow as an arbitrary value.** Live writes
   `shadow-[0_20px_40px_rgba(0,0,0,0.45)]` while `--shadow-card-hover` holds that exact value.
   `DEFECT-HISTORY` #15 — 21 arbitrary shadows across 14 definitions.
4. **Do not use a duration off the scale.** Live transitions at 400ms. §6.5 locks the hover
   duration. *Drift:* a fourth duration nobody chose.
5. **Do not make the whole card a link.** Live puts `role="link"` on the card *and* an anchor
   inside it — two nested interactive targets, and the keyboard gets two stops to one destination.
6. **Do not hand-type the label recipe.** The live badge renders at 8px with `tracking-widest`;
   `DEFECT-HISTORY` #20 split tracking arbitrarily against a spec that named it.
7. **Do not invent an empty-grid treatment inside this component.** Empty is a grid state with its
   own copy, decided once.

---

## 2 · Status badge

### Name and job
Renders a listing's lifecycle state. **One component, one map** — ruled 2026-10-16 (README §8).

### Anatomy

| Slot | Requirement |
|---|---|
| Dot | **Required.** The semantic carrier |
| Label | **Required.** Uppercase |
| Glow | **Conditional.** The active variant only |

Pill, always. Positioned by its host, never by itself.

### The map — 6 statuses into 3 variants

Values are the database's (`database.types.ts:71`). Labels are display strings. **Not the same
thing, and not interchangeable** — `available` and `fully_allocated`, which this audit used for
weeks, exist nowhere in the code.

| Value | Label | Variant | Glow |
|---|---|---|---|
| `draft` | DRAFT | settled | no — and never public |
| `coming_soon` | COMING SOON | active | yes |
| `coming_soon_details` | COMING SOON | active | yes |
| `listed` | AVAILABLE | active | yes |
| `fully_subscribed` | FULLY ALLOCATED | pending | no |
| `completed` | COMPLETED | settled | no |

This matches `DEFECT-HISTORY` #14, which records that `fully_subscribed` was rendering white
"against a locked amber" — the amber is the long-standing intent, now the ruling.

**Variants — a CLOSED list of three:** `active` · `pending` · `settled`. The list is three, not
six: a new status picks an existing variant or forces a ruling.

### States
`focus-visible` if a host makes it interactive. The six input statuses are the state space. **An
unrecognised value is an error, not a fallback.**

### Tokens consumed — and only these
`status-active`, `status-pending`, `status-closed`, `border` at one opacity step, `surface` for the
pill fill, the glow token, `micro` for the label at weight 500 and the badge-pill tracking step
(`departs` — live renders 8px at 300 weight with `tracking-widest`; §6.4 sets a 10px floor and
`DEFECT-HISTORY` #20 makes the badge-pill tracking its own step at `0.05em`). No other colour may
appear in this component at all.

### Content rules
- The label vocabulary above is the **whole** vocabulary. Five strings.
- **A status is never a call to action.** `Become an Owner` is a live label for `listed`, in the
  same enum as `AVAILABLE`. A status answers "what is this?"; a CTA answers "what do I do?"
- `coming_soon_details` shares `coming_soon`'s label and treatment deliberately.
- Uppercase is applied by the component. Source strings stay sentence case.
- The glow marks **motion, not importance.** There is no second glow colour.

### Do-not
1. **Do not build a second status map.** Live has three, and they disagree: `listed` is `AVAILABLE`
   in the grid and `Become an Owner` in the badge; `completed` is muted grey in one, amber in
   another; `fully_subscribed` is amber in one, grey in another. `DEFECT-HISTORY` #13.
2. **Do not declare the enum twice.** `CampaignStatus` exists in `database.types.ts` and again in
   `lib/campaign-status.ts`. The badge imports the app's copy, so the database's copy is not the
   one rendering. *Drift:* two sources of truth agreeing by coincidence.
3. **Do not fall back silently on an unknown value.** Live does `statusConfig[status] ??
   statusConfig.draft` — an unknown status renders as Draft, the one state that must never be
   public. *Drift:* a closed list with a hole that fails open.
4. **Do not override the component's classes after the fact.** Live carries a
   `variantClassOverride` block whose own comment says the variant tokens are wrong and patches the
   rendered classes "per canonical style guide". The rule was known and worked around. *Drift:*
   mechanism 1, utility class over inheritance — and the override uses `/40` where the variants it
   overrides use `/30`, which is a fourth border step against `DEFECT-HISTORY` #16's three.
5. **Do not add a fourth variant** for a status that merely wants to look different.
6. **Do not give `fully_subscribed` a warning's alarm.** Amber here means demand still standing.
   Without this line the next reader will "fix" amber back to grey, which is #14 again.

---

## 3 · Batch 1 · shared rulings

Navigation, footer, the mobile bar and the drawer all consume these four. Stated once.

### 3.1 The container — `departs`

**One container for all chrome and all page content:** `max-w-6xl` (1152px), gutters `px-12
md:px-16 lg:px-20` (48 / 64 / 80).

Live runs **four** schemes:

| Surface | Live | Verdict |
|---|---|---|
| pages | `max-w-6xl px-12 md:px-16 lg:px-20` (15×) | **adopted** — the container |
| nav | `max-w-[1440px] px-6 sm:px-10 lg:px-12` (1×) | retired |
| footer | `max-w-6xl px-8 md:px-16` — no `lg` step, base of 8 | retired |
| dashboard | `max-w-7xl` (4×) | **open** — decision 7 |

**Why the departure.** `DEFECT-HISTORY` #8 is *"Hero and body grid on different gutters (`px-12`
vs `px-6`) — two left edges on one page"*, and its resolution is *"One container pattern."* The
nav's `px-6 sm:px-10 lg:px-12` against the page's `px-12` is that same defect, unfixed — the
chrome and the content disagree about where the left edge is, so the wordmark never lines up with
the headline beneath it. A 1440px nav over a 1152px page is a scheme of one.

### 3.2 The z-ladder — `new`

```
--z-grain    -1    film grain, behind everything
--z-sticky   30    mobile conversion bar
--z-nav      40    global navigation
--z-drawer   50    mobile menu drawer
--z-modal    60    dialogs, including full-screen viewers
```

Rules:
- **`nav` is below `modal`.** Live is inverted: nav `z-[9999]`, and three modal overlays at
  `z-[9990]`/`z-[9995]` open *underneath* it. One was compensated by hand, at the call site, with a
  comment that reads like a rationale — `purchase-flow-modal.tsx:171`: *"Overlay sits above the nav
  (z-[10000] > NavBar z-[9999])."* That is not a decision; it is one author working around an
  accident. Live carries 10 distinct values from `-1` to `10000`.
- `drawer` is above `nav` — a drawer covers the bar it stands in for.
- `drawer` is below `modal` — a dialog opened from the drawer must cover it.
- **No component invents a z value.** Local stacking inside a component (a badge over an image) is
  a local stacking context, not a ladder slot.

**The binding is owed, not decided.** `--z-*` is not a Tailwind v4 namespace, so these tokens
generate no utility — the trap §Workstream B names as "a hard-coded value wearing a costume". The
ladder above is the decision; the mechanism (a real utility declared with `@utility`, or
consumption as `z-[var(--z-nav)]`) settles with README §18 item 2, where the `@theme` block lives.

### 3.3 The touch law
**44px.** `DEFECT-HISTORY` #5: stepper buttons at 24×28px and a 16×16px acceptance checkbox, both
purchase-critical. Anything in the chrome that can be tapped clears it.

### 3.4 Hover guards
**Every hover rule is wrapped in `@media (hover: hover)`.** `DEFECT-HISTORY` #10: zero guards
anywhere, every hover rule shipped to every touch device, and an infinite shimmer ran on phones.
Unconditional in this batch: nav links, footer links, drawer links.

---

## 4 · Global navigation

### Name and job
The persistent top anchor, present on every route. It is the only chrome element that is always on
screen, so it is the one that most needs to never change.

### Anatomy

| Slot | Requirement |
|---|---|
| Brand mark | **Required.** Links to the site root |
| Primary links | **Required.** Two to five |
| Account or CTA slot | **Required.** One, at most |
| Menu toggle | **Required** below the collapse point |

### Variants — a CLOSED list of two

| Variant | When |
|---|---|
| `transparent` | At the top of the page |
| `solid` | Scrolled, or the menu is open |

**adopted** — live already computes exactly this (`NavBar.tsx:135-136`, `isSolid = scrolled ||
isMenuOpen`). The rule is that it stays two. A third — a light variant, a hero-specific variant —
is a ruling.

### States
`transparent` · `solid` · `menu-open` · `link-hover` (guarded) · `link-focus-visible` ·
`link-current` · `disabled` — the last only for the account slot.

### Tokens consumed
`canvas` with alpha, `border`, `heading`, `ink`, `gold` for a CTA, the label-eyebrow role for link
text, the container (§3.1), `z-nav` (§3.2), the state duration, and a named easing. Height: **80px**
(`adopted` — live `h-20`; there is no nav spec anywhere, so this is the first height decision and
there is no reason to move it).

### Content rules
- Five primary links, maximum. More than five is a footer's job.
- Labels are sentence case in source; the role uppercases them.
- One CTA, at most.
- **The brand mark is an SVG wordmark, never type.** Bw Gradual ships as vector paths and must
  never load as a web font (README §6.1).
- The current route carries `aria-current="page"`. Live already does this (`:192`) — it is
  recorded here so it is not lost in a rewrite.

### Do-not
1. **Do not set the logo in Instrument Serif, or in any font.** Instrument Serif is reserved for
   one italic gold word in a page headline (README §6.1). Setting the wordmark in it spends that
   budget on every page, in the chrome, forever.
2. **Do not hand-type the link recipe.** Live mobile links are `text-[14px] font-light
   tracking-wide` — an arbitrary size, a third weight-adjacent value, and an untokenised tracking
   step, all against `DEFECT-HISTORY` #1 (a dead class on every FAQ question) and #20.
3. **Do not use a duration off the scale.** Live is `duration-400`.
4. **Do not ship an unguarded hover.** Live nav links hover unguarded (#10).
5. **Do not write a z literal.** `z-[9999]` is why modals open under the bar (§3.2).
6. **Do not give the nav its own container.** Live's `max-w-[1440px] px-6 sm:px-10 lg:px-12` is
   `DEFECT-HISTORY` #8 unfixed (§3.1).
7. **Do not read scroll position on every frame** to drive the solid transition.

---

## 5 · Global footer

### Name and job
Secondary discovery, the closing brand statement, and the place the site stops. It is the last
thing on every page and the first thing that grows a per-page variant.

### Anatomy

| Slot | Requirement |
|---|---|
| Closing tagline block | Conditional — see variants |
| Link columns | **Required.** Two to four |
| Legal / compliance note | Conditional. **TO VERIFY** — see content rules |

### Variants — a CLOSED list of two

| Variant | When |
|---|---|
| `with-tagline` | The default |
| `links-only` | **Route-determined**, not author-chosen |

**adopted** — live suppresses the tagline on a fixed set of routes (`HERO_HIDDEN_ROUTES`, the
tagline block being founder-locked 2026-09-07). The variant is a property of the route, never a
choice made per page.

### States
`link-hover` (guarded) · `link-focus-visible` · tagline-entrance (Motion, once).

### Tokens consumed
`canvas`, `border`, `heading`, `muted-foreground` for links rising to `heading` on hover, the
label-eyebrow role for column headings, `micro` for the legal note, the container (§3.1).

Vertical padding — **asymmetric, and `adopted`:** `64px` top / `48px` bottom, and `96px` / `64px` above
the collapse point. Live is `pt-16 pb-12 md:pt-24 md:pb-16` and it is asymmetric on purpose: the
footer's top edge separates it from content, its bottom edge only has to clear the viewport. A
symmetric value here was invented once already and matched nothing. *Named spacing tokens for these
four values are owed* (README §18 item 1 — the scale past `--spacing-section` is not yet decided).

### Content rules
- Two to four link columns. Beyond four, the footer is doing the nav's job.
- Column headings are the eyebrow role. Links are never headings.
- **The compliance line is not design content and is not settled here.** A regulatory claim such
  as "Evolution Stables is an NZTR-Authorised Syndicator" carries legal weight; it is out of scope
  for this audit (README §12) and is marked **TO VERIFY** wherever it appears.

### Do-not
1. **Do not invent a symmetric padding value.** The draft reviewed on 2026-10-16 proposed
   `py-16 md:py-20`; live is asymmetric, and neither number matched anything on the page it sits
   on.
2. **Do not lock a compliance claim as a design token.** Content is out of scope, and a regulatory
   claim needs the founder's confirmation before it appears anywhere as settled text.
3. **Do not use an 800ms entrance.** Live's tagline block runs `opacity 800ms … 600ms` delay.
   `DEFECT-HISTORY` #12 already reduced the hero's entrance to 0.2s / 0.32s for LCP — the footer's
   entrance is a Motion decision and is owed (README §7 row 9), not a value this lock invents.
4. **Do not ship an unguarded hover** (#10).
5. **Do not give the footer its own gutter.** Live's `px-8 md:px-16` is a scheme of one — no `lg`
   step, and a base of 8 where every page uses 12 (§3.1).

---

## 6 · Mobile conversion bar

### Name and job
The persistent conversion anchor on a horse page, below the collapse point, where the desktop
investment rail is stacked out of sight.

**This component is invented on purpose.** `DEFECT-HISTORY` #6: *"No sticky mobile CTA on the horse
page; the primary CTA sat at the end of a single-column scroll."* The bridge wrote a `.sticky-buy-bar`
class for it — a class that exists in no live file, and the reason to keep the requirement anyway is
the defect, not the class.

### Anatomy

| Slot | Requirement |
|---|---|
| Price line | **Required** |
| Primary CTA | **Required** |

### Variants — a CLOSED list of one
There is one bar. A second — a variant per campaign status, a variant for a sold-out offering —
is a ruling.

### States
`default` · `pressed` · `hidden` above the collapse point. Never `hover` — it is a touch surface.

### Tokens consumed
`surface` with alpha, `border`, the label-spec role and the financial role (mono, weight 500) for
the price, the primary button (§9, owed), `z-sticky` (§3.2), the container's gutter (§3.1).

**Departures, both argued:**
- **Bottom inset compensation is required** — `env(safe-area-inset-bottom)`. Live has no `env()`
  anywhere in the estate. A fixed bar at the bottom of a phone with a home indicator sits under it.
- **The page must reserve the bar's height** as bottom padding on the scrolling container. A fixed
  bar covers the last element of the document otherwise, and a buyer can end up unable to reach the
  final row — the same shape as `DEFECT-HISTORY` #7, a rail overflowing its column.

### Content rules
- The price line shows the current share price. It never shows a figure the horse page contradicts.
- The CTA is the same action and the same words as the rail's. **One modal, two triggers.**
- The bar is never the *only* route to purchase. It is a second one.
- Nothing else goes in the bar. No navigation, no status, no dismiss control.

### Do-not
1. **Do not name a hook or a function.** A spec that pins exact JSX rots the first time React
   shifts; the decision is "opens the same purchase modal the rail opens."
2. **Do not build a second trigger implementation.** Two implementations of one action is
   `DEFECT-HISTORY` #13's shape, and it is how the badge problem started.
3. **Do not let the bar outrank a modal.** Live's inversion put modals under the nav; the bar is
   lower still (§3.2).
4. **Do not ship a hover state.** #10 — hover rules on touch surfaces.
5. **Do not let the CTA fall below 44px** (#5), and do not disable it to signal a status. A greyed
   button says the opposite of what is meant.

---

## 7 · Mobile menu drawer

### Name and job
Navigation below the collapse point. Pulled out of the nav as its own component — a focus trap,
an Esc handler and a scroll lock are a component's worth of work, not a nav sub-bullet.

### Anatomy

| Slot | Requirement |
|---|---|
| Primary links | **Required.** The nav's links |
| Account or CTA slot | Optional. Mirrors the bar's |
| Toggle | **Required.** Owned by the nav (§4) |

### Variants — a CLOSED list of one

**Shape — `adopted`.** The drawer is a **panel anchored under the bar**, not a full-screen overlay
sheet. Live is a dropdown panel; the overlay sheet was a bridge invention with no argument behind
it. Live is evidence, so the panel is kept, and the work here is the accessibility it is missing.

### States
`closed` · `open` · `link-hover` (guarded) · `link-focus-visible` · `link-current`

### Behaviour — required, not optional
- **Focus trap** while open.
- **Esc closes** it and returns focus to the toggle.
- **Body scroll lock** while open.
- `aria-expanded` on the toggle — live already has this (`:234`).
- `aria-controls` pointing at the panel — live does **not** have this.
- The toggle is a button that opens a disclosure. It is **not** a dialog.
- Links clear the 44px touch law (#5).

### Tokens consumed
`canvas` or `raised` for the panel, `border`, `heading`, `ink`, the label role for links,
`z-drawer` (§3.2).

### Content rules
- The panel carries the nav's links and nothing else. It is not a second footer.
- Labels match the nav's exactly. Two vocabularies for one link is a drift.

### Do-not
1. **Do not make it an `aria-modal` dialog.** Live disabled a coming-soon interception on
   2026-10-01 precisely because it "put a second `aria-modal` dialog on the page"
   (`marketplace-listing-grid.tsx`). A drawer is a disclosure, not a dialog.
2. **Do not let focus escape to the page behind it.**
3. **Do not hand-type the link recipe.** Live mobile links are `px-4 py-3.5 text-[14px]
   tracking-wide` — arbitrary size and untokenised tracking (#1, #20).
4. **Do not ship an unguarded hover** (#10).
5. **Do not give the drawer its own collapse point.** It, the nav and the bar share one (§8).

---

## 8 · One collapse point

The nav's toggle, the drawer and the conversion bar all appear and disappear at the same width.
**That width is 768px**, and it is one token consumed by all three — never three literals.

`departs`: live's drawer has no stated breakpoint, and README §7 row 10 leaves breakpoints open. The
broader breakpoint tokenisation stays open; the *chrome* collapses at one value, and having one
value is the entire point.

---

## 9 · Still to lock

| # | Component | Blocked on |
|---|---|---|
| 1 | **Button hierarchy** | The **elevation ruling** (README §7 row 8, Open decision 5). A primary button's pressed state and the gold hover both want a shadow decision that is not made. **This ruling comes first** — the bar's CTA (§6) and every modal consume it, and it is the last thing standing between Workstream C and done |
| 2 | **Figure row** | Nothing. The mono-figures pattern at weight 500; Geist Mono is already ruled onto financials |
| 3 | **Form field** | Nothing. Buyer and operator inputs share a look; the error state is the drift risk |

**Two jobs that are not components and are owed by these locks:**

- **Consolidate the accordion.** Live ships `ui/CollapsePanel.tsx` and `ui/AccordionList.tsx` against
  a rule that permits one implementation (README §6.5). One survives, and it is the STEP1
  `CollapsePanel` — pure grid rows, no JS measurement. This is `DEFECT-HISTORY` #13's shape a second
  time, and it is not on the six-item list because the six-item list did not know it existed.
- **Name the spacing tokens and the easing.** The footer's four vertical values (§5), the chrome's
  heights, and one easing consumed by the nav and the bar (§4, §6). The easing is Motion granularity
  (README §7 row 9); the spacing is README §18 item 1. Both are *named*, not invented — the values
  above are already decided; only the token names are owed.
