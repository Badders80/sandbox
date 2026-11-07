# V2 audit — final report (2026-11-07)

**Question:** is what we think we have what we actually have?

**Answer:** the build is real and unusually well-fenced. It is not what the documents say it is, and it is not yet safe to take money.

- 13 independent audits, ~240 discrete claims checked, every one cited to `file:line`.
- Baseline `pnpm verify` **EXIT=0** on the working tree: 260 engine tests / 16 files, 50 website tests / 5 files, 8 assertion scripts, typecheck, lint, both builds.
- **No SQL is executed by the test suite.** Every database rule is graded by a TypeScript mirror or a manual probe.

Evidence file: `AUDIT-FINDINGS-2026-11-07.md`. DoD for this audit: `AUDIT-DOD-2026-11-07.md`.

---

## 1. The ten things that block the DoD

Ordered by what stops a real sale.

| # | Blocker | Evidence | Class |
|---|---|---|---|
| B1 | **The repo is public.** `Badders80/engine-v2` → `visibility: PUBLIC` | `gh repo view` | exposure |
| B2 | **`00013_service_role_grants.sql` is not committed.** A fresh clone cannot write a single row | untracked; `dslStoreSupabase.ts:38-55` | planned-not-built |
| B3 | **Two definitions of "ready".** The DB gate checks 5 fields; the compiler needs 10. A DSL can be Available, published and buyable while its PDS cannot compile | `00008:19-57` vs `compile.ts:67-84` | built-not-as-specified |
| B4 | **The charge is not reconciled.** Stripe's `amount_total` is never read; the sale amount is recomputed from live DSL state at webhook time | `purchase.ts:365-370` vs `:518-537` | built-not-as-specified |
| B5 | **Nothing binds the quote to the delivered document.** The DSL is read twice at webhook time with no version or hash tie | `purchase.ts:215,218,518,526` | built-not-as-specified |
| B6 | **No inventory serialisation.** Concurrent webhooks can overdraw `stake_remaining`; a buyer can be charged with no sale | `purchase.ts:526-551` | built-not-as-specified |
| B7 | **`image_count` is a hand-typed form field** and purchase never rechecks it. A horse can claim 3 images with zero objects | `DslForm.tsx:114-121`, `purchase.ts:78-105` | built-not-as-specified |
| B8 | **Trainer and owner edits are silently discarded.** The PDS can print a stale bio | `dsl.ts:214-215,228-229` | built-not-as-specified |
| B9 | **The NZTR disclosure check does not exist in the repo.** The reference set is only in the old engine; the required self-audit was never run | `PLAN.md:317` vs no `reference/` | planned-not-built |
| B10 | **The model contradicts the product law.** `OUTCOME.md` says trainer and owner come from the horse; the founder's intent, and `SESSION-NOTE-2026-10-23.md` §3, say they belong to the DSL. The code implements the former | `00004_horses.sql:24-25` | built-not-as-specified |

## 2. Drift — built, but not as specified

| Finding | Evidence |
|---|---|
| `validateStake` compares in basis points, not literal float `%`. Better behaviour, different contract | `pricing.ts:108` |
| Step 4's commit also edited root `pnpm-lock.yaml`, outside its declared `engine/` scope | `99cf0a3` |
| `viewForStatus` fails open on inherited keys: `'toString'`, `'constructor'`, `'__proto__'` return instead of throwing | `status.ts:104-113` |
| `00011` is a second new migration outside the step-7 fence, which named only `00010` | `6237942` |
| App ceiling disagrees with the DB generated column: a `1.845` input gives 2 in the app and 3 in Postgres | `pricing.ts:51-53` vs `00005:23-24` |
| Rename changes the slug but no code moves the R2 folder, contrary to `OUTCOME.md` | `storage.ts` imports only `PutObjectCommand` |

## 3. Unguarded — green, but nothing would catch a regression

- **The database is untested.** `00008` (availability trigger), `00010`, `00011` have no automated test; `00009` and `00012` are graded by string matching. CI has no Postgres.
- **No gate checks unique migration prefixes** across the series; `assert-read-policies.sh:101-107` checks only `00009`.
- **The credential fence scans `website/src` only.** `.env.example` and `next.config.ts` are unscanned.
- **`/mystable` isolation rests entirely on RLS.** No query filters by user id; no runtime test proves another user's rows are excluded.
- **The buy modal defaults `buyEnabled = true`.** Only the single call site passes the flag.
- **No test renders the modal or compares the four SA declarations to `PLAN.md:232`.**
- **Registration is self-asserted.** Ticking it during an edit promotes an unregistered horse to Available in the same save.
- **A trainer/owner stable or entity change inserts a new row and orphans the old one.**

## 4. What is genuinely solid

This is not a failed build. These are production-grade:

1. **The compiler.** Token union exhaustive with a static gate; SA proven to contain zero soft tokens; renderer throws on unknown tokens and dangling braces; hashes identical across compiles; banned-term scan runs on rendered prose.
2. **The money path's shape.** Signature verification with timestamp tolerance over the raw body, idempotency on `stripe_session_id`, frozen documents plus both hashes on the sale row, compensating delete on partial failure, zero emails on decline or replay.
3. **The fences.** Eight assertion scripts, all chained into `pnpm test` and CI. Ten banned legacy tokens, all present and all scanned.
4. **The read layer.** Website reads only `dsls` and joins outward; the projection omits every private field; all four negative constraints hold.
5. **The status/availability vocabulary** and the sitemap set.

## 5. What the audit changes about the plan

**Steps 1–9 + DSL engine is not quite a clean runway.** Three things sit outside that pair:

1. Five of the ten blockers (B4–B7 plus B5) are money-path defects in steps 7–8, not DSL-engine defects.
2. There is no data spine. The six horses exist only as local rows from 2026-10-23.
3. There is no legal proof, and no remote Supabase project, no Stripe keys, no email config, and no Vercel projects for the new apps.

The full precondition table is in `STEP10-PLAN-2026-11-07.md` §4.

## 6. The three artefacts

| File | What it is |
|---|---|
| `AUDIT-FINDINGS-2026-11-07.md` | Every per-step finding with citations, including the five seam blockers |
| `DSL-ENGINE-BRIEF-2026-11-07.md` | What the DSL engine is, what it does today, the eight decisions to close, the content contract, the build order |
| `STEP10-PLAN-2026-11-07.md` | Step 10 re-chunked into 10.0–10.8, each with a gate, plus the precondition table |

## 7. Recommended first three actions on return

1. ~~`gh repo edit Badders80/engine-v2 --visibility private`~~ — **deferred by founder decision 2026-11-07.** The repo stays public until the build is complete so desktop apps can read it; it goes private at cutover. Residual risk accepted: legal templates and business logic are publicly readable, and any secret committed before cutover is exposed.
2. Commit `00013_service_role_grants.sql` — otherwise every downstream proof is fiction.
3. Read `DSL-ENGINE-BRIEF-2026-11-07.md` §3 and answer D1–D8. Nothing else can be planned until the model is decided.

## 8. Claims I could not verify

- That `pnpm verify` is green on a clean `HEAD` checkout. It was green on the dirty tree; the uncommitted files are inert to the suite.
- That any real sale has ever completed end to end on v2.
- That the R2 bucket's public-read and CORS policy match the doc. No IaC exists.
- That the 2026-10-17/23 manual database probes still pass. The local stack was down during this audit.
