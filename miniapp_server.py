#!/usr/bin/env python3
"""
Grace-Mar Q&A Mini App server.

Serves the interactive Q&A Mini App and provides the /api/ask endpoint.
Optional: Telegram webhook (when TELEGRAM_BOT_TOKEN and webhook URL are set).
Deploy to Railway, Render, or run locally with ngrok for Telegram testing.

Usage:
    pip install flask python-dotenv openai python-telegram-bot
    OPENAI_API_KEY=... python miniapp_server.py

Set PORT (default 5000) for hosting. Enable CORS if Mini App is on a different origin.
Real-time exchanges are appended to users/<user>/session-transcript.md (same as Telegram).
SELF-ARCHIVE is updated only when candidates are merged via process_approved_candidates (gated).
For Telegram webhook: TELEGRAM_BOT_TOKEN, WEBHOOK_BASE_URL (or RENDER_EXTERNAL_URL on Render).
Family hub: FAMILY_APP_TOKEN, routes /app, /api/family/*.
Work-politics internal dashboard (env `WAP_DASHBOARD_TOKEN`), routes `/wap`, `/api/wap/jobs`.
"""

import asyncio
import json
import logging
import os
import re
import secrets
import subprocess
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, send_from_directory

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")
load_dotenv(REPO_ROOT / "bot" / ".env")

USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from repo_io import assert_canonical_record_layout  # noqa: E402

assert_canonical_record_layout(USER_ID, context="miniapp_server")

from openai import OpenAI

from bot.prompt import SYSTEM_PROMPT
from bot.core import (
    run_lookup,
    run_grounded_response,
    LOOKUP_TRIGGER,
    AFFIRMATIVE_WORDS,
    AFFIRMATIVE_PHRASES,
    emit_pipeline_event,
    is_low_risk_candidate,
    quick_merge_candidate,
    update_candidate_status,
    analyze_activity_report,
    get_pending_candidates,
)
from scripts.recursion_gate_review import filter_review_candidates, get_review_candidate, parse_review_candidates
from scripts import process_approved_candidates as pac
from scripts.recursion_gate_territory import TERRITORY_WAP, territory_from_yaml_block
from scripts.work_politics_ops import get_wap_snapshot
from scripts.generate_wap_weekly_brief import build_wap_weekly_brief

app = Flask(__name__, static_folder="miniapp", static_url_path="")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
USER_DIR = REPO_ROOT / "users" / USER_ID
ARTIFACTS_DIR = USER_DIR / "artifacts"
SESSION_TRANSCRIPT_PATH = USER_DIR / "session-transcript.md"
RECURSION_GATE_PATH = USER_DIR / "recursion-gate.md"
PIPELINE_EVENTS_PATH = USER_DIR / "pipeline-events.jsonl"
OPERATOR_FETCH_SECRET = os.getenv("OPERATOR_FETCH_SECRET", "").strip()
FAMILY_APP_TOKEN = os.getenv("FAMILY_APP_TOKEN", "").strip()
WAP_DASHBOARD_TOKEN = os.getenv("WAP_DASHBOARD_TOKEN", "").strip()
OPERATOR_NAME = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web").strip() or "operator-web"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
WEBHOOK_BASE_URL = (
    os.getenv("WEBHOOK_BASE_URL", "").strip()
    or os.getenv("RENDER_EXTERNAL_URL", "").strip()
).rstrip("/")
logger = logging.getLogger(__name__)

_telegram_app = None
_telegram_loop = None


