#!/usr/bin/env python3
"""
Stage OpenClaw session output into Grace-Mar's gated pipeline.

This script is stage-only. It never merges into the Record.

Usage:
  python integrations/openclaw_stage.py --user pilot-001 --artifact ./session-note.md
  python integrations/openclaw_stage.py -u pilot-001 --text "we explored fractions in OpenClaw"
"""

import argparse
import hashlib
import json
import os
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
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
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
