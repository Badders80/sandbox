# DSL Stake Model

**Status:** LOCKED 2026-11-11.

This document defines the stake and the commercial model. It is not legal
prose, an implementation plan, or a replacement for the executed PDS and SA.

## Root requirement

> An eligible investor can digitally buy a fractional leasehold interest in an
> NZTR-registered horse, offered by Evolution Stables as an authorised
> syndicator acting for the owner, in compliance with the Rules of Racing, and
> receive a durable record of that interest.

A **stake** is one purchasable unit of that fractional leasehold interest.

## What a stake is

- **Commercial unit:** a horse percentage point measured against the full
  horse (100 points). A 5-point listing contains five points; an investor who
  buys one of them holds 1 point, not 20% of the listing.
- **Legal interest:** a fixed-term fractional leasehold share governed by the
  PDS, SA, and Rules of Racing. It is not equity in the horse or an unrestricted
  public security.
- **Completed sale:** the investor is eligible, has accepted the PDS and SA and
  required declarations, has satisfied KYC, has paid, and has a recorded sale
  with a durable document.
- **External input:** acquisition of the owner-to-Evolution interest is outside
  this system. Listing assumes an authorised stake is already available.

For investor-facing documents, **one horse point is equivalently described as
a 1% stake**. “Stake percentage” and “shares of 0.5%” are approved wording.
The legal documents define this equivalence once and use the full-horse
100-point denominator in the investor-return formula.

Minimum investment and purchase increment are order-book controls. They
constrain which purchase quantities are available, but do not redefine the
stake, the pricing unit or the full-horse denominator. A purchase must meet the
minimum and be a whole multiple of the increment.

The public offer shows:

- the horse and the total DSL stake being offered, such as 5% or 10% of the
  horse;
- the retail price per 1 horse point per month;
- the duration or fixed expiry;
- the selected investor-return split; and
- the stake quantities the investor is permitted to select.

## The three commercial levers

The model is controlled by three variables. Payment schedule and fees are
mechanics around those variables, not additional economic levers.

| Lever | Definition |
|---|---|
| **Price** | NZD value to buy one horse point for one calendar month. |
| **Duration** | Remaining inclusive calendar months between the sale month and the listing's fixed expiry. |
| **Investor return** | The investor's share of eligible gross stakes won, selected by the owner within the permitted range. |

The investor sees only the retail price. Evolution's revenue model is disclosed
in the PDS and SA and is bundled into that retail price:

- 5% Evolution Stables syndication-management margin.
- 3% platform fee, retained by Evolution to cover payment processing and
  related administrative costs.

The retail price per 1 horse point per month is:

```text
ceil(wholesale × (1 + Σ expense rates))
```

Expense rates are additive against wholesale and are never compounded onto one
another. With the current rates:

```text
expense uplift = 5% Evolution margin + 3% platform fee = 8%
retail = ceil(wholesale × 1.08)
```

If another expense is introduced later, its rate is added to the same sum. It is
still measured against wholesale, not against wholesale plus a prior expense
uplift. For example, adding 2% produces `ceil(wholesale × 1.10)`.

There are no separate management invoices.

### Price

Price is always quoted per 1 horse point per month.

Contract price is proportional to:

```text
purchased horse points × monthly price per point × chargeable months
```

The purchase month is chargeable pro rata. Every month after it is chargeable
as a whole calendar month.

### Duration

- A listing carries a fixed expiry month and year.
- The purchase month is partial. Its charge is the monthly rate multiplied by
  the remaining days from the purchase date through month-end, divided by the
  total days in that month. The purchase date is treated as a billable day.
- Every month after the purchase month is charged as a whole calendar month,
  beginning on the first and ending on the last day.
- The contract ends at the end of the fixed expiry month.
- Dates and expiry are referenced as `Mon YYYY`, such as `Jun 2028`, rather
  than by a specific day. The legal documents should state that a month means
  the whole calendar month.

### Investor return

The investor-return percentage is selected per listing within the advised range
of 50–85%. The recommended starting point is 75%, but 75% is not a default.

```text
investor return =
  eligible gross stakes
  × (investor split / 100)
  × (purchased horse points / 100)
```

For a 75% split and a 1-point holding:

```text
investor return = eligible gross stakes × 0.75 × 0.01
```

For a 2.5-point holding and a 75% split:

```text
$100 × (2.5 / 100) × 0.75 = $1.875
```

Eligible gross stakes means the official gross stakes won by the horse during
the investor's eligible participation period, subject to any fully-paid-up
qualification period in the PDS and SA.

The Prudentia reports evidence the underlying mechanics:

- Q2 2026: `$25,150 × 0.75 × 0.01 = $188.625`.
- Q3 2026: `$525 × 0.75 × 0.01 = $3.9375`.

The cent values printed in those reports were an error. Tokinvest, AED and
per-token reporting are not part of the current model. The final credited
distribution and all investor reporting are rounded up to the next whole NZD:

```text
final amount = ceil(exact investor return)
```

