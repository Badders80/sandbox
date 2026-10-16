# SOURCE-TRUTH — value → source, so every lock can be re-verified

> **What this is:** the provenance ledger for the locked token set (README §6). Every value README
> §6 locks is recorded next to the element, the property and the `file:line` it was read from.
>
> **Why it exists.** This file was briefly the target `DESIGN.md` section 11 (README §7 row 13, since
> removed from the bill of materials). **Provenance was cut from the `DESIGN.md` skeleton on
> 2026-10-16** — `DESIGN.md` is a forward-looking specification consumed by builders and agents, and a
> table of `file:line` is forensic reference that neither can act on. So the evidence lives here
> instead of in the spec, which is where it is useful. §8 Workstream A: *"Provenance is mandatory.
> Every value is recorded with the element and property it came from, so it can be re-verified
> later."* The live page is the source of truth and **it will change** — the domain cutover is coming
> (`PLAN.md:107`) — so this is a **method**, not a copy-paste. It is the file that makes the harvest
> repeatable after the thing being harvested is gone.
>
> **Status:** ✅ collated 2026-10-16 from STEP1–3, `DEFECT-HISTORY`, and a direct read of the live
> source. Nothing below cites `/home/evo/audit/website/`.
>
> **This file does not leave this folder.** Only `DESIGN.md`, the `@theme` block and the check do
> (README §13). This is the evidence behind `DESIGN.md` §11 (Provenance), not §11 itself.

---

## How to re-verify

The test is mechanical, and §5 states it. A value is **verified** only if it is found in
`evolution/engine/website` — the app, `packages/brand_dna/src/theme.generated.css`, or
`packages/brand_dna/src/tokens.ts`. A value found only under `/home/evo/audit/website/` is a
**proposal** — and so, it turns out, is a value whose only home is this folder (see §Corrections).

Two commands reproduce most of the tables below:

```sh
cd evolution/engine/website
cat -n packages/brand_dna/src/theme.generated.css          # colours, type, radii, spacing, fonts
grep -rn 'shadow-\[' apps/web/src --include=*.tsx          # every elevation value in the app
```

**Verdicts.** `adopted` — the live value is the locked value, no argument needed. `departs` — the
locked value differs from live, and §5 requires one argued line saying why.

**A note on the app path.** The app is `apps/web`, not `apps/website`. Four `DEFECT-HISTORY` rows and
one README sentence refer to `apps/website` in prose; the file paths in them are otherwise correct.

---

## 1 · Colour

All from `packages/brand_dna/src/theme.generated.css` unless stated. The theme is a **generated
file** (`tokens.ts` → `generate-theme.ts` → here, per the header at `:1-9`); the hand-edit target is
`tokens.ts`.

### Surfaces — `adopted`

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-canvas` | `#030303` | `theme.generated.css:19` | adopted |
| `--color-surface` | `#0a0a0a` | `theme.generated.css:20` | adopted |
| `--color-raised` | `#111111` | `theme.generated.css:21` | adopted |

The comment at `:18` records the retirement of the `l1–l4` ladder (2026-09-22), which is why three
steps and not four.

### Structure — one `departs`, unsourced

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-border` | `rgba(255,255,255,0.1)` | `theme.generated.css:30` | adopted |
| `--color-edge` | `#9a9aa0` | `theme.generated.css:35` | adopted |
| `--color-disabled` | `#62666d` | **no declaration found anywhere** | **departs — see C2** |

Retired-and-still-declared at `:31-34`: `hairline #050505`, `ash #575757`, `smoke #454545`,
`stage-black #000000`. README §6.3 retires all four; the declarations remain in the generated theme,
so a future reader will meet them.

### Text — `adopted`

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-heading` | `#f8fafc` | `theme.generated.css:25` | adopted |
| `--color-ink` | `rgba(255,255,255,0.5)` | `theme.generated.css:24` | adopted |
| `--color-hover` | `#b9b3a9` | `theme.generated.css:46` | adopted |
| `--color-muted-foreground` | `#7c7c7c` | `theme.generated.css:26` | adopted |
| `--color-foreground` | `= var(--color-ink)` | `theme.generated.css:100` (shadcn slot) | adopted |

