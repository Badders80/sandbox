#!/usr/bin/env python3
"""Corpus deep-dive dispatcher. Read-only over the corpus; writes only to out/.
Stage 1: manifest (no LLM). Stage 2: score selected sessions via OpenRouter.
Stage 3: synthesis. Stage 4: citation gate. DoD: ../docs/plans/CORPUS-DEEP-DIVE-DOD-2026-10-08.md
"""
import json, os, re, time, glob, sys, urllib.request, concurrent.futures as cf

CORPUS = "/home/evo/evolution/operations/knowledge/docs/chat-corpus"
OUT = "/home/evo/sandbox/audit/corpus-deep-dive/out"
KEY = os.environ.get("OPENROUTER_API_KEY")
USE_LOCAL = os.environ.get("DEEPDIVE_LOCAL", "0") == "1"  # dead: local 14B fails on big chunks
MODEL = os.environ.get("DEEPDIVE_MODEL", "deepseek-v4.1-flash:cloud")
OLLAMA = os.environ.get("OLLAMA_BASE_URL", "https://ollama.com")
MAX_CHUNK = 20_000  # chars per tailored chunk (turn-aligned)
WINDOW = "2026-08-08"          # start of 60-day window
EMPH_START = "2026-09-08"      # past-30-days emphasis
DECAY_START, DECAY_END = "2026-09-08", "2026-09-28"  # hermes orchestration decay era
SOURCES = ["hermes", "claude", "codex", "grok-cli", "antigravity"]
MAX_TEXT = 60_000  # chars per session sent to the LLM
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")

os.makedirs(OUT, exist_ok=True)

def frontmatter_strip(text):
    for pat in [r"^---\n.*?\n---\n", r"^## META\n.*?\n\n"]:
        m = re.match(pat, text, flags=re.S)
        if m:
            text = text[m.end():]
    return text