If the final amount contains decimals, it moves to the next whole dollar. An
amount already expressed in whole dollars is unchanged. This is an internal
calculation and display protocol; the legal documents do not need to describe
the rounding mechanic.

## Payment models

Payment timing does not change the purchased points, duration, or return rate.

### Upfront

The full amount is paid once at purchase, regardless of contract duration.
There are no subsequent charges.

Once the monthly pricing model is implemented, upfront requires no separate
economic model: the same monthly rate and term are priced once and collected in
full.

### Subscription Float Model

- Initial payment: three-month deposit reserve, one month in advance, and the
  pro-rata balance of the purchase month.
- Subsequent payments: the first day of each calendar month after join.
- The four non-current months in the initial payment cover the final four
  months of the contract: three deposit months plus one advance month.
- The initial-payment balance is drawn down over those final four months and
  must equal zero at expiry.
- A missed payment pauses distributions.
- If the outstanding balance is not cleared before the next billing cycle, the
  stake and deposit are forfeited to the owner. Evolution retains no benefit.

The monthly model is core to the product and is required for the first-sale
critical path. It must be tested first because it carries the deposit,
advance-payment, billing, draw-down and default complexity. Upfront remains
required and provides the simpler control case.

Payment model is a founder-gated listing decision. If the remaining duration
cannot support monthly payments after the initial payment, the offer is listed
as upfront. This is decided at listing readiness, not converted automatically
at checkout.

## Voluntary exit, default and expiry

### Voluntary Investor Exit

- The account must have no arrears before notice is accepted.
- Voluntary exit is available only when at least five full calendar months
  remain after the month in which notice is given.
- The investor must make the scheduled payment due on the next 1st.
- After that payment, recurring billing stops.
- The one-month advance and three-month deposit reserve are applied at the
  monthly rate over the following four months.
- The investor retains participation and distribution rights throughout the
  five-month wind-down. Winnings are distributed normally.
- The stake and account end with a zero balance at the end of the fifth month.
- If fewer than five full calendar months remain, voluntary exit is unavailable
  and participation continues to the fixed expiry.

### Default

- A default process begins when the scheduled payment due on the 1st is missed.
- Evolution Stables sends recorded written notice during that month.
- The investor may cure by the end of that month.
- If the account is not restored, default takes effect on the 1st of the next
  month.
- Already earned but unpaid winnings in the account are distributed to the
  investor.
- The three-month deposit reserve and the stake are forfeited to the owner.
- The investor's future distribution and ownership rights cease from the
  default date.

### Fixed expiry

At the fixed expiry, the syndicate is automatically wound up. The lease does not
roll over unless the manager offers a renewal and the participant opts into new
terms. Post-racing arrangements remain the responsibility of the horse's
connections and must comply with NZTR welfare requirements.

## Durable sale record — LOCKED 2026-11-11

**Contract ID:** LOCKED 2026-11-11 as `ES-DSL-YYYY-NNNNNN`.

The sale record should make the document, sale and money point to each other:

- Generate a stable, unique contract ID before rendering and print it in both
  the PDS and SA. Do not derive it from mutable horse names or buyer details.
- Compile the PDS and SA from the frozen sale snapshot and combine them into one
  PDF.
- Store the SHA-256 hash of the exact combined PDF bytes on the sale. Store the
  template versions and sale snapshot identifiers with it.
- Store the PDF in immutable object storage and record its object key on the
  sale.
- Email the exact PDF as an attachment. Include the contract ID and document
  hash in the email body.
- Serve the exact stored bytes from MyStable. Never recompile a document for
  historical display.
- Write the contract ID, sale ID, hash, object key, template versions and
  creation time to an external archive manifest. Use the sale and contract IDs
  as the linkage; do not duplicate investor identity data in the manifest.

The immutable executed PDF necessarily contains the investor's personal data
because it is their contract. That exact PDF is retained. KYC evidence, contact
details and other identity records remain in their controlled operational store
and are linked by the sale or contract ID rather than copied into the external
manifest.

The external archive manifest contains exactly:

- `contract_id`
- `sale_id`
- PDF SHA-256 hash
- object key
- template versions
- creation timestamp

## Provider and storage split — LOCKED 2026-11-11

- **Supabase:** structured operational authority for parties, horses, trainers,
  DSL offers, reservations, sales, ledger entries, eligibility state,
  acceptance metadata and document pointers.
- **Stripe:** payment processing and a KYC identity signal. Stripe verification
  is an input to eligibility, not a complete NZTR compliance decision.
- **Local private vault:** server-only storage on local ext4 for retained
  investor records, KYC evidence where legally retained, accepted declarations,
  and the exact executed PDS/SA PDFs. Directories are keyed by opaque account
  and contract IDs, never by investor names.
- **Immutable second copy:** exact document bytes and the manifest mirrored to a
  separate non-overwriting location. A mutable local filesystem is not, by
  itself, WORM storage.
- **Cloudflare R2:** media and other non-legal binary assets by default. It may
  hold a private backup copy of legal documents, but sensitive documents never
  go through the public media path.
