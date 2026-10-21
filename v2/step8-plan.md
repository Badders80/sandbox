# Step 8 — Purchase, the sale write, and MyStable (plan, revision 2)

**Step:** `PLAN.md` § "When you say build" item 8 (`PLAN.md:316`), implementing `PLAN.md` § "Buy workflow" (`PLAN.md:224-239`) and `OUTCOME.md` § "Sale" (`:33-37`), § "Refund" (`:54-56`), and § "Purchase" (`:72`).
**Scope:** `engine/`, `website/`, `supabase/migrations/00012_accounts_signup.sql`, `scripts/assert-purchase-fences.sh`, the repo-root `package.json` test chain, and `engine/OPERATIONS.md`.
**One commit?** No. Two atomic, gated sub-steps on `main`, each with its own Moment 2 audit, conventional commit, push, and green CI run (`PLAN.md:125`, `:211-212`), mirroring Step 7's `7a`–`7d` split:
- **8a — Engine purchase core, Identity & Checkout endpoints, and webhook sale write** (`engine/` only).
- **8b — Website auth (`00012`), buy modal on `/marketplace/[slug]`, and `/mystable` return** (`website/`, `supabase/migrations/00012_accounts_signup.sql`, `scripts/assert-purchase-fences.sh`).

## 0 · Path and naming convention, declared

Every path is repo-root-relative. The repo root is `/home/evo/evolution/engine_v2/website`, which holds `engine/` and `website/` as its two apps (`PLAN.md:11`, `:207`). Every citation below has been verified with `grep -n` against disk.

**Casing boundary:**
- Database columns in SQL and PostgREST wire rows use `snake_case` (`accounts.full_name`, `accounts.kyc_status`, `sales.stripe_session_id`, `dsls.stake_remaining`, `dsls.investor_split`).
- TypeScript domain types in `engine/src/lib/` and `website/src/lib/` use `camelCase` (`account.fullName`, `account.kycStatus`, `sale.stripeSessionId`, `dsl.stakeRemaining`, `dsl.investorSplit`), matching `LegalPackInput.account.fullName` (`engine/src/lib/legal/tokens.ts:23`) and `DslRow` (`engine/src/lib/dslStore.ts:76-95`).
- Template token keys inside `.template.md` and `SCALAR_KEYS` (`engine/src/lib/legal/tokens.ts:60`) use dotted `snake_case` (`{{account.full_name}}`).

## 1 · Deliverables

### Sub-step 8a (`engine/` + `engine/OPERATIONS.md`)

| # | Path | What it is |
|---|---|---|
| D1 | `engine/src/lib/purchaseStore.ts`, `engine/src/lib/purchaseStoreSupabase.ts` | Store interface (`PurchaseStore`), hermetic `createInMemoryPurchaseStore`, and Supabase service-role implementation (`accounts`, `sales`, `dsls` stake drawdown) |
| D2 | `engine/src/lib/stripe.ts` | Zero-SDK Stripe REST + HMAC-SHA256 webhook signature verifier (`verifyStripeSignature`) and `StripeGateway` interface (`createIdentitySession`, `retrieveIdentitySession`, `createCheckoutSession`) |
| D3 | `engine/src/lib/purchase.ts` | Pure purchase domain: `computeQuote` (wiring `effectiveMinStake` at `engine/src/lib/pricing.ts:120`), `compileBuyerDocuments`, `beginOrConfirmIdentity`, `openCheckoutSession`, and `recordWebhookEvent` (writes `sales`, decrements `stake_remaining`, flips `fully_allocated` at 0) |
| D4 | `engine/src/app/api/purchase/quote/route.ts`, `documents/route.ts`, `identity/route.ts`, `checkout/route.ts`, `engine/src/app/api/stripe/webhook/route.ts` | The engine HTTP endpoints called by the website buy flow and by Stripe's webhook |
| D5 | `engine/tests/purchase.test.ts`, `engine/tests/stripe-webhook.test.ts`, `engine/tests/structure.test.ts` | Hermetic unit tests for `effectiveMinStake`, quote math, document compilation, KYC gate, checkout gate, webhook signature verification, frozen sale-row immutability on horse rename/edit, and narrowing `engine/tests/structure.test.ts:73` to allow `['dsl', 'api']` |
| D6 | `engine/OPERATIONS.md` | Purchase, KYC, and webhook operator procedures |

