# DoD — the one walk

The MVP closes when a person who is not the founder can buy a stake on the public
site, and the record agrees with the money.

Evidence, not assertion. Every row needs a captured result.

## The walk

| # | Act | Pass |
|---|---|---|
| 1 | Open the public site, find the horse | Page renders from engine state, placeholder acceptable |
| 2 | Open the offer | Stake, price, split and expiry match the engine row exactly |
| 3 | Start checkout | Stake is reserved; remaining drops by the amount |
| 4 | Pay | Exactly one sale row is written |
| 5 | Read MyStable | The stored PDF is served, its hash matches the sale row |
| 6 | Check the investor's inbox | One combined PDF attachment arrived; both hashes in the body match the sale |
| 7 | Read the ledger | Sold, remaining, revenue and term end agree with the sale |

## The four refusals

| # | Refusal | Enforced by | Evidence |
|---|---|---|---|
| 1 | Buying more than remains | `R-ALLOC-02` | Second checkout refused, or decremented honestly; no negative remaining |
| 2 | A duplicate payment writing a second sale | `R-SALE-02` idempotency | Replayed webhook returns the same sale |
| 3 | Editing or deleting the sale | `R-SALE-01` | `update`, `delete`, `truncate` all refused |
| 4 | Closing a term with money in flight | `R-SALE-05` | Close refused while a hold or unresolved checkout exists |

## Evidence to keep

- the sale row, exported
- the ledger view for that series
- the document hash and the document
- the four refusal outputs
- the exact commit the walk ran against

## Not part of this gate

Recovery drill, archive automation, media, breadth, multiple horses, public
self-service, rename. Those are post-sale.

## If a row fails

The walk stops. A fail is a fail; a workaround is a scope change and needs a
decision, not a note.
