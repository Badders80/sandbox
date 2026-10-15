# SPEC — the V2 design system extraction

> The full spec behind `README.md`. Six workstreams. Every claim here cites a real path,
> a real ruling, or a real observation from the estate.

## 1 · Purpose and end result

**Purpose.** Pull the design decisions out of one page — the live landing page — and lock them
so that every page after it is assembled, not invented. The stated failure is drift: ad-hoc
elements in the marketplace, the horse page, and MyStable.

**End result, stated as three artifacts:**

1. A clean `DESIGN.md` that describes **only** V2, is the starting point of all further building,
   and carries no V1 reference.
2. A `@theme` block in `website/src/app/globals.css` carrying the values, so the document and the
   code cannot disagree.
3. A gate check that fails when a later page invents a colour, a face, or a component variant.

**Why three and not one.** A `DESIGN.md` already existed throughout the period when the drift
happened. `DESIGN.md:83-84` records the instance: Geist Sans *"reached the page through a
`font-sans` utility on four route files while `body` inherited the system stack."* A document
did not prevent it. The mechanism is what prevents it.

## 2 · What is already locked — do not re-open

These are settled rulings. The audit records them, does not relitigate them.

| Face | Role | Delivery | Ruling |
|---|---|---|---|
| **System sans stack** | Primary UI + body | No file. `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, …` | `DESIGN.md:78` |
| **Geist Mono** | Financials, hashes, countdowns, tabular figures — **and the editorial voice**: standfirsts and secondary-page eyebrows | `next/font`, referenced as `var(--font-geist-mono)` | `DESIGN.md:79`, extended 2026-09-23 |
| **Instrument Serif** | **"Reserved drama" — one italic gold word inside a page headline, and nothing else** | `next/font` as `var(--font-instrument-serif)`. The stack reads **that** variable, never `var(--font-serif)` | `DESIGN.md:80`, ruled 2026-09-23 |
| **Bw Gradual** | **Logo mark only — not a web font.** Nothing on the website loads it; the wordmark is SVG vector paths | Ships in `brand/fonts/` | `DESIGN.md:81` |
| **Geist Sans** | **RETIRED 2026-09-22.** Lives in `brand/fonts/retired/` | — | `DESIGN.md:83-84` |

**Two traps this table exists to prevent.** `brand/fonts/` sits next to `brand/logos/` and
invites a wholesale copy — but it holds Bw Gradual (must never load) and `retired/GeistSans-VF.woff2`
(reintroducing it reverses a locked ruling). `PLAN.md:233` already says *"copy the logos"*; read
literally that is correct, and this audit makes the reason explicit so nobody "helpfully" adds fonts.

**Instrument Serif is not a file in the cupboard.** It arrives via `next/font`. Any harvest step
looking for a `.woff2` will not find one, and must not conclude the face is missing.

**Palette and type are already named, not yet valued.** `PLAN.md:233` names canvas, gold
`#c39853`, the system sans for prose, Geist Mono for figures, Instrument Serif for the one italic
emphasis. Workstream A is what turns those names into values.

**Existing label roles to preserve, not reinvent** (`DESIGN.md:150-151`):

| Class | Size | Weight | Tracking | Face | Used for |
|---|---|---|---|---|---|
| `.label-eyebrow` | 11px | 300 | 0.2em | sans | section labels, eyebrows, nav — the workhorse |
| `.label-action` | 11px | 500 | 0.2em | sans | caps that are clicked, and gold status |

## 3 · Workstream A — Harvest (the live landing page)

**What:** read the real values off the live landing page and record each with provenance.
**Why first:** every other workstream consumes this. It is read-only and blocks nothing.

**Recorded — decision 2, 2026-10-15.** The landing page is kept as it is: its sections, its copy,
its look. Its nine sections, in order. This is what retires the *"6a's page structure is not
specified"* note at `engine_v2/CONTINUE.md:26-29` — keeping the page means keeping its structure:

