# Step 1 — Landing Page Audit (`/`)

**Audit date:** 2026-10-15
**Source:** `evolution/engine/website/apps/web/src/app/page.tsx` + all `components/sections/`, `components/ui/`, `packages/brand_dna/src/theme.generated.css`
**Frame:** Empirical harvest. No guess. Every value cited from source.

---

## 1 · Surfaces

Five tokens confirmed in `theme.generated.css`:

| Token | Value | Job |
|---|---|---|
| `--color-canvas` | `#030303` | Page background. Deliberately not `#000000` — the gap is what makes a stage. |
| `--color-surface` | `#0a0a0a` | Cards, panels, raised UI |
| `--color-raised` | `#111111` | Hover surfaces, inner panels |
| `--color-border` | `rgba(255,255,255,0.1)` | Decorative containment — card wrappers, dividers. ~1.2:1. Not for controls. |
| `--color-edge` | `#9a9aa0` | WCAG 3:1 contrast floor for interactive controls, focus rings, pill outlines. ~3.6:1 on surface. Do not use for general card borders. |

**Retired** — do not use: `ash #575757` (fails contrast), `smoke #454545` (fails contrast), `hairline #050505` (imperceptible against canvas), `stage-black #000000` (zero call sites). The `l1–l4` ladder retired 2026-09-22.

---

## 2 · Text

### Colour

| Token | Value | Usage |
|---|---|---|
| `--color-heading` | `#f8fafc` | All headings, subheadings, card titles |
| `--color-ink` | `rgba(255,255,255,0.5)` | Body copy — semi-transparent so it blends with background behind it |
| `--color-foreground` | `var(--color-ink)` | shadcn/Tailwind alias layer — points at ink. Do not use as a free variable; house value is `ink` |
| `--color-muted-foreground` | `#7c7c7c` | Labels, captions, nav metadata, timestamps |

### Type scale

Seven named roles, confirmed in `theme.generated.css`:

| Token | Value | Used on |
|---|---|---|
| `--text-micro` | `10px` | Used for small mono spec text — pedigree table, cap table, right-rail metadata |
| `--text-label` | `11px` | Nav links, section eyebrows, button labels |
| `--text-body-small` | `15px` | Card descriptions, secondary copy |
| `--text-body` | `16px` | Primary body copy |
| `--text-card-heading` | `18px` | Card headings, FAQ questions, subheadings |
| `--text-section-heading` | `36px` | Section h2, single breakpoint |
| `--text-section-heading-wide` | `48px` | Same role, md+ breakpoint |

**Key observation:** 36px and 48px are the same role at two breakpoints — not a display/heading pair. Confirmed in tokens.ts comments.

### Weights

| Rule | Value | |
|---|---|---|
| `--font-weight-light` | `300` | Used for all body text and headings |
| `--font-weight-medium` | `500` | Used for the hero tagline only |

No `font-bold` (700) anywhere on the landing page.

### Label roles (four, in CSS classes)

| Class | Size | Weight | Tracking | Transform | Used on |
|---|---|---|---|---|---|
| `.label-eyebrow` | 11px | 300 | 0.2em | uppercase | Section labels, nav links, eyebrows |
| `.label-action` | 11px | 500 | 0.2em | uppercase | CTAs, action links (View current offerings) |
| `.label-spec` | 10px | 400 | 0.2em | uppercase + mono | HowItWorks card titles, spec strips |
| `.label-mono-intro` | 12px | 400 | 0 | none | (landing page — not currently used) |

---

## 3 · Colour accents

| Token | Value | Usage rule |
|---|---|---|
| `--color-gold` | `#d4a964` | Primary accent — logo, hover states, CTA buttons, text emphasis |
| `--color-gold-hover` | `#c39853` | Gold hover state only — never a surface |
| `--color-on-gold` | `#0a0a0a` | Text on gold — dark, not white |
| `--color-spot-mint` | `#00e599` | One word: "Regulation" in the marketplace headline only |
| `--color-hover` | `#b9b3a9` | Warm hover tone for text links. Hover ONLY — never surface or border |

