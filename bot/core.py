"""
Shared emulation core for Grace-Mar.

Used by both the Telegram and WeChat bots. Handles LLM conversation,
lookup, analyst, archive, and rate limiting. Channel-agnostic — callers
pass a channel_key (e.g. "telegram:123" or "wechat:oABC123") to scope
conversations and rate limits.
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
    from .prompt import (
    SYSTEM_PROMPT,
    LOOKUP_PROMPT,
    LIBRARY_LOOKUP_PROMPT,
    REPHRASE_PROMPT,
    ANALYST_PROMPT,
)
except ImportError:
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
ARCHIVE_PATH = PROFILE_DIR / "ARCHIVE.md"
ARCHIVE_REPO_PATH = "users/pilot-001/ARCHIVE.md"  # repo-relative for GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
GRACE_MAR_REPO = os.getenv("GRACE_MAR_REPO", "rbtkhn/grace-mar").strip()
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

# "We did X" — activity report from parent/operator. Triggers pipeline staging.
WE_DID_PATTERN = re.compile(
    r"^we\s+(drew|wrote|made|learned|read|painted|built|created|did|watched|played)\b",
    re.IGNORECASE,
)

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


def _format_archive_block(event: str, channel_key: str, text: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"**[{ts}]** `{event}` ({channel_key})\n"]
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
        header = "# CONVERSATION ARCHIVE\n\n> Append-only log of all Grace-Mar interactions (Telegram, WeChat, Mini App). One mind, multiple channels.\n\n---\n\n"
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
    """Append an event to the conversation archive. Uses GitHub API when GITHUB_TOKEN set (Render), else local file."""
    block = _format_archive_block(event, channel_key, text)
    if GITHUB_TOKEN and GRACE_MAR_REPO:
        def _run():
            _append_via_github_api(block)
        threading.Thread(target=_run, daemon=True).start()
    else:
        try:
            ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(ARCHIVE_PATH, "a", encoding="utf-8") as f:
                f.write(block)
        except Exception as e:
            logger.warning("Archive local write error: %s", e)


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


def _library_summary() -> str:
    entries = _load_library()
    lines = []
    for e in entries:
        scope_str = ", ".join(e["scope"]) if e["scope"] else "general"
        label = f"{e['title']} (in {e['volume']})" if e.get("volume") else e["title"]
        lines.append(f"- {label}: {scope_str}")
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


ACTIVITY_REPORT_SYNTHETIC = "[Activity reported by parent/operator. No bot response. Treat as direct evidence of real-world activity. Extract knowledge, curiosity, or personality signals.]"


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
        _stage_candidate(analysis, user_message, ACTIVITY_REPORT_SYNTHETIC, channel_key)
        logger.info("ANALYST: activity report staged")
        return True
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


def update_candidate_status(candidate_id: str, status: str) -> bool:
    """Update candidate status (approved/rejected) in PENDING-REVIEW.md."""
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
    emit_pipeline_event(status, candidate_id)
    return True


def get_response(channel_key: str, user_message: str) -> str:
    """Get Grace-Mar's response for a given message. Channel-key scopes conversation."""
    history = conversations[channel_key]

    # "We did X" — activity report from parent; run pipeline, skip chat.
    if WE_DID_PATTERN.search(user_message.strip()):
        archive("ACTIVITY REPORT", channel_key, user_message)
        staged = analyze_activity_report(user_message, channel_key)
        count = len(get_pending_candidates())
        if staged:
            return f"got it! i added that to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review to see them."
        return "ok i wrote that down. nothing new to add to your profile right now, but it's in the log! type /review to see what's waiting."

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
    return _lookup_with_library_first(question, channel_key)


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
    system = SYSTEM_PROMPT + GROUNDED_PROMPT_APPENDIX + excerpt_block
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
        return response.choices[0].message.content.strip()
    except Exception:
        logger.exception("Grounded response error")
        return "um... i got confused. can you try again?"


def reset_conversation(channel_key: str) -> None:
    """Clear conversation history for a channel. Used by /start and /reset."""
    conversations[channel_key] = []
    pending_lookups.pop(channel_key, None)


def get_greeting() -> str:
    return "hi! i'm grace-mar! do you want to talk? i like stories and science and drawing!"


def get_reset_message() -> str:
    return "ok i forgot everything! let's start over. what do you want to talk about?"
