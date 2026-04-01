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
from emit_pipeline_event import append_pipeline_event
from repo_io import resolve_self_memory_path

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


def run_auto_dream(
    *,
    user_id: str = DEFAULT_USER,
    users_dir: Path = DEFAULT_USERS_DIR,
    apply: bool = True,
    emit_event: bool = True,
    write_artifacts: bool = True,
) -> dict[str, Any]:
    memory_result = maintain_self_memory(user_id=user_id, users_dir=users_dir, apply=apply)
    integrity_json = _run_json_command(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate-integrity.py"),
            "--users-dir",
            str(users_dir),
            "--user",
            user_id,
            "--json",
        ],
        REPO_ROOT,
    )
    governance_code, governance_stdout, governance_stderr = _run_text_command(
        [sys.executable, str(REPO_ROOT / "scripts" / "governance_checker.py")],
        REPO_ROOT,
    )

    digest_path = default_digest_path(users_dir=users_dir, user_id=user_id) if apply else None
    digest = generate_contradiction_digest(user_id=user_id, users_dir=users_dir, write_path=digest_path)
    artifact_drafts: list[dict[str, Any]] = []
    if write_artifacts and apply:
        artifact_drafts = write_artifact_drafts(digest)

    summary: dict[str, Any] = {
        "ok": bool(integrity_json.get("ok")) and governance_code == 0,
        "user_id": user_id,
        "self_memory": {
            "path": str(memory_result.path),
            "created": memory_result.created,
            "changed": memory_result.changed,
            "added_sections": memory_result.added_sections,
            "deduped_lines": memory_result.deduped_lines,
            "blank_lines_collapsed": memory_result.blank_lines_collapsed,
        },
        "integrity": integrity_json,
        "governance": {
            "ok": governance_code == 0,
            "returncode": governance_code,
            "stdout": governance_stdout,
            "stderr": governance_stderr,
        },
        "contradiction_digest": digest,
        "artifact_drafts": artifact_drafts,
    }

    if emit_event and apply:
        reviewable = digest.get("reviewable_count", 0)
        contradictions = digest.get("relation_counts", {}).get("contradiction", 0)
        draft_count = sum(1 for row in artifact_drafts if row.get("promotable"))
        event = append_pipeline_event(
            user_id,
            "maintenance",
            None,
            merge={
                "action": "auto_dream",
                "self_memory_changed": str(memory_result.changed).lower(),
                "reviewable_candidates": str(reviewable),
                "contradictions": str(contradictions),
                "artifact_drafts": str(draft_count),
            },
        )
        summary["event"] = event
    return summary


def format_auto_dream_summary(summary: dict[str, Any]) -> str:
    memory = summary.get("self_memory") or {}
    digest = summary.get("contradiction_digest") or {}
    counts = digest.get("relation_counts") or {}
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
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded self-memory maintenance and contradiction digest refresh.")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id (default: grace-mar)")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR, help="Users directory root")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    parser.add_argument("--dry-run", action="store_true", help="Do not write self-memory, derived digest, or events")
    parser.add_argument("--no-event", action="store_true", help="Skip pipeline-events emission")
    parser.add_argument("--no-artifacts", action="store_true", help="Skip contradiction artifact draft writes")
    args = parser.parse_args()

    summary = run_auto_dream(
        user_id=args.user,
        users_dir=args.users_dir,
        apply=not args.dry_run,
        emit_event=not args.no_event and not args.dry_run,
        write_artifacts=not args.no_artifacts and not args.dry_run,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_auto_dream_summary(summary))
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
