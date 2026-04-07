"""
Persistent conversation store for Grace-Mar.

SQLite-backed two-table design: raw messages + rolling summaries.
Borrowed from OpenBrain's Telegram integration pattern (Supabase),
adapted to local SQLite for grace-mar's file-based architecture.

See docs/skill-work/work-dev/persistent-chat-store-spec.md for design.
"""

import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = _REPO_ROOT / "data" / "chat_store.db"

DEFAULT_RECENT_LIMIT = 20
COMPACTION_THRESHOLD = 80
COMPACTION_MIN_AGE_HOURS = 48
COMPACTION_MAX_SUMMARY_TOKENS = 300

_db_lock = threading.Lock()

COMPACTION_PROMPT = """\
You are summarizing a conversation for continuity purposes.
The companion is a child. This summary will be loaded into the
next conversation so the Voice can pick up where it left off.

Preserve:
- Topics discussed (in order)
- Questions the companion asked
- Lookups performed and whether they were saved
- Emotional tone and energy level
- Unresolved threads or open questions
- Activities mentioned

Do not preserve:
- Identity claims about who the companion is
- Factual knowledge (this is in the Record)
- Verbatim quotes

Write an updated summary incorporating any new messages into the
existing summary context. Maximum 300 tokens. Prioritize
unresolved threads and recent topics over completed ones.\
"""

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_key TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);
CREATE INDEX IF NOT EXISTS idx_chat_channel_time
    ON chat_messages(channel_key, created_at DESC);

CREATE TABLE IF NOT EXISTS chat_summaries (
    channel_key TEXT PRIMARY KEY,
    summary TEXT NOT NULL,
    covers_through TEXT,
    updated_at TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);
"""


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create tables if they do not exist."""
    with _db_lock:
        conn = _get_conn()
        try:
            conn.executescript(_SCHEMA)
            conn.commit()
        finally:
            conn.close()


def store_message(channel_key: str, role: str, content: str) -> None:
    """Insert a single message into the store."""
    with _db_lock:
        conn = _get_conn()
        try:
            conn.execute(
                "INSERT INTO chat_messages (channel_key, role, content) VALUES (?, ?, ?)",
                (channel_key, role, content),
            )
            conn.commit()
        finally:
            conn.close()


def load_recent(channel_key: str, limit: int = DEFAULT_RECENT_LIMIT) -> list[dict]:
    """Return the last `limit` messages for a channel, oldest first."""
    with _db_lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT role, content, created_at FROM chat_messages "
                "WHERE channel_key = ? ORDER BY created_at DESC, id DESC LIMIT ?",
                (channel_key, limit),
            ).fetchall()
        finally:
            conn.close()
    rows.reverse()
    return [{"role": r["role"], "content": r["content"], "created_at": r["created_at"]} for r in rows]


def get_summary(channel_key: str) -> str | None:
    """Return the rolling summary for a channel, or None."""
    with _db_lock:
        conn = _get_conn()
        try:
            row = conn.execute(
                "SELECT summary FROM chat_summaries WHERE channel_key = ?",
                (channel_key,),
            ).fetchone()
        finally:
            conn.close()
    return row["summary"] if row else None


def search_messages(channel_key: str, query: str, limit: int = 10) -> list[dict]:
    """Case-insensitive LIKE search across messages and summaries for a channel."""
    pattern = f"%{query}%"
    results: list[dict] = []
    with _db_lock:
        conn = _get_conn()
        try:
            rows = conn.execute(
                "SELECT role, content, created_at FROM chat_messages "
                "WHERE channel_key = ? AND content LIKE ? COLLATE NOCASE "
                "ORDER BY created_at DESC LIMIT ?",
                (channel_key, pattern, limit),
            ).fetchall()
            results.extend(
                {"role": r["role"], "content": r["content"], "created_at": r["created_at"], "source": "message"}
                for r in rows
            )
            summary_row = conn.execute(
                "SELECT summary, updated_at FROM chat_summaries "
                "WHERE channel_key = ? AND summary LIKE ? COLLATE NOCASE",
                (channel_key, pattern),
            ).fetchone()
            if summary_row:
                results.append({
                    "role": "summary",
                    "content": summary_row["summary"],
                    "created_at": summary_row["updated_at"],
                    "source": "summary",
                })
        finally:
            conn.close()
    return results


def message_count(channel_key: str) -> int:
    """Total messages stored for a channel."""
    with _db_lock:
        conn = _get_conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM chat_messages WHERE channel_key = ?",
                (channel_key,),
            ).fetchone()
        finally:
            conn.close()
    return row["cnt"] if row else 0


