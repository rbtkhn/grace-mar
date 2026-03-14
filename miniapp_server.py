#!/usr/bin/env python3
"""
Grace-Mar Q&A Mini App server.

Serves the interactive Q&A Mini App and provides the /api/ask endpoint.
Optional: Telegram webhook (when TELEGRAM_BOT_TOKEN and webhook URL are set).
Deploy to Railway, Render, or run locally with ngrok for Telegram testing.

Usage:
    pip install flask python-dotenv openai python-telegram-bot
    OPENAI_API_KEY=... python miniapp_server.py

Set PORT (default 5000) for hosting. Enable CORS if Mini App is on a different origin.
Real-time exchanges are appended to users/<user>/session-transcript.md (same as Telegram).
SELF-ARCHIVE is updated only when candidates are merged via process_approved_candidates (gated).
For Telegram webhook: TELEGRAM_BOT_TOKEN, WEBHOOK_BASE_URL (or RENDER_EXTERNAL_URL on Render).
"""

import asyncio
import json
import logging
import os
import sys
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")

from openai import OpenAI

from bot.prompt import SYSTEM_PROMPT
from bot.core import (
    run_lookup,
    run_grounded_response,
    LOOKUP_TRIGGER,
    AFFIRMATIVE_WORDS,
    AFFIRMATIVE_PHRASES,
    emit_pipeline_event,
    is_low_risk_candidate,
    quick_merge_candidate,
    update_candidate_status,
)
from scripts.recursion_gate_review import filter_review_candidates, get_review_candidate, parse_review_candidates

app = Flask(__name__, static_folder="miniapp", static_url_path="")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip()
SESSION_TRANSCRIPT_PATH = REPO_ROOT / "users" / USER_ID / "session-transcript.md"
RECURSION_GATE_PATH = REPO_ROOT / "users" / USER_ID / "recursion-gate.md"
OPERATOR_FETCH_SECRET = os.getenv("OPERATOR_FETCH_SECRET", "").strip()
OPERATOR_NAME = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web").strip() or "operator-web"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
WEBHOOK_BASE_URL = (
    os.getenv("WEBHOOK_BASE_URL", "").strip()
    or os.getenv("RENDER_EXTERNAL_URL", "").strip()
).rstrip("/")
logger = logging.getLogger(__name__)

_telegram_app = None
_telegram_loop = None


def _start_telegram_webhook() -> None:
    """Start Telegram webhook in a background thread. Run once at startup."""
    global _telegram_app, _telegram_loop
    if not TELEGRAM_BOT_TOKEN or not WEBHOOK_BASE_URL:
        return
    if not OPENAI_API_KEY:
        logger.warning("Telegram webhook skipped: OPENAI_API_KEY not set")
        return

    def _run_bot() -> None:
        global _telegram_app, _telegram_loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        _telegram_loop = loop

        sys.path.insert(0, str(REPO_ROOT))
        from bot.bot import create_application
        from telegram import Update

        app = create_application(webhook_mode=True)
        _telegram_app = app

        async def _setup() -> None:
            await app.initialize()
            await app.start()
            webhook_url = f"{WEBHOOK_BASE_URL}/telegram/webhook"
            await app.bot.set_webhook(url=webhook_url, allowed_updates=Update.ALL_TYPES)
            logger.info("Telegram webhook set: %s", webhook_url)

        loop.run_until_complete(_setup())
        loop.run_forever()

    t = threading.Thread(target=_run_bot, daemon=True)
    t.start()
    logger.info("Telegram webhook thread started")


def _format_archive_block(event: str, text: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"**[{ts}]** `{event}` (miniapp)\n"]
    for line in (text or "").strip().splitlines():
        lines.append(f"> {line}\n")
    lines.append("\n")
    return "".join(lines)


def _session_transcript_header() -> str:
    return (
        "# SESSION TRANSCRIPT\n\n"
        "> Raw conversation log for operator continuity. Not part of the Record. "
        "Approved content is written to SELF-ARCHIVE on merge.\n\n---\n\n"
    )


def _append_to_session_transcript(blocks: str) -> None:
    """Append exchange to session-transcript.md (real-time log). self-archive.md is gated (merge only)."""
    try:
        SESSION_TRANSCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not SESSION_TRANSCRIPT_PATH.exists():
            SESSION_TRANSCRIPT_PATH.write_text(_session_transcript_header(), encoding="utf-8")
        with SESSION_TRANSCRIPT_PATH.open("a", encoding="utf-8") as f:
            f.write(blocks.strip() + "\n\n")
    except Exception as e:
        logger.warning("Session transcript write error: %s", e)


