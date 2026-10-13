# brain/ — who we are, what it's for, and where the conflicts are

**Created 2026-10-08** as the first draft of a house-level "second brain" (concept from the
Justyn reel + Michael Kocher six-spec reel, banked at `audit/knowledge/`). The census audit
cleaned `/home/evo`; this is the integration step that follows it.

## What it's good for

1. **Any island, same reference point.** A session in sandbox, audit, studio or toolbox can
   read `brain/` to know voice, audience and business without walking into `evolution/engine/SSOT/`.
2. **Anti-drift reference for going-forward work.** New projects open with the three questions:
   does this sound like us (voice.md), is this our audience (audience.md), do claims check out
   (business.md index).
3. **Second-brain structure without the 429** — the reel's method, already mostly built:
   the house's memory hub is `brain/projects` equivalent; CANONICAL_FACTS is `business.md`.

## Existing potential conflicts — read before relying on this

1. **Single-source law.** CANONICAL_FACTS.md (`evolution/engine/SSOT/doc/`) is the locked SSOT.
   `business.md` is an index; if any fact appears in both, the engine file wins and the copy here
   is rot by definition.
2. **Memory-hub overlap.** Tone and process rules also live in the global memory hub
   (`~/.claude/projects/-home-evo/memory/`). This folder is the readable map; the memory files stay
   the law for "how Claude works here". If a rule changes, change memory and cite — don't fork rules here.
3. **Sandbox isolation law.** `sandbox/AGENTS.md` forbids external imports from `evolution/`.
   brain/ points at engine docs by *path reference* (read-only pointers), not imports, and nothing
   in sandbox build code should require these files — the gate must not depend on them.
4. **Placement smell.** Sandbox is a build/test island; who-we-are is house-level. This folder is
   the draft home. If/when the census walk finishes, the locked home is likely house-level
   (`/home/evo/brain/`) — promotion is a move + pointer fix, not a copy.
5. **Spec template.** The six pre-build spec docs (PRD, tech, flow, brief, schema, build order)
   are a per-project discipline — template at `audit/knowledge/second-brain-and-six-specs.md`,
   instantiated per island job; not housed here.

## Maintenance law

- Update on evidence only. A fact that can't cite its source stays out.
- Promotion to house-level home: update `home CLAUDE.md` + island pointer docs in the same pass
  (live-surface-pointer-law: never leave a live doc pointing at a retired path).