# Step 9 — locked Moment 1 checklist

Locked 2026-10-21 by `kimi-k2.7-code` (`num_turns: 1`, `is_error: false`) on `step9-plan.md` (revision 2). The audit returned zero FAIL findings and ended `VERDICT: PASS`.

## Locked checklist (29 single-requirement items)

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