def _start_telegram_webhook() -> None:
    """Start Telegram webhook in a background thread. Run once at startup."""
    global _telegram_app, _telegram_loop
    if not TELEGRAM_BOT_TOKEN or not WEBHOOK_BASE_URL:
        return
    if not OPENAI_API_KEY:
        logger.warning("Telegram webhook skipped: OPENAI_API_KEY not set")
        return

    def _run_bot() -> None:
        global _telegram_app, _telegram_loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        _telegram_loop = loop

        sys.path.insert(0, str(REPO_ROOT))
        from bot.bot import create_application
        from telegram import Update

        app = create_application(webhook_mode=True)
        _telegram_app = app

        async def _setup() -> None:
            await app.initialize()
            await app.start()
            webhook_url = f"{WEBHOOK_BASE_URL}/telegram/webhook"
            await app.bot.set_webhook(url=webhook_url, allowed_updates=Update.ALL_TYPES)
            logger.info("Telegram webhook set: %s", webhook_url)

        loop.run_until_complete(_setup())
        loop.run_forever()

    t = threading.Thread(target=_run_bot, daemon=True)
    t.start()
    logger.info("Telegram webhook thread started")


def _format_archive_block(event: str, text: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"**[{ts}]** `{event}` (miniapp)\n"]
    for line in (text or "").strip().splitlines():
        lines.append(f"> {line}\n")
    lines.append("\n")
    return "".join(lines)


def _session_transcript_header() -> str:
    return (
        "# SESSION TRANSCRIPT\n\n"
        "> Raw conversation log for operator continuity. Not part of the Record. "
        "Approved content is written to SELF-ARCHIVE on merge.\n\n---\n\n"
    )


def _append_to_session_transcript(blocks: str) -> None:
    """Append exchange to session-transcript.md (real-time log). self-archive.md is gated (merge only)."""
    try:
        SESSION_TRANSCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not SESSION_TRANSCRIPT_PATH.exists():
            SESSION_TRANSCRIPT_PATH.write_text(_session_transcript_header(), encoding="utf-8")
        with SESSION_TRANSCRIPT_PATH.open("a", encoding="utf-8") as f:
            f.write(blocks.strip() + "\n\n")
    except Exception as e:
        logger.warning("Session transcript write error: %s", e)


def _archive_miniapp(user_message: str, reply: str, is_lookup: bool = False, lookup_question: str | None = None) -> None:
    """Append exchange to session-transcript.md (same policy as bot: real-time log; self-archive.md only on merge). Runs in background."""
    blocks = _format_archive_block("USER", user_message)
    if is_lookup and lookup_question:
        blocks += _format_archive_block("LOOKUP REQUEST", lookup_question)
    blocks += _format_archive_block("GRACE-MAR (lookup)" if is_lookup else "GRACE-MAR", reply)

    def _run():
        _append_to_session_transcript(blocks)

    threading.Thread(target=_run, daemon=True).start()


def _is_affirmative(text: str) -> bool:
    normalized = text.strip().lower().rstrip("!.,")
    return normalized in AFFIRMATIVE_WORDS or any(p in normalized for p in AFFIRMATIVE_PHRASES)


def _last_user_message_before(history: list, before_index: int) -> str | None:
    """Return the last user message before the given index."""
    for i in range(before_index - 1, -1, -1):
        if history[i].get("role") == "user":
            return (history[i].get("content") or "").strip()
    return None


def _should_run_lookup(message: str, history: list) -> str | None:
    """If this is an affirmative follow-up to a lookup offer, return the question to look up."""
    if not history or len(history) < 2:
        return None
    last = history[-1]
    if last.get("role") != "assistant":
        return None
    last_content = (last.get("content") or "").strip()
    if LOOKUP_TRIGGER not in last_content.lower():
        return None
    if not _is_affirmative(message):
        return None
    question = _last_user_message_before(history, len(history))
    return question if question else None


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():
    """Receive Telegram updates. Only active when TELEGRAM_BOT_TOKEN is set."""
    if _telegram_app is None or _telegram_loop is None:
        return "", 200  # Silently ignore if webhook not configured
    try:
        data = request.get_json()
        if not data:
            return "", 400
        from telegram import Update

        update = Update.de_json(data, _telegram_app.bot)
        asyncio.run_coroutine_threadsafe(
            _telegram_app.update_queue.put(update), _telegram_loop
        ).result(timeout=5.0)
    except Exception as e:
        logger.exception("Telegram webhook error: %s", e)
        return "", 500
    return "", 200


