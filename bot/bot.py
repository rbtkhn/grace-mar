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

import importlib.util
import os
import logging
import subprocess
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta

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
    start_homework_session,
    process_homework_answer,
    is_in_homework_session,
    end_homework_session,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DASHBOARD_MINIAPP_URL = os.getenv("DASHBOARD_MINIAPP_URL", "").rstrip("/")
USER_ID = os.getenv("GRACE_MAR_USER_ID", "pilot-001").strip() or "pilot-001"
OPERATOR_CHAT_ID = os.getenv("GRACE_MAR_OPERATOR_CHAT_ID", "").strip()
OPERATOR_REMINDER_ENABLED = os.getenv("GRACE_MAR_OPERATOR_REMINDERS", "1").strip().lower() not in {"0", "false", "no"}
OPERATOR_REMINDER_INTERVAL_SEC = int(os.getenv("GRACE_MAR_OPERATOR_REMINDER_INTERVAL_SEC", "21600"))
OPERATOR_PENDING_THRESHOLD = int(os.getenv("GRACE_MAR_OPERATOR_PENDING_THRESHOLD", "5"))
OPERATOR_STALE_DAYS = int(os.getenv("GRACE_MAR_OPERATOR_STALE_DAYS", "7"))


def _channel_key(chat_id: int) -> str:
    return f"telegram:{chat_id}"


def _profile_path(filename: str) -> Path:
    return Path(__file__).resolve().parent.parent / "users" / USER_ID / filename


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
        KeyboardButton("Homework"),
        KeyboardButton("Chat with me"),
    ],
]

START_KEYBOARD = ReplyKeyboardMarkup(
    START_PROMPT_OPTIONS,
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Or type anything — buttons are optional",
)

# One-tap answer buttons for homework (quick-fire, gamified)
HOMEWORK_ANSWER_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("A", callback_data="hw:A"), InlineKeyboardButton("B", callback_data="hw:B")],
    [InlineKeyboardButton("C", callback_data="hw:C"), InlineKeyboardButton("D", callback_data="hw:D")],
])


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


async def prp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the Portable Record Prompt as a downloadable .txt file."""
    try:
        repo_root = Path(__file__).resolve().parent.parent
        spec = importlib.util.spec_from_file_location(
            "export_prp",
            repo_root / "scripts" / "export_prp.py",
        )
        if not spec or not spec.loader:
            await update.message.reply_text("Could not load PRP export.")
            return
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        content = mod.export_prp(user_id=USER_ID)
        buf = BytesIO(content.encode("utf-8"))
        buf.seek(0)
        await update.message.reply_document(
            document=buf,
            filename="grace-mar-prp.txt",
            caption="Portable Record Prompt — paste into ChatGPT, Claude, or any LLM to chat with my Record.",
        )
    except Exception:
        logger.exception("PRP export error")
        await update.message.reply_text("i couldn't make the PRP right now. try again in a little bit?")


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


async def _homework_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start homework session (one question at a time). Same as tapping Homework button."""
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    try:
        first_q, err = start_homework_session(key)
        if err:
            await update.message.reply_text(err)
            return
        archive("HOMEWORK START", key, first_q or "")
        await update.message.reply_text(first_q, reply_markup=HOMEWORK_ANSWER_KEYBOARD)
    except Exception:
        logger.exception("Homework start error")
        await update.message.reply_text("um... i couldn't make homework right now. try again in a little bit?")


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


