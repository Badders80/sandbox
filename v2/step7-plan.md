# Step 7 — The legal compiler (plan, revision 1)

**Step:** `PLAN.md` § "When you say build" item 7 (`PLAN.md:306`), against the legal authority (`PLAN.md:27-82`) and the positive rules locked 2026-10-20 (`PLAN.md:69-82`).
**Scope:** the `engine/` app, one new migration, the repo-root `scripts/` and `package.json`, and `engine/OPERATIONS.md`. **No file under `website/` changes.**
**One commit?** No. Two commits, both gated: **7a — payment-model eligibility** (code, migration, tests) and **7b — the compiler** (templates, compiler, preview, tests). 7a lands first because the compiler asserts the rule 7a enforces.

## 0 · Path convention, declared

Every path is repo-root-relative. The repo root is `/home/evo/evolution/engine_v2/website`, which holds `engine/` and `website/` as its two apps (`PLAN.md:11`). A Moment 2 citation resolves against that base.

The legal prose lives in `engine/src/templates/`. The compiler lives in `engine/src/lib/legal/`. Neither is imported by `website/`.

## 1 · Deliverables

| # | Path | What it is |
|---|---|---|
| D0 | `engine/src/lib/term.ts` | **One** inclusive full-calendar-month helper, plus the payment-model predicate |
| D1 | `engine/src/lib/dsl.ts` | **Amended.** Save and edit refuse `subscription_float` at ≤5 months |
| D2 | `engine/src/app/dsl/PaymentModelField.tsx`, `engine/src/app/dsl/DslForm.tsx` | **New client field + amended form.** Upfront is auto-selected and locked at ≤5 months |
| D3 | `supabase/migrations/00010_payment_model_eligibility.sql` | The same rule at the database, plus a check over existing rows |
| D4 | `engine/src/templates/blocks/pds-costs-summary.float.md`, `.upfront.md`, `pds-close-style.fourteen-day.md`, `.three-x-remaining.md` | The four model/branch texts the two templates delegate to their block tokens |
| D5 | `engine/src/templates/SHA256SUMS` | The pinned hashes of the six legal prose files |
| D6 | `engine/src/lib/legal/tokens.ts` | The token union, the resolver map, and the formatters |
| D7 | `engine/src/lib/legal/templates.ts` | The loader, block selection, and the static corpus checks |
| D8 | `engine/src/lib/legal/compile.ts` | Render, validate, hash, return the pack |
| D9 | `engine/src/app/dsl/[id]/legal/page.tsx`, `engine/src/app/dsl/[id]/page.tsx` | The preview page (the non-orphan consumer) and its link |
| D10 | `engine/tests/term.test.ts`, `legal-templates.test.ts`, `legal-compile.test.ts`; `dsl-save.test.ts`, `dsl-edit.test.ts` | Hermetic tests; no database driver |
| D11 | `scripts/assert-legal-templates.sh`, `package.json` | The static legal gate, added to the root `test` chain |
| D12 | `engine/OPERATIONS.md` | The preview click-path, the template-change procedure, the payment rule, the DB probe |
| D13 | `engine/next.config.ts` | `outputFileTracingIncludes` so the templates ship with the built server |

`pnpm-lock.yaml` is not expected to change. No dependency is added.

## 2 · The authority, restated

The two templates are the document authority (`PLAN.md:29-31`). Their fixed text is law; only `{{tokens}}` are data. The compiler is a deterministic interpolator; it does not generate, paraphrase, or improve prose.

Two tokens are **block tokens**, not scalar values:

- `{{pds.costs_summary_block}}` — the Key Information Summary costs list; branches on `payment_model`.
- `{{pds.close_style_block}}` — the PDS §6 exit paragraph; branches on `close_style`.

D4 puts each branch in its own Markdown file. That keeps every legal sentence in `engine/src/templates/`, not in a TypeScript template literal. The compiler selects a block, renders its tokens, then injects the result into the template and renders the rest. A block file with an unknown token fails the same way a template does.

