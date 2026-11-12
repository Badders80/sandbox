#!/usr/bin/env python3
"""Independent read-only code audit through Ollama's raw chat API."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://ollama.com/api/chat"
MAX_TOOL_OUTPUT = 30_000

SYSTEM_PROMPT = """You are an independent read-only code auditor. Verify whether numbered claims are true against the filesystem and command output. Do not trust comments or summaries.

Request exactly one tool per reply as JSON:
{"action":"tool","tool":"read","path":"relative/path","start_line":1,"max_lines":400}
{"action":"tool","tool":"list","path":"."}
{"action":"tool","tool":"search","pattern":"text","path":"relative/path"}
{"action":"tool","tool":"git_status"}
{"action":"tool","tool":"git_diff","path":"optional/path"}
{"action":"tool","tool":"verify"}
{"action":"tool","tool":"dod"}
{"action":"tool","tool":"pdfinfo","path":"relative/path"}
{"action":"tool","tool":"pdftotext","path":"relative/path"}

Rules:
- The host runs only these tools inside the disposable worktree.
- `verify` and `dod` each run at most once.
- Cite every PASS/WARN/FAIL with an absolute path:line or real command output.
- A claim contradicted by disk or a failing command is FAIL.
- Use WARN only when the claim works but has a material caveat.
- Include one adversarial/seam finding if one exists.
- Stop inspecting when the evidence is sufficient.

Return final evidence as:
{"action":"final","report":"one-line summary\n\n| # | Claim | Result | Evidence / Fix Required |\n|---|---|---|---|\n...\n\nVERDICT: PASS|WARN|FAIL","graph":{"claims":[],"edges":[]}}

