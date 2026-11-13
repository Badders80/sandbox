# MVP — what we actually need

Started 2026-11-11. Replaces `v2/v2b/`.

## The definition

One horse, one offer, one investor, one term, one price.

A stranger can find the offer on the website, buy a stake, pay, and receive a
document that is provable — and the system refuses the four ways that can go
wrong.

Anything that is not needed for that is not in the MVP. That includes work that
is correct, desirable, already designed, or already half-built.

## The cut line

Every item gets one of three answers:

| Answer | Means |
|---|---|
| **Must exist** | The sale cannot happen without it |
| **Can be manual** | The founder does it by hand, and it is recorded |
| **Not needed** | Cut. Revisit after the first real sale |

The middle bucket is the lever. Manual and recorded beats unbuilt. A term closed
by hand with a written reason is an MVP feature; a close button is not.

## The trust floor

Five things never move, however small the MVP gets. Cutting any of them makes
the sale a prototype:

1. No oversell.
2. No silent sale — every payment either writes one sale or is recorded as an
   exception.
3. An Investor Pack (PDS + SA) that is frozen and can be proven unchanged.
4. A ledger that agrees with the money.
5. One price authority.

## Where the rules live

`../v2/rulebook/` — it stays there. Rules outlive the MVP; putting them inside a
folder named for a phase is how they get treated as temporary. Cite rule IDs;
do not restate them here.

## Reading order

1. `CONTINUE.md` — current state, work queue and blockers.
2. `MODEL.md` — the locked commercial and legal model.
3. `SCOPE.md` — the three buckets and remaining scope decisions.
4. `DOD.md` — the one walk that closes it.
5. `appendix/` — the full-phase design, kept but explicitly not on the path.

## Rules for this folder

- If a line does not block the first sale, it moves to the appendix or dies.
- One item in progress at a time.
- Closes on evidence, not on a merge.
