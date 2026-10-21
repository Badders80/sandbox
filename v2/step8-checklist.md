# Step 8 — locked Moment 1 checklist

Locked 2026-10-21 by `kimi-k2.7-code` on `step8-plan.md` (revision 2). The audit returned zero FAIL findings and ended `VERDICT: PASS`.

Sub-step 8a (`engine/`) covers items 1–13 (and the 8a portion of item 26). Sub-step 8b (`website/`, `00012`, `scripts/`) covers items 14–26.

## Locked checklist (26 items)

1. `engine/src/lib/pricing.ts:120` `effectiveMinStake` is called from `engine/src/lib/purchase.ts` so that `stake_remaining < min_stake` allows purchasing the full remaining balance without orphaning inventory.
2. The purchase stake gate enforces `stake % step === 0` (basis-points modulo) on every chosen stake.
3. `computeQuote` derives the initial payment (`floatTotal` for `subscription_float`, `upfrontTotal` for `upfront`) and the monthly amount (`totalForStake` for `subscription_float`, `0` for `upfront`) using the DSL's stored/generated retail rate, never recomputing `wholesale × 1.05 × 1.03`.
4. The buyer-facing copy reads the DSL's own `investorSplit` and refuses if it is `null`; no `'75'` or `75` fallback appears anywhere.
5. `compileBuyerDocuments` calls `compileLegalPack` with `account.fullName` mapped from `accounts.full_name`, returning the PDS and SA Markdown plus SHA-256 hashes.
6. The document-acceptance gate requires PDS acceptance, SA acceptance, and the four SA declarations verbatim before the flow advances to Identity.
7. `beginOrConfirmIdentity` skips Stripe Identity when `account.kycStatus === 'verified'` (after the buyer confirms the name), starts a Stripe Identity session when `account.kycStatus === 'unverified'`, and blocks Checkout when `account.kycStatus` is `'failed'` or `'pending'`.
8. `openCheckoutSession` requires `account.kycStatus === 'verified'`, `dsl.status === 'available'`, and `dsl.published === true`, creates a Stripe Checkout session in `payment` mode, and writes no `sales` row at session creation.
9. `verifyStripeSignature` verifies `Stripe-Signature` with HMAC-SHA256 and a 300-second timestamp tolerance against the raw request body.
10. `recordWebhookEvent` is idempotent on `sales.stripe_session_id` (`supabase/migrations/00007_sales.sql:14`).
11. On `checkout.session.completed`, the webhook writes `dsl_id`, `user_id`, `printed_name`, `email`, `stake`, `amount`, `stripe_session_id`, `stripe_identity_id`, `pds_markdown`, `sa_markdown`, `pds_hash`, and `sa_hash` into `public.sales`, decrements `dsls.stake_remaining` by `stake`, and flips `dsls.status` to `'fully_allocated'` when `stake_remaining === 0`.
12. Card-decline / `payment_intent.payment_failed` events write no `sales` row.
13. Later edits or renames to the horse or DSL via `updateDsl` do not alter the `pds_markdown`, `sa_markdown`, `pds_hash`, or `sa_hash` of any existing `sales` row.
14. Migration `00012_accounts_signup.sql` populates `public.accounts` (`id`, `full_name`, `email`, `kyc_status = 'unverified'`) from `auth.users` on signup so Checkout never creates a second profile.
15. `BuyFlowModal.tsx` implements the five responsive screens (`Terms` → `Documents` → `Identity` → `Pay` → `Return`) using only existing 6a theme tokens and `.legal-doc` tokens.
16. The Terms and Pay screens print the verbatim `REFUND_SENTENCE` from `engine/src/lib/pricing.ts:38-39` and contain zero day-count expressions.
17. No screen claims the buyer is an "NZTR-verified member".
18. The Buy Now control renders only on `available` listings and only when `WEBSITE_BUY_ENABLED === 'true'`; `coming_soon`, `fully_allocated`, and `completed` listings never render a Buy Now control under any flag.
19. `/mystable` (`force-dynamic`) reads the authenticated user's `accounts` and `sales` rows.
20. `/mystable` shows a pending state when returning from Checkout before the webhook writes the matching `sales` row, never claiming the stake is owned.
21. Once the `sales` row exists, `/mystable` renders the stake, amount, and both frozen documents plus their hashes.
22. `website/` imports nothing from `engine/` or `sandbox/rebuild`.
23. `website/` holds no `STRIPE_*` or `SERVICE_ROLE` secret and performs no pricing or template compilation.
24. `website/src/lib/mystable.ts` is the only file under `website/src/` that queries `accounts` or `sales`; every other `.from('...')` in `website/src/` targets `dsls`.
25. `scripts/assert-purchase-fences.sh` is included in the root `package.json` `test` chain and fails on any forbidden read, import, or secret in `website/src/`.
26. `engine/OPERATIONS.md` records the purchase flow, webhook verification, and local DB probe.
