# CONTINUE — MVP

> Shape: **Next action · State · Ledger · Blocked**.

**Next action:** carry the generated contract ID through the checkout and sale
record (F1), then connect the local package to the external immutable archive
(F3). The headless document package and final Mulan commercial terms are done.

## State — 2026-11-11

- `MODEL.md` is locked.
- Price, duration and investor return are the three commercial levers.
- Price is retail per 1 horse point per month, with the 5% Evolution margin and
  3% platform fee included.
- Investor return is `eligible gross stakes × investor split × horse points /
  100`; split is explicitly selected from 50–85%.
- Final credited returns and reporting use ceiling rounding to whole NZD.
- Both Upfront and Subscription Float Model are required. Monthly is tested
  first because it carries the deposit, advance, draw-down and default logic.
- The purchase month is pro-rated; subsequent months are whole calendar months.
  Date references use `Mon YYYY`.
- Contract ID is `ES-DSL-YYYY-NNNNNN`.
- The durable document is one immutable combined PDS/SA PDF with an exact-byte
  SHA-256 hash, immutable storage, email attachment, frozen MyStable display and
  a six-field external manifest.
- Supabase owns structured state; Stripe supplies payment/KYC signals; the local
  private vault stores retained investor/KYC/legal evidence; a second immutable
  copy provides durability; email is delivery only.

## Work queue

1. Persist the contract ID through checkout and sale storage (F1).
2. Update the PDS/SA legal copy to match the locked model:
   - full-horse return formula;
   - pro-rata purchase month and `Mon YYYY` references;
   - Subscription Float initial payment and final four-month draw-down;
   - aligned investor declarations;
   - contract ID.
3. Retrieve and verify the current Rules of Racing, including KYC, age,
   declarations, proof-of-address and eligibility requirements.
4. Implement email attachment delivery, frozen MyStable display and the second
   immutable copy.
5. Prove the Subscription Float Model end-to-end first, then the upfront control
   path.
6. Run the seven-step MVP DoD walk and retain the required evidence.

## Review backlog

- [x] Compare the proposed v2 website with production
  `https://evolutionstables.nz/`. Result:
  `audits/V2-VS-PRODUCTION-2026-11-11.md`. Revisit the horse-detail and checkout
  half once one V2 listing is published.
- [x] Review the five-step purchase-flow prototype at
  `sandbox/rebuild/purchase-flow-v2-with-deck.html`. Result:
  `audits/PURCHASE-FLOW-V2-PROTOTYPE-2026-11-11.md`.

## Ledger

| date | what | state |
|---|---|---|
| 2026-11-11 | MVP scope and DoD created | done |
| 2026-11-11 | `MODEL.md` commercial/legal model locked | done |
| 2026-11-11 | Durable sale-record model locked | done |
| 2026-11-11 | Proposed v2 website design review captured | done |
| 2026-11-12 | PDS/SA document-package session DoD locked | done |
| 2026-11-12 | Headless PDS/SA package gate implemented and verified | done |
| 2026-11-12 | Additive expense pricing locked as `ceil(wholesale × 1.08)` | done |
| 2026-11-12 | Voluntary exit, default notice and automatic wind-up restored | done |
| 2026-11-12 | Final Mulan commercials rendered to `ES-DSL-2026-900006` | done |
| 2026-11-12 | wrap — model, legal package and audit evidence committed | done |
| next | persist the contract ID through checkout and sale (F1) | ready |

## Blocked

- **Commercial terms:** final Mulan values are saved: $60 wholesale / $65 retail
  per 1% per month, 75% investor return, 5% listed, 1% minimum, 0.5% steps,
  subscription float, 14-day break, quarterly distributions and Jun 2028 expiry.
- **Legally final documents:** current Rules source is not verified locally and
  the documents still require legal sign-off.
- **KYC evidence:** proof-of-address and NZTR eligibility evidence are not yet
  proven against the current provider flow.
- **Production sale:** durable document path and current legal-copy alignment
  are not implemented.