## 3 · D0 and D1 — the payment-model rule

**The ruling, locked 2026-10-20 (`OUTCOME.md:48`, `PLAN.md:72`):**

- `upfront` is available for **any** term.
- A term of **5 months or less must use `upfront`**.
- A term of **6 months or more may use either**, defaulting to `subscription_float`.

**The reason, stated once.** At ≤5 months the five-month initial payment already covers the whole term; a float would over-collect and refund by construction. At 6+ months the initial 5M is less than the term and the float is doing the job it exists for. The boundary is the float size, not a claim that the float is impossible.

**`engine/src/lib/term.ts`:**

```ts
/** Inclusive full-calendar months between two ISO dates. null on bad input. */
export function termMonthsBetween(startIso: string, endIso: string): number | null {
  // (endYear - startYear) * 12 + (endMonth - startMonth) + 1
}

/** True when the requested model is legal for the term. */
export function paymentModelAllowed(paymentModel: PaymentModel, termMonths: number): boolean {
  return paymentModel === 'upfront' || termMonths >= 6
}
```

The formula is the old one, `term_sheet.ts:55-61`, copied into v2 because v2 has no term helper and must not import the old package.

**D1, `engine/src/lib/dsl.ts`:** in `checkCommercialTerms` (`:173`), after the stake-shape check:

- `const months = termMonthsBetween(dsl.termStart, dsl.endDate)`
- `months === null` → `{ ok: false, reason: 'term dates are invalid' }`
- `months < 1` → refuse.
- `dsl.paymentModel === 'subscription_float' && months <= 5` → refuse with the exact reason: `a ${months}-month term must use upfront; subscription_float requires 6 months or more`.

This is shared by `saveDsl` (`:239`) and `updateDsl` (`:327`) because both call `checkCommercialTerms`. A refusal happens before any row is written, so the store is unchanged.

**D2, the form:** `PaymentModelField.tsx` is the only client component. It renders the select and listens to `termStart` and `endDate` in the same form. At ≤5 months it forces `upfront` and disables the select; above 5 it enables both, leaving `subscription_float` as the default. With JavaScript off, D1 still refuses the illegal combination on submit. The field is used in `DslForm.tsx` in place of the inline select at `:240-243`.

**D3, the database:** `00010_payment_model_eligibility.sql` adds a `before insert or update of payment_model, term_start, end_date` trigger on `public.dsls`. The trigger computes the same inclusive months and raises when `payment_model = 'subscription_float'` and `months <= 5`. The migration first raises if any existing row already violates the rule, so the database cannot be left in a state the trigger would refuse to reproduce.

**Test contract (D10):** 3/4/5-month float refused; 5-month upfront accepted; 6-month float and upfront accepted; 18-month upfront accepted; invalid dates refused; `updateDsl` moving an existing float to a 5-month term refused with the store unchanged.

**Local probe (D12):** against the local stack, with a seeded fixture and the fixture removed afterwards: a 5-month `subscription_float` write is **refused**; the same row as `upfront` is **accepted**; a 6-month float is **accepted**. Recorded in `engine/OPERATIONS.md`, not in `engine/tests/`, which stays hermetic (`PLAN.md:350`).

## 4 · D6 — the token contract

Every token in the two templates and the four block files resolves from one declared key union. `TOKEN_KEYS` is a `const` array; `TokenKey` is its union; `RESOLVERS` is `Record<TokenKey, (input: LegalPackInput) => string>`, so TypeScript fails if a key has no resolver.

