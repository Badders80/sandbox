# STATE — v2, one page

Single source for "where are we at". Read this first; it outranks every dated
session note in this folder where they disagree. Update it at the end of each
session, then bump the verification date below.

**Last verified: 2026-11-09** (gate run, DB queried, env inspected, routes listed).

---

## The DoD

One horse sells on v2, end to end, real money, real investor. Everything else is
a precondition. Two structural invariants ride with it (`PLAN.md` § Acceptance):

1. Edit the stake in its one home → listing, PDS, SA and PDF all follow.
2. Rename the horse → URLs, image paths and new documents follow; already-sold
   documents do not.

## Verified state (2026-11-09)

| Fact | Value | How it was checked |
|---|---|---|
| Code head | `0095106` on `main`, 2026-11-07 | `git log -1` |
| Gate | `pnpm verify` **exit 0**, 339 engine / 54 website, both builds | ran it this session |
| Working tree | clean; CI green | `git status`, `gh run list` |
| Repo | `Badders80/engine-v2` **PUBLIC** (ruling: flips at cutover) | `gh repo view` |
| Local DB | `:54422` — **2 horses, 2 DSLs** | psql |
| DSLs | Mulan The Brave `available` + published; Hottathanafantasy `coming_soon` + draft | psql |
| `SUPABASE_URL` | `http://127.0.0.1:54421` — **local only** | `engine/.env.local` |
| `WEBSITE_BUY_ENABLED` | `false` (correct default) | `website/.env.local` |
| Expiry | `ENGINE_EXPIRE_URL` / `ENGINE_EXPIRE_TOKEN` (repo secrets) **unset**; engine env has `ENGINE_EXPIRE_SECRET` | workflow + env |
| Horse create | **no `/horses/new`**; `insertHorse` only called from `engine/src/lib/dsl.ts:460` in `saveDsl` | route list + grep |
| Horse content | **not in `engine_v2`**; the six live in the old engine at `evolution/engine/content/horses/` | find |

One sellable horse already exists, so the DoD does not need six. Six is content
work, not a gate.

## Built vs not

- **Built and gated:** steps 1–9, the DSL engine, and step 10.0 (audit blockers
  B4–B9 closed at `0095106`). Migrations `00001`–`00018`.
- **10.1 partial:** `OUTCOME.md` line 5 and line 89 both say a *five*-minute hold;
  code and ruling say 600s (`00018`). Line 89 also says the webhook repeats the
  decrement; the shipped design reserves at session creation and the webhook
  reads the bound row. Nothing else in the three briefs is stale.
- **10.2 mostly done:** readiness gate, edits persist, three-section UI, images,
  term sheet + Publish all shipped. Two gaps:
  - Item 5 **unproven** — no evidence the website consumes the full projection.
  - Item 7 **unimplemented** — a rename does not move the R2 image folder. This
    is a DoD structural invariant, not a nicety.
- **Not started:** 10.3 data spine, 10.4 legal record, 10.5 money walk, 10.6
  preview deploy, 10.7 visual parity, 10.8 cutover.

## Blockers and open decisions

1. **Hosted Supabase project — head of the critical path.** Needs the founder's
   account/credentials; an agent cannot mint it. Then migrations are applied and
   `SUPABASE_URL` + service-role key are replaced.
2. **The 10.3 fork — undecided.** Build `/horses/new` (~half a day, planning
   estimate) or seed by script and keep horses coupled to `saveDsl`. Recommendation:
   seed, because one buyable horse already exists and the DoD needs one.
3. **R2 public-read / CORS — unknown.** Policy files are in `r2-config/`; no IaC,
   no recorded proof it is applied.
4. **Expiry secrets** must exist before a preview, or holds are never released.
5. **Real investor** — a relationship task with lead time. Start it in week 1, not
   at cutover.
6. **B1 repo public** — ruled: stays public until the DoD, then flips in the
   cutover batch with the key rotations. Not a blocker during the build.
7. **B2/B3 were closed in code** (`00013` tracked at `4dd95d4`; one readiness gate
   at `b61b850`). `CONTINUE.md` still calls B2/B3 "founder rulings outstanding" —
   confirm with the founder before treating them as settled.

