# Design Audit Index — 2026-10-16

## Governing rule
**Zero debt enters `sandbox/audit/design/`.** Every file here is either written from our own decisions or explicitly adopted from `audit/website/` after review. No bulk imports.

---

## What's been decided

### STEP1 — Landing Page (`/`) ✅ CLOSED
Source: `STEP1-LANDING-PAGE.md`

| Decision | Value |
|---|---|
| Canvas | `#030303` |
| Surface | `#0a0a0a` |
| Raised | `#111111` |
| Border | `rgba(255,255,255,0.1)` |
| Heading | `#f8fafc` |
| Muted | `#7c7c7c` |
| Type scale | 7 roles: micro(10) → section-wide(48) |
| Label roles | `.label-eyebrow` (11px/300/0.2em), `.label-action` (11px/500/0.2em) |
| Section padding | `py-section` = 224px |
| Motion | CollapsePanel, 300ms, `ease-enter` |

### STEP2 — Marketplace (`/`) ✅ CLOSED
Source: `STEP2-MARKETPLACE.md`

| Decision | Value |
|---|---|
| Badge treatment | Green + glow = active (`available`, `coming_soon`); muted gray = terminal (`fully_allocated`, `completed`) |
| V2 enum only | UI props use `available`/`coming_soon`/`fully_allocated`/`completed`. Legacy tokens live only at ingestion boundary. |
| Display heading | `--text-display: 64px`, `--tracking-display: -0.04em`, weight 300, leading 1.05 |
| Card hover shadow | Tokenised: `--shadow-card-hover: 0 20px 40px rgba(0,0,0,0.45)` |
| Tag tracking | 0.05em (`tracking-wider`) for pill badges; 0.2em for action labels — intentionally different |
| Container width | `max-w-6xl` standard for all pages |

### STEP3 — MyStable (`/mystable`) ✅ CLOSED
Source: `STEP3-MYSTABLE.md`

| Decision | Value |
|---|---|
| Financial figures | `font-mono` + weight 500. No 600. |
| Purple purge | `text-purple-400` removed. 5×M label → `text-muted-foreground`; value → mono + 500 |
| Dashboard heading | 64px to match marketplace. Display heading token. |
| Container width | `max-w-6xl` (was 7xl — reduced to match marketplace) |

### Cross-cutting decisions

| Decision | Value |
|---|---|
| Gold naming | `--color-gold` everywhere. No alias. No `accent` as a second name. |
| Gold value | `#d4a964` |
| Gold hover | `#c39853` |
| Status colours | active `#10b981`, pending `#f59e0b`, closed `#64748b`, destructive `#ef4444` |

---

## Audit archive — what's where

All forensic/retrospective work lives in **`evo/audit/website/`**.

| File | Contents | Used for |
|---|---|---|
| `AUDIT-MISSING-PRIMITIVES-2026-10-16.md` | Full extraction: 21 shadow values, dead classes, raw hex literals found in the existing build | Understanding what was broken in evo_02 |
| `DEFECT-HISTORY-2026-10-16.md` | 24 defects from the existing build and their resolutions | The story of what was wrong and how V2 fixes it |
| `AUDIT-MOTION-2026-10-13.md` | Motion/animation findings | Purchase flow motion work |
| `PLAN-CRITICAL-FIXES-2026-10-13.md` | Critical fixes plan for purchase flow | Purchase flow rebuild |
| `V2-DESIGN-SPEC-2026-10-16.md` | Forward-looking spec (from other session) | Reference only — not yet adopted |
| `V2-THEME-2026-10-16.css` | Companion @theme block (from other session) | Reference only — not yet adopted |
| `README.md` | Pre-existing audit README | Context |

**Nothing from `audit/website/` has been adopted into `sandbox/audit/design/` yet.** All adoption is deliberate and step-by-step.

---

## What still needs work

1. **Badge conflict resolution** — the actual code fix: unify `campaign-status-badge.tsx` and `MarketplaceListingGrid STATUS_META` into one component using the locked treatment. Requires code work in the engine repo.

2. **Display heading delivery** — the spec uses `clamp(2.25rem, 6vw, 4rem)` (fluid 36px–64px). Our decision locked 64px. Need to decide: fluid clamp or fixed 64px for the token?

3. **Design decisions to review from audit/website/** — the V2-DESIGN-SPEC and V2-THEME files contain spacing rhythm, button hierarchy, radius scale, motion tokens, and component contracts that we haven't reviewed yet. Each is a separate decision.

4. **DESIGN.md and theme.css for sandbox/audit/design/** — not written yet. These will be built from our own decisions, step by step, starting with what we've already locked above.

---

## File inventory — sandbox/audit/design/

```
README.md          — this directory, scope, and governance
SPEC.md            — the original audit spec (workstreams A–F)
STEP1-LANDING-PAGE.md  — landing page harvest
STEP2-MARKETPLACE.md   — marketplace audit + conflicts
STEP3-MYSTABLE.md      — mystable audit + conflicts
sandbox-design-audit-state.md — closure ledger + handoff
DESIGN-AUDIT-INDEX.md — this file: decisions made, archive map, what's next
```

Zero debt. Every file is intentional.
