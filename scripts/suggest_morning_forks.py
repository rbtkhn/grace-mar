#!/usr/bin/env python3
"""
Deterministic ranked "morning forks" for the operator — gate, WORK lanes, warmup.

Composes signals from recursion-gate, pipeline-events, self-memory tail, and
session-log tail (same family as session_brief.py). No Record writes; stdout only.

Optional: --llm re-orders top candidates with one-line rationales (OPENAI_API_KEY).
LLM output is advisory; deterministic ranking is always computed first.

Usage:
  python3 scripts/suggest_morning_forks.py -u grace-mar
  python3 scripts/suggest_morning_forks.py -u grace-mar --top 5 --markdown
  python3 scripts/suggest_morning_forks.py -u grace-mar --llm   # optional API
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID, profile_dir, read_path, resolve_self_memory_path  # noqa: E402
from session_brief import (  # noqa: E402
    _load_pipeline_events,
    _oldest_pending_age_days,
    _pending_count_full,
    _read,
)


def _session_log_tail(user_dir: Path, max_chars: int = 1500) -> str:
    p = user_dir / "session-log.md"
    if not p.is_file():
        return ""
    raw = read_path(p)
    return raw[-max_chars:] if len(raw) > max_chars else raw


def _memory_tail(user_dir: Path, max_chars: int = 2500) -> str:
    mp = resolve_self_memory_path(user_dir)
    if not mp.is_file():
        return ""
    raw = read_path(mp)
    return raw[-max_chars:] if len(raw) > max_chars else raw


def _score_keyword(text: str, *words: str) -> int:
    low = text.lower()
    return sum(1 for w in words if w.lower() in low)


def build_fork_scores(user_id: str) -> list[tuple[float, str, str, str]]:
    """
    Return list of (score, fork_id, title, rationale_one_line).
    """
    user_dir = profile_dir(user_id)
    pr = _read(user_dir / "recursion-gate.md")
    events = _load_pipeline_events(user_dir)
    pending_all = _pending_count_full(pr, "all")
    pending_wp = _pending_count_full(pr, "work-politics")
    oldest = _oldest_pending_age_days(pr, events)
    mem = _memory_tail(user_dir)
    slog = _session_log_tail(user_dir)
    blob = f"{mem}\n{slog}"

    forks: list[tuple[float, str, str, str]] = []

    # 1 — Gate / pipeline
    gscore = min(12.0, float(pending_all) * 1.8)
    if oldest is not None:
        if oldest >= 7:
            gscore += 5.0
        elif oldest >= 3:
            gscore += 3.0
        elif oldest >= 1:
            gscore += 1.0
    why_g = f"{pending_all} pending in gate"
    if oldest is not None:
        why_g += f"; oldest staged ~{oldest}d"
    if pending_all == 0:
        why_g = "Gate clear — light merge check or staging only"
        gscore = 1.5
    forks.append((gscore, "gate", "Gate + pipeline — review / merge rhythm", why_g))

    # 2 — Operator cadence + brief (always relevant)
    wscore = 4.0 + _score_keyword(blob, "good morning", "warmup", "brief", "polling")
    forks.append(
        (
            float(wscore),
            "warmup",
            "Operator cadence stack — harness + operator_daily_warmup + brief",
            "Fixed coffee session shape; see .cursor/skills/coffee/SKILL.md",
        )
    )

    # 3 — WORK-dev
    dscore = 3.0 + 2.0 * _score_keyword(
        blob, "work-dev", "work_dev", "integration", "continuity", "handback"
    )
    forks.append(
        (
            float(dscore),
            "work_dev",
            "WORK-dev — continuity, sources, integration",
            "High signal when memory/session mentions integration or work-dev",
        )
    )

    # 4 — WORK-strategy
    sscore = 3.0 + 2.0 * _score_keyword(
        blob, "work-strategy", "strategy", "putin", "daily-brief", "geo", "civ-mem"
    )
    forks.append(
        (
            float(sscore),
            "work_strategy",
            "WORK-strategy — daily brief, focus, Putin watch",
            "docs/skill-work/work-strategy/ + generate_work_politics_daily_brief.py",
        )
    )

    # 5 — WORK-politics
    pscore = 2.5 + min(6.0, float(pending_wp) * 1.2)
    pscore += 2.0 * _score_keyword(blob, "massie", "ky-4", "campaign", "wap", "politics")
    forks.append(
        (
            float(pscore),
            "work_politics",
            "WORK-politics — polling, campaign, Massie lane",
            f"{pending_wp} work-politics pending" if pending_wp else "Content queue + polling docs",
        )
    )

    # 6 — Companion / Record session (session_brief family)
    cscore = 2.0 + _score_keyword(blob, "tutor", "grace-mar", "session", "ix-b", "curiosity")
    forks.append(
        (
            float(cscore),
            "companion",
            "Companion session — brief, wisdom, tutoring thread",
            "python3 scripts/session_brief.py -u "
            + user_id
            + " for full snapshot",
        )
    )

    forks.sort(key=lambda x: -x[0])
    return forks


def _llm_rerank(
    user_id: str,
    candidates: list[tuple[float, str, str, str]],
    top_n: int,
    model: str,
) -> list[tuple[float, str, str, str]] | None:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    try:
        import urllib.error
        import urllib.request
    except ImportError:
        return None

    subset = candidates[: min(6, len(candidates))]
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You reorder operator morning work forks. Output ONLY valid JSON: "
                    '{"order":["fork_id",...],"rationales":{"fork_id":"one short line",...}} '
                    "Pick exactly min(3, len(candidates)) ids from the list. "
                    "Rationales must be one line each, no markdown."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "user_id": user_id,
                        "candidates": [
                            {"id": fid, "title": title, "score": sc, "deterministic_why": why}
                            for sc, fid, title, why in subset
                        ],
                    }
                ),
            },
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return None
    try:
        txt = data["choices"][0]["message"]["content"].strip()
        m = re.search(r"\{[\s\S]*\}", txt)
        if not m:
            return None
        parsed = json.loads(m.group(0))
        order = parsed.get("order") or []
        rationales = parsed.get("rationales") or {}
        by_id = {fid: (sc, t, w) for sc, fid, t, w in subset}
        out: list[tuple[float, str, str, str]] = []
        for i, fid in enumerate(order[:top_n]):
            if fid not in by_id:
                continue
            sc, title, why0 = by_id[fid]
            why = rationales.get(fid) or why0
            out.append((float(top_n - i), fid, title, f"[LLM] {why}"))
        if len(out) >= min(3, top_n):
            return out
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        pass
    return None


def format_markdown(
    ranked: list[tuple[float, str, str, str]],
    *,
    top: int,
    user_id: str,
) -> str:
    lines = [
        f"# Ranked morning forks — `{user_id}`",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC_",
        "",
    ]
    for i, (_sc, _fid, title, why) in enumerate(ranked[:top], 1):
        lines.append(f"{i}. **{title}**")
        lines.append(f"   - _Why now:_ {why}")
        lines.append("")
    lines.extend(
        [
            "---",
            "",
            "**Commands (examples)**",
            "",
            f"- `python3 scripts/harness_warmup.py -u {user_id}`",
            f"- `python3 scripts/operator_daily_warmup.py -u {user_id}`",
            f"- `python3 scripts/session_brief.py -u {user_id} --minimal`",
            f"- `python3 scripts/log_operator_choice.py -u {user_id} --context GOOD_MORNING --picked 1`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID)
    ap.add_argument("--top", type=int, default=3, help="How many forks to show (default 3)")
    ap.add_argument("--markdown", action="store_true", help="Markdown output with command hints")
    ap.add_argument(
        "--llm",
        action="store_true",
        help="Optional OpenAI re-rank + rationale (requires OPENAI_API_KEY)",
    )
    ap.add_argument(
        "--llm-model",
        default=os.getenv("OPENAI_ANALYST_MODEL", "gpt-4o-mini"),
        help="Model for --llm (default OPENAI_ANALYST_MODEL or gpt-4o-mini)",
    )
    ap.add_argument("-o", "--output", default="", help="Write markdown to this path (implies --markdown)")
    args = ap.parse_args()
    uid = args.user.strip()
    top = max(1, min(6, args.top))

    ranked = build_fork_scores(uid)
    if args.llm:
        reranked = _llm_rerank(uid, ranked, top_n=top, model=args.llm_model.strip())
        if reranked:
            ranked = reranked + [x for x in ranked if x[1] not in {r[1] for r in reranked}]

    use_md = args.markdown or bool(args.output)
    if use_md:
        text = format_markdown(ranked, top=top, user_id=uid)
        if args.output:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
            print(out)
        else:
            print(text)
    else:
        print(f"Ranked morning forks for {uid} (top {top}):")
        for i, (sc, fid, title, why) in enumerate(ranked[:top], 1):
            print(f"  {i}. [{fid}] (score {sc:.1f}) {title}")
            print(f"      {why}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
