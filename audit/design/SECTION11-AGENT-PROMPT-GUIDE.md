# §11 Agent Prompt Guide — the target `DESIGN.md`, section 11

> **What this is:** the content of section 11 of the target `DESIGN.md`. Section **11**, not 12 —
> Provenance was cut from the skeleton on 2026-10-16 and everything below it renumbered (README §9,
> §18 item 12).
>
> **Status:** ✅ ready. Written 2026-10-16, from the founder's ruling text, with three corrections and
> three additions — all marked and all argued below.
>
> **Why the section exists.** Decision 4 (README §18): a one-pass build is the point, and a machine
> reader needs the no-debt rule and the token prohibitions **stated** rather than inferred. This is the
> only section of `DESIGN.md` written *for* a machine rather than about the system, and it is the one
> that has to survive being read by an agent that has nothing else.
>
> **This file does not leave this folder.** What follows is lifted into `DESIGN.md` verbatim at
> Workstream E (README §13).

---

## 11 · Agent Prompt Guide

When writing or modifying code in `website/`:

**1 · Zero raw values.** Never write an ad-hoc hex code, `rgb()`, `rgba()`, or a raw Tailwind palette
utility (`text-purple-400`, `bg-zinc-900`) outside `globals.css`. Always consume a named semantic token
from the theme. A literal at a call site is the drift this system exists to prevent, and a palette
utility is the same defect wearing a name.

**2 · `body` owns the face.** Never set `font-sans` or `font-serif` on a component — the UI stack is
inherited from `body`. **Instrument Serif** is reserved for one italic gold word per headline and is set
strictly via `var(--font-instrument-serif)`, never `var(--font-serif)`, which carries an OS-dependent
generic tail. **Geist Mono** carries the financials — tabular numbers, hashes, countdowns, `.label-spec`
— **and the editorial voice**: standfirsts and secondary-page eyebrows. It is not financial-only.

**3 · Closed component variants.** Never invent ad-hoc button, card, badge, or input styles. Every
variant list is closed. Adding one requires an explicit architectural ruling, not a local decision.

**4 · One universal horizontal container.** All page layouts and chrome use `max-w-6xl` with gutters
`px-12 md:px-16 lg:px-20`. Never introduce an alternative page width (`max-w-7xl`, `max-w-[1440px]`) or
a rogue gutter (`px-4`, `px-6`). **Overlay dialogs are not pages** — they take an explicit width cap
(760px, 520px) rather than the page container.

**5 · No blind hover, no blind focus.** Every hover transition is wrapped in `@media (hover: hover)`.
Never write `focus:outline-none` without providing the single system focus ring
(`outline-2 outline-offset-4 outline-edge`) **on the same line** — a border recolour is not a ring.

**6 · Beware `text-muted`.** `--color-muted` resolves to surface `#111111`, which is near-black and
never legible as type. Dim metadata uses `text-muted-foreground` (`#7c7c7c`).

**7 · 44px is the floor for anything tappable.** Steppers, checkboxes, toggles, icon buttons. Anything
under it that a person must press to buy something is a defect, not a density choice.

**8 · Seven elevation tokens are the whole shadow vocabulary.** `--shadow-panel`, `--shadow-modal`,
`--shadow-float`, `--shadow-card-hover`, `--shadow-bevel`, `--shadow-glow-success`, `--shadow-glow-gold`.
Never write a `shadow-[…]` literal, never reach for Tailwind's named shadows (`shadow-sm`, `shadow-xl`),
and never concatenate the bevel with a depth shadow — compose them as
`shadow-[var(--shadow-panel),var(--shadow-bevel)]`.

**9 · Vertical rhythm is per surface type.** Marketing sections run `py-section` (224px). Functional
dashboard and application headers run `pt-32 pb-24`. Never force the two into one value, and never
invent a third — if a section feels wrong at its rhythm, fix the section, not the rhythm.

**10 · Motion is CSS-first.** No motion library, no physics engine, no external animation package.
Transitions, not user-triggered keyframes. The hero renders on first paint with entrance delays capped
at 0.2s / 0.32s — nothing may hold the largest contentful paint invisible. Collapse animates
`grid-template-rows: 0fr ↔ 1fr` with no JS measurement. Everything above is zeroed under
`prefers-reduced-motion: reduce`.

---

## What was changed from the ruling text, and why

Three corrections and three additions. **Every one is a rule already locked elsewhere in this folder —
none of them is a new decision.**

**C1 · Rule 2 said Geist Mono is used "exclusively for tabular numbers, financials, and `.label-spec`".**
That is narrower than README §6.1, which gives the face a second job in as many words: *"Financials,
hashes, countdowns, tabular figures — **and the editorial voice**: standfirsts, secondary-page
eyebrows."* As written, the guide would have told an agent that a standfirst in mono is a violation.
Corrected.

**C2 · Rule 2 said to set the serif "strictly via `var(--font-instrument-serif)`" — correct, and it
needed its reason.** `var(--font-serif)` *is* declared and *does* lead with the instrument-serif
variable; what it adds is `ui-serif, Georgia, "Times New Roman", Times, serif` behind it, which is drift
mechanism 2 and the reason the ruling exists. `SOURCE-TRUTH.md` C4, README §6.1.

**C3 · Rule 3's "closed variants" was left as written, but it is the rule with the most reach.** Five
of `DEFECT-HISTORY`'s 24 defects are one job built twice (#13 and the shape it repeats), and §10's
rule on component re-invention is the one that catches them. No change to the sentence; noting that it
is load-bearing rather than boilerplate.

**A1 · Added rule 7 — the 44px touch law.** It is `COMPONENTS.md` §3.3, §10's rule, and `DEFECT-HISTORY`
#5, where a 24×28px stepper and a 16×16px acceptance checkbox sat on the purchase path. An agent guide
that omits the rule guarding the purchase flow is missing its most expensive omission.

**A2 · Added rule 8 — the elevation vocabulary.** It is `COMPONENTS.md` §1 do-not 3 and `DEFECT-HISTORY`
#15: 21 arbitrary shadows across 14 definitions, plus 11 named utilities with no token behind them. This
is the defect class an agent reproduces most readily, because writing a shadow is easier than looking one
up.

**A3 · Added rule 9 — vertical rhythm.** Ruled 2026-10-16 (§18 item 7): horizontal containment is
universal, rhythm is not. `PressShowcaseSection`'s `py-24` is defect #25, found by that ruling, and it is
exactly the mistake an agent makes when a section looks wrong — it adjusts the page rhythm instead of the
component.

**Nothing was removed.** The six rules as supplied are all sound and all survive.

---

## Owed before this section ships

Two tokens this guide names are settled but not yet declared, and a guide that names a token the build
does not have is worse than one that stays quiet:

| Named in | Status |
|---|---|
| `--color-on-light` (rule 1's implied set) | **Ruled 2026-10-16** — declared alongside `--color-on-gold` at `#0a0a0a` (§18 item 10). Not in the theme yet |
| `--tracking-tag` (rule 1's implied set) | **Ruled 2026-10-16** — `.label-badge` is created at 10 / 500 / 0.05em (§18 item 11). Not in the build yet |
| `--duration-*`, `--scale-press` | **Ruled but mechanised wrongly as given** — neither is a Tailwind v4 namespace, so both bind as `@utility` (§18 items 1 and 2). Rule 10's values depend on this landing |

All three are recorded in §18 and none blocks writing `DESIGN.md`; they block the `@theme` block that
compiles from it.