`--color-muted: var(--color-raised)` = `#111111` at `:111` — the `text-muted` landmine README §6.3
names. `stat-row.tsx:11-12` carries the warning in the source itself.

### Accents — one `departs`

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-gold` | `#d4a964` | `theme.generated.css:38` | adopted |
| `--color-gold-hover` | `#c39853` | `theme.generated.css:39` | adopted |
| `--color-on-gold` | `#0a0a0a` | `theme.generated.css:40` | adopted |
| `--color-on-light` | `#0a0a0a` | **not a live token** — bridge `V2-THEME-2026-10-16.css:50` | **departs — see C3** |
| `--color-spot-mint` | `#00e599` | `theme.generated.css:41` | adopted |

Also live and **not in the locked set**: `--color-stripe-purple: #635BFF` and
`--color-stripe-purple-light: #8884FF` (`:42-43`), consumed four times in `purchase-flow-modal.tsx`
(`:1736-1738`, `:1957-1958`). README §6.3 records them and their missing ruling.

### Status — one `departs`, unsourced

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-status-active` | `#10b981` | `theme.generated.css:49`, `tokens.ts:229` | adopted |
| `--color-status-pending` | `#f59e0b` | `theme.generated.css:50`, `tokens.ts:230` | adopted |
| `--color-status-closed` | live `#64748b` / locked `#738396` | `theme.generated.css:51`, `tokens.ts:231`, `globals.css:74` | **departs — see C1** |
| `--color-destructive` | `#ef4444` | `theme.generated.css:52`, `tokens.ts` | adopted |

The status vocabulary is the six-value `CampaignStatus` enum, declared four times live:
`database.types.ts:71`, `lib/campaign-status.ts`, `packages/ui/src/status-pill.tsx`,
`asset-lock.ts:45` (`COMPONENTS.md` §2 do-not 2).

### Legal — `adopted`

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--color-legal-surface` | `#ffffff` | `theme.generated.css:55` | adopted |
| `--color-legal-ink` | `#111111` | `theme.generated.css:56` | adopted |
| `--color-legal-surface-alt` | `#f5f5f5` | `theme.generated.css:57` | adopted |
| `--color-legal-border` | `#dddddd` | `theme.generated.css:58` | adopted |
| `--color-legal-checkbox` | `#b98a2f` | `theme.generated.css:59` | adopted |

---

## 2 · Type roles

### Faces — `adopted`

| Lock | Source | Note |
|---|---|---|
| System sans stack | `theme.generated.css:14` | delivered by `body`; no file |
| Geist Mono | `theme.generated.css:15`, `layout.tsx:60` | `--font-geist-mono`, via `next/font` |
| Instrument Serif | `theme.generated.css:16`, `layout.tsx:73-80` | `--font-instrument-serif`, **italic cut only** |
| Bw Gradual | `brand/fonts/` | logo mark only, SVG paths, not a web font |
| Geist Sans | `brand/fonts/retired/` | retired 2026-09-22 |

`layout.tsx:64-72` carries the serif rationale and `:76-80` the italic-only ruling. **C4** covers why
the stack must read `--font-instrument-serif` and not `var(--font-serif)`.

### Scale — `adopted`

`theme.generated.css:62-68`, seven tokens: `micro 10` · `label 11` · `body-small 15` · `body 16` ·
`card-heading 18` · `section-heading 36` · `section-heading-wide 48`. The comment at `:61` records
that 36 and 48 are one role at two breakpoints.

**The 64px display heading is a role without a token.** Hand-typed as `md:text-[64px]` at
`marketplace/page.tsx:67` and `marketplace/[slug]/page.tsx:116` — one recipe, two files. Weight 300,
tracking `-0.04em`, leading 1.05 (`STEP2:90`). `--text-display` is an owed **name**, and §6.4
records it as such.

### Weights — `adopted`, and three not two

| Value | Source |
|---|---|
| `300` | `theme.generated.css:71` (`--font-weight-light`) |
| `500` | `theme.generated.css:72` (`--font-weight-medium`) |
| `400` | `theme.generated.css:130` (`--label-spec-weight`) — the third weight, live in the label layer rather than the weight layer |

### Label roles — `adopted` as classes, with one locked role that is not live