def _archive_miniapp(user_message: str, reply: str, is_lookup: bool = False, lookup_question: str | None = None) -> None:
    """Append exchange to session-transcript.md (same policy as bot: real-time log; self-archive.md only on merge). Runs in background."""
    blocks = _format_archive_block("USER", user_message)
    if is_lookup and lookup_question:
        blocks += _format_archive_block("LOOKUP REQUEST", lookup_question)
    blocks += _format_archive_block("GRACE-MAR (lookup)" if is_lookup else "GRACE-MAR", reply)

    def _run():
        _append_to_session_transcript(blocks)

    threading.Thread(target=_run, daemon=True).start()


def _is_affirmative(text: str) -> bool:
    normalized = text.strip().lower().rstrip("!.,")
    return normalized in AFFIRMATIVE_WORDS or any(p in normalized for p in AFFIRMATIVE_PHRASES)


def _last_user_message_before(history: list, before_index: int) -> str | None:
    """Return the last user message before the given index."""
    for i in range(before_index - 1, -1, -1):
        if history[i].get("role") == "user":
            return (history[i].get("content") or "").strip()
    return None


def _should_run_lookup(message: str, history: list) -> str | None:
    """If this is an affirmative follow-up to a lookup offer, return the question to look up."""
    if not history or len(history) < 2:
        return None
    last = history[-1]
    if last.get("role") != "assistant":
        return None
    last_content = (last.get("content") or "").strip()
    if LOOKUP_TRIGGER not in last_content.lower():
        return None
    if not _is_affirmative(message):
        return None
    question = _last_user_message_before(history, len(history))
    return question if question else None


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():
    """Receive Telegram updates. Only active when TELEGRAM_BOT_TOKEN is set."""
    if _telegram_app is None or _telegram_loop is None:
        return "", 200  # Silently ignore if webhook not configured
    try:
        data = request.get_json()
        if not data:
            return "", 400
        from telegram import Update

        update = Update.de_json(data, _telegram_app.bot)
        asyncio.run_coroutine_threadsafe(
            _telegram_app.update_queue.put(update), _telegram_loop
        ).result(timeout=5.0)
    except Exception as e:
        logger.exception("Telegram webhook error: %s", e)
        return "", 500
    return "", 200


@app.route("/")
def index():
    """Q&A Mini App — interactive chat with Grace-Mar."""
    return send_from_directory("miniapp", "index.html")


@app.route("/operator/inbox")
def operator_inbox():
    """Browser review surface for RECURSION-GATE."""
    return send_from_directory("miniapp", "operator-inbox.html")


@app.route("/i/<token>")
def interview_by_token(token: str):
    """Shareable interview link — reviewer chats with fork, exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.route("/me/<user_id>")
def interview_by_user(user_id: str):
    """Per-user interview link (e.g. /me/grace-mar). Exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.after_request
def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp


def _operator_auth():
    """Require Bearer token matching OPERATOR_FETCH_SECRET. Return (ok, error_response)."""
    if not OPERATOR_FETCH_SECRET:
        return False, (jsonify({"error": "OPERATOR_FETCH_SECRET not configured"}), 503)
    auth = request.headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        return False, (jsonify({"error": "Authorization: Bearer <secret> required"}), 401)
    token = auth[7:].strip()
    if token != OPERATOR_FETCH_SECRET:
        return False, (jsonify({"error": "Invalid secret"}), 403)
    return True, None


@app.route("/operator/session-transcript", methods=["GET"])
def operator_session_transcript():
    """Return session-transcript.md content for operator sync (e.g. into Cursor). Requires OPERATOR_FETCH_SECRET."""
    ok, err = _operator_auth()
    if not ok:
        return err
    if not SESSION_TRANSCRIPT_PATH.exists():
        return jsonify({"error": "session-transcript.md not found", "path": str(SESSION_TRANSCRIPT_PATH)}), 404
    return SESSION_TRANSCRIPT_PATH.read_text(encoding="utf-8"), 200, {"Content-Type": "text/markdown; charset=utf-8"}


@app.route("/operator/recursion-gate", methods=["GET"])
def operator_recursion_gate():
    """Return recursion-gate.md content for operator sync. Requires OPERATOR_FETCH_SECRET."""
    ok, err = _operator_auth()
    if not ok:
        return err
    if not RECURSION_GATE_PATH.exists():
        return jsonify({"error": "recursion-gate.md not found", "path": str(RECURSION_GATE_PATH)}), 404
    return RECURSION_GATE_PATH.read_text(encoding="utf-8"), 200, {"Content-Type": "text/markdown; charset=utf-8"}


