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
Set GITHUB_TOKEN and GRACE_MAR_REPO (e.g. rbtkhn/grace-mar) to archive to ARCHIVE.md.
For Telegram webhook: TELEGRAM_BOT_TOKEN, WEBHOOK_BASE_URL (or RENDER_EXTERNAL_URL on Render).
"""

import asyncio
import base64
import json
import logging
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

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
)

app = Flask(__name__, static_folder="miniapp", static_url_path="")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GRACE_MAR_REPO = os.getenv("GRACE_MAR_REPO", "rbtkhn/grace-mar").strip()
ARCHIVE_PATH = "users/pilot-001/ARCHIVE.md"
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


def _append_to_github_archive(blocks: str) -> None:
    if GITHUB_TOKEN and GRACE_MAR_REPO:
        _append_via_github_api(blocks)
    else:
        _append_to_local_file(blocks)


def _append_to_local_file(blocks: str) -> None:
    """Fallback for local dev when GITHUB_TOKEN is not set."""
    try:
        path = REPO_ROOT / ARCHIVE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(
                "# CONVERSATION ARCHIVE\n\n> Append-only log (Telegram, WeChat, Mini App). Local dev.\n\n---\n\n",
                encoding="utf-8",
            )
        with path.open("a", encoding="utf-8") as f:
            f.write(blocks.strip() + "\n")
    except Exception as e:
        logger.warning("Archive local file error: %s", e)


def _append_via_github_api(blocks: str) -> None:
    try:
        owner, repo = GRACE_MAR_REPO.split("/", 1)
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{ARCHIVE_PATH}"
        req = Request(
            url,
            headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"},
        )
        try:
            with urlopen(req) as r:
                data = json.loads(r.read())
                content_b64 = data.get("content", "").replace("\n", "")
                sha = data.get("sha", "")
            content = base64.b64decode(content_b64).decode("utf-8")
        except HTTPError as e:
            if e.code != 404:
                raise
            content = ""
            sha = ""
        header = "# CONVERSATION ARCHIVE\n\n> Append-only log of all Grace-Mar interactions (Telegram, WeChat, Mini App). One mind, multiple channels.\n\n---\n\n"
        base = content if content else header
        new_content = base.rstrip() + "\n\n" + blocks.strip() + "\n"
        payload = {"message": "miniapp: archive exchange", "content": base64.b64encode(new_content.encode()).decode()}
        if sha:
            payload["sha"] = sha
        put_data = json.dumps(payload).encode()
        put_req = Request(url, data=put_data, method="PUT")
        put_req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
        put_req.add_header("Accept", "application/vnd.github+json")
        put_req.add_header("Content-Type", "application/json")
        urlopen(put_req)
    except HTTPError as e:
        logger.warning("Archive GitHub API error: %s %s", e.code, e.reason)
    except Exception as e:
        logger.warning("Archive GitHub API error: %s", e)


def _archive_miniapp(user_message: str, reply: str, is_lookup: bool = False, lookup_question: str | None = None) -> None:
    """Append exchange to ARCHIVE.md (same file as bot). Runs in background."""
    blocks = _format_archive_block("USER", user_message)
    if is_lookup and lookup_question:
        blocks += _format_archive_block("LOOKUP REQUEST", lookup_question)
    blocks += _format_archive_block("GRACE-MAR (lookup)" if is_lookup else "GRACE-MAR", reply)

    def _run():
        _append_to_github_archive(blocks)

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
    return send_from_directory("miniapp", "index.html")


@app.route("/i/<token>")
def interview_by_token(token: str):
    """Shareable interview link — reviewer chats with fork, exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.route("/me/<user_id>")
def interview_by_user(user_id: str):
    """Per-user interview link (e.g. /me/pilot-001). Exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.after_request
def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


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
