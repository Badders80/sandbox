# Chunk 4 — Phases B and C (dispatch brief)

Repo: `/home/evo/evolution/engine_v2/website`. Branch `dsl-sidequest` at `47ce66f`. Work **only** in the dispatch worktree.
Before the gate: copy `/home/evo/evolution/engine_v2/website/engine/.env.local` into the worktree at `engine/.env.local` (gitignored).
Do not push, do not merge, do not commit. Leave the diff for review.

**State:** Phase A is merged. `supabase/migrations/00024_ledger.sql` is applied to local **and** hosted and its 27 probes pass. **`00024` is frozen — do not edit it.** Any schema delta you need is `00025`.

Read `00024_ledger.sql` for the exact `record_sale_atomically` signature and the columns it expects.

The governing DoD is `/home/evo/sandbox/v2/dsl-sidequest/CHUNK4-BRIEF-2026-11-11.md`; this brief covers only what remains.

---

## Phase B — sale path and domain

1. **Remove the delete path.** `deleteSaleById` leaves the `PurchaseStore` interface and every live caller (`purchase.ts:710`, `:728`). No replacement.
2. **Wire `record_sale_atomically`.** `purchaseStoreSupabase` calls the RPC with the bound checkout and Stripe session. One call replaces insertSale + completeCheckoutSession + the sellStake fallback. On a typed refusal: write no sale, mark `paid_unfulfilled`, send the founder alert. On success: no further sale or stake writes.
3. **U21 pricing.** Add `isListableDsl` (no `termStart`) and use it in `pricePurchase`: `start` = first day of `executedDate`'s month; `remaining = termMonthsBetween(start, endDate)`; effective model `upfront` when the listing is upfront or `remaining <= 5`, else `subscription_float`; price the remaining months. Do **not** write `dsls.term_start`.
4. **Snapshot through the RPC.** `SaleRow` / `NewSale` carry the snapshot fields; the ledger reads them. No field is recomputed from the live DSL.
5. **Close action.** Add the operator close (status → completed) with the U19 guard: sweep stale holds, refuse while any `open` or `paid_unfulfilled` checkout exists.
6. **Invariant helper.** `listed = sold + open holds + held paid_unfulfilled + remaining`, in horse points, reading `sales`, `checkout_sessions.stake_returned_at` and `dsls.stake_remaining`.
7. **Tests:** replay, duplicate webhook, lapsed hold, concurrent claim, U21 pricing (≤5 and >5 months), close guard (open, held paid_unfulfilled, returned paid_unfulfilled), invariant, no delete method exists.

## Phase C — ledger and proof

1. **Ledger on `/sales`:** per-DSL sections or a DSL filter; cap table (listed, sold, open holds, remaining, revenue, term end); investor rows with stake, amount, date, PDS/SA hashes, contract position; the close action and its refusal reason.
2. **Fixture — local stack only.** Create it through the real reserve → sale path and label it synthetic. The hosted `evolution-engine` DB takes **no synthetic rows**.
3. **Email/MyStable check:** confirm MyStable serves the stored `pds_markdown` / `sa_markdown` bytes, not a recompile. Record the result; do not change the email.
4. Screenshots at 1440×900 and 390×844.

## Gate and proofs

`pnpm verify` green. Then, on the local stack:

- Ledger walk over the fixture: the cap-table numbers, investor rows, hashes.
- `UPDATE`, `DELETE`, `TRUNCATE` on `sales` refused (the Phase A probes already prove this; re-run them).
- Close refused with an open hold and with a `paid_unfulfilled` (held and returned).
- The invariant holds after reserve, sale, expiry and release.
- A dateless listing sells with the correct `term_start`, remaining months and documents.
- The email/MyStable result recorded.

## Out of scope

F1–F5: contract ID, post-sale term freeze, external legal archive, offsite backup, recovery test. Public site, rename/R2, auth, content wizard.

## Return format

Files touched; gate output pasted; probe and ledger-walk output pasted; what you did not do; open decisions.

## Budget

One dispatch seat, **220 tool calls**, hard stop at **2×**. $6 cap.

## Assurance

**Tier A.** One **kimi-code** audit on the mergeable diff, after the gate. Merge is the founder's call.