| Role | Size / weight / tracking | Source | Verdict |
|---|---|---|---|
| `.label-eyebrow` | 11 / 300 / 0.2em | `theme.generated.css:123-125`, class `:142-147` | adopted |
| `.label-action` | 11 / 500 / 0.2em | `theme.generated.css:126-128`, class `:149-154` | adopted |
| `.label-spec` | 10 / **400** / 0.2em + mono | `theme.generated.css:129-131`, class `:156-162` | adopted |
| `.label-mono-intro` | 12 / 400 / 0 | `theme.generated.css:132-134`, class `:164-167` | **live, zero consumers** — `DEFECT-HISTORY` #22 drops it |
| `.label-badge` | 10 / 500 / 0.05em | **no declaration found anywhere** | **departs — see C5** |

**The live theme's own comment is stale.** `:120` reads *"Label roles — one small-uppercase job,
**three** roles"* and then declares four (`:123-134`). The class comment at `:164` is the fourth.

`STEP1:75-82` lists the four roles as eyebrow / action / spec / **mono-intro** — which is the live set
minus the dropped role and **not** the locked set. `STEP3:146-148` is the only STEP file that lists
eyebrow / action / spec correctly, and it does not carry a fourth. `README` §6.2's four are
eyebrow / action / spec / **badge**.

---

