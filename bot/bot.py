"""
Grace-Mar Telegram Bot

A Telegram bot that responds as Grace-Mar, powered by her
cognitive fork profile data and an OpenAI LLM backend.

Usage (local polling):
    1. Copy .env.example to .env and fill in your keys
    2. pip install -r bot/requirements.txt
    3. python -m bot.bot   # from repo root

For production: use webhook mode via miniapp_server (see docs/telegram-webhook-setup.md).
"""
# Allow running as script: python bot/bot.py (simulate package for relative imports)
if __package__ is None:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "bot"

import asyncio
import importlib.util
import os
import re
import logging
import subprocess
from io import BytesIO
from pathlib import Path
from datetime import datetime, timedelta, time

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonDefault,
    Update,
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
    analyze_activity_report,
    reset_conversation,
    get_greeting,
    get_reset_message,
    get_pending_candidates,
    get_candidate_block,
    update_candidate_status,
    is_low_risk_candidate,
    quick_merge_candidate,
    start_homework_session,
    process_homework_answer,
    is_in_homework_session,
    end_homework_session,
    consume_homework_timeout_notice,
    get_pipeline_health_summary,
    get_intent_audit_summary,
    get_intent_review_summary,
    stage_intent_debate_packet,
    resolve_intent_debate_packet,
    list_unresolved_debate_packets,
    emit_pipeline_event,
    stage_last_exchange,
    run_export_curriculum,
    WE_DID_PATTERN,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROFILE_MINIAPP_URL = (
    os.getenv("PROFILE_MINIAPP_URL", "").strip() or os.getenv("DASHBOARD_MINIAPP_URL", "").strip()
).rstrip("/")
USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
OPERATOR_CHAT_ID = os.getenv("GRACE_MAR_OPERATOR_CHAT_ID", "").strip()
OPERATOR_REMINDER_ENABLED = os.getenv("GRACE_MAR_OPERATOR_REMINDERS", "1").strip().lower() not in {"0", "false", "no"}
OPERATOR_REMINDER_INTERVAL_SEC = int(os.getenv("GRACE_MAR_OPERATOR_REMINDER_INTERVAL_SEC", "21600"))
OPERATOR_PENDING_THRESHOLD = int(os.getenv("GRACE_MAR_OPERATOR_PENDING_THRESHOLD", "5"))
OPERATOR_STALE_DAYS = int(os.getenv("GRACE_MAR_OPERATOR_STALE_DAYS", "7"))

# Idle checkpoint prompt: daily nudge to add anything from the day (passive capture)
IDLE_CHECKPOINT_ENABLED = os.getenv("GRACE_MAR_IDLE_CHECKPOINT_ENABLED", "0").strip().lower() in {"1", "true", "yes"}
IDLE_CHECKPOINT_HOUR = int(os.getenv("GRACE_MAR_IDLE_CHECKPOINT_HOUR", "20"))
IDLE_CHECKPOINT_MINUTE = int(os.getenv("GRACE_MAR_IDLE_CHECKPOINT_MINUTE", "0"))
IDLE_CHECKPOINT_CHAT_ID = os.getenv("GRACE_MAR_IDLE_CHECKPOINT_CHAT_ID", "").strip() or OPERATOR_CHAT_ID

# Guided "we did X" / post-activity log prompts (single place for copy)
PROMPT_GOODBYE_ADD_ANYTHING = (
    "ok! anything from today you'd like me to remember? (paste or type to add; or just leave it)"
)
PROMPT_LOG_WHAT_DID_YOU_DO = (
    "What did you do? Reply with a short line and I'll add it for review."
)


def _activity_report_reply(staged: bool, count: int) -> str:
    """Reply text after staging an activity report (shared by /log and awaiting_log)."""
    if staged:
        return (
            f"got it! i added that to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review to see them."
        )
    return "ok i wrote that down. nothing new to add to your profile right now, but it's in the log! type /review to see what's waiting."


def _channel_key(chat_id: int) -> str:
    return f"telegram:{chat_id}"


def _profile_path(filename: str) -> Path:
    return Path(__file__).resolve().parent.parent / "users" / USER_ID / filename


async def _run_blocking(func, *args, **kwargs):
    """Run blocking core work without blocking Telegram event loop."""
    return await asyncio.to_thread(func, *args, **kwargs)


