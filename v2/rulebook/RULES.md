# Rules — v0.1

Canonical unit: **horse percentage points**. Contract percentage is derived
display only; it is never stored, printed in the PDS/SA, or used in a
calculation.

Status is defined in `README.md`. Source references are to the sidequest plan,
state rulings, migrations, engine modules and legal files.

## Parties and ownership

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-PARTY-01` | One profile per real-world person or company; a role is a relationship, not a permission. | DB `parties` + `party_roles` | `00021`; role checks | enforced | Ruling 10 |
| `R-PARTY-02` | A role referenced by a live DSL cannot be removed or cascaded away. | DB trigger | `00021` | enforced | Ruling 22 |
| `R-DSL-01` | A DSL is a contract series. A horse may hold several dated terms and one dateless draft. | DB unique index | `00022`; `00028` | enforced | Ruling 23 |
| `R-DSL-02` | The DSL is the only place a deal links a horse, trainer and owner. Records never author the link. | DB FKs + role trigger | `00021`; `dsl.ts` | enforced | Rulings 10–11 |
| `R-DSL-03` | The DSL name is a human label, not identity. A stable contract ID is required for documents and recovery. | Rulebook | F1 | locked | Ruling 32; F1 |
| `R-DSL-04` | `closed_at` marks a row inactive regardless of status. Every active-row predicate — unique indexes, readiness, listing queries — excludes closed rows. | DB + rulebook | `00028` (index only); readiness and listings not yet filtered | locked | Ruling 33 |
| `R-DSL-05` | A closed row is immutable. Any update to a row with `closed_at` set is refused, including un-closing and a status change. | DB trigger | `00029`; `probe-00029` 5/5 | enforced | Ruling 34 |
| `R-UNIT-01` | Stakes are stored, transmitted, contracted and displayed in horse percentage points. | DB columns | `listed_stake`, `stake`, `stake_remaining` | enforced | Ruling 30 |
| `R-UNIT-02` | Contract percentage is derived display only: never stored, never printed in legal documents, never used in a calculation. | Rulebook | UI rule | locked | Ruling 30 |

## Display and precision

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-DISP-01` | Customer-facing money is shown in whole NZD with no cents. Any fractional contract amount is rounded up before it becomes a contract term and is then stored; display never rounds a different value. | TS + templates | one money formatter; pricing tests | locked | Founder direction 2026-11-11 |
| `R-DISP-02` | Percentages are shown at their stored precision with trailing zeros removed: `1.0%` becomes `1%`; `0.1%` stays `0.1%`. A stake is never rounded to a whole percent for display. | TS + templates | one percentage formatter; PDS/SA checks | locked | Founder direction 2026-11-11 |
| `R-DISP-03` | Website, ledger, PDS/SA and emails use the same formatters. Display never changes a stored or calculated value. | TS + templates | formatter audit | locked | Founder direction 2026-11-11 |

## Contract and pricing

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-PRICE-01` | Wholesale per 1% per month is the sole price input; retail is `ceil(wholesale × 1.05 × 1.03)`. | DB generated column | `pricing.ts`; `00005`; drift tests | enforced (mirrored) | PLAN step 3 |
| `R-PRICE-02` | Investor return has no default; it must sit from 50% to 85% inclusive. | DB check + TS | `pricing.ts`; `00005` | enforced | PLAN step 3 |
| `R-PRICE-03` | Two-way entry is accepted only when a whole-dollar wholesale reproduces the entered retail. | TS | `wholesaleFromRetail`; `00022` | enforced | U7 |
| `R-PRICE-04` | Price is per 1% of the horse per month; the contract percentage does not change the rate. | Rulebook | PDS/SA tokens; `pricing.ts` | enforced | Ruling 30 |
| `R-TERM-01` | A listing carries an expiry and no start. The sale stamps the first day of the buyer's month. | DB + TS | `purchase.ts`; `00024`; `chunk4.test.ts`; local fixture | enforced | Ruling 25; U21 |
| `R-TERM-02` | Effective payment model is `upfront` when the listing is upfront or remaining term is five months or less; otherwise `subscription_float`. | TS + DB | `purchase.ts`; `00024`; `chunk4.test.ts` | enforced | Ruling 25; U21 |
| `R-TERM-03` | The float initial payment is five months: three deposit reserve plus two prepaid. | TS | `pricing.ts`; tests | enforced | PLAN step 3 |

## Readiness and publication

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-READY-01` | One readiness gate decides Available; it names missing fields rather than refusing bare. | TS + DB trigger | `readiness.ts`; `assert_dsl_available` | enforced (mirrored) | H3 |
| `R-READY-02` | Available requires all four narrative slots approved with timestamp and hash. | DB trigger | `00021`; `00022` | enforced | H3 |
| `R-READY-03` | Images never block a listing. Marketing images are not a legal precondition, and the checkout path does not read the bucket. The gallery shows only real images; a missing image stays blank. | DB trigger + checkout | `00023`; `purchase.ts` (checkout no longer reads the bucket) | enforced | Ruling 26 |
| `R-PUB-01` | Published is separate from status. Unpublished DSLs stay off the marketplace. | DB + public read layer | `00009`; `listings.ts` | enforced | OUTCOME § DSL |