## 3 · Space

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--spacing-section` | `224px` | `theme.generated.css:87` | adopted |
| Section padding in use | `py-section` | `FAQSection.tsx:56`, `AboutSection.tsx:25`, `OwnershipFAQSection.tsx:58` | adopted |
| Container | `max-w-6xl`, `px-12 md:px-16 lg:px-20` | `FAQSection.tsx:57`, `AboutSection.tsx:26`, `OwnershipFAQSection.tsx:59` | adopted |
| Touch target floor | `44px` | **a ruling, not a literal** — see §7 | departs from live |

The theme comment at `:86` reads *"the number the landing actually renders"* — the harvest's own
justification, in the generated file. Live's four container schemes are tabulated in
`COMPONENTS.md` §3.1; two of them (nav `max-w-[1440px]`, footer `px-8 md:px-16`) are retired there.

**Two honest exceptions**, per README §6.5: `PressShowcaseSection.tsx:171` runs `py-24` (96px), and
`NavBar.tsx:159` runs its own `max-w-[1440px] px-6 sm:px-10 lg:px-12`.

---

## 4 · Shape

| Lock | Value | Source | Verdict |
|---|---|---|---|
| `--radius-sm` | `8px` | `theme.generated.css:76` | adopted |
| `--radius-md` | `16px` | `theme.generated.css:77` | adopted |
| `--radius-lg` | `24px` | `theme.generated.css:78` | adopted |
| `--radius-xl` / `-2xl` / `-3xl` | `24px` each | `theme.generated.css:81-83` | adopted |
| `--radius-pill` | `9999px` | `theme.generated.css:84` | adopted |
| `--radius-xs` | does not exist | — | adopted (as an absence) |
| Border opacities | `/20`, `/40`, `/60` | literal scan across `apps/web/src` | adopted |

`theme.generated.css:74-75` and `:79-80` carry the reason the aliases exist: so no utility can fall
through to Tailwind's own scale and reintroduce a fifth radius. That is `DEFECT-HISTORY` #2 answered
at the generator rather than at the call site.

---

## 5 · Depth

Seven tokens, derived by `AUDIT-MISSING-PRIMITIVES` §5.2 from the live literals. Every row below was
re-found in `apps/web/src` on 2026-10-16 by grepping `shadow-[`.

| Lock | Value | Live literal at | Verdict |
|---|---|---|---|
| `--shadow-panel` | `0 0 60px rgba(0,0,0,0.6)` | `purchase-flow-modal.tsx:208`, `right-rail.tsx:223`, `modal-shell.tsx:39` — all three composed with the bevel | adopted |
| `--shadow-modal` | `0 0 120px rgba(0,0,0,0.98)` | `CtaLeadModal.tsx:210`, `horse-cta-modal.tsx:73`, `mystable-dashboard.tsx:316` | adopted |
| `--shadow-float` | `0 30px 80px rgba(0,0,0,0.6)` | `auth-card.tsx:182`; `right-rail.tsx:401` (+bevel) | adopted |
| `--shadow-card-hover` | `0 20px 40px rgba(0,0,0,0.45)` | `marketplace-listing-grid.tsx:134` | adopted |
| `--shadow-bevel` | `inset 0 1px 0 rgba(255,255,255,0.05)` | composed at `purchase-flow-modal.tsx:208`, `right-rail.tsx:223`, `:401`, `modal-shell.tsx:39` | adopted |
| `--shadow-glow-success` | `0 0 8px rgba(16,185,129,0.6)` | **does not reproduce — see C7** | **departs** |
| `--shadow-glow-gold` | `0 0 12px rgba(212,169,100,0.25)` | `pedigree-tab.tsx:207`, `:359` (hover highlight) | adopted |

`--shadow-panel` and `--shadow-modal` are the two values that **concatenate depth and highlight**,
which is why the bevel had to be split out rather than tokenised as-is. Every other elevation token
appears as a single value.

**Two live glows the seven do not account for.** `pedigree-tab.tsx:275` runs
`0 0 20px rgba(212,169,100,0.3)` on a selected node — a second gold value beside the locked
12px/0.25, on the same component that carries the locked one. `pedigree-table.tsx:55` runs
`0 0 18px rgba(16,185,129,0.12)` — a third emerald. If the seven tokens are the whole vocabulary,
both are dropped like the blue; neither is recorded in README §6.5, and `DEFECT-HISTORY` #15's "14
distinct values" does not name them.

**Two declared-and-unwired**, `DEFECT-HISTORY` #21: `globals.css:38-39` declares
`--shadow-success-glow` (20px/0.35) and `--shadow-success-glow-strong` (32px/0.55). The `-strong`
variant has no consumer. Note the **name flip** `STEP3:9` flags: this file writes `success-glow`, the
locked token is `glow-success` — one token, two orders.

**The hero's shadow is dropped, not folded.** `page.tsx:30` carries
`shadow-[0_0_80px_RGBA(0,0,0,0.35)]`. `DEFECT-HISTORY` #23 drops it outright. **`STEP1:248` and
`STEP1:300` both say it "collapses into `--shadow-modal`"** — that is superseded, and STEP1 is stale
in two places on this point.

---

## 6 · Motion

| Lock | Value | Source | Verdict |
|---|---|---|---|
| Hover duration | `200ms` | the modal `duration-200` family — `auth-card.tsx:320`, `:345`, `:365` | adopted |
| Nav / chrome duration | `300ms` | `NavBar.tsx:165`, `:173`, `:193`; `GlowPillButton.tsx:13` | adopted, unnamed |
| Collapse | `300ms` in, `200ms` out | `CollapsePanel.tsx:29` (`duration-300`); exit is a ruling, not a literal | departs |
| Shimmer | `2000ms` | `STEP1:304` | adopted (name owed) |
| Hero entrance | `0.2s` / `0.32s` | a ruling — live is `0.85s` / `1.05s`, `STEP1:181` | departs — `DEFECT-HISTORY` #12 |

`CollapsePanel.tsx:22-30` is the JS-measurement defect (#9): it sets `gridTemplateRows` **and** reads
`scrollHeight`. The canonical version is grid rows only.

**Row 9 of §7 is the open one.** Durations are locked; *granularity* — whether motion gets tokens at
all — is not, and `§18` item 1 proposes the shape without deciding it.

---

## 7 · Interactive states

| Lock | Value | Live | Source | Verdict |
|---|---|---|---|---|
| Focus ring | 2px outline, 4px offset, `--color-edge` | **three rings, disagreeing** | `NavBar.tsx:165`, `:193`, `:232`, `GlowPillButton.tsx:13` (`outline-primary/50`, gold at 50%); `field.tsx` (`ring-2 ring-muted-foreground/40`); `PillField` (same pair) | departs — `COMPONENTS.md` §3.5 |
| Touch law | `44px` | `26×28px` steppers; `16×16px` checkbox | `purchase-flow-modal.tsx:434`, `:485` (`h-7 w-6`); `:949`, `:1782` (`h-4 w-4`) | departs — `COMPONENTS.md` §3.3 |
| Hover guards | every hover in `@media (hover: hover)` | **zero guards repo-wide** | `DEFECT-HISTORY` #10 | departs — `COMPONENTS.md` §3.4 |
| Z-ladder | five named slots | ten distinct values, `-1` to `10000` | `COMPONENTS.md` §3.2 | departs |

`purchase-flow-modal.tsx:171` carries the live workaround verbatim: *"Overlay sits above the nav
(z-[10000] > NavBar z-[9999])"* — one author compensating for an accident at the call site.

---

## Corrections — values locked in README §6 that the live build does not contain

These are the point of the exercise. README §6.3 opens *"**Verified 2026-10-16 by measurement.**"*
Four of its rows do not survive that claim, and §5 names exactly this failure: *"a value found only
under `/home/evo/audit/website/` is a **proposal**, however confident the prose around it reads."*
Two of the four below are not even in the bridge.

**C1 · `--color-status-closed` is locked as `#738396`. Live is `#64748b`.** The live value appears at
`theme.generated.css:51`, `tokens.ts:231` and `globals.css:74`. `#738396` appears **nowhere** in
`/home/evo/audit` or `/home/evo/sandbox` except README §6.3 itself and `STEP1:9`. The contrast ratio
§6.3 quotes, **5.32**, is not the live value's: `#64748b` on `#030303` measures **≈4.33:1 and fails
AA**, while `#738396` clears it at 5.32. So the locked value is *better* than live and is a
defensible departure — README §6.3 already argues the family's shape ("do not neutralise it") — but
it is a **departure**, and it is currently presented as a measurement. `STEP1:7-11` propagates the
same claim.

**C2 · `--color-disabled: #62666d` has no source at all.** No declaration in the theme, the app, or
the bridge. Its only occurrence in the estate is `README.md:224`. §6.3 counts it among "eight opaque
neutrals" — on live source read tonight, there are seven.

**C3 · `--color-on-light` is not a live token.** Live has `--color-on-gold: #0a0a0a`
(`theme.generated.css:40`). `--color-on-light` is a bridge proposal (`V2-THEME-2026-10-16.css:50`,
`V2-DESIGN-SPEC-2026-10-16.md:58`). **This one has teeth:** `DEFECT-HISTORY` #4's resolution tells the
builder to use `text-on-light`, and `SECTION10-DO-DONT.md` §10.1 and `COMPONENTS.md` §9 do-not 3
repeat it. Either the token is created as an alias of `on-gold`, or the rule names `--color-on-gold`.
As written, the fix instruction points at a token that does not exist.

**C4 · `--font-serif` carries the generic tail the serif ruling exists to kill.**
`tokens.ts:63` sets `BRAND_FONTS.serif = 'var(--font-instrument-serif), ui-serif, Georgia, "Times New
Roman", Times, serif'`, which the generator writes as `--font-serif` (`generate-theme.ts:100`,
`theme.generated.css:16`). Reading the stack from `--font-serif` therefore re-admits the OS-dependent
fallback chain of drift mechanism 2. `layout.tsx:68-70` reaches the right conclusion — read
`--font-instrument-serif` — from a **stated reason that does not hold** (it calls the alternative "a
self-reference"; it is not). README §6.1 has the conclusion right and does not carry the bad reason.
Two things follow: the reason should be the tail, and `about/page.tsx:109` still sets a drama word in
the `font-serif` *utility*, which README §11's second proposed check would fail.

**C5 · `.label-badge` does not exist in the live build.** A repo-wide grep returns zero occurrences.
The live fourth label class is `.label-mono-intro` (`theme.generated.css:164-167`), declared with zero
consumers — which is `DEFECT-HISTORY` #22. The tracking value `0.05em` **is** live, as Tailwind's
`tracking-wider` on the highlight tags (`STEP2:46`), and `STEP2:155` proposes naming it
`--tracking-tag`. So the locked set's fourth *role* may well be right as a decision; what is wrong is
that §6.2 presents it as a class read off the build.

**C6 · Three further undercounts, for the same reason as C1–C5.** `DEFECT-HISTORY` #4 records one
`text-[#111]`; there are **three** (`solid-pill-button.tsx:39`, `auth-card.tsx:345`,
`purchase-flow-modal.tsx:875`), and the cited line is off by one. `#11` records one `via-black/70`
sweep; there are six across four files. `#24` records one `untitled` asset; there are three. `#13`'s
and `#5`'s cited lines are correct.

**C7 · `--shadow-glow-success`'s stated derivation does not reproduce.** README §6.5 says *"three
inline literals use `8px/0.6`"* and takes the 8px one as the survivor. The 8px/0.6 literal is not in
the build. What is in the build is **one** call site — `marketplace-listing-grid.tsx:65`, written
`shadow-[0_0_8px_var(--shadow-success-glow)]`, which is an 8px blur carrying the **20px/0.35** token's
colour, and `globals.css:38-39` carrying 20px/0.35 and 32px/0.55. So the locked value takes its blur
from one call site and its alpha from a source this pass could not find. This is not necessarily
wrong — the badge rule (`COMPONENTS.md` §2) may be where `0.6` is decided, and a token may legitimately
be an adjudication rather than a harvest — but §6.5 presents it as derived from live literals, and it
is not. Either the derivation is corrected or the adjudication is stated as one.

**C8 · Raw Tailwind palette colours are more widespread than `DEFECT-HISTORY` #17 records.** #17 names
one (`text-purple-400` on the MyStable figure). Live also carries
`bg-emerald-500/15 border-emerald-400/30 text-emerald-200` (`campaign-status.ts:166`),
`border-emerald-500/40` (`pedigree-table.tsx:55`), `bg-zinc-900/60 border-zinc-100/40 text-zinc-100`
(`campaign-status.ts:172`), and `bg-blue-600/20 border-blue-400/40 text-blue-200`
(`campaign-status.ts:177`). This **strengthens** `SECTION10-DO-DONT.md` §10.1's rule and README §11
check 1 as widened — the ban is not a one-off tidy-up, it is the status layer's default habit.

---

## The light scope — a second live palette README §6 does not record

`globals.css:58` opens `[data-theme="light"]`, overriding the house tokens for a light console:
`--color-canvas: #f7f7f5`, `--color-surface: #ffffff`, `--color-ink: rgba(15,18,24,0.72)`,
`--color-gold: #a87c2a`, `--color-status-active: #047857`, and more. A further dormant family sits
beside it — `--color-light-canvas`, `--color-light-ink`, `--color-light-border`,
`--color-light-surface-alt` (`globals.css:80+`, marked "dormant arsenal, NOT activated on any
route").

**It is parked, not active**: `globals.css:49` reads *"no live route sets `data-theme="light"` today
(design-lab demos it)"*. So excluding it from the locked 24 is right. But it is **unrecorded**, and
README §6.3 records its neighbours — the Stripe purples and the 16-slot shadcn block — precisely so
the next reader is not surprised. The scope also carries a **documented contrast gap** at
`globals.css:53-57`: `--color-edge` is not overridden, measures 2.80:1 on the light canvas, and is
below the 3:1 the E03 guard enforces. A light route that adds an outline pill must override it.

---

## What this changes

| Finding | Follows through to |
|---|---|
| C1, C2 | README §6.3 — two rows re-marked `departs`; the "eight opaque neutrals" count |
| C3 | `SECTION10-DO-DONT.md` §10.1, `COMPONENTS.md` §9 do-not 3, `DEFECT-HISTORY` #4's resolution |
| C4 | README §6.1 — the rule stands; the *reason* changes, and `about/page.tsx:109` is an unrecorded call site |
| C5 | README §6.2 — the role may stand as a decision; the provenance claim does not |
| C6 | `DEFECT-HISTORY` #4, #11, #24 — counts, not rules |
| C7 | README §6.5 — the glow's derivation, or its adjudication status |
| C8 | `SECTION10-DO-DONT.md` §10.1, README §11 check 1 — the widened ban is justified by breadth, not by one site |
| Light scope | README §6.3 — record it beside the purples and the shadcn block |
| Two unaccounted glows | README §6.5 — the seven tokens' completeness claim |

**Five of the eight are corrections to this folder's own files**, found by reading them against the
source — which is what §5 says the folder has been burned by twice. C1 and C2 make §6.3 honest about
which values are measurements and which are proposals; C3 and C5 name a token and a class the build
does not contain; C4 corrects a rationale without moving its rule; C6–C8 are counts and derivations.
**None re-opens a locked decision.**
