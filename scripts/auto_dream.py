#!/usr/bin/env python3
"""Bounded self-memory maintenance and contradiction digest refresh."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
DEFAULT_USER = "grace-mar"

for path in (REPO_ROOT / "scripts",):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from contradiction_digest import default_digest_path, generate_contradiction_digest, write_artifact_drafts
from dream_civmem_echoes import CIVMEM_DISCLAIMER, compute_civmem_echoes
from dream_coffee_rollup import rollup_coffee_24h
from dream_execution_paths import build_execution_paths, format_tomorrow_inherits_line
from fork_config import load_fork_config
from emit_pipeline_event import append_pipeline_event
from log_cadence_event import append_cadence_event, resolve_cursor_model
from harness_warmup import _pending_candidates
from repo_io import resolve_self_memory_path

LAST_DREAM_FILENAME = "last-dream.json"
HANDOFF_SCHEMA_VERSION = 2


def _classify_worktree_grace(status_out: str, diff_out: str) -> tuple[str, str]:
    """Read-only triage for last-dream.json (no commits). Mirrors companion-self cadence-dream."""
    combined = f"{status_out}\n{diff_out}".lower()
    if "unmerged" in combined or "both modified" in combined:
        return (
            "risky residue",
            "Merge or conflict state — inspect before continuing.",
        )
    lines = [ln.strip() for ln in status_out.splitlines() if ln.strip()]
    body = [ln for ln in lines if not ln.startswith("## ")]
    if not body:
        return "clean", "leave"
    diff_len = len(diff_out)
    if diff_len > 4000 or len(body) > 12:
        return (
            "risky residue",
            "Large or wide diff — inspect before continuing; use bridge when closing session.",
        )
    return (
        "light residue",
        "leave or commit before sleep; bridge seals when you close the session.",
    )


def _git_worktree_triage_grace() -> tuple[str, str]:
    try:
        st = subprocess.run(
            ["git", "status", "-sb"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        ds = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return _classify_worktree_grace(st.stdout or "", ds.stdout or "")
    except (OSError, subprocess.TimeoutExpired):
        return "light residue", "Could not classify worktree; check git status manually."

_SKELETON = """# MEMORY - Self-memory (short / medium / long)

> Not part of the Record. SELF is authoritative. "Ephemeral" = non-gated and rotatable, not "only short-term." See docs/memory-template.md v2.0 (three horizons).

Last rotated: {today}

## Short-term

(session / day - tone, thread, calibrations, resistance)

## Medium-term

(days-weeks - open loops, labeled hypotheses)

## Long-term

