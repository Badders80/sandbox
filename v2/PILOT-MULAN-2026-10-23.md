# Mulan pilot — local execution runbook

Written 2026-10-23. **Executed 2026-10-23 through the operator UI.** This is the first vertical
slice: one horse entered through the engine's own DSL page, visible on the local marketplace.

## Run log (2026-10-23)

| # | Result |
|---|---|
| 1 | `service_role` had no DML grants. Saving failed: `horses: permission denied for table horses`. Fixed by `supabase/migrations/00013_service_role_grants.sql`. |
| 2 | First image upload failed: `Body exceeded 1 MB limit` (hero is 1.1 MB). Fixed in `engine/next.config.ts`: `serverActions.bodySizeLimit = '15mb'`. |
| 3 | `/dsl/new` saved Mulan: 1 trainer, 1 owner, 1 horse, 1 DSL. Slug derived as `mulan-the-brave-nz`. Retail generated as 65. |
| 4 | Three images uploaded through `/dsl/[id]` → `mulan-the-brave-nz/01..03`, all public on R2 with correct content types. `image_count = 3`. |
| 5 | `/marketplace` renders the COMING SOON card; `/marketplace/mulan-the-brave-nz` renders with the R2 hero. |
| 6 | Setting `available` without a split was refused by the trigger: `cannot be available: investor_split is null`. Correct. |
| 7 | The loveracing.nz link loader returned 403 against the live site. The horse was typed by hand. |

## What "execute a DSL" actually means here

- The engine is a Next.js operator app on **port 3001**. `/dsl/new` writes the horse, trainer,
  owner, and DSL rows in one save, using the service-role key against the local Supabase.
- The website is a Next.js app on **port 3000**, reading local Supabase through the anon key and
  the `00009` read policies.
- Images are **not** copied into a folder. The upload form on `/dsl/[id]` writes
  `{slug}/{NN}` into the R2 bucket `evolution-v2-horse-images`; the database stores only
  `image_count`. No extension, no path column.
- After three images, `available` becomes legal. The trigger checks images, split, price,
  registration, and `published`.

## Verified preconditions

| Check | Result |
|---|---|
| Local Supabase | running; REST `127.0.0.1:54421`, DB `54422` |
| Migrations | `00001`–`00012` applied |
| Tables | `accounts dsls horses owners sales trainers`; **0 rows each** |
| Triggers | `dsls_available_invariants`, `dsls_payment_model_eligibility`, `on_auth_user_created` |
| Mulan content | `profile.md`, `pedigree.json`, `race-record.json` present |
| Mulan images | `01.png`, `02.webp`, `03.jpg` in `evolution/engine/website/apps/web/public/horses/mulan-the-brave/` |
| Engine env | **missing `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`** |
| Website env | has local URL + anon; **missing `WEBSITE_R2_PUBLIC_URL`, `WEBSITE_ENGINE_URL`** |
| Buy flow | additionally needs `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `ENGINE_EMAIL_*` |

## Steps

1. **Local keys.** `supabase status` at the repo root → `API_URL` and `SECRET_KEY`.
2. **Engine env** (`engine/.env.local`):
   ```
   SUPABASE_URL=http://127.0.0.1:54421
   SUPABASE_SERVICE_ROLE_KEY=<supabase status SECRET_KEY>
   ```
   R2_* are already present.
3. **Website env** (`website/.env.local`):
   ```
   WEBSITE_R2_PUBLIC_URL=<same value as engine R2_PUBLIC_URL>
   WEBSITE_ENGINE_URL=http://127.0.0.1:3001
   WEBSITE_BUY_ENABLED=false
   ```
4. **Run both apps:** `pnpm --filter engine dev` and `pnpm --filter website dev`.
5. **Enter the horse** at `http://127.0.0.1:3001/dsl/new`, using the facts table below and the
   terms table below. Save with `status = coming_soon`, `published = false`.
6. **Upload images** on `/dsl/[id]`, in order: `01.png`, `02.webp`, `03.jpg`. Each upload
   increments `image_count`.