### Status colours

| Token | Value | Usage |
|---|---|---|
| `--color-status-active` | `#10b981` | Available campaigns |
| `--color-status-pending` | `#f59e0b` | Coming soon |
| `--color-status-closed` | `#64748b` | Fully allocated / completed |

Status is semantic — these map to a database enum (`public.status`). No other use.

---

## 4 · Structure (borders and dividers)

**Core rule:** structure tokens are DIVIDERS AND BORDERS, NEVER TYPE.

| Token | Value | Job |
|---|---|---|
| `--color-border` | `rgba(255,255,255,0.1)` | Decorative containment — card borders, section dividers, FAQ dividers. ~1.2:1. |
| `--color-edge` | `#9a9aa0` | WCAG 3:1 contrast floor for interactive controls, focus rings, pill button outlines. ~3.6:1 on surface. |

**Retired** — do not use: `hairline #050505` (imperceptible against canvas), `ash #575757` (fails contrast), `smoke #454545` (fails contrast).

**Border radius:**

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `8px` | Image frames, small elements |
| `--radius-md` | `16px` | Cards nested inside containers |
| `--radius-lg` | `24px` | Top-level cards, modals, containers |
| `--radius-pill` | `9999px` | Buttons, pills, badges |

No `rounded-2xl` or `rounded-3xl` in use on the landing page — those fall through to the Tailwind defaults (16px/24px), which are aliased to `--radius-xl`/`--radius-2xl` → `24px` in the theme.

---

## 5 · Typography faces

Three faces total, confirmed in `tokens.ts` and `theme.generated.css`:

| Face | Role | Stack |
|---|---|---|
| **System sans** | Primary UI, body, headings | `ui-sans-serif, system-ui, -apple-system, …` |
| **Geist Mono** | Financials, figures, spec labels, mono-intro | `var(--font-geist-mono), ui-monospace, …` |
| **Instrument Serif** | Reserved drama — one italic gold word in a headline, nothing else | `var(--font-instrument-serif), ui-serif, …` |

**Geist Sans is retired** (2026-09-22). Lives in `brand/fonts/retired/`. Must not be reintroduced.

**Tracking behaviour on headings:**
- Section headings (`text-[36px] md:text-[48px]`): `tracking-tight` (negative tracking, tightens to near-zero at body sizes)
- Body: `leading-[1.7]` for descriptions, `leading-[1.1]` for headings
- Nav links: `tracking-[0.15em]` at 12px/300 weight

---

## 6 · Spacing

| Token | Value | Usage |
|---|---|---|
| `--spacing-section` | `224px` | Section vertical padding (`py-section`). Verified: six section wrappers use `py-56` = 224px. |

**Container:** `max-w-6xl` (1152px), padding `px-12 md:px-16 lg:px-20` (48px/64px/80px sides).

---

## 7 · Motion (landing page only — no purchase flow)

### Scroll reveals (`lib/reveal.ts`)

Single entry point for all sections. GSAP `fromTo`, `power3.out`, capped travel at 24px.

| Pattern | Params used |
|---|---|
| Section headers | `y: 0, start: 'top 85%'` |
| Body paragraphs | `y: 0, start: 'top 78%'` |
| Card grids (stagger) | `y: 60, start: 'top 90%', duration: 0.8, stagger: 0.15` |
| FAQ items | `y: 0, start: 'top 90%', duration: 0.6, stagger: 0.1` |
| Logo strip | `y: 40, start: 'top 90%', duration: 0.6, stagger: 0.08` |

**Reduced motion:** honoured globally via `prefers-reduced-motion` check in `reveal.ts`. Hero also guards in JS. Confirm: the audit found this was honoured in only 1 of 6 sections previously — now fixed.

### Hero parallax

