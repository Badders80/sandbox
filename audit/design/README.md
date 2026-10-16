# audit/design — the V2 design system extraction

> **What this is:** the audit that produces one clean, V2-only `DESIGN.md` — the document every
> page of the V2 build is assembled from — plus the token set it compiles to, and the check that
> keeps the two true.
>
> **Status:** gathering — **eleven of §7's thirteen sections are ready**, and **Workstream C is
> complete**: nine components locked in `COMPONENTS.md`. STEP1 (landing), STEP2
> (marketplace) and STEP3 (MyStable) are closed. Colour, layout and the container are shut, and
> **Do/Don't (#12) closed 2026-10-16** — `SECTION10-DO-DONT.md`. **Provenance was cut from the
> skeleton** the same day (§9, §18 item 12): the evidence lives in `SOURCE-TRUTH.md`, not in the
> spec. The document itself is **not yet written** — see **§7, the bill of materials**, for the two
> rows still standing between this table and a one-pass write.
>
> **Shape:** this README, plus `STEP1-LANDING-PAGE.md`, `STEP2-MARKETPLACE.md`,
> `STEP3-MYSTABLE.md` as the evidence files, `COMPONENTS.md` as the Workstream C working file,
> `SECTION10-DO-DONT.md` as the target `DESIGN.md` section 10, and `SOURCE-TRUTH.md` as the provenance
> ledger behind section 11. Markdown only. No venv, no imports, no scripts.

---

## 1 · What we are building

**One `DESIGN.md`, and it is the authority.**

