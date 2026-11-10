# CONTINUE — sandbox

> Shape (LOCKED): **Next action · State · Ledger · Blocked**. Chat is not storage.

**Next action:** read `v2/dsl-sidequest/HANDOFF-2026-11-11.md`, then start the
**F3** design session: the external immutable archive for executed PDS/SA —
vendor, WORM semantics, manifest shape.

## State — 2026-11-11

- **All four chunks are closed** on `dsl-sidequest` in `engine_v2/website`;
  branch tip `482b6d6`; `main` untouched; nothing pushed or merged.
- Gate `pnpm verify` **395 engine / 1 skipped, 54 website**; `just verify-db`
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