- Background: `y: 80, scrub: 1, ease: none`
- Content: `y: -100, opacity: 0, scrub: 1, ease: none`
- Entrance: `heroLogoIn` (0→24px Y, 0.8s ease-out, 0.85s delay) + `heroTaglineIn` (0→12px Y, 0.8s ease-out, 1.05s delay)
- Reduced motion: parallax skipped entirely via JS guard

### Accordion (FAQ)

`CollapsePanel` — CSS `grid-template-rows: 0fr ↔ 1fr` + opacity, `duration-300 ease-out`. No JS height measurement. Exit mirrors enter.

### Hover interactions

| Element | Hover behaviour |
|---|---|
| HowItWorks card | Border: `border-border` → `border-edge`; text: `text-muted-foreground` → `text-hover`; arrow icon rotates |
| Marketplace card | Vertical accent line scales from `scale-y-0` → `scale-y-100`; text → `text-hover` |
| Press article links | Grayscale → full colour; opacity lift |
| Nav links | Bottom hairline scales from `scale-x-0` → `scale-x-100` with gold colour |

---

## 8 · Components found on the landing page

### GlowPillButton
- Pill shape (`rounded-full`), `px-6 py-2.5`
- Background: `--color-surface`, border: `border-edge/70`
- Hover: `bg-raised`, `border-edge`, gold accent line at bottom (`h-[1px]` gradient)
- Text: `label-action` class (11px/500/0.2em)
- Disabled: `opacity-45`
- Shimmer overlay: `animate-shimmer` (left-to-right gradient sweep)

### Badge variants (CVA)
| Variant | Usage |
|---|---|
| `default` | Solid gold fill, dark text (`bg-primary text-primary-foreground`) |
| `accent` | Gold border at 30% opacity, raised surface fill |
| `success` | Active status — green border + 10% fill |
| `warning` | Pending — amber border + 10% fill |
| `destructive` | Red border + 10% fill |

### Footer
- Three-step: hero tagline (typewriter reveal), gradient divider, legal bar
- Nav links: 12px/300/0.15em uppercase
- Social icons: 20×20px, muted → heading on hover
- Tagline reveal: `opacity 800ms + translateY 800ms, cubic-bezier(0.16,1,0.3,1), delays 400ms/600ms`

### LogoCarousel
- Seamless loop via duplicate array
- Edge fade masks (24px gradient from canvas on both sides)
- Speed: 30s default; logo height 35px
- Logos: 60% opacity, grayscale; 90% on hover
- Animation: `logo-scroll` keyframe (translateX 0 → -50%)

### CtaLeadModal
- Triggered: campaign links only (no auto-pop on organic)
- Overlay: `bg-canvas/80` + `backdrop-blur-[4px]`
- Card: `max-w-[760px]`, `rounded-xl`, border + shadow
- Buttons: `.label-action` pill (primary gold + ghost border)
- Dismiss: sessionStorage scoped per horse slug

---

## 9 · Elevation model

**No shadows on the landing page.** Elevation is carried entirely by:
1. Surface stepping: `canvas → surface → raised`
2. Hairline borders: `border-border` at 10% white
3. Glow effect on GlowPillButton: `blur-md` pseudo-element at hover

**Shadow in use:**
- `shadow-[0_0_80px_RGBA(0,0,0,0.35)]` — on the hero wrapper only
- `shadow-[0_0_120px_rgba(0,0,0,0.98)]` — on the CTA modal only

Both are atmosphere effects, not elevation mechanics.

---

## 10 · Global textures and utilities

- **Film grain:** `body::after`, SVG `feTurbulence`, 3% opacity, fixed position
- **Dot grid:** `.dot-grid-surface` — `radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px)`, 24px grid
- **Glass streak:** `.glass-streak` — left-to-right shimmer on hover
- **Masked border:** `.masked-border` — gradient border via `mask-composite`

---

## 11 · Key deviations from the token source

One inline style on the landing page — the hero tagline under the logo:

