"""
Shared emulation core for Grace-Mar.

Used by both the Telegram and WeChat bots. Handles LLM conversation,
lookup, analyst, archive, and rate limiting. Channel-agnostic — callers
pass a channel_key (e.g. "telegram:123" or "wechat:oABC123") to scope
conversations and rate limits.

Design principle: The integration moment is where meaning enters. The user
gates; the system stages. AI extends humanity; it does not replace it.
The Record is the boundary where interior states are written and read.
Merge, not replace: the user's documented self extends; the Voice speaks it.
"""

import base64
import json
import logging
import os
import re
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from openai import OpenAI

try:
    from .conflict_check import check_conflicts, format_conflicts_for_yaml
except ImportError:
    from conflict_check import check_conflicts, format_conflicts_for_yaml

try:
    from .retriever import retrieve as _retrieve
except ImportError:
    from retriever import retrieve as _retrieve

try:
    from .lookup_cmc import query_cmc
except ImportError:
    query_cmc = None

try:
    from .prompt import (
        SYSTEM_PROMPT,
        LOOKUP_PROMPT,
        LIBRARY_LOOKUP_PROMPT,
        REPHRASE_PROMPT,
        ANALYST_PROMPT,
        HOMEWORK_PROMPT,
    )
except ImportError:
    from prompt import (
        SYSTEM_PROMPT,
        LOOKUP_PROMPT,
        LIBRARY_LOOKUP_PROMPT,
        REPHRASE_PROMPT,
        ANALYST_PROMPT,
        HOMEWORK_PROMPT,
    )

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_HISTORY = 20

USER_ID = os.getenv("GRACE_MAR_USER_ID", "pilot-001").strip() or "pilot-001"
PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / USER_ID
ARCHIVE_PATH = PROFILE_DIR / "VOICE-ARCHIVE.md"
ARCHIVE_REPO_PATH = f"users/{USER_ID}/VOICE-ARCHIVE.md"  # repo-relative for GitHub API
# Real-time conversation log (operator continuity). Gated content goes to VOICE-ARCHIVE only on merge.
SESSION_TRANSCRIPT_PATH = PROFILE_DIR / "SESSION-TRANSCRIPT.md"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GRACE_MAR_REPO = os.getenv("GRACE_MAR_REPO", "rbtkhn/grace-mar").strip()
PENDING_REVIEW_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
MEMORY_PATH = PROFILE_DIR / "MEMORY.md"
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


def emit_pipeline_event(event_type: str, candidate_id: str | None = None, **kwargs: object) -> None:
    """Append a pipeline event (staged, approved, rejected, applied, etc.)."""
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

# "We did X" — activity report from operator. Triggers pipeline staging.
WE_DID_PATTERN = re.compile(
    r"^we\s+(drew|wrote|made|learned|read|painted|built|created|did|watched|played)\b",
    re.IGNORECASE,
)

# Bare "checkpoint" in conversation — companion requests checkpoint save; stage to pipeline and archive.
CHECKPOINT_REQUEST_PATTERN = re.compile(r"^checkpoint\s*[!?.,]*$", re.IGNORECASE)

# Transcript sent to pipeline for checkpoint: last N exchanges, or max chars (abridged).
MAX_CHECKPOINT_EXCHANGES = 25
MAX_CHECKPOINT_TRANSCRIPT_CHARS = 5000

# Pasted checkpoint from external LLM (ChatGPT, PRP, etc.) — route to pipeline.
CHECKPOINT_MARKERS = re.compile(
    r"(?i)(checkpoint\s*[–:-]|abby\s+checkpoint|here[\'s]?\s*(is|my)\s+checkpoint|"
    r"summary\s+of\s+what\s+we|topics\s+covered|checkpoint\s+saved)"
)

_client: OpenAI | None = None
conversations: dict[str, list[dict]] = defaultdict(list)
pending_lookups: dict[str, str] = {}


def _format_checkpoint_transcript(history: list[dict]) -> str:
    """Format conversation history as USER/GRACE-MAR transcript. Returns abridged if over limit."""
    lines: list[str] = []
    user_count = 0
    for msg in history:
        role = (msg.get("role") or "").strip().lower()
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            lines.append(f"USER: {content}")
            user_count += 1
        elif role == "assistant":
            lines.append(f"GRACE-MAR: {content}")
    if not lines:
        return ""
    # Keep last MAX_CHECKPOINT_EXCHANGES exchanges; then truncate by chars.
    if user_count > MAX_CHECKPOINT_EXCHANGES:
        trimmed: list[str] = []
        count = 0
        for i in range(len(lines) - 1, -1, -1):
            trimmed.append(lines[i])
            if lines[i].startswith("USER:"):
                count += 1
                if count >= MAX_CHECKPOINT_EXCHANGES:
                    break
        lines = list(reversed(trimmed))
    transcript = "\n\n".join(lines)
    if len(transcript) > MAX_CHECKPOINT_TRANSCRIPT_CHARS:
        transcript = transcript[-MAX_CHECKPOINT_TRANSCRIPT_CHARS:].strip()
        # Start at a message boundary
        first_br = transcript.find("\n\n")
        if first_br > 0:
            transcript = transcript[first_br:].strip()
        transcript = "(abridged — most recent only)\n\n" + transcript
    return transcript


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


def _channel_label(channel_key: str) -> str:
    """Human-readable channel for archive (Telegram, Test, WeChat, Mini App)."""
    k = (channel_key or "").strip().lower()
    if k.startswith("telegram:") or k.startswith("chat "):
        return "Telegram"
    if k.startswith("test:"):
        return "Test"
    if k.startswith("wechat:"):
        return "WeChat"
    if k.startswith("miniapp:") or k.startswith("miniapp_"):
        return "Mini App"
    return channel_key or "Unknown"


