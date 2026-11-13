# CONTINUE — sandbox

> Shape (LOCKED): **Next action · State · Ledger · Blocked**. Chat is not storage.

**Next action:** open
`mvp/sessions/active/2026-11-13-marketplace-mystable.md` and begin the read-only
production Marketplace audit from a clean website worktree based on
`origin/dsl-sidequest`.

## State — 2026-11-13

- **Landing parity is merged and pushed** on `dsl-sidequest` at `03ea397`; the
  founder accepted the result at desktop and mobile widths.
- **Shared page foundation is locked and pushed** at `ade0cc3`: global
  `ScrollReveal`, `--duration-reveal: 750ms`, `PageShell`, `PageContainer`,
  `PageIntro`, `PageSection`, no page-level separator rule, and pathname-scoped
  reveal re-arming.
- Marketplace, Marketplace horse page and MyStable consume the shared
  primitives. The next job is the production Marketplace audit and visual lock,
  not implementation of the later surfaces.
- Integrated gate: **402 engine passed / 1 skipped, 63 website passed**, both
  builds.
- Unrelated legal/checkout work remains uncommitted in the shared website
  checkout. New website work must use an isolated worktree.

## State — 2026-11-12

- **Landing parity is built and pushed** on `landing-parity-2026-11-12`
  (code `5726a51`):
  production-matched landing structure, hero restored, wordmark-only nav,
  blended glass fade and measured FAQ motion. Gate green; worktree clean; not
  merged pending the founder visual walk.
- Motion audit captured at
  `mvp/audits/EVOLUTION-STABLES-MOTION-AUDIT-2026-11-12.html` (1 Critical,
  4 Important, 6 Opportunities).
- **All four chunks are closed** on `dsl-sidequest` in `engine_v2/website`;
  branch tip `81b5f5d`; `main` untouched; nothing pushed or merged.
- Gate `pnpm verify` **393 engine / 1 skipped, 54 website**; `just verify-db`
  **27 + 7 + 2 + 3 + 5 probes**, `check-db` 6/6. CI runs both on every PR and
  branch push.
- Follow-ons landed this session: `00026` paid_unfulfilled resolution,
  `just verify-db`, `00027` draft archive-in-place, `00028` dateless index,
  `00029` closed-row immutability.
- Hosted `evolution-engine`: **29 migrations**, 1 Mulan draft (narrative
  approved, unpublished), 0 sales, 1 horse, 1 party.
- The rulebook `v2/rulebook/` is committed: **43 rules**, enforcement map and
  gap register. Ruling 35 numbers the dropped 100-point cap.
- Handoff: `v2/dsl-sidequest/HANDOFF-2026-11-11.md`. Live state: `STATE.md`.

## Ledger

| date | what | repo | commit | state |
|---|---|---|---|---|
| 2026-11-13 | Landing merged; shared page foundation locked; next-session plan created | engine_v2/website / sandbox | `03ea397`, `ade0cc3`, this commit | done; pushed |
| 2026-11-12 | V2 landing parity + final visual refinements | engine_v2/website | `c1ca04e`…`5726a51` | done; founder walk pending |
| 2026-11-12 | wrap notes and branch publication | engine_v2/website | — | pushed |
| 2026-11-11 | Images — checkout unblocked; placeholder dropped | engine_v2/website | `81b5f5d` | done |
| 2026-11-11 | DSL chunk 4 + follow-ons + SQL gate + CI + rulebook | engine_v2/website / sandbox | `482b6d6` / `0163348` | done |
| 2026-11-09 | DSL side quest 1 / 1b / 1c + target Supabase | engine_v2/website | `8b6baf4`,`e30e50c`,`82a702d` | done |
| 2026-11-09 | Wrap, docs committed to this repo | sandbox | — | done |

## Blocked

- **Cloudflare Access** on the engine host — `/sales` has no in-app auth; do not
  expose the host without it.
- **F3** — external immutable document archive + manifest. **Priority.**
- **F1 / F2 / F4 / F5** — contract ID; post-sale term freeze; offsite backup;
  recovery drill.
- **Mumbai project** `umxljalfbmvrocaopao` — confirm deleted.
- **Keys** — the service-role JWT was pasted into chat; rotate in one batch at
  cutover (ruled, not blocking).