@app.route("/operator/gate-candidates", methods=["GET"])
def operator_gate_candidates():
    """Return structured review candidates for the approval inbox."""
    ok, err = _operator_auth()
    if not ok:
        return err
    rows = parse_review_candidates(USER_ID)
    rows = filter_review_candidates(
        rows,
        status=(request.args.get("status") or "").strip(),
        risk_tier=(request.args.get("risk_tier") or "").strip(),
        territory=(request.args.get("territory") or "").strip(),
    )
    return jsonify({"user_id": USER_ID, "count": len(rows), "items": rows})


@app.route("/operator/gate-candidates/<candidate_id>/action", methods=["POST"])
def operator_gate_candidate_action(candidate_id: str):
    """Apply review actions while keeping recursion-gate.md canonical."""
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").strip().lower()
    if action not in {"approve", "reject", "defer", "quick_merge"}:
        return jsonify({"error": "action must be approve, reject, defer, or quick_merge"}), 400

    row = get_review_candidate(USER_ID, candidate_id)
    if not row:
        return jsonify({"error": f"{candidate_id} not found above ## Processed"}), 404

    channel_key = "operator:web"
    source = "miniapp_server:approval_inbox"
    rejection_reason = (payload.get("rejection_reason") or "").strip() or None

    if action == "approve":
        if row.get("status") != "approved":
            changed = update_candidate_status(
                candidate_id,
                "approved",
                channel_key=channel_key,
                actor=OPERATOR_NAME,
                source=source,
            )
            if not changed:
                return jsonify({"error": f"could not approve {candidate_id}"}), 409
        return jsonify({"ok": True, "action": action, "candidate": get_review_candidate(USER_ID, candidate_id)})

    if action == "reject":
        changed = update_candidate_status(
            candidate_id,
            "rejected",
            rejection_reason=rejection_reason,
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
        )
        if not changed:
            return jsonify({"error": f"could not reject {candidate_id}"}), 409
        return jsonify({"ok": True, "action": action, "candidate": get_review_candidate(USER_ID, candidate_id)})

    if action == "defer":
        emit_pipeline_event(
            "review_feedback",
            candidate_id,
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
            decision="defer",
        )
        return jsonify({"ok": True, "action": action, "candidate": row})

    if not is_low_risk_candidate(candidate_id):
        return jsonify({"error": f"{candidate_id} is not quick-merge eligible"}), 409
    if row.get("status") == "pending":
        changed = update_candidate_status(
            candidate_id,
            "approved",
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
        )
        if not changed:
            return jsonify({"error": f"could not approve {candidate_id} before quick merge"}), 409
    merged_ok, message = quick_merge_candidate(candidate_id, OPERATOR_NAME)
    if not merged_ok:
        return jsonify({"error": message}), 500
    emit_pipeline_event(
        "review_feedback",
        candidate_id,
        channel_key=channel_key,
        actor=OPERATOR_NAME,
        source=source,
        decision="quick_merge",
    )
    return jsonify({"ok": True, "action": action, "message": message, "candidate_id": candidate_id})


@app.route("/api/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return "", 204
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY not configured"}), 500
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "message required"}), 400
    history = data.get("history") or []
    grounded = data.get("mode") == "grounded"
    interview = data.get("interview") is True

    try:
        channel_key = "interview" if interview else "miniapp"
        if grounded:
            reply = run_grounded_response(message, channel_key=channel_key, history=history)
            if not interview:
                _archive_miniapp(message, reply, is_lookup=False)
            return jsonify({"response": reply})

        # Affirmative follow-up to "do you want me to look it up?" → run lookup
        question = _should_run_lookup(message, history)
        if question:
            reply = run_lookup(question, channel_key="miniapp")
            _archive_miniapp(message, reply, is_lookup=True, lookup_question=question)
            return jsonify({"response": reply})

        # Normal flow: SYSTEM_PROMPT + history + new message
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h in history:
            role = h.get("role")
            content = (h.get("content") or "").strip()
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": message})

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=200,
            temperature=0.9,
        )
        reply = response.choices[0].message.content.strip()
        if not interview:
            _archive_miniapp(message, reply, is_lookup=False)
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and WEBHOOK_BASE_URL:
        _start_telegram_webhook()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