## Allocation, holds and sales

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-ALLOC-01` | `listed = sold + open holds + held paid_unfulfilled + remaining`, in horse points. | DB + ledger query | `ledger.ts`; `chunk4.test.ts`; probes 10–16 | enforced | U20 |
| `R-ALLOC-02` | No oversell. Opening checkout reserves the stake by conditional decrement; expiry restores it. | DB function | `00017`; `reserve_checkout_stake` | enforced | B6 |
| `R-ALLOC-03` | A hold is capacity only while held. `stake_returned_at` null means held; set means returned. | DB column | `00024`; probes 11/13/19 | enforced | U20 |
| `R-SALE-01` | A sale row cannot be updated or deleted. `TRUNCATE` is revoked. | DB trigger + grants | `00024`; probes 24–27 | enforced | H6 |
| `R-SALE-02` | A sale is written by one atomic, idempotent RPC that also claims the hold; there is no delete path. | DB function | `record_sale_atomically`; `00024`; `chunk4.test.ts` | enforced | H6 |
| `R-SALE-03` | The sale stores the executed economic terms and the parties at sale. The ledger reads that snapshot, not mutable DSL terms. | DB columns + ledger | `00024`; `purchaseStore.ts`; `sales/page.tsx` | enforced | U18 |
| `R-SALE-04` | Sale-time start, remaining months, payment model and term end are stored on the sale. | DB columns + TS | `00024`; local fixture `termStart 2026-11-01` | enforced | U21 |
| `R-SALE-05` | A term may be closed only after stale holds are swept and while no `open` or `paid_unfulfilled` checkout exists. | DB + operator action | `00024`; `chunk4.test.ts`; probes 18–23 | enforced | U19 |
| `R-SALE-06` | `paid_unfulfilled` is a financial exception, not a sale and not capacity when its stake was returned. | Rulebook + ledger query | `ledger.ts`; probes 13/15/22/23 | enforced | U19–U20 |

## Documents and evidence

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-DOC-01` | The structured investment row is the operational SSOT; the executed PDS/SA is the legal SSOT and wins on conflict. Hashes bind them. | DB + legal templates | `sales`; `compile.ts`; `templates.ts` | enforced | Ruling 29 |
| `R-DOC-02` | Legal prose lives only in the fixed templates and blocks. The compiler substitutes declared tokens; it never generates or paraphrases prose. | Legal files + loader | `templates.ts`; `compile.ts`; token tests | enforced | PLAN step 7 |
| `R-DOC-03` | The PDS carries all four soft slots; the SA carries none of them. | Legal loader | `templates.ts`; tests | enforced | U14 |
| `R-DOC-04` | A contract ID is printed on both documents and indexed on the sale. | Legal templates + DB | F1 | locked | F1 |
| `R-DOC-05` | An external immutable document archive with its own manifest is required before claiming document recovery. | External control | F3 | locked | F3; D1 |
| `R-DOC-06` | Stored document bytes and hashes are verified; a hash that does not match the document is a defect. | Rulebook + evidence | F3 | locked | D1 |
| `R-DOC-07` | Retired. The buyer email was a link to MyStable, not a copy; recovery was database-only. Superseded by `R-DOC-08`. | Rulebook | `email.ts` history | retired | D1; founder 2026-11-11 |
| `R-DOC-08` | Every sale renders the PDS and SA to one combined PDF before the sale commits, stores both PDF hashes on the sale, and emails the PDF as an attachment with both hashes in the body. The same bytes are archived outside the database and served unchanged by MyStable. A sale without its documents is not a sale. | DB + TS + templates | `pdf_hash` columns; email attachment; archive copy; MyStable serves the same bytes | locked | Founder 2026-11-11 |

## External controls

| ID | Rule | Primary authority | Mirrors / evidence | Status | Source |
|---|---|---|---|---|---|
| `R-EXT-01` | The founder owns horse capacity and external owner terms in v1. The ledger reports known system exposure, not a complete horse cap table. | Manual control | Ruling 31 | external | Ruling 31 |
| `R-EXT-02` | External deals are not inferred from the system. Any horse-level total must say external deals are excluded. | Manual control | Ruling 31 | external | Ruling 31 |
| `R-EXT-03` | Database backup and restore are required for accounts, KYC state, holds and operational history. Documents alone do not rebuild them. | External control | F4 | locked | F4 |
| `R-EXT-04` | A recovery test must rebuild one position from retained documents before the recovery claim is accepted. | External control | F5 | locked | F5 |

