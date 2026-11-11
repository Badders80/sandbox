# Greenfields — what I would build if we started today

Written 2026-11-11. A counterfactual, not a critique.

The product is fixed: horse percentage points, a contract series, a PDS/SA per
investment, priced per 1% per month, whole-month terms. The rulings hold. What
follows is the machine I would build around that product, judged only by one
question: how much of it would you adopt on Monday, and what would you throw
away.

## 1. What the record says

From `sandbox/audit/corpus-deep-dive/out/report.md`, across 73 scored sessions:

| Signal | Rate | Meaning |
|---|---|---|
| time-sink | 91% | Sessions spend their budget on overhead, not output |
| redo | 92% | Work is redone — often re-running gates that already passed |
| scope-drift | 88% | The task grows while it is being done |
| correction | 89% | The agent's own work needs correcting |
| rework-loop | 42% | Near baseline — the actual defect catches |
| frustration | 53% | Near baseline — not caused by errors |

The headline from the report: the structural four rose 29–47 points above the
120-file baseline, while the symptom two barely moved. **The cost is
re-derivation and re-verification, not defect recovery.**

Four named mechanisms in the corpus:

- **Verification tax** — "~10 of 26 redo signals are re-runs of already-passing
  gates"; agents fixing their own harnesses rather than the artefact.
- **Self-review** — the model that executed also audits. It rated a
  settlement-breaking commit PASS because it could not see the break.
- **Collision tax** — sibling sessions fighting over `.next`, `index.lock` and
  branch names; one session swept another's files into a commit.
- **Prompt bloat** — stacked rules and war-room law correlate with the highest
  time-sink counts.

## 2. Five root causes in this build

**R1 — The model moved while the surface was built.** Trainers moved horse →
deal; owners and trainers merged into parties; readiness was redefined; images
stopped blocking. Each changed what the site was rendering. This is the largest
single source of rework, and it is why the sidequest exists.

**R2 — Two codebases.** `engine/website` (`evo_02`) and `engine_v2/website`
(`engine-v2`) are separate repositories with no shared merge base. Two gates,
two deploy pipelines, two sets of docs, and a migration between them.

**R3 — Prose was the source of truth.** The same rule was stated in
`OUTCOME.md`, a migration, a TS module, a test and a template. Every restatement
is a place to drift, and drift is what the rulebook now indexes.

**R4 — State lived in two columns.** `status` plus `closed_at` means every
predicate has to test both. `00027` created the case; `00028` and the `R-DSL-04`
gap are the cleanup.

**R5 — Concurrency was managed by discipline.** Shared `.next`, shared database
port, shared branch names. The corpus shows discipline failing; the fix applied
later (`NEXT_DIST_DIR`) is the shape the design should assume.

## 3. The design

### 3.1 One repository

```
/evolution
  app/          one Next app — route groups (public) and (ops)
  domain/       TS calculations only; no rule of record
  db/
    migrations/ numbered, forward-only
    rules/      one SQL function per rule, named r_<area>_<n>
    probes/     one per migration, each with -- expect: N
  docs/
    rulebook/   RULES, OPEN, decisions
  ops/          justfile, deploy, backup, restore
```

One app, two route groups: the public site is open, `/ops/*` sits behind
Access. One gate, one deploy, one place to look.

**Why:** R2. Two codebases is the most expensive decision in the current build
and the least visible in any single document.

### 3.2 Three nouns, one document

The only structural change I would make to the model:

| Noun | Holds | Exists when |
|---|---|---|
| **horse** | facts, trainer, images, registry | first |
| **series** (the DSL) | owner, commercials, expiry, term | the deal is agreed |
| **offer** | the stake being sold from that series | it is ready and published |
| **investment** | buyer, stake, money, frozen documents | a sale occurs |

Today `dsls` is series and offer in one table with nullable columns. That is why
there is a readiness gate, a "one dateless draft per horse" partial index, and a
`coming_soon` status that also means archived. Split them and all three
workarounds disappear: a series exists only with terms; an offer exists only
when it is offered; a draft is a series nobody has offered yet.

The sale still stores a full snapshot. The documents still compile once, at
sale, from the snapshot. Nothing an investor sees changes.

