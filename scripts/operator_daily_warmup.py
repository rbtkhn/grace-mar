#!/usr/bin/env python3
"""
Generate a compact daily operator warmup for Grace-Mar.

This is an operator workflow surface. It summarizes continuity state,
Work-politics status, repo integrity, and local worktree noise without changing
the Record or processing the gate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from fork_config import load_fork_config
    from harness_warmup import _last_activity_oneliner, _pending_candidates, _read, _session_lines_tail
    from operator_depth_hint import velocity_oneliner
    from work_politics_ops import get_work_politics_snapshot
except ImportError:
    from scripts.fork_config import load_fork_config
    from scripts.harness_warmup import _last_activity_oneliner, _pending_candidates, _read, _session_lines_tail
    from scripts.operator_depth_hint import velocity_oneliner
    from scripts.work_politics_ops import get_work_politics_snapshot

try:
    from context_budget import get_bool, get_int, load_context_budget
except ImportError:
    from scripts.context_budget import get_bool, get_int, load_context_budget

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from dream_execution_paths import format_tomorrow_inherits_line
except ImportError:
    from scripts.dream_execution_paths import format_tomorrow_inherits_line

try:
    from work_jiang.warmup_jiang_pulse import build_morning_pulse_lines
except ImportError:
    build_morning_pulse_lines = None  # type: ignore[misc, assignment]

LAST_DREAM_FILENAME = "last-dream.json"


def _compress_lines(lines: list[str], *, max_lines: int) -> list[str]:
    """Truncate body lines; max_lines <= 0 means no compression."""
    if max_lines <= 0 or len(lines) <= max_lines:
        return list(lines)
    kept = lines[: max_lines - 1]
    overflow = len(lines) - (max_lines - 1)
    kept.append(f"(+{overflow} more line(s) omitted)")
    return kept


def _coffee_context_budget() -> dict:
    return load_context_budget("coffee")


def _read_last_dream(user_dir: Path) -> dict | None:
    path = user_dir / LAST_DREAM_FILENAME
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _agent_surface_line_from_dream(dream: dict) -> str | None:
    """One bullet matching bridge/harvest Agent surface when handoff recorded a model."""
    surf = dream.get("agent_surface")
    if not isinstance(surf, dict):
        return None
    raw = str(surf.get("cursor_model") or "").strip()
    if not raw:
        return None
    display = raw if len(raw) <= 160 else raw[:159] + "…"
    return f"- Agent surface: **Cursor model:** {display}"


def _format_last_dream_block(
    dream: dict,
    *,
    verbose_dream: bool = False,
    show_civ_mem: bool | None = None,
    show_rollup: bool | None = None,
) -> list[str]:
    """Summarize last night's dream handoff. Default is collapsed (~3 lines + header)."""
    coffee_budget = _coffee_context_budget()
    lines = [
        "## Last dream (night handoff)",
        "",
    ]
    ok = dream.get("ok", False)
    status = "pass" if ok else "**issues detected**"
    integ = "pass" if dream.get("integrity_ok") else "FAIL"
    gov = "pass" if dream.get("governance_ok") else "FAIL"
    rc = dream.get("reviewable_count", 0)
    cc = dream.get("contradiction_count", 0)
    tomorrow = str(dream.get("tomorrow_inherits") or "").strip()

    max_body = get_int(coffee_budget, "max_last_dream_lines", 12)
    if show_civ_mem is None:
        show_civ_mem = get_bool(coffee_budget, "show_civ_mem_by_default", False)
    if show_rollup is None:
        show_rollup = get_bool(coffee_budget, "show_rollup_by_default", False)

    if not verbose_dream:
        body: list[str] = []
        body.append(
            f"- Status: {status}; integrity: {integ}; governance: {gov}"
        )
        as_line = _agent_surface_line_from_dream(dream)
        if as_line:
            body.append(as_line)
        body.append(f"- Contradiction digest: reviewable={rc}, contradiction={cc}")
        tar = str(dream.get("topActionReason") or "").strip()
        if tar:
            body.append(
                f"- Top-action reason: {tar[:200]}{'…' if len(tar) > 200 else ''}"
            )
        wt = str(dream.get("worktreeState") or "").strip()
        if wt:
            wadv = str(dream.get("worktreeAdvice") or "").strip()
            body.append(
                f"- Worktree: {wt}"
                + (f" — {wadv[:140]}{'…' if len(wadv) > 140 else ''}" if wadv else "")
            )
        if show_rollup:
            cr = dream.get("coffee_rollup_24h")
            if isinstance(cr, dict):
                cnt = int(cr.get("count") or 0)
                modes = cr.get("by_mode") or {}
                mode_s = ", ".join(f"{k}={v}" for k, v in sorted(modes.items())) if modes else "—"
                body.append(f"- Coffee (24h rollup): {cnt} run(s); modes: {mode_s}")
        if tomorrow:
            body.append(f"- {tomorrow}")
        else:
            paths = dream.get("execution_paths") or []
            idx = int(dream.get("suggested_execution_path_index") or 0)
            reason = str(dream.get("execution_path_suggestion_reason") or "calendar_mod3")
            if (
                isinstance(paths, list)
                and paths
                and all(isinstance(x, dict) for x in paths)
            ):
                body.append(format_tomorrow_inherits_line(paths, idx, reason))
            else:
                body.append(
                    "- Tomorrow inherits: see `last-dream.json` or run warmup with `--verbose-dream`."
                )
        if show_civ_mem:
            suppressed = str(dream.get("civmem_suppressed_reason") or "").strip()
            if suppressed:
                body.append(f"- Civ-mem: suppressed ({suppressed}) — not Record.")
            else:
                echoes = dream.get("civmem_echoes") or []
                civ_missing = dream.get("civmem_index_missing")
                if civ_missing:
                    body.append(
                        "- Civ-mem: index missing (optional build) — no analogy echoes; not Record."
                    )
                elif isinstance(echoes, list) and echoes:
                    body.append(
                        f"- Civ-mem: {len(echoes)} analogy candidate(s) above overlap threshold — "
                        "not evidence or Record; use `--verbose-dream` for path/snippet."
                    )
                else:
                    body.append(
                        "- Civ-mem: no echoes above overlap threshold — not Record."
                    )
        body = _compress_lines(body, max_lines=max_body)
        lines.extend(body)
        lines.append("")
        return lines

    generated = dream.get("generated_at", "unknown")
    lines.append(f"- Ran: {generated}")
    as_line = _agent_surface_line_from_dream(dream)
    if as_line:
        lines.append(as_line)
    lines.append(f"- Status: {status}")
    lines.append(f"- Integrity: {integ}")
    lines.append(f"- Governance: {gov}")
    lines.append(f"- Self-memory changed: {dream.get('self_memory_changed', False)}")
    lines.append(f"- Contradiction digest: reviewable={rc}, contradiction={cc}")
    dc = dream.get("artifact_draft_count", 0)
    pc = dream.get("promotable_draft_count", 0)
    if dc:
        lines.append(f"- Artifact drafts: {pc}/{dc} promotable")

    cr = dream.get("coffee_rollup_24h")
    if isinstance(cr, dict):
        cnt = int(cr.get("count") or 0)
        modes = cr.get("by_mode") or {}
        by_picked = cr.get("by_picked") or {}
        mode_s = ", ".join(f"{k}={v}" for k, v in sorted(modes.items())) if modes else "—"
        picked_s = ""
        if by_picked:
            picked_s = "; menu picks: " + ", ".join(
                f"{k}={v}" for k, v in sorted(by_picked.items())
            )
        first = cr.get("first_ts") or "—"
        last = cr.get("last_ts") or "—"
        note = cr.get("note")
        extra = f" ({note})" if note else ""
        lines.append(
            f"- Coffee (24h rollup): {cnt} run(s); modes: {mode_s}{picked_s}; first={first} last={last}{extra}"
        )

    paths = dream.get("execution_paths")
    idx = int(dream.get("suggested_execution_path_index") or 0)
    if isinstance(paths, list) and paths:
        lines.append("")
        lines.append("**Execution paths (suggested uses integrity / gate backlog / calendar):**")
        for i, p in enumerate(paths):
            if not isinstance(p, dict):
                continue
            mark = " — **suggested tomorrow**" if i == idx else ""
            title = p.get("title") or p.get("id") or "path"
            fm = str(p.get("first_move") or "").strip()
            if fm:
                lines.append(f"- **{i + 1}.** {title}{mark}: `{fm}`")
            else:
                lines.append(f"- **{i + 1}.** {title}{mark}")
    if tomorrow:
        lines.append("")
        lines.append(f"- **Tomorrow inherits:** {tomorrow}")

    echoes = dream.get("civmem_echoes") or []
    disc = str(dream.get("civmem_disclaimer") or "").strip()
    if isinstance(echoes, list) and echoes:
        lines.append("")
        lines.append(f"**Civ-mem echoes:** {disc}")
        for e in echoes[:5]:
            if not isinstance(e, dict):
                continue
            ov = e.get("overlap", "")
            pth = e.get("path", "")
            lbl = str(e.get("analogy_label") or "").strip()
            lbl_s = f" — {lbl}" if lbl else ""
            lines.append(f"  - overlap={ov} `{pth}`{lbl_s}")

    followups = dream.get("followups") or []
    if followups:
        lines.append("")
        lines.append("**Follow-up from dream:**")
        for item in followups:
            lines.append(f"- {item}")
    lines.append("")
    return lines