### Sub-step 8b (`website/` + `00012` + `scripts/`)

| # | Path | What it is |
|---|---|---|
| D7 | `supabase/migrations/00012_accounts_signup.sql` | Auth signup trigger (`auth.users` → `public.accounts` using `raw_user_meta_data->>'full_name'`) so signup creates the one account row and checkout never creates a second profile (`PLAN.md:24`, `:316`, `00006_accounts.sql:2-3`) |
| D8 | `website/src/lib/listings.ts` | **Amended.** Adds `investor_split` (wire) / `investorSplit` (TypeScript) to `LISTING_SELECT` (`:82-96`), `ListingRow` (`:32-52`), and `Listing` (`:54-74`) so Screen 1 and Screen 4 can display the DSL's investor split (`PLAN.md:230`, `:236`) without a `'75'` fallback |
| D9 | `website/src/lib/auth.ts`, `website/src/app/login/page.tsx` | Supabase Auth login/signup (email + Google OAuth, full name required at signup) with `?next=/marketplace/[slug]` return redirect (`PLAN.md:24`, `:226`) |
| D10 | `website/src/lib/mystable.ts`, `website/src/app/mystable/page.tsx` | Server-rendered `/mystable` (`force-dynamic`): reads `accounts` and `sales` under the signed-in user's JWT (`00009_website_read_policies.sql:70-78`), shows pending state when returning from Checkout before the webhook writes the sale (`PLAN.md:238`), and renders stake, amount, and both frozen documents + SHA-256 hashes once written |
| D11 | `website/src/lib/engineClient.ts`, `website/src/components/BuyFlowModal.tsx`, `website/src/app/marketplace/[slug]/page.tsx` | One responsive five-screen buy flow (`Terms` → `Documents` → `Identity` → `Pay` → `Return`) rendered on `available` DSLs only (`coming_soon` renders no Buy Now, `PLAN.md:226`), gated by `WEBSITE_BUY_ENABLED` so Step 10's preview-with-buy-off rule (`PLAN.md:318`) and Step 8's purchase wiring both work without code edits |
| D12 | `website/tests/purchase-flow.test.ts`, `website/tests/listings.test.ts`, `scripts/assert-purchase-fences.sh`, `package.json`, `website/.env.example` | Hermetic tests, narrowed `.from()` fence in `website/tests/listings.test.ts:194-209` (`dsls` for public reads, `accounts` and `sales` only in `website/src/lib/mystable.ts`), and static fence script added to root `package.json` |

`pnpm-lock.yaml` does not change. Zero new npm dependencies are added in either app.

## 2 · Architectural seams and law alignment

### 1. Website never prices, never compiles, and holds no Stripe secret (`PLAN.md:23`, `:290`)
- All pricing (`effectiveMinStake`, `validateStake`, `totalForStake`, `floatTotal`, `upfrontTotal`), all document compilation (`compileLegalPack`), all Stripe Identity session creation, all Stripe Checkout session creation, and the Stripe webhook live in `engine/`.
- `website/` calls `engine/` over server-side HTTP (`WEBSITE_ENGINE_URL`) and receives pre-calculated figures, compiled Markdown + hashes, and redirect URLs.
- `website/` never imports from `engine/`, never computes `stake * rate` or `5 * rate`, and holds zero `STRIPE_*` or `SERVICE_ROLE` variables.

### 2. `effectiveMinStake` is wired (`PLAN.md:230`, `:349`)
- `engine/src/lib/pricing.ts:120` defines `effectiveMinStake(minStake, stakeRemaining)`.
- `engine/src/lib/purchase.ts` calls `effectiveMinStake(dsl.minStake, dsl.stakeRemaining)` in `computeQuote` and `validatePurchaseStake`.
- When `dsl.stakeRemaining < dsl.minStake` and `dsl.stakeRemaining > 0`, the buyer's minimum (and sole remaining slice) is `dsl.stakeRemaining`, preventing orphan inventory (`PLAN.md:230`).

