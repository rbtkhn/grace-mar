#!/usr/bin/env python3
"""
HTTP webhook for structured handback of checkpoints or transcripts from external LLM chats.

Accepts POST /handback with JSON body { "content": "..." } or plain text.
Optional: HANDBACK_API_KEY env var — if set, require X-Api-Key header.

Run: python scripts/handback_server.py
     (or: HANDBACK_API_KEY=secret python scripts/handback_server.py)

Deploy alongside the bot or as a separate service. Integrations (Custom GPTs,
APIs) POST checkpoints or transcripts here; they flow into the analyst pipeline.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = os.getenv("HANDBACK_API_KEY", "").strip()
MAX_CONTENT = 50_000  # chars


def _run_handback(content: str) -> bool:
    """Run analyst on handback content. Returns True if staged."""
    from bot.core import analyze_activity_report

    synthetic = f"we did a chat in an external LLM (API handback). here is the checkpoint or transcript:\n\n{content}"
    return analyze_activity_report(synthetic, "handback:api")


@app.route("/handback", methods=["POST"])
def handback() -> tuple:
    if API_KEY and request.headers.get("X-Api-Key") != API_KEY:
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


@app.route("/health", methods=["GET"])
def health() -> tuple:
    return jsonify({"ok": True}), 200


def main() -> None:
    port = int(os.getenv("PORT", "5050"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
