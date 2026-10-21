# Step 9 — The four transactional emails (plan, revision 2)

**Step:** `PLAN.md` § "When you say build" item 9 (`PLAN.md:317`), implementing `OUTCOME.md` § "How it runs — Emails, sent by the engine" (`OUTCOME.md:74`), `PLAN.md` § "Buy workflow" (`PLAN.md:234-238`), and `engine/OPERATIONS.md` § "Emails" (`engine/OPERATIONS.md:195-204`).
**Scope:** `engine/`, `scripts/assert-email-fences.sh`, the repo-root `package.json` test chain, and `engine/OPERATIONS.md`. `website/` and `supabase/migrations/` are untouched.
**One commit?** Yes. One atomic, gated commit on `main` (`feat(engine): add the four transactional emails and email fence (step 9)`), with its own Moment 2 audit, conventional commit, push, and green CI run (`PLAN.md:125`, `:211-212`).

## 0 · Path and naming convention, declared

Every path is repo-root-relative. The repo root is `/home/evo/evolution/engine_v2/website`, which holds `engine/` and `website/` as its two apps (`PLAN.md:11`, `:207`).
- **Existing files verified on disk with `grep -n`:** `engine/src/lib/purchase.ts`, `engine/src/lib/purchaseStore.ts`, `engine/src/lib/purchaseStoreSupabase.ts`, `engine/src/app/api/purchase/checkout/route.ts`, `engine/src/app/api/stripe/webhook/route.ts`, `engine/tests/purchase.test.ts`, `engine/tests/stripe-webhook.test.ts`, `engine/OPERATIONS.md`, and `package.json`.
- **New files to be created in Step 9:** `engine/src/lib/email.ts`, `engine/tests/email.test.ts`, and `scripts/assert-email-fences.sh`.

**Casing boundary:**
- Database columns in SQL and PostgREST wire rows use `snake_case` (`accounts.full_name`, `accounts.kyc_status`, `sales.stripe_session_id`, `sales.printed_name`).
- TypeScript domain types in `engine/src/lib/` use `camelCase` (`account.fullName`, `account.kycStatus`, `sale.stripeSessionId`, `sale.printedName`), matching `AccountRow` and `SaleRow` in `engine/src/lib/purchaseStore.ts:34-60`.
- Stripe webhook metadata keys inside `event.data.object.metadata` use `snake_case` (`account_id`, `dsl_id`, `stake`, `executed_date`, `stripe_identity_id`) as read by `recordWebhookEvent` in `engine/src/lib/purchase.ts:401-456`.

## 1 · Deliverables

| # | Path | What it is |
|---|---|---|
| D1 | `engine/src/lib/email.ts` | **New.** Closed four-variant email domain (`EMAIL_KINDS`), pure message builders (`buildBuyerSaleWrittenEmail`, `buildBuyerKycFailedEmail`, `buildFounderSaleSucceededEmail`, `buildFounderOurFaultFailureEmail`), `sendEngineEmail` dispatcher, hermetic `createInMemoryEmailSender`, and `createEmailSenderFromEnv` |
| D2 | `engine/src/lib/purchaseStore.ts`, `engine/src/lib/purchaseStoreSupabase.ts` | **Amended.** Adds `deleteSaleById(id: string): Promise<void>` to `PurchaseStore` (`purchaseStore.ts:62-69`), `createInMemoryPurchaseStore` (`purchaseStore.ts:88-163`), and `createSupabasePurchaseStore` (`purchaseStoreSupabase.ts:104-173`) so an our-fault failure in `store.updateDsl` after `store.insertSale` rolls back the sale row and leaves zero sale rows (`PLAN.md:238`) |
| D3 | `engine/src/lib/purchase.ts` | **Amended.** Wires `EmailSender` into `openCheckoutSession` (`:324-377`) and `recordWebhookEvent` (`:389-504`), including compensating `store.deleteSaleById(sale.id)` rollback if `store.updateDsl` throws after `store.insertSale` |
| D4 | `engine/src/app/api/purchase/checkout/route.ts`, `engine/src/app/api/stripe/webhook/route.ts` | **Amended.** Constructs `createEmailSenderFromEnv()` and passes it to `openCheckoutSession` (`checkout/route.ts:62`) and `recordWebhookEvent` (`webhook/route.ts:35`) |
| D5 | `engine/tests/email.test.ts` (new), `engine/tests/stripe-webhook.test.ts`, `engine/tests/purchase.test.ts` | Hermetic unit tests proving all four email contents/recipients, idempotent replay suppression, card-decline silence (`payment_intent.payment_failed`), expired-checkout silence (`checkout.session.expired`), compensating rollback on `updateDsl` failure, and rejection of any fifth email kind |
| D6 | `scripts/assert-email-fences.sh` (new), `package.json` | Static gate script chained into root `package.json` `test` script (`package.json:13`) asserting the closed four-email union, MyStable canonical link, zero email imports/keys in `website/src/`, and zero Gmail SMTP usage |
| D7 | `engine/OPERATIONS.md` | **Amended.** Updates `## Emails` (`engine/OPERATIONS.md:195-204`) with the four email triggers, environment variables (`ENGINE_EMAIL_API_URL`, `ENGINE_EMAIL_API_KEY`, `ENGINE_EMAIL_FROM`, `ENGINE_FOUNDER_EMAIL`), and verification procedure |