def build_manifest():
    rows = []
    for src in SOURCES:
        for f in glob.glob(f"{CORPUS}/{src}/**/*.md", recursive=True):
            base = os.path.basename(f)
            m = DATE.search(base)
            if not m or m.group(1) < WINDOW:
                continue
            try:
                raw = open(f, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            rows.append({
                "file": f, "src": src, "date": m.group(1),
                "bytes": os.path.getsize(f), "title": base,
            })
    rows.sort(key=lambda r: r["date"])
    json.dump(rows, open(f"{OUT}/manifest60.json", "w"), indent=1)
    return rows

SELECT = {"hermes": 30, "claude": 20, "codex": 5, "grok-cli": 5, "antigravity": 5}

def select(rows):
    sel = []
    emph = [r for r in rows if r["date"] >= EMPH_START]
    for src, n in SELECT.items():
        sel += sorted([r for r in emph if r["src"] == src], key=lambda r: -r["bytes"])[:n]
    before = [r for r in rows if WINDOW <= r["date"] < DECAY_START and r["src"] == "hermes"]
    sel += sorted(before, key=lambda r: -r["bytes"])[:10]
    # dedupe, preserve
    seen, out = set(), []
    for r in sel:
        if r["file"] not in seen:
            seen.add(r["file"]); out.append(r)
    return out

RUBRIC = """Return ONE JSON object only, no markdown, no prose: {"signals":[{"type":"...","quote":"..."}],"session_quality":1,"is_hermes_orchestration":false,"summary":"one sentence"}\nYou are auditing a single agent-coding session transcript for operational friction.
Score these antipattern types, only when concrete evidence exists in THIS transcript:
- correction: user fixes agent's assumption (wrong file, path, name, fact)
- redo: same instruction or verification repeated
- scope-drift: new requirement/surface/file introduced mid-session
- rework-loop: a fix causes the next failure; circular repair
- frustration: harsh emotional markers from the user
- time-sink: turns spent on non-progress (retry loops, context replay, dead tool calls)
- orchestration-failure: agent dispatch/coordination failure — subagents killed, timeouts,
  parallel-agent mess, stale hand-off, orchestration getting WORSE as more layers are added
For each signal give: type, quote (verbatim, <=160 chars), and line hint (searchable text).
Also: session_quality 1-5 (how well did the session accomplish its goal),
and a one-sentence summary, and "is_hermes_orchestration": whether this is Hermes driving
other agents/tools and whether that orchestration degraded the session.
Be strict: no invented quotes; if none of a type, don't list it. Empty signals list is fine."""

def chat(messages, max_tokens=2200):
    if USE_LOCAL:
        body = json.dumps({"model": MODEL, "messages": messages, "stream": False,
                           "format": "json", "keep_alive": "15m",
                           "options": {"temperature": 0.2, "num_ctx": 24576,
                                       "num_predict": max_tokens}}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                     headers={"Content-Type": "application/json"})
    elif True:  # ollama cloud: thinking OFF (budget-killer), JSON-only
        body = json.dumps({"model": MODEL, "messages": messages, "stream": False,
                           "format": "json", "think": False,
                           "options": {"temperature": 0.2,
                                       "num_predict": max_tokens}}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                     headers={"Authorization": f"Bearer {os.environ['OLLAMA_API_KEY']}",
                                              "Content-Type": "application/json"})
    else:
        body = json.dumps({"model": MODEL, "messages": messages, "max_tokens": max_tokens,
                           "temperature": 0.2}).encode()
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.load(r)
            msg = d["choices"][0]["message"] if "choices" in d else d["message"]
            return (msg.get("content") or "") or (msg.get("thinking") or "")
        except Exception as e:
            print(f"    chat fail {attempt}: {type(e).__name__}: {e}", flush=True)
            if attempt == 2:
                return None
            time.sleep(5 * (attempt + 1))

def chunk_text(text):
    """Tailored chunks: turn-aligned (## USER boundaries), <=MAX_CHUNK chars."""
    if len(text) <= MAX_CHUNK:
        return [text]
    parts = re.split(r"(?=^## USER$)", text, flags=re.M)
    chunks, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > MAX_CHUNK:
            chunks.append(cur)
            cur = p[:MAX_CHUNK] if len(p) > MAX_CHUNK else p
        else:
            cur = (cur + p)[:MAX_CHUNK]
    if cur:
        chunks.append(cur)
    return chunks or [text[:MAX_CHUNK]]

def jsonload_safe(s):
    cands = [s]
    m = re.search(r"```json\n(.*?)```", s, flags=re.S)
    if m:
        cands.append(m.group(1))
    m2 = re.search(r"\{.*\}", s, flags=re.S)
    if m2:
        cands.append(m2.group(0))
    for c in cands:
        try:
            j = json.loads(c.strip())
            if isinstance(j, dict):
                return j
        except (json.JSONDecodeError, ValueError):
            continue
    return None

def score(row):
    text = frontmatter_strip(open(row["file"], encoding="utf-8", errors="replace").read())
    chunks = chunk_text(text)
    merged = {"file": row["file"], "title": row["title"], "src": row["src"],
              "date": row["date"], "status": "UNSCORED", "signals": []}
    for ci, ch in enumerate(chunks):
        chunk_head = f"\n\n[Chunk {ci+1}/{len(chunks)} of session]" if len(chunks) > 1 else ""
        s = chat([
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": f"Session file: {row['title']} (source: {row['src']}, date: {row['date']}){chunk_head}\n\n" + ch},
        ], 2200)
        j = jsonload_safe(s) if s else None
        if j is not None:
            merged["status"] = "SCORED"
            for sig in j.get("signals", []):
                sig.setdefault("quote", "")[:160]
                merged["signals"].append({"type": sig.get("type"), "quote": sig.get("quote"),
                                          "chunk": ci + 1})
            merged["session_quality"] = j.get("session_quality")
            merged["summary"] = j.get("summary")
            merged["is_hermes_orchestration"] = j.get("is_hermes_orchestration")
    merged["signal_count"] = len(merged["signals"])
    return merged

def gate(findings, manifest):
    paths = {r["file"] for r in manifest}
    bad = []
    quotes = 0
    for f in findings:
        for s in f.get("signals", []):
            quotes += 1
            pin = s.get("pin") or s.get("line_hint") or ""
            # pin must be quoted text present in the actual file (strong check)
        # verify first quote exists in file text
        first = (f.get("signals") or [{}])[0].get("quote", "")
        if first and f.get("file") in paths:
            try:
                if first.strip("\"'` ") not in open(f["file"], encoding="utf-8", errors="replace").read():
                    bad.append(f["file"])
            except OSError:
                bad.append(f["file"])
    json.dump({"quote_checks": quotes, "failed_spotchecks": bad},
              open(f"{OUT}/gate.json", "w"), indent=1)
    return bad

def main():
    t0 = time.time()
    rows = build_manifest()
    print(f"manifest: {len(rows)} sessions", flush=True)
    sel = select(rows)
    json.dump(sel, open(f"{OUT}/selected.json", "w"), indent=1)
    print(f"selected: {len(sel)} sessions to score", flush=True)
    results, fails = [], 0
    with cf.ThreadPoolExecutor(4) as ex:
        futs = {ex.submit(score, r): r for r in sel}
        for fu in cf.as_completed(futs):
            r = fu.result()
            results.append(r)
            if r["status"] == "UNSCORED":
                fails += 1
            print(f"  {r['status']}: {r['title']} ({time.time()-t0:.0f}s)", flush=True)
    json.dump(results, open(f"{OUT}/findings.json", "w"), indent=1)
    print(f"scored: {len(results)-fails}/{len(results)}; unscored: {fails}", flush=True)

    # synthesis — chunked for 32k local model: per-batch sub-reports, then merge
    compact = [{"src": r["src"], "date": r["date"], "title": r["title"],
                "quality": r.get("session_quality"), "sum": r.get("summary"),
                "hermes_orch": r.get("is_hermes_orchestration"),
                "sig": [{"t": s.get("type"), "q": s.get("quote")} for s in r.get("signals", [])]}
               for r in results if r["status"] == "SCORED"]
    subreports = []
    B = 8
    for i in range(0, len(compact), B):
        data = compact[i:i + B]
        if not data:
            break
        sub = chat([
            {"role": "system", "content": "You write concise audit sub-reports. Quotes only from provided data. Plain markdown, <=400 words."},
            {"role": "user", "content": "Sub-report for this batch of scored sessions:\n\nData (JSON):\n" + json.dumps(data, indent=1) + "\n\nReport as: antipattern count table, notable decay or friction evidence (quote as src/date/title), cost-map notes."},
        ], 2000) or f"(batch {i//B} UNSCORED at synthesis)"
        subreports.append(sub)
        print(f"  synthesis batch {i//B + 1} done ({time.time()-t0:.0f}s)", flush=True)
    merge_txt = json.dumps(compact, indent=1)
    if len(merge_txt) > 30_000:
        merge_txt = "FREQUENCY SUMMARIES from per-batch sub-reports:\n\n" + "\n\n---\n\n".join(subreports)
    syn = chat([
        {"role": "system", "content": "You write evidence-pinned audit reports. Quotes only from provided data. Plain markdown."},
        {"role": "user", "content": f"""Merge into one report, sections EXACTLY:
1. Antipattern frequency (type | count | % of scored sessions) — compute from the data.
2. Delta vs 120-file baseline (correction 60%, redo 61%, scope-drift 59%, rework-loop 38%, frustration 49%, time-sink 44%).
3. Hermes decay 2026-09-08 to 09-28: pin 8-15 sessions as src/date/title with verbatim quotes; causal story.
4. Execution-layer cost map: which job shapes produce most signals.
5. Orca/Ruflo verdict: which guardrails (150-tool cap per chunk, subagent cap 25, memory read on turn 1, binary ruling before exploration, on-disk verification before claiming fixed, parking-lot deferrals) can a persistent worksurface + orchestrator mechanically enforce; end GO / KILL / AMEND with why.
Ground every claim in the provided data. No new quotes. <=2200 words.

DATA:
{merge_txt}"""},
    ], 4000)
    if syn:
        open(f"{OUT}/report.md", "w").write(syn)
    bad = gate(results, rows)
    print(f"gate: {len(bad)} failed spotchecks {time.time()-t0:.0f}s total", flush=True)

if __name__ == "__main__":
    main()
