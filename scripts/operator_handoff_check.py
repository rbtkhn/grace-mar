#!/usr/bin/env python3
"""
Generate a stop/resume handoff summary for the current repo state.

Includes a dedicated RECURSION-GATE section: pending counts by territory (work-politics vs
companion), up to a capped list of pending candidate IDs and summaries, and proposed next
steps to review/approve/merge via process_approved_candidates (read-only — this script does
not merge). Intended for good-night / handoff-check workflows.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from recursion_gate_territory import TERRITORY_LABEL_WAP, pending_by_territory
    from work_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.harness_warmup import _last_activity_oneliner, _pending_candidates, _read
    from scripts.recursion_gate_territory import TERRITORY_LABEL_WAP, pending_by_territory
    from scripts.work_politics_ops import get_wap_snapshot

# Max pending rows to list verbatim before collapsing (good night / handoff stays scannable).
_GATE_PENDING_DISPLAY_CAP = 12

REPO_ROOT = Path(__file__).resolve().parent.parent
USERS_DIR = REPO_ROOT / "users"
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from work_jiang.warmup_jiang_pulse import build_night_pulse_lines
except ImportError:
    build_night_pulse_lines = None  # type: ignore[misc, assignment]

RUNTIME_NOISE_MARKERS = (
    "users/grace-mar/pipeline-events.jsonl",
    "users/grace-mar/harness-events.jsonl",
    "runtime-bundle/runtime/",
    "runtime-bundle/audit/",
)

# Regenerated exports / integrity-adjacent — batch-commit or refresh; not "lane editorial" work.
EXPORT_CHURN_MARKERS = (
    "compute-ledger.jsonl",
    "grace-mar-llm.txt",
    "fork-manifest.json",
    "/manifest.json",
    "/llms.txt",
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
    if any(marker in path for marker in EXPORT_CHURN_MARKERS):
        return "export_churn", path
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


def _gate_detail_lines(recursion_gate_md: str, user_id: str) -> list[str]:
    """Human-readable pending queue + proposed merge steps (read-only; does not merge)."""
    gate_rel = f"users/{user_id}/recursion-gate.md"
    wap_rows, companion_rows = pending_by_territory(recursion_gate_md)
    total = len(wap_rows) + len(companion_rows)
    lines: list[str] = [
        "## RECURSION-GATE (pending)",
        "",
        f"- **Total pending:** {total} (work-politics: {len(wap_rows)} · companion: {len(companion_rows)})",
        f"- **Canonical file:** `{gate_rel}`",
        "",
    ]
    if total == 0:
        lines.extend(
            [
                "_No pending candidates above `## Processed`._",
                "",
                "## Proposed: processing pipeline (when you have new candidates)",
                "",
                "1. Stage or confirm candidates in `recursion-gate.md` (pending, above Processed).",
                "2. Review: open the gate file or run "
                f"`python3 scripts/operator_gate_review_pass.py -u {user_id}` for a recommendation-oriented pass.",
                "3. Set `status: approved` or `status: rejected` per companion/operator policy.",
                "4. Merge approved candidates only: "
                f"`python3 scripts/process_approved_candidates.py -u {user_id} --apply` "
                "(or the receipt flow in AGENTS.md). **Record changes require companion approval.**",
                "",
            ]
        )
        return lines

    combined: list[tuple[str, dict]] = [
        *[(TERRITORY_LABEL_WAP, r) for r in wap_rows],
        *[("Companion", r) for r in companion_rows],
    ]
    lines.append("### Pending items")
    lines.append("")
    shown = 0
    for label, row in combined:
        if shown >= _GATE_PENDING_DISPLAY_CAP:
            rest = total - shown
            lines.append(f"- _… and {rest} more — open `{gate_rel}` for full list._")
            break
        cid = row.get("id") or "?"
        summary = (row.get("summary") or "(no summary)")[:160]
        lines.append(f"- **{cid}** [{label}] — {summary}")
        shown += 1
    lines.extend(
        [
            "",
            "## Proposed: complete processing (this handoff does not merge)",
            "",
            f"1. **Review** each pending row in `{gate_rel}` "
            f"or run `python3 scripts/operator_gate_review_pass.py -u {user_id}`.",
            "2. **Decide** `status: approved` or `status: rejected` (companion policy for Record-facing items).",
            "3. **Apply** approved merges only: "
            f"`python3 scripts/process_approved_candidates.py -u {user_id} --apply` "
            "(or `--generate-receipt` / `--apply --receipt` per AGENTS.md).",
            "4. **Verify** pending count is zero: re-run this script or `python3 scripts/harness_warmup.py -u "
            f"{user_id}`.",
            "",
        ]
    )
    return lines


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
                "Start with `python3 scripts/operator_work_politics_pulse.py -u grace-mar` and address the first blocker.",
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
            "Resume work-politics work with `python3 scripts/operator_work_politics_pulse.py -u grace-mar` and then run the brief workflow if ready.",
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
    evidence = _read(user_dir / "self-archive.md") or _read(user_dir / "self-evidence.md")
    gate_pending = _pending_candidates(recursion_gate, "all")
    last_activity = _last_activity_oneliner(evidence) or "_none parsed_"
    wap_snapshot = get_wap_snapshot(user_id)

    status_lines = _run_git("status", "--short")
    recent_commits = _run_git("log", "--oneline", "-3")
    runtime_noise: list[str] = []
    export_churn: list[str] = []
    meaningful_changes: list[str] = []
    for line in status_lines:
        category, _path = _classify_change(line)
        if category == "runtime_noise":
            runtime_noise.append(line)
        elif category == "export_churn":
            export_churn.append(line)
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
        f"- Pending gate items: {len(gate_pending)} (detail below)",
        f"- Active thread guess: {thread_label}",
        "",
    ]
    lines.extend(_gate_detail_lines(recursion_gate, user_id))
    lines.append("")
    if build_night_pulse_lines is not None:
        try:
            lines.extend(build_night_pulse_lines(user_id))
        except Exception:
            lines.append("## Predictive History — night closeout")
            lines.append("")
            lines.append("_Jiang night pulse skipped (could not read work-jiang paths)._")
            lines.append("")
    else:
        lines.append("## Predictive History — night closeout")
        lines.append("")
        lines.append(
            "_Run `python3 scripts/work_jiang/warmup_jiang_pulse.py -u %s --night` if import failed._" % user_id
        )
        lines.append("")
    lines.extend(
        [
            "## Recently committed",
            "",
        ]
    )

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

    lines.extend(["", "## Derived / export churn", ""])
    if export_churn:
        lines.append(
            "_Regenerated or integrity-adjacent files — often safe to batch-commit separately "
            "from editorial work, or refresh via bootstrap verify block (`export_prp`, "
            "`export_manifest`, `validate-integrity`)._"
        )
        lines.append("")
        for line in export_churn[:12]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No derived / export churn detected in `git status`.")

    lines.extend(["", "## Runtime noise", ""])
    if runtime_noise:
        for line in runtime_noise[:10]:
            lines.append(f"- `{line}`")
    else:
        lines.append("- No runtime-only local noise detected.")

    lines.extend(["", "## Work-politics continuity", ""])
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
            "- Treat **derived / export churn** and **runtime noise** separately from meaningful "
            "local work before committing or pushing.",
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