`pnpm-lock.yaml` does not change. Zero new npm dependencies are added in either app.

## 2 · Architectural seams and law alignment

### 1. Exactly four emails, sent by the engine, and no others (`OUTCOME.md:74`, `PLAN.md:317`)
`engine/src/lib/email.ts` defines the closed tuple:
```ts
export const EMAIL_KINDS = [
  'buyer_sale_written',
  'buyer_kyc_failed',
  'founder_sale_succeeded',
  'founder_our_fault_failure',
] as const
export type EmailKind = (typeof EMAIL_KINDS)[number]
```
`sendEngineEmail(input: EmailDispatchInput, sender: EmailSender)` validates `input.kind` against `EMAIL_KINDS` at both compile time and runtime, throwing if an unrecognised kind is passed.

1. **Buyer: sale written (`buyer_sale_written`)** (`OUTCOME.md:74`, `PLAN.md:317`, `engine/OPERATIONS.md:199`):
   - Triggered in `recordWebhookEvent` (`engine/src/lib/purchase.ts:476-503`) after both `store.insertSale` and `store.updateDsl` succeed on `checkout.session.completed`, **only** when `idempotentReplay === false`.
   - Sent to `sale.email`.
   - Body includes the purchased `stake`, the paid `amount`, and the canonical link to MyStable (`https://www.evolutionstables.nz/mystable`).
2. **Buyer: KYC failed (`buyer_kyc_failed`)** (`OUTCOME.md:74`, `PLAN.md:234`, `:317`, `engine/OPERATIONS.md:200`):
   - Triggered in `recordWebhookEvent` (`engine/src/lib/purchase.ts:412-425`) when `event.type` is `'identity.verification_session.requires_input'` or `'identity.verification_session.canceled'` and `store.updateAccountKycStatus(accountId, 'failed')` records `'failed'`.
   - Sent to `updated.email`.
3. **Founder: sale succeeded (`founder_sale_succeeded`)** (`OUTCOME.md:74`, `PLAN.md:317`, `engine/OPERATIONS.md:201`):
   - Triggered in `recordWebhookEvent` (`engine/src/lib/purchase.ts:476-503`) alongside `buyer_sale_written` when a new `sales` row and `dsls` stake drawdown both succeed (`idempotentReplay === false`).
   - Sent to `sender.founderEmail` (configured via `ENGINE_FOUNDER_EMAIL`).
   - Body includes `sale.printedName`, `sale.email`, `quote.horseLegalName`, `sale.stake`, `sale.amount`, and `sale.stripeSessionId`.
4. **Founder: checkout or webhook failed for a reason that is ours (`founder_our_fault_failure`)** (`OUTCOME.md:74`, `PLAN.md:238`, `:317`, `engine/OPERATIONS.md:202`):
   - Triggered in two places:
     - **Checkout (`stage: 'checkout'`):** in `openCheckoutSession` (`engine/src/lib/purchase.ts:357-368`) when buyer validation and `computeQuote` have passed (`account.kycStatus === 'verified'`, `dsl.status === 'available'`, `dsl.published === true`) and `stripe.createCheckoutSession` throws an error (or in `checkout/route.ts:82-87` on an unexpected server exception). No `sales` row is ever written in `openCheckoutSession`.
     - **Webhook (`stage: 'webhook'`):** in `recordWebhookEvent` (`engine/src/lib/purchase.ts:400-503`) when an identity event is missing `metadata.account_id` or `updateAccountKycStatus` throws, or when `checkout.session.completed` is missing `id` or required metadata (`dsl_id`, `account_id`, `stake`), fails `compileBuyerDocuments`, references a missing `dsl`, or throws during `store.insertSale` / `store.updateDsl`.
   - **Rollback guarantee on webhook failure (`PLAN.md:238` — "leaves no sale"):** If `store.updateDsl` throws after `store.insertSale` has succeeded in `recordWebhookEvent`, the catch block calls `await store.deleteSaleById(sale.id)` before sending `founder_our_fault_failure` and returning `{ ok: false, reason }`, ensuring zero `sales` rows remain on an our-fault webhook failure.
   - Sent to `sender.founderEmail` with `stage` (`'checkout'` or `'webhook'`) and `reason`.

