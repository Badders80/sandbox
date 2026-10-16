# Step 2 — Marketplace Page Audit (`/marketplace`)

**Audit date:** 2026-10-15
**Source:** `evolution/engine/website/apps/web/src/app/marketplace/page.tsx`, `marketplace-listing-grid.tsx`, `campaign-status-badge.tsx`, `marketplace-cta.tsx`, `OwnershipFAQSection.tsx`, `horse-page-shell.tsx`
**Frame:** New elements and deviations from Step 1. Conflicts and gaps flagged explicitly.

> **Corrected 2026-10-16 — read this before citing.** §1's status table (`:50-55`) is the **old
> build's** map and is **superseded**: `fully_subscribed` is amber, not muted grey, and `completed`
> is slate. The ruling is `COMPONENTS.md` §2. The *names* in that table were right and this audit's
> own were not — `available` and `fully_allocated` exist nowhere in the code.
>
> **All four questions in §5 are answered**: one badge component and one map (README §8); 64px
> intentional and kept (Q1 — the look stays); the card-hover shadow tokenised as
> `--shadow-card-hover` (§6.5); and `coming_soon` stays green on `status-active` (not amber).
>
> The four tokens proposed in §4 all landed: `--shadow-card-hover` is locked (§6.5);
> `--text-display` and `--tracking-display` are **owed names** for the 64px heading and its
> `-0.04em` (§6.4); `--tracking-tag` is the `0.05em` step, now shared with the status badge (§6.2).
>
> §1's radius note is **correct** and was re-checked: `rounded-2xl` really does render 24px, because
> the theme declares `xl`/`2xl`/`3xl` as aliases onto `lg` (§6.5).

---

## 1 · New patterns not on the landing page

### Listing card (MarketplaceListingGrid)

The primary new component. Specific patterns:

**Card anatomy:**
- `rounded-3xl` on outer card — **this is `24px`**, matching `--radius-lg` in the token system. Not new.
- `rounded-2xl` on image inner frame — Tailwind default `16px`, which aliases to `--radius-xl` → `24px` (per the token comment about `2xl/3xl` falling through). Confirmed: `radius-2xl` = `24px` in practice.
- Status badge: absolute positioned top-right, `rounded-full`, `backdrop-blur-md`
- Status dot: `h-1.5 w-1.5` (24px grid), glow shadow when active (`shadow-[0_0_8px_var(--shadow-success-glow)]`)

**Card hover behaviour:**
- `hover:-translate-y-1` — card lifts 1 unit on hover
- `hover:shadow-[0_20px_40px_rgba(0,0,0,0.45)]` — **new shadow value, not in the token system**
- Image: `opacity-90` → `opacity-100` on hover
- CTA arrow: `group-hover:translate-x-1` — slides right

**Highlight tags:**
- `rounded-full border border-border bg-surface px-3 py-1 text-micro font-light uppercase tracking-wider`
- Uses `--text-micro` (10px) — this is the only use of the micro token on the marketplace page
- `tracking-wider` — this is a Tailwind utility, equivalent to `letter-spacing: 0.05em`. This is a different tracking value than any label role (0.2em for labels)

**Featured card variant:**
- Larger padding: `md:p-8` vs `md:p-6`
- Larger gap: `md:gap-12` vs `md:gap-8`
- Hook text: `text-[14px]` vs `text-[13px]`

### Filter tabs

Three tabs: All Thoroughbreds / Available / Coming Soon.

- Active tab: `text-heading` + bottom hairline `h-px bg-foreground`
- Inactive: `text-muted-foreground hover:text-foreground`
- No pill, no background — pure text + hairline indicator
- Border bottom spans the container: `border-b border-border`

### Status badge colours (MarketplaceListingGrid)

Marketplace defines its own `STATUS_META` map — overrides the standard badge:

| Status | Label | Badge classes | Dot |
|---|---|---|---|
| `listed` | Available | `border-status-active/40 bg-status-active/10 text-status-active` | `bg-status-active` + glow |
| `coming_soon` | Coming Soon | `border-status-active/40 bg-status-active/10 text-status-active` | `bg-status-active` + glow |
| `fully_subscribed` | Fully Allocated | `border-border bg-card text-muted-foreground` | `bg-muted-foreground` |
| `completed` | Completed | `border-border bg-card text-muted-foreground` | `bg-muted-foreground` |

