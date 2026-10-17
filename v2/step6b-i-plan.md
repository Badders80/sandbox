# Step 6b-i — Read policies and the website's read layer (plan, revision 1)

**Step:** `PLAN.md` § "When you say build" item 6b-i (`PLAN.md:276`). Split from 6b on 2026-10-17 (`PLAN.md:272`).
**Scope:** the repo-root migration series, the `website/` app, the repo-root assertion scripts, and one
section of `engine/OPERATIONS.md`.
**One commit.** One conventional commit, pushed, CI green.

## 0 · Path convention, declared

Every path in this plan is written **repo-root-relative** — `website/src/app/globals.css`, not
`website/website/src/...`. The repo root is `/home/evo/evolution/engine_v2/website`, which holds `engine/`
and `website/` as its two apps (`PLAN.md:199`). Repo-root-relative is what PLAN.md uses (`PLAN.md:274`,
`:184`), what `git diff` emits, and therefore what a Moment 2 citation resolves against.

The 6a plan wrote `website/website/src/` (`step6a-plan.md:108`, `step6a-checklist.md:11`), which is correct
only when read from `engine_v2/`. **That form is not used here.** The auditor is asked to grade this plan's
citations against the repo root, and to hold its own citation form to the same base.

## 1 · Deliverables

| # | Path | What it is |
|---|---|---|
| D1 | `supabase/migrations/00009_website_read_policies.sql` | The four read policies, exactly as ruled |
| D2 | `website/src/lib/supabaseRead.ts` | The website's own Supabase client. Anon key, server-side only |
| D3 | `website/src/lib/listings.ts` | The read functions and the listing projection. Originates at `dsls` |
| D4 | `website/.env.example` | The two environment variable **names**, no values |
| D5 | `scripts/assert-read-policies.sh` | Fails CI if 00009 drifts from the four ruled shapes |
| D6 | `website/tests/listings.test.ts` | Hermetic tests: the projection, and the source-level fences |
| D7 | `engine/OPERATIONS.md` | The apply-and-verify click-path for the policies |
| D8 | both `package.json` files | `website/package.json` gains `@supabase/supabase-js`; the root gains `test:read-policies` |

`pnpm-lock.yaml` will change as a consequence of D8. `PLAN.md:203` excludes it from the audited diff.

## 2 · D1 — the migration

**File:** `supabase/migrations/00009_website_read_policies.sql`. That exact name is ruled (`PLAN.md:276`).
`00009` is the next free prefix: the series on disk ends at `00008_dsl_availability_trigger.sql`, and no two
migrations may share a numeric prefix (`PLAN.md:243`, `:315`).

**It adds policies and the grants that make them reachable** — see §14 for how the grants were found.
All six tables already enable row level security in their own migrations (`00002_trainers.sql:13`,
`00003_owners.sql:13`, `00004_horses.sql:33`, `00005_dsls.sql:44`, `00006_accounts.sql:13`,
`00007_sales.sql:23`). This file creates no table, drops no table, and repeats no
`enable row level security`.

- `select` on `trainers`, `owners`, `horses`, `dsls` → `anon` and `authenticated`
- `select` on `accounts`, `sales` → `authenticated` only

**Four shapes, six policies.** The law rules four *predicate shapes* across six tables (`PLAN.md:277-280`);
one policy per table is what it produces.

| Table | Shape | Policy name |
|---|---|---|
| `trainers` | `for select using (true)` | `trainers_read_public` |
| `owners` | `for select using (true)` | `owners_read_public` |
| `horses` | `for select using (true)` | `horses_read_public` |
| `dsls` | `for select using (published = true)` | `dsls_read_published` |
| `accounts` | `for select using (auth.uid() = id)` | `accounts_read_own` |
| `sales` | `for select using (auth.uid() = user_id)` | `sales_read_own` |

The policy names are this plan's choice; the shapes are the law's. D5 pins the names so they cannot drift.