7. **Open the listing:** set `status = available`, `published = true`, save. The trigger refuses
   this if any condition is unmet.
8. **Check the website:** `http://127.0.0.1:3000/marketplace` shows the card;
   `/marketplace/mulan-the-brave` renders the horse page.
9. **Check the quote:** `POST http://127.0.0.1:3001/api/purchase/quote` with
   `{ "dslId": "<id>", "stake": 1.0 }` → expect `$65` per 1%, `$325` float.
10. **Buy flow** comes after this slice: set `WEBSITE_BUY_ENABLED=true`, add Stripe test keys and
    the email sender, then walk Terms → Documents → Identity → Pay → Return.

## Horse facts (from `content/horses/mulan-the-brave/profile.md`)

| Field | Value |
|---|---|
| Legal name | Mulan The Brave (NZ) |
| Foaling date | 2023-08-17 |
| Sex | filly |
| Colour | bay |
| Breeder | C W Kwok |
| Sire | Turn Me Loose (NZ) |
| Dam | Yearn (NZ) |
| Microchip | 985125000128426 |
| Life number | NZ00460867 |
| loveracing id | 460867 |
| Registered | true |
| Trainer | Stephen Gray · Stephen Gray Racing · Copper Belt Lodge, Palmerston North · stephengrayracing.com |
| Owner | Stephen Gray Racing · contact Stephen Gray · stephengrayracing.com |
| Soft prose | `about_horse`, `racing_outlook_and_pedigree`, `race_expectation` — draft from the live page copy, founder approves |
| Trainer bio | `content/trainers/stephen-gray.md` profile section |
| Owner profile | `content/stables/stephen-gray-racing/profile.md` |
| Race record | paste `content/horses/mulan-the-brave/race-record.json` |

## Commercial terms (from the live listing, 2026-10-23)

| Field | Value | Note |
|---|---|---|
| wholesale_monthly_per_percent | 60.00 | retail generates as 65 |
| retail_monthly_per_percent | 65.00 | generated column; do not enter |
| initial payment (5×) | 325.00 | derived |
| listed_stake | 5.00 | live page shows 5.0% |
| min_stake | 1.00 | live page shows 1.00% |
| step | 0.10 | live page shows 0.1% |
| term | 2026-09-01 → 2028-06-30 | 22 months |
| payment_model | subscription_float | 22 months, eligible |
| close_style | fourteen_day | |
| investor_split | **confirm** | live page says 75% — this is the old seed default, not a confirmed term |
| distribution_schedule | **confirm** | free text; compiler refuses empty |

## Founder input required before the save

1. Mulan's **real investor split**. The 75% on the live page is the string the old seed painted
   onto every open horse (`supabase/seed.sql:81`); the audit names it as the class of bug v2
   exists to remove. Do not inherit it.
2. The **distribution schedule** wording.
3. Approval of the three soft-prose paragraphs, because the PDS prints them verbatim.

## Pilot gate

```bash
psql "postgresql://postgres:postgres@127.0.0.1:54422/postgres" -Atc \
  "select (select count(*) from horses), (select count(*) from trainers),
          (select count(*) from owners), (select count(*) from dsls),
          (select image_count from horses where slug='mulan-the-brave');"
# expect: 1|1|1|1|3
```

Then:

- marketplace card and horse page render;
- quote returns stake 1.0 → 65 / 325;
- falsification: set `image_count = 2` and try `status = 'available'` → trigger must raise.

## Rollback

The rows are local only: `supabase db reset` re-applies all migrations and empties the tables.
The three R2 objects remain under `mulan-the-brave/01..03`; delete them before re-running, or the
next upload starts at `04`.

## What this proves, and what it does not

Proves: schema, operator save path, image count, read policies, marketplace and horse page,
quote. This is the spine.

Does not prove: Stripe, webhook, emails, MyStable, the sold-document freeze, or visual parity.
Those are the later gates.
