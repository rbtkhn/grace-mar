"""
Canonical inventory for scripts/validate.py — check ids, argv builders, user scope, groups.

Source of truth for CI parity (`.github/workflows/test.yml` validation steps) and
orchestrator groups. Update when CI workflows change.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

UserScope = Literal["required", "ignored", "optional"]


@dataclass(frozen=True)
class CheckSpec:
    """One subprocess check."""

    id: str
    label: str
    """Path relative to repo root."""
    script_relpath: str
    argv_builder: Callable[[str], list[str]]
    user_scope: UserScope
    groups: frozenset[str]
    timeout_sec: float = 120.0
    requires_network: bool = False
    requires_openai: bool = False
    ci_source: str = ""


def _argv_paths(user: str) -> list[str]:
    return ["--user", user]


def _argv_integrity_ci(user: str) -> list[str]:
    return ["--user", user, "--require-proposal-class"]


def _argv_governance(_user: str) -> list[str]:
    return []


def _argv_template_sync(_user: str) -> list[str]:
    return []


def _argv_work_dev_cp(_user: str) -> list[str]:
    return []


def _argv_measure_growth(user: str) -> list[str]:
    return ["--user", user]


def _argv_measure_uniqueness(_user: str) -> list[str]:
    return ["--limit", "3"]


def _argv_boundary(user: str) -> list[str]:
    return ["--user", user]


def _argv_evidence_refs(user: str) -> list[str]:
    return ["--user", user]


def _argv_validate_skills(_user: str) -> list[str]:
    return []


def _argv_seed_phase_template(_user: str) -> list[str]:
    return ["users/_template/seed-phase", "--allow-placeholders"]


ALL_CHECKS: tuple[CheckSpec, ...] = (
    CheckSpec(
        id="assert_canonical_paths",
        label="Canonical user paths",
        script_relpath="scripts/assert_canonical_paths.py",
        argv_builder=_argv_paths,
        user_scope="required",
        groups=frozenset({"ci", "fast", "full"}),
        timeout_sec=60.0,
        ci_source=".github/workflows/test.yml (Assert canonical paths)",
    ),
    CheckSpec(
        id="validate_integrity",
        label="Record integrity",
        script_relpath="scripts/validate-integrity.py",
        argv_builder=_argv_integrity_ci,
        user_scope="required",
        groups=frozenset({"ci", "full"}),
        timeout_sec=180.0,
        ci_source=".github/workflows/test.yml (Validate integrity)",
    ),
    CheckSpec(
        id="validate_template_sync_contract",
        label="Template sync contract",
        script_relpath="scripts/validate_template_sync_contract.py",
        argv_builder=_argv_template_sync,
        user_scope="ignored",
        groups=frozenset({"ci", "full"}),
        timeout_sec=120.0,
        ci_source=".github/workflows/test.yml (Validate template sync contract)",
    ),
    CheckSpec(
        id="governance_checker",
        label="Governance scan (repo-wide)",
        script_relpath="scripts/governance_checker.py",
        argv_builder=_argv_governance,
        user_scope="ignored",
        groups=frozenset({"ci", "fast", "full"}),
        timeout_sec=120.0,
        ci_source=".github/workflows/test.yml (Governance check)",
    ),
    CheckSpec(
        id="validate_structured_files",
        label="Structured governance files (JSON/TOML/YAML/links)",
        script_relpath="scripts/validate_structured_files.py",
        argv_builder=_argv_governance,
        user_scope="ignored",
        groups=frozenset({"ci", "fast", "full"}),
        timeout_sec=120.0,
        ci_source=".github/workflows/test.yml (Validate structured files)",
    ),
    CheckSpec(
        id="validate_control_plane",
        label="Work-dev control plane",
        script_relpath="scripts/work_dev/validate_control_plane.py",
        argv_builder=_argv_work_dev_cp,
        user_scope="ignored",
        groups=frozenset({"ci", "full"}),
        timeout_sec=120.0,
        ci_source=".github/workflows/test.yml (Validate work-dev control plane)",
    ),
    CheckSpec(
        id="validate_identity_library_boundary",
        label="Identity / library boundary",
        script_relpath="scripts/validate_identity_library_boundary.py",
        argv_builder=_argv_boundary,
        user_scope="required",
        groups=frozenset({"fast"}),
        timeout_sec=90.0,
        ci_source="",
    ),
    CheckSpec(
        id="validate_ix_evidence_refs",
        label="IX evidence refs",
        script_relpath="scripts/validate_ix_evidence_refs.py",
        argv_builder=_argv_evidence_refs,
        user_scope="required",
        groups=frozenset({"fast"}),
        timeout_sec=90.0,
        ci_source="",
    ),
    CheckSpec(
        id="measure_growth_and_density",
        label="Growth and density metrics",
        script_relpath="scripts/measure_growth_and_density.py",
        argv_builder=_argv_measure_growth,
        user_scope="required",
        groups=frozenset({"full"}),
        timeout_sec=120.0,
        ci_source="",
    ),
    CheckSpec(
        id="measure_uniqueness",
        label="Uniqueness vs baseline (OpenAI API)",
        script_relpath="scripts/measure_uniqueness.py",
        argv_builder=_argv_measure_uniqueness,
        user_scope="ignored",
        groups=frozenset({"expensive"}),
        timeout_sec=300.0,
        requires_network=True,
        requires_openai=True,
        ci_source="",
    ),
    CheckSpec(
        id="validate_skills",
        label="Skills index validation",
        script_relpath="scripts/validate_skills.py",
        argv_builder=_argv_validate_skills,
        user_scope="ignored",
        groups=frozenset({"experimental"}),
        timeout_sec=120.0,
        ci_source="",
    ),
    CheckSpec(
        id="validate_seed_phase_template",
        label="Seed phase (_template fixture)",
        script_relpath="scripts/validate-seed-phase.py",
        argv_builder=_argv_seed_phase_template,
        user_scope="ignored",
        groups=frozenset({"experimental"}),
        timeout_sec=180.0,
        ci_source="",
    ),
)


def _by_id() -> dict[str, CheckSpec]:
    return {c.id: c for c in ALL_CHECKS}


def checks_for_group(group: str) -> list[CheckSpec]:
    g = group.strip().lower()
    by_id = _by_id()
    if g == "ci":
        order = [
            "assert_canonical_paths",
            "validate_integrity",
            "validate_template_sync_contract",
            "governance_checker",
            "validate_structured_files",
            "validate_control_plane",
        ]
        return [by_id[i] for i in order]
    if g == "fast":
        order = [
            "assert_canonical_paths",
            "validate_identity_library_boundary",
            "validate_ix_evidence_refs",
            "governance_checker",
            "validate_structured_files",
        ]
        return [by_id[i] for i in order]
    if g == "full":
        out = checks_for_group("ci")
        out = list(out) + [by_id["measure_growth_and_density"]]
        return out
    if g == "expensive":
        return [by_id["measure_uniqueness"]]
    if g == "experimental":
        order = ["validate_skills", "validate_seed_phase_template"]
        return [by_id[i] for i in order]
    out = [c for c in ALL_CHECKS if g in c.groups]
    return sorted(out, key=lambda x: x.id)


def default_user() -> str:
    import os

    env = os.environ.get("GRACE_MAR_USER_ID", "").strip()
    if env:
        return env
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    if (root / "users" / "grace-mar").is_dir():
        return "grace-mar"
    return "_template"