```
1  Hero            horizontal brand lockup over a horse image + tagline
2  About           "Own the Experience"
3  Our Mission     "How It Works" — three audience panels
4  Our Model       "Digital Syndication" — three icon features
5  Marketplace     "Transformation Powered by Regulation" — three steps + CTA
6  News & Updates  card grid, date/author/publisher metadata
7  As Featured In  looping partner-logo marquee
8  FAQ             six accordion entries
9  Closing CTA     "The Future of Ownership Has Arrived" + footer
```

**Harvest list — seven categories:**

1. **Colour** — canvas/base, raised surface, ink, muted ink, gold `#c39853`, gold hover/active,
   borders and dividers, and the four status colours that already exist as an enum in the
   database (`coming_soon`, `available`, `fully_allocated`, `completed` — type `public.status`,
   defined `00001_enums.sql:9`, used `00005_dsls.sql:19`).
2. **Type roles** — for each: family, size, weight, letter-spacing, line-height, case, and the
   live element it is used on. Must include the two label roles above.
3. **Space** — the rhythm the page actually uses, expressed as a scale rather than a list of
   one-off paddings.
4. **Shape** — corner radii, border widths, and where a border is a divider versus a container.
5. **Depth** — any shadow or elevation, and whether the page leans on border instead.
6. **Motion** — durations and easings for hover, focus, and any transition. Record if there is none.
7. **Interactive states** — default, hover, focus-visible, active, disabled, loading, empty, and
   error for every interactive element found.

**Provenance is mandatory.** Every value is recorded with the element and property it came from,
so it can be re-verified later.

**Why re-runnable matters.** The live page is the source of truth and it will change — the domain
cutover is coming (`PLAN.md:107`). The harvest is a **method**, recorded so the values can be
re-checked, not a one-off copy-paste.

## 4 · Workstream B — Token model

**The file:** `website/src/app/globals.css`. Currently 23 bytes — `@import 'tailwindcss';`.
Tailwind **4.3.3**, Next **15.5.27**.

**The mechanism, and the trap.** Tailwind v4 maps *namespaced* custom properties to utilities:
`--color-*` → colour utilities, `--font-*` → font-family, `--text-*` → font-size, `--spacing-*`,
`--radius-*`, `--shadow-*`, `--ease-*`, `--breakpoint-*`. **A custom property outside a known
namespace generates no utility at all** — it exists as a variable and nothing can use it. The
naming convention is therefore not cosmetic; decide it once and freeze it.

**Categories proposed for tokenisation:**

| Tokenise | Why |
|---|---|
| Colour | The reported drift. Highest value. |
| Type roles (family + size + weight + tracking + leading as one named role) | Prevents the two-face page. A role cannot be half-applied. |
| Space rhythm | Prevents every page inventing its own padding. |
| Radii, border widths | Cheap, and a visible drift signal. |
| Interactive states | The drift nobody notices until it is on ten pages. |

**Categories deliberately NOT tokenised:**

- **Layout and grids.** Page arrangements differ legitimately. Tokenising them manufactures drift
  of its own — a token that only one page can use is not a token, it is a hard-coded value wearing
  a costume.
- **Content and copy.** Not design.
- **Shadows, motion, breakpoints** — *open decision 3*. Proposal: record the values, tokenise only
  what the live page actually uses in more than one place.

**The guardrail, stated plainly:** lock **decisions, not markup.** A spec that pins exact JSX rots
the first time React or Tailwind shifts; people route around it, and routing around it is how the
drift started. Lock the vocabulary — "this colour, this role, this variant" — and let the markup
follow.

**The second guardrail:** over-tokenising is its own drift source. A 200-token system that nobody
can hold in their head gets ignored, and an ignored system is a dead one.

## 5 · Workstream C — Pattern locks

A component is locked at **decision level**, in a fixed schema:

```
Name and job      — one sentence, what it is for
Anatomy           — its slots, and which are required
Variants          — a CLOSED list. Adding one is a ruling.
States            — default · hover · focus-visible · active · disabled · loading · empty · error
Tokens consumed   — which tokens, and ONLY which tokens
Content rules     — max lines, truncation, what may never appear inside it
Do-not            — the explicit anti-patterns, each naming the drift it caused
```

