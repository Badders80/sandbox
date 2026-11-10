# Chunk 4 — Ledger (dispatch brief)

Repo: `/home/evo/evolution/engine_v2/website`. Branch `dsl-sidequest`. Work **only** in the dispatch worktree.
Before the gate: copy `/home/evo/evolution/engine_v2/website/engine/.env.local` into the worktree at `engine/.env.local` (gitignored).
Do not push, do not merge, do not commit. Leave the diff for review.

Build order: **Phase A (`00024`) first.** Stop for review when it applies clean to local **and** hosted and the SQL probes pass. Then Phase B (sale path and domain), then Phase C (ledger UI and proof). The frozen DoD follows — it is the contract.

Return format: files touched; gate output pasted; SQL probe output pasted; local ↔ hosted parity for `00024`; what you did not do; open decisions.

---

# Chunk 4 — Ledger — DoD (locked 2026-11-11)

**Done when:** a sold term is visible, closable and immutable; the ledger reads a frozen
snapshot, not mutable DSL state; and a listing created by chunk 3 (expiry only, no start)
can be sold.

Starting surface (verified 2026-11-11):

- `/sales` is a read-only page listing `dslId`, `stake`, `amount`, `createdAt`.
- `sales` has no snapshot columns; `dsls` has no `closed_at`/`closed_reason`/`closed_by`;
  `checkout_sessions` has no `stake_returned_at`.
- `purchase.ts` deletes a just-inserted sale on two failure paths (`:710`, `:728`).
- `isPricedDsl` requires `termStart`, so a chunk-3 listing cannot be bought.

## Criteria

1. **U15 — ledger.** Upgrade `/sales`: per-DSL cap table (listed, sold, open holds,
   remaining, revenue, term end), investor rows with the frozen PDS/SA and hashes, and
   the manual close action. Reads the **snapshot**; never recompiles a document.
2. **U18 — sale snapshot.** `sales` stores the executed terms: `wholesale_monthly_per_percent`,
   `retail_monthly_per_percent`, `investor_split`, `listed_stake`, `min_stake`, `step`,
   `end_date`, `payment_model_at_sale`, `close_style`, `distribution_schedule`,
   `term_start`, `term_end`, `term_months`, and `trainer_id` / `owner_id` at sale.
   Snapshot only. **No post-sale DSL freeze** (F2); the ledger never reads live terms.
3. **U19 — close guard.** `dsls` gains `closed_at`, `closed_reason`, `closed_by`. The
   manual close sweeps stale holds, then refuses while any `open` or `paid_unfulfilled`
   checkout exists — held **or** returned, because money was taken without a sale.
4. **U20 — cap-table identity and fixture.** In horse points:
   `listed = sold + open holds + held paid_unfulfilled + remaining`.
   `00024` adds `checkout_sessions.stake_returned_at timestamptz`: **null** = stake still
   held; **set** = release or expiry returned it. A `paid_unfulfilled` row contributes
   capacity only when null. Proven by an SQL probe and a test. The fixture goes through
   the real reserve → sale path and is labelled synthetic.
5. **U21 — sale-time start and remaining-month pricing.** A listing carries an expiry and
   **no start** (ruling 25). At checkout:
   - `start` = first day of the calendar month of `executedDate` (the month the investor buys).
   - `remaining` = `termMonthsBetween(start, endDate)`, inclusive; refuse `< 1`.
   - Effective model at sale = `upfront` if the listing is `upfront` **or** `remaining <= 5`;
     otherwise `subscription_float`.
   - Initial payment: `upfront` → `upfrontTotal(remaining, retail, stake)`;
     `subscription_float` → `floatTotal(retail, stake)`.
   - Compile the PDS/SA with that `start` and effective model.
   - Store `term_start`, `term_end`, `term_months`, `payment_model_at_sale` on `sales`.
   - Do **not** write `dsls.term_start`; it is not a listing property.
   - Split the guard: add `isListableDsl` (no `termStart`) for purchase pricing; keep
     `isPricedDsl` where a real start exists.
6. **H6 — append-only in fact.** `00024` adds `record_sale_atomically`, one SECURITY
   DEFINER function that writes the sale and claims the hold in a single transaction.
   It is idempotent by `stripe_session_id`, locks the checkout and DSL rows, validates
   amount, currency and hold status, writes the snapshot, claims the hold, updates the
   DSL and completes the checkout. On an expired/released hold or insufficient stake it
   writes no sale, marks `paid_unfulfilled` and alerts the founder. `deleteSaleById`
   leaves the store interface and the live path. Then refuse `UPDATE`, `DELETE` and
   `TRUNCATE` on `sales` with no exception, and revoke them.
   Tests: replay, duplicate webhook, lapsed hold, concurrent claim.
7. **Email verification.** The buyer email links to MyStable; it does not attach the
   documents. Confirm MyStable renders the stored `pds_markdown` / `sa_markdown` and
   hashes without recompiling. Record the result. Do not change the email here.

## Phase A — `00024`

- Add the `sales` snapshot columns (U18) and the `dsls` close columns (U19).
- Add `checkout_sessions.stake_returned_at`; set it in release and expiry.
- Add `record_sale_atomically` (U21 + H6) and its grants (`service_role` only).
- Refuse update, delete and truncate on `sales`; revoke the three privileges.
- Apply to local via `psql`; apply to hosted `evolution-engine`; record parity.
- Stop for review with the probe output.

## Phase B — sale path and domain

- Wire `record_sale_atomically` into the webhook; delete the sale-delete paths.
- Implement U21 pricing and the `isListableDsl` split.
- Implement the close action and its guard; add the invariant helper.
- Gate: `pnpm verify`.

## Phase C — ledger and proof

- Build the ledger on `/sales`; add the fixture through the real path **on the local stack
  only**. The hosted `evolution-engine` DB takes no synthetic rows.
- Run the full gate and every proof below.
- Screenshots at 1440×900 and 390×844.

## Out of scope

F1–F5: contract ID printed/indexed; post-sale term freeze; external legal archive and
manifest; offsite backup and restore drill; recovery test. Public site, rename/R2, auth,
the content wizard.

## Gate

`pnpm verify` green; `00024` applies clean to local and hosted with parity; a ledger walk
over the synthetic fixture on local; `UPDATE`, `DELETE` and `TRUNCATE` on `sales` refused; a close
refused with an open hold and with a `paid_unfulfilled` (held and returned); the
cap-table identity holds in horse points; a dateless listing sells with the correct
`term_start`, remaining months and documents; the email/MyStable result recorded.

## Budget

One dispatch seat, **300 tool calls**, hard stop at **2×**. $5 cap. Phase A stops on a
second failed migration apply.

## Assurance

**Tier A** — money path, data writes, a schema migration and legal documents. One
**kimi-code** audit on the mergeable diff, after the gate is green. If Phase A ships as a
separate diff, it gets its own audit. Merge is the founder's call.

## Open

None. Ruling 25 governs the sale-time start and the one-time payment under five months.
Report any conflict; do not resolve it.