def _format_archive_block(event: str, channel_key: str, text: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = _channel_label(channel_key)
    lines = [f"**[{ts}]** `{event}` ({label})\n"]
    for line in (text or "").strip().splitlines():
        lines.append(f"> {line}\n")
    lines.append("\n")
    return "".join(lines)


def _append_via_github_api(block: str) -> None:
    if not GITHUB_TOKEN or not GRACE_MAR_REPO:
        return
    try:
        owner, repo = GRACE_MAR_REPO.split("/", 1)
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{ARCHIVE_REPO_PATH}"
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
        header = "# VOICE-ARCHIVE\n\n> Append-only log of all Grace-Mar interactions (Telegram, WeChat, Mini App today; eventually email, X, and other platform channels). One mind, multiple channels.\n\n---\n\n"
        base = content if content else header
        new_content = base.rstrip() + "\n\n" + block.strip() + "\n"
        payload = {"message": "bot: archive exchange", "content": base64.b64encode(new_content.encode()).decode()}
        if sha:
            payload["sha"] = sha
        put_req = Request(url, data=json.dumps(payload).encode(), method="PUT")
        put_req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
        put_req.add_header("Accept", "application/vnd.github+json")
        put_req.add_header("Content-Type", "application/json")
        urlopen(put_req)
    except HTTPError as e:
        logger.warning("Archive GitHub API error: %s %s", e.code, e.reason)
    except Exception as e:
        logger.warning("Archive error: %s", e)


def archive(event: str, channel_key: str, text: str) -> None:
    """Append an event to the session transcript (raw log for operator continuity). VOICE-ARCHIVE is written only when candidates are merged."""
    block = _format_archive_block(event, channel_key, text)
    try:
        SESSION_TRANSCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not SESSION_TRANSCRIPT_PATH.exists():
            header = (
                "# SESSION TRANSCRIPT\n\n"
                "> Raw conversation log for operator continuity. Not part of the Record. "
                "Approved content is written to VOICE-ARCHIVE on merge.\n\n---\n\n"
            )
            SESSION_TRANSCRIPT_PATH.write_text(header, encoding="utf-8")
        with open(SESSION_TRANSCRIPT_PATH, "a", encoding="utf-8") as f:
            f.write(block)
    except Exception as e:
        logger.warning("Session transcript write error: %s", e)


def _load_library() -> list[dict]:
    if not LIBRARY_PATH.exists():
        return []
    content = LIBRARY_PATH.read_text()
    entries = []
    for block in re.findall(r"-\s+id:\s+LIB-\d+(.*?)(?=-\s+id:\s+LIB-|\Z)", content, re.DOTALL):
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        scope_m = re.search(r"scope:\s*\[([^\]]*)\]", block)
        status_m = re.search(r"status:\s*(\w+)", block)
        volume_m = re.search(r'volume:\s*["\']([^"\']+)["\']', block)
        if title_m and (status_m is None or status_m.group(1) == "active"):
            scope = scope_m.group(1).split(",") if scope_m else []
            scope = [s.strip() for s in scope if s.strip()]
            volume = volume_m.group(1) if volume_m else None
            entries.append({"title": title_m.group(1), "scope": scope, "volume": volume})
    return entries


def _load_memory_appendix() -> str:
    """Load MEMORY.md if present. Returns appendix for system prompt, or empty string."""
    if not MEMORY_PATH.exists():
        return ""
    content = MEMORY_PATH.read_text(encoding="utf-8").strip()
    if not content:
        return ""
    lines = content.splitlines()
    # Skip placeholders; require at least one line of real content
    useful = []
    for line in lines:
        s = line.strip()
        if not s or "(optional" in s.lower() or s.startswith("> ") or s.startswith("Last rotated:"):
            continue
        useful.append(line)
    # Must have content beyond headers
    has_content = any(not s.startswith("#") for s in [l.strip() for l in useful])
    if not has_content:
        return ""
    block = "\n".join(useful)
    # When Resistance Notes section has content beyond placeholder, prime Voice to honor it
    resistance_hint = ""
    if "## Resistance Notes" in block or "## resistance notes" in block.lower():
        resistance_hint = " If Resistance Notes list topics: do not bring them up unprompted. If the user raises them, meet them where they are—change topic or offer alternatives if they seem resistant. Do not push."
    return """

## SESSION CONTEXT (ephemeral — SELF is authoritative)

The following is ephemeral session context. Use it to refine tone and continuity. If it conflicts with SELF, follow SELF. Do not cite factual content from this section.
""" + resistance_hint + """

""" + block


SELF_PATH = PROFILE_DIR / "SELF.md"
EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"


def _load_recency_context() -> str:
    """Load recent Record content for homework generation: IX-A (knowledge), IX-B (curiosity), recent EVIDENCE entries."""
    parts: list[str] = []

    if SELF_PATH.exists():
        content = SELF_PATH.read_text(encoding="utf-8")
        # Extract IX-A block (knowledge)
        ix_a = re.search(r"### IX-A\. KNOWLEDGE.*?```yaml\n(.*?)```", content, re.DOTALL)
        if ix_a:
            entries = ix_a.group(1).strip()
            # Take last ~12 entries (most recent) — entries start with "  - id:"
            lines = entries.split("\n")
            blocks: list[str] = []
            current: list[str] = []
            for line in lines:
                if re.match(r"\s+-\s+id:\s+", line):
                    if current:
                        blocks.append("\n".join(current))
                    current = [line]
                elif current:
                    current.append(line)
            if current:
                blocks.append("\n".join(current))
            recent_k = blocks[-12:] if len(blocks) > 12 else blocks
            parts.append("### Recent knowledge (IX-A)\n```yaml\n" + "\n".join(recent_k) + "\n```")

        # Extract IX-B block (curiosity)
        ix_b = re.search(r"### IX-B\. CURIOSITY.*?```yaml\n(.*?)```", content, re.DOTALL)
        if ix_b:
            entries = ix_b.group(1).strip()
            lines = entries.split("\n")
            blocks = []
            current = []
            for line in lines:
                if re.match(r"\s+-\s+id:\s+", line):
                    if current:
                        blocks.append("\n".join(current))
                    current = [line]
                elif current:
                    current.append(line)
            if current:
                blocks.append("\n".join(current))
            recent_c = blocks[-6:] if len(blocks) > 6 else blocks
            parts.append("\n### Recent curiosity (IX-B)\n```yaml\n" + "\n".join(recent_c) + "\n```")

    if EVIDENCE_PATH.exists():
        content = EVIDENCE_PATH.read_text(encoding="utf-8")
        # Extract WRITE, ACT, CREATE entries — take highest id numbers (most recent)
        id_matches = list(re.finditer(r"id:\s+(WRITE|ACT|CREATE)-(\d+)", content, re.IGNORECASE))
        if id_matches:
            # Get unique entry ids and sort by number descending
            seen: set[str] = set()
            entries_with_pos: list[tuple[int, str, int]] = []
            for m in id_matches:
                full_id = f"{m.group(1).upper()}-{m.group(2)}"
                if full_id in seen:
                    continue
                seen.add(full_id)
                num = int(m.group(2))
                entries_with_pos.append((m.start(), full_id, num))
            entries_with_pos.sort(key=lambda x: -x[2])  # most recent first
            recent_ids = [e[1] for e in entries_with_pos[:8]]
            # Extract first 400 chars around each recent entry
            excerpt_lines: list[str] = []
            for eid in recent_ids:
                pat = rf"id:\s+{re.escape(eid)}\s*\n(.*?)(?=\n\s+-\s+id:|\n## |\Z)"
                mat = re.search(pat, content, re.DOTALL)
                if mat:
                    block = mat.group(0)[:400].strip()
                    excerpt_lines.append(block + "\n")
            if excerpt_lines:
                parts.append("\n### Recent activities (EVIDENCE)\n" + "\n".join(excerpt_lines[:5]))

    result = "\n".join(parts).strip()
    return result[:3500] if len(result) > 3500 else result


# Homework session state: one question at a time, gamified, 30 total = competency milestone
homework_sessions: dict[str, dict] = {}
HOMEWORK_LEDGER_PATH = PROFILE_DIR / "HOMEWORK-LEDGER.jsonl"
HOMEWORK_MILESTONE = 30  # 30 correct = high competency (relative to age)
HOMEWORK_BATCH_SIZE = 8  # questions per session
HOMEWORK_SESSION_TIMEOUT_SEC = max(60, int(os.getenv("HOMEWORK_SESSION_TIMEOUT_SEC", "1800")))
_homework_timeout_notices: dict[str, bool] = {}


def _parse_homework_json(text: str) -> list[dict]:
    """Extract JSON array from LLM output (may have markdown or trailing text)."""
    text = (text or "").strip()
    # Remove markdown code fences
    if "```" in text:
        for m in re.finditer(r"```(?:json)?\s*([\s\S]*?)```", text):
            try:
                arr = json.loads(m.group(1).strip())
                if isinstance(arr, list) and arr:
                    return arr
            except json.JSONDecodeError:
                pass
    # Find [ ... ] array
    start = text.find("[")
    if start >= 0:
        depth = 0
        for i, c in enumerate(text[start:], start):
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        pass
                    break
    return []


def _get_homework_total_correct() -> int:
    """Total correct answers across all sessions (for 30 milestone)."""
    if not HOMEWORK_LEDGER_PATH.exists():
        return 0
    total = 0
    try:
        for line in HOMEWORK_LEDGER_PATH.read_text().strip().splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            total += int(obj.get("correct", 0))
    except Exception:
        pass
    return total


def _append_homework_session(correct: int, total: int, channel_key: str) -> None:
    """Append session result to ledger."""
    try:
        HOMEWORK_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(HOMEWORK_LEDGER_PATH, "a") as f:
            f.write(json.dumps({
                "ts": datetime.now().isoformat(),
                "channel_key": channel_key,
                "correct": correct,
                "total": total,
            }) + "\n")
    except Exception:
        logger.exception("Homework ledger append error")


def _expire_homework_session_if_stale(channel_key: str) -> bool:
    """Expire stale homework session for a channel. Returns True if expired."""
    session = homework_sessions.get(channel_key)
    if not session:
        return False
    last_active_raw = session.get("last_active_at")
    if not isinstance(last_active_raw, (int, float)):
        return False
    if (time.time() - float(last_active_raw)) <= HOMEWORK_SESSION_TIMEOUT_SEC:
        return False
    end_homework_session(channel_key)
    _homework_timeout_notices[channel_key] = True
    return True


def is_in_homework_session(channel_key: str) -> bool:
    _expire_homework_session_if_stale(channel_key)
    return channel_key in homework_sessions


def consume_homework_timeout_notice(channel_key: str) -> bool:
    """Return and clear timeout notice for UI messaging."""
    return _homework_timeout_notices.pop(channel_key, False)


def end_homework_session(channel_key: str) -> None:
    homework_sessions.pop(channel_key, None)


def start_homework_session(channel_key: str) -> tuple[str | None, str | None]:
    """Start a homework session. Returns (first_question_msg, error_msg). error_msg set on failure."""
    if not _check_rate_limit(channel_key, "main", tokens=2):
        return None, "i'm a little tired right now. can we do homework later?"
    recency = _load_recency_context()
    if not recency.strip():
        return None, "i don't have enough in my record yet to make homework! let's chat and learn some stuff first."
    prompt = HOMEWORK_PROMPT.format(recency_context=recency)
    try:
        result = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Generate the 8 questions as JSON now."},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        if u := getattr(result, "usage", None):
            _log_tokens(channel_key, "main", u.prompt_tokens, u.completion_tokens, OPENAI_MODEL)
        raw = (result.choices[0].message.content or "").strip()
        questions = _parse_homework_json(raw)
        if not questions:
            logger.warning("Homework: no valid questions parsed from %s", raw[:200])
            return None, "um... i couldn't make the questions. try again?"
        # Normalize: ensure options have A) B) C) D) and correct is A/B/C/D
        normalized = []
        for q in questions[:HOMEWORK_BATCH_SIZE]:
            opts = q.get("options") or []
            correct_raw = str(q.get("correct", "A")).upper()
            if len(opts) < 2:
                continue
            letters = "ABCD"[: len(opts)]
            # Format options as "A) text", "B) text", ...
            opts_fmt = []
            for j, o in enumerate(opts):
                text = o.strip()
                if not re.match(r"^[A-D]\)", text, re.IGNORECASE):
                    text = re.sub(r"^[A-Da-d0-9]\)\s*", "", text)
                opts_fmt.append(f"{letters[j]}) {text}")
            # Map correct: if LLM said "A", our first option is A
            correct_letter = correct_raw if correct_raw in letters else letters[0]
            hint = (q.get("hint") or "").strip()
            normalized.append({"q": (q.get("q") or "?").strip(), "options": opts_fmt, "correct": correct_letter, "hint": hint})
        if not normalized:
            return None, "um... i couldn't make the questions. try again?"
        total_correct_ever = _get_homework_total_correct()
        homework_sessions[channel_key] = {
            "questions": normalized,
            "idx": 0,
            "correct_in_session": 0,
            "streak": 0,
            "last_active_at": time.time(),
        }
        q0 = normalized[0]
        msg = f"homework time! 🎯 one at a time — tap A, B, C, or D!\n\n"
        if total_correct_ever >= HOMEWORK_MILESTONE:
            msg += f"you've got {total_correct_ever} right total — you're a champ! 🏆\n\n"
        elif total_correct_ever > 0:
            msg += f"({total_correct_ever} right so far — {HOMEWORK_MILESTONE} = champ! 🏆)\n\n"
        msg += f"Question 1 of {len(normalized)}!\n\n{q0['q']}\n\n" + "\n".join(q0["options"])
        return msg, None
    except Exception:
        logger.exception("Homework generation error")
        return None, "um... i couldn't make homework right now. try again in a little bit?"


def process_homework_answer(channel_key: str, user_reply: str) -> tuple[str, bool, bool]:
    """Process answer. Returns (response_message, session_ended, has_next_question).
    When has_next_question, bot should show A B C D inline buttons."""
    session = homework_sessions.get(channel_key)
    if not session:
        return "", True, False
    session["last_active_at"] = time.time()
    idx = session["idx"]
    questions = session["questions"]
    if idx >= len(questions):
        end_homework_session(channel_key)
        return "", True
    q = questions[idx]
    correct_letter = q["correct"]
    # Parse: "A", "a", "1" (first), "B", "b", "2", etc.
    reply = user_reply.strip().upper()[:1]
    if reply.isdigit():
        num = int(reply)
        if 1 <= num <= 4:
            reply = "ABCD"[num - 1]
    if not reply or reply not in "ABCD":
        return "tap A, B, C, or D to answer! (or type 'stop' to quit)", False, True
    is_correct = reply == correct_letter
    if is_correct:
        session["correct_in_session"] += 1
        session["streak"] += 1
        streak = session["streak"]
        if streak >= 3:
            feedback = "yes! 🔥 " + str(streak) + " in a row!"
        elif streak >= 2:
            feedback = "yes! 2 in a row! 🌟"
        else:
            feedback = "yes! 🎉"
    else:
        session["streak"] = 0
        correct_opt = next(o for o in q["options"] if o.upper().startswith(correct_letter))
        correct_text = correct_opt.split(")", 1)[1].strip()
        hint = q.get("hint") or ""
        if hint:
            feedback = f"here's a hint: {hint}\n\nnot quite — it's {correct_letter}) {correct_text}"
        else:
            feedback = f"not quite — it's {correct_letter}) {correct_text}"
    session["idx"] += 1
    if session["idx"] >= len(questions):
        # Session done
        correct_in = session["correct_in_session"]
        total_in = len(questions)
        _append_homework_session(correct_in, total_in, channel_key)
        total_ever = _get_homework_total_correct()
        end_homework_session(channel_key)
        msg = feedback + f"\n\nall done! {correct_in}/{total_in} right!"
        if total_ever >= HOMEWORK_MILESTONE:
            msg += f" you've got {total_ever} total — champ! 🏆"
        elif total_ever > 0:
            msg += f" ({total_ever} total — {HOMEWORK_MILESTONE} = champ! 🏆)"
        msg += "\n\nwant more? tap Homework again!"
        return msg, True, False
    # Next question
    nq = questions[session["idx"]]
    n = session["idx"] + 1
    total = len(questions)
    return feedback + f"\n\nQuestion {n} of {total}!\n\n{nq['q']}\n\n" + "\n".join(nq["options"]), False, True


def _library_summary() -> str:
    entries = _load_library()
    lines = []
    for e in entries:
        scope_str = ", ".join(e["scope"]) if e["scope"] else "general"
        label = f"{e['title']} (in {e['volume']})" if e.get("volume") else e["title"]
        lines.append(f"- {label}: {scope_str}")
    return "\n".join(lines) if lines else "(no sources)"


def _library_lookup(question: str, channel_key: str = "unknown") -> str | None:
    summary = _library_summary()
    if "(no sources)" in summary:
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
    logger.info("LIBRARY: miss, trying CMC")
    if query_cmc:
        cmc_text = query_cmc(question, limit=5)
        if cmc_text:
            logger.info("CMC: hit for %s", question[:50])
            return _rephrase_lookup(question, cmc_text, channel_key)
    logger.info("CMC: miss, falling back to full lookup")
    return _lookup(question, channel_key)


def _next_candidate_id() -> str:
    with _candidate_counter_lock:
        try:
            content = PENDING_REVIEW_PATH.read_text()
            ids = [int(m) for m in re.findall(r"CANDIDATE-(\d+)", content)]
            return f"CANDIDATE-{max(ids) + 1:04d}" if ids else "CANDIDATE-0001"
        except (FileNotFoundError, ValueError):
            return "CANDIDATE-0001"


ALLOWED_MIND_CATEGORIES = {"knowledge", "curiosity", "personality"}
REQUIRED_ANALYST_FIELDS = {
    "mind_category",
    "signal_type",
    "summary",
    "profile_target",
    "suggested_entry",
    "prompt_section",
    "prompt_addition",
}


def _parse_top_level_yaml(analysis_yaml: str) -> dict[str, str]:
    """Parse simple top-level analyst YAML fields (key: value)."""
    parsed: dict[str, str] = {}
    for line in (analysis_yaml or "").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # We only allow flat top-level keys for analyst payloads.
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        k = key.strip()
        if not k:
            continue
        v = value.strip().strip('"').strip("'")
        parsed[k] = v
    return parsed


def _validate_analysis_yaml(analysis_yaml: str) -> tuple[bool, str]:
    """Validate analyst output schema before staging."""
    parsed = _parse_top_level_yaml(analysis_yaml)
    missing = [f for f in REQUIRED_ANALYST_FIELDS if not parsed.get(f)]
    if missing:
        return False, f"missing fields: {', '.join(sorted(missing))}"
    mind_category = (parsed.get("mind_category") or "").strip().lower()
    if mind_category not in ALLOWED_MIND_CATEGORIES:
        return False, f"invalid mind_category: {mind_category}"
    priority = (parsed.get("priority_score") or "").strip()
    if priority:
        if not priority.isdigit() or not (1 <= int(priority) <= 5):
            return False, f"invalid priority_score: {priority}"
    return True, ""


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
        staged = _stage_candidate(analysis, user_message, assistant_message, channel_key)
        if staged:
            logger.info("ANALYST: signal detected — staged candidate")
        else:
            logger.warning("ANALYST: signal detected but candidate failed schema validation")
    except Exception:
        logger.exception("Analyst error (non-fatal)")


def _stage_candidate(
    analysis_yaml: str,
    user_message: str,
    assistant_message: str,
    channel_key: str,
) -> bool:
    valid, reason = _validate_analysis_yaml(analysis_yaml)
    if not valid:
        logger.warning("ANALYST: invalid candidate payload (%s)", reason)
        emit_pipeline_event(
            "invalid_candidate",
            None,
            channel_key=channel_key,
            reason=reason,
        )
        return False
    candidate_id = _next_candidate_id()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conflicts = check_conflicts(analysis_yaml)
    conflicts_block = format_conflicts_for_yaml(conflicts) if conflicts else ""
    if conflicts:
        logger.info("CONFLICT: %d contradiction(s) flagged for %s", len(conflicts), candidate_id)
    block = f"""### {candidate_id}

```yaml
status: pending
timestamp: {ts}
channel_key: {channel_key}
source_exchange:
  user: "{user_message}"
  grace_mar: "{assistant_message}"
{analysis_yaml}{conflicts_block}
```

"""
    with open(PENDING_REVIEW_PATH, "a") as f:
        f.write(block)
    emit_pipeline_event("staged", candidate_id, channel_key=channel_key)
    return True


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


ACTIVITY_REPORT_SYNTHETIC = "[Activity reported by operator. No bot response. Treat as direct evidence of real-world activity. Extract knowledge, curiosity, or personality signals.]"


def analyze_activity_report(user_message: str, channel_key: str) -> bool:
    """Run analyst on 'we did X' activity report. Returns True if staged."""
    if not _check_rate_limit(channel_key, "analyst", tokens=1):
        return False
    synthetic = f"USER: {user_message}\nGRACE-MAR: {ACTIVITY_REPORT_SYNTHETIC}"
    try:
        result = _get_client().chat.completions.create(
            model=OPENAI_ANALYST_MODEL,
            messages=[
                {"role": "system", "content": ANALYST_PROMPT},
                {"role": "user", "content": synthetic},
            ],
            max_tokens=300,
            temperature=0.2,
        )
        if u := getattr(result, "usage", None):
            _log_tokens(channel_key, "analyst", u.prompt_tokens, u.completion_tokens, OPENAI_ANALYST_MODEL)
        analysis = result.choices[0].message.content.strip()
        if analysis.upper() == "NONE":
            return False
        staged = _stage_candidate(analysis, user_message, ACTIVITY_REPORT_SYNTHETIC, channel_key)
        if staged:
            logger.info("ANALYST: activity report staged")
        return staged
    except Exception:
        logger.exception("Analyst error on activity report (non-fatal)")
        return False


def get_pending_candidates() -> list[dict]:
    """Parse PENDING-REVIEW.md and return list of pending candidates (id, summary)."""
    if not PENDING_REVIEW_PATH.exists():
        return []
    content = PENDING_REVIEW_PATH.read_text()
    candidates: list[dict] = []
    for m in re.finditer(r"### (CANDIDATE-\d+)(?:\s*\([^)]*\))?\s*\n```yaml\n(.*?)```", content, re.DOTALL):
        block = m.group(2)
        if "status: pending" not in block:
            continue
        summary_m = re.search(r"summary:\s*(.+?)(?:\n|$)", block)
        summary = summary_m.group(1).strip().strip('"') if summary_m else "(no summary)"
        candidates.append({"id": m.group(1), "summary": summary[:100]})
    return candidates


def get_pipeline_health_summary(channel_key: str | None = None) -> dict[str, object]:
    """Return lightweight pipeline/rate snapshot for operator status surfaces."""
    pending = get_pending_candidates()
    pending_ids = {c["id"] for c in pending}
    oldest_pending_days: int | None = None
    last_event_ts = ""
    rejection_reasons: list[str] = []

    if PIPELINE_EVENTS_PATH.exists():
        lines = PIPELINE_EVENTS_PATH.read_text(encoding="utf-8").splitlines()
        events: list[dict] = []
        for line in lines[-500:]:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                if isinstance(row, dict):
                    events.append(row)
            except json.JSONDecodeError:
                continue
        if events:
            last_event_ts = str(events[-1].get("ts") or "")
        staged_times: list[datetime] = []
        for row in events:
            if row.get("event") == "staged" and row.get("candidate_id") in pending_ids:
                ts = str(row.get("ts") or "").strip()
                if not ts:
                    continue
                try:
                    staged_times.append(datetime.fromisoformat(ts))
                except ValueError:
                    continue
        if staged_times:
            oldest = min(staged_times)
            oldest_pending_days = max(0, (datetime.now() - oldest).days)
        for row in reversed(events):
            if row.get("event") != "rejected":
                continue
            reason = str(row.get("rejection_reason") or "").strip()
            if reason:
                rejection_reasons.append(reason)
            if len(rejection_reasons) >= 3:
                break

    archive_last_modified = ""
    if SESSION_TRANSCRIPT_PATH.exists():
        archive_last_modified = datetime.fromtimestamp(SESSION_TRANSCRIPT_PATH.stat().st_mtime).isoformat()

    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    main_used = 0
    analyst_used = 0
    with _rate_limit_lock:
        for (key, bucket), timestamps in _rate_counters.items():
            active = [t for t in timestamps if t > window_start]
            if channel_key and key != channel_key:
                continue
            if bucket == "main":
                main_used += len(active)
            elif bucket == "analyst":
                analyst_used += len(active)

    return {
        "pending_count": len(pending),
        "oldest_pending_days": oldest_pending_days,
        "last_event_ts": last_event_ts or None,
        "recent_rejection_reasons": rejection_reasons,
        "archive_last_modified": archive_last_modified or None,
        "main_used": main_used,
        "main_limit": RATE_LIMIT_MAIN,
        "analyst_used": analyst_used,
        "analyst_limit": RATE_LIMIT_ANALYST,
        "rate_limit_window_sec": RATE_LIMIT_WINDOW,
    }


def get_intent_audit_summary(window_days: int = 30) -> dict[str, object]:
    """
    Return advisory intent-alignment summary from pipeline events.
    Focuses on cross-agent intent conflicts and rejection signals.
    """
    cutoff_ts = time.time() - max(1, window_days) * 86400
    conflict_by_source: dict[str, int] = defaultdict(int)
    conflict_by_rule: dict[str, int] = defaultdict(int)
    strategy_counts: dict[str, int] = defaultdict(int)
    rejection_categories: dict[str, int] = defaultdict(int)
    total_conflicts = 0
    total_rejections = 0
    recent_conflicts: list[dict] = []

    if not PIPELINE_EVENTS_PATH.exists():
        return {
            "window_days": window_days,
            "total_conflicts": 0,
            "total_rejections": 0,
            "conflicts_by_source": {},
            "conflicts_by_rule": {},
            "conflict_strategies": {},
            "rejection_categories": {},
            "recent_conflicts": [],
        }

    lines = PIPELINE_EVENTS_PATH.read_text(encoding="utf-8").splitlines()
    for line in lines[-2000:]:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        raw_ts = str(row.get("ts") or "").strip()
        if raw_ts:
            try:
                dt = datetime.fromisoformat(raw_ts)
                if dt.timestamp() < cutoff_ts:
                    continue
            except ValueError:
                pass
        event_name = str(row.get("event") or "").strip()
        if event_name == "intent_conflict_cross_agent":
            source = str(row.get("candidate_source") or "unknown").strip() or "unknown"
            rule_id = str(row.get("rule_id") or "UNKNOWN").strip() or "UNKNOWN"
            strategy = str(row.get("conflict_strategy") or "escalate_to_human").strip() or "escalate_to_human"
            total_conflicts += 1
            conflict_by_source[source] += 1
            conflict_by_rule[rule_id] += 1
            strategy_counts[strategy] += 1
            if len(recent_conflicts) < 5:
                recent_conflicts.append(
                    {
                        "ts": raw_ts,
                        "candidate_id": row.get("candidate_id"),
                        "source": source,
                        "rule_id": rule_id,
                        "reason": str(row.get("reason") or "").strip(),
                    }
                )
        elif event_name == "rejected":
            total_rejections += 1
            reason = str(row.get("rejection_reason") or "").strip().lower()
            if "value_misalignment" in reason:
                rejection_categories["value_misalignment"] += 1
            elif "wrong_tradeoff" in reason:
                rejection_categories["wrong_tradeoff"] += 1
            elif reason:
                rejection_categories["other"] += 1

    return {
        "window_days": window_days,
        "total_conflicts": total_conflicts,
        "total_rejections": total_rejections,
        "conflicts_by_source": dict(sorted(conflict_by_source.items(), key=lambda kv: (-kv[1], kv[0]))),
        "conflicts_by_rule": dict(sorted(conflict_by_rule.items(), key=lambda kv: (-kv[1], kv[0]))),
        "conflict_strategies": dict(sorted(strategy_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "rejection_categories": dict(sorted(rejection_categories.items(), key=lambda kv: (-kv[1], kv[0]))),
        "recent_conflicts": recent_conflicts,
    }


def get_intent_review_summary(window_days: int = 30) -> dict[str, object]:
    """
    Operator-facing intent review summary with lightweight rule-update suggestions.
    Advisory only; does not modify canonical files.
    """
    summary = get_intent_audit_summary(window_days=window_days)
    conflicts_by_rule = summary.get("conflicts_by_rule") or {}
    conflicts_by_source = summary.get("conflicts_by_source") or {}
    rejection_categories = summary.get("rejection_categories") or {}
    suggested_updates: list[dict[str, object]] = []

    for rule_id, count in list(conflicts_by_rule.items())[:5]:
        if int(count) < 2:
            continue
        dominant_source = "unknown"
        if conflicts_by_source:
            dominant_source = max(conflicts_by_source.items(), key=lambda kv: kv[1])[0]
        suggestion = {
            "rule_id": str(rule_id),
            "conflict_count": int(count),
            "dominant_source": dominant_source,
            "suggestion": (
                f"review applies_to or prioritize/deprioritize wording for {rule_id}; "
                f"repeated conflicts detected from {dominant_source}"
            ),
        }
        suggested_updates.append(suggestion)

    if rejection_categories.get("wrong_tradeoff", 0) >= 2:
        suggested_updates.append(
            {
                "rule_id": "MULTI",
                "conflict_count": int(rejection_categories.get("wrong_tradeoff", 0)),
                "dominant_source": "review_feedback",
                "suggestion": "consider adding or tightening conflict_strategy on relevant INTENT rules",
            }
        )

    return {
        **summary,
        "suggested_updates": suggested_updates,
    }


def _next_debate_id() -> str:
    content = PENDING_REVIEW_PATH.read_text(encoding="utf-8") if PENDING_REVIEW_PATH.exists() else ""
    ids = [int(m.group(1)) for m in re.finditer(r"DEBATE-(\d+)", content)]
    n = max(ids, default=0) + 1
    return f"DEBATE-{n:04d}"


def _ensure_debate_section(content: str) -> str:
    if "## Debate Packets" in content:
        return content
    return content.rstrip() + "\n\n## Debate Packets\n\n"


def stage_intent_debate_packet(window_days: int = 30, rule_id: str = "") -> dict[str, object]:
    """
    Stage a debate packet when the same rule conflicts across multiple sources.
    Advisory-only workflow for operator arbitration; never merges canonical Record.
    """
    if not PIPELINE_EVENTS_PATH.exists():
        return {"ok": False, "error": "no pipeline events found"}
    cutoff_ts = time.time() - max(1, window_days) * 86400
    events_by_rule: dict[str, list[dict]] = defaultdict(list)
    lines = PIPELINE_EVENTS_PATH.read_text(encoding="utf-8").splitlines()
    for line in lines[-3000:]:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict) or row.get("event") != "intent_conflict_cross_agent":
            continue
        raw_ts = str(row.get("ts") or "").strip()
        if raw_ts:
            try:
                dt = datetime.fromisoformat(raw_ts)
                if dt.timestamp() < cutoff_ts:
                    continue
            except ValueError:
                pass
        rid = str(row.get("rule_id") or "UNKNOWN").strip() or "UNKNOWN"
        events_by_rule[rid].append(row)

    target_rule = rule_id.strip() if rule_id.strip() else ""
    if target_rule and target_rule not in events_by_rule:
        return {"ok": False, "error": f"no conflicts found for {target_rule}"}

    if not target_rule:
        ranked: list[tuple[str, int]] = []
        for rid, rows in events_by_rule.items():
            sources = {str(r.get("candidate_source") or "unknown") for r in rows}
            if len(sources) < 2:
                continue
            ranked.append((rid, len(rows)))
        if not ranked:
            return {"ok": False, "error": "no multi-source cross-agent conflicts in window"}
        ranked.sort(key=lambda x: (-x[1], x[0]))
        target_rule = ranked[0][0]

    rows = events_by_rule.get(target_rule, [])
    by_source: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        source = str(row.get("candidate_source") or "unknown").strip() or "unknown"
        by_source[source].append(row)
    if len(by_source) < 2:
        return {"ok": False, "error": f"rule {target_rule} does not have multi-source conflicts"}

    source_items = sorted(by_source.items(), key=lambda kv: -len(kv[1]))
    left_source, left_rows = source_items[0]
    right_source, right_rows = source_items[1]
    left = left_rows[0]
    right = right_rows[0]
    debate_id = _next_debate_id()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    debate_block = f"""### {debate_id}

```yaml
status: pending
timestamp: {ts}
topic: "cross-agent intent conflict"
rule_id: {target_rule}
source_agents: [{left_source}, {right_source}]
position_a:
  source: {left_source}
  candidate_id: "{left.get('candidate_id') or 'none'}"
  reason: "{str(left.get('reason') or '').replace(chr(34), chr(39))[:220]}"
position_b:
  source: {right_source}
  candidate_id: "{right.get('candidate_id') or 'none'}"
  reason: "{str(right.get('reason') or '').replace(chr(34), chr(39))[:220]}"
operator_prompt: "choose keep_rule | revise_rule | scope_rule | gather_more_evidence"
```

"""
    content = PENDING_REVIEW_PATH.read_text(encoding="utf-8") if PENDING_REVIEW_PATH.exists() else "## Candidates\n\n## Processed\n\n"
    content = _ensure_debate_section(content)
    content = content.replace("## Debate Packets\n\n", "## Debate Packets\n\n" + debate_block, 1)
    PENDING_REVIEW_PATH.write_text(content, encoding="utf-8")
    emit_pipeline_event(
        "intent_debate_packet_staged",
        debate_id,
        rule_id=target_rule,
        source_agents=f"{left_source},{right_source}",
        window_days=window_days,
        source="core:stage_intent_debate_packet",
    )
    return {
        "ok": True,
        "debate_id": debate_id,
        "rule_id": target_rule,
        "source_agents": [left_source, right_source],
    }


def resolve_intent_debate_packet(
    debate_id: str,
    resolution: str,
    actor: str = "",
    channel_key: str = "",
) -> dict[str, object]:
    """
    Resolve a staged debate packet by writing resolution status in PENDING-REVIEW.
    """
    if not PENDING_REVIEW_PATH.exists():
        return {"ok": False, "error": "PENDING-REVIEW not found"}
    content = PENDING_REVIEW_PATH.read_text(encoding="utf-8")
    pattern = rf"(### {re.escape(debate_id)}(?:\s*\([^)]*\))?\s*\n```yaml\n)(.*?)(\n```)"
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        return {"ok": False, "error": f"{debate_id} not found"}
    block = m.group(2)
    if re.search(r"^status:\s*resolved:", block, re.MULTILINE):
        return {"ok": False, "error": f"{debate_id} already resolved"}
    safe_resolution = resolution.strip() or "gather_more_evidence"
    safe_resolution = re.sub(r"[^a-zA-Z0-9_\-:. ]+", "", safe_resolution)[:80]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated = re.sub(
        r"^status:\s*pending\s*$",
        f"status: resolved:{safe_resolution}",
        block,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == block:
        updated = f"status: resolved:{safe_resolution}\n" + block
    updated += f"\nresolved_at: {now}"
    replacement = m.group(1) + updated + m.group(3)
    new_content = content[: m.start()] + replacement + content[m.end() :]
    PENDING_REVIEW_PATH.write_text(new_content, encoding="utf-8")
    emit_pipeline_event(
        "intent_debate_packet_resolved",
        debate_id,
        resolution=safe_resolution,
        actor=actor or None,
        channel_key=channel_key or None,
        source="core:resolve_intent_debate_packet",
    )
    return {"ok": True, "debate_id": debate_id, "resolution": safe_resolution}


def list_unresolved_debate_packets() -> list[dict[str, object]]:
    """List debate packets in PENDING-REVIEW that are still pending (not resolved)."""
    if not PENDING_REVIEW_PATH.exists():
        return []
    content = PENDING_REVIEW_PATH.read_text(encoding="utf-8")
    if "## Debate Packets" not in content:
        return []
    section = content.split("## Debate Packets")[1].split("## ")[0]
    out: list[dict[str, object]] = []
    for m in re.finditer(r"### (DEBATE-\d+)\s*\n```yaml\n(.*?)\n```", section, re.DOTALL):
        debate_id = m.group(1)
        block = m.group(2)
        if re.search(r"^status:\s*resolved:", block, re.MULTILINE):
            continue
        if "status: pending" not in block:
            continue
        row: dict[str, object] = {"debate_id": debate_id}
        rule_m = re.search(r"^rule_id:\s*(.+)$", block, re.MULTILINE)
        if rule_m:
            row["rule_id"] = rule_m.group(1).strip().strip('"')
        src_m = re.search(r"^source_agents:\s*\[?(.*?)\]?", block, re.MULTILINE)
        if src_m:
            row["source_agents"] = [s.strip().strip('"') for s in src_m.group(1).split(",") if s.strip()]
        out.append(row)
    return out


def update_candidate_status(
    candidate_id: str,
    status: str,
    rejection_reason: str | None = None,
    channel_key: str | None = None,
    actor: str | None = None,
    source: str | None = None,
) -> bool:
    """Update candidate status (approved/rejected) in PENDING-REVIEW.md.
    For rejected, optional rejection_reason is stored in PIPELINE-EVENTS for learning.
    """
    if status not in ("approved", "rejected"):
        return False
    if not PENDING_REVIEW_PATH.exists():
        return False
    content = PENDING_REVIEW_PATH.read_text()
    pattern = rf"(### {re.escape(candidate_id)}(?:\s*\([^)]*\))?\s*\n```yaml\n)(status:\s*)pending"
    replacement = rf"\1\2{status}"
    new_content, n = re.subn(pattern, replacement, content, count=1)
    if n == 0:
        return False
    PENDING_REVIEW_PATH.write_text(new_content)
    kwargs: dict[str, object] = {}
    if status == "rejected" and rejection_reason:
        kwargs["rejection_reason"] = rejection_reason
    if channel_key:
        kwargs["channel_key"] = channel_key
    if actor:
        kwargs["actor"] = actor
    if source:
        kwargs["source"] = source
    emit_pipeline_event(status, candidate_id, **kwargs)
    return True


def get_response(channel_key: str, user_message: str) -> str:
    """Get Grace-Mar's response for a given message. Channel-key scopes conversation."""
    history = conversations[channel_key]

    # "We did X" — activity report from operator; run pipeline, skip chat.
    if WE_DID_PATTERN.search(user_message.strip()):
        archive("ACTIVITY REPORT", channel_key, user_message)
        staged = analyze_activity_report(user_message, channel_key)
        emit_pipeline_event("dyad:activity_report", None, channel_key=channel_key)
        count = len(get_pending_candidates())
        if staged:
            return f"got it! i added that to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review to see them."
        return "ok i wrote that down. nothing new to add to your profile right now, but it's in the log! type /review to see what's waiting."

    # "checkpoint" — companion requests checkpoint save; send transcript (since session/last checkpoint) to pipeline and VOICE-ARCHIVE.
    if CHECKPOINT_REQUEST_PATTERN.search(user_message.strip()):
        archive("USER", channel_key, user_message)
        transcript = _format_checkpoint_transcript(history)
        if transcript:
            synthetic = (
                "we did a checkpoint. here is our Telegram conversation since the last checkpoint (or this session):\n\n"
                + transcript
            )
        else:
            synthetic = "we did a checkpoint — companion requested to save state; no conversation since session start yet."
        staged = analyze_activity_report(synthetic, channel_key)
        emit_pipeline_event("dyad:checkpoint_request", None, channel_key=channel_key)
        count = len(get_pending_candidates())
        reply = (
            f"got it! i added a checkpoint to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review"
            if staged
            else "ok i wrote that checkpoint down. nothing new to add to your profile right now, but it's in the log! type /review to see what's waiting."
        )
        archive("GRACE-MAR", channel_key, reply)
        return reply

    # Pasted checkpoint — long message with checkpoint markers; route to pipeline.
    stripped = user_message.strip()
    if len(stripped) >= 400 and CHECKPOINT_MARKERS.search(stripped):
        synthetic = f"we did a chat in an external LLM (ChatGPT, Claude, PRP, etc). here is the checkpoint or transcript:\n\n{stripped}"
        archive("CHECKPOINT HANDBACK", channel_key, stripped[:500] + ("..." if len(stripped) > 500 else ""))
        staged = analyze_activity_report(synthetic, channel_key)
        emit_pipeline_event("dyad:checkpoint_handback", None, channel_key=channel_key)
        count = len(get_pending_candidates())
        if staged:
            return f"got it! i read that checkpoint and added it to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review"
        return "ok i read that checkpoint. nothing new to add to your profile right now, but it's in the log! type /review to see what's waiting."

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
        emit_pipeline_event("dyad:lookup", None, channel_key=channel_key, question=question[:100])

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

    system_content = SYSTEM_PROMPT + _load_memory_appendix()
    messages = [{"role": "system", "content": system_content}] + history

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


def transcribe_voice(audio_bytes: bytes, channel_key: str = "telegram") -> str | None:
    """Transcribe audio via OpenAI Whisper. Returns transcript or None on failure."""
    import tempfile
    try:
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
            f.write(audio_bytes)
            path = f.name
        try:
            with open(path, "rb") as audio_file:
                result = _get_client().audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                )
            transcript = (result.text or "").strip()
            return transcript if transcript else None
        finally:
            Path(path).unlink(missing_ok=True)
    except Exception:
        logger.exception("Whisper transcription error")
        return None


def run_lookup(question: str, channel_key: str = "miniapp") -> str:
    """Public entry point for lookup. Used by Mini App."""
    result = _lookup_with_library_first(question, channel_key)
    emit_pipeline_event("dyad:lookup", None, channel_key=channel_key, source="miniapp", question=question[:100])
    return result


GROUNDED_PROMPT_APPENDIX = """

## GROUNDED MODE
Answer ONLY from the relevant record excerpts below. If the excerpts do not contain enough information to answer, say "I don't know that yet!" and do NOT guess.
When you use information from the record, cite the source ID at the end of the relevant sentence, e.g. [LEARN-0001] or [WRITE-0003]. At least one citation or explicit abstention is required.
"""


def run_grounded_response(
    question: str,
    channel_key: str = "miniapp",
    history: list[dict] | None = None,
) -> str:
    """Response with retrieval: cite source IDs or abstain. Used by Mini App grounded mode."""
    if not _check_rate_limit(channel_key, "main", tokens=1):
        return "i'm a little tired right now. can we talk more in a bit?"
    chunks = _retrieve(question, top_k=5)
    excerpt_block = ""
    if chunks:
        excerpt_block = "\nRelevant record excerpts:\n" + "\n\n".join(
            text for _, text in chunks
        )
    else:
        excerpt_block = "\nNo relevant record excerpts found for this question."
    system = SYSTEM_PROMPT + _load_memory_appendix() + GROUNDED_PROMPT_APPENDIX + excerpt_block
    messages = [{"role": "system", "content": system}]
    if history:
        for h in history:
            role = h.get("role")
            content = (h.get("content") or "").strip()
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": question})
    try:
        response = _get_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=250,
            temperature=0.7,
        )
        if u := getattr(response, "usage", None):
            _log_tokens(channel_key, "main", u.prompt_tokens, u.completion_tokens, OPENAI_MODEL)
        reply = response.choices[0].message.content.strip()
        emit_pipeline_event("dyad:grounded_query", None, channel_key=channel_key, source="miniapp")
        return reply
    except Exception:
        logger.exception("Grounded response error")
        return "um... i got confused. can you try again?"


def reset_conversation(channel_key: str) -> None:
    """Clear conversation history for a channel. Used by /start and /reset."""
    conversations[channel_key] = []
    pending_lookups.pop(channel_key, None)
    end_homework_session(channel_key)


def get_greeting() -> str:
    return (
        "hi! i'm grace-mar — i remember what you've learned and what you've done. "
        "when something cool happens, say \"we did X\" and i'll add it — then /review to see what's waiting. "
        "do you want to talk? i like stories and science and drawing!"
    )


def get_reset_message() -> str:
    return "ok i forgot everything! let's start over. what do you want to talk about?"
