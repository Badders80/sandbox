BRIEF — Island Install: ruflo (sandbox/rebuild)

Orca was removed 2026-10-13. Do not install it. The orca half of this brief is dead.

SCOPE: Plan/review only. No execution.

PATH LOCK: /home/evo/sandbox/rebuild/src/island/
LAYOUT:
  rebuild/src/island/
    ruflo/             # Adapter + local .mcp.json
    .venv/             # Python isolation
    package.json       # Island-only manifest
    Cargo.toml         # Rust isolation (Ruflo)

CONSTRAINTS (AGENTS.md):
- Own venv/deps/source
- No imports from evolution/, toolbox/, openfang/
- No agent runtimes / cron / daemons
- Gate: just check 10/10
- Ephemeral CLI mode only (one-shot per turn)

STEPS:
1. Clone repos (read-only reference)
2. Audit for forbidden runtimes/cron/agents
3. Strip daemons; wrap in ephemeral CLI adapters
4. Create isolated .venv/, node_modules/, Cargo
5. Define just check gates

RISKS:
- Ruflo ships with background workers (must stub)
- Rust + Python isolation requires separate lock files
- Performance test valid only in ephemeral mode