### 3.3 Rules as functions

Every rule that touches money, allocation, documents or state is a SQL function
in `db/rules/`, named after its rulebook ID, with the ID in the function
comment. TS calls it; TS does not re-implement it. Where TS must mirror a rule
for display, a test binds the mirror to the function.

This is the existing direction, made total. It is why the current build holds
up: `record_sale_atomically` and `close_dsl` are already rules-as-functions.

### 3.4 Proof

One command, one shape:

```
just prove  →  db reset → migrate → probes → rulebook check → tests → build
```

The rulebook check asserts three things: every `enforced` rule names a probe or
test that exists; every probe declares `-- expect: N`; every rule cited in a
migration exists in `RULES.md`.

CI runs exactly the same command. No second definition of green.

### 3.5 Surfaces

- **Public:** reads engine state, renders it, hands off to checkout. No price, no
  readiness, no status decision.
- **Operator:** three screens — records, listings, investments — each a view over
  the same state. The ledger reads the sale snapshot, never live terms.

The test of a correct surface: delete it and the business still runs from the
database and the functions.

### 3.6 Operations

- One deployable, one environment variable set.
- Cloudflare Access in front of `/ops/*`, not the whole host.
- Backups offsite, restore drilled before the first real sale.
- Documents archived with a manifest outside the database, written from the same
  transaction that writes the sale.

## 4. Build order

One vertical slice, then breadth.

1. **Schema + rules** for one horse, one series, one offer, one investment.
2. **Sale path** — reserve, pay, record, freeze, archive, ledger.
3. **Operator** — one screen that shows a series and its investments.
4. **Public** — one horse page, one offer page, checkout handoff.
5. **Walk it** — the DoD from `DOD.md`, both walks.
6. **Breadth** — more horses, owners, terms; only after the slice is proven.

No horizontal layers. Each step ends with something a person can use.

## 5. What survives

| Keep | Why |
|---|---|
| Ownership model and rulings 29–35 | Decisions, not accidents |
| PDS/SA templates and block structure | Legal prose is already right |
| `record_sale_atomically`, `close_dsl` | Already rules-as-functions |
| Sale snapshot + `sales_term_shape` | The ledger depends on it |
| Probes, `verify-db`, schema assert | The cheapest trust you own |
| Placeholder-image rule | Correct, and already end to end |
| Rulebook v0.1 | 43 rules, evidence-backed |

| Discard | Why |
|---|---|
| Two-repo split | Duplicate gates, duplicate docs, no merge base |
| `status` + `closed_at` dual state | One state machine, including `archived` |
| `dsls` as series + offer | The source of three workarounds |
| Readiness as a separate gate | Readiness is a property of an offer |
| One-draft-per-horse index | A draft is just an unoffered series |
| Rule statements repeated in docs | One authority, mirrors bound by tests |
| Admin breadth built early | It is not on the path to a sale |

## 6. What it costs

- Rebuilding the operator surface, which is the part you use every day.
- Rebuilding the public site against the split model.
- A second data migration: one horse, one party, one draft today. Small now,
  expensive after ten horses.
- The risk that the redesign is right and the schedule is not.

**The honest case against:** the current build already satisfies most of the
design. The savings are in deletion, not construction. If the two-repo split and
the series/offer conflation are not causing pain weekly, greenfield is a
preference, not a need.

## 7. How we would know it worked

The corpus gives the acceptance test. Structural antipatterns should fall from
88–92% back toward the 59–61% baseline, while `rework-loop` and `frustration`
hold or improve. If time-sink and redo do not move, the redesign solved the
wrong problem.

## 8. Open questions

1. Can the v1 site keep shipping while the new app takes over, or does one repo
   force a cutover date?
2. Archive vendor and WORM semantics — object lock, or versioned bucket plus a
   signed manifest?
3. Operator surface: three sections as today, or one series view that contains
   its offers and investments?
4. Does the founder want the split model at all, or is `dsls`-as-one-table worth
   keeping once the dual state is fixed?

## See also

- `MEDIA.md` — the speculative media layer: document artefacts, provenance,
  rights and post-sale content.
