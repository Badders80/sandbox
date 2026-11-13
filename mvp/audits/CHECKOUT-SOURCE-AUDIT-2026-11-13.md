# Checkout Source Audit and Source Freeze

**Date:** 2026-11-13
**Status:** LOCKED source boundary
**Scope:** Legacy production checkout, `sandbox/rebuild`, and the current V2
checkout/legal contracts
**Purpose:** Extract only the behaviours and product decisions needed for the
new checkout, then stop treating either old build as an implementation or
content source.

## Verdict

The prototype is the stronger investor-facing journey. Legacy production is the
stronger catalogue of failure and recovery mechanics. `sandbox/rebuild` is not a
source of production code.

The new checkout is therefore rebuilt from the current V2 contracts and design
system. It takes:

- the 0–5 journey and state presentation from the prototype;
- specific recovery and handoff behaviours from legacy production;
- no application code from either old build;
- no legal copy, declarations, prices, sale semantics, fixture data or document
  lifecycle from either old build.

## Evidence Baselines

| Source | Exact baseline | Role |
|---|---|---|
| Legacy production | `origin/main` at `4c1a5c0df77462e3edec7467807d80ebd4843269`, 2026-10-03 | Behavioural evidence only. Local dirty edits on `ci/add-workflow` are excluded. |
| Prototype | `/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html`, 101,690 bytes, 2,591 lines, SHA-256 `8caed0a5308e4699b906cc8387f86a52ed5b76de8ce0f5f99c51d9201308accf` | Journey, layout and state-presentation evidence only |
| Rebuild app | `/home/evo/sandbox/rebuild/src/` | Mock/reference only; no production code reuse |
| Current implementation truth | `engine_v2/website` at `436bd5ff1b237d6d58b8da89e145bde2f30daa92`; feature commit `dbd0184`; migration `00031_checkout_acceptance.sql` | Authority for current quote, acceptance, KYC, payment and sale contracts |
| Locked product/legal model | `sandbox/mvp/MODEL.md`, `SCOPE.md`, `DOD.md`; legal pack `1.0.4` | Authority for commercial, legal and sale semantics |

The prototype folder is ignored by Git. Its HTML hash, not a commit, identifies
the reviewed copy. `purchase-flow-v2.html` and both `.bak` files are not reviewed
sources for the new implementation.

## Hard Cutoff

After this artifact:

1. Legacy production and `sandbox/rebuild` are frozen reference material.
2. New checkout work starts from this audit plus the current V2 contracts.
3. No old React component, HTML, inline JavaScript, fixture, migration guide,
   token package, backup file or mock state hook is copied into V2.
4. Old copy is evidence of intent, never the copy source. Final copy comes from
   the current legal pack and product contract.
5. If a missing fact absolutely requires reopening an old source, record the
   extracted fact and its disposition in this file before implementation.

## Extraction Decision Register

