"""Shared helpers for repo-owned derived regeneration."""

from __future__ import annotations

import fnmatch
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "work-dev" / "rebuild-receipts"


@dataclass(frozen=True)
class RebuildTarget:
    target_id: str
    description: str
    watch_patterns: tuple[str, ...]
    command_templates: tuple[tuple[str, ...], ...]
    outputs: tuple[str, ...]
    depends_on: tuple[str, ...] = ()

    def commands_for_user(self, user: str) -> list[list[str]]:
        return [
            [part.format(user=user) for part in template]
            for template in self.command_templates
        ]


TARGETS: tuple[RebuildTarget, ...] = (
    RebuildTarget(
        target_id="derived-regeneration-manifest",
        description="Machine-readable manifest of repo-owned derived rebuild targets",
        watch_patterns=(
            "scripts/derived_regeneration.py",
            "scripts/build_derived_regeneration_manifest.py",
            "docs/skill-work/work-dev/derived-regeneration.md",
        ),
        command_templates=(("python3", "scripts/build_derived_regeneration_manifest.py"),),
        outputs=("artifacts/work-dev/derived-regeneration-manifest.json",),
    ),
    RebuildTarget(
        target_id="library-index",
        description="SELF-LIBRARY-derived operator dashboard",
        watch_patterns=(
            "users/*/self-library.md",
            "scripts/build_library_index.py",
            "docs/operator-dashboards.md",
        ),
        command_templates=(("python3", "scripts/build_library_index.py"),),
        outputs=("artifacts/library-index.md",),
    ),
    RebuildTarget(
        target_id="work-lanes-dashboard-json",
        description="work-lane JSON aggregate for lane dashboards",
        watch_patterns=(
            "artifacts/work-dev/work-dev-status-summary.json",
            "artifacts/work-strategy/strategy-observability.json",
            "artifacts/work-cadence/cadence-pressure-report.json",
            "scripts/build_work_lanes_dashboard.py",
        ),
        command_templates=(("python3", "scripts/build_work_lanes_dashboard.py"),),
        outputs=("artifacts/work-lanes-dashboard.json",),
    ),
    RebuildTarget(
        target_id="lane-dashboards",
        description="Markdown lane dashboard derived from runtime observations and JSON feeds",
        watch_patterns=(
            "runtime/observations/**",
            "artifacts/work-lanes-dashboard.json",
            "artifacts/handoffs/**",
            "prepared-context/last-budget-builds.json",
            "scripts/build_lane_dashboards.py",
            "scripts/build_work_lanes_dashboard.py",
        ),
        command_templates=(
            ("python3", "scripts/build_work_lanes_dashboard.py"),
            ("python3", "scripts/build_lane_dashboards.py"),
        ),
        outputs=("artifacts/lane-dashboards/README.md", "artifacts/work-lanes-dashboard.json"),
        depends_on=("work-lanes-dashboard-json",),
    ),
    RebuildTarget(
        target_id="review-dashboard",
        description="Review dashboard derived from recursion-gate",
        watch_patterns=(
            "users/*/recursion-gate.md",
            "scripts/build_review_dashboard.py",
        ),
        command_templates=(("python3", "scripts/build_review_dashboard.py"),),
        outputs=("artifacts/review-dashboard.md",),
    ),
    RebuildTarget(
        target_id="gate-board",
        description="Kanban-style gate board derived from recursion-gate",
        watch_patterns=(
            "users/*/recursion-gate.md",
            "scripts/build_gate_board.py",
        ),
        command_templates=(("python3", "scripts/build_gate_board.py"),),
        outputs=("artifacts/gate-board.md",),
    ),
    RebuildTarget(
        target_id="governance-posture",
        description="Governance posture one-pager derived from audit-facing user files",
        watch_patterns=(
            "users/*/self.md",
            "users/*/self-archive.md",
            "users/*/self-evidence.md",
            "users/*/recursion-gate.md",
            "users/*/merge-receipts.jsonl",
            "users/*/pipeline-events.jsonl",
            "users/*/harness-events.jsonl",
            "users/*/session-log.md",
            "scripts/report_governance_posture.py",
            "docs/skill-work/work-dev/safety-story-ux.md",
            "docs/runtime-vs-record.md",
        ),
        command_templates=(
            ("python3", "scripts/report_governance_posture.py", "-u", "{user}"),
        ),
        outputs=("artifacts/governance-posture.md",),
    ),
    RebuildTarget(
        target_id="strategy-notebook-graph",
        description="Strategy-notebook graph and derived views",
        watch_patterns=(
            "docs/skill-work/work-strategy/strategy-notebook/**",
            "scripts/build_strategy_notebook_graph.py",
        ),
        command_templates=(("python3", "scripts/build_strategy_notebook_graph.py"),),
        outputs=(
            "artifacts/work-strategy/strategy-notebook/graph.json",
            "artifacts/work-strategy/strategy-notebook/views/watch-clusters.json",
            "artifacts/work-strategy/strategy-notebook/views/expert-convergence.json",
        ),
    ),
)

