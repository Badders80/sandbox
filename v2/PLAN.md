# V2 build plan

Status: waiting for the word **build**. No repo until then.

Read `OUTCOME.md`, then `CONTINUE.md`. Use `DoD.md` only to check a choice that was already dropped. If `DoD.md` and `OUTCOME.md` disagree, follow `OUTCOME.md`.

## Rulings already made

These close contradictions in the old brief. They are not new product decisions.

1. The repo root is `/home/evo/evolution/engine_v2/website`. One private repo, two hosted apps. `DoD.md` still lists an option to put the repo at `engine_v2/` level (O7). `OUTCOME.md` closed that: do not `git init` the parent. The parent keeps `OUTCOME.md`, `CONTINUE.md`, and `DoD.md`.
2. Do not port the old packages, the monorepo, the alias map, or the 26 MB `engine/content` registry. Soft text is three columns on the horse. Audit item A1 does not block this build.
3. Image files are named from the slug, `01` upward, in a folder for that slug. A rename moves the folder. There is no redirect table and no slug-to-path lookup. `DoD.md` also says to key media by uuid. The outcome wins.
4. Design tokens live in the website app. They are not a gate that runs before the engine exists.
5. Shoulder brand, family number, DNA Typed, PV, and the blank BT field are not columns and are not printed. O9 stays parked.
6. The first slice stores the three soft columns and the race record as one jsonb blob. It does not build a second content stream for updates and highlights (DoD A6).
7. The three finished static horses stay static pages. I Stole A Manolo stays Coming Soon. Lady Ketchikan and Mulan The Brave are the two that can become Available.

## Working defaults

Change these before the first commit if you want a different shape. They are not in the outcome.

- Both apps are Next.js, in the one repo: `engine/` and `website/`. The engine hosts the DSL page, the rules, the compiler, the migrations, and the Stripe webhook. The website reads Supabase, holds the tokens, and never prices, compiles, or holds a Stripe secret.
- Signup and login use Supabase Auth. Google or email. The account row stores full name, email, and KYC status. Full name is collected at signup.
- Stripe stays in test mode until the buy path is flipped on. Live mode flips at the swap, not before.

## The one open decision

Before the compiler is written: the NZTR pro forma Disclosure Statement and the two Syndicate Agreement templates in `evolution/engine/website/packages/legal_engine/reference/nztr-pro-forma/` are the legal source documents (three `.docx` files plus a README, about 504 KB). They are not the 26 MB content registry.

Default if you say build without answering this: copy those four files into the new repo as the document authority, and write the compiler against them. Do not port `legal_engine`. Say "no" before build if those files must not be copied.

## When you say build

Do these in order. Stop at the end of a step if something in the outcome does not fit.

