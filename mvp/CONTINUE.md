# CONTINUE — MVP

> Shape: **Next action · State · Ledger · Blocked**.

**Next action:** open
`sessions/active/2026-11-13-checkout-scroll-mapping.md` and review
`/home/evo/sandbox/rebuild/purchase-flow-v2-with-deck.html` against the current
checkout contracts. Map the PDS/SA scroll locks and post-sale pack/email before
changing implementation.

## State — 2026-11-13

- **Investor Pack = PDS + SA** is locked terminology. The Investor Pack is the
  single investor-facing PDF artifact; PDS and SA remain its two legal
  components with separate acceptance controls.
- Formal assembly is locked: cover page, one contents page indexing both sections
  and all subsections, then the PDS and SA on separate fresh pages. The current
  Mulan saved-record proof is `out/legal/ES-DSL-2026-900018/contract.pdf`: 15
  pages, legal pack 1.0.4, PDS page 3, SA page 10 and 54 indexed headings.
- The V2 landing page is visually aligned to production and is merged/pushed on
  `dsl-sidequest` at `03ea397`; the founder accepted desktop and mobile.
- The shared page foundation is locked/pushed at `ade0cc3`: global scroll reveal,
  `--duration-reveal: 750ms`, shared page primitives, no page-level separator
  rule and client-navigation-safe reveal re-arming.
- The Marketplace plan remains active at
  `sessions/active/2026-11-13-marketplace-mystable.md`. The next focused session
  is `sessions/active/2026-11-13-checkout-scroll-mapping.md`, which maps the
  checkout prototype and scroll locks to the persisted acceptance contract.
- **Checkout source boundary is locked:** legacy production and
  `sandbox/rebuild` are reference-only after
  `audits/CHECKOUT-SOURCE-AUDIT-2026-11-13.md`. New checkout work starts from
  that audit plus the current V2 contracts; no old component, legal copy,
  fixture, price model or migration instruction is carried forward as debt.
- **Marketplace Session 1 visual proof is built** on
  `marketplace-parity-2026-11-14` from `origin/dsl-sidequest` at `e74b725`.
  Mulan is the available lead card in a local six-card fixture; nothing was
  published and no Marketplace data was written. Evidence is in
  `audits/marketplace-parity-2026-11-14/`. Gate: engine 401 passed / 1 skipped,
  website 66 passed, both builds; desktop and mobile axe reports have zero
  violations; founder visual walk remains pending.
- Final landing refinements: monogram nav, gold wordmark hero aligned to the
  copy edge, masked glass fade, mobile drawer lifecycle motion, 750ms
  reveal-once scroll motion, no page-level separator lines and reduced-motion
  fallbacks.
- Gate after the shared foundation: `just check` exit 0, **402 engine passed /
  1 skipped, 63 website**, both builds.
- Paired final screenshots and audit artifacts are in
  `audits/landing-parity-2026-11-12/`.
- Motion review saved at `audits/EVOLUTION-STABLES-MOTION-AUDIT-2026-11-12.html`:
  1 Critical, 4 Important, 6 Opportunities. Best carry-forwards are the nav
  underline, accent-line growth, capped scroll reveals, FAQ expansion and
  footer reveal.
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
- The Investor Pack is one immutable combined PDS + SA PDF with an exact-byte
  SHA-256 hash, immutable storage, email attachment, frozen MyStable display and
  a six-field external manifest.
- **Legal authority boundary:** Owner-to-Evolution authority is assumed, managed
  outside the MVP and recorded manually before publish. Evolution-to-Investor
  offer, acceptance, KYC, sale, Investor Pack and ledger execution remain in
  system. The Investor Pack does not claim to prove the upstream lease or title.
- **F1 acceptance persistence — done:** checkout sessions store PDS/SA acceptance
  timestamps, the canonical declaration snapshot, typed signature and recording
  time. The declaration and signature evidence is immutable, and Stripe cannot
  bind a checkout until acceptance is recorded. The sale remains linked through
  `checkout_session_id`.
- Supabase owns structured state; Stripe supplies payment/KYC signals; the local
  private vault stores retained investor/KYC/legal evidence; a second immutable
  copy provides durability; email is delivery only.

### Checkpoint — 2026-11-13

The Investor Pack presentation baseline is current at legal pack `1.0.4`:
terminology, legal copy, cover, contents, hierarchy, pagination, tables,
grayscale styling, signatures, aligned declarations and the 15-page saved-record
proof are complete and gate-verified. Proof of address remains pending and is
handled manually. This is a presentation checkpoint, not legal authority or a
production-sale approval. Upstream owner authority is a recorded external
assumption. Current Rules verification, Evolution-to-Investor legal sign-off,
KYC evidence and the full checkout/sale chain remain open.

## Work queue

1. Lock the Marketplace initial page from the production audit and shared V2
   foundation; do not publish Mulan or write Marketplace data in this phase.
2. Rebuild the Marketplace horse page.
3. Replace the horse-page checkout with the locked five-screen flow: Terms,
   Documents, Identity, Pay, Return. Keep one stable modal footprint and design
   mobile-first.
4. Rebuild MyStable across signed-out, empty, pending, recorded-sale and frozen
   Investor Pack states.
