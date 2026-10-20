# Step 7 — locked Moment 1 checklist

Locked 2026-10-20 by `kimi-k2.7-code` on `step7-plan.md` at commit `fa24084`. Moment 2 grades the staged diff against exactly these items. The audit returned no FAIL findings and ended `VERDICT: PASS`.

1. The inclusive full-calendar-month helper is single-sourced in `engine/src/lib/term.ts` and used by the save gate, compiler, and preview.
2. `saveDsl` and `updateDsl` refuse `subscription_float` at ≤5 months and accept all legal combos; a refusal leaves the store unchanged.
3. The DSL form auto-selects and locks `upfront` at ≤5 months; server validation is the backstop when JavaScript is off.
4. Migration `00010` enforces the same rule, checks existing rows, and is recorded with a two-direction local probe.
5. The four block files carry the exact ruled text; every legal sentence lives under `engine/src/templates/`.
6. The token union is exhaustive, every key has a resolver, and no extra tokens exist.
7. The SA has zero soft tokens; the PDS has all four; the loader asserts both.
8. The renderer throws on an unknown token and asserts zero dangling braces in both documents.
9. Money, percent, date, and foaling formatting are deterministic and pinned; `foaling_label` carries no age.
10. Required fields throw; `breeder` and `microchip` render `Not recorded`; no other blank reaches a document.
11. The banned list is exactly the ruled list, scanned on rendered prose, case-insensitive and word-bounded; syntax is exempt.
12. The compiler independently enforces the payment-model rule.
13. The two rendered hashes are SHA-256 and identical across repeated compiles of one input.
14. The preview page calls the compiler, renders both documents and hashes, writes no sale row, and is linked from the DSL view.
15. The test matrix covers the 5/6 boundary, 3 and 18 months, both close styles, banned prose, missing soft slots, missing required fields, unknown tokens, and determinism.
16. The static script pins the corpus hashes and joins the root `test` chain.
17. `engine/OPERATIONS.md` records the preview, the template-change procedure, and the DB probe.
18. `outputFileTracingIncludes` is present and the verification proves the templates reach the built server.
19. Each negative constraint in §8 of the plan is falsifiable against the diff.
20. The diff touches only the fence in §11 of the plan.

## Unverified until staged

The auditor marked these consistent-but-unverifiable at Moment 1: the four block-file prose texts, the `00010` SQL body, the static script, the three `engine/src/lib/legal/` modules, the preview page and its link, the build-tracing verification, the §7 test output, and the new `engine/OPERATIONS.md` sections. Moment 2 checks them against the diff.