def _is_operator_chat(update: Update) -> bool:
    """True if chat has operator access. When OPERATOR_CHAT_ID is not set, any chat does (single-chat mode)."""
    if not OPERATOR_CHAT_ID:
        return True  # No restriction: all commands available in every chat
    chat_id = update.effective_chat.id if update.effective_chat else None
    return bool(chat_id) and str(chat_id) == OPERATOR_CHAT_ID


def _looks_like_paste_handback(text: str) -> bool:
    """True if message looks like pasted transcript (external LLM chat, notes)."""
    if not text or len(text) < 500:
        return False
    lines = text.count("\n")
    transcript_markers = re.search(
        r"\b(User|Assistant|Human|AI|Me|ChatGPT|Claude|System|Bot):\s",
        text,
        re.IGNORECASE,
    )
    return lines >= 4 or bool(transcript_markers)


def _is_operator_review_intent(text: str) -> bool:
    """True if message indicates operator wants to see/approve candidates (route to review, not Voice)."""
    t = text.strip().lower()
    if not t:
        return False
    review_words = ("candidate", "approval", "approve", "review")
    if any(w in t for w in review_words) and any(x in t for x in ("show", "these", "one by one", "me")):
        return True
    if "show me these" in t and ("candidate" in t or "approval" in t):
        return True
    if "candidates for approval" in t:
        return True
    return False


def _format_health_summary(summary: dict) -> str:
    oldest = summary.get("oldest_pending_days")
    oldest_txt = "n/a" if oldest is None else f"{oldest} day(s)"
    rejections = summary.get("recent_rejection_reasons") or []
    rejection_txt = "; ".join(rejections) if rejections else "none"
    return (
        f"pending: {summary.get('pending_count', 0)} (oldest: {oldest_txt})\n"
        f"rate(main): {summary.get('main_used', 0)}/{summary.get('main_limit', 0)} "
        f"rate(analyst): {summary.get('analyst_used', 0)}/{summary.get('analyst_limit', 0)}\n"
        f"last event: {summary.get('last_event_ts') or 'n/a'}\n"
        f"recent rejects: {rejection_txt}"
    )


def _format_intent_audit(summary: dict) -> str:
    def _top_items(mapping: dict, limit: int = 3) -> str:
        if not mapping:
            return "none"
        pairs = list(mapping.items())[:limit]
        return ", ".join(f"{k}:{v}" for k, v in pairs)

    lines = [
        f"Intent audit ({summary.get('window_days', 30)}d)",
        f"cross-agent conflicts: {summary.get('total_conflicts', 0)}",
        f"rejections: {summary.get('total_rejections', 0)}",
        f"by source: {_top_items(summary.get('conflicts_by_source') or {})}",
        f"by rule: {_top_items(summary.get('conflicts_by_rule') or {})}",
        f"strategies: {_top_items(summary.get('conflict_strategies') or {})}",
        f"rejection categories: {_top_items(summary.get('rejection_categories') or {})}",
    ]
    recent = summary.get("recent_conflicts") or []
    if recent:
        latest = recent[0]
        lines.append(
            "latest: "
            f"{latest.get('candidate_id') or 'n/a'} "
            f"{latest.get('source') or 'unknown'} "
            f"{latest.get('rule_id') or 'UNKNOWN'}"
        )
    return "\n".join(lines)


def _format_intent_review(summary: dict) -> str:
    lines = [
        f"Intent review ({summary.get('window_days', 30)}d)",
        f"conflicts: {summary.get('total_conflicts', 0)}",
        f"rejections: {summary.get('total_rejections', 0)}",
    ]
    by_source = summary.get("conflicts_by_source") or {}
    if by_source:
        top_source = list(by_source.items())[:3]
        lines.append("top sources: " + ", ".join(f"{k}:{v}" for k, v in top_source))
    by_rule = summary.get("conflicts_by_rule") or {}
    if by_rule:
        top_rules = list(by_rule.items())[:3]
        lines.append("top rules: " + ", ".join(f"{k}:{v}" for k, v in top_rules))
    updates = summary.get("suggested_updates") or []
    if updates:
        lines.append("")
        lines.append("suggested updates:")
        for item in updates[:3]:
            lines.append(
                "- "
                + str(item.get("suggestion") or "review intent rules")
            )
    else:
        lines.append("suggested updates: none")
    return "\n".join(lines)