| Token | Source or derivation |
|---|---|
| `account.full_name` | `accounts.full_name` at sale; a preview input in D9 |
| `dsl.campaign_slug` | `horse.slug` — the campaign is the horse's public page |
| `dsl.distribution_schedule` | `dsls.distribution_schedule`, **required**; no default is invented |
| `dsl.end_date` | `dsls.end_date`, ISO `YYYY-MM-DD` |
| `dsl.investor_split` | `dsls.investor_split`; **required** (the availability trigger already refuses null at `available`) |
| `dsl.listed_stake`, `dsl.min_stake`, `dsl.step` | the DSL values, percent without `%` |
| `dsl.owner_retention_split` | `100 - investor_split`, percent without `%` |
| `dsl.payment_model_label` | `Upfront` or `Monthly (subscription float)` |
| `dsl.term_months` | `termMonthsBetween(term_start, end_date)` |
| `dsl.term_start` | `dsls.term_start`, ISO |
| `horse.about_horse`, `horse.racing_outlook_and_pedigree`, `horse.race_expectation` | the three soft columns, **required non-empty** |
| `horse.breeder`, `horse.microchip` | nullable columns; `Not recorded` when null or empty |
| `horse.colour`, `dam_name`, `sex`, `sire_name`, `legal_name` | required |
| `horse.foaling_label` | `foaling_date` formatted `30 Aug 2023` — **date only**, never an age, so the hash is stable |
| `owner.entity_name` | `owners.entity` |
| `pricing.monthly_lease_payment_unit_nzd` | `money(dsl.retail_monthly_per_percent)` |
| `pricing.float_per_percent_nzd` | `money(floatTotal(retail, 1))` — the 3+2 initial per 1% |
| `pricing.upfront_per_percent_nzd` | `money(upfrontTotal(termMonths, retail, 1))` |
| `sale.executed_date` | the sale date, ISO |
| `sale.initial_payment_nzd` | `money(floatTotal(retail, stake))` or `money(upfrontTotal(termMonths, retail, stake))` |
| `sale.monthly_payment_nzd` | `money(retail * stake)` |
| `sale.stake_pct` | the sale stake, percent without `%` |
| `syndicate.name` | `${horse.legal_name} Syndicate`, the old derivation (`rehearse-dsl-prod.ts:57`) |
| `syndicate.version` | `LEGAL_PACK_VERSION = '1.0.0'`, one constant in `tokens.ts` |
| `trainer.bio`, `trainer.location`, `trainer.name` | the trainer row; `bio` is **required non-empty** |
| `pds.costs_summary_block`, `pds.close_style_block` | D4 block selection; not scalar |

**Formatters** are local and deterministic:

- `money(n)` → `$71.00`, `$1,775.00`; `Intl.NumberFormat('en-NZ', { style: 'currency', currency: 'NZD' })`.
- `pct(n)` → `2.5`, `2`, `0.1`; two decimals maximum, trailing zeros trimmed. The templates add `%`.
- `isoDate(s)` → validates `YYYY-MM-DD` and returns it unchanged.
- `foalingDate(s)` → `30 Aug 2023` from a fixed month array; no locale call, no age.

**No blank markers.** Every scalar token must be non-empty, except `breeder` and `microchip`, which use `Not recorded`. A missing required value throws with the field name; it never renders a blank into a signed document.

## 5 · D7 and D8 — load, render, validate, hash

**`templates.ts`:**

- `LEGAL_DIR = path.join(process.cwd(), 'src/templates')` when the engine app runs; the loader is called only from the engine app and its tests.
- `loadLegalCorpus()` reads the two templates and the four block files, throws on a missing file, and returns raw text plus SHA-256 per file.
- `selectCostsBlock(paymentModel)` and `selectCloseBlock(closeStyle)` throw on an unknown branch; there is no silent default.
- Static checks at load: the SA raw text contains **none** of the four soft tokens; the PDS raw text contains **all four**; every `{{...}}` in the corpus is in `TOKEN_KEYS`; no `{{`/`}}` imbalance.

**`compile.ts`:**

```ts
export type LegalPack = {
  pds: { markdown: string; hash: string }
  sa:  { markdown: string; hash: string }
  templateHashes: Record<string, string>
  version: string
}

export function compileLegalPack(input: LegalPackInput): LegalPack
```

