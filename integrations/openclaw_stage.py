#!/usr/bin/env python3
"""
Stage OpenClaw session output into Grace-Mar's gated pipeline.

This script is stage-only. It never merges into the Record.

Usage:
  python integrations/openclaw_stage.py --user grace-mar --artifact ./session-note.md
  python integrations/openclaw_stage.py -u grace-mar --text "we explored fractions in OpenClaw"
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _build_content(text: str, artifact: Path | None) -> tuple[str, dict]:
    base = (text or "").strip()
    meta: dict[str, str] = {"source": "openclaw_stage"}
    if artifact and artifact.exists():
        rel = str(artifact)
        digest = _sha256(artifact)
        preview = artifact.read_text(encoding="utf-8", errors="ignore").strip()[:1200]
        if base:
            base = base + "\n\n"
        base += (
            f'we did work in OpenClaw and captured an artifact at "{rel}". '
            f'hash: {digest}. excerpt:\n{preview}'
        )
        meta["artifact_path"] = rel
        meta["artifact_sha256"] = digest
    return base.strip(), meta


def _load_intent_profile(user_id: str) -> dict:
    intent_path = REPO_ROOT / "users" / user_id / "INTENT.md"
    if not intent_path.exists():
        return {"ok": False, "tradeoff_rules": []}
    raw = intent_path.read_text(encoding="utf-8")
    m = re.search(r"```(?:yaml|yml)\s*\n(.*?)```", raw, re.DOTALL)
    if not m:
        return {"ok": False, "tradeoff_rules": []}
    block = m.group(1)
    rules: list[dict] = []
    rules_block = re.search(r"^tradeoff_rules:\s*\n((?:^[ \t]+.+\n?)*)", block, re.MULTILINE)
    if rules_block:
        chunks = re.findall(r"(?:^[ \t]*-\s+.+(?:\n(?![ \t]*-\s).+)*)", rules_block.group(1), re.MULTILINE)
        for idx, chunk in enumerate(chunks, 1):
            rid_m = re.search(r"\bid:\s*([^\n]+)", chunk)
            prio_m = re.search(r"\bprioritize:\s*([^\n]+)", chunk)
            de_m = re.search(r"\bdeprioritize:\s*([^\n]+)", chunk)
            rules.append(
                {
                    "id": rid_m.group(1).strip().strip("\"'") if rid_m else f"INTENT-RULE-{idx:03d}",
                    "prioritize": prio_m.group(1).strip().strip("\"'") if prio_m else "",
                    "deprioritize": de_m.group(1).strip().strip("\"'") if de_m else "",
                }
            )
    return {"ok": True, "tradeoff_rules": rules}


def _keywords(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", (text or "").lower())}


def _detect_constitution_conflicts(content: str, intent_profile: dict) -> list[str]:
    if not intent_profile.get("ok"):
        return []
    observed = _keywords(content)
    conflicts: list[str] = []
    for rule in intent_profile.get("tradeoff_rules", []):
        de = _keywords(rule.get("deprioritize", ""))
        pr = _keywords(rule.get("prioritize", ""))
        if not de:
            continue
        hits_de = observed & de
        if not hits_de:
            continue
        hits_pr = observed & pr if pr else set()
        if hits_pr:
            continue
        conflicts.append(str(rule.get("id") or "UNKNOWN"))
    return conflicts


def _emit_constitution_event(user_id: str, status: str, rule_ids: list[str]) -> None:
    extras = [
        f"status={status}",
        "candidate_source=openclaw",
        f"rule_ids={','.join(rule_ids) if rule_ids else 'none'}",
        "source=openclaw_stage",
        "channel_key=openclaw:stage",
    ]
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            user_id,
            "intent_constitutional_critique",
            "none",
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def stage_openclaw(
    stage_url: str,
    user_id: str,
    text: str,
    artifact: Path | None,
    api_key: str,
) -> dict:
    content, meta = _build_content(text, artifact)
    if not content:
        raise ValueError("Provide --text and/or --artifact")
    intent_profile = _load_intent_profile(user_id)
    conflicts = _detect_constitution_conflicts(content, intent_profile)
    status = "advisory_flagged" if conflicts else "advisory_clear"
    _emit_constitution_event(user_id, status=status, rule_ids=conflicts)
    meta["constitution_check_status"] = status
    if conflicts:
        meta["constitution_rule_ids"] = ",".join(conflicts)
        content = (
            f"{content}\n\n"
            f"CONSTITUTION_ADVISORY: status={status}; rule_ids={','.join(conflicts)}"
        )
    payload = {
        "content": content,
        "user_id": user_id,
        "title": "OpenClaw session handback",
        "selection_text": "",
        **meta,
    }
    req = Request(stage_url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("X-Api-Key", api_key)
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage OpenClaw output to Grace-Mar /stage endpoint.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--stage-url", default=os.getenv("OPENCLAW_STAGE_URL", "http://127.0.0.1:5050/stage"))
    parser.add_argument("--text", default="", help='Natural language summary (e.g. "we did X in OpenClaw")')
    parser.add_argument("--artifact", default="", help="Optional artifact file path")
    parser.add_argument("--api-key", default=os.getenv("HANDBACK_API_KEY", "").strip(), help="Optional X-Api-Key")
    args = parser.parse_args()

    artifact = Path(args.artifact) if args.artifact else None
    try:
        result = stage_openclaw(
            stage_url=args.stage_url,
            user_id=args.user,
            text=args.text,
            artifact=artifact,
            api_key=args.api_key,
        )
        if not result.get("ok"):
            print(f"Stage failed: {result}", flush=True)
            return 1
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as e:
        print(f"Stage error: {e}", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
