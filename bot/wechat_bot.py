"""
Grace-Mar WeChat Bot

A WeChat Official Account (公众号) bot that responds as Grace-Mar.
Uses the same emulation core as the Telegram bot. Requires a web server
because WeChat sends messages via HTTP callback.

Usage:
    1. Register a WeChat Official Account at https://mp.weixin.qq.com
    2. Set Server URL in Account settings to https://your-domain/wechat
    3. Copy .env.example to .env and add WECHAT_* keys
    4. pip install -r requirements.txt
    5. python wechat_bot.py

See WECHAT-SETUP.md for detailed setup instructions.
"""

import os
import logging

from flask import Flask, request

from wechatpy import parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import create_reply

from core import (
    get_response,
    archive,
    reset_conversation,
    get_greeting,
    get_reset_message,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

WECHAT_TOKEN = os.getenv("WECHAT_TOKEN")
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID")
WECHAT_APP_SECRET = os.getenv("WECHAT_APP_SECRET")


def _channel_key(openid: str) -> str:
    return f"wechat:{openid}"


@app.route("/wechat", methods=["GET"])
def wechat_verify():
    """WeChat server verification. Must return echostr to confirm URL."""
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")

    if not WECHAT_TOKEN:
        logger.error("WECHAT_TOKEN not configured")
        return "config error", 500

    try:
        check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        return echostr
    except InvalidSignatureException:
        logger.warning("Invalid WeChat signature")
        return "invalid signature", 403


@app.route("/wechat", methods=["POST"])
def wechat_message():
    """Handle incoming WeChat messages."""
    # Verify signature if present (plain mode uses 'signature', encrypted uses 'msg_signature')
    if WECHAT_TOKEN:
        sig = request.args.get("msg_signature") or request.args.get("signature")
        ts = request.args.get("timestamp")
        nc = request.args.get("nonce")
        if sig and ts and nc:
            try:
                check_signature(WECHAT_TOKEN, sig, ts, nc)
            except InvalidSignatureException:
                logger.warning("Invalid WeChat signature on POST")
                return "invalid signature", 403

    xml = request.data
    if not xml:
        return "ok", 200

    msg = parse_message(xml)
    openid = msg.source
    key = _channel_key(openid)

    # WeChat event: subscribe = first follow
    if msg.type == "event" and msg.event == "subscribe":
        reset_conversation(key)
        greeting = get_greeting()
        archive("WECHAT SUBSCRIBE", key, greeting)
        reply = create_reply(greeting, msg)
        return reply.render()

    # Only handle text messages
    if msg.type != "text":
        reply = create_reply("i can only read text right now! try sending me a message.", msg)
        return reply.render()

    user_message = msg.content.strip()

    # Handle text commands (WeChat has no /start, we use keywords)
    normalized = user_message.lower().strip()
    if normalized in ("start", "开始", "hello", "hi", "你好"):
        reset_conversation(key)
        greeting = get_greeting()
        archive("SESSION START", key, greeting)
        reply = create_reply(greeting, msg)
        return reply.render()
    if normalized in ("reset", "重置", "forget"):
        reset_conversation(key)
        msg_text = get_reset_message()
        archive("SESSION RESET", key, msg_text)
        reply = create_reply(msg_text, msg)
        return reply.render()

    try:
        response = get_response(key, user_message)
        reply = create_reply(response, msg)
        return reply.render()
    except Exception:
        logger.exception("Error generating response")
        reply = create_reply("um... i got confused. can you say that again?", msg)
        return reply.render()


def main() -> None:
    if not WECHAT_TOKEN:
        raise RuntimeError("WECHAT_TOKEN not set in .env")

    from core import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in .env")

    from pathlib import Path
    import sys

    _scripts = Path(__file__).resolve().parent.parent / "scripts"
    if str(_scripts) not in sys.path:
        sys.path.insert(0, str(_scripts))
    from repo_io import assert_canonical_record_layout

    uid = (os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")
    assert_canonical_record_layout(uid, context="WeChat bot")

    port = int(os.getenv("WECHAT_PORT", "5000"))
    host = os.getenv("WECHAT_HOST", "0.0.0.0")

    logger.info("Grace-Mar WeChat bot starting on %s:%s", host, port)
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