| Candidate | Source evidence | Disposition | New destination / condition |
|---|---|---|---|
| Six investor surfaces: horse-page offer then five popup screens | Prototype lines 1456–1516; legacy production `Step` union at `purchase-flow-modal.tsx:113` | **Accept concept** | Steps 0–5. Step 0 is page context; Step 1 begins the transaction. |
| Screen/branch review deck | Prototype direct step and pass/fail/pending selectors; KYC, payment and confirmation branches | **Accept as QA pattern** | Build a separate state fixture or Storybook-like review surface. Never ship navigation controls as end-user UI. |
| Step 0 offer rail structure | Prototype lines 1757 onward; production `right-rail.tsx:243-333` | **Reimplement from V2 data** | Engine-backed offer, truthful `TBA`/unavailable states, no hardcoded price or return. |
| Step 1 commercial summary and stake choice | Prototype lines 1809 onward; production term sheet | **Reimplement** | Read quote, stake, payment model and term start from the engine. Keep minimum/step as order-book controls. |
| PDS then SA sequential completion | Prototype lines 1900–1988; production lines 771–1140 | **Accept behaviour, reimplement UI** | PDS and SA remain separate controls inside the combined Investor Pack. PDS unlocks SA. |
| Explicit read-to-end affordance | Production “Scroll to read” at line 931 | **Accept concept with stricter contract** | Support natural scroll, keyboard and assistive technology. Programmatic movement must not falsely certify reading. |
| Disabled-reason copy | Production document and KYC beats | **Accept principle** | Every disabled legal or payment control states what must happen next. |
| Seven canonical declarations | Current `engine/src/lib/purchase.ts` and V2 `BuyFlowModal.tsx` | **Current authority wins** | Ignore the prototype and legacy four-declaration lists. Declarations remain inside SA signing. |
| Typed legal-name signature | Current `engineClient.ts` and `purchase.ts` | **Current authority wins** | Require typed name to match account name before continuing. |
| Acceptance persisted before Stripe | Migration `00031`, `record_checkout_acceptance`, `openCheckoutSession` | **Current authority wins** | No Stripe session may bind without immutable PDS/SA acceptance evidence. |
| KYC pass/fail presentation | Prototype lines 1993–2071 | **Accept concept, expand states** | Cover `unverified`, `pending`, `verified`, `failed` plus gate/redirect/return/expired presentation states. |
| Human gate before Stripe Identity | Production `kycVariant='gate'` and explicit proceed action | **Accept** | No automatic redirect merely because the KYC step mounted. |
| Returning verified investor confirmation | Production lines 1719–1811 | **Accept** | Show that identity is already on file and require an explicit “this is me” confirmation. |
| Pending is not failure | Production KYC return logic and V2 MyStable pending state | **Accept** | A Stripe return or delayed webhook must never be described as a failed check or completed sale. |
| One retry, no KYC loop | Production `kycRetry` guard | **Accept** | A checkout `KYC_REQUIRED` response may re-enter identity once, then show a recoverable failure state. |
| Payment summary before hosted Stripe | Prototype lines 2075–2147; production payment gate | **Accept layout concept** | Repeat the engine quote and require human consent before redirecting. |
| Double-submit guards | Production `checkoutStarted` and `paymentStarted` refs | **Accept behaviour** | Encode as typed transition guards and test rapid repeated actions. |
| Fresh Stripe session on retry | Production `proceedToPayment` / `handOffToCheckout` | **Accept** | Retry must not reuse a completed or expired session. |
| Redirect fallback | Production redirect grace timer | **Accept** | If navigation fails, return the buyer to a usable gate rather than a trapped spinner. |
| Confirmation anatomy | Prototype lines 2149–2222 | **Accept layout concept** | Pending-first until the sale row exists. Then show contract, holding, payment, pack and delivery status. |
| Premature “ownership active” on return | Production `?checkout=success` confirmation effect at line 1406; rebuild `Step5Confirm` | **Reject** | Ownership begins only after the webhook writes the sale. Use V2 pending-until-sale behaviour. |
| Hosted Stripe Checkout | Current V2 purchase contract | **Current authority wins** | No in-modal payment element, Apple Pay/Google Pay claim, or client payment credentials. |
| URL-driven open and resume context | Production `purchase-flow-host.tsx` | **Accept concept** | Persist open state, selected stake and return context so login, refresh and KYC return do not lose the buyer's place. |
| Account gate at purchase intent | Production `purchase-flow-host.tsx` | **Accept concept** | Require account before signed legal documents are compiled, while keeping the horse page public. |
| Fixed 900px modal | Legacy production shell | **Reject** | Use responsive desktop dialog and mobile drawer without clipping content or controls. |
| Prototype mobile drawer | Prototype viewport modes | **Reference only** | It is a scaled presentation, not responsive proof. Implement with V2 responsive primitives. |
| Prototype token values | Prototype CSS variables and inline styles | **Reject as authority** | V2 design tokens own colour, typography, spacing, motion and radii. |
| Rebuild component architecture | `sandbox/rebuild/src/components/purchase/` | **Reference concept only** | Keep step separation and a headless state model; do not port the mock hook or components. |
| Rebuild fixture and mock timers | `usePurchaseFlow.ts` | **Reject** | `setTimeout` identity and payment simulations are not production behaviour. |
| Rebuild pricing functions | `sandbox/rebuild/src/lib/pricing.ts` | **Reject** | Current engine pricing owns quote and sale-time calculations. |
| Old legal copy and PDS/SA download links | Legacy production and rebuild | **Reject as source** | Current legal pack `1.0.4` and templates own content. The product artifact is the combined Investor Pack. |
| Old declarations and checkbox-only signing | Legacy production and rebuild | **Reject** | Superseded by seven declarations plus typed legal-name signature. |
| Hardcoded horse, price, term and contract values | Prototype and rebuild fixtures | **Reject** | Read from the engine and frozen sale snapshot; use `ES-DSL-YYYY-NNNNNN`. |
| Migration plans, `.bak` files and old token audit as active instructions | `sandbox/rebuild/MIGRATION-*`, `*.bak*`, old token notes | **Reject** | Historical only. Current contracts and this audit supersede them. |

## Required State Spine

This is the extraction the next session should refine, not rediscover.

### Step 0 — Offer

