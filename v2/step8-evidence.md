# Step 8 — verification evidence

Recorded 2026-10-21, after the Step 8a and Step 8b commits. Full stdout for each run lived in `/tmp`; this file records the commits, CI runs, falsifications, restored-file hashes, local database probe, and audit verdicts.

## Commits and CI

| Commit | What | CI run | Result |
|---|---|---|---|
| `ba21375` | 8a, engine purchase core, Stripe endpoints, and webhook sale write | `39526758525` | success (1m15s) |
| `6b85013` | 8b, signup trigger `00012`, 5-screen `BuyFlowModal`, `/mystable`, purchase fences | `39528210409` | success (55s) |

## Gates

| Gate | Scope | Exit |
|---|---|---|
| `pnpm verify` on the 8a tree | 6 assertion scripts, 250 engine tests, 41 website tests, both builds | 0 |
| `pnpm verify` on the 8b tree | 7 assertion scripts (including `assert-purchase-fences.sh`), 250 engine tests, 50 website tests, both builds | 0 |
| `bash scripts/assert-purchase-fences.sh` | 6 rule groups (migration `00012`, no engine imports, no Stripe/service-role secrets, no pricing/compilation, `.from()` fence, refund sentence + zero day-counts + no NZTR-member claim, `/mystable` `force-dynamic`) | 0 |

## Falsifications

Each break was watched failing, then restored; the SHA-256 after restore matches the value before the break.

| # | Break | Test / Gate that failed | Restored file hash |
|---|---|---|---|
| 1 | `effectiveMinStake(dsl.minStake, dsl.stakeRemaining)` replaced with `dsl.minStake` in `engine/src/lib/purchase.ts` | `tests/purchase.test.ts`: `wires effectiveMinStake so an orphan remainder smaller than min_stake is buyable` | `purchase.ts` `0a48513ede1c13bd19b15aff2bcf515043be33ed39a394f31290c6ff4170a93d` |
| 2 | `if (!matched)` HMAC check disabled in `engine/src/lib/stripe.ts` | `tests/stripe-webhook.test.ts`: `rejects a tampered payload or wrong secret` | `stripe.ts` `0226538637d175cf0e81addf0369971626f2b2c6268fe696427decf9add43b36` |
| 3 | `if (account.kycStatus !== 'verified')` check disabled in `engine/src/lib/purchase.ts` | `tests/purchase.test.ts`: `blocks Checkout unless kycStatus is verified, and writes no sale row on session creation` | `purchase.ts` `0a48513ede1c13bd19b15aff2bcf515043be33ed39a394f31290c6ff4170a93d` |
| 4 | `.from('horses')` and `STRIPE_SECRET_KEY` injected into `website/src/lib/engineClient.ts` | `scripts/assert-purchase-fences.sh`: `website/src/ references a Stripe or service-role secret` and `queries 'horses'` | `engineClient.ts` `b3bb0ac8a35b5b3eab0c2902ec75076e1624a4029eeb25b27b984bfca90c0492` |
| 5 | `if (status !== 'available')` disabled in `canRenderBuyNow` (`website/src/lib/engineClient.ts`) | `tests/purchase-flow.test.ts`: `allows Buy Now only on available listings when WEBSITE_BUY_ENABLED is true` | `engineClient.ts` `b3bb0ac8a35b5b3eab0c2902ec75076e1624a4029eeb25b27b984bfca90c0492` |
| 6 | Day-count expression (`within 14 days`) injected into `BUY_FLOW_REFUND_SENTENCE` (`website/src/lib/engineClient.ts`) | `scripts/assert-purchase-fences.sh`: `verbatim refund sentence missing` and `day-count expression found in buy flow copy` | `engineClient.ts` `b3bb0ac8a35b5b3eab0c2902ec75076e1624a4029eeb25b27b984bfca90c0492` |

## Database probe (local stack `127.0.0.1:54422`, fixture removed afterwards)

Migration `00012_accounts_signup.sql` and `public.sales`:

```
auth.users insert without full_name          -> ERROR: signup requires full_name in user metadata
auth.users insert with full_name             -> public.accounts row created (Aroha Williams, aroha@example.co.nz, unverified)
sales insert (cs_test_probe_00012, 5%, 1775) -> INSERT 0 1
duplicate stripe_session_id insert           -> ERROR: duplicate key value violates unique constraint "sales_stripe_session_id_key"
authenticated (sub = owner) select accounts  -> 1 row
authenticated (sub = owner) select sales     -> 1 row (5.00, 1775.00, cs_test_probe_00012, pds_hash, sa_hash)
authenticated (sub = other) select accounts  -> 0 rows
authenticated (sub = other) select sales     -> 0 rows
```

After cleanup, `sales`, `accounts`, `dsls`, `horses`, and `auth.users` all returned to 0 rows.

## Audits (`kimi-k2.7-code`)

| Moment | Output | Verdict |
|---|---|---|
| 1, run 1 | `/tmp/step8-moment1.json` | FAIL — 2 casing mismatches (`account.fullName` vs `account.full_name`, `account.kycStatus` vs `account.kyc_status`) and 7 bundled checklist items |
| 1, run 2 | `/tmp/step8-moment1-r2.json` | PASS (`num_turns: 1`, 26-item checklist locked in `/home/evo/sandbox/v2/step8-checklist.md`) |
| 2, 8a | `/tmp/step8a-moment2.json` | PASS (`num_turns: 1`, items 1–13 & 26 + N1–N12 PASS, 0 FAILs) |
| 2, 8b | `/tmp/step8b-moment2.json` | PASS (`num_turns: 1`, items 4, 6, 14–26 + N1–N12 PASS, 0 FAILs) |

The locked checklist is `/home/evo/sandbox/v2/step8-checklist.md`.
