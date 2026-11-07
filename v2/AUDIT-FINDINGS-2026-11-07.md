# V2 audit — findings (2026-11-07)

Working file. Appended as each audit unit returns. Final report is `AUDIT-REPORT-2026-11-07.md`.

Baseline gate: `pnpm verify` **EXIT=0** on the dirty tree — 260 engine tests / 16 files, 50 website tests / 5 files, 8 assertion scripts, typecheck, lint, both builds. Clean-HEAD check not run.

## Working tree (uncommitted) — my own audit

| File | What it is | Verdict |
|---|---|---|
| `engine/next.config.ts` (+9 lines) | `serverActions.bodySizeLimit = '15mb'` so a camera-resolution hero uploads | Real fix, uncommitted, untested |
| `supabase/migrations/00013_service_role_grants.sql` | `grant select, insert, update, delete` on six tables to `service_role` | **Load-bearing**: without it the engine cannot write a single row. Untracked, so a fresh clone cannot save a horse and CI never sees it |
| `scripts/operator_server.py` + `operator_page.html` | Second operator surface. Python stdlib server on 127.0.0.1:8766, direct PostgREST with the service-role key, no auth, reads `/home/evo/evolution/engine/content/horses` | Violates `OUTCOME.md` ("the only operator screen is the DSL page") and the no-legacy-content-path rule. Must be retired or declared throwaway |
| `SESSION-NOTE-2026-10-23.md` §3 | Claims "core domain decoupling — Horse strictly independent of Trainer and Owner" | **False on disk.** `00004_horses.sql:24-25` holds `trainer_id`/`owner_id`; `00005_dsls.sql` holds neither; `operator_server.py:336-339` PATCHes the horse |

## Step 3 — pricing module

23 claims: **22 PASS, 1 DRIFT, 1 UNGUARDED**.

- DRIFT: `validateStake` compares in integer basis points, not literal float `%`. Behaviour is better (0.3/0.1 accepted) but differs from the stated contract.
- UNGUARDED: "pure functions only" has no test asserting purity or absence of imports.
- Unplanned: `upfrontTotal`, `effectiveMinStake`, extra shared constants, basis-point rounding.

## Step 8a — engine purchase core

19 claims: **19 PASS**, with four untested legs noted (Supabase account mapping, the DSL status/published leg of the checkout gate).

**Unplanned behaviour — three are money-path defects:**

1. **Amount is not reconciled with Stripe.** The webhook never reads `payment_status` or `amount_total`. `metadata[amount_nzd]` is emitted at checkout (`stripe.ts:231`) and never read. The sale row is re-derived from live DSL/account state at webhook time (`purchase.ts:518-544`). Edit the DSL between checkout and webhook and the recorded amount differs from what the card was charged.
2. **No inventory reservation.** `stakeRemaining` is read at quote and again at webhook, and the drawdown is read-then-write (`purchase.ts:546-553`). Two concurrent paid sessions for the last slice can leave one buyer charged with no sale.
3. **`stripe_identity_id` is NULL** on the verified-account path (`purchase.ts:306`) though the sale row spec names an Identity id.

Smaller: `deleteSaleById` throw escapes as a 500; account flipped `pending` only after the Stripe session is created, so a store failure allows a second session.

## Step 9 — emails

26 claims: **25 PASS, 1 PARTIAL**.

- PARTIAL: the "zero bare apex URLs" check covers only `engine/src/lib/email.ts`.
- Fence script is line-shape dependent — a fifth kind declared outside the `EMAIL_KINDS` block is not detected.

**Unplanned behaviour — one real defect:**

- Email send failure **after** the sale row is written throws out of `recordWebhookEvent`. Stripe retries, the retry short-circuits on `idempotentReplay` (`purchase.ts:495-501`), and both sale emails are permanently lost. No retry path exists.

## Step 5 — R2 images

19 claims: **8 PASS, 5 DOC-ONLY, 2 MISSING, 4 gaps**.

- MISSING: **rename does not move the R2 folder.** `OUTCOME.md` and `engine/OPERATIONS.md:96` both claim it. `storage.ts` imports only `PutObjectCommand`; no `CopyObject`, `DeleteObject`, or `ListObjects` anywhere. Images 404 under the new slug.
- MISSING: no Supabase Storage fallback. `storage.ts:217-235` throws when R2 env is absent.
- DOC ONLY: bucket existence, public-read/private-write ACL, CORS — described in `sandbox/v2/r2-config/README.md`, which is outside the repo. No wrangler/terraform file in the repo.
- No KYC upload path exists at all, though KYC files are required.

**Unplanned behaviour — three are integrity defects:**