The pattern is fixed and not up for reinvention — the
[getdesign.md](https://getdesign.md/x.ai/) /
[refero](https://styles.refero.design/style/90ce5883-bb24-4466-93f7-801cd617b0d1) form:

- **YAML frontmatter** carrying the tokens as machine-readable data (`colors`, `typography`,
  `rounded`, `spacing`, `components`), so the document is readable by a human *and* by an agent
  building from it.
- **Short, tabular sections** — Overview, Colours, Typography, Layout, Elevation, Shapes, Motion,
  Components, Do/Don't.
- **Values inline, not referenced.** The document is self-contained. Hand it to someone with no
  access to the repo and they have the whole system.

**The `@theme` block is its compiled output.** `DESIGN.md` states the values; the Tailwind v4
`@theme` block in `globals.css` is derived from it and is what the build consumes. Where they
disagree, the document is the source and the CSS is wrong — and **§11, Workstream F**, makes that
mechanical rather than a matter of discipline. Two artifacts, one authored, one compiled, one
check asserting they are identical.

**Why a document alone is not enough.** The estate already ran this experiment. A `DESIGN.md`
existed throughout the period when the drift happened. `brand/DESIGN.md:83-84` records the
instance: Geist Sans *"reached the page through a `font-sans` utility on four route files while
`body` inherited the system stack."* The document did not prevent it. So the deliverable is a
document **plus** the mechanism that checks it, and nothing here ships without both.

### The mode we are in

**We are gathering, not writing.** The purpose of this phase is to assemble every correct input —
each value, each ruling, each piece of provenance — so that when we hit *play* on `DESIGN.md`, it
is written **in one pass**. No drafting, no discovering a missing decision halfway through, no
second pass. **§7 is the test of readiness:** when every line of it is closed, we are at play.

---

## 2 · Why this exists

The V2 build shipped steps 1–5 with **no design authority in the repo at all**. Impeccable's
context loader, run 2026-10-15 against `engine_v2/website`, returned:

```
designPath: null    productPath: null    hasVisualImplementation: false
```

The only design system document in the estate is `evolution/engine/brand/DESIGN.md`, and
`PLAN.md:235` rules that it **stays behind** — correctly, because it is V1-contaminated: it cites
`@evo/ui`, `app/horses/[slug]/about/page.tsx`, the token generator, and
`comms/automated-comms/build-surface.mjs`.

So `PLAN.md:235` tells 6a to *"transcribe the tokens once into `website/src/app/globals.css`"*
while nothing anywhere records **what those tokens are**. They are named — canvas, gold, the
system sans, Geist Mono, Instrument Serif — but never valued. This audit is what turns the names
into values, once, deliberately, outside the build critical path.

---

## 3 · The governing rule: zero debt

**Zero debt enters this folder.** Every file here is either written from our own decisions, or
explicitly adopted from `audit/website/` after review. No bulk imports.

- **Artifacts never cross.** No file from `audit/website/` is copied in. This is mechanical, not
  stylistic: the build-repo gate fails the commit on ten banned legacy tokens, and `brand_dna`
  alone appears in four bridge files. A straight copy cannot survive contact with the gate.
- **Rulings cross deliberately** — one at a time, restated in our own words, with provenance. A
  decision carries no legacy vocabulary; a copied document does.

The archive states the principle better than we did, in its own words
(`/home/evo/audit/website/DEFECT-HISTORY-2026-10-16.md:11,46-48`):

> *"The rulings live in the V2 specification. The defects live here — because a defect in the old
> build is a fact about the old build, and the old build is not the spec."*

> *"A specification that carries a list of the old build's mistakes is a specification arguing with
> a codebase that will not exist."*

The ten tokens the gate arms:

```
INVENTORY_UUID_BY_SLUG   LEGACY_SLUG_ALIASES   slugCandidates   HORSE_STILLS
DEFAULT_CDN_HOST         CONTENT_DIR           resolveHorseSlug  REFUND_WINDOW_DAYS
brand_dna                orca  (case-insensitive)
```

---

## 4 · Standalone by design

`sandbox/v2` is a markdown-only planning island — `v2/README.md:29`: *"This folder is markdown.
Reading the brief is the work."* A ~40-token extraction plus a gate script has no home there, and
`PLAN.md:152` explicitly rules out a design pass on the build critical path.

So this runs as a **separate function**, 100% standalone:

1. Finish the document here, on its own terms.
2. **Then** go into `PLAN.md` and point it at the result.

**Not before.** You cannot write an informed amendment until you know what you are amending for —
and the token scope has already moved from the six values `PLAN.md:235` names to the full set.
`PLAN.md` is not touched while this work is in progress. The amendment is a **downstream step, not
a precondition.**

---

## 5 · Precedence of truth

When two sources disagree, the winner is fixed:

1. **The live landing page** — wins on *values*. `PLAN.md:152` makes it the visual north star, and
   the brand audit rules that where `brand/DESIGN.md` and the live landing page disagree, the live
   landing page wins.
2. **`evolution/engine/brand/DESIGN.md`** — wins on *rulings*. It carries decisions that are not
   observations: which faces are retired, the single serif-drama exception, the label roles. These
   survive as constraints even though the document itself stays behind.
3. **`PLAN.md`** — wins on *scope*.

**The bridge, `/home/evo/audit/website/`**, is reference only. It records what the old build had.
It is mined surgically and never quoted from directly — see §3.

**A trap that has already been sprung once.** Two files in that folder are *forward-looking drafts*,
not records: `V2-DESIGN-SPEC-2026-10-16.md` and `V2-THEME-2026-10-16.css`. The second is 440 lines
and contains `.press`, `.collapse-panel`, `.sticky-buy-bar` and `.legal-doc`. **None of those four
exist in the live build**, whose theme is 169 lines. So a review that checks a draft against "the
theme" and cites `:371-373` is checking it against a *proposal* and reporting the proposal back as
verified. That is not verification; it is a mirror.

The test is mechanical. A value is **verified** only if it is found in
`evolution/engine/website` — the app, or `packages/brand_dna/src/theme.generated.css`. A value found
only under `/home/evo/audit/website/` is a **proposal**, however confident the prose around it
reads, and it needs either a ruling to adopt it or a line explaining why it diverges. §5 makes the
live page the winner on values; a draft does not become the live page by being well written.

---

## 6 · What is already locked

Settled rulings and values. The audit records these; it does not relitigate them.

### 6.1 Faces

| Face | Role | Delivery | Ruling |
|---|---|---|---|
| **System sans stack** | Primary UI + body | No file. `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, …` | `brand/DESIGN.md:78` |
| **Geist Mono** | Financials, hashes, countdowns, tabular figures — **and the editorial voice**: standfirsts, secondary-page eyebrows | `next/font`, as `var(--font-geist-mono)` | `brand/DESIGN.md:79` |
| **Instrument Serif** | **"Reserved drama" — one italic gold word inside a page headline, and nothing else** | `next/font` as `var(--font-instrument-serif)`. The stack reads **that** variable, never `var(--font-serif)` | `brand/DESIGN.md:80` |

**Why the stack must not read `var(--font-serif)` — corrected 2026-10-16.** The rule above is right;
the reason usually given for it is not. `tokens.ts:63` sets `BRAND_FONTS.serif` to
`var(--font-instrument-serif), ui-serif, Georgia, "Times New Roman", Times, serif`, and the generator
writes that into `--font-serif` (`theme.generated.css:16`). So `--font-serif` is not a
self-reference — it *leads with* the right variable and drags an OS-dependent generic chain behind
it. That tail **is** drift mechanism 2, which is why the ruling exists. `layout.tsx:68-70` reaches
the same conclusion from the wrong reason; the conclusion is what this table keeps.
`SOURCE-TRUTH.md` C4.
| **Bw Gradual** | **Logo mark only — not a web font.** The wordmark is SVG vector paths | Ships in `brand/fonts/` | `brand/DESIGN.md:81` |
| **Geist Sans** | **RETIRED 2026-09-22.** Lives in `brand/fonts/retired/` | — | `brand/DESIGN.md:83-84` |

**Two traps this table exists to prevent.** `brand/fonts/` sits next to `brand/logos/` and invites
a wholesale copy — but it holds Bw Gradual (must never load) and `retired/GeistSans-VF.woff2`
(reintroducing it reverses a locked ruling). `PLAN.md:233` says *"copy the logos"*; read literally
that is correct, and this table makes the reason explicit so nobody "helpfully" adds fonts.

**Instrument Serif is not a file in the cupboard.** It arrives via `next/font`. Any harvest step
looking for a `.woff2` will not find one, and must not conclude the face is missing.

### 6.2 Label roles — preserve, do not reinvent (`brand/DESIGN.md:150-151`)

| Class | Size | Weight | Tracking | Face | Used for |
|---|---|---|---|---|---|
| `.label-eyebrow` | 11px | 300 | 0.2em | sans | section labels, eyebrows — the workhorse |
| `.label-action` | 11px | 500 | 0.2em | sans | caps that are clicked, and gold status |
| `.label-spec` | 10px | **400** | 0.2em | **mono** | card titles, spec strips, cap table |
| `.label-badge` | 10px | 500 | **0.05em** | sans | status pills and highlight tags |

**Four roles, not two — and the second one was missing from this table until 2026-10-16.**
`.label-spec` is live and in active use (`cap-table-card.tsx:27`, `data-room-card.tsx:15`,
`horses/[slug]/about/page.tsx:99`). STEP1 and STEP3 both recorded it; this table did not.

**And `.label-badge` is not a class in the build — corrected 2026-10-16.** A repo-wide grep returns
zero occurrences. The live fourth label class is `.label-mono-intro`
(`theme.generated.css:164-167`), declared with zero consumers — which is `DEFECT-HISTORY` #22, and
which this table already records two paragraphs below. The **tracking value** `0.05em` *is* live, as
Tailwind's `tracking-wider` on the highlight tags (`STEP2:46`), and `STEP2:155` proposes naming it
`--tracking-tag`. So the fourth *role* may well be the right decision — a badge/status pill needs one
— but it is a **decision to make**, not a class to read off the build, and it must not be described
as live. The theme's own comment is stale in the same direction: `theme.generated.css:120` says
"three roles" above four declarations. `SOURCE-TRUTH.md` C5.

**The nav is not an eyebrow role.** This table used to say the eyebrow's job was "section labels,
eyebrows, **nav**". That came from the bridge spec's prose, not from the build. Live nav links are
`text-[12px] font-[300] tracking-[0.15em]` (`NavBar.tsx:193`) — a 12px size that is not a type role,
an inline arbitrary weight, and a **fourth tracking step**. The nav's link treatment is its own
decision and is recorded in `COMPONENTS.md` §4.

**And the tracking count is the thing that keeps drifting.** Four steps are live: `0.2em` (eyebrow,
action, spec), `0.15em` (nav), `0.05em` (tags and pills), `-0.04em` (the display heading). STEP2
already proposed `--tracking-tag` for the `0.05em` step and `--tracking-display` for `-0.04em`;
those names are owed, not invented. `DEFECT-HISTORY` #20 found the split on one button type alone.

`DEFECT-HISTORY` #22 dropped `--label-mono-intro` — zero consumers. It is not a role.

### 6.3 Colour — the locked set

**Verified 2026-10-16 by measurement.** Every text token clears WCAG AA (4.5:1) on **both** the
canvas and the card surface; every structural token clears 3:1. Ratios below are canvas / surface.

**Surfaces**

| Token | Value | Role |
|---|---|---|
| `--color-canvas` | `#030303` | page |
| `--color-surface` | `#0a0a0a` | card |
| `--color-raised` | `#111111` | elevated / hover / inset |

**Structure**

| Token | Value | Ratios | Rule |
|---|---|---|---|
| `--color-border` | `rgba(255,255,255,0.1)` | — | Translucent. Works over any surface — never replace with an opaque grey |
| `--color-edge` | `#9a9aa0` | 7.37 / 7.07 | Control floor, secondary metadata, **and the one focus ring** (`COMPONENTS.md` §3.5) |
| `--color-disabled` | `#62666d` — **`departs`**; no live declaration | 3.58 / 3.43 | **Non-text only** — disabled borders and inactive structure. Never text. Corrected 2026-10-16: this value has **no source** in the theme, the app or the bridge. It is a proposal, and it needs either a declaration or the argued line §5 requires. `SOURCE-TRUTH.md` C2 |

**Text**

| Token | Value | Ratios | Rule |
|---|---|---|---|
| `--color-heading` | `#f8fafc` | 19.71 / 18.92 | Headings, hero |
| `--color-ink` | `rgba(255,255,255,0.5)` | 5.29 / 5.33 | **Body copy.** Composites to ≈`#818181`. Translucent so it adapts to the surface beneath it |
| `--color-hover` | `#b9b3a9` | 9.90 / 9.51 | Warm hover tone. Hover only — never a surface, never a border |
| `--color-muted-foreground` | `#7c7c7c` | 4.94 / 4.74 | Secondary metadata, timestamps, helper text. Static |
| `--color-foreground` | `= var(--color-ink)` | — | shadcn compatibility mapping, one direction. Do not delete |

**Accents**

| Token | Value | Ratios | Rule |
|---|---|---|---|
| `--color-gold` | `#d4a964` | 9.49 / 9.11 | **The sole brand accent. 3–5% of the viewport. Never a surface. Never called `accent`.** |
| `--color-gold-hover` | `#c39853` | 7.79 / 7.48 | Hover only |
| `--color-on-gold` / `--color-on-light` | `#0a0a0a` | 9.11 on gold | Dark text for any gold or light fill. **White on gold is 2.17:1 and fails** |
| `--color-spot-mint` | `#00e599` | 12.44 / 11.94 | One display word per page |

**Status — semantic only, never adjacent to mint**

| Token | Value | Ratios | Role |
|---|---|---|---|
| `--color-status-active` | `#10b981` | 8.13 / 7.80 | Active, verified, live availability, positive returns |
| `--color-status-pending` | `#f59e0b` | 9.60 / 9.22 | **`fully_subscribed`**, labelled FULLY ALLOCATED — sold out, waitlist. Read as *demand still standing*, not as closure. `pending` is not a status name; `coming_soon` is green |
| `--color-status-closed` | `#738396` — **`departs`**; live is `#64748b` | 5.32 / 5.11 | Terminal — **completed**. Neutral slate. **The departure is the fix:** live `#64748b` measures ≈4.33:1 on canvas and fails AA, while `#738396` clears at 5.32. Corrected 2026-10-16 — this row was presented as a measurement and it is a proposal. `SOURCE-TRUTH.md` C1 |
| `--color-destructive` | `#ef4444` | 5.48 / 5.26 | Error, cancelled, declined |

**Legal document surface** — the white PDS/SA read inside the dark flow, scoped to `.legal-doc`

| Token | Value | Ratio | Note |
|---|---|---|---|
| `--color-legal-surface` | `#ffffff` | — | |
| `--color-legal-ink` | `#111111` | 18.88 | |
| `--color-legal-surface-alt` | `#f5f5f5` | — | Table headers |
| `--color-legal-border` | `#dddddd` | 1.36 | **Deliberate** — a document hairline, not a control boundary. Do not "fix" it |
| `--color-legal-checkbox` | `#b98a2f` | 3.12 | Clears the 3:1 control floor |

**Seven opaque neutrals are live** (canvas, surface, raised, heading, edge, muted, hover) plus two
translucent whites (`border`, `ink`). That is the greyscale, counted by job rather than by ramp.
**This said eight until 2026-10-16**, counting `disabled` — which is not declared anywhere live
(`SOURCE-TRUTH.md` C2).

**Retired — do not use:** `ash #575757`, `smoke #454545` (fail contrast — 2.85:1 and 2.15:1),
`hairline #050505`, `stage-black #000000` (zero call sites). The bridge theme still declares all
four; they do not survive into V2.

**The 24 are not the whole of what is live.** `theme.generated.css` also declares the following, and
none of it is in the locked set above. Recorded 2026-10-16 because the next reader will meet it:

- **Two purple tokens with live call sites.** `--color-stripe-purple: #635BFF` and
  `--color-stripe-purple-light: #8884FF` (`theme.generated.css:42-43`), used four times in
  `purchase-flow-modal.tsx` for the *Powered by Stripe Identity* badge. The bridge spec claims
  "there are no purple tokens in this system" and that the Stripe mark is self-contained. That is a
  proposal, not a description — the live build does the opposite. **The Stripe attribution still
  needs a V2 ruling**; it cannot be waved off as absent.
- **A 16-token shadcn compatibility block** (`:99-114`): `background`, `card`, `card-foreground`,
  `popover`, `popover-foreground`, `primary`, `primary-foreground`, `secondary`,
  `secondary-foreground`, `accent`, `accent-foreground`, `muted`, `destructive-foreground`,
  `input`, `ring`. Every one is an alias onto a real token, so none is a new colour — but
  `--color-accent` → gold is **used 127 times in the app**, while §6.3's own rule says the accent
  is "never called `accent`". The prohibition is not enforceable against the live build as
  written; it needs restating as a rule about *new* names, or dropping.
- **`text-muted` is a landmine, and it is live.** The shadcn block maps `--color-muted` →
  `--color-raised` = **`#111111`**, so `text-muted` — which reads as "muted text" in every Tailwind
  habit — actually renders *near-black text on a near-black canvas*. `packages/ui/src/stat-row.tsx`
  carries a comment warning about exactly this. The token is correct as a **surface**; only its name
  is a trap. Anything wanting dim text wants `muted-foreground`.
- **A stale secondary value to catch:** `stat-row.tsx`'s comment cites `muted-foreground` as
  `#737373`. The theme and this document both say `#7c7c7c`. The comment is wrong; the token is right.
- **Four more type roles** than §6.4 lists: `--text-label` 11px, `--text-body-small` 15px,
  `--text-body` 16px, `--text-card-heading` 18px. §6.4's "seven roles" is right — it just is not the
  seven in its own table, which lists a `display 64px` role that **is not a token at all**:
  `--text-display` appears nowhere, and 64px lives as a hand-typed `md:text-[64px]` copied into
  `marketplace/page.tsx:67` and `marketplace/[slug]/page.tsx:116`. Two pages, one recipe, typed
  twice. That is drift mechanism #6 happening in the file §6.4 was harvested from.
- **`--color-on-light` is not declared anywhere.** Live has `--color-on-gold` (`#0a0a0a`,
  `theme.generated.css:40`); `--color-on-light` is a **bridge proposal**
  (`V2-THEME-2026-10-16.css:50`). This one has teeth: `DEFECT-HISTORY` #4's resolution, §6.3's own
  row below, `COMPONENTS.md` §9 do-not 3 and `SECTION10-DO-DONT.md` §10.1 all tell the builder to use
  `text-on-light`. Either it is created as an alias of `on-gold`, or those four rules name
  `--color-on-gold`. `SOURCE-TRUTH.md` C3.
- **A second live palette, parked.** `globals.css:58` opens `[data-theme="light"]` — a light console
  overriding the house tokens (canvas `#f7f7f5`, gold `#a87c2a`, and a dormant `--color-light-*`
  family beside it). No live route sets it (`globals.css:49`; the design lab demos it), so excluding
  it from the locked set is right — but its neighbours are recorded here and it was not. It also
  carries its own **documented contrast gap** at `globals.css:53-57`: `--color-edge` is not
  overridden and measures 2.80:1 on the light canvas. `SOURCE-TRUTH.md` §The light scope.

**Three notes for whoever reads this next.**

1. **`ink` and `muted-foreground` are ~5 RGB units apart.** The distinction is mechanical and
   semantic, not visual — `ink` is translucent and adapts, `muted` is static. Do not expect a
   visible hierarchy step between body copy and secondary metadata, and do not push them apart to
   manufacture one.
2. **`status-closed` is a slate, not a true neutral** — it measures B−R **+35**. The name is
   "neutral slate". Do not neutralise it: blue is what the original defect looked like, and the
   value was chosen to pass AA while staying in the terminal family.
3. **These values are the website palette.** The estate also carries a comms/wireframe family
   (`--ink #eceae6`, `--ink-soft #9c9a96`, `--ink-faint #6a6865`, green `#5fca8f`, gold
   `#c49a5a`) that lives in `comms/automated-comms/` and `website/docs/wire/`. It is a different
   medium. It has tried to cross into this set four times — see §16.

### 6.4 Type

Seven fixed roles, `micro 10px → section-heading-wide 48px`. `--text-micro` (10px) is **not
reserved** — it is in active use (pedigree, cap table, right rail, MyStable). 36px and 48px are
**one role at two breakpoints**, not a display/heading pair.

| Token | Size | Use |
|---|---|---|
| `--text-micro` | 10px | tags, meta, pedigree, cap table |
| `--text-label` | 11px | the label roles — §6.2 |
| `--text-body-small` | 15px | dense body — card hooks, helper text |
| `--text-body` | 16px | default body |
| `--text-card-heading` | 18px | card and panel headings |
| `--text-section-heading` | 36px | section h2, base breakpoint |
| `--text-section-heading-wide` | 48px | same role, `md:` |

**The 64px page heading is a role without a token.** `--text-display` does not exist. 64px is
hand-typed as `md:text-[64px]` into `marketplace/page.tsx:67` and `marketplace/[slug]/page.tsx:116`
— one recipe, two files, typed twice. Weight 300, tracking `-0.04em`, leading 1.05. It needs a name
before it is written down; the two copies are drift mechanism #6 in the file this section was
harvested from.

**Three weights, and one of them is not a choice — it is a live value this section did not know
about.** `300` body and headings · `500` clicked caps, the hero tagline · **`400` the
`.label-spec` role**, which is live in `cap-table-card.tsx`, `data-room-card.tsx` and the horse
about page. "300 and 500 only" was wrong for as long as `.label-spec` has existed. `DEFECT-HISTORY`
#18 maps `font-semibold` (600) to 500 and says nothing about 400, because it was looking at MyStable
financials rather than at the label roles.

So the rule is **300 / 400 / 500** — **ruled 2026-10-16**: the scale admits 400 rather than moving
`.label-spec`, because `label-spec` is mono, 10px and in active use, and pulling it to 300 or 500
would break the one role that carries spec labels on cap tables and data rooms. `600` maps to 500
(`DEFECT-HISTORY` #18).

### 6.5 Shape, depth, motion

| Token | Value | Source |
|---|---|---|
| `--radius-sm` | `8px` | inputs, steppers, image frames |
| `--radius-md` | `16px` | inner cards, accordion panels |
| `--radius-lg` | `24px` | outer cards, rail, modals |
| `--radius-xl` / `--radius-2xl` / `--radius-3xl` | `24px` **each** | **Aliases onto `lg`**, declared in the theme. This is why `rounded-2xl` and `rounded-3xl` render 24px and not Tailwind's 16px/24px defaults |
| `--radius-pill` | `9999px` | pills, badges, status dots |
| `--radius-xs` | **does not exist** | `rounded-xs` falls through to Tailwind's own ~2px. The bridge spec's checkbox uses it; nothing in the theme backs it |
| border opacities | three steps: `/20`, `/40`, `/60` | `DEFECT-HISTORY` #16 |
| `--shadow-card-hover` | `0 20px 40px rgba(0,0,0,0.45)` | listing card, on hover |

**Elevation — ruled 2026-10-16, decision 5 closed.** Four elevation, one bevel, two glow. Derived
from the live literals by `AUDIT-MISSING-PRIMITIVES` §5.2 — *not* copied from the bridge, which
proposes the same set; the two agree because both read the same 14 distinct values.

| Token | Value | Use |
|---|---|---|
| `--shadow-panel` | `0 0 60px rgba(0,0,0,0.6)` | rail card, modal shell |
| `--shadow-modal` | `0 0 120px rgba(0,0,0,0.98)` | dialog shells — all three |
| `--shadow-float` | `0 30px 80px rgba(0,0,0,0.6)` | auth card, rail error card |
| `--shadow-card-hover` | `0 20px 40px rgba(0,0,0,0.45)` | listing card, on hover |
| `--shadow-bevel` | `inset 0 1px 0 rgba(255,255,255,0.05)` | top highlight — **composes**, never concatenated |
| `--shadow-glow-success` | `0 0 8px rgba(16,185,129,0.6)` | the status dot, and nothing else |
| `--shadow-glow-gold` | `0 0 12px rgba(212,169,100,0.25)` | selected pedigree node |

**The bevel is a separate concern from depth.** Two live values concatenate a depth shadow and a
highlight into one string, which is why they could not be tokenised as-is. They are written
`shadow-[var(--shadow-panel),var(--shadow-bevel)]` and never as one hand-written value.

**Two live glows these seven do not account for — found 2026-10-16, recorded not ruled.**
`pedigree-tab.tsx:275` runs `0 0 20px rgba(212,169,100,0.3)` on a selected node, a second gold value
beside the locked 12px/0.25 on the same component; `pedigree-table.tsx` runs
`0 0 18px rgba(16,185,129,0.12)`, a third emerald. If the seven tokens are the whole vocabulary —
which adjudication 3 below says they are — both are dropped like the blue glow. Neither is currently
named, and `DEFECT-HISTORY` #15's "14 distinct values" does not include them. `SOURCE-TRUTH.md` §5.

**Three adjudications, so they are not re-opened:**

1. **One success glow, not two.** Live carries `--shadow-success-glow` at `20px/0.35` *and*
   `-strong` at `32px/0.55`, while three inline literals use `8px/0.6`. `DEFECT-HISTORY` #21 already
   folds the strong variant in. The survivor is the **8px** one, and the checkout banner — currently
   the `20px` token's only consumer — **drops its glow entirely** and takes `--shadow-panel`. Its
   green is already carried by `border-status-active/40` and `bg-status-active/10`; the bloom was
   saying it twice. This is also what makes the glow single-purpose: it marks *motion*, per §2.6 of
   the badge rule. **Corrected 2026-10-16:** the "three inline literals use `8px/0.6`" does not
   reproduce — the build holds **one** 8px site (`marketplace-listing-grid.tsx:65`, an 8px blur
   carrying the *20px/0.35* token's colour) and two declared tokens, none at alpha `0.6`. The
   adjudication may still be right; it is an adjudication, not a derivation. `SOURCE-TRUTH.md` C7.
2. **The blue glow is dropped.** `0 0 8px rgba(96,165,250,0.6)` has one call site and introduces an
   info-blue that appears in none of the locked 24. §6.3 already rules there is no fourth status
   colour. The call site moves to `--shadow-glow-gold` or loses the glow.
3. **Tailwind's named shadows are banned, like bare `rounded`.** Eleven live uses with no token
   backing — `shadow-sm` ×5, `shadow-xl` ×3, `shadow-2xl` ×2, `shadow-md` ×1 — five of them on one
   orphan page. The elevation table above is the whole vocabulary, exactly as `DEFECT-HISTORY` #2
   made five tiers the whole radius vocabulary.

**One correction to the bridge's own table:** its §5.1 lists `--radius-xs: 4px` as a token. It is
not declared anywhere, which is the same phantom this README carried until 2026-10-16.
| `--spacing-section` | `224px` | `py-section`; six wrappers use `py-56` |
| container | `max-w-6xl` (1152px) | padding `px-12 md:px-16 lg:px-20` |
| touch target law | **44px** | `DEFECT-HISTORY` #5 |
| durations | hover `200ms` · collapse `300ms` · shimmer `2000ms` | STEP1 |

**CollapsePanel:** the STEP1 version is canonical — pure grid rows, no JS measurement. Exit
differentiates at 300ms/200ms, with a reduced-motion guard.

**But the live build ships two accordions**, against a rule that permits one:
`ui/CollapsePanel.tsx` and `ui/AccordionList.tsx`. Consolidated in `COMPONENTS.md` §12's owed list as
owed work, not yet locked. This is `DEFECT-HISTORY` #13's shape a second time — two implementations
of one job, which is how the badge problem started.

**The container is now universal, and horizontal only — ruled 2026-10-16 (decision 7).** Every page
surface sits inside `max-w-6xl`: `/`, `/marketplace`, `/marketplace/[slug]`, `/mystable` and any
nested route, with `px-12 md:px-16 lg:px-20` on every one. Dialogs are not pages and keep their own
caps. `COMPONENTS.md` §3.1 carries the six live schemes this replaces, and the corrected count — the
dashboard carries **one** `max-w-7xl`, not the four this document and §18 item 7 both claimed.

**Section rhythm, confirmed and ruled on 2026-10-16.** `--spacing-section: 224px` is declared in
`brand_dna/src/theme.generated.css:87` and is **fixed** — the live build has no fluid section rule
at any viewport, including mobile. The bridge's `clamp(5rem, 12vw, 14rem)` is therefore a proposal,
not a harvest, and it is **declined**: nothing in the audit has ever recorded a mobile defect, and
adopting a fix for an unmeasured problem is how the second palette got in. If V2 later wants a
fluid rhythm it is a deliberate improvement with a reason recorded, argued as such — not a
correction of a value we never measured wrong.

**And the rhythm is per surface type, not one rule — ruled 2026-10-16.** Marketing sections run
`py-section` (224px). Functional dashboard and application headers run `pt-32 pb-24` (128px / 96px),
which is what `/mystable` does today, and that asymmetry is intended rather than a drift. Do not
force the two into one value; they are different kinds of surface.

**Two things this leaves unsettled, named rather than buried.** `PressShowcaseSection.tsx:171` runs
`py-24` (96px) and **is** a marketing section, so under the rule above it needs changing rather than
exempting — this document called it an "honest exception" until 2026-10-16, and the ruling makes it
a defect. And `NavBar.tsx:159` still runs its own `max-w-[1440px] px-6 sm:px-10 lg:px-12`, which was
where the bridge's `px-6 sm:px-10 lg:px-16` gutter numbers came from; §3.1 retires it.

**One correction to what this paragraph used to say.** Until 2026-10-16 it read that the
`px-6 sm:px-10 lg:px-12` family "belongs to the nav bar… They are not a page container." **That is
false.** `marketplace/[slug]/page.tsx:134` is a page container using it — and it is one of the two
lines `DEFECT-HISTORY` #8 names as "two left edges on one page". The family has a page call site, the
defect it causes is live, and `COMPONENTS.md` §3.1 now retires it.

**The `py-56` count stands on its own.** Six section wrappers use `py-56` = 224px, which is where the
spacing token came from; that is a count of six, not of every section on the page.

---

## 7 · The bill of materials — readiness for play

**This is the readiness test.** Every section `DESIGN.md` must contain, whether we have it, and
where it comes from. When every line reads ✅, we write the document in one pass.

| # | `DESIGN.md` section | Ready | Where it comes from |
|---|---|---|---|
| 1 | Frontmatter tokens | ✅ | §6.3–6.5 — values locked |
| 2 | Overview / posture | ✅ | *"Dark, quiet, editorial."* Gold carries 3–5%, never a surface |
| 3 | Non-negotiables | ✅ | §6.1–6.2 — retired faces, the one serif word, the label roles |
| 4 | Colours | ✅ | §6.3 — 24 tokens, contrast-verified on canvas and surface, including the legal set |
| 5 | Typography | ✅ | §6.4 — seven roles, two weights |
| 6 | Shapes — radius & borders | ✅ | §6.5 — three radius **steps** (8 / 16 / 24) plus pill, with `xl`/`2xl`/`3xl` as aliases onto `lg`; 3 border opacities |
| 7 | Layout — spacing & container | ✅ | §6.5 — `224px` rhythm, `max-w-6xl`. **Confirmed against the live source 2026-10-16**: `brand_dna/src/theme.generated.css:87` declares `--spacing-section: 224px` — fixed, not a clamp — and every page section uses `px-12 md:px-16 lg:px-20`. The bridge's fluid values are declined, not missing. The container is ruled for the chrome and all page content (`COMPONENTS.md` §3.1); the dashboard's `max-w-7xl` is a separate open item — decision 7 |
| 8 | Elevation & Depth | ✅ | §6.5 — **ruled 2026-10-16**: 4 elevation + 1 bevel + 2 glow, derived from the live literals, with the two near-duplicate success glows folded and the one-off blue dropped. Bevel composes, never concatenates |
| 9 | Motion | ⚠️ partial | Durations locked (§6.5). Granularity open — Open decision 1 |
| 10 | Layout — breakpoints | ✅ | **Ruled 2026-10-16 — not tokenised.** Breakpoints stay out of the `@theme` set: page layouts and responsive behaviour differ legitimately per view, and forcing breakpoints into tokens manufactures constraints the pages do not share. Standard Tailwind prefixes (`sm:` / `md:` / `lg:`) apply, mobile-first, under one rule. The single exception already ruled is the *chrome* collapse point (`COMPONENTS.md` §8, 768px) — one value, because the nav, the drawer and the bar must agree with each other. `SPEC` originally excluded breakpoints too; the reference pattern's inclusion is declined |
| 11 | Components | ✅ | **9 components locked — Workstream C complete** (`COMPONENTS.md`). All six on the §8 list, plus the mobile conversion bar, the mobile menu drawer and the button hierarchy — three the six-item list never knew existed. Four consolidation jobs remain and none of them is a component |
| 12 | Do / Don't | ✅ | **Written 2026-10-16** — `SECTION10-DO-DONT.md`. `DEFECT-HISTORY`'s 24 defects collated into **21 rules**: 8 restated from the component locks, 11 from §6 (9 rules, after collating #21+#22 and folding #23 into #15), **4 written new** — #7, #11, #12, #17 — and 1 excluded as build hygiene (#24). Every rule is stated forward, carrying the drift that is its reason. Four corrections to `DEFECT-HISTORY` came out of the collation; see that file's §Corrections |
| 13 | Agent Prompt Guide | ⚠️ decided | **Decided 2026-10-16 — include it.** Decision 4 closed: the section ships, because a one-pass build is the whole point and a machine reader of `DESIGN.md` needs the no-debt and token rules stated for it rather than inferred. **Not written yet** — the section itself is owed, and it is the only reason this row is not ✅. Becomes **section 11** of `DESIGN.md`, since Provenance was cut from the skeleton |

**A row was removed from this table on 2026-10-16, and the tally below is recomputed from what
remains.** It carried *"Provenance — collated, `SOURCE-TRUTH.md`"*. Provenance is no longer a
`DESIGN.md` section (ruled 2026-10-16, §9), so it is not a line in a bill of materials scoped to *what
`DESIGN.md` must contain*. **The work is not lost and was not undone:** `SOURCE-TRUTH.md` remains the
forensic record of every locked value against its source (§17), and Workstream A remains complete
(§8). It moved from *a deliverable* to *the evidence behind one*.

**Reading it plainly:** eleven sections are ready, two are partial, none is not started.

---

## 8 · Coverage — the six workstreams

| # | Workstream | Produces | State |
|---|---|---|---|
| A | **Harvest** — read the real values off the live landing page | A ground-truth table: every colour, size, weight, tracking, radius, spacing, with provenance | ✅ **Complete — collated 2026-10-16** into `SOURCE-TRUTH.md`: seven categories, every value against its `file:line`, `adopted`/`departs` marked, and eight corrections filed |
| B | **Token model** — how those values compile | The `@theme` block, its categories, its naming | Values ready; naming conventions settled in Tailwind v4 terms |
| C | **Pattern locks** — the components | Decision-level specs for card, button, badge, nav, listing row, form field | ✅ **Complete — 9 components locked** in `COMPONENTS.md`: the whole chrome, the button hierarchy, the data and form primitives, and the mobile surfaces the old build never had. Four consolidation jobs remain, none a component |
| D | **Drift mechanisms** — why it went wrong before | A catalogue of causes, each with the guard that prevents it | Done — §10 |
| E | **Target `DESIGN.md`** | The document, in the pattern of §1 | ❌ Blocked on §7 |
| F | **Enforcement** — how it stays true | A gate check in the `assert-*.sh` style, plus the audit rubric hook | Designed — §11 |

### Workstream A · Harvest

**Seven categories:** colour · type roles · space · shape · depth · motion · interactive states.

**Provenance is mandatory.** Every value is recorded with the element and property it came from,
so it can be re-verified later. The live page is the source of truth and it will change — the
domain cutover is coming (`PLAN.md:107`), so the harvest is a **method**, recorded so values can be
re-checked, not a one-off copy-paste.

**The landing page's nine sections are kept** (decision 2, 2026-10-15). This is what retires the
*"6a's page structure is not specified"* note at `engine_v2/CONTINUE.md:26-29`:

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

### Workstream B · Token model

**The file:** `website/src/app/globals.css`. Currently 23 bytes — `@import 'tailwindcss';`.
Tailwind **4.3.3**, Next **15.5.27**.

**The mechanism, and the trap.** Tailwind v4 maps *namespaced* custom properties to utilities:
`--color-*` → colour, `--font-*` → font-family, `--text-*` → font-size, `--spacing-*`, `--radius-*`,
`--shadow-*`, `--ease-*`, `--breakpoint-*`. **A custom property outside a known namespace
generates no utility at all** — it exists as a variable and nothing can use it. The naming
convention is therefore not cosmetic. Decide it once and freeze it.

**Tokenise:** colour · type roles (family + size + weight + tracking + leading as one name) · space
rhythm · radii and border widths · interactive states.

**Deliberately NOT tokenised:** **layout and grids** — page arrangements differ legitimately, and
a token only one page can use is not a token, it is a hard-coded value wearing a costume. Also not
tokenised: content and copy.

**The guardrails, stated plainly.** Lock **decisions, not markup** — a spec that pins exact JSX
rots the first time React or Tailwind shifts, people route around it, and routing around it is how
the drift started. And **over-tokenising is its own drift source**: a 200-token system nobody can
hold in their head gets ignored, and an ignored system is a dead one.

### Workstream C · Pattern locks

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

1. **Listing card** — the marketplace unit. Highest drift exposure. ✅ *Locked* — `COMPONENTS.md` §1
2. **Status badge** — the four statuses are already a database enum; the badge must not invent a
   fifth look. ✅ *Decided 2026-10-16:* one component, one map, three treatments — green + glow
   (`listed`, `coming_soon`); **amber, no glow** (`fully_subscribed`); slate, no glow
   (`completed`). Locked in full at `COMPONENTS.md` §2.

   This reverses the muted-grey treatment the old build gave the sold-out state, and it supersedes
   `STEP2-MARKETPLACE.md:50-55` — **on the colour only.** STEP2's *names* were right all along; the
   audit's own were the wrong ones. That answers the two questions STEP2 left open at `:146` and
   `:148`, and it moves §6.3 and this list onto the same answer — they disagreed for one commit,
   and amber is the side that won.

   **The status vocabulary, read off the code 2026-10-16.** `database.types.ts:71` declares the
   Postgres type `CampaignStatus` with **six** values: `draft`, `coming_soon`,
   `coming_soon_details`, `listed`, `fully_subscribed`, `completed`. `ListingStatus`
   (`asset-lock.ts:45`) is the public subset of four — `listed`, `coming_soon`,
   `fully_subscribed`, `completed`.

   That kills a name this audit has been using. **`available` and `fully_allocated` do not exist**
   — not in the enum, not in the app, anywhere. `PLAN.md:206` and `FORENSIC-AUDIT.md:97` both record
   the enum as `(coming_soon, available, fully_allocated, completed)`: wrong on two of four names,
   and missing two states. The amber ruling above stands, but it applies to **`fully_subscribed`**
   — the *value* is `fully_subscribed` and the *label* is **FULLY ALLOCATED**; they are not
   interchangeable.

   `coming_soon_details` is the sixth state and it is **absent from every map we hold** — PLAN.md,
   this section, and the bridge's §2.6 alike, which only alludes to "its internal term-sheet
   variant". Its label and treatment need a ruling.

   §5 makes `PLAN.md` the authority on *scope*, never on values. `918e197` treated it as both and
   wrote `draft` off as "not a status" — it is one. Read the schema, not the plan, for values.
3. **Button hierarchy** — primary, secondary, and the disabled/loading forms of each.
   ✅ *Locked* — `COMPONENTS.md` §9. Two variants, solid and ghost; **the primary CTA is white, not
   gold**, because §6.3 rules gold never a surface.
4. **Figure row** — the mono-figures pattern. `brand/DESIGN.md:79` puts Geist Mono on financials and
   tabular figures specifically, so this is a token decision, not a styling choice.
   ✅ *Locked* — `COMPONENTS.md` §10. Live renders the value in the **sans stack at 300**; ruled to
   mono at 500, because §5 makes `brand/DESIGN.md` the authority on rulings.
5. **Nav and footer** — shared across every page, so the first place a per-page variant appears.
   ✅ *Locked* — `COMPONENTS.md` §4, §5. Neither had a spec anywhere in the estate, so both were
   ruled from source.
6. **Form field** — buyer and operator inputs share a look; the error state is the drift risk.
   ✅ *Locked* — `COMPONENTS.md` §11. `field.tsx`'s header asks for one spelling and ships two.

**Two components were not on this list and are now locked**, both from the 38-item inventory rather
than the six: the **mobile conversion bar** (`COMPONENTS.md` §6, which the old build never had —
`DEFECT-HISTORY` #6) and the **mobile menu drawer** (§7, pulled out of the nav because a focus trap,
an Esc handler and a scroll lock are a component's worth of work).

**And one shared ruling cut across three of them:** there were three different focus rings in the
live build. One now — §3.5.

**The "closed list" rule is the whole mechanism.** The drift was not one wrong colour; it was a
second and third variant of the same thing. A variant list closed by default means adding one
requires a ruling — a conversation instead of an accident.

---

## 9 · The target `DESIGN.md`

The skeleton, in the fixed pattern of §1. Sections 3, 9 and 13 are ours — neither reference has
them, and they are the three that do the most work here.

```
---  YAML frontmatter: colors · typography · rounded · spacing · components
1    Overview            posture, and "Key Characteristics"
2    Colours             Brand & Accent · Surface · Text · Semantic
3    Non-negotiables     retired faces, the one serif word, the label roles
4    Typography          families · hierarchy table · principles · substitutes
5    Layout              spacing scale · container · breakpoints · touch targets
6    Elevation & Depth   table: Level | Treatment | Use
7    Shapes              radius scale · border opacity steps
8    Components          buttons · cards · inputs · nav · footer · drawer · mobile bar · badge · listing card
9    Motion              durations, easings, and what is allowed to move
10   Do / Don't          the anti-patterns, each naming the drift it caused
11   Agent Prompt Guide  explicit instructions for machine readers   (open decision 4)
```

**Provenance is deliberately not a section — ruled 2026-10-16.** The skeleton carried an 11th section,
*"Provenance — value → source element, so it can be re-verified"*. It is **cut**. `DESIGN.md` is a
forward-looking specification consumed by builders and agents; a table of `file:line` is forensic
reference, and neither reader can act on it. The evidence lives where it is useful — `SOURCE-TRUTH.md`,
in this folder (§17), which is what makes the locked values re-verifiable after the cutover. **Nothing
is lost:** §11's third check compares `DESIGN.md` against `globals.css` by *value*, not by citation, so
the check that makes the doc-first flip safe is unaffected. And §10's drift narratives stay — they are
the reason a rule exists, not a citation to go and read.

**A second consequence, applied rather than noted.** The same principle governs §10's citations: it
restates each rule and previously added `(COMPONENTS.md §9)`-style references. Those point at files
that do not leave this folder (§13, §17), so they dangle for the reader who holds only `DESIGN.md` and
has been stripped from the shippable content. **The drift stays; the audit-folder citation goes.**

**One number here does not resolve.** The sentence below used to read *"Sections 3, 9 and 13 are
ours"*. There is no section 13 in a twelve-section skeleton, and there is now no section 11 either.
Section 3 (Non-negotiables) and section 9 (Motion) are ours in the sense meant; the third is
unidentified and needs a reader who has the two reference documents.

---

## 10 · Drift mechanisms

The estate's own history, catalogued so the spec prevents **causes**, not symptoms.

| # | Mechanism | Documented evidence | Guard that prevents it |
|---|---|---|---|
| 1 | **Utility class over inheritance** — a face applied per-file while the parent sets another | `brand/DESIGN.md:83-84`: Geist Sans reached four route files via `font-sans` while `body` inherited the system stack | `body` owns the face. A component may only name a **role**, never a family |
| 2 | **Unpinned generic fallback** — a raw generic resolving differently per OS | `brand/DESIGN.md:80`: `font-serif` rendered Georgia on macOS, Times New Roman on Windows, Noto Serif on Android — one page, three faces | Never use a raw generic. Only named role tokens |
| 3 | **Ad-hoc colour** — a hex literal written at the point of use | The reported drift across marketplace, horse page, MyStable | No hex literal outside `globals.css`. Mechanical, via Workstream F |
| 4 | **Per-page palette invention** | `PLAN.md:153` forbids it; `PLAN.md:245` repeats it for 6b | Make the prohibition mechanical rather than remembered |
| 5 | **Component re-invention** — the same component built twice | `DEFECT-HISTORY` #13: two badge implementations of one enum | Workstream C, closed variant list |
| 6 | **Hand-typed label styling** — repeating an 11px/0.2em recipe per page | `brand/DESIGN.md:150-151` had them as *classes*, meaning they were applied by hand | Label roles become tokens, so the recipe exists once |

**Two lessons this table encodes.** Every one of these is a *value written at the point of use*
instead of *a name referring to a decision*. And every one survived because the system was
documented but not **checked**.

---

## 11 · Workstream F — enforcement

**The mechanism already exists in the build repo.** `scripts/assert-no-anti-patterns.sh` scans for
the ten banned tokens and fails the gate; `scripts/assert-operations-doc.sh` asserts another
invariant. The root `pnpm test` chains both, and `pnpm verify` runs
typecheck → lint → test → build.

**Proposed checks, in the same style:**

1. **No raw colour outside `globals.css`** in `website/` — **both spellings**: a hex or `rgb()`/`oklch()`
   literal, *and* a raw Tailwind palette utility (`text-purple-400`, `bg-zinc-900/60`, `border-blue-400/40`).
   Catches mechanism 3. **Widened 2026-10-16** — the literal-only wording was proposed first and it
   misses the defect it was written for: `DEFECT-HISTORY` #17 is `text-purple-400`, a palette class
   with no literal in it, and the widened check is what catches it. Live is full of both spellings.
2. **No raw generic font utility** (`font-sans`, `font-serif`) and no `font-family` declaration
   outside `globals.css`. Catches mechanisms 1 and 2.
3. **`DESIGN.md` values match `globals.css`.** Catches the two-sources-of-truth failure — the
   check that makes the doc-first flip in §1 safe.

**Scope: code and configuration only.** Prose in `engine/OPERATIONS.md` is exempt, per the existing
ruling.

**Plus the audit hook.** Each remaining build step goes through the gemma4:31b rubric. A
design-token item belongs in that rubric from 6a onward, so a step that invents a colour fails its
audit rather than passing it.

**Strength: fail, not warn.** Warn is how the last drift survived. *(Open decision 3.)*

---

## 12 · Non-goals

- Not a redesign. `PLAN.md:150` makes the landing page the north star; its look is kept.
- Not a component library with its own conventions and ceremony.
- Not a change to any page. This audit writes documents; the build consumes them.
- Not a V1 migration. Nothing from `@evo/ui`, the old token package, or the generator is carried
  over.
- Not in `engine/`. Scope is the system the website consumes.

---

## 13 · Where the outputs go

| Artifact | Home | Note |
|---|---|---|
| The V2 `DESIGN.md` | `evolution/engine_v2/website/website/DESIGN.md` | Authored here, lands in the build repo next to the app it describes. `PLAN.md:203` bans `CLAUDE.md` and `AGENTS.md` there — `DESIGN.md` is not on that list |
| The `@theme` block | `evolution/engine_v2/website/website/src/app/globals.css` | `PLAN.md:235`. Compiled from `DESIGN.md` |
| The enforcement check | `evolution/engine_v2/website/scripts/` | Chained in the root `pnpm test` |

The **only** artifacts that leave this folder are the finished `DESIGN.md`, the `@theme` block it
compiles to, and the check.

---

## 14 · Sequencing

```
A  → harvest collated into SOURCE-TRUTH.md        [read-only, blocks nothing]
C  → pattern locks written                        [the largest remaining gap]
D  → drift mechanisms catalogued                 [done — §10]
B  → token model decided, naming frozen
E  → DESIGN.md written, one pass, citing the values
F  → gate check written and chained
   → then the PLAN.md amendment, pointing v2 at the result
   → 6a becomes: consume the locked system, build the landing page
   → 6b, then 7, 8, 9 — already bound by PLAN.md:155 and :245
```

**The amendment comes last, not first** — §4.

---

## 15 · Acceptance criteria

- `SOURCE-TRUTH.md` records every value with provenance, and nothing is inferred. **Not yet met —
  corrected 2026-10-16.** The ledger is complete and every row carries a `file:line`, but it records
  **two rows that fail this criterion rather than passing it**: `--color-disabled` has no source
  anywhere, and `--color-status-closed`'s locked value is a proposal (`SOURCE-TRUTH.md` C1, C2). The
  criterion is met when those two either get a declaration or lose their place in the locked set.
  A further two rows, C3 and C5, are filed as §18 items 10 and 11 for the same reason.
- Every token sits in a Tailwind v4 namespace, so each generates a utility.
- No hex literal exists outside `globals.css` anywhere in `website/`.
- `DESIGN.md` describes no V1 artifact, and reintroduces none of the ten banned tokens.
- Every component in Workstream C has a closed variant list and a named do-not.
- The gate fails when a new colour or a raw generic font utility is introduced — demonstrated by
  actually introducing one and watching it fail, not by asserting that it would.
- `pnpm verify` passes with the new check chained in.

---

## 16 · Constraints on this folder

- **Sandbox island law holds** (`sandbox/AGENTS.md`): no external imports from `evolution/`, own
  venv, and `just check` stays 10/10. Markdown does not affect it.
- **Markdown only.** No venv, no dependencies, no scripts.
- **Never reintroduce a banned legacy token** — §3.
- **Do not import the comms/wireframe palette.** The estate carries a second colour family in
  `comms/automated-comms/` and `website/docs/wire/`. It has been proposed for adoption four times
  (`#eceae6`, `#5fca8f`, `#c49a5a`, `#6a6865`). It is a different medium. Values may be *considered*
  but must be re-derived in the website family, never copied across.
- **Do not call the output a lookbook.** `PLAN.md:150,275` ban the word. This produces an audit and
  a `DESIGN.md`.

### Keeping the runsheet true

`README.md` is the runsheet — §7's readiness table is the bill of materials. `COMPONENTS.md` is the
component ledger. Three constraints keep them honest, and they are stated so they can be **checked
in one command**, because a rule that lives in prose is a remembered rule:

- **A decision and its record ride the same commit.** Any commit that changes a decision, a
  readiness row, or a component lock updates these files in *that* commit — not a later one, and not
  only when someone remembers to. A commit that changes no decision needs no update; "every commit
  touches the README" is how a rule becomes noise and then becomes ignored.
- **Derived sentences are recomputed, never carried forward.** Count §7's table and write the
  sentence from the count. Both were wrong at once already: the summary claimed five of fourteen
  when the table showed seven, and Components was "two of six" with six locked. The failure is the
  document disagreeing with *itself*, which no push rule would have caught.
- **Push at a checkpoint; do not batch.** Six commits sat unpushed through 2026-10-16 while this
  repo was being read on GitHub. Committing is local; a runsheet nobody can read is not a runsheet.

**Why these are three rules and not one.** The proposal that prompted them was "every push updates
the README", which conflates two separate axes — record currency, which belongs to the commit, and
push cadence, which belongs to the checkpoint. It would also have missed every staleness found on
2026-10-16, because all of it was *internal*: a summary contradicting its own table, and a component
list contradicting a correction ten lines below it.

Whether this ever becomes mechanical rather than remembered is Workstream F's question — §11's
checks run in the build repo, and this folder is markdown-only. Until then it is the one rule in this
document kept by discipline, and it should be read that way.

---

## 17 · The evidence files

| File | What it holds |
|---|---|
| `STEP1-LANDING-PAGE.md` | Landing page harvest. **Closed, clean** — spacing rhythm and container width re-verified against the live source 2026-10-16 (§6.5, decision 6). Colours, 7 type roles, 2 label roles, radius scale, motion |
| `STEP2-MARKETPLACE.md` | Marketplace audit. **Closed.** Listing card anatomy, display heading, card hover shadow, tag tracking, container width. Its **badge treatment is superseded** — `:50-55` is the old-build map, and its open questions at `:146`/`:148` were answered 2026-10-16 (§8) |
| `STEP3-MYSTABLE.md` | MyStable audit. **Closed.** Financial figures (mono, 500), the purple purge, dashboard heading, container width |
| `COMPONENTS.md` | **Workstream C.** The decision-level locks — **complete at 9 components**, plus the shared rulings: the single container, the z-ladder, the touch law, hover guards, one focus ring. A working file; it does not leave this folder |
| `SECTION10-DO-DONT.md` | **The target `DESIGN.md` section 10** (§7 row 12), closed 2026-10-16. 24 defects collated into 21 rules, plus the collation table and four corrections to `DEFECT-HISTORY`. A working file; it does not leave this folder |
| `SOURCE-TRUTH.md` | **The forensic record behind `DESIGN.md` §2 and §7** — not a `DESIGN.md` section itself, ruled 2026-10-16 (§9). Every value §6 locks against the element, property and `file:line` it came from, in §8's seven categories, plus eight corrections to §6 and the parked light scope. Kept so the harvest is re-runnable after the domain cutover. A working file; it does not leave this folder |
| `DEFECT-HISTORY-2026-10-16.md` | The old build's 24 defects, each with the ruling that closed it. The source for §7 row 12 — `Do/Don't` is a collation of this file, not new work. Lives in the bridge folder |
| `AUDIT-MISSING-PRIMITIVES-2026-10-16.md` | Texture utilities, keyframes, dead classes, raw hex, and **21 arbitrary shadows across 14 distinct values**. The material for §7 row 8 (Elevation) and §18 decision 5. Uncited until now. Lives in the bridge folder |

Read-only source material. The findings are cited above; these files hold the full detail and the
file:line provenance behind each value.

**Careful with the last two, and with the bridge spec.** Everything in
`/home/evo/audit/website/` — including `V2-DESIGN-SPEC-2026-10-16.md` and
`V2-THEME-2026-10-16.css`, which §7 row 8 calls "the archive" — sits **outside version control**:
that path is not a git repository. §5 keeps it reference-only and mined decision-by-decision, which
is exactly why it needs watching: a value copied from there is a value with no commit behind it.

**One cross-reference to correct.** `DEFECT-HISTORY:11` points the rulings at
`sandbox/audit/design/DESIGN.md`, and `:46-48` puts them at "`DESIGN.md` §§5–8". Neither is where
this audit is going: §13 lands the document at `evolution/engine_v2/website/website/DESIGN.md`, and
the skeleton in §9 has Components at 8, Motion at 9 and Do/Don't at 10. The file is right that the
rulings live with us and the defects live there; only the path is stale. Nothing to fix over there
— the bridge is read-only — but do not go looking for a `DESIGN.md` in this folder. There isn't one
yet, and the moment there is, it will be in `engine_v2`.

**And one row of it is wrong, found while collating §10 on 2026-10-16.** `DEFECT-HISTORY` #19 says
`benedict.css` was *"Nuked"*. It was not: `apps/web/src/app/benedict.css` is live, imported at
`globals.css:9`, still declaring the unlicensed face — and it has a live consumer,
`story-block.tsx:71`. The row's resolution is also wrong on its own terms: it says *"`--font-serif`
owns the role"* where §6.1 says the stack reads `var(--font-instrument-serif)` and **never**
`var(--font-serif)`. The full finding, with the three further corrections that came out of the same
pass (#11's one site is six; `layout.tsx:68-70`'s stated reason does not hold; an unrecorded
`font-serif` call site at `about/page.tsx:109`), is in `SECTION10-DO-DONT.md` §Corrections. The
bridge stays read-only; what changes is that `#19` is no longer quotable as closed.

---

## 18 · Open decisions

| # | Decision | Status |
|---|---|---|
| 1 | Token granularity past colour and type | Open — spacing and radii yes; shadows and motion only if used in more than one place |
| 2 | `@theme` in `globals.css`, or a separate `theme.css` it imports | Open — `PLAN.md:235` says `globals.css`; the archive's draft uses a separate file. **Now carries the z-binding too**: `--z-*` is not a Tailwind v4 namespace, so the z-ladder in `COMPONENTS.md` §3.2 generates no utility until this is settled |
| 3 | Enforcement strength | Open — proposed **fail**, not warn |
| 4 | Keep the reference's *Agent Prompt Guide* section? | **Resolved 2026-10-16 — include it.** A one-pass build is the point, and a machine reader of `DESIGN.md` needs the no-debt rule and the token prohibitions stated for it rather than inferred. Section **11** of the skeleton (§9) ships. **The section is owed** — §7 row 13 is partial until it is written |
| 5 | Elevation: adopt the archive's 4 + 1 + 2 proposal? | **Resolved 2026-10-16 — adopted, with three adjudications.** Both the archive and `AUDIT-MISSING-PRIMITIVES` §5.2 derived the same seven tokens from the same 14 live literals, so the agreement is evidence rather than inheritance. See §6.5: one success glow not two, the blue glow dropped, Tailwind's named shadows banned. This unblocks the button hierarchy |
| 6 | Layout rhythm and gutters: 224px and `px-12→20`, or the fluid clamp and `px-6→16`? | **Resolved 2026-10-16 — the harvest wins.** `theme.generated.css:87` declares `--spacing-section: 224px`, fixed; the page container is `px-12 md:px-16 lg:px-20` in every section. The clamp is declined and the `px-6 sm:px-10` family belongs to `NavBar.tsx:159`, not to a page container. No measurement was needed once the source was read — see §6.5 |
| 7 | The dashboard container — `max-w-7xl` against the ruled `max-w-6xl` | **Resolved 2026-10-16 — one universal horizontal container.** Every page surface sits inside `max-w-6xl` with `px-12 md:px-16 lg:px-20`: zero conditional page widths, zero dashboard exceptions. `COMPONENTS.md` §3.1 carries the full table. **Two scope boundaries, both ruled:** dialogs and modals are *not* pages and keep their own caps under §10's rule 7 (`CtaLeadModal` 760px, the billing dialog 520px, `pedigree-tab.tsx:590`); and the lock is **horizontal only** — vertical rhythm varies by surface type (marketing `py-section` 224px, functional headers `pt-32 pb-24`), which must not be forced into one rule. **This ruling also corrected a miscount:** the "(4×)" this item and `COMPONENTS.md` §3.1 both carried attributed all four `max-w-7xl` sites to the dashboard; only **one** is — one is MyStable, two are the horse-about route, one is the pedigree modal |
| 8 | `coming_soon_details` — its label and its treatment | Open. The sixth database status, absent from every map in the estate. `COMPONENTS.md` §2 has it sharing `coming_soon`'s; that may be right, but it is not yet a recorded decision |
| 9 | Breakpoints: tokenise them, as the reference pattern does? | **Resolved 2026-10-16 — no.** Breakpoints stay out of `@theme`. Page layouts differ legitimately per view, and tokenising the set constrains pages that share nothing. Standard Tailwind prefixes apply, mobile-first, under one rule. The one exception is the *chrome* collapse point, `COMPONENTS.md` §8 — 768px, one value for three surfaces that must agree with each other. Closes §7 row 10 |
| 10 | `--color-on-light` — create it, or name `--color-on-gold`? | **Open, raised 2026-10-16 by the provenance pass.** Live declares only `--color-on-gold: #0a0a0a` (`theme.generated.css:40`); `--color-on-light` is a bridge proposal, and four rules already tell the builder to use `text-on-light` — §6.3, `COMPONENTS.md` §9 do-not 3, `SECTION10-DO-DONT.md` §10.1, and `DEFECT-HISTORY` #4's resolution. Either the alias is created or those four name `--color-on-gold`. `SOURCE-TRUTH.md` C3 |
| 11 | `.label-badge` — create the class, or drop the fourth label role? | **Open, raised 2026-10-16 by the provenance pass.** §6.2 locks four roles; three exist as classes, and the fourth (`.label-badge`, 10 / 500 / 0.05em) exists nowhere in the build. The live fourth class is `.label-mono-intro`, declared with zero consumers. The **tracking** value `0.05em` is live as `tracking-wider`. A status pill plausibly needs the role, and `STEP2:155` already proposes the name `--tracking-tag` — but it is a decision, not a harvest. `SOURCE-TRUTH.md` C5 |
| 12 | Should `DESIGN.md` carry a Provenance section? | **Resolved 2026-10-16 — no, cut.** The skeleton's 11th section is removed and the sections below it renumber (`Agent Prompt Guide` becomes 11). `DESIGN.md` is a forward-looking spec consumed by builders and agents; a value→source table is forensic reference and neither reader can act on it. `SOURCE-TRUTH.md` keeps the evidence in this folder. `§11`'s third check compares values against `globals.css`, not citations, so the doc-first flip is unaffected — and §10's drift narratives stay, since they are the reason a rule exists. §9 carries the full argument |

---

## 19 · Next action

**Workstream C — pattern locks. ✅ Complete.** Nine components locked in `COMPONENTS.md`: the whole
chrome, the button hierarchy, the figure row and form field, and the mobile surfaces the old build
never had. Four consolidation jobs remain there and none is a component.

**Do/Don't (#12) — ✅ closed 2026-10-16.** `SECTION10-DO-DONT.md` collates `DEFECT-HISTORY`'s 24
defects into 21 rules. Four needed writing from scratch (#7, #11, #12, #17) because no rule existed
for them anywhere in the estate; one (#24, asset naming) is not a design rule and is excluded with
that reason stated. The collation also corrected four rows of `DEFECT-HISTORY` — see §17.

**Provenance — ✅ collated 2026-10-16, and no longer a `DESIGN.md` section.** `SOURCE-TRUTH.md`
records every value §6 locks against the element, property and `file:line` it came from, in §8's
seven categories. Provenance was **cut from the `DESIGN.md` skeleton** on 2026-10-16 (§9, §18 item 12):
`DESIGN.md` is a forward spec consumed by builders and agents, and a `file:line` table serves neither.
The file stays as the forensic record, so the values remain re-verifiable after the cutover. It was a
collation, and it still found **eight corrections**: four values §6.3 presents as measured are
proposals (the status slate, the disabled grey, the on-light alias, the badge class), and `#64748b` —
the value actually live — fails AA where the proposed one clears it. Four more correct a rationale in
§6.1, a derivation in §6.5, and three undercounts in `DEFECT-HISTORY`. All eight are filed in
`SOURCE-TRUTH.md` and argued in §6.

**Two rows stand between this table and thirteen ✅, and neither is a collation:**

- **Rule on §7 row 9 — motion granularity.** The one row ruled nowhere. §18 item 1 already proposes
  the shape ("spacing and radii yes; shadows and motion only if used in more than one place"), and
  the durations are locked in §6.5. What is missing is the decision itself.
- **Write §7 row 13 — the Agent Prompt Guide.** Decided 2026-10-16 (include it); the section is owed.
  It should say what a machine reader of `DESIGN.md` needs stated rather than inferred: zero debt,
  name a role never a value, and the four prohibitions this audit keeps re-learning.

Three smaller jobs beside them:

- **Rule on `coming_soon_details`.** The sixth status has no label or treatment anywhere in the
  estate (§8). It currently shares `coming_soon`'s, which may be right — but it is unrecorded.
- **Rule on §18 item 2** — whether the `@theme` block lives in `globals.css` or a `theme.css` it
  imports, and with it how the z-ladder binds. Not on the critical path; it has to be settled
  before the block is written.
- **Rule on §18 items 10 and 11** — whether `--color-on-light` is created or the four rules naming it
  switch to `--color-on-gold`, and whether `.label-badge` becomes a real class or the fourth label
  role is dropped. Both came out of the provenance pass; both are decisions, not edits.

**Closed here since this list was written, and removed from it rather than left struck through:**
§18 item 7, the dashboard container — ruled 2026-10-16, one universal horizontal container. §18 item
9, breakpoints — not tokenised. §18 item 4, the Agent Prompt Guide — included, so it appears above as
a writing job rather than a decision.

**And the harvest's own follow-through**, if it is wanted: `SOURCE-TRUTH.md`'s eight corrections change
four rows of §6.3, one reason in §6.1, one derivation in §6.5, the provenance claim in §6.2 and the
completeness claim in §6.5. They are recorded and argued but **not all applied** — C3 (`--color-on-light`) and C5
(`.label-badge`) need a ruling, not an edit, because each is a decision to create a token or to
rename one.