(meta - rotation policy, pointers to self.md / self-work.md; no durable facts)
"""


@dataclass
class MemoryMaintenanceResult:
    path: Path
    before: str
    after: str
    created: bool
    changed: bool
    added_sections: list[str]
    deduped_lines: int
    blank_lines_collapsed: int


def _run_json_command(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    stdout = completed.stdout.strip()
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = {
                "ok": False,
                "errors": [f"non-json stdout from {' '.join(command)}"],
                "stdout": stdout,
                "stderr": completed.stderr.strip(),
            }
    else:
        payload = {
            "ok": completed.returncode == 0,
            "errors": [] if completed.returncode == 0 else [completed.stderr.strip() or "command failed without JSON output"],
        }
    payload["_returncode"] = completed.returncode
    payload["_stdout"] = stdout
    payload["_stderr"] = completed.stderr.strip()
    return payload


def _run_text_command(command: list[str], cwd: Path) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def _collapse_blank_lines(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    collapsed = 0
    blank_run = 0
    for line in lines:
        if line.strip():
            blank_run = 0
            out.append(line.rstrip())
            continue
        blank_run += 1
        if blank_run > 1:
            collapsed += 1
            continue
        out.append("")
    while out and not out[-1].strip():
        out.pop()
    return out, collapsed


def _dedupe_bullets(section_text: str) -> tuple[str, int]:
    deduped: list[str] = []
    seen_bullets: set[str] = set()
    removed = 0
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            key = stripped.lower()
            if key in seen_bullets:
                removed += 1
                continue
            seen_bullets.add(key)
        deduped.append(line.rstrip())
    return "\n".join(deduped).strip("\n"), removed


def _ensure_rotated_line(text: str, *, changed: bool) -> str:
    today = date.today().isoformat()
    replacement = f"Last rotated: {today}"
    if re.search(r"^Last rotated:\s*.+$", text, re.MULTILINE):
        if changed:
            return re.sub(r"^Last rotated:\s*.+$", replacement, text, flags=re.MULTILINE)
        return text
    lines = text.splitlines()
    insert_at = 0
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            insert_at = idx
            break
    lines[insert_at:insert_at] = [replacement, ""]
    return "\n".join(lines)


def normalize_self_memory_content(existing_text: str) -> tuple[str, list[str], int, int]:
    if not existing_text.strip():
        return _SKELETON.format(today=date.today().isoformat()).rstrip() + "\n", [
            "Short-term",
            "Medium-term",
            "Long-term",
        ], 0, 0

    text = existing_text.replace("\r\n", "\n").rstrip() + "\n"
    sections = {
        "Short-term": "## Short-term",
        "Medium-term": "## Medium-term",
        "Long-term": "## Long-term",
    }
    added_sections: list[str] = []

    if all(header not in text for header in sections.values()):
        prelude = text.strip()
        text = (
            prelude
            + "\n\n## Short-term\n\n"
            + "(legacy content retained below)\n\n"
            + prelude
            + "\n\n## Medium-term\n\n"
            + "\n\n## Long-term\n"
        )
        added_sections = list(sections)

    for label, header in sections.items():
        if header not in text:
            text = text.rstrip() + f"\n\n{header}\n"
            added_sections.append(label)

    matches = list(re.finditer(r"(?m)^## (Short-term|Medium-term|Long-term)\s*$", text))
    if len(matches) < 3:
        normalized_lines, collapsed = _collapse_blank_lines([line.rstrip() for line in text.splitlines()])
        normalized = "\n".join(normalized_lines).rstrip() + "\n"
        normalized = _ensure_rotated_line(normalized, changed=bool(added_sections))
        return normalized, added_sections, 0, collapsed

    prefix = text[: matches[0].start()].rstrip()
    built_sections: list[str] = []
    removed_duplicates = 0
    for idx, match in enumerate(matches):
        header = match.group(0)
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[body_start:body_end]
        cleaned_body, removed = _dedupe_bullets(body)
        removed_duplicates += removed
        built_sections.append(f"{header}\n\n{cleaned_body}".rstrip())
    normalized = prefix + "\n\n" + "\n\n".join(built_sections) + "\n"
    normalized_lines, collapsed = _collapse_blank_lines([line.rstrip() for line in normalized.splitlines()])
    normalized = "\n".join(normalized_lines).rstrip() + "\n"
    normalized = _ensure_rotated_line(
        normalized,
        changed=bool(added_sections or removed_duplicates or collapsed or normalized != existing_text),
    )
    return normalized, added_sections, removed_duplicates, collapsed


def maintain_self_memory(
    *,
    user_id: str = DEFAULT_USER,
    users_dir: Path = DEFAULT_USERS_DIR,
    apply: bool = True,
) -> MemoryMaintenanceResult:
    user_dir = users_dir / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    memory_path = resolve_self_memory_path(user_dir)
    before = memory_path.read_text(encoding="utf-8") if memory_path.exists() else ""
    after, added_sections, deduped_lines, blank_lines_collapsed = normalize_self_memory_content(before)
    changed = after != before
    if apply and changed:
        memory_path.write_text(after, encoding="utf-8")
    return MemoryMaintenanceResult(
        path=memory_path,
        before=before,
        after=after,
        created=not bool(before.strip()),
        changed=changed,
        added_sections=added_sections,
        deduped_lines=deduped_lines,
        blank_lines_collapsed=blank_lines_collapsed,
    )


def _persist_memory_result(result: MemoryMaintenanceResult) -> None:
    result.path.write_text(result.after, encoding="utf-8")


def _load_dream_budget_dict() -> dict[str, Any]:
    try:
        from context_budget import load_context_budget
    except ImportError:
        from scripts.context_budget import load_context_budget  # type: ignore

    return load_context_budget("dream")


def _apply_coffee_rollup_budget(
    coffee_rollup: dict[str, Any],
    dream_budget: dict[str, Any],
) -> dict[str, Any]:
    try:
        from context_budget import get_bool
    except ImportError:
        from scripts.context_budget import get_bool  # type: ignore

    if get_bool(dream_budget, "allow_rollup", True):
        return coffee_rollup
    return {
        "window_start_utc": coffee_rollup.get("window_start_utc"),
        "window_end_utc": coffee_rollup.get("window_end_utc"),
        "window_hours": coffee_rollup.get("window_hours", 24.0),
        "count": 0,
        "first_ts": None,
        "last_ts": None,
        "span_hours": None,
        "by_mode": {},
        "runs": [],
        "picks": [],
        "by_picked": {},
        "note": "rollup_disabled_by_budget",
    }


def _apply_civmem_budget(
    *,
    digest: dict[str, Any],
    self_memory_text: str,
    integrity_ok: bool,
    governance_ok: bool,
    dream_budget: dict[str, Any],
) -> tuple[list[dict[str, Any]], bool, str | None]:
    try:
        from context_budget import get_bool, get_int
    except ImportError:
        from scripts.context_budget import get_bool, get_int  # type: ignore

    if not get_bool(dream_budget, "allow_civ_mem_echo", True):
        return [], False, "disabled_by_budget"

    sup_int = get_bool(dream_budget, "suppress_analogy_when_integrity_fails", True)
    sup_gov = get_bool(dream_budget, "suppress_analogy_when_governance_alert", True)
    if sup_int and not integrity_ok:
        return [], False, "suppressed_integrity_fail"
    if sup_gov and not governance_ok:
        return [], False, "suppressed_governance_alert"

    max_echoes = get_int(dream_budget, "max_civ_mem_echoes", 1)
    min_overlap = get_int(dream_budget, "min_civ_mem_overlap", 4)
    query_limit = get_int(dream_budget, "civmem_query_limit", 24)
    require_spec = get_bool(dream_budget, "require_specific_civ_mem_token", False)

    civ_echoes, civ_index_missing = compute_civmem_echoes(
        digest=digest,
        self_memory_text=self_memory_text,
        limit=max_echoes,
        min_overlap=min_overlap,
        query_limit=query_limit,
        require_specificity=require_spec,
        dream_budget=dream_budget,
    )
    max_echoes = max(0, max_echoes)
    civ_echoes = civ_echoes[:max_echoes]
    return civ_echoes, civ_index_missing, None


def _write_last_dream_handoff(
    summary: dict[str, Any],
    *,
    users_dir: Path = DEFAULT_USERS_DIR,
    user_id: str = DEFAULT_USER,
    cursor_model: str = "unknown",
) -> Path:
    """Write a compact JSON handoff so tomorrow's coffee Step 1 can pick up
    what dream found overnight."""
    from datetime import datetime, timezone

    memory = summary.get("self_memory") or {}
    digest = summary.get("contradiction_digest") or {}
    counts = digest.get("relation_counts") or {}
    artifact_drafts = summary.get("artifact_drafts") or []
    promotable = sum(1 for row in artifact_drafts if row.get("promotable"))

    followups: list[str] = []
    if counts.get("contradiction", 0) > 0:
        followups.append(f"{counts['contradiction']} contradiction(s) in digest — review recommended")
    if digest.get("reviewable_count", 0) > 0:
        followups.append(f"{digest['reviewable_count']} reviewable item(s) in digest")
    if promotable > 0:
        followups.append(f"{promotable} promotable artifact draft(s) prepared")

    if summary.get("civmem_index_missing"):
        followups.append(
            "In-repo civ-mem index missing — optional: python3 scripts/build_civmem_inrepo_index.py build"
        )

    handoff: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "agent_surface": {"cursor_model": cursor_model},
        "strict_mode": summary.get("strict_mode", False),
        "ok": summary.get("ok", False),
        "integrity_ok": bool((summary.get("integrity") or {}).get("ok")),
        "governance_ok": bool((summary.get("governance") or {}).get("ok")),
        "self_memory_changed": memory.get("changed", False),
        "reviewable_count": digest.get("reviewable_count", 0),
        "contradiction_count": counts.get("contradiction", 0),
        "artifact_draft_count": len(artifact_drafts),
        "promotable_draft_count": promotable,
        "followups": followups,
    }
    cr = summary.get("coffee_rollup_24h")
    if cr is not None:
        handoff["coffee_rollup_24h"] = cr
    if summary.get("execution_paths") is not None:
        handoff["execution_paths"] = summary["execution_paths"]
        handoff["suggested_execution_path_index"] = summary.get("suggested_execution_path_index", 0)
        if summary.get("execution_path_suggestion_reason"):
            handoff["execution_path_suggestion_reason"] = summary["execution_path_suggestion_reason"]
        if summary.get("tomorrow_inherits"):
            handoff["tomorrow_inherits"] = summary["tomorrow_inherits"]
    if summary.get("civmem_echoes") is not None:
        handoff["civmem_echoes"] = summary["civmem_echoes"]
    if summary.get("civmem_disclaimer"):
        handoff["civmem_disclaimer"] = summary["civmem_disclaimer"]
    if "civmem_index_missing" in summary:
        handoff["civmem_index_missing"] = bool(summary["civmem_index_missing"])
    if summary.get("civmem_suppressed_reason"):
        handoff["civmem_suppressed_reason"] = summary["civmem_suppressed_reason"]

    # Schema v2 alignment with companion-self night-handoff (operational; not Record).
    handoff["handoffSchemaVersion"] = HANDOFF_SCHEMA_VERSION
    reason = (summary.get("execution_path_suggestion_reason") or "").strip()
    if not reason and summary.get("tomorrow_inherits"):
        reason = "Carry-forward from dream execution-path / tomorrow_inherits."
    handoff["topActionReason"] = reason or (
        "Dream digest and followups shaped priorities; see followups and integrity flags."
    )
    rc = int(handoff.get("reviewable_count", 0) or 0)
    cc = int(handoff.get("contradiction_count", 0) or 0)
    handoff["quietRun"] = bool(handoff.get("ok")) and rc == 0 and cc == 0 and len(followups) == 0
    handoff["residueLedger"] = {
        "must_resume": (followups[0][:120] if followups else ""),
        "safe_to_drop": "",
        "blocked": "",
        "watch_later": (followups[1][:120] if len(followups) > 1 else ""),
    }
    if not handoff["ok"]:
        handoff["residueLedger"]["blocked"] = "Dream reported not ok — review integrity/governance before new work."
    wt_state, wt_adv = _git_worktree_triage_grace()
    handoff["worktreeState"] = wt_state
    handoff["worktreeAdvice"] = wt_adv

    path = users_dir / user_id / LAST_DREAM_FILENAME
    path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    return path


def run_auto_dream(
    *,
    user_id: str = DEFAULT_USER,
    users_dir: Path = DEFAULT_USERS_DIR,
    apply: bool = True,
    emit_event: bool = True,
    write_artifacts: bool = True,
    strict_mode: bool = False,
    cursor_model: str | None = None,
) -> dict[str, Any]:
    memory_result = maintain_self_memory(user_id=user_id, users_dir=users_dir, apply=False)
    integrity_command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "validate-integrity.py"),
        "--users-dir",
        str(users_dir),
        "--user",
        user_id,
        "--json",
    ]
    if strict_mode:
        integrity_command.append("--require-proposal-class")
    integrity_json = _run_json_command(integrity_command, REPO_ROOT)
    governance_code, governance_stdout, governance_stderr = _run_text_command(
        [sys.executable, str(REPO_ROOT / "scripts" / "governance_checker.py")],
        REPO_ROOT,
    )
    integrity_ok = bool(integrity_json.get("ok"))
    governance_ok = governance_code == 0
    halted = strict_mode and (not integrity_ok or not governance_ok)

    digest_path = default_digest_path(users_dir=users_dir, user_id=user_id) if apply and not halted else None
    artifact_drafts: list[dict[str, Any]] = []
    if halted:
        digest = {
            "generated_at": None,
            "user_id": user_id,
            "strict_mode": True,
            "skipped": True,
            "skip_reason": "strict maintenance halted after integrity/governance failure",
            "pending_candidate_count": None,
            "reviewable_count": 0,
            "relation_counts": {},
            "entries": [],
        }
    else:
        digest = generate_contradiction_digest(
            user_id=user_id,
            users_dir=users_dir,
            write_path=digest_path,
            strict_mode=strict_mode,
        )
        if apply and memory_result.changed:
            _persist_memory_result(memory_result)
        if write_artifacts and apply:
            artifact_drafts = write_artifact_drafts(digest)

    summary: dict[str, Any] = {
        "ok": integrity_ok and governance_ok and not halted,
        "user_id": user_id,
        "strict_mode": strict_mode,
        "halted": halted,
        "self_memory": {
            "path": str(memory_result.path),
            "created": memory_result.created,
            "changed": memory_result.changed and not halted,
            "would_change": memory_result.changed,
            "added_sections": memory_result.added_sections,
            "deduped_lines": memory_result.deduped_lines,
            "blank_lines_collapsed": memory_result.blank_lines_collapsed,
        },
        "integrity": integrity_json,
        "governance": {
            "ok": governance_ok,
            "returncode": governance_code,
            "stdout": governance_stdout,
            "stderr": governance_stderr,
        },
        "contradiction_digest": digest,
        "artifact_drafts": artifact_drafts,
    }

    if emit_event and apply and not halted:
        reviewable = digest.get("reviewable_count", 0)
        contradictions = digest.get("relation_counts", {}).get("contradiction", 0)
        draft_count = sum(1 for row in artifact_drafts if row.get("promotable"))
        event = append_pipeline_event(
            user_id,
            "maintenance",
            None,
            merge={
                "action": "auto_dream",
                "strict_mode": str(strict_mode).lower(),
                "self_memory_changed": str(memory_result.changed).lower(),
                "reviewable_candidates": str(reviewable),
                "contradictions": str(contradictions),
                "artifact_drafts": str(draft_count),
            },
        )
        summary["event"] = event

    if apply and not halted:
        from datetime import datetime, timezone

        now_utc = datetime.now(timezone.utc)
        dream_budget = _load_dream_budget_dict()
        coffee_rollup = rollup_coffee_24h(user_id=user_id, now_utc=now_utc)
        coffee_rollup = _apply_coffee_rollup_budget(coffee_rollup, dream_budget)
        dc = summary.get("contradiction_digest") or {}
        rel_counts = dc.get("relation_counts") or {}
        gate_path = users_dir / user_id / "recursion-gate.md"
        gate_text = gate_path.read_text(encoding="utf-8") if gate_path.is_file() else ""
        gate_pending_count = len(_pending_candidates(gate_text, "all"))
        fork_cfg = load_fork_config()
        raw_max = fork_cfg.get("max_pending_candidates")
        max_pending = int(raw_max) if raw_max is not None else None

        paths, sugg_idx, sugg_reason = build_execution_paths(
            user_id=user_id,
            now_utc=now_utc,
            integrity_ok=integrity_ok,
            governance_ok=governance_ok,
            reviewable_count=int(dc.get("reviewable_count") or 0),
            contradiction_count=int(rel_counts.get("contradiction") or 0),
            coffee_count_24h=int(coffee_rollup.get("count") or 0),
            gate_pending_count=gate_pending_count,
            max_pending_candidates=max_pending,
        )
        civ_echoes, civ_index_missing, civ_suppressed = _apply_civmem_budget(
            digest=dc,
            self_memory_text=memory_result.before,
            integrity_ok=integrity_ok,
            governance_ok=governance_ok,
            dream_budget=dream_budget,
        )
        tomorrow_line = format_tomorrow_inherits_line(paths, sugg_idx, sugg_reason)
        summary["coffee_rollup_24h"] = coffee_rollup
        summary["execution_paths"] = paths
        summary["suggested_execution_path_index"] = sugg_idx
        summary["execution_path_suggestion_reason"] = sugg_reason
        summary["tomorrow_inherits"] = tomorrow_line
        summary["civmem_echoes"] = civ_echoes
        summary["civmem_disclaimer"] = CIVMEM_DISCLAIMER
        summary["civmem_index_missing"] = civ_index_missing
        if civ_suppressed:
            summary["civmem_suppressed_reason"] = civ_suppressed
        else:
            summary.pop("civmem_suppressed_reason", None)

        cm = resolve_cursor_model(explicit=cursor_model)
        handoff_path = _write_last_dream_handoff(
            summary,
            users_dir=users_dir,
            user_id=user_id,
            cursor_model=cm,
        )
        summary["handoff_path"] = str(handoff_path)
        summary["agent_surface"] = {"cursor_model": cm}

        digest = summary.get("contradiction_digest") or {}
        counts = digest.get("relation_counts") or {}
        try:
            append_cadence_event(
                "dream",
                user_id,
                ok=summary.get("ok", False),
                mode="strict" if strict_mode else "default",
                cursor_model=cm,
                kv={
                    "integrity": "pass" if integrity_ok else "fail",
                    "governance": "pass" if governance_ok else "fail",
                    "mem_changed": str(memory_result.changed).lower(),
                    "reviewable": str(digest.get("reviewable_count", 0)),
                    "contradictions": str(counts.get("contradiction", 0)),
                    "civmem_echo_count": str(len(civ_echoes)),
                    "civmem_suppressed": str(bool(civ_suppressed)).lower(),
                },
            )
        except Exception:
            pass

    return summary


def format_auto_dream_summary(summary: dict[str, Any]) -> str:
    memory = summary.get("self_memory") or {}
    digest = summary.get("contradiction_digest") or {}
    counts = digest.get("relation_counts") or {}
    if summary.get("strict_mode"):
        lines = [
            "strict autoDream" if summary.get("ok") else "strict autoDream FAILED",
            f"user: {summary.get('user_id', DEFAULT_USER)}",
            f"self-memory changed: {memory.get('changed', False)}",
            f"integrity ok: {bool((summary.get('integrity') or {}).get('ok'))}",
            f"governance ok: {bool((summary.get('governance') or {}).get('ok'))}",
        ]
        if digest.get("skipped"):
            lines.append(f"digest: skipped ({digest.get('skip_reason')})")
        else:
            lines.append(
                "digest: "
                f"reviewable={digest.get('reviewable_count', 0)} "
                f"contradiction={counts.get('contradiction', 0)} "
                f"duplicate={counts.get('duplicate', 0)} "
                f"refinement={counts.get('refinement', 0)}"
            )
            promotable = sum(1 for row in summary.get("artifact_drafts") or [] if row.get("promotable"))
            lines.append(f"artifact drafts: {promotable}")
        cr = summary.get("coffee_rollup_24h") or {}
        if cr.get("count", 0) > 0:
            lines.append(
                f"coffee rollup 24h: count={cr.get('count')} modes={cr.get('by_mode')}"
            )
        return "\n".join(lines)

    lines = [
        "autoDream status",
        f"user: {summary.get('user_id', DEFAULT_USER)}",
        f"self-memory changed: {memory.get('changed', False)}",
        f"sections added: {', '.join(memory.get('added_sections') or []) or 'none'}",
        f"deduped lines: {memory.get('deduped_lines', 0)}",
        f"blank lines collapsed: {memory.get('blank_lines_collapsed', 0)}",
        f"integrity ok: {bool((summary.get('integrity') or {}).get('ok'))}",
        f"governance ok: {bool((summary.get('governance') or {}).get('ok'))}",
        (
            "digest: "
            f"reviewable={digest.get('reviewable_count', 0)} "
            f"duplicate={counts.get('duplicate', 0)} "
            f"refinement={counts.get('refinement', 0)} "
            f"contradiction={counts.get('contradiction', 0)}"
        ),
    ]
    artifact_drafts = summary.get("artifact_drafts") or []
    promotable = sum(1 for row in artifact_drafts if row.get("promotable"))
    if artifact_drafts:
        lines.append(f"artifact drafts: {promotable}/{len(artifact_drafts)} promotable")
    cr = summary.get("coffee_rollup_24h") or {}
    if cr.get("count", 0) > 0:
        lines.append(
            f"coffee rollup 24h: count={cr.get('count')} modes={cr.get('by_mode')}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded self-memory maintenance and contradiction digest refresh.")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id (default: grace-mar)")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR, help="Users directory root")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    parser.add_argument("--dry-run", action="store_true", help="Do not write self-memory, derived digest, or events")
    parser.add_argument("--no-event", action="store_true", help="Skip pipeline-events emission")
    parser.add_argument("--no-artifacts", action="store_true", help="Skip contradiction artifact draft writes")
    parser.add_argument("--strict", action="store_true", help="Use strict maintenance semantics and fail fast on checks")
    parser.add_argument(
        "--cursor-model",
        default=None,
        help="Cursor UI model label for agent_surface + cadence log (else CURSOR_MODEL env, else unknown)",
    )
    args = parser.parse_args()

    summary = run_auto_dream(
        user_id=args.user,
        users_dir=args.users_dir,
        apply=not args.dry_run,
        emit_event=not args.no_event and not args.dry_run,
        write_artifacts=not args.no_artifacts and not args.dry_run,
        strict_mode=args.strict,
        cursor_model=(args.cursor_model.strip() if args.cursor_model else None),
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_auto_dream_summary(summary))
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
