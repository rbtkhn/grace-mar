"""
Shared emulation core for Grace-Mar.

Used by both the Telegram and WeChat bots. Handles LLM conversation,
lookup, analyst, archive, and rate limiting. Channel-agnostic — callers
pass a channel_key (e.g. "telegram:123" or "wechat:oABC123") to scope
conversations and rate limits.
"""

import json
import os
import re
import logging
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompt import (
    SYSTEM_PROMPT,
    LOOKUP_PROMPT,
    LIBRARY_LOOKUP_PROMPT,
    REPHRASE_PROMPT,
    ANALYST_PROMPT,
)

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_HISTORY = 20

PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / "pilot-001"
ARCHIVE_PATH = PROFILE_DIR / "TELEGRAM-ARCHIVE.md"
PENDING_REVIEW_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
LIBRARY_PATH = PROFILE_DIR / "LIBRARY.md"
COMPUTE_LEDGER_PATH = PROFILE_DIR / "COMPUTE-LEDGER.jsonl"
PIPELINE_EVENTS_PATH = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"

LIBRARY_MISS = "LIBRARY_MISS"

OPENAI_ANALYST_MODEL = os.getenv("OPENAI_ANALYST_MODEL", "gpt-4o-mini")

RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "3600"))
RATE_LIMIT_MAIN = int(os.getenv("RATE_LIMIT_MAIN", "60"))
RATE_LIMIT_ANALYST = int(os.getenv("RATE_LIMIT_ANALYST", "120"))

_candidate_counter_lock = threading.Lock()
_rate_limit_lock = threading.Lock()
_ledger_lock = threading.Lock()
_rate_counters: dict[tuple[str, str], list[float]] = defaultdict(list)


def _log_tokens(
    channel_key: str,
    bucket: str,
    prompt_tokens: int,
    completion_tokens: int,
    model: str,
) -> None:
    """Append token usage to compute ledger (energy ledger)."""
    try:
        usage = {
            "ts": datetime.now().isoformat(),
            "channel_key": channel_key,
            "bucket": bucket,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "model": model,
        }
        with _ledger_lock:
            with open(COMPUTE_LEDGER_PATH, "a") as f:
                f.write(json.dumps(usage) + "\n")
    except Exception:
        logger.exception("Failed to log tokens (non-fatal)")


def emit_pipeline_event(event_type: str, candidate_id: str | None = None, **kwargs: str) -> None:
    """Append a pipeline event (staged, approved, rejected, applied)."""
    try:
        event = {
            "ts": datetime.now().isoformat(),
            "event": event_type,
            "candidate_id": candidate_id,
            **kwargs,
        }
        with _ledger_lock:
            with open(PIPELINE_EVENTS_PATH, "a") as f:
                f.write(json.dumps(event) + "\n")
    except Exception:
        logger.exception("Failed to emit pipeline event (non-fatal)")

LOOKUP_TRIGGER = "do you want me to look it up"
AFFIRMATIVE_WORDS = {"yes", "yeah", "yea", "yep", "sure", "ok", "okay", "please", "ya", "y"}
AFFIRMATIVE_PHRASES = {"look it up", "go ahead", "do it", "go for it", "find out", "tell me", "look up", "yes please"}

_client: OpenAI | None = None
conversations: dict[str, list[dict]] = defaultdict(list)
pending_lookups: dict[str, str] = {}


def _check_rate_limit(channel_key: str, bucket: str, tokens: int = 1) -> bool:
    """Check and consume rate limit. Returns False if over limit."""
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    limit = RATE_LIMIT_MAIN if bucket == "main" else RATE_LIMIT_ANALYST
    key = (channel_key, bucket)
    with _rate_limit_lock:
        times = _rate_counters[key]
        times[:] = [t for t in times if t > window_start]
        if len(times) + tokens > limit:
            return False
        for _ in range(tokens):
            times.append(now)
    return True


