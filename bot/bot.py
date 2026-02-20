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
import threading
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from prompt import SYSTEM_PROMPT, LOOKUP_PROMPT, REPHRASE_PROMPT, ANALYST_PROMPT

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_HISTORY = 20

PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / "pilot-001"
ARCHIVE_PATH = PROFILE_DIR / "GRACE-MAR-BOT-ARCHIVE.md"
PENDING_REVIEW_PATH = PROFILE_DIR / "PENDING-REVIEW.md"

OPENAI_ANALYST_MODEL = os.getenv("OPENAI_ANALYST_MODEL", "gpt-4o-mini")

_candidate_counter_lock = threading.Lock()

LOOKUP_TRIGGER = "do you want me to look it up"
AFFIRMATIVE_WORDS = {"yes", "yeah", "yea", "yep", "sure", "ok", "okay", "please", "ya", "y"}
AFFIRMATIVE_PHRASES = {"look it up", "go ahead", "do it", "go for it", "find out", "tell me", "look up", "yes please"}

_client = None
conversations: dict[int, list[dict]] = defaultdict(list)
pending_lookups: dict[int, str] = {}


def archive(event: str, chat_id: int, text: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVE_PATH, "a") as f:
        f.write(f"**[{ts}]** `{event}` (chat {chat_id})\n")
        for line in text.strip().splitlines():
            f.write(f"> {line}\n")
        f.write("\n")


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def lookup(question: str) -> str:
    """Two-step process: get factual answer, then rephrase in Grace-Mar's voice."""
    client = get_client()

    factual = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": LOOKUP_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=0.3,
    )
    facts = factual.choices[0].message.content

    rephrased = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": REPHRASE_PROMPT},
            {"role": "user", "content": f"The question was: {question}\n\nThe answer is: {facts}\n\nNow explain this in your own words."},
        ],
        max_tokens=200,
        temperature=0.9,
    )
    return rephrased.choices[0].message.content


def _next_candidate_id() -> str:
    """Read PENDING-REVIEW.md to find the next CANDIDATE number."""
    import re
    with _candidate_counter_lock:
        try:
            content = PENDING_REVIEW_PATH.read_text()
            ids = [int(m) for m in re.findall(r"CANDIDATE-(\d+)", content)]
            return f"CANDIDATE-{max(ids) + 1:04d}" if ids else "CANDIDATE-0001"
        except (FileNotFoundError, ValueError):
            return "CANDIDATE-0001"


def analyze_exchange(user_message: str, assistant_message: str, chat_id: int) -> None:
    """Run the profile analyst on an exchange. Stages a candidate if a signal is found."""
    try:
        result = get_client().chat.completions.create(
            model=OPENAI_ANALYST_MODEL,
            messages=[
                {"role": "system", "content": ANALYST_PROMPT},
                {"role": "user", "content": f"USER: {user_message}\nGRACE-MAR: {assistant_message}"},
            ],
            max_tokens=300,
            temperature=0.2,
        )
        analysis = result.choices[0].message.content.strip()

        if analysis.upper() == "NONE":
            return

        stage_candidate(analysis, user_message, assistant_message, chat_id)
        logger.info("ANALYST: signal detected — staged candidate")

    except Exception:
        logger.exception("Analyst error (non-fatal)")


def stage_candidate(analysis_yaml: str, user_message: str, assistant_message: str, chat_id: int) -> None:
    """Append a candidate entry to PENDING-REVIEW.md."""
    candidate_id = _next_candidate_id()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    block = f"""### {candidate_id}

```yaml
status: pending
timestamp: {ts}
chat_id: {chat_id}
source_exchange:
  user: "{user_message}"
  grace_mar: "{assistant_message}"
{analysis_yaml}
```

"""
    with open(PENDING_REVIEW_PATH, "a") as f:
        f.write(block)


def _run_analyst_background(user_message: str, assistant_message: str, chat_id: int) -> None:
    """Fire-and-forget analyst in a background thread so it doesn't block Telegram."""
    thread = threading.Thread(
        target=analyze_exchange,
        args=(user_message, assistant_message, chat_id),
        daemon=True,
    )
    thread.start()


def get_response(chat_id: int, user_message: str) -> str:
    history = conversations[chat_id]

    normalized = user_message.strip().lower().rstrip("!.,")
    is_affirmative = normalized in AFFIRMATIVE_WORDS or any(p in normalized for p in AFFIRMATIVE_PHRASES)

    if chat_id in pending_lookups and is_affirmative:
        question = pending_lookups.pop(chat_id)
        logger.info("LOOKUP: %s", question)
        archive("LOOKUP REQUEST", chat_id, question)

        assistant_message = lookup(question)

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})

        logger.info("USER: %s", user_message)
        logger.info("GRACE-MAR (lookup): %s", assistant_message)
        archive("USER", chat_id, user_message)
        archive("GRACE-MAR (lookup)", chat_id, assistant_message)

        _run_analyst_background(user_message, assistant_message, chat_id)

        return assistant_message

    pending_lookups.pop(chat_id, None)

    history.append({"role": "user", "content": user_message})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.9,
    )

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    if LOOKUP_TRIGGER in assistant_message.lower():
        pending_lookups[chat_id] = user_message

    logger.info("USER: %s", user_message)
    logger.info("GRACE-MAR: %s", assistant_message)

    archive("USER", chat_id, user_message)
    archive("GRACE-MAR", chat_id, assistant_message)

    _run_analyst_background(user_message, assistant_message, chat_id)

    return assistant_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations[chat_id] = []
    greeting = "hi! i'm grace-mar! do you want to talk? i like stories and science and drawing!"
    archive("SESSION START", chat_id, greeting)
    await update.message.reply_text(greeting)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    conversations[chat_id] = []
    msg = "ok i forgot everything! let's start over. what do you want to talk about?"
    archive("SESSION RESET", chat_id, msg)
    await update.message.reply_text(msg)


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_message = update.message.text

    try:
        response = get_response(chat_id, user_message)
        await update.message.reply_text(response)
    except Exception:
        logger.exception("Error generating response")
        await update.message.reply_text("um... i got confused. can you say that again?")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Grace-Mar bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