## Critical path

`10.1 (two lines) → 10.3 → 10.4 → 10.5 → 10.6 → 10.8`, with 10.7 parallel and
blocking only the founder's eye. Full status table: `STEP10-PLAN-2026-11-07.md` §4–§6.

## If the founder says "go" — ordered work

Estimates are planning estimates, not measurements.

1. Commit the remaining untracked planning docs (`ALIGNMENT-2026-10-23.md`,
   `ALIGNMENT-2026-11-03.md`, `PILOT-MULAN-2026-10-23.md`,
   `SESSION-NOTE-2026-10-23.md`). ~20 min.
2. Close 10.1: fix both hold lines and the webhook sentence in `OUTCOME.md`. ~30 min.
3. Record the fork decision (seed vs `/horses/new`). One call.
4. Create the hosted Supabase project and replace `SUPABASE_URL` + key. Founder.
5. Apply migrations `00001`–`00018` by script; prove a fresh clone reproduces the
   rows. ~2–3 h.
6. Seed one buyable horse (content source: the old engine's `content/horses/`;
   images already in R2). ~1 h.
7. Apply the R2 public-read/CORS policy and record the evidence. ~30 min.
8. Set `ENGINE_EXPIRE_URL` / `ENGINE_EXPIRE_TOKEN` repo secrets. ~10 min.
9. 10.4 — record the NZTR audit output + pack version in `engine/OPERATIONS.md`.
   ~30 min, parallel.
10. 10.5 — local money walk: `stripe listen`, five screens, sale row, frozen
    hashes, four emails, MyStable; then the failure walk (KYC fail, cancel,
    decline, duplicate webhook). Written record, not a claim. ~1 day.
11. 10.6 preview (two Vercel projects, buy flag false, screenshots 1440×900 and
    390×844) and 10.7 visual parity. ~1–2 days.
12. 10.8 cutover — flag on, domain, one real sale, verify hashes/amount/MyStable/
    emails, then the whole key-rotation batch. ~1 day.

The DoD's "real investor" line may need a real person, not a test card. Confirm
before counting a test-mode sale as the gate.

## Verification commands

Fast (about 30 seconds), from this folder:

```bash
cd /home/evo/evolution/engine_v2/website
git log -1 --format='%h %ci %s'; git status --short
gh repo view Badders80/engine-v2 --json visibility -q .visibility
grep '^SUPABASE_URL=' engine/.env.local
ls engine/src/app/horses
PGPASSWORD=postgres psql -h 127.0.0.1 -p 54422 -U postgres -d postgres -tAc \
 "select (select count(*) from horses)||' horses, '||(select count(*) from dsls)||' dsls';"
```

Slow (3–5 min), only if you are going to assert the gate is green:

```bash
cd /home/evo/evolution/engine_v2/website && pnpm verify
```

If ports 54421/54422 are not listening, the local stack is stopped: run
`supabase start` from `engine_v2/website` before trusting the DB rows.

## Recap protocol

When asked "where are we at on evo/sandbox/v2":

1. Read this file.
2. Run the fast checks. Do not trust a stale date.
3. Run `pnpm verify` only if the answer will claim the gate is green; otherwise
   say "last verified 2026-11-09, exit 0".
4. Answer in this order: verified state → DoD → head of the critical path and its
   blocker → open decisions → one next action under two minutes.
5. Never state a count, commit, secret or route unless it came from a command in
   this session or is marked verified here.

## Where each fact lives

| Topic | File |
|---|---|
| Product outcome (wins over everything) | `OUTCOME.md` |
| Working plan and acceptance | `PLAN.md` |
| Step-10 status table, critical path, cutover batch | `STEP10-PLAN-2026-11-07.md` |
| Build log and gate evidence | `/home/evo/evolution/engine_v2/CONTINUE.md` |
| Code | `/home/evo/evolution/engine_v2/website` |
| R2 policy | `r2-config/` |
| Prior sessions | `SESSION-2026-11-07.md`, `SESSION-NOTE-2026-10-23.md` (read for history only) |
