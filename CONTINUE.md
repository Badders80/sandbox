# CONTINUE — sandbox

> Shape (LOCKED): **Next action · State · Ledger · Blocked**. Chat is not storage.

**Next action:** founder-walk V2 branch `landing-parity-2026-11-12` (`5726a51`)
using `mvp/audits/landing-parity-2026-11-12/EVIDENCE.md`; then decide integration
and resume F1 before the F3 archive design.

## State — 2026-11-12

- **Landing parity is built locally** on `landing-parity-2026-11-12` (`5726a51`):
  production-matched landing structure, hero restored, wordmark-only nav,
  blended glass fade and measured FAQ motion. Gate green; worktree clean; not
  merged or pushed pending the founder visual walk.
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
| 2026-11-12 | V2 landing parity + final visual refinements | engine_v2/website | `c1ca04e`…`5726a51` | done; founder walk pending |
| 2026-11-11 | Images — checkout unblocked; placeholder dropped | engine_v2/website | `81b5f5d` | done |
| 2026-11-11 | DSL chunk 4 + follow-ons + SQL gate + CI + rulebook | engine_v2/website / sandbox | `482b6d6` / `0163348` | done |
| 2026-11-09 | DSL side quest 1 / 1b / 1c + target Supabase | engine_v2/website | `8b6baf4`,`e30e50c`,`82a702d` | done |
| 2026-11-09 | Wrap, docs committed to this repo | sandbox | — | done |

## Blocked

- **Landing parity:** founder visual walk at 1440 and 390, then integration
  decision; no merge or push before that gate.
- **Cloudflare Access** on the engine host — `/sales` has no in-app auth; do not
  expose the host without it.
- **F3** — external immutable document archive + manifest. **Priority.**
- **F1 / F2 / F4 / F5** — contract ID; post-sale term freeze; offsite backup;
  recovery drill.
- **Mumbai project** `umxljalfbmvrocaopao` — confirm deleted.
- **Keys** — the service-role JWT was pasted into chat; rotate in one batch at
  cutover (ruled, not blocking).