### 2. What sends NO email (`OUTCOME.md:74`, `PLAN.md:236`, `:317`)
- **Card decline (`payment_intent.payment_failed`)**: `recordWebhookEvent` (`engine/src/lib/purchase.ts:427-430`) returns `{ action: 'ignored' }`, writes no `sales` row, and sends **zero** emails.
- **Cancelled / expired Checkout (`checkout.session.expired`)**: `recordWebhookEvent` (`engine/src/lib/purchase.ts:427-430`) returns `{ action: 'ignored' }`, writes no `sales` row, and sends **zero** emails.
- **Idempotent webhook replay (`idempotentReplay === true`)**: when `store.findSaleByStripeSessionId(stripeSessionId)` (`engine/src/lib/purchase.ts:441-447`) finds an existing `sales` row, `recordWebhookEvent` returns `{ action: 'sale_written', sale: existingSale, idempotentReplay: true }` and sends **zero** duplicate emails.
- **Buyer-fault validation rejections before Checkout**: when `openCheckoutSession` (`engine/src/lib/purchase.ts:338-354`) rejects unaccepted declarations, unverified/pending/failed KYC, or an off-step/unavailable stake, it returns `{ ok: false, reason }` and sends **zero** founder alert emails.

### 3. Transport seam (`PLAN.md:343`, `engine/OPERATIONS.md:204`)
- `createInMemoryEmailSender(founderEmail)` records every sent `EmailMessage` in memory (`sender.sent`) so `engine/tests/` stays hermetic with zero network calls and zero credentials in CI.
- `createEmailSenderFromEnv(env)` reads `ENGINE_EMAIL_API_URL`, `ENGINE_EMAIL_API_KEY`, `ENGINE_EMAIL_FROM`, and `ENGINE_FOUNDER_EMAIL` at call time, throwing an explicit error naming any missing variable, and dispatches via `fetch` with `Authorization: Bearer ${apiKey}` and JSON body `{ from, to, subject, text, kind }`. Zero Gmail SMTP (`nodemailer` / `smtp.gmail.com`) is used (`PLAN.md:343`, `engine/OPERATIONS.md:204`).

## 3 · Negative constraints (each falsifiable against a diff)

- **N1** No fifth email kind beyond `buyer_sale_written`, `buyer_kyc_failed`, `founder_sale_succeeded`, and `founder_our_fault_failure` (`OUTCOME.md:74`, `PLAN.md:317`).
- **N2** No email sent on `payment_intent.payment_failed` (card decline) or `checkout.session.expired` (`OUTCOME.md:74`, `PLAN.md:236`, `:317`).
- **N3** No duplicate email sent when `checkout.session.completed` is replayed for an already-recorded `stripe_session_id` (`engine/src/lib/purchase.ts:441-447`).
- **N4** No founder alert email sent when a buyer fails input/KYC validation in `openCheckoutSession` (`engine/src/lib/purchase.ts:338-354`).
- **N5** `website/` never imports `engine/src/lib/email.ts`, never sends emails, and holds zero `ENGINE_EMAIL_*` or `ENGINE_FOUNDER_EMAIL` variables (`OUTCOME.md:74`, `PLAN.md:23`, `:290`).
- **N6** No Gmail SMTP (`smtp.gmail.com`, `nodemailer`) anywhere in the repo (`PLAN.md:343`, `engine/OPERATIONS.md:204`).
- **N7** No apex URL (`https://evolutionstables.nz`) in any email body; the MyStable link in `buyer_sale_written` is `https://www.evolutionstables.nz/mystable` (`PLAN.md:92`).
- **N8** No import from `sandbox/rebuild`, `engine/website/...`, or `legal_engine` anywhere (`PLAN.md:216`).
- **N9** No database driver imported in `engine/tests/` or `website/tests/`; all tests stay hermetic (`PLAN.md:350`).
- **N10** No `AGENTS.md`, `CLAUDE.md`, or `HOW-WE-WORK.md` (`PLAN.md:120`, `:208`).