1. **`image_count` is an operator-editable number field** (`DslForm.tsx:114-121`). A horse can claim 3 images with zero objects in R2 and satisfy the availability trigger.
2. **`imageCountFromKeys` — the only no-gap / no-overwrite validator — is never called in production.** Only `storage.test.ts:285-306` uses it. Uploads trust a stale or hand-edited count and can overwrite an existing key.
3. **Orphaned object on partial failure.** If `PutObject` succeeds and `updateHorse` fails, the object stays, the count does not advance, and the next upload reuses the same number and overwrites it.
4. At HEAD, Next's default 1 MB server-action limit blocks camera-resolution uploads. The uncommitted `next.config.ts` is the fix.

## Step 8b — website buy flow

22 claims: **22 PASS**, but the tests are source-string greps, not render tests.

**Unplanned behaviour:**

1. **`BuyFlowModal` defaults `buyEnabled = true`** (`:67`) and converts it to `canRenderBuyNow(status, 'true')` (`:81`). The component's own gate ignores `WEBSITE_BUY_ENABLED`; only the call site passes the flag. Correct today, one forgotten prop away from selling with the flag off.
2. **Screen 5 renders before Stripe, not after.** The Return screen is selected at `:200` and the redirect fires at `:201`; the real post-checkout return lands on `/mystable`.
3. **`/mystable` isolation rests entirely on RLS.** Neither query filters by user id (`mystable.ts:174-189`). No runtime test proves another user's rows are excluded.
4. No test renders the modal per screen; no test compares the four SA declarations to `PLAN.md:232` (it compares the constant to itself).

## Step 6a — tokens and landing page

13 checklist items: **10 PASS, 2 FAIL-at-HEAD-only, 1 unverifiable**.

The two FAILs are time-scope artefacts, not drift: items 8 and 12 were true at the 6a commit `b4b1e10` and are false at HEAD because later steps legitimately added Supabase clients and restored landing images. The audit unit is the commit, not HEAD — recording this so the report does not double-count them.

Real finding: `globals.css:59` re-declares `--font-serif` and `:218` consumes `var(--font-serif)`, which plan §2/N7 says never to do. Unchanged since `b4b1e10`, so the ban's scope is ambiguous rather than violated.

Minor: Wexford partner mark ships as `.jpg`; the plan names `.png`. Page matches the file.

## Step 1 — repo setup and CI

23 claims: **21 PASS, 2 DRIFT**.

1. **The repo is PUBLIC.** `gh repo view Badders80/engine-v2` → `isPrivate:false, visibility:PUBLIC`. `PLAN.md:252` and `:110` both require private before the first code commit. This is the only finding in the audit that is a live exposure, not just drift.
2. History was rebuilt on an empty root commit `1e69fc9` ("Blank canvas — content removed to restart Step 1 under audit"); the Step 1 payload is the second commit `432f8ab`.

All ten banned tokens are scanned and the script passes (`0 of 10 across 175 files`). Scope is `git ls-files --cached --others --exclude-standard` with `grep -I`, so banned tokens in ignored or binary files are not caught.

## Step 2 — schema and migrations

24 claims: **22 PASS, 2 FAIL**.

1. **`00013_service_role_grants.sql` is not in HEAD.** A fresh apply of HEAD leaves `service_role` with no DML on any table, so every engine write fails `42501`. The migrations 00001–00012 grant it nothing.
2. No SQL in the repo is executed by the suite. `00008` (availability trigger), `00010`, `00011` are graded only by TypeScript mirrors and manual probes in `engine/OPERATIONS.md`. `00009` and `00012` are source-substring assertions. **CI has no database.**

Also: no gate checks unique migration prefixes across the series — `assert-read-policies.sh:101-107` checks only `00009`. Two stale citations: `00009:3` still claims an anon read returns `[]` silently (contradicted by `CONTINUE.md:189-193`); `dsl-save.test.ts:171` cites the wrong line for `stake_remaining`.

## Step 7 — the compiler

23 claims: **22 PASS, 1 FAIL, 1 WARN**.

- **FAIL — the NZTR disclosure check does not exist in the new repo.** `PLAN.md:317` requires the compiler's self-audit to run against `reference/nztr-pro-forma/README.md`. That directory is not in `engine-v2` at all; the only copy is in the **old** repo at `evolution/engine/website/packages/legal_engine/reference/nztr-pro-forma`. No self-audit result is recorded in `engine/OPERATIONS.md`. The compiler interpolates correctly but cannot prove it neither contradicts nor omits a required disclosure.
- WARN: `00011_term_month_boundaries.sql` is a second new migration outside the step-7 plan's fence, which named only `00010`.

Everything else is genuinely strong: token union exhaustive with a static gate, SA proven to contain zero soft keys, renderer throws on unknown tokens and dangling braces, hashes deterministic across compiles, banned-term scan on rendered prose, preview page writes no sale row, and the template files reach the built server via `outputFileTracingIncludes`.

Minor: `foalingLabel` has no direct golden assertion; "pinned" is weaker there than for money and percent.

## Step 6b-i — read policies and website read layer

13 checklist items: **13 PASS**, all four negative constraints verified by script.

The cleanest step in the build. Remaining notes:

