# Step 3 — MyStable Dashboard Audit (`/mystable`)

**Audit date:** 2026-10-15
**Source:** `evolution/engine/website/apps/web/src/app/mystable/page.tsx`, `mystable-dashboard.tsx`
**Frame:** New elements and deviations from Steps 1 and 2. Conflicts and gaps flagged explicitly.

> **Corrected 2026-10-16 — read this before citing.** Three of §5's five questions are answered
> elsewhere: `font-semibold` maps to **500** (`DEFECT-HISTORY` #18), `text-purple-400` is **purged**
> (#17), and `shadow-success-glow` is folded into `--shadow-glow-success` (#21 — note the name flip:
> this file writes `success-glow`, the defect log writes `glow-success`; one token, two orders).
>
> §2's label-role rows are the most complete in the folder and were used to correct README §6.2:
> `.label-spec` is live at weight **400**, which the "300 and 500 only" rule did not admit. That
> makes the weight scale three values, not two.
>
> Still genuinely open here: the `aspect-[16/10]` holdings image (Q4), the `gap-4` stat-card step
> (Q3), and the alpha-fill tokens §4 proposes — `--color-status-active-10` and `--color-accent-10`.

---

## 1 · New patterns not on Steps 1 or 2

### Tab navigation (bottom border style)

Dashboard uses a tab bar with bottom-border indicator — different from any nav or filter pattern on the landing page or marketplace:

```tsx
className={`label-action pb-3 px-4 transition-colors border-b-2 ${
  activeTab === tab
    ? 'border-accent text-accent font-medium'
    : 'border-transparent text-muted-foreground hover:text-foreground'
}`}
```
- Active: `border-b-2 border-accent`, `text-accent`, `font-medium` (500)
- Inactive: `border-transparent`, `text-muted-foreground`
- Same `.label-action` base class as other action labels

### Stat cards (four-column grid)

```tsx
<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
  <div className="rounded-xl border bg-card p-5">
```
- `rounded-xl` — **24px** (same as `--radius-lg`)
- `border` — no explicit class, uses `--color-border` default
- `bg-card` — `--color-surface` alias
- **New:** `gap-4` (16px) — not used on landing or marketplace
- Active vs empty state distinction: `opacity-70` + `border-border/60` on empty cards

### Financial typography

Every numeric value uses `font-mono` (Geist Mono) + `font-semibold` (600):

```tsx
<span className="text-card-heading font-semibold font-mono text-foreground">
  ${Number(holding.stake_percentage).toFixed(2)}%
</span>
```

Also:
```tsx
<span className="text-card-heading font-semibold font-mono text-accent">
  {/* stake percentage */}
</span>
<span className="text-card-heading font-semibold font-mono text-purple-400">
  {/* 5×M value */}
</span>
```

**Conflict: `--font-weight-semibold` is not defined.** The token system defines only `--font-weight-light: 300` and `--font-weight-medium: 500`. `font-semibold` = 600 is used here and is not in the token system.

### 5×M display value

```tsx
<span className="text-card-heading font-mono font-semibold text-purple-400">
  ${pricing.joinFloatUnitNzd.toLocaleString()}
</span>
```

`text-purple-400` — **raw Tailwind class, not a token.** This is the only use of a purple accent on the page. Confirmed gap: no token for `purple-400`.

### Status chip (KYC)

```tsx
<span className="rounded-md border border-status-active/40 bg-status-active/10 px-2.5 py-1 text-label font-medium text-status-active">
```
Same pattern as badge variants in Step 1, but applied directly inline.

### Checkout success banner

```tsx
<div className="rounded-2xl border border-status-active/40 bg-status-active/10 p-6 shadow-[var(--shadow-success-glow)]">
```
Uses the CSS variable `var(--shadow-success-glow)` from `globals.css` (defined as `0 0 20px rgba(16, 185, 129, 0.35)`). Confirmed: this is the first use of a named shadow token in the audit series.

### Holdings card

```tsx
<div className="rounded-2xl border border-border bg-card overflow-hidden">
```
- `rounded-2xl` = `24px` (same as `--radius-lg` / `--radius-xl`)
- Inner grid: `grid lg:grid-cols-12` — two columns, 4/8 split
- Image: `aspect-[16/10]` — aspect ratio not seen before
- Data grid inside: `grid grid-cols-2 sm:grid-cols-4 gap-3 rounded-xl border border-border bg-background p-4`

### Billing pills (segmented control)

```tsx
<div className="inline-flex rounded-md border border-border bg-background p-0.5">
  <button className={`rounded px-3.5 py-1 ${
    scope === segment
      ? 'bg-accent/10 text-accent'
      : 'text-muted-foreground hover:text-foreground'
  }`}>
```
- `rounded-md` — 16px
- `bg-accent/10` — gold at 10% opacity as active pill fill
- Same segmented control pattern used for LIVE/ALL toggle

### Billing dialog

```tsx
<div className="pointer-events-auto relative w-full max-w-[520px] rounded-xl border border-border bg-canvas shadow-[0_0_120px_rgba(0,0,0,0.98)]">
```
- Same shadow value as CTA modal on the landing page
- Same `backdrop-blur-[4px]` + `bg-canvas/80` overlay

### Vault section

Same card style: `rounded-xl border border-border bg-card p-6` as MyStable cards.

### Legal document download row

```tsx
<div className="flex flex-col sm:flex-row sm:items-center justify-between rounded-lg border border-border bg-background p-4 gap-4">
```
- `rounded-lg` — 16px (same as `--radius-md`)
- `bg-background` — `--color-canvas` alias

---

## 2 · Confirmed same as previous steps

| Pattern | Value | Same as Step 1/2? |
|---|---|---|
| `.label-eyebrow` | 11px/300/0.2em | ✅ |
| `.label-action` | 11px/500/0.2em | ✅ |
| `.label-spec` | 10px/400/0.2em + mono | ✅ |
| Section padding | `py-section` = `224px` | ✅ |
| `text-heading` | `#f8fafc` | ✅ |
| `text-muted-foreground` | `#7c7c7c` | ✅ |
| `border-border` | `rgba(255,255,255,0.1)` | ✅ |
| `text-accent` / `bg-accent` | `#d4a964` | ✅ |
| Gold hover | `hover:bg-gold-hover` / `hover:text-heading` | ✅ |
| `rounded-xl` | `24px` | ✅ |
| `rounded-2xl` | `24px` (aliased via `--radius-xl`) | ✅ |
| Accordion | `CollapsePanel`, `duration-300` | ✅ |
| `text-card-heading` | `18px` | ✅ |
| `text-body-small` | `15px` | ✅ |
| `text-body` | `16px` | ✅ |

---

## 3 · Conflicts with the token system

### Conflict 1: `font-semibold` (600) not defined (HIGH)

The weight system only defines 300 and 500. Every financial figure in MyStable uses `font-semibold` (600). This is the first time 600 has appeared as an explicit class in the audit series.

### Conflict 2: `text-purple-400` not tokenised (HIGH)

One use: the 5×M unit value. Not a named token. Should either be added to the accent palette or the value should be changed to use an existing token.

### Conflict 3: Dashboard page heading uses `tracking-tight` and `md:text-[48px]` (LOW)

Same scale as the landing page section headings. `tracking-tight` = `letter-spacing: -0.025em` approximately — not a named token but consistent with the display heading convention.

---

## 4 · New tokens surfaced

| Token needed | Proposed value | Source |
|---|---|---|
| `--font-weight-semibold` | `600` | All financial figures in MyStable |
| `--color-purple-400` (or named 5×M accent) | `Tailwind's purple-400 ≈ #c084fc` | 5×M value only |
| `--shadow-success-glow` | `0 0 20px rgba(16, 185, 129, 0.35)` | Checkout success banner, globals.css |
| `--shadow-modal` | `0 0 120px rgba(0,0,0,0.98)` | Billing dialog, CTA modal |
| `--color-status-active-10` | `rgba(16, 185, 129, 0.1)` | Success banners, status pill fills |
| `--color-accent-10` | `rgba(212, 169, 100, 0.1)` | Billing pill active state |

---

## 5 · Elements to confirm in review

1. **Is `font-semibold` (600) intentional for financial figures?** It is the first use of a weight between 500 and 700. If it is correct, the token system needs `--font-weight-semibold: 600`.
2. **Is `text-purple-400` the correct colour for the 5×M display?** It is a one-off colour. Should it be a named token (`--color-5xm`?) or should it use an existing token?
3. **Should the stat card gap (`gap-4`) be tokenised as a spacing step?**
4. **Is the `aspect-[16/10]` ratio intentional for the holdings card image?** Not seen in Steps 1 or 2.
5. **Should `shadow-success-glow` be elevated to a formal token, or kept as a CSS variable in globals.css?**
