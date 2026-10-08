BRIEF — Island Install: orca + ruflo (sandbox/rebuild)

SCOPE: Plan/review only. No execution.

PATH LOCK: /home/evo/sandbox/rebuild/src/island/
LAYOUT:
  rebuild/src/island/
    orca/              # Adapter + stubs
    ruflo/             # Adapter + local .mcp.json
    .venv/             # Python isolation
    node_modules/      # Node isolation (Orca)
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
- Both repos ship with background workers (must stub)
- Rust + Python + Node isolation requires separate lock files
- Performance test valid only in ephemeral mode
