# Implementation Plan — Critical Motion Fixes (Purchase Flow First)

**Date:** 2026-10-13
**Feeds from:** `AUDIT-MOTION-2026-10-13.md`
**Primary target:** purchase flow rebuild at `/home/evo/sandbox/rebuild` → migration into `apps/web`
**Scope law:** this plan does not authorise code changes to production. It defines what the rebuild must do so critical findings close by design, not patch.

---

## Phase 0 — Foundations (brand_dna motion tokens)

The polish-loss report (FR2) already identifies that motion tokens don't exist. Define once, in `packages/brand_dna/src/tokens.ts`:

```ts
export const BRAND_MOTION = {
  // Step/beat enter — v2 wireframe spec (220ms, custom ease)
  'ease-enter': 'cubic-bezier(0.16, 1, 0.3, 1)',
  'duration-step': '220ms',
  // Modal presence
  'ease-modal': 'cubic-bezier(0.32, 0.72, 0, 1)', // iOS-like, from Emil's Vaul defaults
  'duration-modal-enter': '240ms',
  'duration-modal-exit': '160ms',
  // Press feedback (Apple principle #1)
  'scale-press': '0.97',
  // Beat system (post-fix floor: readable-by-transition, not timer)
  'duration-beat-enter': '280ms',
} as const;
```

Generate into `theme.generated.css`. Every fix below references these tokens — no ad-hoc values.

## Phase 1 — Beat system rewrite (closes C1)

**In the sandbox rebuild** (`usePurchaseFlow.ts`):

1. Keep `nextPaint()`-equivalent: state set → network fires after paint. Preserve as-is.
2. Replace `MIN_BEAT_MS=1400` floor logic with:
   - Beat content mounts inside an animated container (`opacity 0→1`, `translateY 6px→0`, `duration-beat-enter`, `ease-enter`).
   - Readability floor drops from 1400ms → 350ms (just enough that a genuinely-sub-350ms network response doesn't strobe).
   - `REDIRECT_GRACE_MS=8000` stays (it's a correctness guard, not polish).
3. Add per-beat exit as subtler sibling: 120ms opacity fade (no translate) — the outgoing beat dissolves while the incoming slides.
4. Each beat boundary becomes a small `key`-swapped wrapper so React remounts the content inside the animation (CSS-class retrigger; no keyframes — transitions triggered by class change are interruptible).

**Acceptance:** walking Steps 2→3→4→5 shows a crossfade each time; no step waits longer than network + ~350ms; rapid next/back still animates smoothly (interruptible).

## Phase 2 — Modal presence (closes C2)

In `PurchaseShell.tsx`:

1. Shell renders permanently while mounted; `isOpen` drives classes, not conditionals.
2. Enter: overlay `bg-canvas/80` fades 150ms; panel `scale 0.96→1` + `y 8→0`, 240ms, `ease-modal`.
3. Exit: same, reversed, 160ms, subtler (no scale-down overshoot, `y 4`).
4. On close, keep DOM until exit completes (either `setTimeout`-based unmount from the host, or the persistent-shell approach — host holds `isOpen` false but shell stays mounted with `pointer-events-none` + `opacity-0` end-state).

**Acceptance:** opening and closing the purchase modal animates; no flash on unmount; focus stays managed (Radix Dialog handles it — verify visually).

## Phase 3 — Stepper upgrade (closes C3, partial Apple-grade)

**Minimum (must land in rebuild):**
1. `:active` press scale on stepper buttons (0.97, 100ms ease-out) — Apple #1.
2. Number display: keyed `<span key={stakePct}>` with a 150ms opacity/translateY micro-crossfade on change — makes frequency-high increments feel alive without delay.
3. Bounds: keep clamp, but add 1-step "overshoot-and-return" feel via a 200ms ease-out-back on hitting min/max (instead of the dead `opacity-40 cursor-not-allowed` clamp) — cheap approximation of Apple rubber-band.

**Phase 2 (optional, if time allows):** full drag-to-adjust with pointer capture, transform-only tracking, velocity-based release. Not required for parity with v2 wireframe spec.

**Acceptance:** clicking ▲/▼ rapidly animates cleanly; hitting min/max feels damped, not disabled.

## Phase 4 — CollapsePanel standardisation (closes C4)

1. In `CollapsePanel`: remove `maxH`/`scrollHeight` state entirely. Pure `grid-template-rows 0fr↔1fr` + opacity. Drop `transition-all` → transition only `grid-template-rows, opacity`. 300ms, `ease-enter`.
2. Refactor `PressShowcaseSection` expanded panel to reuse `CollapsePanel` (deletes its bespoke `max-h` code).
3. Verify global reduced-motion block nukes both properties (it does, `transition-duration:0.01ms`, fine).

**Acceptance:** FAQ + Press expand/collapse with zero JS measurement; layout shifts only inside the collapsing block's own paint, not the page (it's still within `overflow-hidden`, so no external reflow except document height — acceptable, the CSS-only alternative for true zero-page-reflow is `content-visibility` which is out of scope).

## Phase 5 — Migration gate (from rebuild into apps/web)

Per `MIGRATION-PLAN.md` + polish-loss report merge sequence:

1. Complete rebuild phases 1–4 in sandbox first (this plan, above).
2. Wire real handlers into `usePurchaseFlow` replacing setTimeout simulations (accept endpoint, checkout session create). Keep the beat/paint logic.
3. Port via `components/purchase/` exactly per MIGRATION-PLAN (imports mapping table).
4. Run Playwright E2E at 375/768/1280 — verify mobile drawer geometry unaffected by new transitions.
5. Visual regression against `purchase-flow-v2.html` (the approved craft); motion regression against this plan's acceptance criteria.

## Non-goals (explicit)

- No Framer Motion dependency addition unless the founder approves; CSS transitions cover everything in phases 1–4, and springs (drag) are phase-3-optional.
- No changes to backend/handlers/stripe — this is a motion-layer plan only.
- No marketing-section animation changes in this plan (I3 staggers, I5 hero delays tracked as "second pass" — not blocking purchase migration).

## Success criteria for the whole plan

- [ ] Beat floor ≤350ms everywhere; beats transition, not snap.
- [ ] Modal animates in AND out.
- [ ] Stepper gives press feedback + micro-crossfade; bounds feel damped.
- [ ] CollapsePanel is measurement-free and reused by PressShowcase.
- [ ] All values sourced from `BRAND_MOTION` tokens — zero hardcoded durations/easings in purchase flow.
- [ ] Reduced-motion path verified with OS toggle.
- [ ] `pnpm check` passes in both sandbox and migrated site.
