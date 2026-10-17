# Step 6a — Draft Plan, revision 4 (Moment 1 round-4 candidate)

**Revision 4, 2026-10-17.** Rev 1, 2 and 3 were each graded `VERDICT: FAIL`. Repair ledgers in §11.
The executor repaired the plan. The executor does not grade its own repair — Moment 1 re-audits.

**App root:** `/home/evo/evolution/engine_v2/website/website`
**Repo root:** `/home/evo/evolution/engine_v2/website` (`Badders80/engine-v2`) — holds `engine/` and `website/`, plus root `scripts/` and the root `package.json` that defines `verify`.
**Step scope:** the `website/` app, plus the two repo-level artifacts README §13 assigns to 6a (§1 D7, D8).
**No application code is written until `VERDICT: PASS`.**

---

## 1 · Deliverables

| # | Artifact | Absolute path | State today |
|---|---|---|---|
| D1 | Tailwind v4 `@theme` block **+ the `@utility` declarations it needs** | `/home/evo/evolution/engine_v2/website/website/src/app/globals.css` | 23 bytes — `@import 'tailwindcss';` only |
| D2 | Font wiring via `next/font` | `/home/evo/evolution/engine_v2/website/website/src/app/layout.tsx` | exists; needs the two faces |
| D3 | Landing page, nine sections | `/home/evo/evolution/engine_v2/website/website/src/app/page.tsx` | 8-line scaffold: "Step 1 scaffold. The landing page and the marketplace land here." |
| D4 | Brand marks | `/home/evo/evolution/engine_v2/website/website/public/brand/` | `public/` does not exist |
| D5 | Landing imagery | `/home/evo/evolution/engine_v2/website/website/public/images/landing/` | **not created — no source exists. §3 OPEN-2** |
| D6 | Partner marks | `/home/evo/evolution/engine_v2/website/website/public/images/partners/` | does not exist |
| D7 | V2 `DESIGN.md` deployed | `/home/evo/evolution/engine_v2/website/website/DESIGN.md` | absent. Assigned to 6a by README §13 |
| D8 | Design-enforcement check | `/home/evo/evolution/engine_v2/website/scripts/` | absent; chained into the root `pnpm test`. Fails the build on raw colour literals, raw palette utilities, and generic font utilities inside `website/website/src/` |

---

## 2 · Tokens (D1) — full compile of `DESIGN.md` frontmatter, lines 1–131

**Ruling.** README §13 describes the second artifact as *"The `@theme` block … Compiled from `DESIGN.md`"*. It is a compile of the **whole document**, not a filter to 6a's consumers: `PLAN.md` §7 requires later steps to reuse this one file and add no tokens. What that does **not** mean is that every key becomes an `@theme` property — `@theme` only generates utilities from Tailwind-namespaced keys. So the artifact splits in three, and this is the correction that matters:

| Tier | What lands | Where |
|---|---|---|
| **`@theme` properties** | colours, font families, text scale, weights, leading, tracking, radius, spacing, elevation, eases — **frontmatter lines 1–131 filtered to those namespaces** | `@theme { … }` |
| **`@utility` declarations** | the z-ladder (`grain −1`, `sticky 30`, `nav 40`, `drawer 50`, `modal 60`), the duration family, `scale-press`/`scale-lift` — none of these are `@theme` namespaces | `@utility` blocks beside the theme |
| **Documented rules** | `layout` (`container max-w-6xl`, `gutter [px-12, md:px-16, lg:px-20]`, `chrome_collapse 768px`, `touch_target 44px`) and the `components` variant enums | **comments in `globals.css`**, not fake utilities |

The consumer-test exemption for the first two tiers rests on the compile ruling, cited rather than assumed. The third tier claims no exemption because it generates nothing.

**Colour** (DESIGN.md 6–36). Surfaces `canvas #030303`, `surface #0a0a0a`, `raised #111111`. Structure `border rgba(255,255,255,0.1)`, `edge #9a9aa0`, `disabled #62666d`. Text `heading #f8fafc`, `ink rgba(255,255,255,0.5)`, `hover #b9b3a9`, `muted-foreground #7c7c7c`. Accent `gold #d4a964`, `gold-hover #c39853`, `on-gold #0a0a0a`, `on-light #0a0a0a`. Semantic `spot-mint #00e599`, `status-active #10b981`, `status-pending #f59e0b`, `status-closed #738396`, `destructive #ef4444`. Legal `legal-surface #ffffff`, `legal-ink #111111`, `legal-surface-alt #f5f5f5`, `legal-border #dddddd`, `legal-checkbox #b98a2f`.

**Retired — must NOT appear** (DESIGN.md 232–235): `ash #575757`, `smoke #454545`, `hairline #050505`, `stage-black #000000`, the `l1–l4` ladder.

