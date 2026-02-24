#!/usr/bin/env python3
"""
HTTP webhook for structured handback of checkpoints or transcripts from external LLM chats.

Endpoints:
- POST /handback — Checkpoints/transcripts from external LLMs. JSON { "content": "..." } or plain text.
- POST /stage   — Activity reports from browser extension. JSON { "content": "we read...", "url": "..." }.
                  Returns { ok, staged, pending_count } for confirmation.
- GET  /status  — Pipeline status for extension popup ({ ok, pending_count, oldest_pending_days }).
- GET  /health  — Health check.

Security model:
- Loopback requests (127.0.0.1 / ::1) are allowed without API key.
- Non-loopback requests require X-Api-Key matching HANDBACK_API_KEY.
- Server binds to 127.0.0.1 by default (override with HANDBACK_HOST).

Run: python scripts/handback_server.py
     (or: HANDBACK_API_KEY=secret python scripts/handback_server.py)

Deploy alongside the bot or as a separate service. See extension/README.md for browser extension setup.
"""

import os
import sys
from pathlib import Path
from ipaddress import ip_address

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = os.getenv("HANDBACK_API_KEY", "").strip()
MAX_CONTENT = 50_000  # chars


def _is_loopback_request() -> bool:
    """Allow unauthenticated access only from local loopback."""
    remote = (request.remote_addr or "").strip()
    if not remote:
        return False
    try:
        return ip_address(remote).is_loopback
    except ValueError:
        return False


def _is_authorized() -> bool:
    """Authorize if valid API key OR local loopback request."""
    header_key = (request.headers.get("X-Api-Key") or "").strip()
    if API_KEY and header_key == API_KEY:
        return True
    return _is_loopback_request()


def _run_handback(content: str) -> bool:
    """Run analyst on handback content. Returns True if staged."""
    from bot.core import analyze_activity_report

    synthetic = f"we did a chat in an external LLM (API handback). here is the checkpoint or transcript:\n\n{content}"
    return analyze_activity_report(synthetic, "handback:api")


@app.route("/handback", methods=["POST"])
def handback() -> tuple:
    if not _is_authorized():
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    if request.is_json:
        data = request.get_json() or {}
        content = (data.get("content") or data.get("text") or "").strip()
    else:
        content = (request.get_data(as_text=True) or "").strip()

    if not content:
        return jsonify({"ok": False, "error": "empty content"}), 400

    if len(content) > MAX_CONTENT:
        return jsonify({"ok": False, "error": f"content too long (max {MAX_CONTENT} chars)"}), 400

    try:
        staged = _run_handback(content)
        return jsonify({"ok": True, "staged": staged})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


def _run_stage(content: str, user_id: str = "") -> tuple[bool, int]:
    """Run analyst on activity report. Returns (staged, pending_count)."""
    from bot.core import analyze_activity_report, get_pending_candidates

    channel_key = f"extension:browser:{user_id}" if user_id else "extension:browser"
    staged = analyze_activity_report(content, channel_key)
    count = len(get_pending_candidates())
    return (staged, count)


@app.route("/stage", methods=["POST"])
def stage() -> tuple:
    """Stage activity report from browser extension (local only).
    Accepts JSON: { "content": "we read...", "url": "..." }.
    content is required; url is optional provenance.
    Returns { ok, staged, pending_count } for extension confirmation."""
    if not _is_authorized():
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    if not request.is_json:
        return jsonify({"ok": False, "error": "JSON body required"}), 400

    data = request.get_json() or {}
    content = (data.get("content") or data.get("text") or "").strip()
    url = (data.get("url") or "").strip()
    user_id = (data.get("user_id") or "").strip()
    title = (data.get("title") or "").strip()
    selection_text = (data.get("selection_text") or "").strip()

    if not content:
        return jsonify({"ok": False, "error": "empty content"}), 400

    meta_parts = []
    if user_id:
        meta_parts.append(f"user_id={user_id}")
    if title:
        meta_parts.append(f"title={title}")
    if url:
        meta_parts.append(f"url={url}")
    if selection_text:
        meta_parts.append(f'selection="{selection_text[:500]}"')
    if meta_parts:
        content = f"{content} META: {'; '.join(meta_parts)}"

    if len(content) > MAX_CONTENT:
        return jsonify({"ok": False, "error": f"content too long (max {MAX_CONTENT} chars)"}), 400

    try:
        staged, pending_count = _run_stage(content, user_id=user_id)
        return jsonify({
            "ok": True,
            "staged": staged,
            "pending_count": pending_count,
            "user_id": user_id or None,
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status() -> tuple:
    if not _is_authorized():
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    from bot.core import get_pending_candidates, PIPELINE_EVENTS_PATH
    from datetime import datetime
    import json

    pending = get_pending_candidates()
    pending_ids = {c.get("id") for c in pending}
    oldest_pending_days = None
    if PIPELINE_EVENTS_PATH.exists() and pending_ids:
        try:
            staged_ts = []
            for line in PIPELINE_EVENTS_PATH.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row.get("event") != "staged":
                    continue
                if row.get("candidate_id") not in pending_ids:
                    continue
                ts = str(row.get("ts") or "").strip()
                if not ts:
                    continue
                staged_ts.append(datetime.fromisoformat(ts))
            if staged_ts:
                oldest_pending_days = max(0, (datetime.now() - min(staged_ts)).days)
        except Exception:
            oldest_pending_days = None
    return jsonify({
        "ok": True,
        "pending_count": len(pending),
        "oldest_pending_days": oldest_pending_days,
    }), 200


@app.route("/health", methods=["GET"])
def health() -> tuple:
    return jsonify({"ok": True}), 200


def main() -> None:
    port = int(os.getenv("PORT", "5050"))
    host = os.getenv("HANDBACK_HOST", "127.0.0.1").strip() or "127.0.0.1"
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