def _git_status_lines() -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"git status failed: {proc.stderr.strip() or 'unknown error'}"]
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _integrity_errors(user_id: str) -> list[str]:
    proc = subprocess.run(
        ["python3", "scripts/validate-integrity.py", "--user", user_id, "--json"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode not in {0, 1}:
        return [f"integrity validator failed to run: {proc.stderr.strip() or 'unknown error'}"]
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return ["integrity validator returned invalid JSON"]
    errors = payload.get("errors")
    if not isinstance(errors, list):
        return ["integrity validator returned malformed payload"]
    return [str(item) for item in errors]


def _priority_list(
    *,
    pending_all: list[tuple[str, str]],
    pending_politics: list[tuple[str, str]],
    integrity_errors: list[str],
    politics_snapshot: dict[str, object],
    dirty_files: list[str],
) -> list[str]:
    priorities: list[str] = []
    if integrity_errors:
        priorities.append("Fix integrity failures before export or merge work.")
    if pending_all:
        priorities.append(
            f"Review {len(pending_all)} pending gate candidate(s) in `users/grace-mar/recursion-gate.md` before they go stale."
        )
    if pending_politics:
        priorities.append("Handle live work-politics gate items before creating more territory continuity.")

    blockers = politics_snapshot.get("territory_blockers") or []
    if blockers:
        first = blockers[0]
        if isinstance(first, dict) and first.get("action"):
            priorities.append(str(first["action"]))

    next_actions = politics_snapshot.get("next_actions") or []
    for action in next_actions:
        if isinstance(action, str):
            priorities.append(action)

    if dirty_files and not priorities:
        priorities.append("Clean up or commit current local changes before starting a new work block.")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in priorities:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)

    if not deduped:
        deduped.append("No urgent blockers detected. Pick the next highest-value work-politics or architecture task.")
    return deduped[:3]


def build_operator_daily_warmup(
    user_id: str = "grace-mar",
    *,
    verbose_dream: bool = False,
    show_civ_mem: bool | None = None,
    show_rollup: bool | None = None,
) -> str:
    user_dir = USERS_DIR / user_id
    recursion_gate = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-archive.md") or _read(user_dir / "self-evidence.md")
    session = _read(user_dir / "session-log.md")

    pending_all = _pending_candidates(recursion_gate, "all")
    pending_politics = _pending_candidates(recursion_gate, "pol")
    pending_companion = _pending_candidates(recursion_gate, "companion")
    fork_cfg = load_fork_config()
    max_pending = fork_cfg.get("max_pending_candidates")
    last_activity = _last_activity_oneliner(evidence) or "_none parsed_"
    coffee_budget = _coffee_context_budget()
    tail_n = get_int(coffee_budget, "max_session_tail_lines", 3)
    session_tail = _session_lines_tail(session, tail_n)
    politics_snapshot = get_work_politics_snapshot(user_id)
    integrity_errors = _integrity_errors(user_id)
    dirty_files = _git_status_lines()
    content_counts = (politics_snapshot.get("content_queue") or {}).get("status_counts") or {}
    brief_counts = (politics_snapshot.get("brief_readiness") or {}).get("status_counts") or {}
    primary_label = ((politics_snapshot.get("campaign_status") or {}).get("primary_date")) or "unknown"
    days_until_primary = ((politics_snapshot.get("campaign_status") or {}).get("days_until_primary"))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Daily operator warmup",
        "",
        f"- Generated: {ts}",
        f"- User: `{user_id}`",
        f"- Gate pending: {len(pending_all)} total ({len(pending_politics)} work-politics, {len(pending_companion)} companion)",
    ]
    if max_pending is not None and len(pending_all) > int(max_pending):
        lines.append(
            f"- **Gate backlog:** {len(pending_all)} pending exceeds `max_pending_candidates` ({max_pending}) in `config/fork-config.json` — review or merge soon."
        )
    lines.extend(
        [
            f"- Last activity: {last_activity}",
            f"- Integrity: {'PASS' if not integrity_errors else f'FAIL ({len(integrity_errors)} issue(s))'}",
            f"- Worktree: {'clean' if not dirty_files else f'{len(dirty_files)} changed file(s)'}",
            "",
            "## Top priorities",
            "",
        ]
    )
    for item in _priority_list(
        pending_all=pending_all,
        pending_politics=pending_politics,
        integrity_errors=integrity_errors,
        politics_snapshot=politics_snapshot,
        dirty_files=dirty_files,
    ):
        lines.append(f"- {item}")

    last_dream = _read_last_dream(user_dir)
    if last_dream and get_bool(_coffee_context_budget(), "allow_last_dream", True):
        lines.append("")
        lines.extend(
            _format_last_dream_block(
                last_dream,
                verbose_dream=verbose_dream,
                show_civ_mem=show_civ_mem,
                show_rollup=show_rollup,
            )
        )

    lines.append("")
    if build_morning_pulse_lines is not None:
        try:
            lines.extend(build_morning_pulse_lines(user_id))
        except Exception:
            lines.append("## Predictive History — morning momentum")
            lines.append("")
            lines.append("_Jiang pulse skipped (could not read work-jiang paths)._")
            lines.append("")
    else:
        lines.append("## Predictive History — morning momentum")
        lines.append("")
        lines.append("_Run `python3 scripts/work_jiang/warmup_jiang_pulse.py -u %s` if import failed._" % user_id)
        lines.append("")

    lines.extend(
        [
            "## Pipeline velocity (operator depth)",
            "",
            f"- {velocity_oneliner(user_id)}",
            "",
            "## Work-politics snapshot",
            "",
            f"- Primary date: {primary_label} ({days_until_primary} day(s) remaining)",
            f"- Territory blockers: {len(politics_snapshot.get('territory_blockers') or [])}",
            f"- Brief readiness: ready={brief_counts.get('ready', 0)}, watch={brief_counts.get('watch', 0)}, needs_refresh={brief_counts.get('needs_refresh', 0)}",
            f"- Content queue: idea={content_counts.get('idea', 0)}, draft={content_counts.get('draft', 0)}, review={content_counts.get('review', 0)}, posted={content_counts.get('posted', 0)}",
            "",
            "## Repo health",
            "",
        ]
    )

    if integrity_errors:
        for err in integrity_errors[:5]:
            lines.append(f"- {err}")
        if len(integrity_errors) > 5:
            lines.append(f"- ... and {len(integrity_errors) - 5} more integrity issue(s)")
    else:
        lines.append("- Integrity validator passed.")

    lines.extend(["", "## Local changes", ""])
    if dirty_files:
        for path in dirty_files[:8]:
            lines.append(f"- `{path}`")
        if len(dirty_files) > 8:
            lines.append(f"- ... and {len(dirty_files) - 8} more")
    else:
        lines.append("- Worktree clean.")

    lines.extend(["", "## Session tail", ""])
    if session_tail:
        for item in session_tail:
            lines.append(f"- {item}")
    else:
        lines.append("- `users/grace-mar/session-log.md` tail unavailable.")

    lines.extend(
        [
            "",
            "## Coffee — KY-4 polling + prediction markets (lazy)",
            "",
            "- With **coffee** (legacy `hey`): **Polymarket** + independent poll **web search** + Massie X run **only** after **menu A — Today** (or explicit same-message request), per `docs/skill-work/work-politics/polling-and-markets.md` — **not** in Step 1. This script does not fetch markets; follow the skill after this command.",
            "",
            "## Guardrail",
            "",
            "- Read-only summary only. Do not merge Record changes without companion approval.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily operator warmup for Grace-Mar.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument(
        "--verbose-dream",
        action="store_true",
        help="Expand last-dream handoff (paths, civ-mem detail, followups). Default is collapsed.",
    )
    parser.add_argument(
        "--show-civ-mem",
        action="store_true",
        help="Show civ-mem summary line in collapsed Last dream (overrides coffee.json default).",
    )
    parser.add_argument(
        "--show-rollup",
        action="store_true",
        help="Show coffee 24h rollup line in collapsed Last dream (overrides coffee.json default).",
    )
    args = parser.parse_args()
    print(
        build_operator_daily_warmup(
            user_id=args.user,
            verbose_dream=args.verbose_dream,
            show_civ_mem=True if args.show_civ_mem else None,
            show_rollup=True if args.show_rollup else None,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