Required presentation states:

- available and buyable;
- coming soon or not yet priced;
- fully allocated;
- closed or unavailable;
- offer data failed to load.

Step 0 is not a checkout transaction state. It owns discovery, truthful pricing
disclosure, offer availability and the entry action.

### Step 1 — Terms

Required presentation states:

- quote loading;
- quote valid;
- stake adjusted;
- quote expired or listing changed;
- login required;
- documents failed to compile.

### Step 2 — Investor Pack

Required presentation states:

- PDS not started;
- PDS reading;
- PDS complete;
- SA locked;
- SA reading;
- declarations incomplete;
- typed name mismatch;
- acceptance ready;
- acceptance saving;
- acceptance saved;
- document version changed and re-acceptance required.

The control path is:

`PDS end -> PDS acceptance -> SA end -> seven declarations -> typed full legal
name -> final signing action -> immutable acceptance evidence`

### Step 3 — Identity

Required states:

- unverified;
- identity gate shown;
- redirecting to Stripe Identity;
- pending;
- verified;
- returning verified, awaiting identity confirmation;
- failed or requires input;
- retry already used;
- session expired.

### Step 4 — Payment

Required states:

- payment gate ready;
- checkout session creating;
- redirecting to hosted Stripe;
- cancelled;
- failed;
- payment submitted but webhook not yet processed;
- paid but sale is `paid_unfulfilled`.

Acceptance evidence must already be saved before this step can create a Stripe
session.

### Step 5 — Settlement and Delivery

Required states:

- confirming payment;
- webhook pending;
- sale written;
- executed Investor Pack generating;
- executed Investor Pack ready;
- email delivery pending or failed;
- proof of address pending;
- complete;
- operator recovery required.

No surface may say ownership is active until the sale row exists.

## Zero-Debt Rules

1. **No code transplant.** Old source contributes a named behaviour, not a
   component, hook, stylesheet or state object.
2. **One state vocabulary.** UI labels map to typed states backed by the engine,
   Stripe flow or an explicitly documented presentation timer.
3. **One content authority.** Legal text, declarations, hashes, prices, term
   dates and contract IDs come from current locked sources.
4. **One sale truth.** Pending remains pending until the webhook writes the sale.
   Email delivery does not prove the sale; the sale plus immutable evidence does.
5. **No duplicate acceptance paths.** The final signing action records the
   evidence once. KYC and payment reuse it and cannot rewrite it.
6. **No inaccessible proof.** Touch, keyboard, screen-reader and reduced-motion
   paths must reach the same legal endpoint without a scroll trap.
7. **No dead QA-only code in production.** Step selectors, branch selectors,
   reset controls and mock states live in a separate review surface.
8. **No legacy dependency.** V2 must not import from the legacy website,
   `sandbox/rebuild`, old flow mockups or rebuild fixtures.
9. **No unowned retention.** Every extracted behaviour must appear in the state
   specification and have a test or an explicit manual-check owner.
10. **No silent fallback.** Missing price, return, offer, quote or document data
    produces an honest unavailable state, never invented data.

## Implementation Boundary

New implementation evidence:

- `engine_v2/website/website/src/components/BuyFlowModal.tsx`
- `engine_v2/website/website/src/lib/engineClient.ts`
- `engine_v2/website/engine/src/lib/purchase.ts`
- `engine_v2/website/engine/src/lib/purchaseStore.ts`
- `engine_v2/website/supabase/migrations/00031_checkout_acceptance.sql`
- `engine_v2/website/engine/src/templates/PDS.template.md`
- `engine_v2/website/engine/src/templates/SA.template.md`
- `sandbox/mvp/MODEL.md`
- `sandbox/mvp/SCOPE.md`
- `sandbox/mvp/DOD.md`
- this artifact

Frozen inputs, not implementation sources:

- `evolution/engine/website` legacy production checkout;
- `sandbox/rebuild`;
- prior migration plans;
- prior prototype and polish audits.

## Next-Session Entry Rule

The checkout scroll-mapping session must begin with this artifact and the current
V2 contracts. It must not browse the legacy or rebuild implementations again to
reconstruct requirements. Its output is the final screen/state map and scroll
unlock contract, not another source inventory.

## Open Risks Carried Forward

- Current Rules of Racing verification and Evolution-to-Investor legal sign-off
  remain open.
- KYC evidence and proof-of-address handling remain unproven against the current
  provider flow.
- Production-sale authority remains blocked.
- Owner-to-Evolution authority remains an external publish-time assumption.

These are not debt inherited from the old builds. They are current product
blockers and remain visible.