### 3. Five screens, one responsive surface (`PLAN.md:228-238`)
- One component (`BuyFlowModal.tsx`), reflowing across phone and desktop with 44px minimum touch targets (`website/DESIGN.md:415`), using existing 6a theme tokens (`website/src/app/globals.css`) and `.legal-doc` tokens (`--color-legal-surface`, `--color-legal-ink`, `--color-legal-surface-alt`, `--color-legal-border`, `--color-legal-checkbox` at `globals.css:49-54`). No separate mobile flow, no drawer, no new tokens.
- **Screen 1 — Terms (`PLAN.md:230`):**
  - Horse's `legalName`.
  - Stepper bound to `effectiveMinStake(dsl.minStake, dsl.stakeRemaining)`, `dsl.step`, and `dsl.stakeRemaining`.
  - Four rows from the engine quote:
    1. Initial payment (`subscription_float`: 5 months — 3 months deposit reserve, 2 months prepaid — times retail rate; `upfront`: full term).
    2. Monthly thereafter (`subscription_float`: 1× monthly share price, billed on the 1st starting Month 3; `upfront`: $0.00).
    3. Lease period (`dsl.termStart` to `dsl.endDate`).
    4. Distribution share (`dsl.investorSplit`% of stakes won, from official NZTR results — never defaulted to 75%; a null split throws).
  - Exact note under rows: fixed monthly payment, no surprise capital calls, plus verbatim `REFUND_SENTENCE` (`If the horse is retired or the lease ends early, the leaseholder receives a pro-rata refund of the unused lease fee for the full months remaining.`, `OUTCOME.md:56`) with zero day-count expressions.
  - Footer: `Evolution Stables is an NZTR-authorised syndicator.`
  - Button: `Review Legal Documents` (or sign-in redirect returning to `/marketplace/[slug]` if logged out, `PLAN.md:226`).
- **Screen 2 — Documents (`PLAN.md:232`):**
  - Title: `Review & Sign Documents`.
  - Renders the PDS and then the SA, compiled by the engine with `account.fullName` (mapped from `accounts.full_name` into `LegalPackInput.account.fullName` at `engine/src/lib/legal/tokens.ts:23`).
  - Buyer must tick acceptance of the PDS, and acceptance of the SA including the four mandatory declarations verbatim (`PLAN.md:232`):
    1. not disqualified or suspended under the NZTR Rules of Racing;
    2. acquiring the stake as the true beneficial owner;
    3. bound by the NZTR Rules of Racing and the Welfare Guidelines;
    4. Evolution Stables Limited is the syndicate manager.
  - Button (enabled only when all acceptances are ticked): `Continue to Identity Verification`.
  - Footer: `Signed documents are hashed and stored for MyStable.` (the webhook writes the hashes).
- **Screen 3 — Identity (`PLAN.md:234`):**
  - If `account.kycStatus === 'verified'` (mapped from `accounts.kyc_status`), the buyer confirms they are `account.fullName` and continues.
  - Otherwise, the engine creates a Stripe Identity `VerificationSession` (`type: 'document'`, driver licence or passport), records `accounts.kyc_status = 'pending'` (`account.kycStatus = 'pending'`), and returns the verification URL. It never claims the buyer is an "NZTR-verified member".
  - If `account.kycStatus === 'failed'`, the engine stops the sale and does not open Checkout.
  - Footer: `Encrypted and handled under the NZ Privacy Act 2020.`
- **Screen 4 — Pay (`PLAN.md:236`):**
  - Repeats the initial payment, the monthly amount, the lease period, and the investor split, and states the card is processed by Stripe Checkout.
  - Button redirects the browser to the Stripe Checkout URL returned by the engine (`mode: 'payment'`, `OUTCOME.md:48`, `cancel_url` back to `/marketplace/[slug]`, `success_url` to `/mystable?session_id={CHECKOUT_SESSION_ID}`).
- **Screen 5 — Return / MyStable (`PLAN.md:238`):**
  - `/mystable` reads the authenticated user's `accounts` row and `sales` rows (`00009_website_read_policies.sql:70-78`).
  - If `?session_id=...` is present and the webhook has not yet written the matching `sales` row, `/mystable` renders that purchase as **pending** and never says the stake is owned (`PLAN.md:222`, `:238`).
  - Once the `sales` row exists, `/mystable` renders the horse name, the stake %, the amount paid, and the frozen `pds_markdown` and `sa_markdown` with their `pds_hash` and `sa_hash`.