# Session paths shown on /start — instructions/commands to Grace-Mar.
# Each option sets a different interaction model; tapping sends that text to Grace-Mar.
# All must be actions Grace-Mar can execute (ask, help, explore, chat).
# - Ask me what I'm thinking: thought-exposure path (she asks, user shares, she responds)
# - Look something up: lookup flow (user asks, she looks up and explains)
# - Explore: curiosity-driven topic dive
# - Ask me what I'm curious about: she asks, user answers
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
    await update.message.reply_text(greeting)


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
            filename="grace-mar-llm.txt",
            caption="Portable Record Prompt — paste into ChatGPT, Claude, or any LLM to chat with my Record.",
        )
    except Exception:
        logger.exception("PRP export error")
        await update.message.reply_text("i couldn't make the PRP right now. try again in a little bit?")


async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not PROFILE_MINIAPP_URL:
        await update.message.reply_text(
            "Profile Mini App URL not configured. Set PROFILE_MINIAPP_URL (or DASHBOARD_MINIAPP_URL) in .env and "
            "serve the profile over HTTPS. See docs/miniapp-setup.md."
        )
        return
    summary = get_pipeline_health_summary()
    summary_text = _format_health_summary(summary)
    await update.message.reply_text(
        "Open the fork profile to view identity, pipeline, SKILLS, benchmarks, and disclosure.\n\n"
        f"Quick health:\n{summary_text}\n\n{PROFILE_MINIAPP_URL}"
    )