**Trap — must NOT appear as type:** `--color-muted` is an alias onto the raised surface `#111111`, surface-only. Not deprecated, must not be deleted from a shadcn compatibility layer, and nothing in 6a consumes it, so it does not ship here. Dim type is always `muted-foreground`.

**Type** (DESIGN.md 38–61). Sans = the system stack, **verbatim**: `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`. Mono = **verbatim**: `var(--font-geist-mono), ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`. Serif = `var(--font-instrument-serif)`, **italic only, never `var(--font-serif)`**. Scale micro 10, label 11, body-small 15, body 16, card-heading 18, section-heading 36, section-heading-wide 48, display 64. Weights 300/400/500 only, **600 maps to 500**. Leading none 1, display 1.05, heading 1.25, body 1.625. Tracking label 0.2em, nav 0.15em, tag 0.05em, display −0.04em.

**Four label roles** (DESIGN.md 268–271), declared in D1 and consumed in D3:
`.label-eyebrow` 11/300/0.2em/sans · `.label-action` 11/500/0.2em/sans · `.label-spec` 10/**400**/0.2em/**mono** · `.label-badge` 10/500/**0.05em**/sans.

**Radius — nine suffixed tokens, all pinned, plus the frontmatter-only bare key** (DESIGN.md 63–75; §18 item 14). Suffixed: `xs` 8, `sm` 8, `md` 16, `lg` 24, `xl` 24, `2xl` 24, `3xl` 24, `4xl` 24, `pill` 9999px. Bare key: the generator reads `bare: 8px` onto `--radius`, and `bare` is **frontmatter-only, not itself a utility name**. `rounded-none` (0) and `rounded-full` (9999px) are hardcoded in the utility and both legal. `rounded-[...]` bypasses the theme and is banned in CI.

**Spacing / layout** (DESIGN.md 79–83, 119–124): section 224px, app-header-top 128px, app-header-bottom 96px. container `max-w-6xl`, gutter `[px-12, md:px-16, lg:px-20]`, chrome_collapse 768px, touch_target 44px.

**Motion** (DESIGN.md 85–96): `ease-enter cubic-bezier(0.16,1,0.3,1)`, `ease-modal cubic-bezier(0.32,0.72,0,1)`; durations micro 140, hover 200, step 220, collapse 300, modal-enter 240, modal-exit 160, shimmer 2000; `scale-press 0.98`, `scale-lift 1.02`.

**Z-ladder** (DESIGN.md 100–104): local [0,10,20], grain −1, sticky 30, nav 40, drawer 50, modal 60.

**Elevation** (DESIGN.md 106–113): panel `0 0 60px rgba(0,0,0,0.6)`, modal `0 0 120px rgba(0,0,0,0.98)`, float `0 30px 80px rgba(0,0,0,0.6)`, card-hover `0 20px 40px rgba(0,0,0,0.45)`, bevel `inset 0 1px 0 rgba(255,255,255,0.05)`, glow-success `0 0 8px rgba(16,185,129,0.6)`, glow-gold `0 0 12px rgba(212,169,100,0.25)`.

**`@utility` bindings — not custom properties.** Per DESIGN.md §18 items 1–2, every token outside a Tailwind `@theme` namespace is bound as an `@utility` declaration, because a bare custom property generates no utility:
- `z-grain` → `-1`; `z-sticky` → `30`; `z-nav` → `40`; `z-drawer` → `50`; `z-modal` → `60`.
- `duration-micro` sets **both** `transition-duration: 140ms` **and** `animation-duration: 140ms` (README §6.5).
- `duration-hover` 200ms, `duration-step` 220ms, `duration-collapse` 300ms, `duration-modal-enter` 240ms, `duration-modal-exit` 160ms → `transition-duration`.
- `duration-shimmer` → `animation-duration: 2000ms` only.
- `scale-press` 0.98 and `scale-lift` 1.02 use Tailwind v4's native **`--tw-scale-x/y/z` + `scale` property** form, **never** `transform: scale()`.

**Component variant enums** (DESIGN.md 126–131) are **declared as data only** — listing-card, status-badge, navigation, footer, mobile-bar, menu-drawer, button, figure-row, form-field. This step builds no component from them except what D3 consumes. Declaring them is part of the compile; building them is not this step.

**Banned everywhere:** raw `hex` / `rgb()` / **`rgba()`** / `hsl()` / `oklch()` outside the `@theme` block — `rgba()` is named explicitly because `border` and `ink` are `rgba()` values, so an executor could write an `rgba()` literal outside the theme and still satisfy a bare "no hex" rule; `bg-[var(--color-*)]`; numeric scale guesses (`bg-canvas-500`); arbitrary values that bypass the theme — `rounded-[...]`, `scale-[...]`, `duration-[...]`, `z-[...]`; `text-muted` (it renders the raised *surface* `#111111` as type); `font-sans` or `font-serif` on a component (`body` owns the face); `var(--font-serif)`; gold as body text or a surface (gold is CTAs, key metrics, monograms only — 3–5% visual weight).