1. Create the private repo at `evolution/engine_v2/website`. Do not `git init` `evolution/engine_v2`. Do not add `CLAUDE.md` or `AGENTS.md`. First commit is the two empty apps and CI that typechecks, lints, and tests.
2. New empty Supabase project. One migration series for the rows in `OUTCOME.md`: trainers, owners, horses, dsls, accounts, sales. No copied business data. No two migrations share a number. No slug-to-id table.
3. Rules module. Shared numbers live there, not on each DSL. Listed price is wholesale cost × 1.05 × 1.03, rounded up to the next whole dollar. Float is 3 months reserve plus 2 months prepaid. Unused float is refunded within 14 business days. An investor must be paid up for two full months before a race to share in that race. Investor split is between 50% and 85%. An empty form shows 75%, and that is not a horse's split. Close styles are `fourteen_day` and `three_x_remaining`. The DSL stores the owner's terms. The engine writes the retail monthly figure.
4. DSL page on the engine. Create, edit, and view. Horse, trainer, and owner are written from that page. They do not get their own screens. A registered horse loads from a loveracing.nz link, then the operator confirms and fills the soft slots. An unregistered horse is typed by hand and cannot be published past Coming Soon. Branding fields from the page are not stored.
5. New R2 bucket. Public images only, for the horses that go through this flow. Minimum three images before a DSL can be Available. `image_count` is the only image fact in the database. Private KYC and proof-of-address files stay in Supabase Storage, not R2.
6. Website reads the rows. Marketplace and horse listing. Press, updates, and the FAQ do not live on the horse, trainer, or owner. Coming Soon is visible and cannot be bought. Available means Buy Now. Unpublished stays off the marketplace.
7. Compiler, after the template decision above. PDS reads the horse soft text, the trainer bio, and the DSL terms. SA reads hard facts and commercial terms, no soft prose. Promoter line on every document: Alex Baddeley, Evolution Stables Ltd. Payment default, prize freeze, and forfeiture are printed procedures. A system that runs them is not part of this outcome.
8. Purchase. Logged-in buyer. The website modal asks the engine for the PDS and SA compiled with the account name. Buyer accepts. Engine starts Stripe Identity if the account is not verified, and records the result on the account. Engine creates Checkout and returns the URL. Webhook writes the sale: stake, amount, Stripe session id, Identity id, both documents, both hashes. A later edit to the horse does not change a document already sold. Browser returns to MyStable. MyStable reads that account and that user's sales. Checkout does not create another profile.
9. Four emails, sent by the engine, and no others. Buyer: sale written (stake, amount, link to MyStable). Buyer: KYC failed. Founder: sale succeeded. Founder: checkout or webhook failed for a reason that is ours. A card decline does not send that alert. Later monthly charges and defaults are manual.
10. Preview with the buy path off. Listings may show Coming Soon. Prove the purchase wiring on a preview, not on the live domain. The flip to Buy Now is a readiness decision. The proof is one real sale after that flip. The old website keeps serving until then, and the new build does not call back into the old one.

## Before any deletion of the old production data

Not code, and not step 1. These block cleanup only.

- Export and keep the old Supabase project. It holds 10 named people's emails, phones, KYC ids, and signed document hashes, plus the private document buckets. Handle it under the NZ Privacy Act 2020. Do not delete it.
- The founder's live Mulan purchase ($42, refunded, subscription `cancel_at` 2028-05-01) is real. Cancel what is still open, confirm the refund, and keep the invoices and the subscription. Do not delete the Stripe account. Delete only the probe products and the dead test webhook after that check.
- New R2 bucket. Do not reuse the old media keys.

## Acceptance

- One horse sells on v2, end to end, real money, real investor. That is the roll gate.
- Edit the stake in its one home. The listing, the PDS, the SA, and the generated PDF all change. Rename the horse. URLs, image paths, and new documents follow. Sold documents do not.
- No duplicate migration numbers. No slug-to-id lookup anywhere.

## Parked

| Item | Why it waits |
|---|---|
| O6 / A1, the 26 MB registry | Not a requirement. Soft text is on the horse row. |
| O8, performance-profile field list | Race record is one jsonb blob. Read the profile when the entry loader is built. |
| O9 / A7, branding fields in the PDS or SA | Not in the outcome. Deciding later must not be done by porting a frozen package. |
| A6, content stream shape | First slice has the three soft columns only. |
| A11, how many old GitHub repos are public | Re-verify before archiving. The Sep-14 count is stale. |
| Observability vendor, and the email sender that replaces Gmail SMTP | Needed before the public buy path, not before the first commit. |
| Second owner on Supabase, Stripe, R2, Vercel, GitHub, DNS, Google | Account task, before the public buy path. |
| Fuller investor profile, reservations, race-by-race table, payout engine, automated monthly charges | Later. They attach to these rows. |

## Removed on 2026-10-13

- `evolution/docs/superpowers/plans/2026-10-13-v2-build-plan.md` contradicted this layout and put O6 first. Deleted.
- Empty `evolution/engine_v2/docs/superpowers/plans/` deleted.
- `sandbox/v2/O6-inventory.md` treated the NZTR pro formas as the 26 MB registry. Deleted. The distinction is in "The one open decision" above.