## 4 · Non-orphan consumer wiring

| Symbol / Deliverable | Production Call Site |
|---|---|
| `EMAIL_KINDS`, `EmailSender`, `sendEngineEmail`, `buildBuyerSaleWrittenEmail`, `buildBuyerKycFailedEmail`, `buildFounderSaleSucceededEmail`, `buildFounderOurFaultFailureEmail` (`engine/src/lib/email.ts`) | `openCheckoutSession` and `recordWebhookEvent` in `engine/src/lib/purchase.ts` |
| `deleteSaleById` (`engine/src/lib/purchaseStore.ts`, `engine/src/lib/purchaseStoreSupabase.ts`) | Compensating rollback in `recordWebhookEvent` (`engine/src/lib/purchase.ts`) when `store.updateDsl` throws after `store.insertSale` |
| `createEmailSenderFromEnv` (`engine/src/lib/email.ts`) | `POST` in `engine/src/app/api/purchase/checkout/route.ts` and `POST` in `engine/src/app/api/stripe/webhook/route.ts` |
| `createInMemoryEmailSender` (`engine/src/lib/email.ts`) | Hermetic test suites in `engine/tests/email.test.ts`, `engine/tests/purchase.test.ts`, and `engine/tests/stripe-webhook.test.ts` |
| `scripts/assert-email-fences.sh` (`D6`) | Root `package.json` `test` chain (`package.json:13`) |

## 5 · Verification protocol

1. `pnpm verify` from `/home/evo/evolution/engine_v2/website` exits 0 with `--max-warnings=0`.
2. Falsifications (each broken, watched failing, restored, and SHA-256 hash-verified):
   - Emit a founder email on `payment_intent.payment_failed` in `engine/src/lib/purchase.ts` → `engine/tests/email.test.ts` fails.
   - Omit the MyStable URL (`https://www.evolutionstables.nz/mystable`) from `buildBuyerSaleWrittenEmail` in `engine/src/lib/email.ts` → `scripts/assert-email-fences.sh` and `engine/tests/email.test.ts` fail.
   - Remove the `!idempotentReplay` guard on sale emails in `engine/src/lib/purchase.ts` → replay test in `engine/tests/email.test.ts` fails on duplicate emails.
   - Reference `ENGINE_EMAIL_API_KEY` inside `website/src/lib/engineClient.ts` → `scripts/assert-email-fences.sh` fails.

## 6 · Moment 1 candidate checklist (29 single-requirement items)