def maybe_compact(
    channel_key: str,
    threshold: int = COMPACTION_THRESHOLD,
    min_age_hours: int = COMPACTION_MIN_AGE_HOURS,
) -> bool:
    """Lazy compaction: if enough old messages exist, summarize and delete them.

    Returns True if compaction ran.
    """
    cutoff = (datetime.now() - timedelta(hours=min_age_hours)).strftime("%Y-%m-%dT%H:%M:%S")

    with _db_lock:
        conn = _get_conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM chat_messages "
                "WHERE channel_key = ? AND created_at < ?",
                (channel_key, cutoff),
            ).fetchone()
            old_count = row["cnt"] if row else 0
        finally:
            conn.close()

    if old_count < threshold:
        return False

    with _db_lock:
        conn = _get_conn()
        try:
            old_rows = conn.execute(
                "SELECT role, content, created_at FROM chat_messages "
                "WHERE channel_key = ? AND created_at < ? ORDER BY created_at ASC",
                (channel_key, cutoff),
            ).fetchall()
            summary_row = conn.execute(
                "SELECT summary FROM chat_summaries WHERE channel_key = ?",
                (channel_key,),
            ).fetchone()
        finally:
            conn.close()

    old_messages = [{"role": r["role"], "content": r["content"], "created_at": r["created_at"]} for r in old_rows]
    existing_summary = summary_row["summary"] if summary_row else None

    new_summary = _summarize_messages(old_messages, existing_summary, channel_key)
    if not new_summary:
        logger.warning("Compaction LLM returned empty summary for %s; skipping", channel_key)
        return False

    with _db_lock:
        conn = _get_conn()
        try:
            conn.execute(
                "INSERT INTO chat_summaries (channel_key, summary, covers_through, updated_at) "
                "VALUES (?, ?, ?, strftime('%Y-%m-%dT%H:%M:%S', 'now')) "
                "ON CONFLICT(channel_key) DO UPDATE SET "
                "summary = excluded.summary, covers_through = excluded.covers_through, "
                "updated_at = excluded.updated_at",
                (channel_key, new_summary, cutoff),
            )
            conn.execute(
                "DELETE FROM chat_messages WHERE channel_key = ? AND created_at < ?",
                (channel_key, cutoff),
            )
            conn.commit()
        finally:
            conn.close()

    logger.info("Compacted %d messages for %s", len(old_messages), channel_key)
    return True


def clear_channel(channel_key: str) -> None:
    """Delete all messages and summary for a channel (used by reset)."""
    with _db_lock:
        conn = _get_conn()
        try:
            conn.execute("DELETE FROM chat_messages WHERE channel_key = ?", (channel_key,))
            conn.execute("DELETE FROM chat_summaries WHERE channel_key = ?", (channel_key,))
            conn.commit()
        finally:
            conn.close()


def _summarize_messages(
    messages: list[dict],
    existing_summary: str | None,
    channel_key: str,
) -> str | None:
    """Call GPT-4o-mini to produce a rolling summary."""
    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("openai not available for compaction")
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_ANALYST_MODEL", "gpt-4o-mini")
    if not api_key:
        logger.warning("No OPENAI_API_KEY for compaction")
        return None

    user_content_parts = []
    if existing_summary:
        user_content_parts.append(f"Existing summary:\n{existing_summary}\n")
    user_content_parts.append("New messages since last summary:\n")
    for msg in messages:
        role_label = "Companion" if msg["role"] == "user" else "Grace-Mar"
        user_content_parts.append(f"[{msg.get('created_at', '?')}] {role_label}: {msg['content']}")

    user_content = "\n".join(user_content_parts)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": COMPACTION_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=COMPACTION_MAX_SUMMARY_TOKENS,
            temperature=0.3,
        )
        result = (response.choices[0].message.content or "").strip()

        if u := getattr(response, "usage", None):
            _log_compaction_tokens(channel_key, u.prompt_tokens, u.completion_tokens, model)

        return result or None
    except Exception as e:
        logger.warning("Compaction LLM error for %s: %s", channel_key, e)
        return None


def _log_compaction_tokens(channel_key: str, prompt_tokens: int, completion_tokens: int, model: str) -> None:
    """Log compaction token usage to compute-ledger.jsonl."""
    ledger_path = _REPO_ROOT / "users" / os.getenv("GRACE_MAR_USER_ID", "grace-mar") / "compute-ledger.jsonl"
    try:
        entry = {
            "ts": datetime.now().isoformat(),
            "channel_key": channel_key,
            "bucket": "compaction",
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "model": model,
            "task_type": "compaction",
        }
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.warning("Compaction ledger write error: %s", e)


# Auto-init on import
init_db()
