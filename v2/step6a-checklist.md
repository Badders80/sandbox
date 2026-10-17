# Step 6a — LOCKED CHECKLIST (Moment 1, round 4)

**Verdict: `VERDICT: PASS`.** Locked 2026-10-17 by the independent auditor (`kimi-k2.7-code`, Ollama Cloud, headless).
Audited plan: `/tmp/step6a-plan.md` (revision 4). Audit output: `/tmp/audit4.out`.
Round 4 graded **no items FAIL**. Rounds 1–3 were FAIL (4, 10 and 6 items respectively); every finding was repaired and re-audited, never overridden.

**This checklist is the Moment 2 rubric.** Moment 2 audits the pre-numbered staged diff against these items, one at a time, PASS/FAIL with a `file:line` citation. A dummy citation fails the item.

---

1. `website/website/src/app/globals.css` contains exactly one `@theme { … }` block, carrying all namespaced custom properties derived from `DESIGN.md` frontmatter (`--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`, `--radius-*`, `--spacing-*`, `--shadow-*`, `--ease-*`). **No `--duration-*`, `--scale-*` or `--z-*` custom property appears inside `@theme`.**
2. `globals.css` declares `@utility` blocks: `z-grain -1`, `z-sticky 30`, `z-nav 40`, `z-drawer 50`, `z-modal 60`; `duration-micro` sets **both** `transition-duration` and `animation-duration`; `duration-hover/step/collapse/modal-enter/modal-exit` set `transition-duration`; `duration-shimmer` sets `animation-duration`; `scale-press`/`scale-lift` use `--tw-scale-x/y/z` with the `scale` property and **never** `transform: scale(…)`.
3. `globals.css` documents the `layout` values (`max-w-6xl`, gutters, `chrome_collapse`, `touch_target`) and the `components` variant enums **as comments**; they generate no utilities.
4. `layout.tsx` wires exactly two `next/font` faces: Geist Mono (`--font-geist-mono`) and Instrument Serif (`--font-instrument-serif`). No `@font-face`, loader or file for BwGradual; no `var(--font-serif)`.
5. `page.tsx` renders the nine locked sections — Hero, About, Our Mission, Our Model, Marketplace, News & Updates, As Featured In, FAQ, Closing CTA — with `max-w-6xl px-12 md:px-16 lg:px-20`, canvas background, the four `.label-*` roles, at most one italic gold serif word, and zero Postgres/Supabase fetching.
6. `public/brand/` is populated from `/home/evo/evolution/engine/brand/logos/` with web-ready vector assets only. No BwGradual web font, no `brand/DESIGN.md`, no `fonts/` directory.
7. `public/images/partners/` contains the nine unique partner marks listed in the plan.
8. **`public/images/landing/` is not created** — D5 refused, no source exists.
9. `website/website/DESIGN.md` exists as a copy of `/home/evo/sandbox/audit/design/DESIGN.md`.
10. A design-enforcement script is added under `website/scripts/`, chained into the root `pnpm test`, and fails CI on raw colour literals, raw Tailwind palette utilities, generic font utilities (`font-sans`/`font-serif`) and `text-muted` inside `website/website/src/`.
11. Root `package.json` retains `verify`; `website/website/package.json` does not define it; `pnpm verify` exits 0 with `--max-warnings=0`.
12. The diff contains no `@supabase/*` imports/clients/fetches in `website/website/src/`, no import resolving into `engine/`, no `AGENTS.md`/`CLAUDE.md`/`HOW-WE-WORK.md`, no new `theme/`/`tokens/`/`design/` directory, no retired token name or value, no component built from the `components` variant enums beyond D3, and **exactly one conventional commit**.
13. Moment 2 itself runs with the staged diff pre-numbered, `kimi-k2.7-code`, split stdout/stderr, a 15-minute blocking timeout, and the verdict read from the **last** non-empty line of `.result`.

---

## Still open — founder rulings, not executor decisions

- **OPEN-1.** The brief says six partner logos; disk holds nine unique brands. Plan copies all nine and lets the founder name the rendered subset.
- **OPEN-2.** The brief's "5 photo dividers (converted to WebP)" has no source on disk. D5 refused.
- **PLAN.md gold.** `PLAN.md:235` reads `gold #c39853`; `#c39853` is `gold-hover`. Gold is `#d4a964` (`DESIGN.md:20-21`). One-line fix, outside this step.
