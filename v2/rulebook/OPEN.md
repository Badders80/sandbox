# Open items — v0.1

This file records what the rulebook cannot yet assert as fully enforced. It is
the gap register, not a second rulebook.

## Known conflicts and decisions

| ID | Item | Current position | Needed |
|---|---|---|---|
| `O-01` | U18 is snapshot-only. The live DSL can still drift until F2. | The ledger reads the sale snapshot; no post-sale economic-term guard lands in chunk 4. | F2 decides whether to freeze live economic terms after a sale. |
| `O-02` | D1 is deferred, not resolved. | The buyer email links to MyStable; it is not a copy. Document recovery is database-only until F3. | F3 external archive plus manifest. |
| `O-03` | Horse capacity is external. | The founder owns total horse capacity and external owner terms in v1. | Keep the ledger labelled as known system exposure. Add external allocation support only when required. |
| `O-09` | Contract ID is not printed yet. | F1. | Add to templates, compile input, sale, index and archive naming. |
| `O-10` | MyStable frozen-byte rendering is unverified. | Chunk 4 verification item. | Confirm stored `pds_markdown`/`sa_markdown` are served, not recompiled. |
| `O-11` | Display precision is not yet standardised. | The legal money formatter can render cents, while customer-facing rules require whole dollars. | Add one money formatter and one percentage formatter; audit website, ledger, PDS/SA and emails. Do not round stake percentages. |

**Closed 2026-11-11 by chunk 4 (`00024`/`00025`):** `O-04`–`O-08` — `stake_returned_at`, `record_sale_atomically`, the close audit columns, the sale snapshot and the sale-time start are implemented and evidenced.

## Follow-up register

| ID | Follow-up | Status |
|---|---|---|
| `F1` | Contract ID printed on PDS/SA and indexed. | after chunk 4 |
| `F2` | Post-sale economic-term freeze guard. | after chunk 4 |
| `F3` | External immutable document archive and hash manifest. | after chunk 4 |
| `F4` | Offsite database backup and restore drill. | after chunk 4 |
| `F5` | Recovery test: rebuild one position from retained documents. | after chunk 4 |

## Rules lacking direct evidence

These are recorded as rules but should not be treated as proven until the named
evidence exists:

- `R-DOC-04` — contract ID test.
- `R-DOC-05` to `R-DOC-06` — archive, hash verification and recovery test.
- `R-UNIT-02` — one horse point equals a 1% stake; percentage wording is
  investor-facing language and the 100-point denominator is stated once.
- `R-DISP-01` to `R-DISP-03` — formatter audit and rendered-output checks.

## Deferred public work

The public wrap remains separate: `dsl-sidequest/PUBLIC-WRAP.md`.

- P1 wholesale removed from the public payload.
- P2 default stake at 1%.
- P3 public projection proof.
- P4 images-coming-soon fallback.
- S1 rename moves the R2 image folder.

These are not rules of the engine, but they depend on the engine contract and
must be reconciled at the public integration review.

## Candidates from build corpora (2026-11-11)

Extracted from the 10-step build (`sandbox/v2/`) and the sidequest
(`sandbox/v2/dsl-sidequest/`). None of these carries a rule ID yet. Ordered by
risk: money and legal first, then allocation, then process.

