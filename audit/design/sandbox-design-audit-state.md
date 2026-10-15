# sandbox-design-audit-state

## Audit handoff — 2026-10-16

STEP1 is closed and clean. STEP2 and STEP3 have open items.

---

## What's closed

### STEP1 — Landing Page (`/`) ✅

Source: `STEP1-LANDING-PAGE.md`
Status: complete, clean, no open conflicts.

Key deliverables locked:
- 5 colour tokens (canvas, surface, raised, border, edge)
- 7 type roles (micro 10px → section-heading-wide 48px)
- 2 label roles (.label-eyebrow, .label-action)
- Motion: CollapsePanel, 300ms
- Section padding: `py-section` = 224px

---

## What's open

### STEP2 — Marketplace (`/marketplace`) ⚠️ CRITICAL

Source: `STEP2-MARKETPLACE.md`

#### §3 — Conflicts and gaps

**Conflict 1 (CRITICAL): Status badge systems — two implementations**

Two independent implementations of the same `public.status` enum:
- `campaign-status-badge.tsx` — badge + variant class override system (used on horse page shell / right rail)
- `MarketplaceListingGrid`'s own `STATUS_META` map (used on marketplace index)

Both exist in the same codebase. They produce different visuals for the same status values:
- `listed` → Available: both use status-active green, but different opacity/class combos
- `coming_soon` → Coming Soon: both use status-active, dot has glow
- `fully_subscribed` → Fully Allocated: both use muted
- `completed` → Completed: both use muted

The two systems must be unified into **one badge component with one source of truth**.

**Conflict 2: Page heading size**
`md:text-[64px]` on the marketplace heading — exceeds the type scale (max 48px). Deliberate marketing/hero deviation.

**Gap: Shadow not tokenised**
`hover:shadow-[0_20px_40px_rgba(0,0,0,0.45)]` on listing card — not in the token system.

**Gap: Tracking not tokenised**
`tracking-[-0.04em]` on marketplace heading — confirmed real pattern, not in token scale.

**Gap: Highlight tag tracking**
`tracking-wider` (0.05em) on tag labels — not the spec label role (0.2em).

#### §4 — New tokens surfaced

| Token | Proposed value | Source |
|---|---|---|
| `--text-display` | `64px` | Marketplace heading |
| `--tracking-display` | `-0.04em` | Marketplace heading |
| `--shadow-card-hover` | `0 20px 40px rgba(0,0,0,0.45)` | Listing card hover |
| `--tracking-tag` | `0.05em` | Highlight tags |

#### §5 — Review questions

1. Is 64px for the marketplace heading intentional? (exceeds type scale by 16px)
2. Should the status badge systems be unified into one component?
3. Should the card hover shadow be tokenised or removed?
4. Is `coming_soon` badge using `status-active`/green correct, or should it use `warning`/pending?

---

### STEP3 — MyStable (`/mystable`) ⚠️ HIGH

Source: `STEP3-MYSTABLE.md`

#### §3 — Conflicts with the token system

**Conflict 1 (HIGH): `font-semibold` (600) not defined**
Weight system only defines 300 and 500. All financial figures use `font-semibold` (600). If intentional, token system needs `--font-weight-semibold: 600`.

**Conflict 2 (HIGH): `text-purple-400` not tokenised**
One use: the 5×M unit value. Raw Tailwind class. Should be a named token or replaced with existing token.

**Conflict 3 (LOW): Dashboard heading tracking**
`tracking-tight` on page heading — not a named token.

#### §4 — New tokens surfaced

| Token | Proposed value | Source |
|---|---|---|
| `--font-weight-semibold` | `600` | Financial figures in MyStable |
| `--color-purple-400` (or named 5×M accent) | `≈ #c084fc` | 5×M value only |
| `--shadow-success-glow` | `0 0 20px rgba(16, 185, 129, 0.35)` | Checkout success banner |
| `--shadow-modal` | `0 0 120px rgba(0,0,0,0.98)` | Billing dialog, CTA modal |
| `--color-status-active-10` | `rgba(16, 185, 129, 0.1)` | Success banners |
| `--color-accent-10` | `rgba(212, 169, 100, 0.1)` | Billing pill active state |

#### §5 — Review questions

1. Is `font-semibold` (600) intentional for financial figures?
2. Is `text-purple-400` correct for the 5×M display? Should it be a named token?
3. Should stat card gap (`gap-4`) be tokenised?
4. Is `aspect-[16/10]` intentional for the holdings card image?
5. Should `shadow-success-glow` be a formal token or stay as a CSS variable?

---

## Source files

The actual `.tsx` source files were not present in this sandbox. The audit was run on a different codebase state (the `evolution/engine/website/` path cited in the docs). The source files to resolve the badge conflict are:

- `campaign-status-badge.tsx` — horse page shell (right rail)
- `marketplace-listing-grid.tsx` — marketplace index (has its own STATUS_META)

Locate these in the actual repo before resolving Conflict 1.

---

## Next action

1. **CRITICAL first:** resolve Conflict 1 in STEP2 — unify the two status badge systems into one component. Requires reading the actual `.tsx` files.
2. Answer the §5 review questions for STEP2 (4 questions).
3. Answer the §5 review questions for STEP3 (5 questions).
4. Once all review questions answered → write the final `DESIGN.md` and `globals.css` `@theme` block (Workstreams E + B).
