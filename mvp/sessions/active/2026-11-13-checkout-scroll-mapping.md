# Next Session Plan — Checkout Workflow and Scroll Gating

**Status:** READY
**Created:** 2026-11-13
**Owning code repo:** `/home/evo/evolution/engine_v2/website`
**Owning planning repo:** `/home/evo/sandbox` (`mvp/` is inside this repo)

## Outcome

Review `/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html` as an
interaction reference, map its steps to the current checkout contracts, and
define exactly where the PDS/SA scroll locks, declarations, typed signature,
KYC, payment, executed Investor Pack and proof-of-address request sit.

This is a checkout-workflow session. It must preserve the legal and acceptance
foundation now committed below; it does not reopen legal copy unless a real
contradiction is found.

## Current Baseline

- Legal pack `1.0.4`; current Mulan proof:
  `/home/evo/sandbox/mvp/out/legal/ES-DSL-2026-900018/contract.pdf` (15 pages).
- Investor Pack = PDS + SA. Declarations live inside the SA signing flow; there
  is no third declaration document.
- Seven canonical declarations are shared by the SA, engine validator and
  checkout UI.
- Typed legal name is required in the checkout and must match the account name
  in the browser gate; the database enforces the same match before Stripe binds.
- Checkout sessions persist PDS/SA acceptance timestamps, declaration snapshot,
  typed signature and acceptance time. The evidence is immutable.
- Migration `00031_checkout_acceptance.sql` prevents Stripe from binding before
  acceptance and preserves the checkout-to-sale link through
  `checkout_session_id`.
- Feature commit: `dbd0184` on `dsl-sidequest`.
- Gate at wrap: `pnpm verify` exit 0; engine 402 passed / 1 skipped; website 64
  passed; both builds. `just verify-db` PASS at schema `00031`.
- Proof of address is manual and remains `pending` until an operator records
  the external evidence.

## Read First

1. `/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html`
2. `/home/evo/sandbox/mvp/CONTINUE.md`
3. `/home/evo/sandbox/mvp/DOD.md`
4. `/home/evo/sandbox/mvp/SCOPE.md`
5. `/home/evo/sandbox/mvp/MODEL.md`
6. `/home/evo/evolution/engine_v2/website/website/src/components/BuyFlowModal.tsx`
7. `/home/evo/evolution/engine_v2/website/engine/src/lib/purchase.ts`
8. `/home/evo/evolution/engine_v2/website/supabase/migrations/00031_checkout_acceptance.sql`

## Required Review

Produce a screen-by-screen and state-by-state map of the prototype HTML:

- current step order and navigation;
- every state transition and where state is held;
- which copy/layout is reference material and which is implementation truth;
- where the PDS and SA are displayed;
- where scroll progress can be measured reliably on desktop and mobile;
- how keyboard and assistive-technology users reach the scroll endpoint;
- when acceptance and signature controls become enabled;
- what happens to the current checkout if the user navigates back or refreshes.

## Scroll-Gating Contract To Define

The next session must lock:

1. The PDS checkbox/control remains disabled until the PDS content reaches its
   end.
2. The SA acceptance, declarations and typed signature remain disabled until
   the SA content reaches its end.
3. Short content that does not need scrolling is treated as complete without a
   false scroll requirement.
4. Keyboard, touch and reduced-motion paths work without trapping the user.
5. The UI retains a clear reason the control is disabled.
6. Acceptance is recorded only after the final signing action, not merely on
   reaching the bottom.

## Workflow Contract To Map

Use this sequence as the candidate contract; correct it only if the HTML exposes
a concrete conflict:

1. Review unsigned Investor Pack.
2. Scroll/read PDS; accept PDS.
3. Scroll/read SA; tick declarations; type full legal name.
4. Continue to KYC.
5. Payment.
6. Webhook writes the sale.
7. Generate and freeze the executed Investor Pack after the sale.
8. Email the executed pack with ownership confirmation and proof-of-address
   request.
9. Proof of address remains `pending` for manual external handling.

The session must identify the exact UI and engine/API changes needed to support
this sequence without changing the accepted legal-content hashes.

## Required Deliverables

- Prototype screen/state inventory with file/line references.
- Mapping table: prototype step → current repository behavior → required change.
- Final scroll-unlock specification for PDS and SA.
- Final acceptance/signature payload contract.
- Executed-pack generation and storage timing.
- Post-sale email attachment and proof-of-address request contract.
- Current/next-month term-start mapping, kept separate from executed date.
- Test plan covering browser behavior, API payloads, sale snapshots and email.
- A short implementation sequence with one merge gate.

## Definition of Done

1. Founder accepts the screen/state mapping.
2. PDS/SA scroll behavior is specified for desktop, mobile, keyboard and short
   documents.
3. The acceptance and typed-signature contract matches the existing API and
   database evidence.
4. The post-sale executed-pack/email sequence is specified and linked to the
   frozen sale.
5. Contract ID and selected term start are carried through quote, documents,
   checkout and sale.
6. No legal-copy hash changes unless a documented contradiction requires one.
7. The implementation plan names its gate before coding begins.

## Out of Scope

- reopening the locked commercial model;
- Owner-to-Evolution upstream authority;
- current Rules of Racing verification and final legal sign-off;
- producing a real sale or publishing Mulan;
- redesigning Marketplace or MyStable;
- a third declaration document;
- automated proof-of-address upload.

## Starting Location

Use a clean worktree from local `dsl-sidequest` after this wrap commit. Do not
work in the shared checkout while `engine/tsconfig.json` and
`website/.impeccable/` remain unrelated dirty work.