| # | Candidate rule | Primary authority | Evidence found at | Why it matters | Conflicts with |
|---|---|---|---|---|---|
| 1 | A checkout hold expires after 600 seconds and its reserved stake returns to the listing. | TS constant + DB TTL | `evolution/engine_v2/website/engine/src/lib/purchase.ts:54`; `evolution/engine_v2/website/supabase/migrations/00018_checkout_hold_ten_minutes.sql:2` | A shorter or inherited default strands capacity or lets a hold outlive the buyer's session. | none |
| 2 | Checkout proceeds only when `kyc_status = verified`; `pending` and `failed` are refused. | TS | `evolution/engine_v2/website/engine/src/lib/purchase.ts:326`; `evolution/engine_v2/website/engine/src/lib/purchase.ts:395` | An unverified buyer could contract for a lease without identity checks. | none |
| 3 | An investor must be paid up for two full calendar months before sharing in a race. | Legal procedure | `sandbox/v2/OUTCOME.md:24` | A holder in arrears would receive prize money. | none |
| 4 | Refunds are calculated on full calendar months remaining only, with zero day-count apportionment, and paid only after trailing care and operational costs are settled. | Legal procedure | `sandbox/v2/PLAN.md:73` | Day-count refunds create disputed amounts and refund money before costs are known. | none |
| 5 | Insurance proceeds belong to the owner/lessor; leaseholders have zero entitlement. | Legal template | `sandbox/v2/PLAN.md:74`; `evolution/legals/legal-foundation/sa-foundation.md:143` | Paying proceeds to holders would convert a leasehold into equity. | none |
| 6 | On a missed payment, prize distributions pause immediately; if the balance is not cleared before the next billing cycle, the stake and deposit are forfeited to the horse owner, with no benefit to Evolution. | Legal procedure | `sandbox/v2/PLAN.md:75` | Continued payouts to a defaulter, or Evolution retaining a forfeit, misstates the deal. | none |
| 7 | `upfront` collects 100% of the lease term at checkout and makes zero subsequent charges. | TS | `evolution/engine_v2/website/engine/src/lib/pricing.ts:103`; `sandbox/v2/PLAN.md:72` | A second charge after the full term is collected is double-billing. | none |
| 8 | Recurring billing starts on the 1st of the month following join, pays Month 3 in advance, and holds a five-month float buffer drawn down in the final months. | Legal procedure | `sandbox/v2/PLAN.md:71` | A wrong start date or buffer breaks the deposit reserve and leaves the term underfunded. | none |
| 9 | The owner may end a DSL only by 14-day written notice (default) or a 3× remaining-lease-value buyout, and the SA must state the settlement for both payment models. | Legal template | `sandbox/v2/dsl-sidequest/STATE.md:109`; `evolution/legals/legal-foundation/break-clause.md:20` | An unstated or single-model settlement produces an unenforceable exit. | none |
| 10 | A sale is refused when the inclusive remaining term is fewer than one month, counted from the first day of the buyer's purchase month. | TS + DB | `sandbox/v2/dsl-sidequest/CHUNK4-BRIEF-2026-11-11.md:49` | Selling a zero-month term collects money for nothing. | none |
| 11 | Every PDS and SA names Alex Baddeley, Evolution Stables Ltd, as promoter. | Legal template | `sandbox/v2/OUTCOME.md:52`; `evolution/legals/legal-foundation/pds-foundation.md:284` | A missing or wrong promoter breaks the disclosure and signature block. | none |
| 12 | An expired or released hold writes no sale; it marks `paid_unfulfilled` and alerts the founder. | DB function | `sandbox/v2/dsl-sidequest/CHUNK4-BRIEF-2026-11-11.md:59` | Money taken without a sale would otherwise disappear from the ledger. | none |
| 13 | A stake must be a whole multiple of the DSL step in basis points; `min_stake` and `step` are positive, `min_stake <= listed_stake`, and `listed_stake` divides by `step`. | DB check + TS | `evolution/engine_v2/website/supabase/migrations/00005_dsls.sql:36`; `evolution/engine_v2/website/engine/src/lib/pricing.ts:135` | Off-step stakes mis-price the deal and cannot be reconciled to the listing. | none |
| 14 | The effective minimum stake is `min(min_stake, stake_remaining)`, so the last slice is always buyable. | TS | `evolution/engine_v2/website/engine/src/lib/pricing.ts:151`; `sandbox/v2/PLAN.md:230` | A stranded remainder leaves unsold inventory that no buyer can purchase. | none |
| 15 | The sum of listed stakes across a horse's live DSLs must not exceed 100 percentage points, checked manually by the founder. | Manual control | `sandbox/v2/dsl-sidequest/STATE.md:80` | More than 100 points listed oversells the horse. | none |
| 16 | `stake_remaining` is set from `listed_stake` when null and is never reset by an edit. | TS + DB | `sandbox/v2/dsl-sidequest/STATE.md:185` | Resetting it reopens sold capacity and breaks the cap-table identity. | none |
| 17 | Only these status moves are legal: `coming_soon -> available`, `available -> fully_allocated`, `available -> coming_soon`, `fully_allocated -> completed`, `available -> completed`, plus no-op and `null -> coming_soon`/`available`. | DB trigger + TS | `evolution/engine_v2/website/supabase/migrations/00021_parties_and_hardening.sql:125` | Any other edge bypasses readiness or reopens a completed term. | none |
| 18 | When a sale takes the last point, status becomes `fully_allocated` from `stake_remaining = 0`, not from the caller's claim. | DB function | `evolution/engine_v2/website/supabase/migrations/00024_ledger.sql:455` | A caller-supplied terminal state can desynchronise status from capacity. | none |
| 19 | A horse that is not registered cannot move out of `coming_soon`. | DB trigger | `evolution/engine_v2/website/supabase/migrations/00021_parties_and_hardening.sql:147` | An unregistered horse could be offered for sale. | none |
| 20 | A horse slug is derived from the legal name and unique; a rename changes the slug and moves the image folder, with no redirect table. | TS + DB | `sandbox/v2/OUTCOME.md:13` | Duplicate horses or broken image URLs after a rename. | none |
| 21 | A trainer may be blank in `coming_soon` but is required, like the owner, before `available`. | DB trigger | `evolution/engine_v2/website/supabase/migrations/00021_parties_and_hardening.sql:351`; `sandbox/v2/dsl-sidequest/STATE.md:45` | A live listing would print without a trainer. | none |
| 22 | `available` requires a non-empty distribution schedule. | DB trigger | `evolution/engine_v2/website/supabase/migrations/00021_parties_and_hardening.sql:383` | A live deal would have no stated prize-distribution basis. | none |
| 23 | A trainer is stored as one row per company with trainer names joined `' & '`. | TS | `sandbox/v2/dsl-sidequest/STATE.md:59` | Separate rows drop names from the PDS, which prints `trainer.name`. | none |
| 24 | Synthetic fixture rows are never written to the hosted `evolution-engine` database. | Manual control | `sandbox/v2/dsl-sidequest/CHUNK4-PHASE-BC-BRIEF-2026-11-11.md:28` | Test buyers would pollute the production ledger and documents. | none |

