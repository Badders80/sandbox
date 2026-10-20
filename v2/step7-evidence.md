# Step 7 — verification evidence

Recorded 2026-10-20, after the Step 7 commits. Full stdout for each run is in `/tmp`; this file records the outcomes that matter and the hashes proving each falsification was restored byte-for-byte.

## Commits and CI

| Commit | What | CI run | Result |
|---|---|---|---|
| `c7cb159` | float wording, both templates | — | pushed |
| `30fb926` | 7a, payment-model eligibility | `39402608126` | success |
| `40b1a40` | 7b, the legal compiler | `39403685601` | success |
| `6237942` | 7c, month-boundary term dates | `39405544011` | success |
| `85939c6` | 7d, precise term-date messages | `39406874066` | success |

## Gates

| Gate | Log | Exit |
|---|---|---|
| `pnpm verify` on the 7a tree | `/tmp/verify-7a.log` | 0 |
| `pnpm verify` on the 7b tree | `/tmp/verify-7b-final.log` | 0 |
| `pnpm verify` on the 7c tree | `/tmp/verify-7c-final.log` | 0 |
| `bash scripts/assert-legal-templates.sh` | stdout in the 7b session | 0, six checks |
| `sha256sum -c engine/src/templates/SHA256SUMS` | inside the static gate | 0, six files |

Build tracing: `engine/.next/server/app/dsl/[id]/legal/page.js.nft.json` lists all six prose files and `SHA256SUMS`.

## Falsifications

Each break was watched failing, then restored; the SHA-256 after restore matches the value before the break.

| # | Break | Test that failed | Restored file hash |
|---|---|---|---|
| 1 | `checkCommercialTerms` payment check disabled | `dsl-save`: 5-month float refusal | `dsl.ts` `62bc65b5676de9aef2d1b3ffee9f78c5b15d99182affc0892de509cecdb6c0de` |
| 2 | `paymentModelAllowed` widened to 5 months | 3 tests: term rule, save, edit | `term.ts` `9aef817b37bf74386738e41e7cc483420bc67bcdb5893fd01fabf9cc4c545ec2` |
| 3 | `pct()` emitted two decimals | `renders a whole percent without decimals` | `tokens.ts` `965588bede93073bc15016f4ebd78248f8a3305e68abf3c3cd882967721fab16` |
| 4 | dangling-brace assert removed | `throws on a dangling brace the renderer cannot substitute` | `compile.ts` `88678f3fded98291b581d1f6a37fc25a5041b9af177f2c21e8009b7f4fa1cbbd` |
| 5 | `absorb` removed from the banned list | `throws on the word absorb in a soft slot` | `compile.ts` `88678f3fded98291b581d1f6a37fc25a5041b9af177f2c21e8009b7f4fa1cbbd` |
| 6 | month-boundary checks removed from `termMonthsBetween` | 4 tests: mid-month start, mid-month end, same-month reverse, save refusal | `term.ts` `5dbc0e16610ed95ccea534070fa0c4c71046eb85138901e92efda82f698031c8` |

## Database probes (local stack, fixtures removed afterwards)

Migration `00010`, one seeded horse:

```
5-month subscription_float  -> ERROR: a 5-month term must use upfront; subscription_float requires 6 months or more
5-month upfront             -> INSERT 0 1
6-month subscription_float  -> INSERT 0 1
```

Migration `00011`, one seeded horse:

```
2026-01-15 -> 2026-06-30, upfront            -> ERROR: a term starts on the 1st and ends on the last day of a month, and the end must follow the start
2026-01-01 -> 2026-06-15, upfront            -> ERROR: same
2026-03-20 -> 2026-03-01, upfront            -> ERROR: same
2026-06-01 -> 2026-05-31, upfront            -> ERROR: same
2026-01-01 -> 2026-05-31, subscription_float -> ERROR: a 5-month term must use upfront; subscription_float requires 6 months or more
2026-01-01 -> 2026-05-31, upfront            -> INSERT 0 1
2026-01-01 -> 2026-06-30, subscription_float -> INSERT 0 1
```

Both fixtures removed; `dsls` and `horses` returned to 0 rows.

## Audits

| Moment | Output | Verdict |
|---|---|---|
| 1, run 1 | `/tmp/audit.out` | FAIL — two pricing tokens had no call site |
| 1, run 2 | `/tmp/audit.out` (overwritten) | PASS |
| 2, 7a | `/tmp/audit2.out` | PASS |
| 2, 7b | `/tmp/audit2b.out` | PASS |
| 2, 7c, run 1 | `/tmp/audit2c.out` (overwritten) | FAIL — SQL helper lacked the `months >= 1` guard |
| 2, 7c, run 2 | `/tmp/audit2c.out` | PASS |
| 2, 7d, run 1 | `/tmp/audit2d.out` (overwritten) | FAIL — rubric scoping: item 3 bundles the 7a payment lock with the 7d form message |
| 2, 7d, run 2 | `/tmp/audit2d.out` | PASS |

Run 1 of Moment 1 and run 1 of the 7c audit are recorded from the session; their stdout was overwritten by the passing rerun. The defects they found are fixed in `fa24084` and `6237942`.

The locked checklist is `/home/evo/sandbox/v2/step7-checklist.md`.