---

## 3 · Assets

**D4 — brand marks.** Source `/home/evo/evolution/engine/brand/logos/` (`lockups/`, `monogram/`, `wordmark/`, `favicon/`, `source-files/`). Vector marks copied as-is into `public/brand/`. No `DESIGN.md` from that folder, no `fonts/`, no `BwGradual` web font anywhere (logo mark only; the wordmark is SVG vector paths).

**D6 — partner marks.** Source `/home/evo/evolution/engine/website/apps/web/public/images/partners/` — 11 files, **9 unique brands**: `arabian-business.png` · `businessdesk.jpg` · `investing-com.png` · `nztr-white.png` · `singularry.png` (+`.webp` dup) · `stephen-grey-racing.png` · `tokinvest-dark.png` + `tokinvest-light.png` (one brand, two cuts) · `trackside-nz.png` · `wexford-stables.png`.

**OPEN-1.** The brief says *six* partner logos; disk holds *nine* unique brands. The plan does not invent a sixth-or-ninth. It copies all nine; D3's marquee renders whatever set the founder names, defaulting to all nine. **Ruling requested.**

**OPEN-2 — no divider source.** The brief's "5 photo dividers (converted to WebP)" has **no source on disk**. `/home/evo/evolution/engine/website/apps/web/public/images/` holds `brand/`, `content/`, `partners/`, `press/` — no divider or feature-photo set. Nearest adjacent: `images/press/`, 17 files, 8 unique outlets. **D5 stays out; `public/images/landing/` is not created. Ruling requested.**

---

## 4 · Landing page (D3) — the nine locked sections

Per README 698–710, "the landing page's nine sections are kept":

1. **Hero** — horizontal brand lockup over a horse image + tagline. No button.
2. **About** — "Own the Experience"
3. **Our Mission** — "How It Works", three audience panels
4. **Our Model** — "Digital Syndication", three icon features
5. **Marketplace** — "Transformation Powered by Regulation", three steps + CTA
6. **News & Updates** — card grid with date/author/publisher metadata
7. **As Featured In** — looping partner-logo marquee
8. **FAQ** — six accordion entries
9. **Closing CTA** — "The Future of Ownership Has Arrived" + footer

Container `max-w-6xl` with gutters `px-12 md:px-16 lg:px-20`, applied at the page shell. Canvas background. At most one italic gold serif word in the whole page. The four label roles used where DESIGN.md assigns them. Zero rows read from Postgres — nothing waits on a policy, on data, or on the missing Cloudflare R2 token.

**Note on section 6:** the brief called this a quiet "Coming Soon" stub. README's locked version is a card grid with metadata. The locked version governs; with no data source in 6a, the grid renders as a static shell and reads zero rows.

---

## 5 · Negative constraints (each falsifiable against a diff)