### Already covered

- Retail `ceil(wholesale × 1.05 × 1.03)` — `R-PRICE-01`.
- Investor return 50–85 inclusive, no default, never a stored 75 — `R-PRICE-02`.
- Two-way price entry only on a whole-dollar wholesale — `R-PRICE-03`.
- Float initial payment of five months (3 deposit reserve + 2 prepaid) — `R-TERM-03`.
- Term of five months or fewer must use `upfront`; six or more defaults to float — `R-TERM-02`.
- One dateless draft per horse; dated terms unlimited — `R-DSL-01`.
- Images never block a listing — `R-READY-03`.
- Four narrative slots approved with timestamp and hash — `R-READY-02`.
- `stake_remaining` between zero and `listed_stake`; no oversell — `R-ALLOC-02`.
- `listed = sold + open holds + held paid_unfulfilled + remaining`, and the cap table is derived rather than stored — `R-ALLOC-01`.
- Sale snapshot, sale-time start and the atomic sale-plus-hold claim — `R-SALE-02` to `R-SALE-04`.
- One horse point equals a 1% stake; percentage wording is permitted —
  `R-UNIT-02`.
- Published is separate from status — `R-PUB-01`.

### Contradictions found

1. **Hold duration: five minutes vs ten. RESOLVED.** `OUTCOME.md:5` and `:89` say five minutes; `00018_checkout_hold_ten_minutes.sql:2` and `CHECKOUT_HOLD_SECONDS` (`purchase.ts:54`) say 600 seconds. Ruling (2026-11-07): ten minutes, because Stripe Identity does not fit in five. The sweep is `*/5` (`expire-checkouts.yml:12`), so the window is two sweeps. Ten minutes is current; the two `OUTCOME.md` lines are stale.
2. **Images: three required vs never blocking. RESOLVED.** Not a contradiction once the mechanism is named: every listing carries three image slots, and a generic placeholder fills them until real images exist. The slot count is a presentation requirement; readiness never gates on images (`00023`).
3. **Horse-level ceiling: none vs a 100-point manual cap. DROPPED.** A point is one horse percentage point, so 100 points is 100% of the horse across all live DSLs; several DSLs on one horse must not sum above it. Founder decision 2026-11-11: **no system-enforced horse ceiling in v1.** The founder manages the sum externally, alongside owner relationships and inventory, because the system cannot see external deals and a check it cannot see is not a check. Ruling **35** (`dsl-sidequest/STATE.md`). Follow-on, not in chunk 4: `DslWizard.tsx:530` still prints the cap copy and `dsl.ts:362` still describes it as an operator check; both should become a passive exposure readout or be removed.
4. **A listed DSL carries a start vs has no start. RESOLVED.** A listing carries an expiry only (ruling 25). The start is stamped at sale: first day of the investment month, then `term_end`, `term_months` and `payment_model_at_sale` are written to the sale (U21). Ruling 24 is superseded.
5. **Refund basis: full calendar months vs a termination-to-end calculation. RESOLVED.** Whole months, zero day-count. A 14-day notice date rolls forward to the next full month boundary. The SA text must state that rounding explicitly; the policy does not change.
6. **Billing start wording. NOT A CONTRADICTION.** Two different rules were conflated. `OUTCOME.md:24` is racing eligibility: two full calendar months paid before sharing in a race. `PLAN.md:71` is billing: the initial payment covers the three-month deposit, one month in advance and the current month; the next bill falls on the 1st of the following month. Both stand.

### Corpus defects

- `sandbox/v2/dsl-sidequest/STATE.md:16` says 23 migrations (`00001`–`00023`); `00024_ledger.sql` exists and is applied and frozen (`CHUNK4-PHASE-BC-BRIEF-2026-11-11.md:7`).
- `RULES.md` still labels `00024` as "planned", and `OPEN.md` O-04 to O-08 describe its columns as absent, although `00024` has landed.
- `CHUNK4-BRIEF-2026-11-11.md:24` cites the sale-delete paths at `purchase.ts:710` and `:728`; Phase B removes `deleteSaleById` and those paths (`CHUNK4-PHASE-BC-BRIEF-2026-11-11.md:17`).
- `sandbox/v2/PLAN.md:351` says `effectiveMinStake` is wired to nothing; `purchase.ts:120` now calls it.
- `OUTCOME.md:5`, `:42` and `:89` are stale on the hold duration and the image gate; `STEP10-PLAN-2026-11-07.md:66` already flags the hold text.


- `readiness.ts` and `listings.ts` never test `closed_at`. They are correct today only because closing a listed DSL flips its status to `completed` — the exact coupling `R-DSL-04` exists to remove. `R-DSL-04` stays `locked` until both predicates filter closed rows.
