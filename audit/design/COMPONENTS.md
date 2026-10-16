# Workstream C — pattern locks

The component half of the V2 `DESIGN.md`. Six components, each locked at **decision level**: what
it is for, what it is made of, a CLOSED variant list, its states, the tokens it may consume, its
content rules, and its do-nots — each do-not naming the drift it caused.

**This is a working file.** It does not leave this folder. Its content is collated into
`DESIGN.md` §8 when that document is written (README §9, §13).

**Locked decisions, not markup.** A spec that pins exact JSX rots the first time React or Tailwind
shifts, people route around it, and routing around it is how the drift started. Nothing below names
a component file or a class string as a rule; it names the decision, and cites the live code only
as evidence for why the decision exists.

**Status: 2 of 6 locked.** Listing card and status badge. Button hierarchy, figure row, nav/footer
and form field remain — see the end of this file.

---

## 0 · The evidence base

Everything below is ruled from the live build at `evolution/engine/website`, read 2026-10-16, plus
`DEFECT-HISTORY-2026-10-16.md`. The three status maps actually in the code:

| Where | Shape | Used by |
|---|---|---|
| `asset-lock.ts:45` | `ListingStatus` — 4 public values | `marketplace-listing-grid.tsx` |
| `database.types.ts:71` | `CampaignStatus` — the Postgres type, 6 values | the DB schema |
| `lib/campaign-status.ts` | `CampaignStatus` again, 6 values, plus `CampaignStatusLegacy` (5 deprecated aliases) | `campaign-status-badge.tsx` |

**The same six values are declared twice under the same type name, in two packages.** Both agree
today. Nothing makes them agree tomorrow. That is finding one of the two components below, and it
is why the badge is locked before the card.

---

## 1 · Listing card

### Name and job
The marketplace unit. One offering, presented as something a buyer can scan and open. It is the
highest drift-exposure component in the system and the one most likely to grow a second look.

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

**Adding a third is a ruling.** The featured variant is differentiated by *proportion*, never by
padding — see the first do-not.

### States
`default` · `hover` · `focus-visible` · `active` · `loading` (skeleton, same footprint) ·
`image-error` (falls back to the placeholder, never to a broken frame). There is no `disabled`
card: an unsellable offering is a *status*, not an absent card.

### Tokens consumed — and only these
Surfaces: `canvas`, `surface`, `raised`. Structure: `border` at one of the three opacity steps.
Text: `heading`, `muted-foreground`, `micro`, the card-heading role, the body role. Accent: `gold`
for the CTA's hover only. Status: the badge's own three (§2). Shape: `radius-lg` outer,
`radius-md` for the image frame. Depth: `shadow-card-hover`, and nothing else. Motion: the hover
duration.

### Content rules
- The name is one line. It never wraps to two and never truncates with an ellipsis — a horse name
  that does not fit is a name the card is wrong for.
- The hook is a fixed maximum with a hard truncation. It never expands the card's height.
- Tags are uppercase, three at most, and describe the *horse* — never the offer's terms.
- **No price, no percentage, no figures inside the card.** Financials belong to the horse page,
  where Geist Mono is the ruled face for them. A price on the card invites a second price style,
  and then a third.
- Exactly one CTA. Its words change with intent (`View Offering`, or `Register Interest` where
  there is nothing to buy) but there is never a second action competing with it.

### Do-not
1. **Do not let siblings differ in padding.** The live build does: `p-5`, `md:p-6`, and `p-8` on
   the featured card, so two cards on one surface carry two padding values. Featured differs by
   gap and image width. *Drift caused:* it makes "what is our card padding" unanswerable, which is
   how a spacing scale stops existing.
2. **Do not use Tailwind's numeric radius names.** The live build uses `rounded-3xl` and
   `rounded-2xl` while the theme defines five named tiers. Same pixels today; the moment the scale
   moves, one of the two stops following it. *Drift caused:* two radius vocabularies for one scale.
3. **Do not write the hover shadow as an arbitrary value.** The live build writes
   `shadow-[0_20px_40px_rgba(0,0,0,0.45)]` even though `--shadow-card-hover` is the locked token for
   exactly this, at exactly that value. That is one of 21 arbitrary shadows across 14 values found
   in the estate (`AUDIT-MISSING-PRIMITIVES`). *Drift caused:* the token exists and is bypassed, so
   the token is decoration.
4. **Do not use a duration off the scale.** The live card transitions at 400ms; §6.5 locks the
   hover duration. *Drift caused:* a fourth duration nobody chose.
5. **Do not make the whole card a link.** The live build puts `role="link"` on the card *and* an
   anchor inside it, so one card is two nested interactive targets and a keyboard user gets two
   stops with the same destination. One link. The card surface is not itself a link.
6. **Do not hand-type the label recipe.** The live badge renders at 8px with `tracking-widest`;
   the locked label roles are 11px at `0.2em`. *Drift caused:* mechanism 6 — the recipe existed as
   a class, so it was retyped per page, and this one was retyped wrong.