async def _homework_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start homework session (one question at a time). Same as tapping Homework button."""
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    try:
        first_q, err = await _run_blocking(start_homework_session, key)
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
    await update.message.reply_text(msg)


def _checkpoint_to_github() -> tuple[bool, str]:
    """
    Commit and push session-transcript.md and recursion-gate.md to GitHub.
    Returns (ok, message). Operator should run this from the bot's repo root.
    """
    repo_root = Path(__file__).resolve().parent.parent
    files = [
        f"users/{USER_ID}/session-transcript.md",
        f"users/{USER_ID}/recursion-gate.md",
    ]
    for f in files:
        if not (repo_root / f).exists():
            return False, f"file not found: {f}"
    try:
        r = subprocess.run(
            ["git", "-C", str(repo_root), "add"] + files,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode != 0:
            return False, f"git add failed: {r.stderr or r.stdout or 'unknown'}"
        r = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"] + files,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not (r.stdout or "").strip():
            return True, "nothing new to push (already up to date)"
        r = subprocess.run(
            ["git", "-C", str(repo_root), "commit", "-m", "checkpoint: sync transcript and recursion-gate"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode != 0:
            return False, f"git commit failed: {r.stderr or r.stdout or 'unknown'}"
        r = subprocess.run(
            ["git", "-C", str(repo_root), "push"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode != 0:
            return False, f"git push failed: {r.stderr or r.stdout or 'unknown'}"
        return True, "checkpoint pushed to GitHub ✓"
    except subprocess.TimeoutExpired:
        return False, "git command timed out"
    except FileNotFoundError:
        return False, "git not found"
    except Exception as e:
        logger.exception("Checkpoint error")
        return False, str(e)


async def checkpoint_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only: commit and push session-transcript + recursion-gate to GitHub."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    try:
        ok, msg = await _run_blocking(_checkpoint_to_github)
        await update.message.reply_text(msg)
        if ok:
            archive("CHECKPOINT", _channel_key(update.effective_chat.id), msg)
    except Exception:
        logger.exception("Checkpoint command error")
        await update.message.reply_text("checkpoint failed — try again or push manually.")


def _is_in_review_session(context: ContextTypes.DEFAULT_TYPE) -> bool:
    """True if chat has an active review session (one-letter entry flow)."""
    candidates = context.chat_data.get("review_candidate_ids")
    index = context.chat_data.get("review_index", 0)
    return candidates is not None and 0 <= index < len(candidates)


def _format_review_candidate(c: dict, index: int, total: int) -> str:
    """Format one candidate for review, with one-letter prompt."""
    short = c["summary"][:80] + "…" if len(c["summary"]) > 80 else c["summary"]
    return f"[{index + 1}/{total}] {c['id']}:\n{short}\n\nA=Approve R=Reject N=Skip Q=Quit"


async def _process_review_choice(
    update: Update, context: ContextTypes.DEFAULT_TYPE, choice: str
) -> bool:
    """Process A/R/N/Q in review session. Returns True if handled."""
    candidates = context.chat_data.get("review_candidate_ids") or []
    index = context.chat_data.get("review_index", 0)
    if index >= len(candidates):
        return False
    cid = candidates[index]
    choice = choice.strip().upper()
    chat_id = update.effective_chat.id if update.effective_chat else None
    actor_id = update.effective_user.id if update.effective_user else None
    key = _channel_key(chat_id) if chat_id else None
    approved_by = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator").strip() or "operator"

    if choice == "A":
        ok = update_candidate_status(cid, "approved", channel_key=key, actor=f"telegram:{actor_id}" if actor_id else None, source="telegram:review")
        if ok and _is_operator_chat(update) and is_low_risk_candidate(cid):
            try:
                merge_ok, msg = await _run_blocking(quick_merge_candidate, cid, approved_by)
                await update.message.reply_text(f"✅ {cid} — merged! (quick approve)")
            except Exception:
                logger.exception("Quick merge in review")
                await update.message.reply_text(f"✅ {cid} — approved. Quick merge failed — /merge for receipt.")
        elif ok:
            await update.message.reply_text(f"✅ {cid} — approved")
        else:
            await update.message.reply_text(f"couldn't approve {cid} (not pending?)")
    elif choice == "R":
        ok = update_candidate_status(cid, "rejected", channel_key=key, actor=f"telegram:{actor_id}" if actor_id else None, source="telegram:review")
        await update.message.reply_text(f"❌ {cid} — rejected" if ok else f"couldn't reject {cid}")
    elif choice == "N":
        await update.message.reply_text(f"⏭ {cid} — skipped")
    elif choice == "Q":
        context.chat_data.pop("review_candidate_ids", None)
        context.chat_data.pop("review_index", None)
        await update.message.reply_text("review ended")
        return True
    else:
        await update.message.reply_text("type A, R, N, or Q")
        return True

    context.chat_data["review_index"] = index + 1
    await _show_next_review_candidate(update, context)
    return True


async def _show_next_review_candidate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show next candidate in review session, or 'that's all'."""
    candidates = context.chat_data.get("review_candidate_ids") or []
    index = context.chat_data.get("review_index", 0)
    key = _channel_key(update.effective_chat.id) if update.effective_chat else None
    if index >= len(candidates):
        context.chat_data.pop("review_candidate_ids", None)
        context.chat_data.pop("review_index", None)
        msg = "that's all — no more candidates."
        if key:
            archive("GRACE-MAR (review)", key, msg)
        await update.message.reply_text(msg)
        return
    fresh = get_pending_candidates()
    cid = candidates[index]
    c = next((x for x in fresh if x["id"] == cid), {"id": cid, "summary": "(no longer pending)"})
    text = _format_review_candidate(c, index, len(candidates))
    if key:
        archive("GRACE-MAR (review)", key, f"showing {cid} [{index + 1}/{len(candidates)}]")
    await update.message.reply_text(text)


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show pending candidates one at a time. Type A=Approve R=Reject N=Skip Q=Quit."""
    candidates = get_pending_candidates()
    chat_id = update.effective_chat.id if update.effective_chat else None
    key = _channel_key(chat_id) if chat_id else None
    if not candidates:
        msg = "nothing to review right now! when we add something new, you'll see it here."
        if key:
            archive("USER", key, "/review")
            archive("GRACE-MAR (review)", key, msg)
        await update.message.reply_text(msg)
        return
    context.chat_data["review_candidate_ids"] = [c["id"] for c in candidates]
    context.chat_data["review_index"] = 0
    if key:
        archive("USER", key, "/review")
    await _show_next_review_candidate(update, context)


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
        if consume_homework_timeout_notice(key):
            await query.edit_message_text("homework timed out after a break — tap Homework to start again!")
        else:
            await query.edit_message_text("homework session ended — tap Homework to start again!")
        return
    try:
        response, session_ended, has_next = await _run_blocking(process_homework_answer, key, letter)
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

    # Low-friction: operator + low-risk + approve → quick merge (one-tap)
    do_quick_merge = (
        action == "approve"
        and _is_operator_chat(update)
        and is_low_risk_candidate(candidate_id)
    )
    approved_by = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator").strip() or "operator"

    ok = update_candidate_status(
        candidate_id,
        status,
        channel_key=channel_key,
        actor=f"telegram:{actor_id}" if actor_id else None,
        source="telegram:callback",
    )
    if not ok:
        await query.edit_message_text(f"couldn't update {candidate_id}")
        return

    if do_quick_merge:
        try:
            merge_ok, msg = await _run_blocking(quick_merge_candidate, candidate_id, approved_by)
            if merge_ok:
                await query.edit_message_text(f"✅ {candidate_id} — merged! (quick approve)")
            else:
                await query.edit_message_text(f"✅ {candidate_id} — approved. Merge failed: {msg[:80]}. Run /merge for receipt flow.")
        except Exception:
            logger.exception("Quick merge error")
            await query.edit_message_text(f"✅ {candidate_id} — approved. Quick merge failed — run /merge for receipt flow.")
        return

        emoji = "✅" if action == "approve" else "❌"
        await query.edit_message_text(f"{emoji} {candidate_id} — {status}")


async def stage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Agentic pipeline assistant: stage the last exchange to PENDING-REVIEW (never merge)."""
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    try:
        ok, msg = await _run_blocking(stage_last_exchange, key)
        archive("STAGE (agentic)", key, msg)
        await update.message.reply_text(msg)
    except Exception:
        logger.exception("Stage command error")
        await update.message.reply_text("i couldn't stage that right now. try again?")


