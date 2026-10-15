# Motion & Interaction Audit — Evolution Stables Website

**Date:** 2026-10-13
**Scope:** `evolution/engine/website/apps/web` — every animated surface (marketing sections, purchase flow, accordions, modals, buttons)
**Frameworks applied:** `design-motion-principles` skill (Emil Kowalski / Jakub Krehel / Jhey Tompkins lenses, full audit checklist + anti-checklist) AND the apple-design skill (Emil Kowalski's 17 WWDC fluid-interface principles, fetched manually — skill not installable in sandbox, applied as reference doc)
**Purpose:** (1) full rebuild context for `evo/sandbox/v2` blank-canvas decisions; (2) critical-fix plan for the purchase flow before its migration from `evo/sandbox/rebuild`.

---

## 1. Project Context (Reconnaissance)

- **Type:** Marketing/landing + SaaS purchase funnel (digital racehorse ownership, NZ).
- **Stack:** Next.js 15, React 19, Tailwind 4, Radix UI. **No Framer Motion.** GSAP + ScrollTrigger for scroll reveals and hero parallax. CSS transitions/keyframes for UI motion.
- **Motion inventory:**
  - Scroll reveals: `lib/reveal.ts` wraps GSAP `fromTo` with `power3.out`, travel capped at 24px, staggers ~0.15s, durations 0.8–1s.
  - Hero parallax: bg `y:80` scrub, content `y:-100` + fade, `scrub:1`.
  - Accordions/FAQ: `CollapsePanel` — CSS `grid-template-rows 0fr↔1fr`, `transition-all 300ms ease-out`, plus opacity.
  - Purchase modal: hand-rolled beat system (`MIN_BEAT_MS=1400` floor, `REDIRECT_GRACE_MS=8000`), keyframe-based, steps swap instantly.
  - Buttons: `transition-all duration-200–400`, hover color/border/scale; press `active:scale-90` on stepper only.
  - Keyframes in `globals.css`: `logo-scroll`, `cursor-blink`, `shimmer`, `fadeIn` 0.8s, `heroLogoIn`/`heroTaglineIn` 0.8s delay 0.85/1.05s.
  - Reduced motion: global `@media (prefers-reduced-motion: reduce)` kills all animation/transition durations (globals.css:295–301); `reveal.ts` and `HeroSection` also guard in JS.

## 2. Weighting Proposed (per skill workflow)

| Lens | Weight | Why |
|---|---|---|
| **Jakub Krehel** | Primary | Consumer brand, production polish matters (marketing pages, purchase trust surfaces). |
| **Emil Kowalski** | Secondary | Purchase funnel = high-stakes conversion; frequency rule + speed + interruptibility govern it. |
| **Jhey Tompkins** | Selective | Hero entrance, parallax, shimmer — deliberate moments only. |

## 3. Apple Design (17 WWDC Principles) — Full Mapping

| # | Principle | Status | Evidence |
|---|---|---|---|
| 1 | Response — kill latency; respond on pointer-down | ❌ | No `:active` press feedback on most buttons; no `onPointerDown` handlers. Purchase beats artificially held 1400ms. |
| 2 | Direct manipulation — 1:1 tracking | ❌ | Stepper is click-only (▲/▼). No drag, no grab-offset. |
| 3 | Interruptibility | ❌ | `MIN_BEAT_MS` floor prevents mid-animation interruption; CSS keyframes can't retarget; reveals are `toggleActions: play none none reverse` (not scrubbed, not interruptible mid-tween). |
| 4 | Springs over keyframes | ❌ | Zero spring physics anywhere. All easing is Bézier/`power3.out`. |
| 5 | Velocity handoff | ❌ | No drag→spring handoff (nothing draggable). |
| 6 | Momentum projection | ❌ | Not implemented. |
| 7 | Rubber-banding | ❌ | Stepper clamps hard at min/max (opacity-40, cursor-not-allowed). No progressive resistance. |
| 8 | Gesture details (hysteresis, parallel recognition) | ❌ | Mouse/keyboard only. |
| 9 | Frame smoothness (transform/opacity only) | ⚠️ Partial | Reveals + parallax use transform/opacity ✅. **But** `CollapsePanel` and `PressShowcase` animate `max-height`/`height` (layout thrash ❌). |
| 10 | Multimodal feedback | ❌ | Visual only. (Acceptable for web; haptics are out of scope.) |
| 11 | Reduced motion | ✅ | Global CSS kill-switch + JS guards in `reveal.ts` and `HeroSection`. **Gap:** CollapsePanel and PressShowcase still transition (durations nuked globally so effectively instant — acceptable, but no component-level guard). |
| 12 | Translucent materials | ✅ | `backdrop-blur-md` modal overlay, `dot-grid-surface`, glass-streaks, film grain. |
| 13 | Spatial consistency | ✅ | Modal shell locked `max-w-lg × h-[900px]` across all steps; `dvh` viewport guard. |
| 14 | Typography craft | ✅ | System sans stack, tracking-tight headings, `tracking-[0.2em]` labels, mono + `tnum` for financials, Instrument Serif accents. |
| 15 | Hint direction | ✅ | Stepper ▲/▼ telegraph direction; reveal travel direction signals entry. |
| 16 | Feedback continuity during interaction | ❌ | Purchase beats: feedback only at end of the 1400ms hold, not continuous. Stripe redirect beat = spinner only. |
| 17 | Serves safety / understanding / achievement / joy | ⚠️ | Safety & understanding: good (locked shell, clear copy). Achievement (completing a purchase): **hindered by forced waits**. Joy: limited to hero/shimmer moments. |

## 4. Design-Motion-Principles Checklist — Detailed Findings

### 4a. Philosophy gate

| Check | Verdict |
|---|---|
| Frequency rule | Purchase flow is used rarely *per user* but it is conversion-critical — forced 1400ms beats are an **anti-pattern** for any moment a user is waiting on real work. Stepper increments can be high-frequency in-session → should be instant or <180ms. |
| Keyboard = no animate | Purchase modal has no keyboard navigation for stepper (separate a11y miss). Keyboard nav within flow is tab/focus only — fine. |
| Purpose vs decoration | Reveals = orientation ✅. Hero parallax = atmosphere ✅. Shimmer = brand accent ✅. 1400ms beat floor = **no purpose beyond "make sure the user sees the beat" — but it's applied even when the beat is trivial**. |
| Noticeable after 10th use | Step 2→3→4→5 transitions read as sluggish on replay. |

### 4b. Motion gaps (conditional renders without animation)

| Location | Pattern | Gap |
|---|---|---|
| `purchase-flow-modal.tsx` beats | state-machine `beat` transitions (`pending`, `gate`, `error`, `verified`, …) | Content **snaps** between beats — no enter/exit animation at all |
| `purchase-flow-host.tsx:110` | `if (!isOpen) return null` | Modal unmounts instantly — no exit animation |
| `purchase-flow-host.tsx:94` | `{isOpen && <ModalShell/>}` equivalent | Modal mounts instantly — no enter animation |
| `purchase-flow-modal.tsx` spinner | `beat !== 'error' && beat !== 'gate'` → spinner renders | Loading state appears with no transition |
| Right-rail error (`right-rail.tsx:148`) | `{error && <p/>}` | Error appears instantly |
| Step content swaps within modal | conditional blocks per step | No cross-fade/slide between steps (the v2 wireframe HAS a 220ms step-enter — polish-loss report item 1) |

### 4c. Anti-checklist flags

| Anti-pattern | Found? | Where |
|---|---|---|
| Pulsing indicators | No | — |
| Blur-everywhere entrances | No | Blur used sparingly (modal backdrop only) |
| Hover-scale-everything | No | Scale reserved to stepper press + GlowPillButton glow |
| Stagger-spam | ⚠️ Borderline | `DigitalSyndicationSection` + `MarketplaceSection` both use `stagger: 0.15` — just at the "≥2 lists" tell. One deliberate pattern reused identically; recommend varying or reducing to primary lists only. |
| Bouncy springs on utility | No | (No springs at all — the opposite problem) |
| **Animating layout properties** | 🔴 Yes | `CollapsePanel`: `maxHeight` + `gridTemplateRows`. `PressShowcaseSection`: `max-h-0↔max-h-[900px]`. Layout thrash on every expand/collapse. Grid-rows technique is actually compositor-friendlier than raw maxHeight, but both pattern with opacity transitions still trigger reflow. |
| Exit = Enter | 🔴 Yes | CollapsePanel exit mirrors enter exactly; PressShowcase same; purchase beats no exit at all |
| scale(0) entrances | No | — |
| Default easing | No | Custom Béziers used (`cubic-bezier(0.4,0,0.2,1)`, `power3.out`) ✅ |
| Keyframes for interruptible animations | 🔴 Yes | Entire purchase-beat system is timing-floor based; `animate-fade-in` on modals is a keyframe, so closing/reopening mid-animation misbehaves. |
| will-change everywhere | No | — |

## 5. Critical Findings (Must Fix — Ranked)

### C1 — Purchase-flow beat system: artificial 1400ms floor, no transition between beats
- **Files:** `apps/web/src/components/horse/purchase-flow-modal.tsx:146–163`
- **Principles violated:** Apple #1 (response), #3 (interruptibility), #16 (continuity); Emil frequency rule; anti-checklist "keyframes for interruptible."
- **Why it matters:** In a conversion funnel, every artificial wait is abandoned-cart risk. The floor was added to fix a perceived "beat too short to read" bug (2026-09-14 walk) — the real fix is a *transition into the beat*, not a timer. A 250–350ms cross-fade/slide-in makes a beat readable without holding the user hostage; slow network already extends the beat naturally (`holdBeat` only tops up to the floor when fast).
- **Fix shape:** Convert each beat's content mount to an animated enter (opacity+Y 8px+optional blur, 220–300ms, custom ease `cubic-bezier(0.16,1,0.3,1)` — already the v2 wireframe spec). Keep `nextPaint()` to guarantee paint-before-network, drop `holdBeat` floor to ~350ms, keep redirect grace. Beats then feel instant and readable.

### C2 — Modal mounts/unmounts with zero animation
- **Files:** `apps/web/src/components/marketplace/purchase-flow-host.tsx:94,110`
- **Principles violated:** Apple #3, #4; anti-checklist "no exit animations."
- **Fix shape:** Wrap modal in a presence-preserving mount (Framer `AnimatePresence` equivalent or CSS class-toggle on a persistent shell). Enter: overlay fade 150ms + panel `scale(0.96→1)` + `y(8→0)` 220ms custom ease. Exit subtler: 150ms, `y:4`, no blur.

### C3 — Stepper: click-only, no spring, no direct manipulation
- **File:** `purchase-flow-modal.tsx` stepper logic
- **Principles violated:** Apple #2, #4, #5, #6, #7; Emil press-feedback tip.
- **Fix shape (minimal viable, no full Apple-grade required):**
  1. `:active` scale + instant visual feedback on the number (not just buttons).
  2. Number crossfades/springs on value change (Motion one, or a tiny CSS transition on a keyed span).
  3. Optional (phase 2): draggable track with pointer capture + rubber-band at bounds using `transform` only.
- **Note:** v2 wireframe already upsized hitboxes to 44px tactile — carry that through.

### C4 — Height/max-height animations cause layout thrash
- **Files:** `CollapsePanel.tsx`, `PressShowcaseSection.tsx` (also `OwnershipFAQSection`, FAQ variants via CollapsePanel)
- **Fix shape:** CollapsePanel's `grid-template-rows 0fr↔1fr` is already the modern approach — but remove the dual `maxHeight`/scrollHeight JS state which fights it and forces measure; keep pure `grid-template-rows` + opacity + `translateY` and drop `transition-all` (transition only `grid-template-rows, opacity`). PressShowcase: replace `max-h` pattern with the same `CollapsePanel`, killing the duplicated code.

### 5a. Important findings

| # | Finding | Fix |
|---|---|---|
| I1 | CollapsePanel/PressShowcase exit = enter exactly | Make exit subtler (shorter duration or smaller travel, per Jakub) |
| I2 | CollapsePanel lacks local reduced-motion guard | Covered by global kill but add a cheap early-return or rely on global guard alone (verify global guard fully nukes `transition-all`) |
| I3 | Stagger reuse across ≥2 sections (borderline) | Differentiate or dedupe |
| I4 | No pointer-down feedback on primary CTAs | Add `active:scale-[0.97]` + `transition-[transform,background-color] duration-100 to GlowPillButton/SolidPillButton` |
| I5 | Hero entrance delays (0.85s/1.05s) hold LCP element invisible | Convert to CSS `backwards` fill with content painted (already `both`) but reduce first delay to ~0.3s — a 0.85s invisible hero hurts LCP and Apple #1 |

## 6. What's working well (keep in rebuild)

1. `lib/reveal.ts` centralisation with travel cap + missing-target no-op — port this pattern into v2 as the single reveal API.
2. Global reduced-motion kill-switch (globals.css:295–301) — carry forward verbatim.
3. Custom Bézier easings already in use — match v2's `cubic-bezier(0.16,1,0.3,1)` step-enter spec.
4. Locked modal shell geometry (`max-w-lg × h-[900px]` + dvh guard) — strong spatial consistency.
5. Typography system (system sans, tracking, mono tabular financials) — Apple-aligned, keep.
6. Translucent materials (backdrop-blur modal overlay, dot-grid, film grain) — keep.
7. `nextPaint()` beat-paint guarantee — keep the *pattern*, fix the *floor*.

## 7. V2 Blank-Canvas Guidance (from this audit)

The rebuild (`evo/sandbox/v2/PLAN.md`) starts from zero. Recommendations flowing from this audit:

1. **Pick one motion primitive and enforce it site-wide.** Recommendation: CSS transitions with custom Béziers for interactive/enter-exit (interruptible by nature), GSAP only for scroll-driven (parallax, scrub reveals). No keyframes for anything interactive. If Framer Motion is acceptable, `AnimatePresence` for all mount/unmount and springs for anything draggable — otherwise Motion One for springs.
2. **Bake step-enter into the architecture from day one** — the v2 wireframe already defines it (opacity + translateY(6px), 220ms, `cubic-bezier(0.16,1,0.3,1)`). Make this a token in brand_dna (motion group: `--ease-enter`, `--duration-step`), not per-component CSS.
3. **Beat system redesign:** replace timing floors with transition-into-state. Paint guarantee stays; readability comes from the animated enter, not a timer.
4. **CollapsePanel pattern (grid-rows, no maxHeight JS)** is the right primitive — standardise it, remove PressShowcase's bespoke copy.
5. **Stagger budget:** one deliberate staggered moment per page max.
6. **Apple principles worth adopting early:** pointer-down feedback (scale on `:active` on every interactive element, one token), interruptibility (transitions-not-keyframes rule), transform/opacity-only rule enforced by a lint/audit script.
7. **Things NOT to carry forward:** `MIN_BEAT_MS` as a hard floor, exit=enter collapses, ad-hoc inline shadows (23 arbitrary values — tokenise), `max-h` accordion variants, two competing stagger patterns.

## 8. Evidence Base

- `apps/web/src/components/horse/purchase-flow-modal.tsx` (2061 lines; MIN_BEAT_MS:146; beat system)
- `apps/web/src/components/marketplace/purchase-flow-host.tsx` (URL-gated mount pattern)
- `apps/web/src/components/ui/CollapsePanel.tsx` (grid-rows collapse)
- `apps/web/src/components/sections/HeroSection.tsx` (parallax + reduced-motion guard)
- `apps/web/src/components/sections/PressShowcaseSection.tsx` (max-h accordion)
- `apps/web/src/lib/reveal.ts` (centralised GSAP reveal)
- `apps/web/src/app/globals.css` (keyframes, reduced-motion scopes, theme transitions)
- `evo/sandbox/rebuild/POLISH-LOSS-AUDIT-REPORT.md` (visual-craft delta: v2 wireframe ≠ live, motion tokens missing)
- `evo/sandbox/rebuild/src/components/purchase/` (skeleton: 858 lines, hook uses setTimeout-simulated async — needs real handlers)
- `evo/sandbox/v2/PLAN.md` (blank-canvas rulings)
