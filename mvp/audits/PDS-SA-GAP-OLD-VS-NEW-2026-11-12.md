# PDS/SA gap analysis — old test trade vs new package

**Old PDS:** `/mnt/c/Users/Evo/Downloads/mulan-the-brave-pds-fbd0ba0c (2).pdf`  
**Old SA:** `/mnt/c/Users/Evo/Downloads/mulan-the-brave-sa-a31a955c (1).pdf`  
**New package:** `/home/evo/sandbox/mvp/out/legal/ES-DSL-2026-900005/contract.pdf`  
**Date:** 2026-11-12

## Improvements in the new package

- Correct horse identity: Mulan The Brave (NZ) replaces the stale Turn Me Loose x Yearn 2023 name.
- Current commercial terms: $60 wholesale, $65 retail, 75%, 5% offered, 1% minimum, 0.5% increments, subscription float, 14-day break, quarterly distributions, Jun 2028 expiry.
- Stable contract ID in both documents.
- One combined PDF instead of separate PDS and SA files.
- Exact PDF hash, rendered PDS/SA hashes and eight source-template hashes in a local manifest.
- GST-inclusive disclosure.
- Additive expense pricing: 5% + 3% against wholesale, multiplier 1.08.
- Owner/trainer identity is current and explicit.
- 14-day break appears in both PDS and SA.
- Full 18+, disqualification and leasehold declarations are present.

## Must-fix mismatches against the locked model

### 1. Horse-point terminology — resolved by founder

The founder confirmed that `1% stake`, `Stake Percentage`, `shares of 0.5%`
and `per 1%` are intentional investor-facing language. One horse point equals a
1% stake. The documents should define the 100-point denominator once for the
return formula rather than remove the percentage wording.

Required: define that one horse point equals a 1% stake and state the
100-point full-horse denominator once in the return formula.

### 2. Return formula is still missing

The new documents say 75% is distributed pro-rata but do not print:

```text
eligible gross stakes × investor split × purchased horse points / 100
```

The denominator of 100 and the 25-point owner retention should be explicit.

### 3. Pro-rata purchase month is not implemented or disclosed

The locked model says the purchase month is charged pro-rata from the purchase date through month-end and later months are whole months. The new package uses a `2026-11-01` term start, a full 20-month term and a full five-month initial payment (`$325` at 1 point / $65), with no pro-rata purchase-month amount.

This is both a pricing-code gap and a legal-copy gap. The code, quote, checkout snapshot, sale snapshot and PDF must agree on whether the first month is pro-rata.

### 4. Legal dates still use ISO days

The new PDS/SA print `2026-11-01` and `2028-06-30`. The locked model requires `Mon YYYY` references in legal documents, with the full-month meaning defined in prose.

### 5. Acceptance evidence disappeared from the document

The old PDFs printed an `accepted` timestamp on every page. The new PDF prints only execution date and has no acceptance timestamp. Current checkout acceptance is validated as booleans/declarations but no PDS acceptance time, SA acceptance time or declarations acceptance time is persisted.

Required before a real sale: persist immutable acceptance evidence and decide whether it is printed into the executed PDF, represented in a companion receipt, or both.

## High-priority legal/operational gaps

### 6. Proof of address is stronger than the verified provider flow

Schedule 2 says each shareholder has provided verified proof of address. The current Stripe document-identity flow has not been proven to collect or validate acceptable proof of address.

Either add a verified proof-of-address step or change the declaration and manually record the missing evidence.

### 7. Old investor exit right — corrected 2026-11-12

The old PDS allowed an investor to give notice before the next installment and wind down through the 3+2 balance. The new PDS has no investor exit right; its `Exit` section contains only the owner break and default forfeiture.

Restored as a five-month runway: the next scheduled payment plus four
reserve-funded months. It is available only with no arrears and at least five
full future calendar months.

### 8. Default notice — corrected 2026-11-12

The old PDS/SA said Evolution would notify during default. The new documents move directly from missed payment to paused distributions and forfeiture if not cleared before the next billing cycle.

Restored: recorded written notice during the missed month, cure by month-end,
default on the next 1st, accrued unpaid winnings paid, then reserve and stake
forfeited.

### 9. Distribution payment timing is missing

The old SA promised payment within 14 business days of receipt. The new SA says distributions are remitted but sets no timeframe. The old phrase is currently banned from the corpus.

Define an honest replacement, for example a calendar-day commitment after reconciliation.

### 10. NZTR data-sharing consent was removed

The old PDS declaration included consent to provide the investor's details to NZTR and Evolution for AML/CFT, registration and regulatory purposes. The new declaration only mentions consent to identity verification.

Add the NZTR/regulatory disclosure consent if it remains legally required.

## Medium-priority clarity gaps

- Restored: automatic wind-up, no rollover and post-lease welfare arrangement.
- The old SA gave the actual number of automated payments and last payment date. The new Schedule 1 gives term and start/end dates but not the remaining instalment count or final instalment date.
- The new SA notice clause says notices go to Evolution Stables Ltd but gives no address or email.
- The old PDS said no mortality insurance was secured. The new PDS/SA say insurance is at owner discretion and leaseholders receive no proceeds, but do not state whether a policy exists.
- The new SA relies on electronic acceptance without a signature line. This is acceptable only if the missing acceptance evidence above is retained.

## Old-document defects not to copy

- Old PDS body used the retired horse name and campaign slug.
- Old PDS Investment Details were not filled in.
- Old PDS and SA were accepted at different times as separate files.
- Old SA described 0.1% shares and a $7 monthly slice; those terms are superseded.
- Old insurance wording contradicted itself between PDS and SA.
- Old PDF footers showed only a truncated hash.

## Unclear decisions for the founder/legal review

1. Is investor-initiated exit intentionally removed?
2. Is default forfeiture allowed without notice or a cure letter?
3. What replaces the old 14-business-day distribution promise?
4. Is NZTR data-sharing consent required?
5. Is proof of address mandatory before the first sale?
6. Does any insurance policy currently exist, or should the documents say none is secured?
7. Should acceptance timestamps appear in the PDF or only in a separate immutable acceptance record?