**Note:** The `STATUS_META` map diverges from the `campaign-status-badge.tsx` status config. Both exist:
- `campaign-status-badge.tsx` — used on the horse page shell (`right-rail`)
- `MarketplaceListingGrid`'s own `STATUS_META` — used on the marketplace index

These two should be unified. Confirmed **gap/conflict**: two separate status rendering systems for the same underlying enum.

### OwnershipFAQSection

Identical in structure to `FAQSection` on the landing page:
- Same `CollapsePanel` component
- Same `reveal()` pattern
- Same label structure
- **Content differs**: ownership mechanics (DSL, float, prize money, trainer authority) vs storefront FAQ

### Page heading

```tsx
<h1 className="mt-4 text-[36px] font-light tracking-[-0.04em] text-heading md:text-[64px] leading-[1.05]">
```
- `tracking-[-0.04em]` — **new tracking value**, not in the type system. This is the display heading on the marketplace page.
- `md:text-[64px]` — **new type size**, not in the scale (max is `48px`)

### Hero tagline link

```tsx
className="text-accent underline decoration-accent/40 underline-offset-4 transition-colors hover:text-heading"
```
- `underline decoration-accent/40` — gold underline at 40% opacity. New decorative pattern.
- `hover:text-heading` — underline stays gold but text shifts to heading colour on hover.

---

## 2 · Confirmed same as landing page (no conflict)

| Pattern | Value | Same as Step 1? |
|---|---|---|
| Section padding | `py-section` = `224px` | ✅ |
| Container | `max-w-6xl`, `px-12` to `px-20` | ✅ |
| `.label-eyebrow` | 11px/300/0.2em uppercase | ✅ |
| `text-muted-foreground` | `#7c7c7c` | ✅ |
| `text-heading` | `#f8fafc` | ✅ |
| `border-border` | `rgba(255,255,255,0.1)` | ✅ |
| Gold CTA link | `text-accent hover:text-heading` | ✅ |
| Accordion animation | `CollapsePanel`, `duration-300` | ✅ |

---

## 3 · Conflicts and gaps

### Conflict 1: Status badge systems (CRITICAL)

Two independent implementations of the same status enum:
- `campaign-status-badge.tsx` — badge + variant class override system
- `MarketplaceListingGrid`'s own `STATUS_META` — parallel map with different class choices

The two systems produce different visual results for the same status. This needs to be resolved: one badge component, one source of truth.

### Conflict 2: Page heading size

The marketplace page uses `md:text-[64px]` for the main heading. The type scale maxes at `48px` (`--text-section-heading-wide`). This is a deliberate deviation — 64px is used for the marketing "hero" feel on the marketplace heading.

### Gap: Shadow value not tokenised

`hover:shadow-[0_20px_40px_rgba(0,0,0,0.45)]` — used on listing card hover. This is not in the token system. Should either be added to `--shadow-*` tokens or removed.

### Gap: Tracking value not tokenised

`tracking-[-0.04em]` on the marketplace heading — same value appears in Warp's design spec. Confirmed as a real pattern but not in the token scale.

### Gap: Highlight tag tracking

`tracking-wider` (≈ `0.05em`) on tag labels — not a named label role. Uses `--text-micro` (10px) but with different tracking than the spec label role (`0.2em`).

---

## 4 · New tokens surfaced

| Token needed | Proposed value | Source |
|---|---|---|
| `--text-display` | `64px` | Marketplace heading |
| `--tracking-display` | `-0.04em` | Marketplace heading |
| `--shadow-card-hover` | `0 20px 40px rgba(0,0,0,0.45)` | Listing card hover |
| `--tracking-tag` | `0.05em` (Tailwind `tracking-wider`) | Highlight tags |

---

## 5 · Elements to confirm in review

1. Is `64px` for the marketplace heading intentional? It exceeds the type scale by 16px.
2. Should the status badge system be unified into one component?
3. Should the card hover shadow be tokenised or removed?
4. Is `coming_soon` badge using the `success`/`status-active` variant correct, or should it use `warning`/`pending`?