async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guided 'we did X': log activity for the record. With no args, ask for a reply; with args, stage immediately."""
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    args = context.args or []

    if not args:
        await update.message.reply_text(PROMPT_LOG_WHAT_DID_YOU_DO)
        context.user_data["awaiting_log"] = True
        return

    text = " ".join(args).strip()
    synthetic = text if WE_DID_PATTERN.search(text) else "we did " + text
    archive("ACTIVITY REPORT (/log)", key, text)
    try:
        staged = await _run_blocking(analyze_activity_report, synthetic, key)
        count = len(get_pending_candidates())
        await update.message.reply_text(_activity_report_reply(staged, count))
    except Exception:
        logger.exception("Log command error")
        await update.message.reply_text("i couldn't add that right now. try again?")


async def export_curriculum_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Export curriculum profile (JSON) — shareable for adaptive curriculum engines."""
    args = context.args or []
    audience = "alpha-school" if "alpha" in " ".join(args).lower() else None
    try:
        content = await _run_blocking(run_export_curriculum, None, audience)
        buf = BytesIO(content.encode("utf-8"))
        buf.seek(0)
        caption = "Curriculum profile — curiosity, knowledge, skills edge, evidence anchors."
        if audience:
            caption += " (alpha-school context included)"
        await update.message.reply_document(
            document=buf,
            filename="curriculum_profile.json",
            caption=caption,
        )
    except Exception:
        logger.exception("Export curriculum error")
        await update.message.reply_text("i couldn't make the curriculum export right now. try again in a bit?")


async def approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Approve a candidate by ID. If operator and low-risk, quick-merge immediately."""
    args = context.args or []
    if not args:
        await update.message.reply_text(
            "Usage: /approve CANDIDATE-0040\n"
            "If you're the operator and the candidate is low-risk, it merges immediately."
        )
        return
    candidate_id = args[0]
    if not candidate_id.upper().startswith("CANDIDATE-"):
        await update.message.reply_text(f"Expected CANDIDATE-XXXX, got {candidate_id}")
        return
    chat_id = update.effective_chat.id if update.effective_chat else None
    actor_id = update.effective_user.id if update.effective_user else None
    approved_by = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator").strip() or "operator"

    ok = update_candidate_status(
        candidate_id,
        "approved",
        channel_key=_channel_key(chat_id) if chat_id else None,
        actor=f"telegram:{actor_id}" if actor_id else None,
        source="telegram:command",
    )
    if not ok:
        await update.message.reply_text(f"couldn't approve {candidate_id} (not pending?)")
        return

    if _is_operator_chat(update) and is_low_risk_candidate(candidate_id):
        try:
            merge_ok, msg = await _run_blocking(quick_merge_candidate, candidate_id, approved_by)
            if merge_ok:
                await update.message.reply_text(f"✅ {candidate_id} — merged! (quick approve)")
            else:
                await update.message.reply_text(
                    f"✅ {candidate_id} — approved. Merge failed: {msg[:80]}. Run /merge for receipt flow."
                )
        except Exception:
            logger.exception("Quick approve merge error")
            await update.message.reply_text(
                f"✅ {candidate_id} — approved. Quick merge failed — run /merge for receipt flow."
            )
    else:
        await update.message.reply_text(
            f"✅ {candidate_id} — approved. Type /merge for receipt-based merge instructions."
        )


async def merge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tell user how to merge approved candidates."""
    candidates = get_pending_candidates()
    # Count approved (we only have pending in get_pending_candidates — approved are different)
    from pathlib import Path
    import re
    from scripts.recursion_gate_review import split_gate_sections
    recursion_gate_path = _profile_path("recursion-gate.md")
    content = recursion_gate_path.read_text() if recursion_gate_path.exists() else ""
    active_section, _processed_section = split_gate_sections(content)
    approved = len(re.findall(r"status: approved", active_section))
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
    """Rotate MEMORY/SELF-ARCHIVE context files and emit maintenance event."""
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


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only runtime/pipeline status summary."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    chat_id = update.effective_chat.id if update.effective_chat else 0
    summary = get_pipeline_health_summary(channel_key=_channel_key(chat_id))
    await update.message.reply_text(f"Operator status:\n{_format_health_summary(summary)}")


