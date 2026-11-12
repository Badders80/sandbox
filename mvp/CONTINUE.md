# CONTINUE — MVP

> Shape: **Next action · State · Ledger · Blocked**.

**Next action:** open `audits/landing-parity-2026-11-12/EVIDENCE.md` and founder
walk V2 branch `landing-parity-2026-11-12` (`5726a51`) at 1440 and 390. After the
merge decision, resume F1: carry the contract ID through checkout and sale.

## State — 2026-11-12

- The V2 landing page is visually aligned to production on branch
  `landing-parity-2026-11-12` at `5726a51`; the worktree is clean, local only,
  not merged or pushed.
- Final landing refinements: wordmark-only nav, no divider, masked glass fade,
  112px visual nav height with the 80px content row unchanged, hero image
  restored, and a 300ms FAQ grid transition with reduced-motion fallback.
- Gate: `just check` exit 0, **393 engine passed / 1 skipped, 54 website**, both
  builds. The original landing audit passed; the final refinement audit's only
  WARN was its read-only skipped build, which was then run green in its
  disposable clone.
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
- The durable document is one immutable combined PDS/SA PDF with an exact-byte
  SHA-256 hash, immutable storage, email attachment, frozen MyStable display and
  a six-field external manifest.
- Supabase owns structured state; Stripe supplies payment/KYC signals; the local
  private vault stores retained investor/KYC/legal evidence; a second immutable
  copy provides durability; email is delivery only.

## Work queue

1. Founder-walk the V2 landing parity branch and decide whether to integrate it.
2. Persist the contract ID through checkout and sale storage (F1).
3. Update the PDS/SA legal copy to match the locked model:
   - full-horse return formula;
   - pro-rata purchase month and `Mon YYYY` references;
   - Subscription Float initial payment and final four-month draw-down;
   - aligned investor declarations;
   - contract ID.
4. Retrieve and verify the current Rules of Racing, including KYC, age,
   declarations, proof-of-address and eligibility requirements.
5. Implement email attachment delivery, frozen MyStable display and the second
   immutable copy.
6. Prove the Subscription Float Model end-to-end first, then the upfront control
   path.
7. Run the seven-step MVP DoD walk and retain the required evidence.

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
| 2026-11-12 | V2 landing parity built, refined, gated and audited (`5726a51`) | done; founder walk pending |
| 2026-11-12 | Production motion audit captured (1 Critical / 4 Important / 6 Opportunities) | done |
| next | persist the contract ID through checkout and sale (F1) | ready |

## Blocked

- **Landing parity merge:** waiting on the founder visual walk at 1440 and 390;
  the branch is local and must not merge or push until that gate is cleared.
- **Commercial terms:** final Mulan values are saved: $60 wholesale / $65 retail
  per 1% per month, 75% investor return, 5% listed, 1% minimum, 0.5% steps,
  subscription float, 14-day break, quarterly distributions and Jun 2028 expiry.
- **Legally final documents:** current Rules source is not verified locally and
  the documents still require legal sign-off.
- **KYC evidence:** proof-of-address and NZTR eligibility evidence are not yet
  proven against the current provider flow.
- **Production sale:** durable document path and current legal-copy alignment
  are not implemented.