- **N1** No `@supabase/*` import, no Supabase client, no `fetch` to a Supabase URL in **`website/website/src/`**. Grep. (Rev 3 said `website/src/` — one level short of the real app; corrected.)
- **N2** No import path resolving into `engine/`, and no new shared/workspace package in `pnpm-workspace.yaml` bridging the apps. Import-specifier read + workspace diff.
- **N3** No `hex` / `rgb()` / **`rgba()`** / `hsl()` / `oklch()` literal outside the single `@theme` block in `globals.css`, and no `rounded-[...]` / `scale-[...]` / `duration-[...]` / `z-[...]` arbitrary value anywhere. One file exempt by path for the literals.
- **N4** No `AGENTS.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, or other meta-rule file created anywhere in the repo (PLAN.md §8 item 2 and the Execution Protocol preamble).
- **N5** No new directory matching `theme/`, `tokens/`, `design/`, or a lookbook; no branch other than `main`. Path-and-ref check.
- **N6** No `@font-face`, `next/font` loader, or file in `public/fonts/` for `BwGradual`.
- **N7** No second serif face; no `var(--font-serif)`. The only serif reference is `--font-instrument-serif`.
- **N8** No retired token name or value from §2 in any new file. Grep for the five.
- **N9** No component built from the DESIGN.md §126–131 variant enums beyond what D3 consumes. Enums are data, not a build order.
- **N10** One step, one commit. No multi-step execution across prompt boundaries.

---

## 6 · Non-orphan consumer wiring

| Introduced | Consumer |
|---|---|
| colour tokens for canvas/surface/raised/border/edge/heading/muted-foreground/ink/gold/gold-hover | D3 across the nine sections |
| four `.label-*` roles | D3 section labels, CTAs, card titles, status pills |
| `next/font` faces ×2 | D2 → D3 prose, standfirsts, the one italic gold word |
| ten radius tokens + bare key | pinned ahead of need — **sound, not a loophole**: DESIGN.md §18 item 14 pins every named utility so a Tailwind numeric tier cannot reintroduce a fourth radius; bare `rounded` shipped to 17 call sites at the wrong 4px before it was pinned |
| `z-*`, `duration-*`, `scale-*` `@utility` bindings | pinned ahead of need, same ruling (`DESIGN.md` §18 items 1–2). D3 consumes `duration-hover` for the marquee and `duration-shimmer` for its animation |
| elevation, layout, remaining colour/type tokens, component variant enums | **no 6a consumer.** Covered by the compile ruling in §2 and reused by Steps 6b–10 |

**Flagged for the auditor:** the last row is the one place this plan claims a blanket exemption rather than a call site. The compile ruling is its basis; if you reject it, name which tokens to cut and the founder decides.

---

## 7 · Local verification

`pnpm verify` runs from the **repo root** `/home/evo/evolution/engine_v2/website`, where the script is defined (`verify: typecheck && lint && test && build`). It is **not** defined in `website/website/package.json`. Exit code 0, `--max-warnings=0`. Raw output pasted; self-attestation is void (PLAN.md §4).

## 8 · Audit and push gate

- **Moment 2** runs the §5 invocation verbatim — `kimi-k2.7-code` via Ollama Cloud, headless, stdout/stderr split, blocking wait, 15-minute timeout, timeout = FAIL, verdict read from the **last line** of `.result`. The staged diff is pre-numbered before dispatch. The rubric carries the **explicit `engine/OPERATIONS.md` prose exemption** (PLAN.md §8 item 5) — scope-leakage checks apply to code and configuration only.
- **Commit:** exactly one conventional commit for 6a.
- **Push:** `git push origin main` from `/home/evo/evolution/engine_v2/website` — `origin` is `Badders80/engine-v2`, **not** the sandbox planning repo — then `gh run watch --exit-status`.

---

## 9 · Scope fence, resolved

The step brief said "scope: `website/` only". README §13 assigns two further artifacts to 6a. Resolution: **D7 is inside the app** (`website/website/DESIGN.md`) so there is no conflict. **D8 lands in the repo-root `scripts/`**, which is outside the app directory but inside the same repo and is where the root `test` script already chains its assertions (`assert-no-anti-patterns.sh`, `assert-operations-doc.sh`). It is included because README §13 makes it 6a work and parking it leaves the theme unenforced. **If the founder reads the fence as app-only, D8 drops to Parked and that is the only change.**

## 10 · Still parked

- **PLAN.md gold is wrong.** `PLAN.md:235` reads `gold #c39853`. `#c39853` is `gold-hover`; gold is `#d4a964` (DESIGN.md 20–21). One-line fix, outside this step.

## 11 · Repair ledger — rev 2 → rev 3

| Rev 2 FAIL | Repair |
|---|---|
| F1 `DESIGN.md` deploy parked | Promoted to D7, in scope; §9 |
| F2 enforcement check parked, conflict unresolved | Promoted to D8 with the conflict resolved in §9 |
| F3 block narrowed to frontmatter lines 1–100 | Now lines 1–131: z-ladder, elevation, layout, component enums added |
| F4 `@utility` binding not stated | §2 `@utility` paragraph; shimmer on `animation-duration` |
| F5 "eleven radius entries" | Corrected to ten named tokens + the frontmatter-only bare key |
| F6 mono stack abbreviated with "…" | Verbatim stack |
| F7 four label roles missing | §2 with all four specs |
| F8 `engine/OPERATIONS.md` exemption missing | §8 |
| F9 landing outline vague vs nine locked sections | §4 now the nine, with the section-6 change noted |
| F10 wrong `pnpm verify` path | §7 corrected to repo root |

### Rev 3 → rev 4

| Rev 3 FAIL | Repair |
|---|---|
| B2 the compile ruling overstated what `@theme` can generate | §2 restated as a three-tier artifact: `@theme` properties (namespaced keys only) · `@utility` declarations (z, durations, scales) · documented rules as comments (layout, component enums) |
| B1 sans stack value omitted | §2 now carries the verbatim stack from DESIGN.md:39 |
| B3 `@utility` binding details incomplete | §2: `duration-micro` sets both `transition-duration` and `animation-duration`; scales use Tailwind v4 `--tw-scale-x/y/z` + `scale`, never `transform: scale()` |
| A5 radius prose miscount | §2: "nine suffixed tokens plus the frontmatter-only bare key" |
| B10/N1 wrong app path in N1 | §2 N1 corrected to `website/website/src/` |
| B10/N3 `rgba()` not banned | §2 N3 and the banned list now name `rgba()` explicitly, plus `text-muted` and the arbitrary-value families |
