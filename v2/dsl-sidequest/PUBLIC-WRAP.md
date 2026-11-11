# Public wrap — the follow-on integration review

**Deferred 2026-11-09. This is not part of the DSL engine quest.** The engine
quest (chunks 1–4) closes first. Then we review what the public site needs from
it, how it integrates, and in what order. Until that review, the public page keeps
showing the wholesale total.

The side quest is admin-only. Anything it changes that flows onto the public site
is recorded here as it is found, then executed **once**, in that review.

Read with `STATE.md` and `PLAN.md` §4 (Public flow-ons).

## Register

| ID | What | Source item | Status |
|---|---|---|---|
| P1 | Public page stops rendering wholesale; the 100% total is dropped | H4 | open |
| P2 | Buy flow defaults to 1%, bounded by min, step, remaining | retired U6 | open |
| P3 | Prove the public site renders the full listing projection | retired S2 | open |
| S1 | Rename changes public image URLs (slug-derived); copy-first, no 404 window | S1 — deferred with the wrap | open |
| P4 | Public card falls back to a templated "images coming soon" when the R2 folder is empty | ruling 26 — images never block a listing; asset on file at `website/public/brand/coming-soon.jpg` | open |
| R1 | `horses.trainer_id` is dropped; the DSL carries `trainer_id` | ruling 10 re-rule | **dropped — no public consequence** (checked 2026-11-10: `website/src` never reads a horse trainer; only marketing copy names the word) |

`S1` is deferred with the rest of the wrap. The marketplace derives
image URLs from the slug (`website/src/lib/site.ts` → `imageKey(slug, 1)`), so the
rename must copy to the new slug, switch the DB, verify, and only then delete the
old keys. The review checks that the window was never visible.

Add a row the moment an admin change implies a public consequence. Do not fix it
in-pass; log it here.

---

## P1 — Wholesale off the public page

**Why:** the wholesale rate is the lease cost; retail is derived from it. Showing
it reveals the 5% + 3% margin. The 100% total is never quoted on any surface.

**Where:**
- `website/src/app/marketplace/[slug]/page.tsx:163` — remove the “Wholesale · $N
  at 100%” figure.
- `website/src/lib/listings.ts` — remove `wholesale_monthly_total` from the public
  projection.
- `supabase/migrations/` (next free number at review time) — `alter table public.dsls drop column
  wholesale_monthly_total`.
- `engine/src/lib/dslStore.ts`, `dslStoreSupabase.ts`, `website/tests/listings.test.ts`
  — drop the field from types, mapping and fixtures.

**Done when:** the column does not exist; the public payload carries no wholesale
figure; retail still renders ($65 per 1%/month on Mulan).

## P2 — Buy-flow default stake

**Why:** an investor expects to start at 1% and adjust.

**Where:** `engine/src/lib/purchase.ts:174-175` (today it opens at
`effectiveMinStake`); `website/src/components/BuyFlowModal.tsx` stepper.

**Rule:** `default = max(1%, min_stake)` snapped to the step, clamped to
`stake_remaining`; if 1% is not a valid step, use the first valid step above it.

**Done when:** opening a listing shows 1% for a 1%-minimum listing; the stepper
cannot go below the effective minimum or above the remaining, or off-step.

## P3 — Public projection proof

**Why:** “the website consumes the full projection” has never been evidenced.

**Method:** seed one listing with every field set; assert the marketplace card and
detail page render each field; assert no wholesale figure appears; screenshot at
1440×900 and 390×844. A written record, not a claim.

**Done when:** the record exists in this folder (`PROOF.md`) and the screenshots
are on disk.

---

## Handoff to the main build

When the quest merges back into the v2 line, reconcile these documents — the
quest deliberately does not edit them:

| Doc | What changed |
|---|---|
| `sandbox/v2/OUTCOME.md` | status edges are now enforced; `wholesale_monthly_total` is gone; price may be entered as retail; wholesale is not public |
| `sandbox/v2/PLAN.md` | § table definition (`:258`) loses the generated total; pricing gains the two-way entry rule |
| `sandbox/v2/STEP10-PLAN-2026-11-07.md` | 10.2 items 5 and 7 close |
| `sandbox/v2/STATE.md` | facts and the go-list |

## Rules

- One public movement, one gate, one proof.
- Nothing here runs until the integration review.
- If an item turns out not to flow onto the public site, mark it **dropped** with
  the reason; do not delete it silently.
