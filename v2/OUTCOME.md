# Engine V2 — Outcome

Locked 2026-10-12. This file is the product outcome and the way it runs. `DoD.md` is the previous architecture brief.

**Amended 2026-11-07** to match the built model, by founder decision: the trainer sits on the horse and the owner sits on the DSL; a DSL may exist before its deal does, with nullable commercial terms; one readiness gate decides Available; the operator surface is three sections (Records, Listings, Sales); and Checkout reserves the stake for five minutes so a listing cannot be oversold.

The public site stays. It lists ownership stakes for purchase. The pages that matter are the marketplace and the horse listing. Press, updates, and the FAQ on the homepage are a separate stream and do not live on the horse, trainer, or owner.

## Records

Three records. Each is mostly hard facts, plus a few fixed text slots filled by hand. A later generator writes those same slots.

**Horse.** Legal name, foaling date, sex, colour, breeder, sire, dam, microchip, life number, loveracing id. Internal key is a uuid. External key is the microchip. The slug is derived from the legal name when the horse is saved. A second horse that produces the same slug is refused. A rename changes the slug, and the engine moves the image folder with it. Sales and DSLs point at the uuid. There is no redirect table. Sire and dam are names on the horse. Images belong to the horse and are added with the profile. Three is the minimum required before a DSL can be Available. More are allowed. Files are named in order from the slug, starting at `01`. There is no lookup list from horse to image path.

**Trainer.** Name, stable, location, website. One bio.

**Owner.** Entity name, contact person, website. One profile paragraph. No race record and no results. The documents print the entity name.

**Soft text the PDS reads.** `aboutHorse`, `racingOutlookAndPedigree`, and `raceExpectation` are columns on the horse. The trainer bio is the trainer's bio. The SA reads no soft prose. It prints hard facts and the commercial terms.

**How a horse gets in.** A registered horse starts from a loveracing.nz link: load, confirm or edit, save, then fill the soft slots. The race record is pulled from that page. An unregistered horse is typed by hand, named by the convention, and its sire and dam are entered manually. An unregistered horse cannot be published past Coming Soon.

## DSL

A DSL is downstream of the horse. A horse can have more than one. The difference between them is the end date: one DSL per horse per end date. At the start, each horse has one. A second listing is allowed only with a different end date.

The DSL points at the horse for the horse's facts and its trainer. The owner is a party to the deal, so the owner sits on the DSL: one horse can have several owners, and each lists their own stake on their own terms. A horse is physically with one trainer at a time, so the trainer sits on the horse; changing it changes every live DSL and leaves sold documents alone. The commercial terms are typed on the DSL from the owner's deal.

Status sits on the DSL: Coming Soon, Available, Fully Allocated, Completed. Coming Soon may be incomplete. Available must be complete. Available means Buy Now. Coming Soon is visible and cannot be bought.

Published is a separate flag on the DSL. An unpublished DSL stays off the marketplace. A published DSL shows its status.

A DSL exists from the moment its horse does. It may be created before the deal is done, with no commercial terms at all, and published as Coming Soon carrying only the horse's facts. Those columns are nullable for exactly that reason. Four visible states come from the two flags plus one derived fact:

| State | published | status | commercials |
|---|---|---|---|
| Not listed | false | coming_soon | any |
| Coming soon, no commercials | true | coming_soon | absent |
| Coming soon, with commercials | true | coming_soon | present |
| Live | true | available | present, and the pack compiles |

**The readiness gate.** One check decides whether a DSL may become Available. It requires the owner, both term dates, the payment model, the close style, the wholesale rate, the investor split, the listed, minimum and step stakes, the stake remaining, the distribution schedule, the three horse paragraphs, a trainer bio, a registered horse and at least three images. It lives in the engine, is called by the save action and the compiler, and is mirrored by the Postgres trigger. It returns the missing fields, not a bare refusal.

The operator surface has three sections on the engine. **Records**: horses, trainers and owners, each with a list, a detail page and an edit form. **Listings**: the DSLs, each opening its term sheet and the pre-execution PDS and SA preview. **Sales**: one row per purchase, read-only.

The operator is trusted to enter a valid stake. There is no ceiling across a horse's live DSLs in this version; only the shape of a single DSL and the readiness gate are enforced.

## Sale

A sale freezes the compiled PDS and the SA, including their hashes. The frozen documents contain the horse's soft text and that DSL's commercials as they were at that moment. A later edit to the horse does not change a document already sold.

The promoter line on every document is Alex Baddeley, Evolution Stables Ltd.

## Pricing Rules (V2 Philosophy Alignment)

These rules implement the V2 pricing rewrite's three pillars:
1. **Single Source of Truth**: Only `wholesale_monthly_per_percent` is user-editable
2. **Buyer's Mental Model**: All pricing is derived from the per-1% rate
3. **Fractional-Cent Elimination**: Ceiling calculations ensure whole-dollar shares

These are known. They live in the engine's rules module. The manual in that same repo is the readable copy. A DSL row holds one owner's terms. It does not restate the shared numbers.

