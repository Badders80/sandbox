# Purchase Flow V2 Prototype Reference

**Date:** 2026-11-11  
**Source:** `/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html`  
**Status:** useful interaction blueprint, not production code or current commercial truth

## What It Is

A 2,591-line interactive HTML deck mapping a five-step purchase flow:

1. Marketplace rail and offer summary.
2. Investment terms and stake stepper.
3. Sequential PDS and SA review and acceptance.
4. Stripe Identity/KYC gate.
5. Stripe payment and settlement.
6. Confirmation and MyStable handoff.

The deck includes KYC pass/fail, payment settled/cancelled, and confirmation
active/pending branches.

## Strong Reference Material to Keep

### Five-step workflow

The ordering is clear and worth preserving as the basis for the later V2
purchase implementation:

`offer → terms → legal documents → eligibility/KYC → payment → proof/confirmation`

### Explicit state matrix

The prototype demonstrates these required branches:

- KYC pass and rejected/failed;
- payment settled and cancelled/declined;
- confirmation active and pending/delayed.

This is useful as the initial test/state checklist for the production flow.

### Sequential document gate

- PDS is reviewed and accepted first.
- SA remains locked until the PDS is complete.
- Payment cannot continue until both documents are accepted.

Keep the underlying rule, but implement it with accessible semantic controls and
the immutable acceptance evidence from `MODEL.md`.

### Clear settlement summary

The payment state separates:

- amount due today;
- recurring monthly amount;
- payment provider;
- success, failure and retry paths.

The structure is useful; the amounts and copy must be replaced with the locked
commercial model.

### Confirmation record

The confirmation state shows the right conceptual components:

- contract reference;
- investor holding;
- identity verification status;
- payment status;
- final ownership status;
- PDF/document access;
- MyStable handoff.

Use this as the basis for the durable-record and confirmation screen.

### Content deck concept

The deck groups copy by step, role and state. That is useful for:

- preventing copy drift between normal/error/pending states;
- reviewing all wording without walking the whole flow;
- exporting a copy proposal for implementation.

It is not yet authoritative because the live flow templates contain separate
hardcoded copy. In production, one state/copy model should drive both the flow
and the deck.

### Scenario and viewport tooling

Useful review tools worth carrying conceptually:

- direct navigation to every step;
- branch selectors for success/failure/pending states;
- Reset State;
- desktop, mobile-drawer and dual-view previews;
- visible context label for the current surface.

These are design/QA aids, not end-user features.

## What Not to Port Directly

- The single 2,591-line HTML implementation or its inline JavaScript patterns.
- Hardcoded Mulan/Stephen Gray data and `Jun 2028` values.
- Hardcoded contract reference `#EVO-2026-0884`; use
  `ES-DSL-YYYY-NNNNNN` from the locked model.
- Old float arithmetic and copy such as "5x float", "3-month deposit reserve &
  2 initial billing cycles", and an unapplied pro-rata purchase month.
- Prominent minimum/maximum stake treatment. These are order-book controls in
  the current model, not the core public offer.
- `Subscription` terminology until it is mapped deliberately to the locked
  Subscription Float Model naming.
- Clickable `div`/`p` elements for Close, Back and document headers.
- The `28×18px` stake stepper, `36px` close control and other undersized targets.
- The mobile drawer as proof of production responsiveness; it is a scaled
  preview mode, not the real mobile component.
- The separate copy deck as an alternate source of truth.

## Detector Findings

The Impeccable detector returned 24 warnings/advisories. The material findings
were:

- repeated low-contrast secondary text;
- 9–11px functional labels and body copy;
- undersized interactive controls;
- dark glow effects.

Some font and decorative-grid findings are false positives because the prototype
intentionally reproduces a fixed reference style. The contrast, sizing and
semantic-control issues still need correction in production.

## How to Reuse It Later

Use this prototype as:

1. The source for the production purchase-state matrix.
2. A checklist for success, failure, pending and recovery states.
3. A reference for the confirmation record layout.
4. A reference for copy governance by role/state.
5. A design QA pattern for stepping through every branch.

Do not use it as:

- the commercial source of truth;
- production component code;
- legal-document evidence;
- responsive-mobile proof;
- the copy SSOT.

## Recommended Follow-Up

When website implementation resumes, extract a state table with one row per:

`step → state → trigger → data required → server result → UI copy → recovery action → test/evidence`

Then rebuild the flow with V2 components and `MODEL.md`, using this prototype
only as the behavioural reference.
