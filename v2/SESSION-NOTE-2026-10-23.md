# Session Note — 2026-10-23

**Status:** Completed session. Operator Console live on port 8766. DB populated & verified. `pnpm verify` 100% green.  
**Author:** Pair programming session (User & Antigravity).  
**Context:** Handoff and state summary for the next session.

---

## 1. Executive Summary

Today's session transitioned from the pure build steps (Steps 1–9) to operational backfill and preparation for the money rail test (Step 10b) and visual parity pass (Step 10.5):

1. **Strategic Realignment**: Confirmed "prove the money rails first, then make it pretty". Do not let presentation work block payment rail certification.
2. **Operator Console Created (`scripts/operator_page.html` & `scripts/operator_server.py`)**: Modeled after the ultra-lightweight `ops/gst` reviewer pattern. No build chains, zero npm dependencies, instant loading, native dark/light theme. Runs on `http://127.0.0.1:8766`.
3. **Core Domain Decoupling**: Refactored the data model hierarchy so that **Horse** is strictly independent of **Trainer** and **Owner**. A Horse holds equine biological facts and legal soft prose. Trainer and Owner are assembled only when forming a **DSL** (Digital Syndication Listing).
4. **Fast Microchip Auto-Loader**: Verified with microchip `985125000139165` (`Hottathanafantasy (NZ)`). Instantly queries local archive and extracts pedigree, foaling date, sex, color, life number, Loveracing ID, plus PDS soft prose (`about_horse`, `racing_outlook_and_pedigree`, `race_expectation`).
5. **Commercial & Term Calculations**: Enforces NZ date format (`DD/MM/YYYY`), automated wholesale-to-retail conversion (`ceil(wholesale × 1.05 × 1.03)`), initial 5-month float calculation (`retail × 5`), and dynamic active term duration (e.g. fixed end date `30/06/2028` with current month calculates dynamically as 21 months).
6. **Data Verified in Supabase**:
   - `Mulan The Brave (NZ)`: Updated with 75% investor split, 21-month term (`30/06/2028`), status `available`, `published = true`. Availability triggers verified.
   - `Lance O'Sullivan & Andrew Scott` (`Wexford Stables`): Created in `trainers`.
   - `Bax Bloodstock` (`Kylie Bax`): Created in `owners`.
   - `Hottathanafantasy (NZ)`: Created as an independent horse record in `horses`.
   - `Hottathanafantasy DSL`: Created with Wexford + Bax Bloodstock, wholesale $65 $\to$ retail $71, 5% stake.
7. **CI / Test Suite 100% Green**: `pnpm verify` passes all checks (0 anti-pattern token violations, 16 test files, 260 tests passed, 0 failures, Next.js build clean for both engine and website).

---

## 2. Infrastructure & Running Services Map

| Service | Port | Directory / Command | Status |
|---|---|---|---|
| Local Supabase PostgREST | `54421` | Docker container `supabase_kong_website` | Active |
| Local Supabase Postgres | `54422` | Docker container `supabase_db_website` | Active |
| Operator Console Server | `8766` | `cd evolution/engine_v2/website && python3 scripts/operator_server.py --port 8766` | Running (`http://127.0.0.1:8766`) |
| Website Frontend | `3000` | `pnpm --filter website dev` | Idle (ready to launch) |
| Engine API & Legal Preview | `3001` | `pnpm --filter engine dev` | Idle (ready to launch) |

---

## 3. Operator Console Architecture

The Operator Console is located in `/home/evo/evolution/engine_v2/website/`:
- **Server:** `scripts/operator_server.py`
  - Lightweight Python standard library HTTP server (`ThreadingHTTPServer`).
  - Communicates directly with local Supabase PostgREST (`http://127.0.0.1:54421/rest/v1/`) using `SUPABASE_SERVICE_ROLE_KEY`.
  - Serves static UI, handles CRUD for `/api/horse`, `/api/trainer`, `/api/owner`, `/api/dsl`, and archive lookup `/api/lookup-horse`.
  - Automatically generates UUIDs for tables that lack database defaults (`trainers`, `owners`).