1. The credential fence scans `website/src` **only**. `website/.env.example`, `website/next.config.ts`, and the rest of `website/` are unscanned.
2. `00009_website_read_policies.sql:2-4` still carries the stale "anon read returns `[]` and raises no error" comment. The owed correction was disclosed in `PLAN.md:276` and never made.
3. "No `to` clause" and the env-name/throw behaviour rest on inspection, not a test.
4. `assert-read-policies.sh` shipped non-executable and was only fixed in `57c799e`.

## Step 6b-ii — marketplace, horse page, search

18 checklist items: **13 PASS, 5 FAIL**, but four of the five FAILs are later steps outgrowing a literal 6b-ii wording (Buy Now mounted at 8b, `investor_split` added, `accounts`/`sales` reads at 8b, ordering rewritten by a later commit). At commit `f977b04` the step held.

**One genuine defect that survives at HEAD:**

`viewForStatus` in `website/src/lib/status.ts:104-113` guards with `if (!view)` against an object literal. Inherited keys are truthy, so `viewForStatus('toString')`, `'constructor'`, and `'__proto__'` **return a value instead of throwing**. The ruled contract is "a value it cannot translate is an error"; it is not total.

Also worth recording: `LISTING_SELECT` omits all five private categories as required — `about_horse`, `racing_outlook_and_pedigree`, `race_expectation`, `trainers.*`, `owner entity`, `race_record`, `distribution_schedule`.

## Seam audit — the joins between steps

**Five blockers.** These are the findings the per-step audits structurally could not see.

1. **A DSL can be Available and published while its PDS cannot compile.** The trigger checks 5 fields (`00008:19-57`); the compiler additionally requires `distribution_schedule` (`compile.ts:67-72`), the three horse paragraphs and `trainer.bio` (`:74-84`), and every scalar non-empty (`tokens.ts:183-241`). The save gate checks only registration and commercial terms. So the marketplace can take money for a listing whose documents do not exist.
2. **Images are not rechecked at purchase.** `validatePurchaseStake` checks status, published, stake — never `image_count` (`purchase.ts:78-105`). The count is an editable form field, and the trigger fires on `dsls` only, so dropping from 3 to 0 revokes nothing.
3. **Nothing binds the charge to the compiled document.** Checkout quotes at `purchase.ts:359`; the webhook recompiles at `:518` from a fresh read at `:526`; `compileBuyerDocuments` itself reads the DSL twice (`:215`, `:218`). No row version, document hash, or session metadata ties them.
4. **The recorded amount is recomputed, not read from Stripe.** Charged `quote.initialPaymentNzd` (`:365-370`); written from a fresh recomputation (`:531-537`). A price edit between checkout and webhook records a different amount from the charge.
5. **Concurrent webhooks can overdraw `stake_remaining`.** Read at `:526`, absolute write at `:546-551`. No serialization, and no constraint ties `sum(sales.stake)` to `listed_stake`.

**Risks:**

- **App and database disagree on the ceiling price.** `pricing.ts:51-53` ceils the raw JS input; `00005:23-24` rounds to `numeric(10,2)` first. A 1.845 input gives 2 in the app and 3 in the database. The server accepts >2dp; only the client's `step="0.01"` prevents it.
- **No test executes SQL.** Every engine test uses an in-memory store; the in-memory store accepts caller-supplied derived prices, so unit tests certify JS `Math.ceil`, never the generated column.
- **The website page is structurally complete and narrative-empty.** It renders name, hero, status and terms — none of the prose that makes a listing sell.
- A buyer can be charged and end with no sale row: the webhook returns 400 if prose was cleared between checkout and delivery, and Stripe's retries will keep failing while the content stays invalid.

## Step 4 — the DSL page

~20 claims: majority PASS, with five real defects.

1. **Trainer and owner edits are silently discarded.** The edit form shows location, website, bio, contact and profile as editable and prefilled; `resolveTrainer`/`resolveOwner` return the existing row untouched (`dsl.ts:214-215`, `:228-229`). There is no `updateTrainer` or `updateOwner` on the store at all (`dslStore.ts:97-114`).
2. **Changing a trainer's stable or an owner's entity inserts a new row and orphans the old one** (`dsl.ts:214-223`, `:228-236`).
3. **Registration is self-asserted.** Ticking "Registered" during an edit lets an unregistered horse jump to `available` in the same save, with no loveracing link (`dsl.ts:354`, `dsl-edit.test.ts:235-252`).
4. **A loveracing page missing the "Registered" fact is silently treated as unregistered** instead of being refused (`loveracing.ts:183-205`).
5. **Trainer/owner required fields are enforced only in the HTML form**, not in the save action (`actions.ts:112-125`, `dsl.ts:152-168`).

Also: the untracked Python console is a full second writer (POST/PATCH for all four tables), bypassing `dsl.ts` and its registration/status gate entirely. And the DSL read view omits trainer bio and owner profile, so the operator cannot see the text that goes into the PDS.