def archive(event: str, channel_key: str, text: str) -> None:
    """Append an event to the conversation archive."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVE_PATH, "a") as f:
        f.write(f"**[{ts}]** `{event}` ({channel_key})\n")
        for line in text.strip().splitlines():
            f.write(f"> {line}\n")
        f.write("\n")


def _load_library() -> list[dict]:
    if not LIBRARY_PATH.exists():
        return []
    content = LIBRARY_PATH.read_text()
    entries = []
    for block in re.findall(r"-\s+id:\s+LIB-\d+(.*?)(?=-\s+id:\s+LIB-|\Z)", content, re.DOTALL):
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        scope_m = re.search(r"scope:\s*\[([^\]]*)\]", block)
        status_m = re.search(r"status:\s*(\w+)", block)
        if title_m and (status_m is None or status_m.group(1) == "active"):
            scope = scope_m.group(1).split(",") if scope_m else []
            scope = [s.strip() for s in scope if s.strip()]
            entries.append({"title": title_m.group(1), "scope": scope})
    return entries


def _library_summary() -> str:
    entries = _load_library()
    lines = []
    for e in entries:
        scope_str = ", ".join(e["scope"]) if e["scope"] else "general"
        lines.append(f"- {e['title']}: {scope_str}")
    return "\n".join(lines) if lines else "(no books)"


def _library_lookup(question: str, channel_key: str = "unknown") -> str | None:
    summary = _library_summary()
    if "(no books)" in summary:
        return None
    prompt = LIBRARY_LOOKUP_PROMPT.format(
        library_summary=summary,
        question=question,
    )
    result = _get_client().chat.completions.create(
        model=OPENAI_ANALYST_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=0.2,
    )
    if u := getattr(result, "usage", None):
        _log_tokens(channel_key, "library_lookup", u.prompt_tokens, u.completion_tokens, OPENAI_ANALYST_MODEL)
    reply = result.choices[0].message.content.strip()
    if LIBRARY_MISS in reply:
        return None
    return reply


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _rephrase_lookup(question: str, facts: str, channel_key: str = "unknown") -> str:
    result = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": REPHRASE_PROMPT},
            {
                "role": "user",
                "content": f"The question was: {question}\n\nThe answer is: {facts}\n\nNow explain this in your own words.",
            },
        ],
        max_tokens=200,
        temperature=0.9,
    )
    if u := getattr(result, "usage", None):
        _log_tokens(channel_key, "lookup_rephrase", u.prompt_tokens, u.completion_tokens, OPENAI_MODEL)
    return result.choices[0].message.content


def _lookup(question: str, channel_key: str = "unknown") -> str:
    client = _get_client()
    factual = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": LOOKUP_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=0.3,
    )
    if u := getattr(factual, "usage", None):
        _log_tokens(channel_key, "lookup_factual", u.prompt_tokens, u.completion_tokens, OPENAI_MODEL)
    facts = factual.choices[0].message.content
    return _rephrase_lookup(question, facts, channel_key)


def _lookup_with_library_first(question: str, channel_key: str = "unknown") -> str:
    lib_answer = _library_lookup(question, channel_key)
    if lib_answer:
        logger.info("LIBRARY: hit for %s", question[:50])
        return _rephrase_lookup(question, lib_answer, channel_key)
    logger.info("LIBRARY: miss, falling back to full lookup")
    return _lookup(question, channel_key)


def _next_candidate_id() -> str:
    with _candidate_counter_lock:
        try:
            content = PENDING_REVIEW_PATH.read_text()
            ids = [int(m) for m in re.findall(r"CANDIDATE-(\d+)", content)]
            return f"CANDIDATE-{max(ids) + 1:04d}" if ids else "CANDIDATE-0001"
        except (FileNotFoundError, ValueError):
            return "CANDIDATE-0001"


def analyze_exchange(user_message: str, assistant_message: str, channel_key: str) -> None:
    if not _check_rate_limit(channel_key, "analyst", tokens=1):
        logger.debug("Analyst rate limit exceeded (%s), skipping", channel_key)
        return
    try:
        result = _get_client().chat.completions.create(
            model=OPENAI_ANALYST_MODEL,
            messages=[
                {"role": "system", "content": ANALYST_PROMPT},
                {"role": "user", "content": f"USER: {user_message}\nGRACE-MAR: {assistant_message}"},
            ],
            max_tokens=300,
            temperature=0.2,
        )
        if u := getattr(result, "usage", None):
            _log_tokens(channel_key, "analyst", u.prompt_tokens, u.completion_tokens, OPENAI_ANALYST_MODEL)
        analysis = result.choices[0].message.content.strip()
        if analysis.upper() == "NONE":
            return
        _stage_candidate(analysis, user_message, assistant_message, channel_key)
        logger.info("ANALYST: signal detected — staged candidate")
    except Exception:
        logger.exception("Analyst error (non-fatal)")


def _stage_candidate(
    analysis_yaml: str,
    user_message: str,
    assistant_message: str,
    channel_key: str,
) -> None:
    candidate_id = _next_candidate_id()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = f"""### {candidate_id}

