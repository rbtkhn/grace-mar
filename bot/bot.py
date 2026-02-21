"""
Grace-Mar Telegram Bot

A Telegram bot that responds as Grace-Mar, powered by her
cognitive fork profile data and an OpenAI LLM backend.

Usage:
    1. Copy .env.example to .env and fill in your keys
    2. pip install -r requirements.txt
    3. python bot.py
"""

import os
import logging

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, Update, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from core import (
    get_response,
    archive,
    reset_conversation,
    get_greeting,
    get_reset_message,
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    reset_conversation(key)
    greeting = get_greeting()
    archive("SESSION START", key, greeting)
    await update.message.reply_text(greeting)


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
    await update.message.reply_text(msg)


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


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")

    from core import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in .env")

    async def set_menu_button(application: Application) -> None:
        if DASHBOARD_MINIAPP_URL:
            await application.bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="Dashboard", web_app=WebAppInfo(url=DASHBOARD_MINIAPP_URL))
            )
            logger.info("Dashboard menu button configured: %s", DASHBOARD_MINIAPP_URL)

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(set_menu_button)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Grace-Mar Telegram bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
