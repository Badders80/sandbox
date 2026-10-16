# §10 Do / Don't — the target `DESIGN.md`, section 10

> **What this is:** the content of section 10 of the target `DESIGN.md` (README §7 row 12, README §9).
> A collation of `DEFECT-HISTORY-2026-10-16.md`'s 24 defects — **plus three the audit produced later**
> (#25 the `PressShowcase` rhythm break, #26 the 1400ms beat floor, #27 the pedigree zoom) — into
> **24 rules**, each stated forward and carrying the drift that is its reason.
>
> **Status:** ✅ ready. Written 2026-10-16. Verdicts marked `adopted` / `departs` per README §5.
>
> **Superseded for rule text, 2026-10-16.** The rules below now live in `DESIGN.md` §10, which is
> authoritative. What is unique to this file is the audit-side apparatus — not the rules.
>
> **This file does not leave this folder.** Only `DESIGN.md`, the `@theme` block and the check do
> (README §13). What follows is lifted into `DESIGN.md` verbatim at Workstream E.

---

## The ruling on form — restate, and cite

**`DESIGN.md` restates each rule in its own words and cites the lock as provenance.** It does not
reference the lock as the substance.

Three reasons, and they are the whole argument:

1. **`DESIGN.md` is the only artifact that leaves this folder** (README §13) and it lands in
   `evolution/engine_v2/website/website/` beside the app it describes. `COMPONENTS.md` "does not leave
   this folder" (README §17). A reference would point the reader of `DESIGN.md` at a document they
   will never hold.
2. **README §11's third check compares `DESIGN.md` against `globals.css`.** A section made of
   dangling references is not machine-checkable, and §11 is what makes the doc-first flip safe.
3. **The cost is one line per rule against a reader who cannot act.** Restating is cheap; a
   specification that only works if you have the working folder is not a specification.

**And both pressures are held.** `DEFECT-HISTORY` is right that "a specification that carries a list
of the old build's mistakes is a specification arguing with a codebase that will not exist" — so no
rule below is phrased as a prohibition on the old build. The `DESIGN.md` skeleton (README §9) is
equally right that each entry must **name the drift it caused** — so every rule carries its drift as
a footnote, in the past tense, as *reason*, never as *rule*. Forward rule; the defect as why.

---

## §10 Do / Don't

**The rules are numbered 1–24, in document order, and the numbers are stable.** They are cited by
number in the collation below and in README §6.5, so a new rule **appends** as 25 — numbering is
never re-flowed to make a section read tidier. The number is a citation handle, not a priority:
rule 16 is not more important than rule 22.

### 10.1 Colour and surface

**1 · Don't take a colour from anywhere but the locked set. Do read it off the token table.**
*Drift:* `text-purple-400` went on the MyStable `5×M` figure — a raw Tailwind palette class, in a
system that has no purple. A ban on *literals* alone does not catch it: a palette utility is the
same defect wearing a name.

**2 · Don't write a hex as a text colour. Do use `--color-on-light` for dark text on any light fill.**
*Drift:* `text-[#111]` sat beside a token holding `#0a0a0a` — wrong value, and the raised-surface
colour used as type. Wrong twice.

**3 · Don't declare a token nothing consumes. Do delete it.**
*Drift:* `--shadow-success-glow-strong` was declared and never wired; `--label-mono-intro` was a
label role with zero consumers. A declaration with no consumer is an intention that does not
resolve — the same failure as a class that resolves to nothing.

**4 · Don't ship a decorative effect that cannot be seen on the surface beneath it. Do check the
mid-stop against the canvas.**
*Drift:* `via-black/70` ran over a `#030303` canvas — invisible at every one of its six call sites
across four files, all copied from one another.

**5 · Don't pick a status colour by eye. Do take the colour and the words from the locked status table.**
*Drift:* `completed` shipped blue and `fully_subscribed` shipped white against a locked amber.
Amber on `fully_subscribed` means *demand still standing*, never a warning.

### 10.2 Type

**6 · Don't name a family inside a component. Do let `body` own the face.**
*Drift:* `font-heading` was applied to every FAQ question and resolved to nothing — a utility naming
a face that had never been declared.

**7 · Don't declare a second serif face. Do take the one serif from `--font-instrument-serif`, italic,
one word per page.**
*Drift:* `benedict.css` declared a commercial face that was never licensed, and the stack fell
through to Georgia — one page, whichever face the OS had.

**8 · Don't use a weight off the scale. Do use 300 / 400 / 500; 600 maps to 500.**
*Drift:* `font-semibold` appeared 30 times across 6 files against a system that had three weights.

**9 · Don't hand-type a tracking value. Do take one of the four named steps.**
*Drift:* one button type carried `0.2em` and `0.05em` — two answers to a question the spec had
already answered.

### 10.3 Shape and depth

**10 · Don't use a numeric Tailwind radius name. Do take the scale — 8 / 16 / 24 plus pill.**
*Drift:* bare `rounded` fell through to Tailwind's built-in 4px at 17 call sites. The named tiers are
the same defect completed.

**11 · Don't invent a border opacity. Do use `/20`, `/40`, `/60`.**
*Drift:* 19 distinct border-opacity values were live.

**12 · Don't write a shadow at a call site. Do use one of the seven elevation tokens.**
*Drift:* 21 arbitrary shadows across 14 distinct definitions, plus 11 named utilities with no token
behind them, plus a call-site literal with no token at all.

**13 · Don't build a job twice. Do keep one component per job.**
*Drift:* two status-badge implementations of one enum — and the component written to unify them
became a third. A second implementation is a defect even when it is written better than the first.

### 10.4 Layout

**14 · Don't give a surface its own gutter. Do use the one container: `max-w-6xl`, `px-12 md:px-16
lg:px-20`.**
*Drift:* hero and body grid ran `px-12` and `px-6` — two left edges on one page. The chrome and the
content disagreeing about the left edge is the same defect, and it is why the wordmark never lines
up with the headline beneath it.

**15 · Don't fix a column's width in pixels. Do make it fluid and cap it at a breakpoint —
`w-full md:max-w-[300px]`.**
*Drift:* a `w-[300px]` rail overflowed its column by 28px at 320px. A fixed width inside a fluid
parent is an overflow waiting for a narrow viewport.

**This rule governs dialogs and modals, and the page container does not.** A dialog is an overlay
shell, not a viewport: it takes its own intentional cap — `760px` for the CTA lead modal, `520px` for
the billing dialog, and the pedigree modal's own — rather than the page's `max-w-6xl`. Containment
rules bind pages and chrome; a cap binds an overlay.

**16 · Don't size a tappable control below 44px.**
*Drift:* stepper buttons at 24×28px and a 16×16px acceptance checkbox — both purchase-critical.

**17 · Don't put the only route to purchase at the end of a scroll. Do keep the mobile conversion bar.**
*Drift:* the horse page's primary CTA sat at the bottom of a single-column mobile scroll.

**18 · Don't scale a DOM node to make it fit. Do let the container scroll, or scale the SVG's
`viewBox`.**
*Drift:* the pedigree table ran `scale-[0.76] origin-top-left -mb-[24%] -mr-[24%]` — the node scaled
down to fit a narrow viewport, with negative margins compensating for space the transform never freed.
A transform shrinks the paint but not the box, so the tap targets and the layout flow keep the
unscaled geometry. A transform is not a responsive layout.

**19 · Don't invent a fifth page-level padding scheme. If a section feels wrong at its rhythm, fix the
section, not the rhythm.**
*Drift:* `PressShowcaseSection` ran `py-24` (96px) on a marketing page because someone eyeballed the
logo carousel and broke the 224px section rhythm. Fix component spacing inside the section, not by
altering page rhythm.

### 10.5 Components and states

**20 · Don't write a hover state that matches its own base. Do make the hover change something.**
*Drift:* the ghost variant hovered `border-border` → `border-border` — identical to its base, a no-op
that read as a working interaction.

**21 · Don't ship an unguarded hover. Do wrap every hover rule in `@media (hover: hover)`.**
*Drift:* zero guards anywhere — every hover rule shipped to every touch device, and an infinite
shimmer ran on phones.

### 10.6 Motion

**22 · Don't hold the largest contentful paint invisible. Do have the content present at first paint.**
*Drift:* the hero was held invisible for 0.85s and the tagline for 1.05s, both paid for in LCP.
Entrance timing is not styling; it is a cost the page pays before anyone reads it.

**23 · Don't measure in JavaScript what CSS can animate. Do collapse with grid rows only.**
*Drift:* the panel read `scrollHeight` in JS while also animating grid rows — two mechanisms for one
movement, and the measurement had to be retaken on every open.

**24 · Don't hold conversion steps behind artificial elapsed-time timers. Do bound wait times strictly by
real network and API responses.**
*Drift:* the legacy purchase flow enforced a mandatory `MIN_BEAT_MS = 1400` timer on every step,
degrading conversion under the guise of readability. Readability is solved by the 220ms enter
transition, not by holding the user hostage. Elapsed time is bounded by the API, never by a clock we
invented.

### 10.7 Out of scope for this section — stated, not silently dropped

**Asset naming is not a design rule.** Three assets shipped named `untitled-35`, `-36` and `-37`.
That is build hygiene, and this is not a build checklist — a spec that grows conventions for file
names has started describing a repository instead of a system. The other 23 defects each produced a
rule; this one did not, and the exclusion is stated here rather than leaving the reader to wonder why
the count is 23.

### 10.8 Owed before this section ships

Two rules below name something the build does not have, and a spec must not name a token that does
not resolve. Both are open decisions, not edits — the rule is right either way, only the noun changes.

| Rule | Names | Status |
|---|---|---|
| rule 2 | `--color-on-light` | Not a live token. Live declares `--color-on-gold`. Either it is created as an alias, or this rule switches noun — and three other places say the same thing, so it is one decision, not four. |
| rule 7 | `--font-instrument-serif` | **Live and correct.** Listed here only because the obvious alternative, `var(--font-serif)`, *is* declared and carries an OS-dependent generic tail. This one resolves; that one would not. |

The first is recorded as README §18 item 10 and `SOURCE-TRUTH.md` C3.

---

## The collation — 27 defects into 24 rules

| Defect | Rule (§10.1–10.6) | Home before this file | Disposition |
|---|---|---|---|
| 1 | **6** · Don't name a family; `body` owns the face | README §6.1 | restated |
| 2 | **10** · Don't use a numeric radius name | README §6.5; `COMPONENTS.md` §1 | restated |
| 3 | **20** · Don't write a hover that matches its base | `COMPONENTS.md` §9 do-not 4 | restated |
| 4 | **2** · Don't write a hex as text | `COMPONENTS.md` §9 do-not 3 | restated |
| 5 | **16** · Don't size a tap target below 44px | `COMPONENTS.md` §3.3; README §6.5 | restated |
| 6 | **17** · Don't put the only purchase route at the end | `COMPONENTS.md` §6 | restated |
| 7 | **15** · Don't fix a column width in px | **none** — §6 cited the shape, stated no rule | **new** |
| 8 | **14** · Don't give a surface its own gutter | `COMPONENTS.md` §3.1 | restated |
| 9 | **23** · Don't measure in JS what CSS can animate | README §6.5; `COMPONENTS.md` §12 | restated |
| 10 | **21** · Don't ship an unguarded hover | `COMPONENTS.md` §3.4 | restated |
| 11 | **4** · Don't ship an invisible effect | **none** | **new** |
| 12 | **22** · Don't hold the LCP element invisible | **none** — §5 do-not 3 asserted 0.2/0.32 in passing | **new** |
| 13 | **13** · Don't build a job twice | `COMPONENTS.md` §2 do-not 1–2 | restated |
| 14 | **5** · Don't pick a status colour by eye | `COMPONENTS.md` §2 do-not 6; README §6.3 | restated |
| 15 | **12** · Don't write a shadow at a call site | README §6.5 | restated |
| 16 | **11** · Don't invent a border opacity | README §6.5 | restated |
| 17 | **1** · Don't take a colour outside the token set | **none** — §11 check 1 banned literals only | **new** |
| 18 | **8** · Don't use a weight off the scale | README §6.4; `COMPONENTS.md` §10 | restated |
| 19 | **7** · Don't declare a second serif | README §6.1 | restated — **see C1** |
| 20 | **9** · Don't hand-type a tracking value | README §6.2 | restated |
| 21 + 22 | **3** · Don't declare a token nothing consumes | README §6.5, §6.2 | restated — collated into one rule |
| 23 | (folds into **12**) | README §6.5 | restated — collated |
| 24 | — | — | **excluded** (§10.7) |
| **25** | **19** · Don't invent a fifth page-level padding scheme | **none** — found after the harvest, by the 2026-10-16 rhythm ruling | **new** |
| **26** | **24** · Don't hold conversion steps behind artificial timers | **none** — `AUDIT-MOTION` C1, not `DEFECT-HISTORY`. Ruled to land in §9 and here on 2026-10-16 | **new** |
| **27** | **18** · Don't scale a node to make it fit | **none** — found by the 2026-10-16 vocabulary ban | **new** |

**Counted:** 8 restated from component locks · 11 restated from section rules (9 rules, after
collating #21+#22 and folding #23 into #15) · **7 written new** · 1 excluded. 8 + 11 + 7 + 1 = 27,
into **24 rules**.

**None of #25, #26 or #27 is in `DEFECT-HISTORY`, and none can be.** That file lives in the bridge,
outside version control, and is the extraction's read-only record of 24 rows. #25 came from the
rhythm ruling (`PressShowcaseSection`'s `py-24`); #26 from `AUDIT-MOTION`'s C1 (the 1400ms beat
floor). Both are logged here and in README §6.5. **So this file is no longer purely a collation of
`DEFECT-HISTORY` — it is that collation plus two rules the audit produced later**, and the opening
line says so.

---

## Corrections found while collating

Findings 1–4 change a rule or a source citation and are recorded here because they are not
fixable in place. README §16 states the reason plainly: this folder is markdown-only, and README §12
rules that this audit "writes documents" and is "not a change to any page" — so the build repo is
read and cited, never edited.

**C1 · `DEFECT-HISTORY` #19 says `benedict.css` was "Nuked". It was not.** As read on 2026-10-16,
`apps/web/src/app/benedict.css` exists, is imported at `globals.css:9`, still declares the
unlicensed `@font-face`, and has a **live consumer** — `story-block.tsx:71` uses `font-benedict` on
the story heading. The defect is open, not closed, and the §10.2 rule above is written as a standing
rule rather than as a resolution, because the thing it resolves is still shipping.

**C2 · `DEFECT-HISTORY` #19's resolution contradicts README §6.1.** #19 reads *"Nuked; `--font-serif`
owns the role."* README §6.1 reads *"The stack reads **that** variable, never `var(--font-serif)`."*
Restating #19 as written would import the generic tail the ruling exists to kill — `tokens.ts:63`
sets `BRAND_FONTS.serif` to `var(--font-instrument-serif), ui-serif, Georgia, "Times New Roman",
Times, serif`. §6.1 wins, and §10.2 follows §6.1.

**C3 · `layout.tsx:68-70`'s stated reason is wrong, though its conclusion is right.** The comment
says pointing the stack at `var(--font-serif)` "would be a self-reference". It would not: per
`tokens.ts:63` the generated `--font-serif` *leads with* `var(--font-instrument-serif)` and carries
the generic chain behind it. The real reason to read `--font-instrument-serif` is that `--font-serif`
drags an OS-dependent generic tail — which is drift mechanism 2, the exact defect the ruling exists
to prevent. Recorded, not corrected: it is a comment in the build repo.

**C4 · A live `font-serif` call site survives that no file records.** `horses/[slug]/about/page.tsx:109`
sets the barn-name drama word in `font-serif`. README §11's second proposed check bans `font-sans`
and `font-serif` outside `globals.css` — which would fail this call site — and README §6.1 does not
mention it. It is the same shape as defect #1: intent that does not resolve to the chosen face.

**C5 · `DEFECT-HISTORY` #11 understates its own defect.** It records one site
(`MarketplaceSection.tsx:89`); the sweep is at `:92` and appears **six times across four files** —
`MarketplaceSection.tsx:92,129,171`, `DigitalSyndicationSection.tsx:127`, `HowItWorksSection.tsx:104`,
`design-lab/page.tsx:61`. All six are the identical copied string, and all six also carry
`duration-400`, a duration off the lock. A resolution applied at one site leaves five broken.

**C6 · Two minor drifts, recorded for the next reader.** README §6.2 cites `NavBar.tsx:192`; the
class string is at `:193`. And `DEFECT-HISTORY` #22 describes `--label-mono-intro` as one role; the
theme declares it as four — `-size`, `-weight`, `-tracking` at `theme.generated.css:132-134` plus the
class at `:164-167`.

**Also verified while collating, and worth having on the record.** Every defect cited against source
was checked against `evolution/engine/website` (`apps/web`, plus `packages/brand_dna`): #3's no-op
ghost hover, #4's `text-[#111]`, #9's `scrollHeight` beside grid rows, #14's blue `completed` and
white `fully_subscribed`, #7's `w-[300px]`, #21/#22's unwired declarations, and
`--spacing-section: 224px` at `theme.generated.css:87` with the `xl`/`2xl`/`3xl` radius aliases all
holding `24px` at `:81-83`. Nothing in this section rests on a value found only under
`/home/evo/audit/website/`.

---

## Provenance

| Value or rule | Source |
|---|---|
| The 24 defects | `DEFECT-HISTORY-2026-10-16.md` (bridge folder, outside version control) |
| The 25th (#25) | README §6.5 — the rhythm ruling, 2026-10-16. Not in `DEFECT-HISTORY` |
| Container, gutters, touch law, hover guards, focus ring | `COMPONENTS.md` §3.1–3.5 |
| Component do-nots | `COMPONENTS.md` §2, §6, §9, §10 |
| Faces, label roles, colour, type, shape, depth, motion | README §6.1–6.5 |
| Live verification | `evolution/engine/website` — `apps/web`, `packages/brand_dna/src/theme.generated.css`, `packages/brand_dna/src/tokens.ts` |