async def intent_audit_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only summary of intent conflicts and drift signals."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    window_days = 30
    if context.args and context.args[0].isdigit():
        window_days = max(1, min(180, int(context.args[0])))
    summary = await _run_blocking(get_intent_audit_summary, window_days)
    await update.message.reply_text(_format_intent_audit(summary))


async def intent_review_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only constitution review with actionable suggestions."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    window_days = 30
    if context.args and context.args[0].isdigit():
        window_days = max(1, min(180, int(context.args[0])))
    summary = await _run_blocking(get_intent_review_summary, window_days)
    chat_id = update.effective_chat.id if update.effective_chat else None
    emit_pipeline_event(
        "intent_review_generated",
        None,
        source="telegram:command",
        channel_key=_channel_key(chat_id) if chat_id else None,
        actor=f"telegram:{update.effective_user.id}" if update.effective_user else None,
        window_days=window_days,
        suggestion_count=len(summary.get("suggested_updates") or []),
    )
    await update.message.reply_text(_format_intent_review(summary))


async def intent_debate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only: stage a debate packet from cross-agent intent conflicts."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    rule_id = ""
    window_days = 30
    for arg in context.args or []:
        if arg.isdigit():
            window_days = max(1, min(180, int(arg)))
        elif arg.upper().startswith("INTENT-RULE-"):
            rule_id = arg.strip()
    result = await _run_blocking(stage_intent_debate_packet, window_days, rule_id)
    if not result.get("ok"):
        await update.message.reply_text(f"no debate staged: {result.get('error', 'unknown error')}")
        return
    await update.message.reply_text(
        "debate packet staged: "
        f"{result.get('debate_id')} "
        f"(rule={result.get('rule_id')}, sources={','.join(result.get('source_agents') or [])})"
    )


async def resolve_debate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only: resolve a staged debate packet."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    args = context.args or []
    if len(args) < 2:
        await update.message.reply_text(
            "Usage: /resolve_debate DEBATE-0001 <keep_rule|revise_rule|scope_rule|gather_more_evidence>"
        )
        return
    debate_id = args[0].strip().upper()
    resolution = " ".join(args[1:]).strip()
    if not debate_id.startswith("DEBATE-"):
        await update.message.reply_text(f"Expected DEBATE-XXXX, got {debate_id}")
        return
    chat_id = update.effective_chat.id if update.effective_chat else None
    actor = f"telegram:{update.effective_user.id}" if update.effective_user else ""
    result = await _run_blocking(
        resolve_intent_debate_packet,
        debate_id,
        resolution,
        actor,
        _channel_key(chat_id) if chat_id else "",
    )
    if not result.get("ok"):
        await update.message.reply_text(f"couldn't resolve debate: {result.get('error', 'unknown error')}")
        return
    await update.message.reply_text(
        f"debate resolved: {result.get('debate_id')} -> {result.get('resolution')}"
    )