5. Complete F1:
   - persist the contract ID through checkout and sale storage;
   - keep the executed date separate from the selected term start;
   - carry the selected whole-month start through quote, Investor Pack, checkout
     and the frozen sale snapshot;
   - require the PDS to be scrolled through before acceptance;
   - require the SA to be scrolled through, its declarations to be ticked, and a
     typed full legal name before signing;
   - keep declarations inside the SA signing flow; do not create a third document;
   - freeze an unsigned review Investor Pack before signing, then generate the
     executed Investor Pack only after payment writes the sale;
   - persist PDS/SA hashes and acceptance times, the declaration snapshot, typed
     signature, review-pack hash, executed-pack hash, checkout ID and sale ID;
   - set proof-of-address status to `pending` when the executed Investor Pack is
     emailed; proof of address is verified manually outside the workflow, with no
     upload or automated request step in this phase;
   - run the investor sequence in this order: review and sign the Investor Pack,
     complete KYC, complete payment, write the sale, email the executed Investor
     Pack confirming ownership and requesting proof of address, then keep proof of
     address `pending` while it is monitored manually.
6. Add the listing-publish control that records the upstream Owner-to-Evolution
   authority check, operator, date and internal reference.
7. Update the PDS/SA legal copy to match the locked model:
   - full-horse return formula;
   - pro-rata purchase month and `Mon YYYY` references;
   - Subscription Float initial payment and final four-month draw-down;
   - aligned investor declarations;
   - contract ID.
8. Retrieve and verify the current Rules of Racing, including KYC, age,
   declarations, proof-of-address and eligibility requirements.
9. Implement email attachment delivery, frozen MyStable display and the second
   immutable copy.
10. Prove the Subscription Float Model end-to-end first, then the upfront control
   path.
11. Run the seven-step MVP DoD walk and retain the required evidence.

## Review backlog

- [x] Compare the proposed v2 website with production
  `https://evolutionstables.nz/`. Result:
  `audits/V2-VS-PRODUCTION-2026-11-11.md`. Revisit the horse-detail and checkout
  half once one V2 listing is published.
- [x] Review the five-step purchase-flow prototype at
  `sandbox/rebuild/purchase-flow-v2-with-deck.html`. Result:
  `audits/PURCHASE-FLOW-V2-PROTOTYPE-2026-11-11.md`.
- [x] Build the V2 landing parity branch and refine nav, hero and FAQ motion.
  Result: `audits/landing-parity-2026-11-12/EVIDENCE.md`.
- [x] Audit production motion. Result:
  `audits/EVOLUTION-STABLES-MOTION-AUDIT-2026-11-12.html`.
- [x] Audit and implement the Marketplace initial page as a local visual proof.
  Result: `audits/marketplace-parity-2026-11-14/EVIDENCE.md`.
- [x] Audit legacy production checkout and `sandbox/rebuild`, extract only the
  reusable behaviours, and freeze both old builds as reference-only. Result:
  `audits/CHECKOUT-SOURCE-AUDIT-2026-11-13.md`.

## Ledger

| date | what | state |
|---|---|---|
| 2026-11-13 | Landing merged; shared V2 page foundation locked; Marketplace→MyStable next-session plan created | done; pushed (`03ea397`, `ade0cc3`) |
| 2026-11-11 | MVP scope and DoD created | done |
| 2026-11-11 | `MODEL.md` commercial/legal model locked | done |
| 2026-11-11 | Durable sale-record model locked | done |
| 2026-11-11 | Proposed v2 website design review captured | done |
| 2026-11-12 | [PDS/SA document-package session DoD](sessions/archive/2026-11-12-pds-sa-package.md) locked | done |
| 2026-11-12 | Headless PDS/SA package gate implemented and verified | done |
| 2026-11-12 | Additive expense pricing locked as `ceil(wholesale × 1.08)` | done |
| 2026-11-12 | Voluntary exit, default notice and automatic wind-up restored | done |
| 2026-11-12 | Final Mulan commercials rendered to `ES-DSL-2026-900006` | done |
| 2026-11-12 | wrap — model, legal package and audit evidence committed | done |
| 2026-11-12 | V2 landing parity built, refined, gated and audited (`5726a51`) | done; founder walk pending |
| 2026-11-12 | Production motion audit captured (1 Critical / 4 Important / 6 Opportunities) | done |
| 2026-11-12 | wrap notes committed and branch published | done |
| 2026-11-13 | Investor Pack terminology locked as PDS + SA | done |
| 2026-11-13 | Formal cover, indexed contents and fresh-page PDS/SA assembly | done |
| 2026-11-13 | Legal-document typography polish and running page furniture | done |
| 2026-11-13 | Body prose corrected to true justified alignment | done |
| 2026-11-13 | Legal pack 1.0.3 redlines, Investor terminology and grayscale polish | done |
| 2026-11-13 | Structural layout pass: break control, clause hierarchy and schedule tables | done |
| 2026-11-13 | Contents page refined to whitespace-aligned hierarchy without dot leaders | done |
| 2026-11-13 | Final density pass: compact type, uppercase subsections and signature grids | done |
| 2026-11-13 | Investor Pack presentation baseline checkpointed at legal pack 1.0.3 | done |
| 2026-11-13 | Legal pack 1.0.4 aligned SA and checkout declarations; KYC and proof of address deferred as future obligations | done |
| 2026-11-13 | Legal authority boundary locked: upstream authority external and recorded at publish; Evolution-to-Investor in system | done |
| 2026-11-13 | F1 acceptance persistence: immutable PDS/SA declarations, typed signature and checkout binding | done |
| 2026-11-13 | Checkout scroll-mapping next-session plan created | ready |
| 2026-11-13 | Checkout source audit and legacy/rebuild freeze created | done |
| 2026-11-14 | Marketplace production audit and V2 local-fixture implementation | built; founder walk pending |
| next | F1: contract ID plus executed date / selectable term-start mapping | ready |

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