**No `to` clause, deliberately.** The law writes the shapes without one (`PLAN.md:277-280`), so none is
added. The practical difference is nil: `service_role` bypasses row level security outright, and an
unnamed policy defaults to `to public`, which already covers `anon` and `authenticated`. Adding
`to anon, authenticated` would be a deviation from the literal ruling with no behavioural gain.

**The load-bearing security fact, stated plainly.** `horses_read_public` grants every column of every horse
to `anon`, including unpublished and unregistered rows. That is what the law rules, and the reason it is
safe is `PLAN.md:282`: the site must never query `horses` directly, and must reach it only by joining
outward from `dsls`, where `published` lives. The policy is a deliberate grant; the client rule is the
fence. N1 below is that fence, and D5 and D6 both test it.

## 3 · D2 and D3 — the website's read layer

**D2 — `website/src/lib/supabaseRead.ts`.** The website's first data access. It holds its **own** client:
`PLAN.md:282` forbids importing `engine/` source, so nothing in `engine/src/lib/dslStoreSupabase.ts` is
reused. That module is the shape to imitate, not a dependency.

- Exports the env names as constants: `WEBSITE_SUPABASE_URL`, `WEBSITE_SUPABASE_ANON_KEY`.
- **No `NEXT_PUBLIC_` prefix, deliberately.** These reads happen in server components and route handlers,
  so the key never needs to reach a browser, and keeping the prefix off makes it impossible for Next to
  inline it into a client bundle. A logged-out visitor still reads through the `anon` role, so row level
  security applies exactly as the policies intend.
- The client is constructed per call, not at module load, and **throws** if either variable is missing.
  A silently undefined URL is the failure mode that renders an empty site instead of an error.
- The service-role key is never read, never named, and never referenced here (`PLAN.md:23`, `:282`).

**D3 — `website/src/lib/listings.ts`.** Two reads and one pure projection.

- `listPublishedListings()` — `.from('dsls')`, `.eq('published', true)`. Returns every published DSL,
  including `coming_soon` (`PLAN.md:284`, `OUTCOME.md:29`).
- `getListingBySlug(slug)` — the same origin, `.eq('horses.slug', slug)` via the embedded resource.
- The horse is reached by **embedding**, not by a second query: `dsls` selects `horses!inner(...)`. This is
  a join outward from `dsls`, which is what `PLAN.md:282` requires. A `.from('horses')` anywhere in this
  file is a defect, and D5/D6 fail on it.
- Embedded horse columns are limited to what a listing needs: `id`, `slug`, `legal_name`, `registered`,
  `image_count`. Not the horse's soft prose, not the trainer, not the owner.
- **`status` crosses this boundary raw.** The projection carries the database enum value verbatim as a
  four-member union (`coming_soon | available | fully_allocated | completed`). 6b-i contains **no**
  translation table, **no** label strings, and **no** status colour. That is the seam between 6b-i and
  `PLAN.md:286`'s status map, and D6 asserts the absence so 6b-ii cannot inherit a half-built one.
- The projection is a pure function from a row to a listing view model, so it is testable with a fixture
  and no database.

**No ordering is applied.** Neither `PLAN.md` nor `OUTCOME.md` states a marketplace sort order, and a grep
for one finds nothing. `listPublishedListings()` returns rows in whatever order PostgREST returns them and
the plan says so rather than inventing a rule. The grid's order is a 6b-ii question.

## 4 · D4 — configuration

`website/.env.example` documents the two names with **no values**. `.gitignore` already ignores `.env` and
`.env.*` while whitelisting `!.env.example`, and those patterns match at any depth, so
`website/.env.local` is ignored without touching `.gitignore`.

The values for the local stack come from `supabase status` (API on `127.0.0.1:54421`, per `PLAN.md:243`).
They are written to `website/.env.local` on the operator's machine and **never committed**. No credential,
local or otherwise, appears in any tracked file, in this plan, or in the audited diff.

## 5 · D5 — `scripts/assert-read-policies.sh`