### 4. Webhook sale write and frozen-document immutability (`PLAN.md:316`, `OUTCOME.md:35`)
- `POST /api/stripe/webhook` verifies `Stripe-Signature` using HMAC-SHA256 (`t=...,v1=...`) and a 300-second timestamp tolerance against the raw request body.
- Handles:
  - `identity.verification_session.verified` → updates `accounts.kyc_status = 'verified'` (`account.kycStatus = 'verified'`).
  - `identity.verification_session.requires_input` / `canceled` → updates `accounts.kyc_status = 'failed'` (`account.kycStatus = 'failed'`).
  - `checkout.session.completed` → idempotent on `sales.stripe_session_id` (`00007_sales.sql:14`). Compiles the PDS and SA at sale execution, writes `dsl_id`, `user_id`, `printed_name`, `email`, `stake`, `amount`, `stripe_session_id`, `stripe_identity_id`, `pds_markdown`, `sa_markdown`, `pds_hash`, `sa_hash` into `public.sales`, and decrements `dsls.stake_remaining` by `stake` (setting `status = 'fully_allocated'` when `stake_remaining` reaches `0`).
  - Payment intent / card decline events (`payment_intent.payment_failed`) write **no sale** (`PLAN.md:236`).
- Because `pds_markdown`, `sa_markdown`, `pds_hash`, and `sa_hash` are stored verbatim on `public.sales`, any subsequent `updateDsl` or horse rename (`engine/src/lib/dsl.ts:340`) leaves existing `sales` rows byte-for-byte untouched (`PLAN.md:316`, `:331`).

## 3 · Fences and narrowings

1. **`engine/tests/structure.test.ts:73`**:
   Currently asserts `const unexpected = routes.filter((name) => !['dsl'].includes(name))`. Step 8a narrows this to `['dsl', 'api']` so the engine route handlers under `engine/src/app/api/` are permitted while standalone `horses`, `trainers`, `owners`, `admin`, `manage`, `crud`, `registry` screens remain banned (`:25-39`).
2. **`website/tests/listings.test.ts:194-209`**:
   Currently asserts every `.from('...')` in `website/src/` is `'dsls'`. Step 8b narrows this fence by one path: `website/src/lib/mystable.ts` may query `'accounts'` and `'sales'` (which `00009_website_read_policies.sql:47-48, 70-78` explicitly granted and policed for `authenticated`), while `.from('horses')`, `.from('trainers')`, and `.from('owners')` remain banned across all of `website/src/`.
3. **Preview buy-path toggle (`PLAN.md:318`)**:
   Step 8 builds the buy workflow and Step 10 requires previewing with the buy path off until the readiness flip. On `/marketplace/[slug]`, the Buy Now button renders on `available` listings only when `process.env.WEBSITE_BUY_ENABLED === 'true'`. `coming_soon`, `fully_allocated`, and `completed` never render a Buy Now button under any flag.

## 4 · Negative constraints (each falsifiable against a diff)

- **N1** No import from `sandbox/rebuild`, `engine/website/...`, or `legal_engine` anywhere (`PLAN.md:216`, `:316`).
- **N2** `website/` never imports from `engine/`, never holds a `STRIPE_*` or `SERVICE_ROLE` secret, never computes retail or checkout prices, and never compiles legal templates (`PLAN.md:23`, `:290`).
- **N3** No `.from('horses')`, `.from('trainers')`, or `.from('owners')` anywhere under `website/src/` (`PLAN.md:290`).
- **N4** No new design tokens and no edits to `website/src/app/globals.css` (`PLAN.md:194`, `:346`). All components pass `scripts/assert-design-tokens.sh`.
- **N5** No `'75'` or `75` fallback for `investor_split` anywhere (`PLAN.md:219`, `:230`).
- **N6** No day-count expression (`/\d+\s+days?/i`) in the buy flow copy (`PLAN.md:267`).
- **N7** No screen or copy that claims the buyer is an "NZTR-verified member" (`PLAN.md:234`) or claims the stake is owned before the `sales` row exists (`PLAN.md:222`, `:238`).
- **N8** No Buy Now control on `coming_soon`, `fully_allocated`, or `completed` listings (`PLAN.md:226`, `:292`).
- **N9** Checkout does not create a second profile table or duplicate account row (`PLAN.md:316`).
- **N10** No email sending in Step 8 (the four emails belong to Step 9, `PLAN.md:317`).
- **N11** No database driver imported in `engine/tests/` or `website/tests/`; all tests stay hermetic (`PLAN.md:350`).
- **N12** No `AGENTS.md`, `CLAUDE.md`, or `HOW-WE-WORK.md` (`PLAN.md:120`, `:208`).