**Components to lock, in priority order:**

1. **Listing card** — the marketplace unit. Highest drift exposure.
2. **Status badge** — the four statuses are already a database enum; the badge must not invent a
   fifth look. Coming Soon is visible and cannot be bought; Available means Buy Now
   (`PLAN.md:243`).
3. **Button hierarchy** — primary, secondary, and the disabled/loading forms of each.
4. **Figure row** — the mono-figures pattern. `DESIGN.md:79` puts Geist Mono on financials and
   tabular figures specifically, so this is a token decision, not a styling choice.
5. **Nav and footer** — shared across every page, so the first place a per-page variant appears.
6. **Form field** — buyer and operator inputs share a look; the error state is the drift risk.

**The "closed list" rule is the whole mechanism.** The drift was not one wrong colour; it was a
second and third variant of the same thing. A variant list that is closed by default means adding
one requires a ruling, which is a conversation instead of an accident.

## 6 · Workstream D — Drift mechanisms

The estate's own history, catalogued so the spec prevents **causes**, not symptoms.

| # | Mechanism | Documented evidence | Guard that prevents it |
|---|---|---|---|
| 1 | **Utility class over inheritance** — a face applied per-file while the parent sets another | `DESIGN.md:83-84`: Geist Sans reached four route files via `font-sans` while `body` inherited the system stack | `body` owns the face. A component may only name a **role**, never a family. |
| 2 | **Unpinned generic fallback** — a raw generic resolving differently per OS | `DESIGN.md:80`: `font-serif` rendered Georgia on macOS, Times New Roman on Windows, Noto Serif on Android — one page, three faces | Never use a raw generic (`font-sans`, `font-serif`). Only named role tokens. |
| 3 | **Ad-hoc colour** — a hex literal written at the point of use | The reported drift across marketplace, horse page, MyStable | No hex literal outside `globals.css`. Mechanical, via Workstream F. |
| 4 | **Per-page palette invention** | `PLAN.md:153` forbids it for later pages; `PLAN.md:243` repeats it for 6b | Make the prohibition mechanical rather than remembered. |
| 5 | **Component re-invention** — the same component built twice with different padding or states | Implied by the drift report | Workstream C, closed variant list. |
| 6 | **Hand-typed label styling** — repeating an 11px/0.2em/weight recipe per page | `DESIGN.md:150-151` already had `.label-eyebrow` and `.label-action` as classes, which means they were being applied by hand | Label roles become tokens, so the recipe exists once. |

**Two lessons this table encodes.** Every one of these is a *value written at the point of use*
instead of *a name referring to a decision*. And every one survived because the system was
documented but not **checked**.

## 7 · Workstream E — Target `DESIGN.md`

**The shape** — adapted from the getdesign.md pattern the founder referenced
(`getdesign.md/linear.app`, `getdesign.md/x.ai`), which is: identity → tokens → type roles →
component patterns → do/don't.

```
1  Identity          One line: what this looks like, and the surface mode it serves
2  Non-negotiables   The locked rulings. Retired faces, the one serif word, the label roles
3  Colour            Token name · value · when to use · when never
4  Type              Role table: family, size, weight, tracking, leading, case, where used
5  Space             The rhythm scale
6  Shape             Radii and borders
7  Depth             Elevation, or an explicit "borders carry this instead"
8  Motion            Durations, easings, and what is allowed to move
9  Components        Workstream C, verbatim
10 Do / Don't        The anti-patterns, each naming the drift it caused
11 Provenance        Where every value came from, and how to re-verify it
```

