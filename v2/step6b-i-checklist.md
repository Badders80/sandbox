# Step 6b-i — LOCKED CHECKLIST (Moment 1, round 1)

**Verdict: `VERDICT: PASS`.** Locked 2026-10-17 by the independent auditor (`kimi-k2.7-code`, Ollama Cloud, headless).
Audited plan: `/tmp/step6b-i-plan.md` (revision 1). Audit output: `/tmp/step6b-i-m1.out`.
Round 1 graded **no items FAIL** — 27 turns, 102 s. Parts A1–A9 and B1–B7 all satisfied `PLAN.md` and `OUTCOME.md` as they stood at `c4cd581`.

Two drafting notes were raised, neither affecting execution, both repaired in the plan's revision 2 without touching any item below:
(a) §2's heading said "the four policies" while its table correctly lists six — the law rules four *shapes* across six tables;
(b) D8 was labelled `website/package.json` but describes changes to both workspace `package.json` files.

**This checklist is the Moment 2 rubric.** Moment 2 audits the pre-numbered staged diff against these items, one at a time, PASS/FAIL with a `file:line` citation. A dummy citation fails the item.

---

1. `supabase/migrations/00009_website_read_policies.sql` exists and contains exactly six `create policy` statements with the names `trainers_read_public`, `owners_read_public`, `horses_read_public`, `dsls_read_published`, `accounts_read_own`, `sales_read_own`, each using the predicate shape ruled in `PLAN.md:277-280`, and no `to` clause, no `create/drop/alter table`, and no repeated `enable row level security`.
2. No other file under `supabase/migrations/` begins with the prefix `00009`.
3. `website/src/lib/supabaseRead.ts` exists, exports the env-name constants `WEBSITE_SUPABASE_URL` and `WEBSITE_SUPABASE_ANON_KEY`, constructs a Supabase client per call, throws if either env var is missing, and never names or reads a service-role key.
4. `website/src/lib/listings.ts` exists, reads only from `dsls`, joins `horses!inner(...)` for `id`, `slug`, `legal_name`, `registered`, `image_count`, passes the `status` enum value through verbatim with no translation table/label/colour, applies no ordering, and contains no `.from('horses')`, `.from('trainers')`, or `.from('owners')`.
5. `website/.env.example` exists and documents only the two env names in §3-D4, with no values.
6. `scripts/assert-read-policies.sh` exists, is wired into the root `package.json` via a new `test:read-policies` script that is appended to the root `test` chain, and fails CI when the six policy shapes drift or when `website/src/` queries `horses`/`trainers`/`owners` directly.
7. `website/tests/listings.test.ts` exists, runs hermetically with no database driver/connection, tests the listing projection, asserts raw `status` passes through untranslated, and asserts no status label strings or status colours exist under `website/src/`.
8. `engine/OPERATIONS.md` gains a new section documenting `supabase migration up --local` and the recorded anon probe results for `dsls`, `horses`, `accounts`, `sales`.
9. `website/package.json` gains `@supabase/supabase-js`; root `package.json` gains `test:read-policies` and appends it to the `test` chain.
10. No file under `website/src/` imports from `engine/`, and `pnpm-workspace.yaml` is not edited to add a bridge package.
11. No file under `website/` contains a Stripe secret, `SERVICE_ROLE` key, or `sb_secret_` value.
12. No new design tokens, palette additions, or edits to `website/src/app/globals.css`; no new `theme/`/`tokens/`/`design/` directory; no new `AGENTS.md`/`CLAUDE.md`/`HOW-WE-WORK.md`; and the existing pre-commit hook finds no banned legacy tokens in new files.
13. The change lands as exactly one conventional commit on `origin main` of `Badders80/engine-v2`, and `gh run watch --exit-status` exits 0.