TARGETS_BY_ID = {target.target_id: target for target in TARGETS}


def normalize_rel_path(path: str) -> str:
    return Path(path).as_posix().lstrip("./")


def detect_git_changed_paths(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return repo-relative changed paths from the current worktree."""
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []

    changed: set[str] = set()
    for raw_line in proc.stdout.splitlines():
        if not raw_line:
            continue
        path_part = raw_line[3:]
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1]
        changed.add(normalize_rel_path(path_part))
    return sorted(changed)


def path_matches_target(path: str, target: RebuildTarget) -> bool:
    rel = normalize_rel_path(path)
    return any(fnmatch.fnmatch(rel, pattern) for pattern in target.watch_patterns)


def select_targets_for_paths(paths: list[str]) -> list[RebuildTarget]:
    rel_paths = [normalize_rel_path(path) for path in paths]
    selected: list[RebuildTarget] = []
    for target in TARGETS:
        if any(path_matches_target(path, target) for path in rel_paths):
            selected.append(target)
    return selected


def expand_with_downstream(selected_targets: list[RebuildTarget]) -> list[RebuildTarget]:
    """Include downstream targets that depend on any selected target."""
    selected_ids = {target.target_id for target in selected_targets}
    changed = True
    while changed:
        changed = False
        for target in TARGETS:
            if target.target_id in selected_ids:
                continue
            if any(dep in selected_ids for dep in target.depends_on):
                selected_ids.add(target.target_id)
                changed = True
    return [TARGETS_BY_ID[target_id] for target_id in selected_ids]


def topologically_sort_targets(selected_targets: list[RebuildTarget]) -> list[RebuildTarget]:
    """Sort selected targets so upstream dependencies run first."""
    selected_ids = {target.target_id for target in selected_targets}
    remaining = {target.target_id: set(target.depends_on) & selected_ids for target in selected_targets}
    ordered: list[RebuildTarget] = []

    while remaining:
        ready = sorted(target_id for target_id, deps in remaining.items() if not deps)
        if not ready:
            unresolved = ", ".join(sorted(remaining.keys()))
            raise ValueError(f"cyclic derived regeneration dependencies: {unresolved}")
        for target_id in ready:
            ordered.append(TARGETS_BY_ID[target_id])
            remaining.pop(target_id)
            for deps in remaining.values():
                deps.discard(target_id)

    return ordered


def matched_paths_for_target(paths: list[str], target: RebuildTarget) -> list[str]:
    return [
        normalize_rel_path(path)
        for path in paths
        if path_matches_target(path, target)
    ]


def build_manifest_payload() -> dict:
    """Machine-readable manifest for current derived regeneration targets."""
    return {
        "schemaVersion": "1.0.0-derived-regeneration-manifest",
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "recordAuthority": "none",
        "gateEffect": "none",
        "targets": [
            {
                "targetId": target.target_id,
                "description": target.description,
                "watchPatterns": list(target.watch_patterns),
                "commands": [" ".join(cmd) for cmd in target.command_templates],
                "outputs": list(target.outputs),
                "dependsOn": list(target.depends_on),
            }
            for target in TARGETS
        ],
    }


def default_receipt_path(
    *,
    receipt_prefix: str = "derived-rebuild",
    receipt_dir: Path = DEFAULT_RECEIPT_DIR,
    now: datetime | None = None,
) -> Path:
    ts = now or datetime.now(timezone.utc)
    stamp = ts.strftime("%Y%m%d-%H%M%S")
    return receipt_dir / f"{receipt_prefix}-{stamp}.json"


def write_receipt(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