## 5 · Non-orphan consumer wiring

| Symbol / Deliverable | Production Call Site |
|---|---|
| `effectiveMinStake` (`engine/src/lib/pricing.ts:120`) | `computeQuote` and `validatePurchaseStake` in `engine/src/lib/purchase.ts` |
| `PurchaseStore` & `createSupabasePurchaseStore` (`D1`) | Route handlers under `engine/src/app/api/purchase/*` and `engine/src/app/api/stripe/webhook/route.ts` |
| `verifyStripeSignature` & `StripeGateway` (`D2`) | `engine/src/app/api/stripe/webhook/route.ts` and `engine/src/lib/purchase.ts` |
| `computeQuote`, `compileBuyerDocuments`, `beginOrConfirmIdentity`, `openCheckoutSession`, `recordWebhookEvent` (`D3`) | `quote/route.ts`, `documents/route.ts`, `identity/route.ts`, `checkout/route.ts`, `webhook/route.ts` (`D4`) |
| `engineClient.ts` (`D11`) | `BuyFlowModal.tsx` and `/marketplace/[slug]/page.tsx` |
| `BuyFlowModal.tsx` (`D11`) | `/marketplace/[slug]/page.tsx` |
| `mystable.ts` (`D10`) | `/mystable/page.tsx` |
| `auth.ts` (`D9`) | `/login/page.tsx`, `/marketplace/[slug]/page.tsx`, `/mystable/page.tsx` |
| `scripts/assert-purchase-fences.sh` (`D12`) | Root `package.json` `test` chain |

## 6 · Verification protocol

1. `pnpm verify` from `/home/evo/evolution/engine_v2/website` exits 0 with `--max-warnings=0`.
2. Falsifications (each broken, watched failing, restored, and hash-verified):
   - Replace `effectiveMinStake(dsl.minStake, dsl.stakeRemaining)` with `dsl.minStake` → orphan-remainder purchase test fails.
   - Tamper with `Stripe-Signature` HMAC digest → webhook test refuses with 400 and writes 0 rows.
   - Allow checkout when `account.kycStatus !== 'verified'` → checkout gate test fails.
   - Mutate horse `legalName` and DSL `wholesaleMonthlyPerPercent` via `updateDsl` after `recordWebhookEvent` → test confirms stored `sales.pds_markdown`, `sa_markdown`, `pds_hash`, and `sa_hash` remain unchanged.
   - Add a `.from('horses')` call or a `STRIPE_SECRET_KEY` reference in `website/src/` → `scripts/assert-purchase-fences.sh` and `website/tests/` fail.
3. Local database probe for `00012_accounts_signup.sql` and the sale write against local Postgres on `54422` (seeded fixture, verified, and torn down so 0 rows remain), recorded in `engine/OPERATIONS.md`.

## 7 · Moment 1 candidate checklist (25 single-requirement items)

