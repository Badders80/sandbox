# Step 9 — verification evidence

Recorded 2026-10-21, after the Step 9 commit (`c3ec894`). Full stdout for each run lived in `/tmp`; this file records the commit, CI run, gates, falsifications, restored-file hashes, and audit verdicts.

## Commit and CI

| Commit | What | CI run | Result |
|---|---|---|---|
| `c3ec894` | Step 9 (12 files): `engine/src/lib/email.ts`, `purchaseStore.ts`, `purchaseStoreSupabase.ts`, `purchase.ts`, `checkout/route.ts`, `stripe/webhook/route.ts`, `email.test.ts`, `purchase.test.ts`, `stripe-webhook.test.ts`, `scripts/assert-email-fences.sh`, `package.json`, and `engine/OPERATIONS.md` | `39536613709` | success (1m0s) |

## Gates

| Gate | Scope | Exit |
|---|---|---|
| `pnpm verify` on the Step 9 tree | 8 assertion scripts (including `assert-email-fences.sh`), 260 engine tests across 16 files, 50 website tests across 5 files, both builds | 0 |
| `bash scripts/assert-email-fences.sh` | 4 rule groups (closed 4-member `EMAIL_KINDS`, canonical `https://www.evolutionstables.nz/mystable` + zero bare apex URLs, zero `smtp.gmail.com` / `nodemailer`, zero email imports or `ENGINE_EMAIL_*` / `ENGINE_FOUNDER_EMAIL` in `website/src/`) | 0 |

## Falsifications

Each break was watched failing, then restored; the SHA-256 after restore matches the value before the break.

| # | Break | Test / Gate that failed | Restored file hash |
|---|---|---|---|
| 1 | Emit `founder_our_fault_failure` on `payment_intent.payment_failed` in `engine/src/lib/purchase.ts` | `engine/tests/email.test.ts`: `writes no sale row and sends zero emails on payment_intent.payment_failed and checkout.session.expired` | `purchase.ts` `24ed1765783943136e22a274820782f4a01a6d7f78d6cdf3947cf3e37ae973b6` |
| 2 | Replace `https://www.evolutionstables.nz/mystable` with `https://www.evolutionstables.nz/account` in `engine/src/lib/email.ts` | `scripts/assert-email-fences.sh` (`canonical MyStable URL ... missing`) and `engine/tests/email.test.ts` (`builds all four messages with exact recipients and required fields`) | `email.ts` `52bfab284bd0039ec60d47572ae879721bfd121ce57b7c476739fba541bf5c4d` |
| 3 | Dispatch `buyer_sale_written` inside the `existingSale !== null` replay branch in `engine/src/lib/purchase.ts` | `engine/tests/email.test.ts`: `sends buyer_sale_written and founder_sale_succeeded once on a new checkout.session.completed, and zero emails on replay` | `purchase.ts` `24ed1765783943136e22a274820782f4a01a6d7f78d6cdf3947cf3e37ae973b6` |
| 4 | Inject `ENGINE_EMAIL_API_KEY` comment into `website/src/lib/engineClient.ts` | `scripts/assert-email-fences.sh`: `website/src/ imports engine email module or references ENGINE_EMAIL_* / ENGINE_FOUNDER_EMAIL` | `engineClient.ts` `b3bb0ac8a35b5b3eab0c2902ec75076e1624a4029eeb25b27b984bfca90c0492` |

## Audits (`kimi-k2.7-code`)

| Moment | Output | Verdict |
|---|---|---|
| 1, run 1 | `/tmp/step9-moment1.out` | FAIL — 5 findings (unseparated new vs existing disk citations in `step9-plan.md`, missing `deleteSaleById` rollback if `updateDsl` threw after `insertSale`, and 4 bundled checklist items) |
| 1, run 2 | `/tmp/step9-moment1-r2.out` | PASS (`num_turns: 1`, 29-item checklist locked in `/home/evo/sandbox/v2/step9-checklist.md`) |
| 2 | `/tmp/step9-moment2.out` | PASS (`num_turns: 1`, items 1–29 + N1–N10 PASS, 0 FAILs) |

The locked checklist is `/home/evo/sandbox/v2/step9-checklist.md`.

**Next:** Step 10 — preview deployment with the buy path off (`WEBSITE_BUY_ENABLED` unset/`false`) on the new Vercel projects.
