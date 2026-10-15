# Website audit

This folder records motion findings on the live site, and the review of where those findings go. It does not authorise a change to production, and it does not amend `/home/evo/sandbox/v2/PLAN.md`. The plan is the build authority.

## Chain

| Date | File | What it does |
|---|---|---|
| 2026-10-13 | `AUDIT-MOTION-2026-10-13.md` | Reads the live site's motion: purchase beats, the modal, the stepper, accordions, homepage reveals. Ranks C1–C4 and I1–I5. |
| 2026-10-13 | `PLAN-CRITICAL-FIXES-2026-10-13.md` | Turns those findings into a fix sequence. The sequence runs through `sandbox/rebuild` into `apps/web`, using `brand_dna` motion tokens and `MIGRATION-PLAN.md`. |
| 2026-10-13 | This file | Reviews that plan against the v2 build. The findings stay. The destination does not. |

Sibling audits sit outside this folder. `website-brand-audit/` (2026-10-09) looked at the live landing page, marketplace, and MyStable while `engine_v2` was still empty. The 2026-10-12 files in `/home/evo/audit/` used `DoD.md`. `OUTCOME.md` is the product authority now, and `sandbox/v2/PLAN.md` is the build authority.

## Review, 2026-10-13

The motion findings are real. The implementation plan points them at the live site, which the v2 build has already ruled out.

`evolution-3-0` keeps deploying `Badders80/evo_02`. The new repo does not import `sandbox/rebuild` or the token package. `PLAN-CRITICAL-FIXES-2026-10-13.md` is the old migration. It is kept here as the record of that proposal. It is not a v2 work order.

Three observations are kept, and they are applied when the v2 page that needs them is built:

- The live purchase flow holds each beat for 1400ms so the buyer can read it. A short enter transition is the right fix. The sale still waits on the network and the webhook, not on a timer.
- The purchase modal should animate in and out. The stepper should show a press. Both are ordinary CSS on the buy modal at step 8.
- The homepage hero waits 0.85s before it appears. The v2 landing page paints the hero in the first response.

Left behind, and not copied into the v2 plan: a `brand_dna` motion group, a GSAP reveal library, Framer Motion, a drag-to-adjust stepper, an accordion rewrite for Press and the FAQ, and a motion lint. Press and the FAQ are later pages. Marketplace, the horse page, and MyStable stay plain server-rendered pages. Landing motion stays on the landing page, in the one theme file.

## Covered here

- How the live site moves: reveals, hero parallax, accordions, the purchase beat floor, reduced motion.
- Which of those motions are conversion problems (C1, C2) and which are polish (C3, C4, I1–I5).
- The decision that those fixes do not migrate into `apps/web`.

## Not covered here

- The buy screen words, the price functions, and the Stripe Checkout handoff. Those are in `sandbox/v2/PLAN.md` under "Buy workflow" and "Reference: sandbox/rebuild".
- Accounts, the legal reference set, search, and the page order. Those are in the same plan.
- A visual spec for the landing page. The current landing page is the north star. This folder only flags the hero delay.
- Marketplace, horse listing, and MyStable behaviour. The 2026-10-09 brand audit described the live pages. It is not a v2 build list.
- Whether the live `CollapsePanel` or `reveal.ts` should be rewritten in `evo_02`. That site stays as it is until the domain cutover.