async def callback_homework_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle A/B/C/D inline button taps during homework."""
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    if not data.startswith("hw:"):
        return
    letter = data.split(":")[-1].strip().upper()
    if letter not in "ABCD":
        return
    chat_id = query.message.chat.id if query.message else None
    if not chat_id:
        return
    key = _channel_key(chat_id)
    if not is_in_homework_session(key):
        await query.edit_message_text("homework session ended — tap Homework to start again!")
        return
    try:
        response, session_ended, has_next = process_homework_answer(key, letter)
        archive("HOMEWORK ANSWER (tap)", key, letter)
        archive("GRACE-MAR (homework)", key, response)
        await query.edit_message_text(
            response,
            reply_markup=HOMEWORK_ANSWER_KEYBOARD if has_next else None,
        )
    except Exception:
        logger.exception("Homework callback error")
        await query.edit_message_text("oops! try again — tap A, B, C, or D")


async def callback_approve_reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Approve/Reject button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data
    if ":" not in data:
        return
    action, candidate_id = data.split(":", 1)
    status = "approved" if action == "approve" else "rejected"
    chat_id = query.message.chat.id if query.message else None
    actor_id = update.effective_user.id if update.effective_user else None
    channel_key = _channel_key(chat_id) if chat_id else None
    ok = update_candidate_status(
        candidate_id,
        status,
        channel_key=channel_key,
        actor=f"telegram:{actor_id}" if actor_id else None,
        source="telegram:callback",
    )
    if ok:
        emoji = "✅" if action == "approve" else "❌"
        await query.edit_message_text(f"{emoji} {candidate_id} — {status}")
    else:
        await query.edit_message_text(f"couldn't update {candidate_id}")


async def merge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tell user how to merge approved candidates."""
    candidates = get_pending_candidates()
    # Count approved (we only have pending in get_pending_candidates — approved are different)
    from pathlib import Path
    import re
    pending_path = _profile_path("PENDING-REVIEW.md")
    content = pending_path.read_text() if pending_path.exists() else ""
    approved = len(re.findall(r"status: approved", content.split("## Processed")[0]))
    if approved == 0:
        await update.message.reply_text("no approved candidates to merge. approve some with /review first!")
        return
    await update.message.reply_text(
        f"you have {approved} approved candidate(s). merge now needs a receipt.\n\n"
        "1) python3 scripts/process_approved_candidates.py --generate-receipt /tmp/receipt.json --approved-by <your_name>\n"
        "2) python3 scripts/process_approved_candidates.py --apply --approved-by <your_name> --receipt /tmp/receipt.json"
    )


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
    chat_id = update.effective_chat.id if update.effective_chat else None
    actor_id = update.effective_user.id if update.effective_user else None
    ok = update_candidate_status(
        candidate_id,
        "rejected",
        rejection_reason=reason,
        channel_key=_channel_key(chat_id) if chat_id else None,
        actor=f"telegram:{actor_id}" if actor_id else None,
        source="telegram:command",
    )
    if ok:
        msg = f"❌ {candidate_id} — rejected"
        if reason:
            msg += f" (reason: {reason})"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text(f"couldn't update {candidate_id} (not pending?)")