1. `engine/src/lib/email.ts` exports `EMAIL_KINDS` with the exact four members `'buyer_sale_written'`, `'buyer_kyc_failed'`, `'founder_sale_succeeded'`, and `'founder_our_fault_failure'`, and defines no fifth kind.
2. `sendEngineEmail` in `engine/src/lib/email.ts` rejects any message kind outside `EMAIL_KINDS`.
3. `buildBuyerSaleWrittenEmail` addresses the email to `sale.email`.
4. `buildBuyerSaleWrittenEmail` includes the purchased `stake`, the paid `amount`, and the canonical MyStable link `https://www.evolutionstables.nz/mystable`.
5. `buildBuyerKycFailedEmail` addresses the email to `account.email`.
6. `buildFounderSaleSucceededEmail` addresses the email to `sender.founderEmail`.
7. `buildFounderSaleSucceededEmail` includes the buyer's printed name, buyer email, horse legal name, `stake`, `amount`, and `stripeSessionId`.
8. `buildFounderOurFaultFailureEmail` addresses the email to `sender.founderEmail`.
9. `buildFounderOurFaultFailureEmail` includes the failure `stage` (`'checkout'` or `'webhook'`) and `reason`.
10. On a new `checkout.session.completed` (`idempotentReplay === false`), `recordWebhookEvent` sends `buyer_sale_written`.
11. On a new `checkout.session.completed` (`idempotentReplay === false`), `recordWebhookEvent` sends `founder_sale_succeeded`.
12. On a replayed `checkout.session.completed` (`idempotentReplay === true`), `recordWebhookEvent` sends zero emails.
13. On `identity.verification_session.requires_input` or `identity.verification_session.canceled`, `recordWebhookEvent` updates the account KYC status to `'failed'`.
14. On `identity.verification_session.requires_input` or `identity.verification_session.canceled`, `recordWebhookEvent` sends `buyer_kyc_failed`.
15. On `payment_intent.payment_failed` or `checkout.session.expired`, `recordWebhookEvent` writes no `sales` row.
16. On `payment_intent.payment_failed` or `checkout.session.expired`, `recordWebhookEvent` sends zero emails.
17. When `stripe.createCheckoutSession` throws in `openCheckoutSession`, `openCheckoutSession` sends `founder_our_fault_failure` with `stage: 'checkout'`.
18. When `stripe.createCheckoutSession` throws in `openCheckoutSession`, zero `sales` rows are written.
19. When `recordWebhookEvent` encounters an our-fault failure (missing metadata, compile failure, missing DSL, or store write failure), `recordWebhookEvent` sends `founder_our_fault_failure` with `stage: 'webhook'`.
20. If `store.updateDsl` throws after `store.insertSale` in `recordWebhookEvent`, `store.deleteSaleById(sale.id)` removes the sale row so zero `sales` rows remain.
21. Buyer-fault validation rejections in `openCheckoutSession` (`!accepted.ok`, `account.kycStatus !== 'verified'`, or invalid stake) send zero founder emails.
22. `engine/src/app/api/purchase/checkout/route.ts` constructs `createEmailSenderFromEnv()` and passes it to `openCheckoutSession`.
23. `engine/src/app/api/stripe/webhook/route.ts` constructs `createEmailSenderFromEnv()` and passes it to `recordWebhookEvent`.
24. `scripts/assert-email-fences.sh` is chained into the root `package.json` `test` script (`package.json:13`).
25. `scripts/assert-email-fences.sh` fails if any fifth email kind exists.
26. `scripts/assert-email-fences.sh` fails if the MyStable URL (`https://www.evolutionstables.nz/mystable`) is missing from `engine/src/lib/email.ts`.
27. `scripts/assert-email-fences.sh` fails if any Gmail SMTP reference (`smtp.gmail.com` or `nodemailer`) exists in `engine/src/` or `website/src/`.
28. `scripts/assert-email-fences.sh` fails if `website/src/` imports `engine/src/lib/email.ts` or references `ENGINE_EMAIL_*` / `ENGINE_FOUNDER_EMAIL`.
29. `engine/OPERATIONS.md` records the four email triggers, the required `ENGINE_EMAIL_*` / `ENGINE_FOUNDER_EMAIL` variables, and the verification steps.

## 7 · Repair ledger — revision 1 → revision 2

Revision 1 went to Moment 1 round 1 (`kimi-k2.7-code`) and returned `VERDICT: FAIL` with 5 findings. All 5 were verified true and repaired:

| # | Round 1 Finding | Repair in Revision 2 |
|---|---|---|
| 1 | `step9-plan.md:9` claimed every citation was verified with `grep -n` against disk without separating new Step 9 files from existing disk files, and `step9-moment1-prompt.txt` omitted some cited `PLAN.md` lines | Explicitly separated existing disk-verified files from new Step 9 files in §0, and inlined all cited `PLAN.md`, `purchaseStore.ts`, and `purchaseStoreSupabase.ts` lines in `step9-moment1-prompt.txt` |
| 2 | Candidate item 3 bundled the recipient and three content fields | Split into item 3 (recipient) and item 4 (content fields) |
| 3 | Candidate item 5 bundled the recipient and six content fields | Split into item 6 (recipient) and item 7 (content fields) |
| 4 | Candidate item 11 bundled checkout failure, webhook failure, and the no-sale guarantee, and `recordWebhookEvent` lacked a rollback if `updateDsl` threw after `insertSale` | Added `deleteSaleById` to `PurchaseStore` (`D2`) and compensating rollback in `recordWebhookEvent` (`D3`), and split the checklist items into items 17, 18, 19, and 20 |
| 5 | Candidate item 14 bundled four gate conditions into one item | Split into items 24, 25, 26, 27, and 28 |

The last line of the audit reply must be exactly `VERDICT: PASS` or `VERDICT: FAIL`.