The final non-empty line inside report must be exactly VERDICT: PASS, VERDICT: WARN, or VERDICT: FAIL."""


def load_api_key(path: Path) -> str:
    for line in path.read_text().splitlines():
        if line.startswith("OLLAMA_API_KEY="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                return value
    raise SystemExit(f"OLLAMA_API_KEY not found in {path}")


def api_chat(api_key: str, model: str, messages: list[dict[str, object]]) -> dict:
    body = json.dumps(
        {
            "model": model,
            "stream": False,
            "options": {"temperature": 0.1},
            "messages": messages,
        }
    ).encode()
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            payload = json.loads(response.read())
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(f"Ollama HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Ollama request failed: {error}") from error

    message = payload.get("message")
    if not isinstance(message, dict):
        raise RuntimeError(f"Ollama returned no message object: {payload}")
    if not message.get("content") and not message.get("tool_calls"):
        raise RuntimeError(f"Ollama returned no content or tool call: {payload}")
    return message


def extract_json_object(text: str) -> dict:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError("auditor reply contained no JSON object")


def inside(workdir: Path, raw_path: str) -> Path:
    path = (workdir / raw_path).resolve()
    if path != workdir and workdir not in path.parents:
        raise ValueError(f"path escapes the audit worktree: {raw_path}")
    return path


def truncate(value: str, limit: int = MAX_TOOL_OUTPUT) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"\n\n[truncated at {limit} characters]"


def run_command(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=900,
        check=False,
    )
    output = f"$ {' '.join(args)}\nexit={completed.returncode}\n{completed.stdout}"
    return truncate(output)


def execute_tool(workdir: Path, action: dict, executed: dict[str, str]) -> str:
    tool = action.get("tool")

    if tool == "read":
        path = inside(workdir, str(action.get("path", "")))
        if not path.is_file():
            raise ValueError(f"not a file: {path}")
        lines = path.read_text(errors="replace").splitlines()
        start = max(int(action.get("start_line", 1)), 1)
        count = min(max(int(action.get("max_lines", 400)), 1), 1200)
        selected = lines[start - 1 : start - 1 + count]
        rendered = "\n".join(f"{start + offset:6}: {line}" for offset, line in enumerate(selected))
        return truncate(f"{path} lines {start}-{start + len(selected) - 1}\n{rendered}")

    if tool == "list":
        path = inside(workdir, str(action.get("path", ".")))
        if not path.is_dir():
            raise ValueError(f"not a directory: {path}")
        entries = sorted(path.iterdir(), key=lambda item: item.name)[:500]
        return "\n".join(
            ("d " if item.is_dir() else "f ") + str(item.relative_to(workdir))
            for item in entries
        )

    if tool == "search":
        pattern = str(action.get("pattern", ""))
        if not pattern:
            raise ValueError("search.pattern is required")
        path = inside(workdir, str(action.get("path", ".")))
        args = [
            "rg",
            "-n",
            "--hidden",
            "--glob",
            "!node_modules/**",
            "--glob",
            "!.git/**",
            "--glob",
            "!.next*/**",
            pattern,
            str(path),
        ]
        return run_command(args, workdir)

    if tool == "git_status":
        return run_command(["git", "status", "--short"], workdir)

    if tool == "git_diff":
        path = action.get("path")
        args = ["git", "diff", "--"] + ([str(path)] if path else [])
        return run_command(args, workdir)

    if tool == "verify":
        if "verify" not in executed:
            executed["verify"] = run_command(["pnpm", "verify"], workdir)
        return executed["verify"]

    if tool == "dod":
        if "dod" not in executed:
            executed["dod"] = run_command(["bash", "scripts/legal-package-dod.sh"], workdir)
        return executed["dod"]

    if tool == "pdfinfo":
        path = inside(workdir, str(action.get("path", "")))
        return run_command(["pdfinfo", str(path)], workdir)

    if tool == "pdftotext":
        path = inside(workdir, str(action.get("path", "")))
        return run_command(["pdftotext", str(path), "-"], workdir)

    raise ValueError(f"unknown tool: {tool!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--claims-file", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--model", default="kimi-k2.7-code")
    parser.add_argument("--max-calls", type=int, default=40)
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path.home() / ".config/evo/ollama-active.env",
    )
    args = parser.parse_args()

    workdir = args.workdir.resolve()
    run_dir = args.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    claims = args.claims_file.read_text().strip()
    if not claims:
        raise SystemExit("claims file is empty")

    api_key = load_api_key(args.env_file)
    messages: list[dict[str, object]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Audit worktree: {workdir}\n\n"
                f"Claims:\n{claims}\n\n"
                "Inspect the worktree and return the required final JSON."
            ),
        },
    ]
    executed: dict[str, str] = {}
    transcript: list[dict[str, object]] = []

    for call_number in range(1, args.max_calls + 1):
        message = api_chat(api_key, args.model, messages)
        reply = str(message.get("content") or "")
        native_calls = message.get("tool_calls")
        transcript.append(
            {
                "call": call_number,
                "assistant": reply,
                "thinking": message.get("thinking"),
                "tool_calls": native_calls,
            }
        )
        (run_dir / "transcript.json").write_text(json.dumps(transcript, indent=2) + "\n")

        action: dict | None = None
        if isinstance(native_calls, list) and native_calls:
            first_call = native_calls[0]
            function = first_call.get("function", {}) if isinstance(first_call, dict) else {}
            name = function.get("name")
            arguments = function.get("arguments", {})
            if isinstance(name, str) and isinstance(arguments, dict):
                action = {"action": "tool", "tool": name, **arguments}

        if action is None:
            try:
                action = extract_json_object(reply)
            except ValueError:
                messages.append({"role": "assistant", "content": reply})
                messages.append(
                    {
                        "role": "user",
                        "content": "Invalid reply. Return one JSON tool request or one JSON final object exactly as specified.",
                    }
                )
                continue

        messages.append({"role": "assistant", "content": json.dumps(action)})

        if action.get("action") == "final":
            report = str(action.get("report", "")).strip()
            if not re.search(r"VERDICT:\s*(PASS|WARN|FAIL)\s*$", report):
                messages.append(
                    {
                        "role": "user",
                        "content": "The report must end with VERDICT: PASS, VERDICT: WARN, or VERDICT: FAIL.",
                    }
                )
                continue
            (run_dir / "report.md").write_text(report + "\n")
            (run_dir / "graph.json").write_text(
                json.dumps(action.get("graph", {}), indent=2) + "\n"
            )
            print(report)
            return 1 if report.endswith("VERDICT: FAIL") else 0

        if action.get("action") != "tool":
            messages.append(
                {"role": "user", "content": "Unknown action. Use action=tool or action=final."}
            )
            continue

        try:
            result = execute_tool(workdir, action, executed)
        except Exception as error:
            result = f"TOOL ERROR: {error}"

        transcript.append({"call": call_number, "tool": action, "result": result})
        (run_dir / "transcript.json").write_text(json.dumps(transcript, indent=2) + "\n")
        messages.append(
            {
                "role": "user",
                "content": f"Tool call {call_number}/{args.max_calls} result:\n{result}",
            }
        )

    messages.append(
        {
            "role": "user",
            "content": "Tool-call cap reached. Return the required final JSON now using the evidence gathered.",
        }
    )
    message = api_chat(api_key, args.model, messages)
    reply = str(message.get("content") or "")
    transcript.append({"call": args.max_calls + 1, "assistant": reply, "forced_final": True})
    (run_dir / "transcript.json").write_text(json.dumps(transcript, indent=2) + "\n")
    action = extract_json_object(reply)
    report = str(action.get("report", "")).strip()
    if action.get("action") != "final" or not report:
        raise SystemExit("auditor did not return a usable final report at the call cap")
    (run_dir / "report.md").write_text(report + "\n")
    (run_dir / "graph.json").write_text(json.dumps(action.get("graph", {}), indent=2) + "\n")
    print(report)
    return 1 if report.endswith("VERDICT: FAIL") else 0


if __name__ == "__main__":
    raise SystemExit(main())