The mechanism that stops the fence from rotting. Without it, a later edit turning `published = true` into
`true` silently publishes every DSL, and nothing in the gate notices. Modelled on the three assertion
scripts already chained into `pnpm test`.

Fails CI when any of these is false:

1. `supabase/migrations/00009_website_read_policies.sql` exists.
2. It contains exactly six `create policy` statements, with exactly the six names in §2.
3. Each policy carries the shape ruled for its table, matched on the table name and the predicate together —
   so `dsls` may not carry `using (true)` and `horses` may not carry a `published` predicate.
4. It contains no `create table`, no `drop table`, no `alter table`, and no repeated
   `enable row level security`.
5. No other file under `supabase/migrations/` begins with `00009`.
6. No file under `website/src/` contains `.from('horses')`, `.from('trainers')`, or `.from('owners')`.

Wired as `test:read-policies` in the root `package.json` and appended to the root `test` chain alongside
`assert-no-anti-patterns.sh`, `assert-operations-doc.sh` and `assert-design-tokens.sh`.

## 6 · D6 — `website/tests/listings.test.ts`

Hermetic. **No test imports a database driver and no test opens a connection** — CI runs `pnpm test` with
no database service, and `PLAN.md:333` keeps the physical check out of the test suite for exactly that
reason. The database is proven by §7's recorded procedure instead.

1. The projection maps a fixture row to the expected view model.
2. The projection does not coerce, default, or invent a `status`: a fixture carrying a value outside the
   four members comes through verbatim rather than being replaced.
3. `website/src/` contains no status label map, no status colour, and no `COMING SOON` / `AVAILABLE` /
   `FULLY ALLOCATED` / `COMPLETED` string. This keeps the `PLAN.md:286` seam real.
4. Every Supabase read in `website/src/` originates at `dsls`; no `.from('horses')`, `.from('trainers')`, or
   `.from('owners')` appears anywhere under `website/src/`.
5. `WEBSITE_SUPABASE_ANON_KEY` is read by name and the service-role key is never referenced anywhere under
   `website/`.

## 7 · D7 — the operator click-path, and the local verification

`PLAN.md:236` makes `engine/OPERATIONS.md` the one operator guide and requires each step to add the
click-path for what it built. 6b-i adds one section:

**Applying the policies to the local stack.** Apply *pending* migrations — `supabase migration up --local`
from the repo root. **Not `supabase db reset`**: that discards whatever the operator has loaded into the
local database, and nothing in this step needs a clean slate.

**The probe, with expected results.** Against `http://127.0.0.1:54421/rest/v1/`, as `anon`:

| Request | Expected |
|---|---|
| `dsls?select=id,published` | only rows with `published = true` |
| `horses?select=id` | rows returned — the policy grants it, which is what lets the outward join resolve |
| `accounts?select=id` | `[]`, and no error raised |
| `sales?select=id` | `[]`, and no error raised |

The last two return `[]` rather than `401` **because a policy exists and denies**, which is the whole point
of `PLAN.md:276`: without this migration an anon read returns `[]` too, but for the wrong reason, and an
empty site looks identical to a working one. The observed output is pasted into the new section, so the
evidence is on disk rather than in a transcript.

## 8 · Negative constraints (each falsifiable against a diff)

- **N1** No `.from('horses')`, `.from('trainers')`, or `.from('owners')` anywhere under `website/src/`.
  Every read originates at `dsls` and joins outward. Grep on the diff. (`PLAN.md:282`)
- **N2** No service-role key, no `SERVICE_ROLE`, no `sb_secret_`, no Stripe key or secret under `website/`.
  Grep on the diff. (`PLAN.md:23`, `:282`)
- **N3** No import specifier resolving into `engine/`, and no new package added to `pnpm-workspace.yaml`
  bridging the two apps. Import-specifier read plus workspace-file diff. (`PLAN.md:282`)
