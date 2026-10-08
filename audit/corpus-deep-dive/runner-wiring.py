#!/usr/bin/env python3
"""Runbook-distillation dispatch. Model (gemma-4-31b, free, review-grade) writes
RUNBOOK.md content only. Pointer wiring into boot files is deterministic script lines.
Brief: dispatch-runbook-wiring.md. DoD: ../../docs/plans/GUARDRAIL-RUNBOOK-DOD-2026-10-08.md
"""
import json, os, urllib.request, time, glob, re

OUT = "/home/evo/sandbox/docs/plans/RUNBOOK.md"
MODEL = os.environ.get("DEEPDIVE_MODEL", "qwen3.8:27b-64k")
BRIEF = open("/home/evo/sandbox/audit/corpus-deep-dive/dispatch-runbook-wiring.md", encoding="utf-8").read()
DOD = open("/home/evo/sandbox/docs/plans/GUARDRAIL-RUNBOOK-DOD-2026-10-08.md", encoding="utf-8").read()

def cloud_call(messages, max_tokens=8000, timeout=300):
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False, "think": False,
                       "temperature": 0.3, "num_predict": max_tokens}).encode()
    req = urllib.request.Request(f"{os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')}/api/chat", data=body,
        headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
            msg = d["message"]
            return (msg.get("content") or "") or (msg.get("thinking") or "")
        except Exception as e:
            print(f"  call fail {attempt}: {type(e).__name__}: {str(e)[:150]}", flush=True)
            time.sleep(20 * (attempt + 1))
    return None

PROMPT = f"""You distill an execution-law runbook. Read the source DoD and brief, then write the operator contract ONLY — you do not have file access; your reply is the file content.

Rules for your reply:
- Markdown, <=120 lines.
- Sections in order: header "RUNBOOK — seven guardrails (default execution law)" / Boot order (the 7 rules in session order: rule name, trigger, enforcer, one line each) / Auditor law / Acceptance test / Scope fence wording / Root hygiene.
- No invented content: only what the DoD and brief contain. Tight prose, no essays.

=== SOURCE DoD ===
{DOD}

=== SOURCE BRIEF ===
{BRIEF}
"""

t0 = time.time()
md = cloud_call([{"role": "user", "content": PROMPT}])
if not md:
    print("MODEL UNAVAILABLE — nothing written")
    raise SystemExit(1)
md = re.sub(r"^```(markdown)?\n|```$", "", md.strip(), flags=re.M).strip()
ok_rules = all(k in md for k in ["Boot", "Binary ruling", "Budget", "Verification",
                                 "Auditor", "Scope", "Root"])
lines = md.count("\n") + 1
print(f"draft received {time.time()-t0:.0f}s: {lines} lines, all-rules={ok_rules}")
if lines > 130 or not ok_rules:
    print("QUALITY GATE FAIL — rejecting draft, no files written")
    raise SystemExit(1)

open(OUT, "w").write(md)
print(f"wrote {OUT}")

# deterministic pointer wiring — verbatim block, no model hands on boot files
BLOCK = """
## Runbook (default execution law)
Every execution session runs the seven guardrails: /home/evo/sandbox/docs/plans/RUNBOOK.md
Acceptance re-audit: /home/evo/sandbox/audit/corpus-deep-dive/out/report.md
"""
BOOT = ["/home/evo/CLAUDE.md", "/home/evo/AGENTS.md",
        "/home/evo/evolution/engine/website/AGENTS.md", "/home/evo/studio/AGENTS.md",
        "/home/evo/sandbox/AGENTS.md"]
wired = []
for f in BOOT:
    txt = open(f, encoding="utf-8").read()
    if "docs/plans/RUNBOOK.md" in txt:
        print(f"  already wired: {f}")
        wired.append(f)
        continue
    open(f, "a", encoding="utf-8").write(BLOCK)
    wired.append(f)
    print(f"  wired: {f}")

gate = {
    "runbook": {"exists": os.path.exists(OUT), "lines": lines, "all_rules": ok_rules},
    "wired": wired,
    "gate_ok": ok_rules and lines <= 130 and len(wired) == 5,
    "model": MODEL,
}
os.makedirs("/home/evo/sandbox/audit/runbook-wiring", exist_ok=True)
json.dump(gate, open("/home/evo/sandbox/audit/runbook-wiring/gate.json", "w"), indent=1)
print(json.dumps(gate, indent=1))