async def debates_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only: list unresolved debate packets."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return
    packets = await _run_blocking(list_unresolved_debate_packets)
    if not packets:
        await update.message.reply_text("no unresolved debate packets.")
        return
    lines = [f"• {p['debate_id']} — rule={p.get('rule_id', '?')} — {', '.join(p.get('source_agents') or [])}" for p in packets]
    await update.message.reply_text("unresolved debates:\n" + "\n".join(lines) + "\n\n/resolve_debate DEBATE-XXXX <resolution>")


async def openclaw_export_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Operator-only OpenClaw export trigger."""
    if OPERATOR_CHAT_ID and not _is_operator_chat(update):
        await update.message.reply_text("this command is operator-only.")
        return

    fmt = "md+manifest"
    output = ""
    if context.args:
        if context.args[0] in {"md", "md+manifest", "json+md", "full-prp", "fork-json"}:
            fmt = context.args[0]
        if len(context.args) > 1:
            output = context.args[1]
    cmd = [
        "python3",
        "integrations/openclaw_hook.py",
        "--user",
        USER_ID,
        "--format",
        fmt,
        "--emit-event",
    ]
    if output:
        cmd.extend(["--output", output])
    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (result.stdout or result.stderr or "").strip()
        if result.returncode == 0:
            await update.message.reply_text(f"openclaw export complete ({fmt}).")
        else:
            await update.message.reply_text(f"openclaw export failed: {out[:400]}")
    except Exception:
        logger.exception("OpenClaw export command failed")
        await update.message.reply_text("openclaw export failed unexpectedly.")


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


async def idle_checkpoint_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Daily idle checkpoint prompt: gentle nudge to add anything from the day (passive capture)."""
    if not IDLE_CHECKPOINT_ENABLED or not IDLE_CHECKPOINT_CHAT_ID:
        return
    try:
        await context.bot.send_message(
            chat_id=int(IDLE_CHECKPOINT_CHAT_ID),
            text="anything from today you'd like me to remember? (paste or type to add; or just leave it)",
        )
    except Exception:
        logger.exception("Idle checkpoint job error")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    key = _channel_key(chat_id)
    user_message = update.message.text

    # Homework flow: one question at a time, gamified
    if user_message.strip().lower() == "homework":
        try:
            first_q, err = await _run_blocking(start_homework_session, key)
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
    if (not is_in_homework_session(key)) and consume_homework_timeout_notice(key):
        await update.message.reply_text("homework timed out after a break — tap Homework to start again 🎯")
        return

    if is_in_homework_session(key):
        reply_lower = user_message.strip().lower()
        if reply_lower in ("stop", "quit", "done", "exit"):
            end_homework_session(key)
            archive("HOMEWORK STOPPED", key, reply_lower)
            await update.message.reply_text("ok homework paused! tap Homework anytime to start again 🎯")
            return
        try:
            response, session_ended, has_next = await _run_blocking(process_homework_answer, key, user_message)
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

    # Review session: A/R/N/Q one-letter entry (no buttons)
    if _is_in_review_session(context):
        letter = user_message.strip().upper()[:1]
        if letter in "ARNQ":
            await _process_review_choice(update, context, letter)
        else:
            await update.message.reply_text("type A, R, N, or Q")
        return

    # Operator intent: "show me candidates one by one" etc → route to review
    if _is_operator_chat(update) and _is_operator_review_intent(user_message):
        archive("USER", key, user_message)
        await review(update, context)
        return

    # Guided log: reply after /log (no args) or after goodbye prompt → treat as activity report
    if context.user_data.get("awaiting_log"):
        context.user_data["awaiting_log"] = False
        msg_stripped = user_message.strip()
        synthetic = msg_stripped if WE_DID_PATTERN.search(msg_stripped) else "we did " + msg_stripped
        archive("ACTIVITY REPORT (guided)", key, user_message)
        try:
            staged = await _run_blocking(analyze_activity_report, synthetic, key)
            count = len(get_pending_candidates())
            await update.message.reply_text(_activity_report_reply(staged, count))
        except Exception:
            logger.exception("Guided log (awaiting_log) error")
            await update.message.reply_text("i couldn't add that right now. try again or say \"we did X\" later?")
        return

    # Paste-as-handback: long transcript-like paste → stage as activity report
    if _looks_like_paste_handback(user_message):
        synthetic = (
            "we did a chat in an external LLM (ChatGPT, Claude, etc). here is the checkpoint or transcript:\n\n"
            + user_message
        )
        archive("HANDBACK PASTE", key, user_message[:500] + ("..." if len(user_message) > 500 else ""))
        try:
            staged = await _run_blocking(analyze_activity_report, synthetic, key)
            count = len(get_pending_candidates())
            if staged:
                await update.message.reply_text(
                    f"got it! i read that and added it to your record. you have {count} thing{'s' if count != 1 else ''} to review — type /review"
                )
            else:
                await update.message.reply_text(
                    "ok i read that. nothing new to add to your profile right now, but it's in the log! type /review"
                )
        except Exception:
            logger.exception("Paste handback error")
            await update.message.reply_text("i couldn't read that paste right now. try again or send as a .txt file?")
        return

    # Session-end idle prompt: goodbye-type phrase → gentle "anything to add?"
    goodbye_patterns = (
        "bye", "goodbye", "good bye", "see you", "talk later", "that's all",
        "done for now", "done for today", "done for the day", "signing off",
    )
    if user_message.strip().lower() in goodbye_patterns or any(
        user_message.strip().lower().startswith(p) for p in ("bye", "goodbye", "see you", "talk later")
    ):
        archive("USER", key, user_message)
        await update.message.reply_text(PROMPT_GOODBYE_ADD_ANYTHING)
        context.user_data["awaiting_log"] = True
        return

    try:
        response = await _run_blocking(get_response, key, user_message)
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
    staged = await _run_blocking(analyze_activity_report, synthetic, key)
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
        transcript = await _run_blocking(transcribe_voice, bytes(buf), channel_key=key)
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
            response, _, has_next = await _run_blocking(process_homework_answer, key, transcript)
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
        response = await _run_blocking(get_response, key, transcript)
        await update.message.reply_text(response)
    except Exception:
        logger.exception("Error generating response after voice")
        await update.message.reply_text("um... i got confused. can you say that again?")