@app.route("/manifest.json")
def manifest():
    """PWA manifest — served with correct MIME type."""
    return send_from_directory("miniapp", "manifest.json", mimetype="application/manifest+json")


@app.route("/service-worker.js")
def service_worker():
    """PWA service worker."""
    return send_from_directory("miniapp", "service-worker.js", mimetype="application/javascript")


@app.before_request
def _https_redirect():
    """Redirect HTTP to HTTPS in production when FORCE_HTTPS=1 (e.g. behind reverse proxy)."""
    if os.getenv("FORCE_HTTPS", "").lower() not in ("1", "true", "yes"):
        return None
    if request.is_secure:
        return None
    if request.headers.get("X-Forwarded-Proto") == "https":
        return None
    return redirect(request.url.replace("http://", "https://", 1), code=301)


@app.route("/")
def index():
    """Q&A Mini App — interactive chat with Grace-Mar."""
    return send_from_directory("miniapp", "index.html")


@app.route("/operator/console")
def operator_console():
    """Operator console: submit observations, upload artifacts, review gate, view timeline. No markdown on critical path."""
    return send_from_directory("miniapp", "operator-console.html")


@app.route("/operator/inbox")
def operator_inbox():
    """Browser review surface for RECURSION-GATE."""
    return send_from_directory("miniapp", "operator-inbox.html")


@app.route("/operator/wap")
def operator_wap():
    """Browser ops surface for work-politics."""
    return send_from_directory("miniapp", "operator-wap.html")