7. **Do not invent a treatment for an empty grid inside this component.** Empty is a grid state
   with its own copy, decided once.

---

## 2 · Status badge

### Name and job
Renders a listing's lifecycle state. **One component, one map** — ruled 2026-10-16 (README §8).

### Anatomy

| Slot | Requirement |
|---|---|
| Dot | **Required.** The semantic carrier |
| Label | **Required.** Uppercase |
| Glow | **Conditional.** Present on the active variant only |

Pill, always. Positioned by its host, never by itself — it does not know it lives on a card.

### The map — 6 statuses into 3 variants

The values are the database's (`database.types.ts:71`). The labels are display strings. **They are
not the same thing, and they must not be interchanged.**

| Value | Label | Variant | Glow |
|---|---|---|---|
| `draft` | DRAFT | settled | no — and never public |
| `coming_soon` | COMING SOON | active | yes |
| `coming_soon_details` | COMING SOON | active | yes |
| `listed` | AVAILABLE | active | yes |
| `fully_subscribed` | FULLY ALLOCATED | pending | no |
| `completed` | COMPLETED | settled | no |

**Variants — a CLOSED list of three:** `active` (green + glow) · `pending` (amber, no glow) ·
`settled` (slate, no glow). The closed list is three, not six: statuses map onto variants, and a
new status picks an existing variant or forces a ruling. That is the whole mechanism.

### States
`focus-visible` (it is not interactive; it inherits the ring if a host makes it so). The six input
statuses are the state space. **An unrecognised value is an error, not a fallback** — see do-not 3.

### Tokens consumed — and only these
`status-active`, `status-pending`, `status-closed`, `border` at one opacity step, `surface` for the
pill fill, the glow token, and the label-action role. No other colour may appear in this component,
at all.

### Content rules
- The label vocabulary above is the **whole** vocabulary. Five strings.
- **A status is never a call to action.** `Become an Owner` is one of the live labels for `listed`,
  in the same enum as `AVAILABLE`. A status answers "what is this?"; a CTA answers "what do I do?".
  Mixing them is why the same offering reads as two different things across two pages.
- `coming_soon_details` shares `coming_soon`'s label and treatment deliberately. The term-sheet
  variant is an internal distinction and is never shown as a second look.
- Uppercase is applied by the component. Source strings stay sentence case.
- The glow marks **motion, not importance**. Only the two still-going statuses carry it; a settled
  state is flat. There is no second glow colour.

### Do-not
1. **Do not build a second status map.** The live build has three, and they disagree: `listed` is
   `AVAILABLE` in the card grid and `Become an Owner` in the badge; `completed` is muted grey in one
   and amber in the other; `fully_subscribed` is amber in one and grey in the other. *Drift caused:*
   `DEFECT-HISTORY` #13, two implementations of one enum — and the two disagree about what the enum
   means.
2. **Do not declare the enum twice.** `CampaignStatus` exists in `database.types.ts` and again in
   `lib/campaign-status.ts`, both six values. The app's copy is the one the badge imports, so the
   database's copy is not the one rendering. *Drift caused:* two sources of truth that agree by
   coincidence.
3. **Do not fall back silently on an unknown value.** The live badge does `statusConfig[status] ??
   statusConfig.draft`, so a status the map has never heard of renders as Draft — the one state
   that must never appear in public. *Drift caused:* a closed variant list with a hole in it, and
   the hole fails open.
4. **Do not override the component's own classes after the fact.** The badge carries a
   `variantClassOverride` block whose own comment says the variant tokens are wrong and the
   rendered classes are patched "per canonical style guide". The rule was known and worked around
   instead of fixed. *Drift caused:* mechanism 1, utility class over inheritance — and worse, the
   override uses a different opacity step than the variants it overrides, so both are live.
5. **Do not add a fourth variant** for a status that merely wants to look different.
6. **Do not give `fully_subscribed` a warning's alarm.** Amber here means demand still standing,
   not danger — the ruling is recorded in README §6.3, and without it the next reader will "fix"
   amber back to grey.

---

## 3 · Still to lock

In priority order (README §8). Each is a ruling, not a restyle.

| # | Component | Why it is the risk |
|---|---|---|
| 3 | **Button hierarchy** | Primary, secondary, and disabled/loading forms of each. The estate has 21 arbitrary shadows; buttons are where the next one gets born |
| 4 | **Figure row** | The mono-figures pattern. Weight 500. A token decision, not a styling choice — Geist Mono is ruled onto financials |
| 5 | **Nav and footer** | Shared across every page, so the first place a per-page variant appears. `NavBar` already runs its own container scheme, separate from every page |
| 6 | **Form field** | Buyer and operator inputs share a look; the error state is the drift risk |

**One open question blocks #3.** The button hierarchy depends on the elevation scale (§7 row 8,
Open decision 5) — a primary button's pressed state and the `gold` hover both want a shadow
decision that is not made yet. That ruling comes first.