def create_application(webhook_mode: bool = False) -> Application:
    """Build and return the configured Telegram Application.
    When webhook_mode=True, uses updater=None for custom webhook (caller injects updates)."""
    async def set_menu_button(application: Application) -> None:
        # Keyboard-first: no custom menu button (default bot commands)
        await application.bot.set_chat_menu_button(menu_button=MenuButtonDefault())
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
        if IDLE_CHECKPOINT_ENABLED and IDLE_CHECKPOINT_CHAT_ID and application.job_queue:
            application.job_queue.run_daily(
                idle_checkpoint_job,
                time=time(hour=IDLE_CHECKPOINT_HOUR, minute=IDLE_CHECKPOINT_MINUTE),
                name="idle_checkpoint",
            )
            logger.info(
                "Idle checkpoint prompt enabled for chat %s (daily at %02d:%02d)",
                IDLE_CHECKPOINT_CHAT_ID,
                IDLE_CHECKPOINT_HOUR,
                IDLE_CHECKPOINT_MINUTE,
            )

    builder = Application.builder().token(TELEGRAM_TOKEN).post_init(set_menu_button)
    if webhook_mode:
        builder = builder.updater(None)
    app = builder.build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prp", prp))
    app.add_handler(CommandHandler("profile", profile_cmd))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("intent_audit", intent_audit_command))
    app.add_handler(CommandHandler("intent_review", intent_review_command))
    app.add_handler(CommandHandler("intent_debate", intent_debate_command))
    app.add_handler(CommandHandler("resolve_debate", resolve_debate_command))
    app.add_handler(CommandHandler("debates", debates_command))
    app.add_handler(CommandHandler("openclaw_export", openclaw_export_command))
    app.add_handler(CommandHandler("homework", _homework_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("review", review))
    app.add_handler(CommandHandler("checkpoint", checkpoint_command))
    app.add_handler(CommandHandler("approve", approve_command))
    app.add_handler(CommandHandler("stage", stage_command))
    app.add_handler(CommandHandler("log", log_command))
    app.add_handler(CommandHandler("export_curriculum", export_curriculum_command))
    app.add_handler(CommandHandler("merge", merge_command))
    app.add_handler(CommandHandler("reject", reject_with_reason))
    app.add_handler(CommandHandler("rotate", rotate_context_command))
    app.add_handler(CallbackQueryHandler(callback_homework_answer, pattern=r"^hw:[ABCD]$"))
    app.add_handler(CallbackQueryHandler(callback_approve_reject))  # Legacy: old review messages with buttons
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