Order, which is the contract:

1. Validate the input: term months, payment-model rule, investor split present, distribution schedule present, four soft slots non-empty, required horse/trainer/owner/account/sale fields present.
2. Load the corpus; hash the templates.
3. Render the selected blocks with the scalar values.
4. Insert the rendered blocks into the two templates as the two block-token values.
5. Render the templates with the same scalar map.
6. Assert zero `{{...}}` remains in either document, and assert no `{{` or `}}` at all.
7. Scan both rendered documents for banned prose.
8. Return the two Markdown strings, their SHA-256 hashes, and the template hashes.

**Strict substitution.** One regex, `/\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}/g`. Unknown key → throw with the key. No `?? ''`, no default, no recursion beyond the explicit block-first pass.

**Banned prose**, case-insensitive, word-bounded where the term is a word:

```
Tokinvest
\bVARA\b
digital\s+token
\btokenis(?:ed|ing)\b
\btokens?\b
fair\s+value
\b14\s+business\s+days\b
\babsorb(?:ed|ing|s)?\b
```

The scan runs on **rendered prose**, not on template syntax or code identifiers. A soft column containing a banned term fails the compile; that is intended — the operator edits the copy.

**The payment-model assertion in the compiler** is a backstop, not the primary gate: `subscription_float` with `termMonths <= 5` throws before any document is produced.

**D9, the non-orphan consumer.** `engine/src/app/dsl/[id]/legal/page.tsx` is a dynamic server page:

- Loads the DSL view through the existing `loadDslView(id)` (`engine/src/app/dsl/data.ts`).
- A GET form takes `stake`, `buyer`, and `date`; defaults are `min_stake`, `Preview`, and today's ISO date.
- Validates the stake with `validateStake` and the listed/remaining bounds.
- Calls `compileLegalPack` and renders the two documents in `<pre>` with their hashes.
- Writes no sale row, creates no PDF, and is labelled **preview only**.
- `engine/src/app/dsl/[id]/page.tsx` gains one link to it.

This is the production call site the protocol requires (`PLAN.md:178`). Step 8 replaces the preview inputs with the real account and sale, and writes `pds_markdown`, `sa_markdown`, `pds_hash`, `sa_hash` to `sales` (`00007_sales.sql`).

**D13, build tracing.** `engine/next.config.ts` gains:

```ts
outputFileTracingIncludes: { '/*': ['./src/templates/**/*.md'] }
```

The verification runs `pnpm --filter engine build` and then confirms `SA.template.md` and `PDS.template.md` are present in the build output's traced files. Without it, the preview route would work under `next dev` and fail in a deployed server with `ENOENT`.

## 6 · D11 — the static gate

`scripts/assert-legal-templates.sh`, added to the root `test` chain next to the five existing scripts:

1. The two templates and four block files exist.
2. `sha256sum -c engine/src/templates/SHA256SUMS` passes — any legal-prose edit is deliberate and updates the manifest.
3. No banned term appears in the raw corpus.
4. The SA raw text has zero soft tokens; the PDS raw text has all four.
5. Every `{{...}}` is in `TOKEN_KEYS` (the list is duplicated in the script as fixed strings), and braces are balanced.
6. `engine/src/lib/legal/` is imported by the preview page and by the compiler tests (non-orphan wiring).

The script prints one `ok`/`FAIL` line per check and exits non-zero on any FAIL, matching `assert-read-policies.sh`.

## 7 · D10 — the tests

**`term.test.ts`:** inclusive months: Jan 1→May 31 = 5; Jan 1→Jun 1 = 6; Jan 15→Jun 30 = 6; 18-month case; same month = 1; invalid dates = null; `paymentModelAllowed` truth table.

**`legal-templates.test.ts`:** corpus presence; pinned hashes; token contract; SA zero soft / PDS four; banned corpus scan; block files present and each branch selectable.

