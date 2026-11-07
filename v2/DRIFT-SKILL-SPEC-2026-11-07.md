# Drift report — skill spec (2026-11-07)

Not built yet. This is the design so the next session does not re-derive it.

## Why

The costliest defect class this estate keeps hitting: **a document claiming something the live surface no longer does.** Today's example — `OUTCOME.md` said trainer and owner hang off the horse; the schema had already disagreed since the model changed. The audit found it by hand; nothing would have caught it.

EGM's `drift-report` is the one idea worth taking from that plugin. Everything else in it is more review rounds, which is the anti-pattern.

## Shape

A thin skill + one script. The skill is judgement; the script is the gate.

```
~/.claude/skills/drift-report/
  SKILL.md          under 60 lines
  drift.sh          under 80 lines, no dependencies beyond bash + grep
```

## Mechanism — declared facts, not NLP

Do **not** scrape prose and guess. False positives kill the tool on first use.

The repo carries a `.drift` file of explicit line assertions:

```
# <name> | <file that must contain it> | <regex>
dsls.owner_id          | supabase/migrations | owner_id uuid references public\.owners
horses has no owner_id | supabase/migrations | ^(?!.*horses.*owner_id)
route /sales           | engine/src/app     | app/sales/page\.tsx
```

`drift.sh` runs each regex against its file glob and exits non-zero on a miss. That is a gate, not an opinion, and it belongs in `pnpm test` / `just check` wherever it is adopted.

Anything that cannot be expressed as a regex stays in the skill as a checklist, not in the script.

## The RED test (required before writing it)

`superpowers:writing-skills` says no skill without a failing baseline. Before writing `SKILL.md`:

1. Give a subagent a repo with one stale doc claim and no `.drift` file.
2. Ask: "are the docs accurate?" — no hint.
3. Record whether it finds the drift and how long it takes unaided.

If an agent finds it cheaply, the skill earns its place only as the *script*; skip the prose.

## Trigger

Use when a migration, rename, table change or schema edit has landed and the docs describe the old shape; or before a release tag; or when a doc is cited as authority and nobody has run it against the code lately.

## Not this

- Not a general docs linter.
- Not a prose reviewer — that is the anti-pattern.
- Not a replacement for the test suite. It checks claims, not behaviour.

## Target

45 minutes end to end, including the baseline. Under 60 lines of skill, under 80 of script.