- **UI:** `scripts/operator_page.html`
  - Single-file HTML/CSS/JS with zero external CDNs or bundling.
  - Sidebar layout: Vertical accordion groups for **Horse** $\to$ **Trainer** $\to$ **Owner** $\to$ **DSL**.
  - Clicking any group reveals existing records and a **+ Add** button.
  - Clicking any item opens a rich detail view with live status badges (`AVAILABLE`, `COMING SOON`).
  - Horse view includes microchip lookup bar: enter microchip and click **⚡ Fetch & Autofill** to pull facts + soft prose.
  - DSL form has two clean sections:
    - Section 1: "Assemble Syndicate Entities" (Horse + Trainer + Owner + Status + Published).
    - Section 2: "Commercial Deal & Term Calculations" (Wholesale input $\to$ auto retail/float, investor split 50–85%, dynamic term calculation with NZ dates).

---

## 4. Key Files Modified or Created

### In `/home/evo/evolution/engine_v2/website/`:
1. `scripts/operator_server.py` *(New)*: Python backend for operator console.
2. `scripts/operator_page.html` *(New)*: Single-file operator frontend.
3. `supabase/migrations/00013_service_role_grants.sql` *(New)*: Service role DML grants on tables.
4. `engine/next.config.ts` *(Modified)*: Configured `serverActions.bodySizeLimit = '15mb'` to prevent 1 MB default cutoff during camera-resolution hero photo uploads.

### In `/home/evo/sandbox/v2/`:
1. `ALIGNMENT-2026-10-23.md` *(New)*: Strategic alignment on data backfill before visual pass.
2. `PILOT-MULAN-2026-10-23.md` *(New)*: Pilot execution runbook for Mulan The Brave (NZ).
3. `SESSION-NOTE-2026-10-23.md` *(This file)*: End-of-day handoff and session record.

---

## 5. Playbook for Next Session

When returning to the project, execute in this order:

### Track A: Step 10b — The Money Test (Payment Rail Verification)
1. Ensure Supabase is running (`supabase status`).
2. Add Stripe test keys to `engine/.env.local`:
   ```bash
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```
3. Set `WEBSITE_BUY_ENABLED=true` in `website/.env.local`.
4. Run `stripe listen --forward-to localhost:3001/api/purchase/stripe/webhook` in a terminal.
5. Boot services:
   ```bash
   cd /home/evo/evolution/engine_v2/website
   pnpm --filter engine dev    # port 3001
   pnpm --filter website dev   # port 3000
   ```
6. Visit `http://localhost:3000/marketplace/mulan-the-brave-nz` and execute a test purchase:
   - Accept terms $\to$ view legal docs $\to$ complete Stripe KYC $\to$ Stripe checkout $\to$ webhook event triggers.
   - Verify: Sale written to `sales` table, legal hashes recorded, 4 confirmation emails sent (logged), investment visible on MyStable (`/mystable`).

### Track B: Step 10.5 — Visual Parity Pass (Frontend Polish)
1. Cut the presentation-only git branch in `engine_v2/website`:
   ```bash
   git checkout -b visual-parity
   ```
2. Port components from `evolution/engine/website/apps/web/src/components/`:
   - `BuyFlowModal.tsx`: Extract into clean shell, state machine/reducer, and sub-screens.
   - Horse page presentation blocks: `media-deck`, `tabs`, `right-rail`, `pedigree-tab`.
   - Landing page sections: `HeroSection`, `AboutSection`, `HowItWorksSection`, `DigitalSyndicationSection`, `MarketplaceSection`, `PressShowcaseSection`, `FAQSection`.
3. Verify visual rhythm against screenshot baselines at `1440×900` & `390×844`.
4. Keep `pnpm verify` green with zero anti-pattern violations throughout.