**Where it lives:** `evolution/engine_v2/website/website/DESIGN.md`.
`PLAN.md:201` bans `CLAUDE.md` and `AGENTS.md` in the build repo. `DESIGN.md` is not on that
list, and the brand audit treats it as the intended companion (*"A short `DESIGN.md` is written
from that file and the finished page before Marketplace starts"*, `06-status-tokens.md:38`).

**The single-source rule, and why it matters more than the prose.** If `DESIGN.md` restates the
values and `globals.css` declares them, there are two sources of truth, and two sources of truth
is the definition of drift. **`globals.css` is the machine truth. `DESIGN.md` cites it.** Workstream
F includes a check that compares the document's stated values against the theme file, so the prose
cannot silently fall behind the code.

**Naming caution.** `PLAN.md:150,275` ban the word *lookbook*. This audit deliberately does not
produce one, and does not call its output one. The output is an audit and a `DESIGN.md`.

## 8 · Workstream F — Enforcement

**The mechanism already exists in this repo.** `scripts/assert-no-anti-patterns.sh` scans 61 files
for ten banned legacy tokens and fails the gate; `scripts/assert-operations-doc.sh` asserts another
invariant. The root `pnpm test` chains both, and `pnpm verify` runs typecheck → lint → test → build.

**Proposed checks, in the same style:**

1. **No colour literal outside `globals.css`** in `website/`. Catches mechanism 3.
2. **No raw generic font utility** (`font-sans`, `font-serif`) and no `font-family` declaration
   outside `globals.css`. Catches mechanisms 1 and 2.
3. **`DESIGN.md` values match `globals.css`.** Catches the two-sources-of-truth failure.

**Scope of the checks: code and configuration only.** Prose in `engine/OPERATIONS.md` is exempt,
per the existing ruling — that guide describes the whole product by design and is not code.

**Plus the audit hook.** Each remaining build step already goes through the gemma4:31b rubric.
A design-token item belongs in that rubric from 6a onward, so a step that invents a colour fails
its audit rather than passing it.

**Strength: fail, not warn.** *Open decision 5.* Warn is how the last drift survived.

## 9 · Non-goals

- Not a redesign. `PLAN.md:150` makes the landing page the north star; its look is kept.
- Not a component library with its own conventions and ceremony — `PLAN.md:150` rules out a design
  pass, a token gate, and a lookbook.
- Not a change to any page. This audit writes documents; the build consumes them.
- Not a V1 migration. Nothing from `@evo/ui`, the old token package, or the generator is carried over.
- Not in `engine/`. Scope is the system the website consumes.

## 10 · Sequencing

```
Ruling  → the PLAN.md amendment (§Ruling required in README)
A       → harvest the live page into SOURCE-TRUTH.md   [read-only, blocks nothing]
B       → token model decided, naming frozen
C       → pattern locks written
D       → drift mechanisms catalogued (can run alongside B and C)
E       → DESIGN.md written, citing globals.css
F       → gate check written and chained
        → 6a becomes: consume the locked system, build the landing page
        → 6b, then 7, 8, 9 — all already bound by PLAN.md:153 and :243
```

## 11 · Acceptance criteria

- `SOURCE-TRUTH.md` records every value with provenance, and nothing is inferred.
- Every token in `globals.css` sits in a Tailwind v4 namespace, so each generates a utility.
- No hex literal exists outside `globals.css` anywhere in `website/`.
- `DESIGN.md` describes no V1 artifact, and reintroduces none of the ten banned legacy tokens.
- Every component in Workstream C has a closed variant list and a named do-not.
- The gate fails when a new colour or a raw generic font utility is introduced — demonstrated by
  actually introducing one and watching it fail, not by asserting that it would.
- `pnpm verify` passes with the new check chained in.

## 12 · Open decisions

| # | Decision | Status |
|---|---|---|
| 1 | Amend `PLAN.md` §7 and §Ruling 4 to pull the design pass forward into the build critical path, updating the source doc it cites | **Open** — required before anything here lands |
| 2 | Does "replicate" mean the live page's sections and copy, or its look? | **ANSWERED 2026-10-15** — keep the landing page as it is: its sections, its copy, its look. Its nine-section structure is now known (§3) and replaces the "structure unspecified" note at `engine_v2/CONTINUE.md:26-29` |
| 3 | Token granularity past colour and type | **Open** — spacing and radii yes; shadows and motion only if used in more than one place |
| 4 | `DESIGN.md` home | **Open** — proposed: the build repo, `website/DESIGN.md` |
| 5 | Enforcement strength | **Open** — proposed: fail the gate. Warn is how the drift survived |
