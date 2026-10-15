# audit/design — the V2 design system extraction

> **What this is:** the audit that produces a clean, V2-only `DESIGN.md` and the token set
> that `website/src/app/globals.css` will carry, so that every page built from here —
> marketplace, horse page, MyStable — is *assembled from decisions already made* rather
> than re-invented.
>
> **Status:** spec written, not run. Needs one ruling (see **Ruling required**) before it
> can land.
>
> **Shape:** README · SPEC · out/. Markdown only, per `v2/README.md:29` ("This folder is
> markdown"). No venv, no imports, no scripts until the harvest is designed.

## Why this exists

The V2 build shipped steps 1–5 with **no design authority in the repo at all**. Impeccable's
context loader, run 2026-10-15 against `engine_v2/website`, returned:

```
designPath: null    productPath: null    hasVisualImplementation: false
```

The only design system document in the estate is `evolution/engine/brand/DESIGN.md`, and
`PLAN.md:233` rules that it **stays behind** — correctly, because it is V1-contaminated: it
cites `@evo/ui`, `app/horses/[slug]/about/page.tsx`, the token generator, and
`comms/automated-comms/build-surface.mjs`.

So `PLAN.md:233` tells 6a to "transcribe the tokens once into `website/src/app/globals.css`"
while nothing anywhere records **what those token values are**. They are named — canvas,
gold `#c39853`, the system sans, Geist Mono, Instrument Serif — but never transcribed.

Meanwhile the stated problem is real and historical: **drift with ad-hoc elements across the
marketplace, the horse page, and MyStable.** The estate has already suffered at least one
documented instance of exactly that (`DESIGN.md:83-84`: Geist Sans reached four route files
through a `font-sans` utility while `body` inherited the system stack). A `DESIGN.md` existed
throughout. That is the whole argument for this audit's second half: **a document alone did
not prevent drift, so the deliverable is a document plus a mechanism.**

## Ruling required before this lands

`PLAN.md:150` — *"The landing page is the visual north star. There is NO separate design pass,
design token gate, or lookbook."*
`PLAN.md:275` — parks *"per-page styling, a lookbook, and any token beyond the 6a theme file."*

This audit **is** the lookbook, pulled forward from the post-build visual pass into the build
critical path. That is an amendment to `PLAN.md`, not an extension of 6a. Per the house rule in
`~/.claude/CLAUDE.md`, a changed ruling updates the SSOT file **and** the source doc it cites.
Until that amendment is written, this folder is a proposal.

## Scope

**In:**
- The token set: colour, type roles, spacing rhythm, radii, borders, elevation, motion, breakpoints.
- The component *decisions* that must be locked so a card, a button, a status badge, and a
  listing row are reused rather than re-invented.
- The drift mechanisms catalogued from the estate's own history, so the spec prevents causes
  rather than symptoms.
- The target `DESIGN.md`: its sections, its home, and how it stays true.
- The enforcement half: a mechanical check, in the existing gate style.

**Out:**
- Page layout and grids. They differ legitimately per page; tokenising them manufactures
  drift of its own.
- Copy and content. The landing page's copy is a separate question (see Open decisions).
- Business logic, pricing, data. This audit never touches `dsls`, `horses`, or the rules engine.
- Anything in `engine/`. Scope is the design system the website consumes.

## Precedence of truth

When two sources disagree, the winner is fixed:

1. **The live landing page** — wins on *values*. `PLAN.md:150` makes it the visual north star,
   and the brand audit rules that where `brand/DESIGN.md` and the live landing page disagree,
   **the live landing page wins**.
2. **`evolution/engine/brand/DESIGN.md`** — wins on *rulings*. It carries decisions that are not
   observations: which faces are retired, the single serif-drama exception, the label roles.
   These survive the rewrite as constraints even though the document itself stays behind.
3. **`PLAN.md`** — wins on *scope*. What 6a may and may not do.

## Coverage map

Six workstreams. `SPEC.md` holds the detail for each.

| # | Workstream | Produces |
|---|---|---|
| A | **Harvest** — read the real values off the live landing page | A ground-truth table: every colour, size, weight, tracking, radius, and spacing value, with the element it came from |
| B | **Token model** — how those values become tokens | The `@theme` block in `globals.css`, its categories, and its naming |
| C | **Pattern locks** — the components | Decision-level specs for card, button, badge, nav, listing row, form field |
| D | **Drift mechanisms** — why it went wrong before | A catalogue of the causes, each with the guard that prevents it |
| E | **Target `DESIGN.md`** — the end result | The document, its sections, and where it lives |
| F | **Enforcement** — how it stays true | A gate check in the `assert-*.sh` style, plus the audit rubric hook |

## What this audit produces

```
audit/design/
├── README.md      ← this file: the map
├── SPEC.md        ← the full spec: workstreams A–F
├── SOURCE-TRUTH.md  (on run) the harvest output — values with provenance
└── out/
    ├── report.md    (on run) findings, in the house audit shape
    └── gate.json    (on run) machine-readable pass/fail
```

The **only** artifact that leaves this folder is the finished `DESIGN.md` and the `@theme`
block, both landing in the build repo.

## Where the outputs go

| Artifact | Home | Note |
|---|---|---|
| The V2 `DESIGN.md` | `evolution/engine_v2/website/website/DESIGN.md` | New file, in the build repo next to the app it describes. `PLAN.md:201` bans `CLAUDE.md` and `AGENTS.md` there — `DESIGN.md` is **not** on that list, and the brand audit treats it as the intended companion. |
| The tokens | `evolution/engine_v2/website/website/src/app/globals.css` | `PLAN.md:151`. Currently 23 bytes: `@import 'tailwindcss';` |
| The enforcement check | `evolution/engine_v2/website/scripts/` | Alongside `assert-no-anti-patterns.sh` and `assert-operations-doc.sh`, chained in the root `pnpm test` |

## How this plugs into the build

`PLAN.md` currently runs 6a → 6b → 7 → 8 → 9. This audit sits **before 6a** and changes what
6a is: 6a becomes "consume the locked system" rather than "invent the token values".

Downstream is already bound: `PLAN.md:153` — marketplace, horse listing, and MyStable
*"reuse the established theme file. They do not introduce new tokens or palettes."*
`PLAN.md:243` — *"6b introduces no new tokens: it reuses the 6a theme file."*

So this is the one pass that sets the values, and every later step is forbidden from adding
more. That is the point of doing it deliberately rather than during 6a.

## Constraints on this folder

- **Sandbox island law holds** (`sandbox/AGENTS.md`): `just check` must stay 10/10. Writing
  markdown here does not affect it — `audit/` already carries `.py` and `.json`.
- **Markdown only**, matching `v2/`. No venv, no dependencies, no scripts until the harvest
  is designed and agreed.
- **Never reintroduce a banned legacy token.** The gate scans for ten, including `brand_dna`
  and `orca`. `DESIGN.md` is prose and must not carry any of them back in.

## Open decisions

Four open, one answered. `SPEC.md` §12 carries the detail.

1. **The ruling** — amend `PLAN.md` §7 and §Ruling 4 to pull the design pass forward, and settle
   the amendment's own lookbook exclusion wording.
2. ~~**"Replicate" means what?**~~ — **answered 2026-10-15.** Keep the landing page as it is: its
   sections, its copy, its look. Its nine-section structure is now recorded in `SPEC.md` §3, which
   replaces the *"6a's structure is unspecified"* note at `engine_v2/CONTINUE.md:26-29`.
3. **Token granularity** — how far past colour and type to go: spacing and radii are proposed;
   shadows and motion are open.
4. **Where `DESIGN.md` lives** — proposed in the build repo; confirm.
5. **Enforcement strength** — fail the gate on an unknown colour, or warn. Fail is proposed,
   because warn is how the last drift survived.

## Next action

Confirm the map. Then `SPEC.md` gets exercised in order: **A** (harvest the live page into
`SOURCE-TRUTH.md`), which is read-only and produces the values everything else depends on.