- **Email:** delivery channel only. The sale is proven by the stored sale,
  acceptance record, document bytes and hash, not by delivery of an email.

KYC evidence and executed legal documents should be stored in separately
permissioned vault areas and linked through the account, sale and contract IDs.

## Investor eligibility and declarations

These are legal obligations and remain in scope:

- investor is at least 18 years old;
- AML/CFT consent and identity verification;
- identity and proof-of-address evidence as required;
- investor is not disqualified, excluded, or banned under the Rules of Racing;
- investor acquires as true beneficial owner;
- investor accepts the Rules of Racing and Welfare Guidelines;
- investor acknowledges Evolution Stables as manager;
- investor receives and electronically accepts the PDS and SA.

KYC provider choice and UI workflow are implementation details. Stripe Identity
is the current provider, not the legal requirement itself. Its current
document-only flow has not been verified as satisfying every proof-of-address
and NZTR eligibility obligation.

## MVP take-list

### System capabilities to retain

- One horse, one offer, and one public sale page.
- Horse points, minimum, increment, price, investor split, expiry, and
  remaining inventory.
- PDS/SA compilation with aligned declarations and an explicit return formula.
- Eligibility and electronic acceptance gate.
- Checkout reservation and no-oversell enforcement.
- One compliant payment path.
- Atomic, idempotent sale with an immutable sale snapshot.
- A ledger that agrees with held, sold, and remaining points.
- Combined PDS/SA PDF, both hashes, attachment delivery, and frozen-byte
  retrieval.
- Recorded handling for paid-but-unfulfilled exceptions.

### Manual controls

- Owner-to-Evolution acquisition evidence.
- Current Rules of Racing retrieval and legal sign-off.
- Pilot investor identity, proof-of-address, and eligibility evidence.
- Horse-wide external capacity check.
- Refunds, defaults, and term closure.
- External document archive plus manifest.
- Database backup and one recorded restore check.

## Not in the MVP

- Acquisition, owner onboarding, or horse-wide deal management.
- Multiple horses, owners, or trainers beyond the pilot needs.
- Content wizard, broad admin screens, filters, and bulk operations.
- Media/studio pipeline, generated assets, and rename handling.
- Automated multi-DSL capacity or an automatic horse-wide cap.
- Automated monthly billing, dunning, payouts, or default engine.
- Archive automation and recovery drills before the first sale.
- Public self-service beyond buying.

## Existing-work reconciliation

The existing PDS/SA, rulebook, pricing, term, purchase, reservation, ledger, and
legal compiler are substantially reusable.

The following must be corrected or explicitly accepted before a compliant sale:

1. The PDS and SA must print the return formula and state that the denominator
   is the full 100-point horse.
2. PDS declarations, SA Schedule 2, and checkout declarations must be aligned.
3. The current Rules of Racing must be retrieved, dated, and checked.
4. Identity, proof-of-address, and NZTR disqualification evidence must be
   verified or handled by a recorded manual control.
5. A stable contract ID must be printed and indexed.
6. PDS/SA must explain the pro-rata purchase month and whole-month references
   using `Mon YYYY`.
7. The combined PDF, email attachment, frozen-byte MyStable display, and
   external archive must exist before the first sale.
8. Subscription Float legal copy must state that the retained four months cover
   the last four months and that the balance reaches zero at expiry.
9. The link-only email wording in `O-02` must be corrected. Investor-facing
   percentage language is approved because one horse point equals a 1% stake;
   the legal documents must define that equivalence and the 100-point
   denominator.
10. The database reservation path does not currently evidence minimum/step
    enforcement; TypeScript currently owns that check.

## Review decisions

These are decisions, not implementation choices:

1. ~~Confirm the 5% + 3% price derivation or replace it.~~ **LOCKED
   2026-11-12:** investors see retail only; the 5% Evolution margin and 3%
   platform fee are additive rates against wholesale (`×1.08` total), not
   compounding multipliers. Future expense rates join the same sum.
2. ~~Confirm whether ceiling-to-whole-NZD applies to the credited distribution
   as well as reporting.~~ **LOCKED 2026-11-11:** both the final credited amount
   and reporting use ceiling rounding to whole NZD.
3. ~~Decide whether the first pilot supports monthly payment or is
   upfront-only.~~ **LOCKED 2026-11-11:** both are required for the first sale;
   monthly is core and must be tested first, while upfront is the simpler
   control case.
4. ~~Confirm tenant-in-common wording after checking current legal advice and
   the Rules of Racing.~~ **DROPPED 2026-11-11:** safe to ignore for this model.

## Sources

- `sandbox/mvp/README.md`
- `sandbox/mvp/SCOPE.md`
- `sandbox/mvp/DOD.md`
- `sandbox/v2/rulebook/RULES.md`
- `sandbox/v2/rulebook/OPEN.md`
- `evolution/engine_v2/website/engine/src/templates/PDS.template.md`
- `evolution/engine_v2/website/engine/src/templates/SA.template.md`
- Prudentia Q2 and Q3 2026 quarterly investor reports
