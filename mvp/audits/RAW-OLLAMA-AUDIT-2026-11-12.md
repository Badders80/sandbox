# Raw Ollama audit — PDS/SA package

**Date:** 2026-11-12  
**Auditor:** `kimi-k2.7-code` via direct Ollama `/api/chat` tool loop  
**Target:** engine_v2 headless legal package diff

## Initial verdict — WARN

| # | Claim | Result |
|---|---|---|
| 1 | One combined PDS/SA PDF in a new contract directory | PASS |
| 2 | `ES-DSL-YYYY-NNNNNN` printed and used for directory/object key | PASS |
| 3 | Six-field manifest, no investor identity, full provenance IDs | PASS |
| 4 | PDF/source/template hashes recorded and verified | PASS |
| 5 | Saved-record mode loads DSL/horse/trainer/owner and sale-time terms | PASS |
| 6 | Fixture DOD and `pnpm verify` pass | WARN — DOD not wired into CI |
| 7 | No successful path omits identifiers/hashes or overwrites a package | PASS |

## Repair

`.github/workflows/ci.yml` now:

- installs Python 3.12, ReportLab 5.0.0 and Poppler;
- runs `pnpm verify`;
- runs `bash scripts/legal-package-dod.sh`.

## Re-audit

All three CI claims passed. The re-audit's additional warning claimed
`actions/checkout@v7`, `pnpm/action-setup@v6` and `actions/setup-node@v7` do not
exist. Live `git ls-remote` checks proved that warning false: all three tags
exist.

**Material audit status:** PASS after seam repair; residual model warning is a
verified false positive.

## Additive pricing follow-up

A targeted raw Kimi audit confirmed the TypeScript formula, SQL generated
column, `$100 → $108` case, `$60 → $65` case, and additive PDS/SA wording. It
found one stale operator-doc sentence still describing `1.05 × 1.03`.

`engine/OPERATIONS.md` now states the summed `1.08` rule and the old `$109`
example was corrected to `$108`. Local and hosted databases both report schema
`00030`; the generated expression is `ceil(wholesale_monthly_per_percent * 1.08)`.