The same for every horse: listed price per 1% is wholesale cost per 1% × 1.05 × 1.03, rounded up to the next whole dollar. The initial payment collected at checkout is strictly 5 months (3 months deposit reserve, 2 months prepaid) times the retail rate. Ongoing billing is 1× the monthly share price, billed on the 1st of each calendar month, commencing on Month 3 (paying for that month in advance). `upfront` is available for any term: 100% of the lease term is collected at checkout with zero subsequent charges. A term of 5 months or less must use `upfront`, because the five-month initial payment already covers the whole term. A term of 6 months or more may use either model, defaulting to `subscription_float`. In V2, the Stripe webhook handles the initial one-time checkout completion (mode: 'payment'). Subsequent monthly charges on the 1st are administered manually via the Stripe Dashboard until the automated billing engine is attached in a future milestone. An investor must be paid up for two full months before a race to share in that race. The investor split must sit between 50% and 85%. 75% is the value an empty form shows, and it is not a substitute for a horse's own split. Close styles are `fourteen_day` and `three_x_remaining`.

Typed on the DSL, from the owner's deal: payment style, close style, investor split, **wholesale_monthly_per_percent**, listed stake, step size, term start, end date, distribution schedule. The retail price and the monthly amount are calculated.

Payment default, prize freeze, and forfeiture are written procedures. They are printed into the documents. A system that runs payouts and defaults is not part of this outcome.

## Refund

If the horse is retired or the lease ends early, the leaseholder receives a pro-rata refund of the unused lease fee for the full months remaining. The buy screen, the PDS, and the SA print that sentence. They do not print a day count. The amount is worked out after the owner and Evolution have agreed the termination date and reconciled the accounts.

## Horses in play

Six horses are on the current marketplace. Prudentia, Hottathanafantasy, and First Gear stay as finished static pages. I Stole A Manolo stays Coming Soon. Lady Ketchikan and Mulan The Brave are the two that go live.

## How it runs

Locked 2026-10-12. One new repo, two hosted apps. This `engine_v2` folder is not that repo. Do not `git init` it. The seven current repos stay the archive. The old website keeps serving until the new surface replaces it. The new build does not call back into the old one.

The engine app is the home for the DSL page, the rules, the compiler, the migrations, and the Stripe webhook. It stays up with the founder's PC off. The website app reads Supabase and holds the design tokens. It does not price, compile, or hold a Stripe secret.

Supabase holds the rows. The CDN holds the images, ordered from `01` under the horse slug. `image_count` is the only image fact in the database. Three is the minimum for Available. Stripe takes the payment and the identity check, then calls the engine.

**Rows.** `trainers` (name, stable, location, website, bio). `owners` (entity, contact, website, profile). `horses` (id, microchip, slug, legal name, foaling date, sex, colour, breeder, sire name, dam name, life number, loveracing id, registered, trainer id, about horse, racing outlook, race expectation, image count, race record as one jsonb blob). `dsls` (horse id, owner id, end date, term start, payment model `subscription_float` or `upfront`, close style `fourteen_day` or `three_x_remaining`, investor split, wholesale_monthly_per_percent, listed stake, stake remaining, min stake, step, distribution schedule, retail_monthly_per_percent, status, published). Every commercial and term column on a DSL is nullable: a listing can exist before its deal does, and the readiness gate is what fills them in. One end date per horse. The engine writes the retail figure. `accounts` (id, full name, email, kyc status), created at signup. `sales` (dsl id, user id, printed name, email, stake, amount, Stripe session id, Stripe identity id, PDS markdown, SA markdown, both hashes, created at).

**Purchase.** The buyer is logged in on the website. The modal asks the engine for the PDS and SA, compiled with the account name, and shows them. After the buyer accepts, the engine starts KYC if the account is not verified and records the result on the account. It then creates the Stripe Checkout session and returns the URL. The browser goes to Stripe. The webhook hits the engine, which writes the sale. The browser returns to MyStable. MyStable reads the account and that user's sales. Checkout does not create another profile.

**No oversell.** Opening Checkout reserves the stake: `stake_remaining` is decremented when the session is created, for a five-minute hold, and restored when the session expires or the payment fails. A minute-by-minute sweep expires overdue sessions. The webhook repeats the decrement as an atomic conditional update, so a lost race can never write a second sale. A buyer who cannot get the stock is told on screen, not charged and refunded: "No stock available right now. Evolution Stables will be in touch with a new offer." That message is a screen, not a fifth email kind.

**Emails, sent by the engine.** Four messages, and no others. The buyer receives one when the sale is written: the stake, the amount, and a link to MyStable. The buyer receives one if KYC fails. The founder receives one when a sale succeeds, and one when checkout or the webhook fails for a reason that is ours. A card decline does not send that alert.

## Not this outcome

Porting the old packages, the monorepo layout, design tokens as a gate, alias maps, and the 26 MB registry are not requirements. The old engine is a source of pieces and of the rules above. A fuller investor profile, reservations, a race-by-race table, a payout engine, and automated monthly charges are later. They attach to these rows.
