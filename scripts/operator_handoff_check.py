#!/usr/bin/env python3
"""
Generate a stop/resume handoff summary for the current repo state.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

try:
    from harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from work_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from scripts.work_politics_ops import get_wap_snapshot

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"

RUNTIME_NOISE_MARKERS = (
    "users/grace-mar/pipeline-events.jsonl",
    "users/grace-mar/harness-events.jsonl",
    "runtime-bundle/runtime/",
    "runtime-bundle/audit/",
)


def _run_git(*args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return [f"git {' '.join(args)} failed: {proc.stderr.strip() or 'unknown error'}"]
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _classify_change(path_line: str) -> tuple[str, str]:
    path = path_line[3:] if len(path_line) > 3 else path_line
    if any(marker in path for marker in RUNTIME_NOISE_MARKERS):
        return "runtime_noise", path
    if (
        path.startswith(".cursor/skills/")
        or path == "docs/operator-skills.md"
        or path.startswith("scripts/operator_")
    ):
        return "operator_workflow", path
    if (
        "work-politics" in path
        or "operator-wap" in path
        or "work_politics" in path
        or "generate_wap_weekly_brief.py" in path
    ):
        return "wap_operations", path
    if path.startswith("users/") or "recursion_gate" in path or path == "bot/prompt.py":
        return "record_pipeline", path
    return "repo_misc", path


def _active_thread(meaningful_changes: list[str], gate_pending: int, wap_blockers: list[dict]) -> tuple[str, str]:
    counts = {
        "operator_workflow": 0,
        "wap_operations": 0,
        "record_pipeline": 0,
        "repo_misc": 0,
    }
    for raw in meaningful_changes:
        category, _path = _classify_change(raw)
        if category in counts:
            counts[category] += 1
    dominant = max(counts, key=counts.get)
    if counts[dominant] == 0:
        if gate_pending:
            return (
                "gate continuity",
                "Start with `python3 scripts/operator_gate_review_pass.py -u grace-mar` to review pending candidates.",
            )
        if wap_blockers:
            return (
                "wap operations",
                "Start with `python3 scripts/operator_wap_pulse.py -u grace-mar` and address the first blocker.",
            )
        return (
            "stable baseline",
            "Start with `python3 scripts/operator_daily_warmup.py -u grace-mar` and choose the next highest-value task.",
        )
    if dominant == "operator_workflow":
        return (
            "operator workflow stack",
            "Resume the operator workflow pass and either test or commit the local workflow files.",
        )
    if dominant == "wap_operations":
        return (
            "wap operations",
            "Resume WAP work with `python3 scripts/operator_wap_pulse.py -u grace-mar` and then run the brief workflow if ready.",
        )
    if dominant == "record_pipeline":
        return (
            "record pipeline",
            "Resume with a gate review before making any Record-adjacent edits.",
        )
    return (
        "mixed repo maintenance",
        "Start with `python3 scripts/operator_daily_warmup.py -u grace-mar` and sort local changes into one active thread.",
    )


def build_handoff_check(user_id: str = "grace-mar") -> str:
    user_dir = USERS_DIR / user_id
    recursion_gate = _read(user_dir / "recursion-gate.md")
    evidence = _read(user_dir / "self-evidence.md")
    gate_pending = _pending_candidates(recursion_gate, "all")
    last_activity = _last_activity_oneliner(evidence) or "_none parsed_"
    wap_snapshot = get_wap_snapshot(user_id)

    status_lines = _run_git("status", "--short")
    recent_commits = _run_git("log", "--oneline", "-3")
    runtime_noise: list[str] = []
    meaningful_changes: list[str] = []
    for line in status_lines:
        category, _path = _classify_change(line)
        if category == "runtime_noise":
            runtime_noise.append(line)
        else:
            meaningful_changes.append(line)

    thread_label, reentry_prompt = _active_thread(
        meaningful_changes,
        gate_pending=len(gate_pending),
        wap_blockers=wap_snapshot.get("territory_blockers") or [],
    )

    lines = [
        "# Handoff check",
        "",
        f"- User: `{user_id}`",
        f"- Last activity: {last_activity}",
        f"- Pending gate items: {len(gate_pending)}",
        f"- Active thread guess: {thread_label}",
        "",
        "## Recently committed",
        "",
    ]

    if recent_commits:
        for line in recent_commits:
            lines.append(f"- {line}")
    else:
        lines.append("- No recent commits found.")

    lines.extend(["", "## Local work still in progress", ""])
    if meaningful_changes:
        for line in meaningful_changes[:10]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No meaningful local changes detected.")

    lines.extend(["", "## Runtime noise", ""])
    if runtime_noise:
        for line in runtime_noise[:10]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No runtime-only local noise detected.")

    lines.extend(["", "## WAP continuity", ""])
    lines.append(f"- Territory blockers: {len(wap_snapshot.get('territory_blockers') or [])}")
    for action in (wap_snapshot.get("next_actions") or [])[:3]:
        lines.append(f"- {action}")

    lines.extend(["", "## Next re-entry prompt", ""])
    lines.append(f"- {reentry_prompt}")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Treat runtime noise separately from meaningful local work before committing or pushing.",
            "- This workflow summarizes stop/resume state only; it does not stage, commit, or merge anything.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a handoff summary for Grace-Mar.")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    args = parser.parse_args()
    print(build_handoff_check(user_id=args.user))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
