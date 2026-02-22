"""
Grace-Mar Telegram Bot

A Telegram bot that responds as Grace-Mar, powered by her
cognitive fork profile data and an OpenAI LLM backend.

Usage (local polling):
    1. Copy .env.example to .env and fill in your keys
    2. pip install -r bot/requirements.txt
    3. python -m bot.bot   # from repo root

For production: use webhook mode via miniapp_server (see docs/TELEGRAM-WEBHOOK-SETUP.md).
"""
# Allow running as script: python bot/bot.py (simulate package for relative imports)
if __package__ is None:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "bot"

import os
import logging

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    MenuButtonWebApp,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from .core import (
    get_response,
    archive,
    reset_conversation,
    get_greeting,
    get_reset_message,
    get_pending_candidates,
    update_candidate_status,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DASHBOARD_MINIAPP_URL = os.getenv("DASHBOARD_MINIAPP_URL", "").rstrip("/")


def _channel_key(chat_id: int) -> str:
    return f"telegram:{chat_id}"


# Session paths shown on /start — instructions/commands to Grace-Mar.
# Each option sets a different interaction model; tapping sends that text to Grace-Mar.
# All must be actions Grace-Mar can execute (ask, help, explore, chat).
# - Ask me what I'm thinking: thought-exposure path (she asks, user shares, she responds)
# - Look something up: lookup flow (user asks, she looks up and explains)
# - Explore: curiosity-driven topic dive
# - Ask me what I'm curious about: she asks, user answers
# - Chat: open conversation
START_PROMPT_OPTIONS = [
    [
        KeyboardButton("Ask me what I'm thinking"),
        KeyboardButton("Look something up for me"),
    ],
    [
        KeyboardButton("Explore a topic with me"),
        KeyboardButton("Ask me what I'm curious about"),
    ],
    [
        KeyboardButton("Chat with me"),
    ],
]

START_KEYBOARD = ReplyKeyboardMarkup(
    START_PROMPT_OPTIONS,
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Or type anything — buttons are optional",
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    reset_conversation(key)
    greeting = get_greeting()
    archive("SESSION START", key, greeting)
    await update.message.reply_text(
        greeting,
        reply_markup=START_KEYBOARD,
    )


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not DASHBOARD_MINIAPP_URL:
        await update.message.reply_text(
            "Dashboard Mini App URL not configured. Set DASHBOARD_MINIAPP_URL in .env and "
            "serve the dashboard over HTTPS. See docs/MINIAPP-SETUP.md."
        )
        return
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Open Dashboard", web_app=WebAppInfo(url=DASHBOARD_MINIAPP_URL))
    )
    await update.message.reply_text(
        "Open the fork dashboard to view profile, pipeline, benchmarks, and disclosure:",
        reply_markup=keyboard,
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    reset_conversation(key)
    msg = get_reset_message()
    archive("SESSION RESET", key, msg)
    await update.message.reply_text(msg, reply_markup=START_KEYBOARD)


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show pending pipeline candidates with Approve/Reject buttons."""
    candidates = get_pending_candidates()
    if not candidates:
        await update.message.reply_text("nothing to review right now! when we add something new, you'll see it here.")
        return
    lines = [f"You have {len(candidates)} thing{'s' if len(candidates) != 1 else ''} to review:\n"]
    buttons = []
    for c in candidates[:5]:  # max 5 rows
        short = c["summary"][:50] + "…" if len(c["summary"]) > 50 else c["summary"]
        lines.append(f"• {c['id']}: {short}")
        buttons.append([
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{c['id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{c['id']}"),
        ])
    keyboard = InlineKeyboardMarkup(buttons)
    text = "\n".join(lines)
    if len(candidates) > 5:
        text += f"\n… and {len(candidates) - 5} more. Type /review again after approving to see the rest."
    await update.message.reply_text(text, reply_markup=keyboard)


async def callback_approve_reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Approve/Reject button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if ":" not in data:
        return
    action, candidate_id = data.split(":", 1)
    status = "approved" if action == "approve" else "rejected"
    ok = update_candidate_status(candidate_id, status)
    if ok:
        emoji = "✅" if action == "approve" else "❌"
        await query.edit_message_text(f"{emoji} {candidate_id} — {status}")
    else:
        await query.edit_message_text(f"couldn't update {candidate_id}")


async def reject_with_reason(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reject a candidate with optional reason: /reject CANDIDATE-123 [reason].
    Reason is stored in PIPELINE-EVENTS for learning from rejection."""
    args = context.args or []
    if not args:
        await update.message.reply_text(
            "Usage: /reject CANDIDATE-123 [optional reason]\n"
            "Example: /reject CANDIDATE-0045 too trivial"
        )
        return
    candidate_id = args[0]
    reason = " ".join(args[1:]).strip() if len(args) > 1 else None
    if not candidate_id.upper().startswith("CANDIDATE-"):
        await update.message.reply_text(f"Expected CANDIDATE-XXXX, got {candidate_id}")
        return
    ok = update_candidate_status(candidate_id, "rejected", rejection_reason=reason)
    if ok:
        msg = f"❌ {candidate_id} — rejected"
        if reason:
            msg += f" (reason: {reason})"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text(f"couldn't update {candidate_id} (not pending?)")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    user_message = update.message.text

    try:
        response = get_response(key, user_message)
        await update.message.reply_text(response)
    except Exception:
        logger.exception("Error generating response")
        await update.message.reply_text("um... i got confused. can you say that again?")


async def handle_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Transcribe voice message and process like text (chat or 'we did X' pipeline)."""
    from .core import transcribe_voice

    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    voice = update.message.voice

    if not voice:
        await update.message.reply_text("i didn't get that — can you try again?")
        return

    try:
        file = await context.bot.get_file(voice.file_id)
        buf = await file.download_as_bytearray()
        transcript = transcribe_voice(bytes(buf), channel_key=key)
    except Exception:
        logger.exception("Voice download/transcribe error")
        await update.message.reply_text("i couldn't understand the voice message — can you type it?")
        return

    if not transcript:
        await update.message.reply_text("i couldn't make out what you said — can you try again or type it?")
        return

    try:
        response = get_response(key, transcript)
        await update.message.reply_text(response)
    except Exception:
        logger.exception("Error generating response after voice")
        await update.message.reply_text("um... i got confused. can you say that again?")


def create_application(webhook_mode: bool = False) -> Application:
    """Build and return the configured Telegram Application.
    When webhook_mode=True, uses updater=None for custom webhook (caller injects updates)."""
    async def set_menu_button(application: Application) -> None:
        if DASHBOARD_MINIAPP_URL:
            await application.bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="Dashboard", web_app=WebAppInfo(url=DASHBOARD_MINIAPP_URL))
            )
            logger.info("Dashboard menu button configured: %s", DASHBOARD_MINIAPP_URL)

    builder = Application.builder().token(TELEGRAM_TOKEN).post_init(set_menu_button)
    if webhook_mode:
        builder = builder.updater(None)
    app = builder.build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("review", review))
    app.add_handler(CommandHandler("reject", reject_with_reason))
    app.add_handler(CallbackQueryHandler(callback_approve_reject))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    return app


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")

    from .core import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in .env")

    app = create_application(webhook_mode=False)
    logger.info("Grace-Mar Telegram bot starting (polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