async def rotate_context_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rotate MEMORY/ARCHIVE context files and emit maintenance event."""
    try:
        result = subprocess.run(
            [
                "python3",
                "scripts/rotate_context.py",
                "--user",
                USER_ID,
                "--apply",
            ],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        output = (result.stdout or result.stderr or "").strip()
        if result.returncode == 0:
            await update.message.reply_text(output or "context rotation complete")
        else:
            await update.message.reply_text(f"context rotation failed: {output[:300]}")
    except Exception:
        logger.exception("Rotate context command failed")
        await update.message.reply_text("couldn't rotate context right now")


async def operator_reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Periodic operator-only reminder about stale or large review queue."""
    if not OPERATOR_CHAT_ID:
        return
    try:
        result = subprocess.run(
            [
                "python3",
                "scripts/session_brief.py",
                "--users-dir",
                "users",
                "--user",
                USER_ID,
                "--reminder",
                "--pending-threshold",
                str(OPERATOR_PENDING_THRESHOLD),
                "--stale-days",
                str(OPERATOR_STALE_DAYS),
            ],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            logger.warning("Operator reminder failed: %s", (result.stderr or "").strip())
            return
        text = (result.stdout or "").strip()
        if not text:
            return

        key = "last_operator_reminder_text"
        ts_key = "last_operator_reminder_ts"
        now = datetime.now()
        last_text = context.application.bot_data.get(key, "")
        last_ts = context.application.bot_data.get(ts_key)
        # Do not spam unchanged reminder more than once every 24h.
        if text == last_text and isinstance(last_ts, datetime) and (now - last_ts) < timedelta(hours=24):
            return

        await context.bot.send_message(chat_id=int(OPERATOR_CHAT_ID), text=text)
        context.application.bot_data[key] = text
        context.application.bot_data[ts_key] = now
    except Exception:
        logger.exception("Operator reminder job error")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    user_message = update.message.text

    # Homework flow: one question at a time, gamified
    if user_message.strip().lower() == "homework":
        try:
            first_q, err = start_homework_session(key)
            if err:
                await update.message.reply_text(err)
                return
            archive("HOMEWORK START", key, first_q or "")
            await update.message.reply_text(first_q, reply_markup=HOMEWORK_ANSWER_KEYBOARD)
        except Exception:
            logger.exception("Homework start error")
            await update.message.reply_text("um... i couldn't make homework right now. try again in a little bit?")
        return

    # In homework session: treat message as answer (or stop/quit to exit)
    if is_in_homework_session(key):
        reply_lower = user_message.strip().lower()
        if reply_lower in ("stop", "quit", "done", "exit"):
            end_homework_session(key)
            archive("HOMEWORK STOPPED", key, reply_lower)
            await update.message.reply_text("ok homework paused! tap Homework anytime to start again 🎯")
            return
        try:
            response, session_ended, has_next = process_homework_answer(key, user_message)
            archive("HOMEWORK ANSWER", key, user_message)
            archive("GRACE-MAR (homework)", key, response)
            await update.message.reply_text(
                response,
                reply_markup=HOMEWORK_ANSWER_KEYBOARD if has_next else None,
            )
        except Exception:
            logger.exception("Homework answer error")
            await update.message.reply_text("oops! tap A, B, C, or D to answer (or 'stop' to quit)")
        return

    try:
        response = get_response(key, user_message)
        await update.message.reply_text(response)
    except Exception:
        logger.exception("Error generating response")
        await update.message.reply_text("um... i got confused. can you say that again?")


async def handle_document(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle .txt document upload — handback of checkpoint or long transcript from external LLM chat."""
    from .core import analyze_activity_report, archive

    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    doc = update.message.document

    if not doc or not doc.file_name or not doc.file_name.lower().endswith(".txt"):
        await update.message.reply_text("send me a .txt file for handback (checkpoint or transcript)")
        return

    if doc.file_size and doc.file_size > 100_000:  # 100KB limit
        await update.message.reply_text("file too big — keep it under 100KB (or paste a summary instead)")
        return

    try:
        tg_file = await context.bot.get_file(doc.file_id)
        buf = await tg_file.download_as_bytearray()
        text = bytes(buf).decode("utf-8", errors="replace").strip()
    except Exception:
        logger.exception("Document download error")
        await update.message.reply_text("i couldn't read that file — try pasting the text instead")
        return

    if not text:
        await update.message.reply_text("file was empty")
        return

    # Treat as activity report: "we did a chat in external LLM, here's the content"
    synthetic = f"we did a chat in an external LLM (ChatGPT, Claude, etc). here is the checkpoint or transcript:\n\n{text}"
    archive("HANDBACK DOCUMENT", key, f"[{doc.file_name}] {text[:200]}...")
    staged = analyze_activity_report(synthetic, key)
    count = len(get_pending_candidates())
    if staged:
        await update.message.reply_text(
            f"got it! i read that and added it to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review"
        )
    else:
        await update.message.reply_text(
            "ok i read that. nothing new to add to your profile right now, but it's in the log! type /review"
        )


async def handle_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Transcribe voice message and process like text (chat, homework answer, or 'we did X' pipeline)."""
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

    # In homework: treat voice as answer (e.g. "A" or "B")
    if is_in_homework_session(key):
        reply_lower = transcript.strip().lower()
        if reply_lower in ("stop", "quit", "done", "exit"):
            end_homework_session(key)
            archive("HOMEWORK STOPPED", key, reply_lower)
            await update.message.reply_text("ok homework paused! tap Homework anytime to start again 🎯")
            return
        try:
            response, _, has_next = process_homework_answer(key, transcript)
            archive("HOMEWORK ANSWER (voice)", key, transcript)
            archive("GRACE-MAR (homework)", key, response)
            await update.message.reply_text(
                response,
                reply_markup=HOMEWORK_ANSWER_KEYBOARD if has_next else None,
            )
        except Exception:
            logger.exception("Homework answer error (voice)")
            await update.message.reply_text("tap A, B, C, or D to answer (or type 'stop' to quit)")
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
        if OPERATOR_CHAT_ID and OPERATOR_REMINDER_ENABLED and application.job_queue:
            application.job_queue.run_repeating(
                operator_reminder_job,
                interval=max(300, OPERATOR_REMINDER_INTERVAL_SEC),
                first=30,
                name="operator_reminder",
            )
            logger.info(
                "Operator reminders enabled for chat %s (interval=%ss)",
                OPERATOR_CHAT_ID,
                max(300, OPERATOR_REMINDER_INTERVAL_SEC),
            )

    builder = Application.builder().token(TELEGRAM_TOKEN).post_init(set_menu_button)
    if webhook_mode:
        builder = builder.updater(None)
    app = builder.build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prp", prp))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("homework", _homework_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("review", review))
    app.add_handler(CommandHandler("merge", merge_command))
    app.add_handler(CommandHandler("reject", reject_with_reason))
    app.add_handler(CommandHandler("rotate", rotate_context_command))
    app.add_handler(CallbackQueryHandler(callback_homework_answer, pattern=r"^hw:[ABCD]$"))
    app.add_handler(CallbackQueryHandler(callback_approve_reject))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
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
