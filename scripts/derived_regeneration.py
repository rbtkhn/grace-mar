"""Shared helpers for repo-owned derived regeneration."""

from __future__ import annotations

import fnmatch
import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECEIPT_DIR = REPO_ROOT / "artifacts" / "work-dev" / "rebuild-receipts"
RATIONALE_SCHEMA_ID = "schema-registry/derived-artifact-rationale.v1.json"
RATIONALE_SCHEMA_VERSION = "1.0.0-derived-artifact-rationale"
RATIONALE_SIDECAR_SUFFIX = ".derived-rationale.json"


@dataclass(frozen=True)
class RebuildTarget:
    target_id: str
    description: str
    producer_script: str
    policy_mode: str
    rationale: str
    watch_patterns: tuple[str, ...]
    command_templates: tuple[tuple[str, ...], ...]
    outputs: tuple[str, ...]
    depends_on: tuple[str, ...] = ()
    human_review_required: bool = False
    owned_output_patterns: tuple[str, ...] = ()

    def commands_for_user(self, user: str) -> list[list[str]]:
        return [
            [part.format(user=user) for part in template]
            for template in self.command_templates
        ]

    def outputs_for_user(self, user: str) -> list[str]:
        return [part.format(user=user) for part in self.outputs]

    def owned_output_patterns_for_user(self, user: str) -> list[str]:
        patterns = self.owned_output_patterns or self.outputs
        return [part.format(user=user) for part in patterns]


TARGETS: tuple[RebuildTarget, ...] = (
    RebuildTarget(
        target_id="derived-regeneration-manifest",
        description="Machine-readable manifest of repo-owned derived rebuild targets",
        producer_script="scripts/build_derived_regeneration_manifest.py",
        policy_mode="Rebuild",
        rationale="Capture the current rebuild target registry in one inspectable manifest so incremental regeneration stays explicit and bounded.",
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
        producer_script="scripts/build_library_index.py",
        policy_mode="Surface",
        rationale="Surface SELF-LIBRARY coverage as a derived navigation dashboard without changing canonical library truth.",
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
        producer_script="scripts/build_work_lanes_dashboard.py",
        policy_mode="Rebuild",
        rationale="Aggregate lane telemetry into a machine-readable feed that downstream operator dashboards can rebuild from without touching Record files.",
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
        producer_script="scripts/build_lane_dashboards.py",
        policy_mode="Surface",
        rationale="Compose runtime observations and work-lane telemetry into a derived operator dashboard for navigation across active lanes.",
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
        outputs=("artifacts/lane-dashboards/README.md",),
        depends_on=("work-lanes-dashboard-json",),
    ),
    RebuildTarget(
        target_id="review-dashboard",
        description="Review dashboard derived from recursion-gate",
        producer_script="scripts/build_review_dashboard.py",
        policy_mode="Surface",
        rationale="Provide a compact operator view of pending and recently processed gate candidates while keeping recursion-gate.md authoritative.",
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
        producer_script="scripts/build_gate_board.py",
        policy_mode="Surface",
        rationale="Translate gate candidate state into a dashboard board for operator triage without changing candidate status or merge authority.",
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
        producer_script="scripts/report_governance_posture.py",
        policy_mode="Surface",
        rationale="Summarize governance posture and audit paths in a derived one-pager for operator or partner review.",
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
        human_review_required=True,
    ),
    RebuildTarget(
        target_id="strategy-notebook-graph",
        description="Strategy-notebook graph and derived views",
        producer_script="scripts/build_strategy_notebook_graph.py",
        policy_mode="Strategy",
        rationale="Project markdown-canonical strategy notebook structure into derived graph views for orientation, clustering, and navigation.",
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
    RebuildTarget(
        target_id="work-dev-compound-autoresearch",
        description="Work-dev compound and Autoresearch operator summaries",
        producer_script="scripts/build_work_dev_compound_dashboard.py",
        policy_mode="Surface",
        rationale="Rebuild work-dev compound dashboards and exports when compound notes or Autoresearch run notes change, keeping research scaffolding inspectable without Record authority.",
        watch_patterns=(
            "docs/skill-work/work-dev/compound-notes/**",
            "docs/skill-work/work-dev/autoresearch-runs/**",
            "scripts/work_dev_compound_refresh.py",
            "scripts/export_work_dev_compound_gate_candidates.py",
            "scripts/build_work_dev_compound_dashboard.py",
            "scripts/work_dev/compound_notes.py",
        ),
        command_templates=(
            ("python3", "scripts/work_dev_compound_refresh.py"),
            ("python3", "scripts/export_work_dev_compound_gate_candidates.py"),
            ("python3", "scripts/build_work_dev_compound_dashboard.py"),
        ),
        outputs=(
            "artifacts/work-dev-compound-refresh.md",
            "artifacts/work-dev-compound-gate-candidates.md",
            "artifacts/work-dev-compound-dashboard.md",
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


def sidecar_path_for_artifact(artifact_path: str) -> str:
    return f"{normalize_rel_path(artifact_path)}{RATIONALE_SIDECAR_SUFFIX}"


def build_rebuild_command(target: RebuildTarget, user: str) -> str:
    commands = target.commands_for_user(user)
    return " && ".join(" ".join(shlex.quote(part) for part in command) for command in commands)


def build_rationale_payload(
    *,
    target: RebuildTarget,
    user: str,
    artifact_path: str,
    generated_at: str,
    matched_paths: list[str],
) -> dict:
    inputs = matched_paths or [normalize_rel_path(path) for path in target.watch_patterns]
    payload: dict[str, object] = {
        "$schema": RATIONALE_SCHEMA_ID,
        "schemaVersion": RATIONALE_SCHEMA_VERSION,
        "producer_script": target.producer_script,
        "policy_mode": target.policy_mode,
        "generated_at": generated_at,
        "artifact_path": normalize_rel_path(artifact_path),
        "canonical_surfaces_touched": False,
        "rebuild_command": build_rebuild_command(target, user),
        "inputs": inputs,
        "rationale": target.rationale,
        "human_review_required": target.human_review_required,
    }
    return payload


def cleanup_owned_outputs(repo_root: Path, *, target: RebuildTarget, user: str) -> list[str]:
    cleaned: list[str] = []
    for pattern in target.owned_output_patterns_for_user(user):
        rel_pattern = normalize_rel_path(pattern)
        if not any(char in rel_pattern for char in "*?[]"):
            continue
        for path in sorted(repo_root.glob(rel_pattern)):
            if path.name == ".gitkeep" or not path.is_file():
                continue
            path.unlink()
            cleaned.append(normalize_rel_path(path.relative_to(repo_root).as_posix()))
            sidecar_path = repo_root / sidecar_path_for_artifact(path.relative_to(repo_root).as_posix())
            if sidecar_path.is_file():
                sidecar_path.unlink()
                cleaned.append(normalize_rel_path(sidecar_path.relative_to(repo_root).as_posix()))
    return cleaned


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
                "producerScript": target.producer_script,
                "policyMode": target.policy_mode,
                "humanReviewRequired": target.human_review_required,
                "watchPatterns": list(target.watch_patterns),
                "commands": [" ".join(cmd) for cmd in target.command_templates],
                "outputs": list(target.outputs),
                "rationaleSidecars": [sidecar_path_for_artifact(output) for output in target.outputs],
                "dependsOn": list(target.depends_on),
                "ownedOutputPatterns": list(target.owned_output_patterns or target.outputs),
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