```yaml
status: pending
timestamp: {ts}
channel_key: {channel_key}
source_exchange:
  user: "{user_message}"
  grace_mar: "{assistant_message}"
{analysis_yaml}
```

"""
    with open(PENDING_REVIEW_PATH, "a") as f:
        f.write(block)
    emit_pipeline_event("staged", candidate_id, channel_key=channel_key)


def _run_analyst_background(
    user_message: str,
    assistant_message: str,
    channel_key: str,
) -> None:
    thread = threading.Thread(
        target=analyze_exchange,
        args=(user_message, assistant_message, channel_key),
        daemon=True,
    )
    thread.start()


def get_response(channel_key: str, user_message: str) -> str:
    """Get Grace-Mar's response for a given message. Channel-key scopes conversation."""
    history = conversations[channel_key]

    normalized = user_message.strip().lower().rstrip("!.,")
    is_affirmative = normalized in AFFIRMATIVE_WORDS or any(
        p in normalized for p in AFFIRMATIVE_PHRASES
    )

    if channel_key in pending_lookups and is_affirmative:
        question = pending_lookups.pop(channel_key)
        if not _check_rate_limit(channel_key, "main", tokens=2):
            logger.warning("Rate limit exceeded (main, %s)", channel_key)
            return "i'm a little tired right now. can we talk more in a bit?"
        logger.info("LOOKUP: %s", question)
        archive("LOOKUP REQUEST", channel_key, question)

        assistant_message = _lookup_with_library_first(question, channel_key)

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": assistant_message})

        logger.info("USER: %s", user_message)
        logger.info("GRACE-MAR (lookup): %s", assistant_message)
        archive("USER", channel_key, user_message)
        archive("GRACE-MAR (lookup)", channel_key, assistant_message)

        _run_analyst_background(user_message, assistant_message, channel_key)
        return assistant_message

    pending_lookups.pop(channel_key, None)
    history.append({"role": "user", "content": user_message})

    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    if not _check_rate_limit(channel_key, "main", tokens=1):
        logger.warning("Rate limit exceeded (main, %s)", channel_key)
        return "i'm a little tired right now. can we talk more in a bit?"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = _get_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.9,
    )
    if u := getattr(response, "usage", None):
        _log_tokens(channel_key, "main", u.prompt_tokens, u.completion_tokens, OPENAI_MODEL)

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    if LOOKUP_TRIGGER in assistant_message.lower():
        pending_lookups[channel_key] = user_message

    logger.info("USER: %s", user_message)
    logger.info("GRACE-MAR: %s", assistant_message)
    archive("USER", channel_key, user_message)
    archive("GRACE-MAR", channel_key, assistant_message)
    _run_analyst_background(user_message, assistant_message, channel_key)

    return assistant_message


def reset_conversation(channel_key: str) -> None:
    """Clear conversation history for a channel. Used by /start and /reset."""
    conversations[channel_key] = []
    pending_lookups.pop(channel_key, None)


def get_greeting() -> str:
    return "hi! i'm grace-mar! do you want to talk? i like stories and science and drawing!"


def get_reset_message() -> str:
    return "ok i forgot everything! let's start over. what do you want to talk about?"
