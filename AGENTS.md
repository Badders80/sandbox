# Sandbox Build Rules

## Gate
`just check` — must pass 10/10

## Constraints
- Own venv (.venv/)
- Own deps (package.json / requirements.txt)
- Own source (src/)
- No external imports from evolution/, toolbox/, openfang/
- No agent runtimes, no cron, no daemons

## Runbook (default execution law)
Every execution session runs the seven guardrails: /home/evo/sandbox/docs/plans/RUNBOOK.md
Acceptance re-audit: /home/evo/sandbox/audit/corpus-deep-dive/out/report.md