- **N4** No pricing and no compilation in `website/`: no import of `engine/src/lib/pricing`, and no
  reimplementation of the retail formula. The website renders `retail_monthly_per_percent` and
  `wholesale_monthly_total` as stored, never computes them. (`PLAN.md:282`, `:23`)
- **N5** `status` crosses into `website/` as the raw database enum only. No translation table, no label
  string, no status colour, and specifically not the strings `COMING SOON`, `AVAILABLE`,
  `FULLY ALLOCATED`, `COMPLETED`. That is 6b-ii's `PLAN.md:286` map. Grep on the diff.
- **N6** No `AGENTS.md`, `CLAUDE.md`, `HOW-WE-WORK.md`, or any other meta-rule file created anywhere in the
  repo. (`PLAN.md:112`, `:200`)
- **N7** No new directory matching `theme/`, `tokens/`, or `design/`, and no lookbook. No branch other than
  `main`. Path-and-ref check.
- **N8** `00009` creates no table, drops none, and repeats no `enable row level security`. Policies only.
- **N9** No migration file shares a numeric prefix, and no slug-to-id table or slug-to-id lookup is
  introduced anywhere. (`PLAN.md:243`, `:315`)
- **N10** None of the ten banned legacy tokens (`PLAN.md:242`) appears in any new file. The existing
  pre-commit hook already scans tracked and untracked files for these.
- **N11** No new design token, no palette addition, and no edit to `website/src/app/globals.css`. 6b-i
  reuses the 6a theme file unchanged. (`PLAN.md:186`, `:329`)
- **N12** One step, one commit, pushed once. No multi-step execution across a prompt boundary.
  (`PLAN.md:117`)
- **N13** No credential value appears in any tracked file. `website/.env.local` stays ignored, and
  `.env.example` carries names only.

## 9 · Non-orphan consumer wiring

Every deliverable has a consumer, and nothing is pinned ahead of need.

| Introduced | Consumer |
|---|---|
| `00009` and its six policies | The probe in §7, and 6b-ii's pages |
| `website/src/lib/supabaseRead.ts` | `listings.ts` |
| `listings.ts`'s two reads | 6b-ii. **They have no caller in 6b-i.** |
| `assert-read-policies.sh` | The root `test` chain, hence CI |
| `website/tests/listings.test.ts` | The `website` workspace's `vitest run` |
| The `OPERATIONS.md` section | The operator |

**Flagged for the auditor.** `listings.ts` is the one deliverable with no in-step call site: 6b-i ships a
read layer and 6b-ii renders it. The alternative is folding the read layer into 6b-ii, which would put the
migration and its only consumer in the same diff and make the policies unverifiable in isolation. If the
auditor rejects the split, name which deliverable to cut and the founder decides.

## 10 · Local verification protocol

`pnpm verify` from the repo root — exit code 0, `--max-warnings=0` (`PLAN.md:202`). It runs typecheck, lint
in both workspaces, the four assertion scripts, both workspaces' vitest suites, and both builds.

Then §7's local-stack probe, recorded in `engine/OPERATIONS.md`. It is a logged manual procedure, not a CI
test, and it is the only evidence in this step that touches a database.

## 11 · Audit and push gate

**Moment 1 — this plan, before a line is written.** `kimi-k2.7-code` via Ollama Cloud, headless,
stdout/stderr split, blocking wait with a 15-minute timeout, timeout = FAIL, verdict read from the **last
non-empty line** of `.result`. It returns the numbered checklist that Moment 2 then grades against.
`PLAN.md:203` carries the explicit exemption for `engine/OPERATIONS.md` prose within scope-leakage checks.

**Moment 2 — the staged diff, after `pnpm verify` exits 0.** `git diff --cached -- . ':(exclude)pnpm-lock.yaml'`,
pre-numbered with `nl -ba` before dispatch, same model and protocol. Every item graded PASS or FAIL with a
non-dummy `file:line` citation; a citation that does not say what it claims fails its item.