1. `effectiveMinStake` (`engine/src/lib/pricing.ts:120`) is called from `engine/src/lib/purchase.ts` so that `stake_remaining < min_stake` allows purchasing the full remaining balance without orphaning inventory.
2. `validateStake` (or the purchase stake gate) enforces `stake % step === 0` on standard steps above the effective minimum.
3. `computeQuote` derives the initial payment (`floatTotal` for `subscription_float`, `upfrontTotal` for `upfront`) and the monthly amount (`totalForStake` for `subscription_float`, `0` for `upfront`) without recomputing the per-1% retail rate.
4. The buyer-facing copy reads the DSL's own `investor_split` and refuses if it is `null`; no `'75'` or `75` fallback appears anywhere.
5. `compileBuyerDocuments` calls `compileLegalPack` with `account.fullName` mapped from `accounts.full_name`, returning the PDS and SA Markdown plus hashes.
6. The document-acceptance gate requires PDS acceptance, SA acceptance, and the four SA declarations verbatim before the flow advances to Identity.
7. `beginOrConfirmIdentity` skips Stripe Identity when `account.kycStatus === 'verified'` (after the buyer confirms the name), starts a Stripe Identity session when `account.kycStatus === 'unverified'`, and blocks Checkout when `account.kycStatus` is `'failed'` or `'pending'`.
8. `openCheckoutSession` requires `account.kycStatus === 'verified'`, `dsl.status === 'available'`, and `dsl.published === true`, creates a Stripe Checkout session in `payment` mode, and writes no `sales` row at session creation.
9. `verifyStripeSignature` verifies `Stripe-Signature` with HMAC-SHA256 and a timestamp tolerance against the raw request body.
10. `recordWebhookEvent` is idempotent on `sales.stripe_session_id` (`supabase/migrations/00007_sales.sql:14`).
11. On `checkout.session.completed`, the webhook writes `dsl_id`, `user_id`, `printed_name`, `email`, `stake`, `amount`, `stripe_session_id`, `stripe_identity_id`, `pds_markdown`, `sa_markdown`, `pds_hash`, and `sa_hash` into `public.sales`, decrements `dsls.stake_remaining` by `stake`, and flips `dsls.status` to `'fully_allocated'` when `stake_remaining === 0`.
12. Card-decline / `payment_intent.payment_failed` events write no `sales` row.
13. Later edits or renames to the horse or DSL via `updateDsl` do not alter the `pds_markdown`, `sa_markdown`, `pds_hash`, or `sa_hash` of any existing `sales` row.
14. Migration `00012_accounts_signup.sql` populates `public.accounts` (`id`, `full_name`, `email`, `kyc_status = 'unverified'`) from `auth.users` on signup so Checkout never creates a second profile.
15. `BuyFlowModal.tsx` implements the five responsive screens (`Terms` → `Documents` → `Identity` → `Pay` → `Return`) using only existing 6a theme tokens and `.legal-doc` tokens.
16. The Terms and Pay screens print the verbatim `REFUND_SENTENCE` from `engine/src/lib/pricing.ts:38-39` with zero day-count expressions, and no screen claims the buyer is an "NZTR-verified member".
17. The Buy Now control renders only on `available` listings and only when `WEBSITE_BUY_ENABLED === 'true'`; `coming_soon`, `fully_allocated`, and `completed` listings never render a Buy Now control under any flag.
18. `/mystable` (`force-dynamic`) reads the authenticated user's `accounts` and `sales` rows.
19. `/mystable` shows a pending state when returning from Checkout before the webhook writes the matching `sales` row, never claiming the stake is owned.
20. Once the `sales` row exists, `/mystable` renders the stake, amount, and both frozen documents plus their hashes.
21. `website/` imports nothing from `engine/` or `sandbox/rebuild`.
22. `website/` holds no `STRIPE_*` or `SERVICE_ROLE` secret and performs no pricing or template compilation.
23. `website/src/lib/mystable.ts` is the only file under `website/src/` that queries `accounts` or `sales`; every other `.from('...')` in `website/src/` targets `dsls`.
24. `scripts/assert-purchase-fences.sh` is included in the root `package.json` `test` chain and fails on any forbidden read, import, or secret in `website/src/`.
25. `engine/OPERATIONS.md` records the purchase flow, webhook verification, and local DB probe.

## 8 · Repair ledger — revision 1 → revision 2

Revision 1 went to Moment 1 round 1 (`kimi-k2.7-code`) and returned `VERDICT: FAIL` with 9 findings (2 casing/property-name mismatches in prose, 7 bundled checklist items). All 9 were verified true on disk and repaired:

| # | Round 1 Finding | Repair in Revision 2 |
|---|---|---|
| 1 | `step8-plan.md:66` wrote `account.full_name` where `LegalPackInput` (`engine/src/lib/legal/tokens.ts:23`) uses `account.fullName` | Declared the SQL `snake_case` vs TypeScript `camelCase` boundary in §0 and updated §2 Screen 2 to `account.fullName` (mapped from `accounts.full_name`) |
| 2 | `step8-plan.md:75` and `:90-91` mixed `account.kyc_status` and `account.kycStatus` | Standardized all TypeScript property references on `account.kycStatus` and SQL column references on `accounts.kyc_status` |
| 3–9 | Candidate checklist items 1, 3, 6, 7, 9, 10, 11 bundled multiple requirements per item | Adopted the auditor's 25 single-requirement checklist items verbatim in §7 |
| — | Header line 5 said "Three atomic, gated sub-steps" while listing two (`8a`, `8b`) | Corrected to "Two atomic, gated sub-steps" |

The last line of the audit reply must be exactly `VERDICT: PASS` or `VERDICT: FAIL`.