**HeroSection.tsx line 97:**
```tsx
<p className="mt-8 max-w-[720px] font-medium leading-relaxed animate-hero-tagline uppercase"
  style={{ fontSize: 12, letterSpacing: '3px', color: '#a1a1aa' }}>
```
Full spec: `12px / 500 / 3px tracking / #a1a1aa / uppercase / leading-relaxed (1.625)`. None are in the token system:
- `12px` — not a type role (scale is 10/11/15/16/18/36/48)
- `letterSpacing: 3px` — exceeds any label role (0.2em ≈ 2.2px at 11px)
- `#a1a1aa` — Tailwind `zinc-400`, raw inline; resolves to nothing named
- `leading-relaxed (1.625)` — a fourth leading value not on the scale

This style stays (keep the look per Q1), and the four values are tokenised in `DESIGN.md`.

---

## 12 · Confirmed working elements (keep)

- Three-surface model (`canvas → surface → raised`) with no fourth step
- Gold at `#d4a964` as the one chromatic accent; mint at `#00e599` for one word only
- System sans + Geist Mono + Instrument Serif (reserved drama) — no other faces
- `label-eyebrow` / `label-action` / `label-spec` as the three active label roles
- CSS-only accordion (`grid-template-rows`) with no JS measurement
- Single `reveal()` entry point for all scroll animations, with reduced-motion guard
- Logo carousel with edge fade masks — no JS required
- Footer typewriter reveal using CSS transitions only

---

## 13 · Gaps identified

| Gap | Status | Resolution |
|---|---|---|
| **Elevation** | **Ruled** | Surface-stepping + hairlines is the system. Three shadow tokens: `--shadow-card-hover`, `--shadow-modal`, `--shadow-glow`. Hero's `0 0 80px` collapses into `--shadow-modal`. |
| **Motion durations** | **Ruled** | Adopt `BRAND_MOTION` tokens; add `--duration-hover: 200ms`, `--duration-collapse: 300ms`. |
| **Hero tagline inline style** | **Tokenised** | `12px / 500 / 3px / #a1a1aa / uppercase / leading-relaxed (1.625)` — stays, values get names in `DESIGN.md`. |
| **CollapsePanel exit = enter** | **Ruled** | Differentiate: enter 300ms / exit 200ms, opacity-led. Add local reduced-motion guard. |
| **GlowPillButton shimmer** | **Tokenised + dead animation fixed** | `--duration-shimmer: 2000ms`. `animate-border-shimmer` in `CtaLeadModal` has no keyframe (FX-09) — delete the dead class, do not define a keyframe. |

---

## Summary: what the landing page has that we need to lock

```
Surfaces:     canvas #030303 / surface #0a0a0a / raised #111111
Structures:   border rgba(255,255,255,0.1) / edge #9a9aa0 (WCAG 3:1 for controls)
Text:         heading #f8fafc / ink rgba(255,255,255,0.5) / muted #7c7c7c
Gold:         #d4a964 (hover #c39853) / on-gold #0a0a0a — 3-5% of viewport
Mint:         #00e599 — one display word per page only
Status:       active #10b981 / pending #f59e0b / closed #64748b
Radii:        sm 8px / md 16px / lg 24px / pill 9999px
Type faces:   system sans + Geist Mono + Instrument Serif (reserved drama)
Type scale:   micro 10 / label 11 / body-small 15 / body 16 / card-heading 18 / section 36+48
Weights:      300 (body/headings) / 500 (clicked caps, hero tagline)
Label roles:  eyebrow (11/300/0.2em) / action (11/500/0.2em) / spec (10/400/0.2em + mono)
Section pad:  224px
Container:    max-w-6xl, px-12 to px-20
Motion:       GSAP reveals (clamped to 24px travel), hero parallax, CSS accordion, reduced-motion guard
Elevation:    surface stepping. Shadows are atmosphere (modal/hero) and status (glow) only.
Tagline:      12px/500/3px tracking/#a1a1aa/uppercase/leading-relaxed — tokenised, stays
```