@app.route("/i/<token>")
def interview_by_token(token: str):
    """Shareable interview link — reviewer chats with fork, exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.route("/me/<user_id>")
def interview_by_user(user_id: str):
    """Per-user interview link (e.g. /me/grace-mar). Exchanges not archived."""
    return send_from_directory("miniapp", "index.html")


@app.route("/app")
def family_hub():
    """Family hub: chat, log activity, parent-gated review. Bookmark with ?t=<FAMILY_APP_TOKEN>."""
    return send_from_directory("miniapp", "family-hub.html")


@app.after_request
def _cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Family-Token, X-Wap-Token"
    return resp


def _operator_auth():
    """Require Bearer token matching OPERATOR_FETCH_SECRET. Return (ok, error_response)."""
    if not OPERATOR_FETCH_SECRET:
        return False, (jsonify({"error": "OPERATOR_FETCH_SECRET not configured"}), 503)
    auth = request.headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        return False, (jsonify({"error": "Authorization: Bearer <secret> required"}), 401)
    token = auth[7:].strip()
    if token != OPERATOR_FETCH_SECRET:
        return False, (jsonify({"error": "Invalid secret"}), 403)
    return True, None


def _wap_jobs_path() -> Path:
    raw = os.getenv("WAP_JOBS_PATH", "").strip()
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (REPO_ROOT / p)
    return REPO_ROOT / "data" / "wap_jobs.json"


def _wap_load_jobs() -> list[dict]:
    path = _wap_jobs_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        logger.exception("wap jobs load failed")
        return []


def _wap_save_jobs(jobs: list[dict]) -> None:
    path = _wap_jobs_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    tmp.replace(path)


def _wap_auth():
    """Require dashboard token (env WAP_DASHBOARD_TOKEN) via Bearer or X-Wap-Token."""
    if not WAP_DASHBOARD_TOKEN:
        return False, (jsonify({"error": "WAP_DASHBOARD_TOKEN not configured"}), 503)
    auth = (request.headers.get("Authorization") or "").strip()
    header_tok = (request.headers.get("X-Wap-Token") or "").strip()
    if auth.startswith("Bearer "):
        token = auth[7:].strip()
    else:
        token = header_tok
    if not token or token != WAP_DASHBOARD_TOKEN:
        return False, (jsonify({"error": "X-Wap-Token or Authorization: Bearer required"}), 401)
    return True, None


@app.route("/wap")
def wap_dashboard():
    """Internal work-politics job tracker for SMM + operator. Token on API; bookmark /wap?t=..."""
    return send_from_directory("miniapp", "wap-dashboard.html")


@app.route("/api/wap/jobs", methods=["GET", "POST", "OPTIONS"])
def wap_jobs():
    if request.method == "OPTIONS":
        return "", 204
    ok, err = _wap_auth()
    if not ok:
        return err
    if request.method == "GET":
        limit = min(int(request.args.get("limit") or 100), 500)
        jobs = _wap_load_jobs()
        jobs.sort(key=lambda j: j.get("created_at") or "", reverse=True)
        return jsonify({"jobs": jobs[:limit]})
    payload = request.get_json(silent=True) or {}
    client_slug = (payload.get("client_slug") or "").strip()
    workflow = (payload.get("workflow") or "").strip()
    if not client_slug or not workflow:
        return jsonify({"error": "client_slug and workflow required"}), 400
    now = datetime.now(timezone.utc).isoformat()
    job = {
        "id": f"wap-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(4)}",
        "created_at": now,
        "updated_at": now,
        "client_slug": client_slug,
        "workflow": workflow,
        "context": (payload.get("context") or "").strip(),
        "urls": (payload.get("urls") or "").strip(),
        "status": "new",
        "output": "",
    }
    jobs = _wap_load_jobs()
    jobs.append(job)
    _wap_save_jobs(jobs)
    return jsonify({"job": job}), 201


@app.route("/api/wap/jobs/<job_id>", methods=["PATCH", "OPTIONS"])
def wap_job_patch(job_id: str):
    if request.method == "OPTIONS":
        return "", 204
    ok, err = _wap_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    jobs = _wap_load_jobs()
    found = None
    for i, j in enumerate(jobs):
        if j.get("id") == job_id:
            found = i
            break
    if found is None:
        return jsonify({"error": "job not found"}), 404
    job = dict(jobs[found])
    if "status" in payload:
        job["status"] = str(payload["status"]).strip() or job["status"]
    if "output" in payload:
        job["output"] = str(payload["output"])
    if "context" in payload:
        job["context"] = str(payload["context"])
    if "urls" in payload:
        job["urls"] = str(payload["urls"])
    job["updated_at"] = datetime.now(timezone.utc).isoformat()
    jobs[found] = job
    _wap_save_jobs(jobs)
    return jsonify({"job": job})


@app.route("/operator/session-transcript", methods=["GET"])
def operator_session_transcript():
    """Return session-transcript.md content for operator sync (e.g. into Cursor). Requires OPERATOR_FETCH_SECRET."""
    ok, err = _operator_auth()
    if not ok:
        return err
    if not SESSION_TRANSCRIPT_PATH.exists():
        return jsonify({"error": "session-transcript.md not found", "path": str(SESSION_TRANSCRIPT_PATH)}), 404
    return SESSION_TRANSCRIPT_PATH.read_text(encoding="utf-8"), 200, {"Content-Type": "text/markdown; charset=utf-8"}


@app.route("/operator/recursion-gate", methods=["GET"])
def operator_recursion_gate():
    """Return recursion-gate.md content for operator sync. Requires OPERATOR_FETCH_SECRET."""
    ok, err = _operator_auth()
    if not ok:
        return err
    if not RECURSION_GATE_PATH.exists():
        return jsonify({"error": "recursion-gate.md not found", "path": str(RECURSION_GATE_PATH)}), 404
    return RECURSION_GATE_PATH.read_text(encoding="utf-8"), 200, {"Content-Type": "text/markdown; charset=utf-8"}


@app.route("/operator/observations", methods=["POST"])
def operator_observations():
    """Submit an observation (same pipeline as 'we did X'). Stages to RECURSION-GATE; no markdown editing."""
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text required"}), 400
    channel_key = "operator:console"
    try:
        staged = analyze_activity_report(text, channel_key)
    except Exception as e:
        logger.exception("analyze_activity_report failed")
        return jsonify({"error": str(e), "staged": False}), 500
    pending = get_pending_candidates()
    count = len(pending)
    if staged:
        emit_pipeline_event("dyad:activity_report", None, channel_key=channel_key, replay_mode="dyad")
        message = f"Added to your record. You have {count} thing{'s' if count != 1 else ''} to review."
    else:
        message = f"Nothing new to add right now. You have {count} in review."
    return jsonify({
        "ok": True,
        "staged": staged,
        "pending_count": count,
        "message": message,
    })


@app.route("/operator/artifacts", methods=["POST"])
def operator_artifacts():
    """Upload a file to users/<id>/artifacts/ and optionally submit an observation. No markdown editing."""
    ok, err = _operator_auth()
    if not ok:
        return err
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "file required"}), 400
    # Safe filename: keep extension, sanitize name
    base = re.sub(r"[^\w.\-]", "_", file.filename)[:120]
    if not base:
        base = "upload"
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = ARTIFACTS_DIR / base
    try:
        file.save(str(dest))
    except Exception as e:
        logger.exception("artifact save failed")
        return jsonify({"error": str(e)}), 500
    rel_path = f"artifacts/{base}"
    observation = (request.form.get("observation") or "").strip()
    text = f"we added an artifact: {base}. {observation}" if observation else f"we added an artifact: {base}."
    channel_key = "operator:console"
    staged = False
    try:
        staged = analyze_activity_report(text, channel_key, staging_meta={"artifact_path": rel_path})
        if staged:
            emit_pipeline_event("dyad:activity_report", None, channel_key=channel_key, replay_mode="dyad")
    except Exception as e:
        logger.warning("artifact observation staging failed: %s", e)
    pending = len(get_pending_candidates())
    return jsonify({
        "ok": True,
        "path": rel_path,
        "staged": staged,
        "pending_count": pending,
        "message": f"Saved {base}. " + (f"{pending} in review." if staged else "Nothing new to add to profile."),
    })


def _timeline_events(limit: int = 50) -> list[dict]:
    """Read pipeline-events.jsonl and return last events for fork timeline (read-only)."""
    out = []
    if not PIPELINE_EVENTS_PATH.exists():
        return out
    lines = []
    try:
        with PIPELINE_EVENTS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
    except Exception:
        return out
    for line in lines[-limit:]:
        try:
            data = json.loads(line)
            ts = data.get("ts") or ""
            event = data.get("event") or ""
            summary = event
            if data.get("candidate_id"):
                summary = f"{event} {data.get('candidate_id')}"
            if data.get("evidence_id"):
                summary += f" → {data['evidence_id']}"
            out.append({
                "ts": ts,
                "event": event,
                "candidate_id": data.get("candidate_id"),
                "evidence_id": data.get("evidence_id"),
                "channel_key": data.get("channel_key"),
                "summary": summary,
            })
        except (json.JSONDecodeError, TypeError):
            continue
    return out


@app.route("/operator/timeline", methods=["GET"])
def operator_timeline():
    """Return recent pipeline events for fork timeline (read-only). No markdown editing."""
    ok, err = _operator_auth()
    if not ok:
        return err
    limit = min(int(request.args.get("limit", 50)), 100)
    events = _timeline_events(limit=limit)
    return jsonify({"user_id": USER_ID, "events": events, "count": len(events)})


@app.route("/operator/gate-candidates", methods=["GET"])
def operator_gate_candidates():
    """Return structured review candidates for the approval inbox."""
    ok, err = _operator_auth()
    if not ok:
        return err
    rows = parse_review_candidates(USER_ID)
    rows = filter_review_candidates(
        rows,
        status=(request.args.get("status") or "").strip(),
        risk_tier=(request.args.get("risk_tier") or "").strip(),
        territory=(request.args.get("territory") or "").strip(),
    )
    return jsonify({"user_id": USER_ID, "count": len(rows), "items": rows})


@app.route("/operator/wap-status", methods=["GET"])
def operator_wap_status():
    """Return structured work-politics operator state."""
    ok, err = _operator_auth()
    if not ok:
        return err
    return jsonify(get_wap_snapshot(USER_ID))


@app.route("/operator/wap-brief", methods=["GET"])
def operator_wap_brief():
    """Return a generated weekly brief scaffold for work-politics."""
    ok, err = _operator_auth()
    if not ok:
        return err
    start = (request.args.get("start") or "").strip()
    brief = build_wap_weekly_brief(start_text=start, user_id=USER_ID)
    return brief, 200, {"Content-Type": "text/markdown; charset=utf-8"}


@app.route("/operator/gate-candidates/<candidate_id>/action", methods=["POST"])
def operator_gate_candidate_action(candidate_id: str):
    """Apply review actions while keeping recursion-gate.md canonical."""
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").strip().lower()
    if action not in {"approve", "reject", "defer", "quick_merge"}:
        return jsonify({"error": "action must be approve, reject, defer, or quick_merge"}), 400

    row = get_review_candidate(USER_ID, candidate_id)
    if not row:
        return jsonify({"error": f"{candidate_id} not found above ## Processed"}), 404

    channel_key = "operator:web"
    source = "miniapp_server:approval_inbox"
    rejection_reason = (payload.get("rejection_reason") or "").strip() or None

    if action == "approve":
        if row.get("status") != "approved":
            changed = update_candidate_status(
                candidate_id,
                "approved",
                channel_key=channel_key,
                actor=OPERATOR_NAME,
                source=source,
            )
            if not changed:
                return jsonify({"error": f"could not approve {candidate_id}"}), 409
        return jsonify({"ok": True, "action": action, "candidate": get_review_candidate(USER_ID, candidate_id)})

    if action == "reject":
        changed = update_candidate_status(
            candidate_id,
            "rejected",
            rejection_reason=rejection_reason,
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
        )
        if not changed:
            return jsonify({"error": f"could not reject {candidate_id}"}), 409
        return jsonify({"ok": True, "action": action, "candidate": get_review_candidate(USER_ID, candidate_id)})

    if action == "defer":
        emit_pipeline_event(
            "review_feedback",
            candidate_id,
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
            decision="defer",
            replay_mode="gate",
        )
        return jsonify({"ok": True, "action": action, "candidate": row})

    if not is_low_risk_candidate(candidate_id):
        return jsonify({"error": f"{candidate_id} is not quick-merge eligible"}), 409
    if row.get("status") == "pending":
        changed = update_candidate_status(
            candidate_id,
            "approved",
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
        )
        if not changed:
            return jsonify({"error": f"could not approve {candidate_id} before quick merge"}), 409
    merged_ok, message = quick_merge_candidate(candidate_id, OPERATOR_NAME)
    if not merged_ok:
        return jsonify({"error": message}), 500
    emit_pipeline_event(
        "review_feedback",
        candidate_id,
        channel_key=channel_key,
        actor=OPERATOR_NAME,
        source=source,
        decision="quick_merge",
        replay_mode="gate",
    )
    return jsonify({"ok": True, "action": action, "message": message, "candidate_id": candidate_id})


@app.route("/operator/gate-candidates/merge-approved", methods=["POST"])
def operator_merge_approved():
    """
    Merge all approved candidates (above ## Processed, status approved) into SELF/EVIDENCE/prompt.
    Uses receipt + process_approved_candidates --apply (same as CLI). Default territory=companion (family MVP).
    """
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    territory = (payload.get("territory") or "companion").strip().lower()
    if territory not in ("companion", "wap", "all"):
        return jsonify({"error": "territory must be companion, wap, or all"}), 400

    pac._set_user(USER_ID)
    approved = pac.get_approved_in_candidates()
    if territory == "wap":
        approved = [c for c in approved if territory_from_yaml_block(c["block"]) == TERRITORY_WAP]
    elif territory == "companion":
        approved = [c for c in approved if territory_from_yaml_block(c["block"]) != TERRITORY_WAP]

    if not approved:
        return jsonify({
            "ok": True,
            "merged": 0,
            "message": f"No approved candidates waiting to merge (territory={territory}).",
        })

    receipt = pac._build_receipt(approved, OPERATOR_NAME, territory if territory != "all" else "all")
    receipt["min_evidence_tier"] = max(
        int(receipt.get("min_evidence_tier", pac.MIN_EVIDENCE_TIER)),
        pac.MIN_EVIDENCE_TIER,
    )

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = ARTIFACTS_DIR / ".merge-receipt-temp.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "process_approved_candidates.py"),
                "-u",
                USER_ID,
                "--apply",
                "--receipt",
                str(receipt_path),
                "--approved-by",
                OPERATOR_NAME,
                "--territory",
                territory,
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600,
        )
    finally:
        receipt_path.unlink(missing_ok=True)

    if result.returncode != 0:
        err_text = (result.stderr or result.stdout or "merge failed").strip()
        if len(err_text) > 3000:
            err_text = err_text[-3000:]
        logger.warning("merge-approved failed: %s", err_text)
        return jsonify({"error": err_text, "exit_code": result.returncode}), 500

    ids = [c["id"] for c in approved]
    emit_pipeline_event(
        "operator_merge_approved_batch",
        None,
        channel_key="operator:web",
        actor=OPERATOR_NAME,
        source="miniapp_server:merge_approved",
        territory=territory,
        merged_count=len(ids),
        replay_mode="merge",
    )
    return jsonify({
        "ok": True,
        "merged": len(approved),
        "candidate_ids": ids,
        "message": f"Merged {len(approved)} candidate(s) into the Record (territory={territory}).",
    })


@app.route("/operator/gate-candidates/batch-action", methods=["POST"])
def operator_gate_candidates_batch_action():
    """Batch approve or reject candidates. Emits one pipeline event per candidate."""
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").strip().lower()
    if action not in {"approve", "reject"}:
        return jsonify({"error": "action must be approve or reject"}), 400
    candidate_ids = payload.get("candidate_ids")
    if not isinstance(candidate_ids, list) or not candidate_ids:
        return jsonify({"error": "candidate_ids must be a non-empty list"}), 400
    candidate_ids = [str(x).strip() for x in candidate_ids if str(x).strip()]
    if not candidate_ids:
        return jsonify({"error": "candidate_ids must contain at least one id"}), 400
    rejection_reason = (payload.get("rejection_reason") or "").strip() or None
    channel_key = "operator:web"
    source = "miniapp_server:approval_inbox"
    results = []
    for cid in candidate_ids:
        row = get_review_candidate(USER_ID, cid)
        if not row:
            results.append({"id": cid, "ok": False, "error": "not found above ## Processed"})
            continue
        if action == "approve" and row.get("status") == "approved":
            results.append({"id": cid, "ok": True, "skipped": "already approved"})
            continue
        if action == "reject" and row.get("status") == "rejected":
            results.append({"id": cid, "ok": True, "skipped": "already rejected"})
            continue
        new_status = "approved" if action == "approve" else "rejected"
        changed = update_candidate_status(
            cid,
            new_status,
            rejection_reason=rejection_reason if action == "reject" else None,
            channel_key=channel_key,
            actor=OPERATOR_NAME,
            source=source,
        )
        if changed:
            results.append({"id": cid, "ok": True})
        else:
            results.append({"id": cid, "ok": False, "error": "status update failed"})
    return jsonify({"ok": True, "action": action, "results": results})


@app.route("/operator/gate-candidates/generate-receipt", methods=["POST"])
def operator_gate_candidates_generate_receipt():
    """Generate a merge receipt for the given approved candidate IDs. Does not apply merge."""
    ok, err = _operator_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    candidate_ids = payload.get("candidate_ids")
    if not isinstance(candidate_ids, list) or not candidate_ids:
        return jsonify({"error": "candidate_ids must be a non-empty list"}), 400
    candidate_ids = sorted({str(x).strip() for x in candidate_ids if str(x).strip()})
    if not candidate_ids:
        return jsonify({"error": "candidate_ids must contain at least one id"}), 400
    pac._set_user(USER_ID)
    approved = pac.get_approved_in_candidates()
    requested = [c for c in approved if c["id"] in candidate_ids]
    missing = [cid for cid in candidate_ids if cid not in (c["id"] for c in requested)]
    if missing:
        return jsonify({
            "error": "some ids are not approved or not found",
            "missing": missing,
            "hint": "Only approved candidates above ## Processed can be included",
        }), 400
    receipt = pac._build_receipt(requested, OPERATOR_NAME, "all")
    receipt["min_evidence_tier"] = max(getattr(pac, "MIN_EVIDENCE_TIER", 3), receipt.get("min_evidence_tier", 3))
    apply_cmd = (
        f"python3 scripts/process_approved_candidates.py -u {USER_ID} --apply --receipt <path> --approved-by {OPERATOR_NAME!r}"
    )
    return jsonify({
        "ok": True,
        "receipt": receipt,
        "apply_command": apply_cmd,
        "candidate_count": len(requested),
    })


def _process_ask_body(data: dict, channel_key: str, archive: bool) -> dict:
    """Run ask flow; channel_key for grounded/lookup (e.g. miniapp, web:family)."""
    if not OPENAI_API_KEY:
        return {"_error": ("OPENAI_API_KEY not configured", 500)}
    message = (data.get("message") or "").strip()
    if not message:
        return {"_error": ("message required", 400)}
    history = data.get("history") or []
    grounded = data.get("mode") == "grounded"
    interview = data.get("interview") is True
    ck = "interview" if interview else channel_key
    if grounded:
        reply = run_grounded_response(message, channel_key=ck, history=history)
        if archive and not interview:
            _archive_miniapp(message, reply, is_lookup=False)
        return {"response": reply}
    question = _should_run_lookup(message, history)
    if question:
        reply = run_lookup(question, channel_key=channel_key)
        if archive and not interview:
            _archive_miniapp(message, reply, is_lookup=True, lookup_question=question)
        return {"response": reply}
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history:
        role = h.get("role")
        content = (h.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.9,
    )
    reply = response.choices[0].message.content.strip()
    if archive and not interview:
        _archive_miniapp(message, reply, is_lookup=False)
    return {"response": reply}


@app.route("/api/family/activity", methods=["POST", "OPTIONS"])
def family_activity():
    if request.method == "OPTIONS":
        return "", 204
    ok, err = _family_auth()
    if not ok:
        return err
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text required"}), 400
    if not re.match(r"(?i)^we\s+", text):
        text = "we did " + text.lstrip()
    channel_key = "web:family"
    try:
        staged = analyze_activity_report(text, channel_key)
    except Exception as e:
        logger.exception("family analyze_activity_report failed")
        return jsonify({"error": str(e), "staged": False}), 500
    pending = get_pending_candidates()
    count = len(pending)
    if staged:
        emit_pipeline_event("dyad:activity_report", None, channel_key=channel_key, replay_mode="dyad")
    return jsonify({
        "ok": True,
        "staged": staged,
        "pending_count": count,
        "message": "Sent for review." if staged else "Nothing new to add right now.",
    })


@app.route("/api/family/pending-count", methods=["GET", "OPTIONS"])
def family_pending_count():
    if request.method == "OPTIONS":
        return "", 204
    ok, err = _family_auth()
    if not ok:
        return err
    pending = get_pending_candidates()
    return jsonify({"pending_count": len(pending), "user_id": USER_ID})


@app.route("/api/family/ask", methods=["POST", "OPTIONS"])
def family_ask():
    if request.method == "OPTIONS":
        return "", 204
    ok, err = _family_auth()
    if not ok:
        return err
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY not configured"}), 500
    data = request.get_json() or {}
    try:
        out = _process_ask_body(data, channel_key="web:family", archive=True)
        if "_error" in out:
            msg, code = out["_error"]
            return jsonify({"error": msg}), code
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return "", 204
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY not configured"}), 500
    data = request.get_json() or {}
    try:
        out = _process_ask_body(data, channel_key="miniapp", archive=True)
        if "_error" in out:
            msg, code = out["_error"]
            return jsonify({"error": msg}), code
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and WEBHOOK_BASE_URL:
        _start_telegram_webhook()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