**`legal-compile.test.ts`:** the fixture matrix:

| Case | Expect |
|---|---|
| 21-month float | renders; PDS contains the four soft texts; SA contains none; no `{{`; costs block is the float branch |
| 18-month upfront (Prudentia shape) | renders; costs block is the upfront branch; `upfront_per_percent_nzd = 18 × rate` |
| 5-month upfront | renders |
| 5-month float | throws with the payment-model reason |
| 6-month float | renders |
| 6-month upfront | renders |
| 3-month float | throws |
| 3-month upfront | renders |
| missing soft slot | throws naming the column |
| banned term in soft prose | throws naming the term |
| unknown token in a test template | throws naming the token |
| null breeder / microchip | renders `Not recorded` |
| null investor_split / distribution_schedule | throws |
| both close styles | the correct block text appears; the other does not |
| two compiles of one input | identical markdown and hashes |
| hash | equals `sha256(markdown)` |

No test opens a connection; no test imports a database driver. The engine suite stays hermetic, as it is today.

**Additions to `dsl-save.test.ts` / `dsl-edit.test.ts`:** the D1 matrix, including the store-unchanged assertion on refusal.

**Source assertion:** `legal-templates.test.ts` reads `engine/src/app/dsl/[id]/legal/page.tsx` and asserts it imports `compileLegalPack`. That is the non-orphan fence, in the style already used by `dsl-images.test.ts`.

## 8 · Negative constraints (each falsifiable against a diff)

- No new dependency. No template engine, date library, or Markdown library.
- No import from `engine/website/...`, `sandbox/rebuild`, `legal_engine`, or `engine/website/docs/legal-foundation/`.
- No file under `website/` changes.
- No PDF, no cover page, no signature image (parked).
- No sale-row write in Step 7; the preview writes nothing.
- No AI prose generation. The compiler emits template text and resolved values only.
- No default investor split. A null split throws.
- No blank marker in a document. `Not recorded` is used only for `breeder` and `microchip`.
- No `absorb`, `Fair Value`, `14 business days`, `Tokinvest`, `VARA`, `token`, `tokens`, `tokenised`, or `digital token` in rendered prose.
- No `{{` or `}}` in either rendered document.
- No direct read of `horses`, `trainers`, or `owners` from `website/`; the engine app may read them through its store.
- No branch other than `main`. No `AGENTS.md`, `CLAUDE.md`, or `HOW-WE-WORK.md`.

## 9 · Verification protocol

1. `pnpm verify` from the repo root, exit 0, `--max-warnings=0`.
2. Falsifications, each broken, watched failing, restored, and verified byte-for-byte:
   - remove the payment-model check from `checkCommercialTerms` → the 5-month float test fails;
   - widen `paymentModelAllowed` to allow float at 5 → the same test fails;
   - change `pct()` to emit a trailing `.00` → the golden test fails;
   - remove the dangling-token assert → the unknown-token test fails;
   - add `absorb` to a soft fixture → the banned-prose test fails.
3. `pnpm --filter engine build`, then confirm both templates are in the traced output (D13).
4. The local DB probe for `00010`, both directions, recorded in `engine/OPERATIONS.md`.
5. `engine/src/templates/SHA256SUMS` verifies after every restore.

## 10 · Audit and push gate

**Moment 1 — this plan, before a line is written.** `kimi-k2.7-code` via Ollama Cloud, headless, stdout/stderr split, blocking wait under 900 s, timeout = FAIL, verdict read from the **last non-empty line** of `.result`, parsed as JSON and tested for equality. Never by substring. It returns the numbered checklist that Moment 2 grades against.

**Moment 2 — the staged diff, after `pnpm verify` exits 0.** The diff is pre-numbered before dispatch. Every item is graded PASS/FAIL with a non-dummy `file:line` citation. Prose in `engine/OPERATIONS.md` is exempt from scope-leakage checks (`PLAN.md:181`).

