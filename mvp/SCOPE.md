# Scope — in, manual, out

Status: first pass. Founder owns the final placement; every row is a proposal
with a reason.

## Must exist

| Item | Why it blocks the sale |
|---|---|
| Horse record with name, trainer, facts | There is nothing to sell without it |
| Three image slots, placeholder allowed | Ruling 26; the page must render |
| Series with owner, price, split, expiry, listed stake | The offer has no terms otherwise |
| Readiness → publish | A public page must not show an unready offer |
| Public horse page and offer page | The entry point |
| Checkout, KYC if required | The money path |
| Reserve on checkout, sweep on expiry | No oversell |
| PDS/SA compiled at sale | The legal artefact |
| Sale row, append-only | The record |
| Ledger over the sale snapshot | The operator's truth |
| Email with the MyStable link | The investor must receive it |
| One combined PDS+SA PDF, attached to the sale email, both hashes in the body | The investor must hold the document, not a link to it |
| MyStable showing the stored document | The document must be readable |

## Can be manual

| Item | Manual form |
|---|---|
| Capacity across several DSLs on one horse | Founder check; ruling 35 |
| Term close | Operator action, recorded reason |
| `paid_unfulfilled` resolution | Operator action, recorded who/when/why |
| Refunds | Stripe dashboard, noted in the ledger |
| Image selection and upload | Founder, via the horse record |
| Document archive | Scheduled copy to external storage plus a manifest |
| The combined PDF itself | Copied outside the database on the same schedule, so a rebuild never depends on a link, a codebase or a vendor |
| Backup verification | Restore into a scratch project, recorded once |

## Not needed

| Item | Revisit when |
|---|---|
| Rename / R2 folder move | After the first sale |
| Content wizard | After the first sale |
| Multiple horses, owners or trainers beyond the pilot | When the second is real |
| Media layer, studio integration, generated assets | Post-sale |
| Greenfield restructure (`appendix/GREENFIELDS.md`) | Only if duplication is hurting weekly |
| Public self-service beyond buying | Never in this phase |
| Admin breadth: three sections, filters, bulk actions | When volume demands it |

## Open decisions

| # | Decision | Why it matters |
|---|---|---|
| 1 | ~~Is the frozen artefact the markdown or the rendered PDF?~~ **RESOLVED — the PDF is the artefact** (founder, 2026-11-11). Markdown stays as the source; the sale stores the PDF hash and the investor receives the PDF. |
| 2 | Is KYC mandatory for the pilot investor, or manual? | Stripe Identity is the slowest step in checkout; manual is allowed if recorded. |
| 3 | Does the pilot sell through the public site, or through the engine first? | The engine-first walk proves the money path; the site walk proves the join. Both are in `DOD.md`. |
| 4 | Is the archive manual or automated before the first sale? | Manual copy plus manifest satisfies the trust floor; automation is post-sale. |

## Cutting order, if something has to go

Cut from the bottom of `Must exist`. Never from the trust floor in `README.md`.
