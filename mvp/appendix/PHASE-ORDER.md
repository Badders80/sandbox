# Finish — the model and the order

Written 2026-11-11, after chunk 4 closed.

## The model

Finish by proving one path and every refusal around it, not by completing a
feature list.

1. **Prove the engine alone, then prove the join.** Two walks with different
   jobs. Never debug both at once.
2. **The website is a view.** Delete it and the business still runs from the
   engine. Any rule in a page is trust in the wrong layer.
3. **Trust is made of refusals.** Oversell, edit after sale, close with an open
   hold, publish without narrative, checkout without KYC. Features make it
   useful; refusals make it sellable.
4. **A rule with no probe is an intention.** Enforced in DB or TS, and
   demonstrated — or it does not exist.
5. **Two SSOTs, one direction.** The structured row is operational; the executed
   PDS/SA is legal and wins. Hashes bind them. Neither is guessed from the other.

## The order

| # | Step | Question it answers | Closes when | Status |
|---|---|---|---|---|
| 1 | **Engine walk, hosted** | Does the money path work without a website? | One sale on hosted plus three deliberate refusals | **NEXT** |
| 2 | **F1 + F3 — identity and survival** | Can the document be named and does it still exist? | Contract ID printed and indexed; immutable archive with a manifest | OPEN |
| 3 | **F2 — freeze the live row** | Can the DSL drift from what was sold? | A post-sale economic edit is refused at the DB | OPEN |
| 4 | **F4 + F5 — recovery** | Can the position be rebuilt from documents? | Backup restored; one position rebuilt and reconciled | OPEN |
| 5 | **Wire the public site** | Does the site decide anything? | One path wired: horse → listing → checkout → MyStable | OPEN |
| 6 | **Browser walk** | Does the join hold? | A stranger buys on the public site end to end | OPEN |
| 7 | **Cut over** | Is it safe to take real money? | Access in front of the engine host; monitoring live | OPEN |

## Why this order

- Step 1 isolates the engine. Every later failure is then either the site or the
  join, never all three.
- Steps 2–4 make the artefact trustworthy before anyone outside sees it. A
  contract that cannot be named, archived or recovered is not a contract.
- Step 5 is deliberately late. The site is the cheapest layer to change and the
  most expensive to debug against a moving engine.
- Step 6 is the DoD. Step 1 proves the parts; step 6 proves the system.

## Already done

- Chunks 1–4 closed on `dsl-sidequest`; rulebook v0.1 with 43 rules.
- `verify-db` in CI: every probe, schema assert, localhost only.
- Images never block, end to end, including checkout.
- Mulan draft on hosted: narrative approved, `coming_soon`, unpublished.

## What "done" means

A stranger can buy 1% of Mulan on the public site, and the system refuses every
way that could go wrong.

## Non-goals for this phase

- Breadth across horses, owners or trainers.
- Public self-service for anything except buying.
- Re-litigating the ownership model. It is locked; changes go through a ruling
  and the rulebook.