**Then:** two conventional commits on `main` (`7a` eligibility, `7b` compiler), each pushed, each with `gh run watch --exit-status`. The law edits already made in `OUTCOME.md` / `PLAN.md` live in `Badders80/sandbox-v2`, not in the build diff.

## 11 · Scope fence, resolved

Touched locations:

1. `engine/` — source, tests, templates, Next config.
2. `supabase/migrations/00010_...` — one new migration, no edit to 00001-00009.
3. `scripts/assert-legal-templates.sh` and the root `package.json` test chain.
4. `engine/OPERATIONS.md` — the operator guide.

Nothing else. If the auditor reads the migration as outside Step 7, D3 drops and the application gate remains, but the database can then be written around the rule; that is the only change.

## 12 · Rulings locked

1. **Payment models.** Upfront any term; ≤5 months must be upfront; ≥6 months either, defaulting to float (`OUTCOME.md:48`, `PLAN.md:72`). The reason is the five-month initial payment, not an impossibility claim.
2. **The templates are the document authority.** Two templates, four block files, no prose in TypeScript.
3. **No legacy copy.** The five files in `engine/website/docs/legal-foundation/` are not imported or copied.
4. **The float wording.** "A 5-month float buffer, drawn down in the final months of the term" replaces "constant" (`SA.template.md:63`, `PDS.template.md:101`).
5. **Hashes at sale.** The rendered Markdown and SHA-256 are the frozen artifact; a later edit to the horse cannot change a sold document (`OUTCOME.md:35`; `PLAN.md:312, 316`).

## 13 · Still parked

- The buy path and the sale-row write — Step 8.
- The PDF renderer, cover page, and signature image — future render work.
- `effectiveMinStake` wiring — Step 8.
- The partial-failure chaos test on `saveDsl` — with the horse editor.
- The horse-side Available gate — with the horse editor.
- The marketplace split/reserve copy gap (`website/src/app/page.tsx:29,50`; `marketplace/page.tsx:119`) — a `website/` change, not Step 7.

## 14 · Moment 1 checklist proposal

The auditor may repair, split, or reject any item, but the final list must cover:

1. The inclusive-month helper is single-sourced and used by the save gate, the compiler, and the preview.
2. `saveDsl` and `updateDsl` refuse float at ≤5 months and accept all legal combinations; refusals leave the store unchanged.
3. The form auto-selects and locks upfront at ≤5; server validation is the backstop when JavaScript is off.
4. Migration `00010` enforces the same rule, checks existing rows, and is recorded with a two-direction local probe.
5. The four block files carry the exact ruled text; every legal sentence is in `engine/src/templates/`.
6. The token union is exhaustive, every token has a resolver, and there are no extras.
7. The SA has zero soft tokens; the PDS has all four; the loader asserts both.
8. The renderer throws on an unknown token and asserts zero dangling braces.
9. Money, percent, date, and foaling formatting are deterministic and pinned.
10. Required fields throw; `breeder`/`microchip` render `Not recorded`; no blank markers elsewhere.
11. The banned list is exactly the ruled list, scanned on rendered prose, case-insensitive, word-bounded.
12. The compiler independently enforces the payment-model rule.
13. The two rendered hashes are SHA-256 and identical across repeated compiles.
14. The preview page calls the compiler, renders both documents and hashes, writes no sale row, and is linked from the DSL view.
15. The tests cover the full matrix in §7, including both close styles and the 5/6 boundary.
16. The static script pins the corpus hashes and joins the root `test` chain.
17. `OPERATIONS.md` records the preview, the template-change procedure, and the DB probe.
18. The build traces the templates into the deployed server.
19. Each negative constraint in §8 is falsifiable against the diff.
20. The diff touches only the fence in §11.

The last line of the audit reply must be exactly `VERDICT: PASS` or `VERDICT: FAIL`.