**Then:** one conventional commit, `git push origin main` from `/home/evo/evolution/engine_v2/website`
(`origin` is `Badders80/engine-v2`, not the sandbox planning repo), then `gh run watch --exit-status`.
(`PLAN.md:204`)

## 12 · Scope fence, resolved

The step brief's fence is not restated here; `PLAN.md:276-282` defines 6b-i and it touches four locations:

1. `supabase/migrations/` at the repo root — where the series already lives.
2. `website/` — the app, its lib, its tests, its env example, its `package.json`.
3. `scripts/` at the repo root — where the three existing assertion scripts live and where the root `test`
   chain already looks.
4. `engine/OPERATIONS.md` — **the one location that can be read as leaking into `engine/`.**

The fourth is deliberate, and it is the only item here a reasonable reader could call scope leakage.
`PLAN.md:236` names `engine/OPERATIONS.md` as the single operator guide and requires each step to add the
click-path for what it built; `PLAN.md:203` exempts that file's prose from scope-leakage checks. It is
documentation, not code, and no `website/` file imports from it. **If the auditor reads the fence as
`website/`-and-schema only, D7 drops and that is the only change.**

## 13 · Still parked

- **The physical trigger check** (`PLAN.md:333`). It says verify against the local stack *before the first
  listing goes live*. The first listing is 6b-ii, so this stays parked and becomes 6b-ii's gate. It must
  stay out of `engine/tests/`.
- **The horse-side Available gate** (`PLAN.md:330`) — the constraint trigger fires on `dsls` writes only,
  so clearing a horse's `registered` or dropping `image_count` below three leaves an Available DSL
  standing. Not 6b-i; the horse editor is later.
- **`effectiveMinStake` wired to nothing** (`PLAN.md:332`) — becomes load-bearing at step 8.
- **No new tokens past 6a** (`PLAN.md:329`) — N11 keeps 6b-i inside the existing theme file.
- **Observability vendor and the email sender** (`PLAN.md:326`) — before the public buy path, not before
  this commit.

## 14 · Repair ledger — revision 1 → revision 2

Revision 1 passed Moment 1 with no FAILs. Revision 2 changes three things. Two are the drafting notes the
auditor raised; the third is a defect the step's own verification found, disclosed here rather than
buried in the diff.

| Found | Repair |
|---|---|
| §2's heading read "the four policies" while its table lists six | Reworded: four *shapes*, six tables (`PLAN.md:277-280`) |
| D8 was labelled `website/package.json` but covers both workspace manifests | Relabelled "both `package.json` files" |
| **A policy with no matching GRANT is inert** | Six `grant select` statements added to `00009`, and `assert-read-policies.sh` now fails if any disappears |

**How the third one surfaced.** §7's probe was run against the local stack with a fixture, because the
database was empty and an empty probe proves nothing. The first run failed outright:

```
{"code":"42501","message":"permission denied for table dsls",
 "hint":"Grant the required privileges to the current role with: GRANT SELECT ON public.dsls TO anon;"}
```

Supabase sets default privileges on schema `public` twice — for `supabase_admin` and for `postgres` — and
the `postgres` set grants `anon` and `authenticated` only `Dxtm`, with no `r`. Every table in this series
was created by `postgres`, so table-level select was never granted, and row level security was never even
reached. The grant is therefore part of making the ruling real; the migration adds it.

**This also corrects a premise in the law.** `PLAN.md:276` says that because every table is
deny-by-default, *"an anon read returns `[]` with no error raised"*. It does not. It raises `42501`, both
before and after the policies land, because the failure is at the grant layer. The law's conclusion — that
00009 is the first deliverable and nothing works without it — stands unchanged; only its account of the
symptom was wrong. **A `PLAN.md` correction is owed and is not made in this step**, since this step's diff
should not carry a law edit; it is recorded here for the founder to rule on.

**Falsification.** Both new fences were proven to go red before being trusted: widening `dsls` to
`using (true)` fails the script, adding a direct read of `horses` fails the script and the test suite, and
removing one grant fails the script. Each was restored and re-run green.
