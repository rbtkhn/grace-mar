#!/usr/bin/env python3
"""
Grace-Mar integrity validator.

Enforces **SELF-KNOWLEDGE vs SELF-LIBRARY**: IX-A topics must not look like corpus dumps
(length / keywords) — same rules as validate_identity_library_boundary (integrated here, not advisory-only).

Checks:
  1. SELF IX-A/B/C entries include evidence_id
  2. SELF evidence_id references resolve to EVIDENCE ACT-* entries
  3. EVIDENCE ACT entries include required fields and evidence_tier >= minimum
  4. Optional artifact references resolve and sha256 matches when provided
  5. recursion-gate candidates have required shape
  6. ID format and required section shape checks for SELF/SKILLS
  7. Derived export freshness and runtime portability contract checks
  8. SELF-KNOWLEDGE vs SELF-LIBRARY — IX-A topic length / corpus keywords (identity/library boundary)
  9. recursion-gate proposal_class value valid when present
  10. Optional --strict-self-library: fail if self-library.md missing
  11. Library Domain Registry (docs/self-library-domains.json) — required fields and routable domain ids

Human output prints an **Identity / library boundary** section first; JSON includes **identity_library_boundary**.

Usage:
  python scripts/validate-integrity.py
  python scripts/validate-integrity.py --user grace-mar
  python scripts/validate-integrity.py --users-dir users --json

Exit:
  0 if pass, 1 if any check fails.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
MIN_EVIDENCE_TIER = 3
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from recursion_gate_review import split_gate_sections
from validate_identity_library_boundary import (
    collect_identity_library_violations,
    collect_self_library_file_warnings,
)
from validate_library_domain_registry import validate_library_domain_registry
from repo_io import resolve_surface_markdown_path, self_skills_layout_warnings

ALLOWED_PROPOSAL_CLASS = frozenset({
    "SELF_KNOWLEDGE_ADD",
    "SELF_KNOWLEDGE_REVISE",
    "SELF_LIBRARY_ADD",
    "SELF_LIBRARY_REVISE",
    "CIV_MEM_ADD",
    "CIV_MEM_REVISE",
    "META_INFRA",
    "SIMULATION_RESULT",
})

VALID_FORK_PHASES = frozenset({"seed", "interact", "diverge", "merge_pending", "snapshotted"})
LIFECYCLE_ORIGINS = frozenset(
    {
        "seed_capture",
        "session_interaction",
        "operator_observation",
        "artifact_ingest",
        "parent_merge",
        "self_library_curation",
    }
)
LIFECYCLE_CLASSES = frozenset(
    {
        "fork_native",
        "real_world_update",
        "boundary_reclassification",
        "snapshot_only",
    }
)


def extract_yaml_blocks(content: str, section_marker: str | None = None) -> list[str]:
    """Extract YAML blocks from markdown. If section_marker given, only blocks after it."""
    if section_marker:
        idx = content.find(section_marker)
        if idx >= 0:
            content = content[idx:]
    pattern = r"```(?:yaml|yml)?\s*\n(.*?)```"
    return re.findall(pattern, content, re.DOTALL)


def parse_yaml_entries(block: str) -> list[dict]:
    """Naive YAML list parser for ACT/LEARN/CUR/PER candidate-style entries."""
    entries: list[dict] = []
    current: dict[str, str] = {}
    for line in block.splitlines():
        if line.strip().startswith("- "):
            if current and "id" in current:
                entries.append(current)
            current = {}
            match = re.match(r"\s*-\s+(\w+):\s*(.+)", line)
            if match:
                k, v = match.groups()
                current[k] = v.strip().strip("\"'")
            continue
        if current and line.strip() and ":" in line and not line.strip().startswith("#"):
            match = re.match(r"\s*(\w+):\s*(.+)", line)
            if match:
                k, v = match.groups()
                current[k] = v.strip().strip("\"'")
    if current and "id" in current:
        entries.append(current)
    return entries


def _iter_user_dirs(users_dir: Path, user: str | None) -> list[Path]:
    if user:
        target = users_dir / user
        return [target] if target.is_dir() else []
    return [p for p in users_dir.iterdir() if p.is_dir()]


def _safe_read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def validate_self(user_dirs: list[Path]) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    evidence_ids: set[str] = set()
    for user_dir in user_dirs:
        self_path = user_dir / "self.md"
        content = _safe_read(self_path)
        if not content:
            continue
        for section, marker in [
            ("IX-A. KNOWLEDGE", "### IX-A. KNOWLEDGE"),
            ("IX-B. CURIOSITY", "### IX-B. CURIOSITY"),
            ("IX-C. PERSONALITY", "### IX-C. PERSONALITY"),
        ]:
            if marker not in content:
                continue
            for block in extract_yaml_blocks(content, marker):
                for entry in parse_yaml_entries(block):
                    eid = entry.get("id", "?")
                    evidence_id = entry.get("evidence_id", "").strip()
                    if not evidence_id:
                        errors.append(f"{self_path.relative_to(REPO_ROOT)} {section}: {eid} missing evidence_id")
                    else:
                        evidence_ids.add(evidence_id)
    return errors, evidence_ids


def validate_evidence(user_dirs: list[Path], min_evidence_tier: int) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    act_ids: set[str] = set()
    for user_dir in user_dirs:
        ev_path = user_dir / "self-archive.md"
        content = _safe_read(ev_path)
        if not content.strip():
            ev_path = user_dir / "self-evidence.md"
            content = _safe_read(ev_path)
        if "## V. ACTIVITY LOG" not in content:
            continue

        idx = content.find("## V. ACTIVITY LOG")
        blocks = extract_yaml_blocks(content[idx:])
        for block in blocks:
            for m in re.finditer(r"-\s+id:\s*(ACT-\d+)(.*?)(?=\n\s*-\s+id:\s*ACT-|\Z)", block, re.DOTALL):
                act_id, chunk = m.groups()
                act_ids.add(act_id)
                for field in ("date:", "source:", "activity_type:"):
                    if field not in chunk:
                        errors.append(f"{ev_path.relative_to(REPO_ROOT)} {act_id} missing required field {field[:-1]}")

                tier_match = re.search(r"evidence_tier:\s*(\d+)", chunk)
                if not tier_match:
                    errors.append(f"{ev_path.relative_to(REPO_ROOT)} {act_id} missing evidence_tier")
                else:
                    tier = int(tier_match.group(1))
                    # Enforce stricter minimum for pipeline-generated merges while allowing legacy evidence.
                    is_pipeline_merge = "source: pipeline merge" in chunk
                    if is_pipeline_merge and tier < min_evidence_tier:
                        errors.append(
                            f"{ev_path.relative_to(REPO_ROOT)} {act_id} evidence_tier {tier} below minimum {min_evidence_tier}"
                        )

                artifact_path_match = re.search(r"artifact_path:\s*([^\n]+)", chunk)
                artifact_sha_match = re.search(r"artifact_sha256:\s*([a-fA-F0-9]{64})", chunk)
                if artifact_path_match:
                    raw = artifact_path_match.group(1).strip().strip("\"'")
                    candidate_path = Path(raw)
                    resolved = candidate_path if candidate_path.is_absolute() else REPO_ROOT / raw
                    if not resolved.exists():
                        errors.append(f"{ev_path.relative_to(REPO_ROOT)} {act_id} artifact_path not found: {raw}")
                    elif artifact_sha_match:
                        expected = artifact_sha_match.group(1).lower()
                        actual = _sha256_file(resolved).lower()
                        if actual != expected:
                            errors.append(
                                f"{ev_path.relative_to(REPO_ROOT)} {act_id} artifact_sha256 mismatch for {raw}"
                            )
                elif artifact_sha_match:
                    errors.append(f"{ev_path.relative_to(REPO_ROOT)} {act_id} has artifact_sha256 without artifact_path")
    return errors, act_ids


def validate_recursion_gate(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    allowed_mind_categories = {"knowledge", "curiosity", "personality"}
    for user_dir in user_dirs:
        pr_path = user_dir / "recursion-gate.md"
        content = _safe_read(pr_path)
        if "## Candidates" not in content:
            continue
        if "## Processed" in content:
            candidates_section, after_processed = split_gate_sections(content)
            for m in re.finditer(
                r"### (CANDIDATE-\d+)\s*\n```yaml\s*\n(.*?)```", after_processed, re.DOTALL
            ):
                blk = m.group(2)
                if re.search(r"^status:\s*pending\s*$", blk, re.MULTILINE):
                    errors.append(
                        f"{pr_path.relative_to(REPO_ROOT)} {m.group(1)} pending below ## Processed "
                        f"(merge only scans above Processed — move block up)"
                    )
        candidates_section, _processed_section = split_gate_sections(content)
        for m in re.finditer(r"### (CANDIDATE-\d+)\s*\n```yaml\s*\n(.*?)```", candidates_section, re.DOTALL):
            cid, yaml_block = m.groups()
            if "status:" not in yaml_block:
                errors.append(f"{pr_path.relative_to(REPO_ROOT)} {cid} missing status")
            elif "status: pending" in yaml_block and ("mind_category:" not in yaml_block or "summary:" not in yaml_block):
                errors.append(f"{pr_path.relative_to(REPO_ROOT)} {cid} missing mind_category or summary")
            mind_m = re.search(r"^mind_category:\s*([^\n]+)", yaml_block, re.MULTILINE)
            if mind_m:
                mind_category = mind_m.group(1).strip().strip("\"'").lower()
                if mind_category not in allowed_mind_categories:
                    errors.append(
                        f"{pr_path.relative_to(REPO_ROOT)} {cid} invalid mind_category '{mind_category}'"
                    )
    return errors


def validate_gate_proposal_class(
    user_dirs: list[Path], *, require_proposal_class: bool
) -> list[str]:
    errors: list[str] = []
    for user_dir in user_dirs:
        pr_path = user_dir / "recursion-gate.md"
        content = _safe_read(pr_path)
        if "## Candidates" not in content:
            continue
        candidates_section, _ = split_gate_sections(content)
        for m in re.finditer(
            r"### (CANDIDATE-\d+)\s*\n```yaml\s*\n(.*?)```", candidates_section, re.DOTALL
        ):
            cid, yaml_block = m.groups()
            if "status: pending" not in yaml_block:
                continue
            pcm = re.search(r"^proposal_class:\s*(\S+)\s*$", yaml_block, re.MULTILINE)
            if pcm:
                v = pcm.group(1).strip().strip("\"'")
                if v not in ALLOWED_PROPOSAL_CLASS:
                    errors.append(
                        f"{pr_path.relative_to(REPO_ROOT)} {cid} invalid proposal_class "
                        f"'{v}' (see identity-fork-protocol §3.5)"
                    )
            elif require_proposal_class:
                errors.append(
                    f"{pr_path.relative_to(REPO_ROOT)} {cid} pending: missing proposal_class "
                    f"(use --no-require-proposal-class or add proposal_class per IFP §3.5)"
                )
    return errors


def validate_cross_ref(evidence_ids: set[str], act_ids: set[str]) -> list[str]:
    return [f"Orphan evidence_id reference: {eid}" for eid in sorted(evidence_ids) if eid not in act_ids]


ID_PATTERNS = {
    "LEARN": re.compile(r"LEARN-\d{4}$"),
    "CUR": re.compile(r"CUR-\d{4}$"),
    "PER": re.compile(r"PER-\d{4}$"),
    "ACT": re.compile(r"ACT-\d{4}$"),
    "CANDIDATE": re.compile(r"CANDIDATE-\d{4}$"),
}


def validate_id_format(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    for user_dir in user_dirs:
        for fname in ("self.md", "self-archive.md", "recursion-gate.md"):
            path = user_dir / fname
            content = _safe_read(path)
            if not content:
                continue
            for prefix, pat in ID_PATTERNS.items():
                for m in re.finditer(rf"\b{prefix}-(\d+)\b", content):
                    full = f"{prefix}-{m.group(1)}"
                    if not pat.match(full):
                        errors.append(f"{path.relative_to(REPO_ROOT)}: {full} must be 4-digit")
    return errors


def validate_self_sections(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    required = ["## I.", "## II."]
    ix_sections = ["### IX-A.", "### IX-B.", "### IX-C."]
    for user_dir in user_dirs:
        path = user_dir / "self.md"
        content = _safe_read(path)
        if not content:
            continue
        for marker in required:
            if marker not in content:
                errors.append(f"{path.relative_to(REPO_ROOT)} missing required section {marker.strip()}")
        if "## IX." in content or "### IX-A." in content:
            for marker in ix_sections:
                if marker not in content:
                    errors.append(f"{path.relative_to(REPO_ROOT)} IX present but missing {marker.strip()}")
    return errors


def validate_skills_sections(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    skills_markers = ["## II. CAPABILITY CLAIMS", "## III. CAPABILITY GAPS"]
    skill_files = ["skill-think.md", "skill-write.md"]
    for user_dir in user_dirs:
        try:
            skills_path = resolve_surface_markdown_path(user_dir, "self_skills")
        except ValueError:
            continue
        content = _safe_read(skills_path)
        if not content:
            continue
        for marker in skills_markers:
            if marker not in content:
                errors.append(f"{skills_path.relative_to(REPO_ROOT)} missing required section '{marker}'")
        found = any((user_dir / f).exists() for f in skill_files)
        if not found:
            errors.append(f"{user_dir.relative_to(REPO_ROOT)} missing at least one of {skill_files}")
    return errors


def validate_derived_exports(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    prompt_path = REPO_ROOT / "bot" / "prompt.py"
    for user_dir in user_dirs:
        skills_path = resolve_surface_markdown_path(user_dir, "self_skills")
        source_paths = [
            user_dir / "self.md",
            skills_path,
            user_dir / "self-archive.md",
            user_dir / "self-library.md",
            user_dir / "intent.md",
            prompt_path,
        ]
        source_mtimes = [p.stat().st_mtime for p in source_paths if p.exists()]
        latest_source = max(source_mtimes, default=0)

        prp_path = REPO_ROOT / "grace-mar-llm.txt" if user_dir.name == "grace-mar" else user_dir / f"{user_dir.name}-llm.txt"
        derived_paths = [
            user_dir / "manifest.json",
            user_dir / "llms.txt",
            user_dir / "intent_snapshot.json",
            user_dir / "fork-manifest.json",
            prp_path,
        ]
        for path in derived_paths:
            if not path.exists():
                errors.append(f"Missing derived export: {path.relative_to(REPO_ROOT)}")
                continue
            if path.stat().st_mtime < latest_source:
                errors.append(f"Stale derived export: {path.relative_to(REPO_ROOT)}")

        manifest_path = user_dir / "manifest.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                errors.append(f"{manifest_path.relative_to(REPO_ROOT)} is not valid JSON")
            else:
                readable = set(manifest.get("readable") or [])
                required = {"SKILLS/THINK", "SKILLS/WRITE", "WORK/context", "INTENT/goals", "INTENT/tradeoff_rules"}
                missing = sorted(required - readable)
                if missing:
                    errors.append(
                        f"{manifest_path.relative_to(REPO_ROOT)} missing required readable surfaces: {', '.join(missing)}"
                    )
                deprecated = {"SKILLS/READ", "SKILLS/BUILD"} & readable
                if deprecated:
                    errors.append(
                        f"{manifest_path.relative_to(REPO_ROOT)} contains deprecated readable surfaces: {', '.join(sorted(deprecated))}"
                    )
                if not manifest.get("runtime_mode"):
                    errors.append(f"{manifest_path.relative_to(REPO_ROOT)} missing runtime_mode")
                degraded = manifest.get("degraded_mode")
                if not isinstance(degraded, dict) or "enabled" not in degraded:
                    errors.append(f"{manifest_path.relative_to(REPO_ROOT)} missing degraded_mode contract")

        bundle_dir = user_dir / "runtime-bundle"
        bundle_path = bundle_dir / "bundle.json"
        if bundle_path.exists():
            if bundle_path.stat().st_mtime < latest_source:
                errors.append(f"Stale runtime bundle: {bundle_path.relative_to(REPO_ROOT)}")
            try:
                bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                errors.append(f"{bundle_path.relative_to(REPO_ROOT)} is not valid JSON")
            else:
                for lane in ("record", "runtime", "audit", "policy"):
                    if lane not in (bundle.get("lanes") or {}):
                        errors.append(f"{bundle_path.relative_to(REPO_ROOT)} missing lane '{lane}'")
                degraded = bundle.get("degraded_mode")
                if not isinstance(degraded, dict) or "enabled" not in degraded:
                    errors.append(f"{bundle_path.relative_to(REPO_ROOT)} missing degraded_mode contract")
    return errors


def _yaml_scalar(block: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.+?)(?:\n|$)", block, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip('"\'')


def validate_fork_lifecycle(
    user_dirs: list[Path],
    *,
    strict: bool,
) -> tuple[list[str], list[str], dict]:
    """fork_state.json presence/phase; optional strict pending-candidate lineage fields."""
    errors: list[str] = []
    warnings: list[str] = []
    info: dict[str, dict] = {}
    for ud in user_dirs:
        fid = ud.name
        fs_path = ud / "fork_state.json"
        if not fs_path.is_file():
            warnings.append(
                f"{fid}: fork_state.json missing — run: python scripts/fork_lifecycle.py init -u {fid}"
            )
            info[fid] = {"phase": None, "drift_score": None}
            continue
        try:
            data = json.loads(fs_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            errors.append(f"{fs_path.relative_to(REPO_ROOT)}: invalid fork_state.json ({e})")
            continue
        phase = str(data.get("phase") or "")
        if phase not in VALID_FORK_PHASES:
            errors.append(f"{fid}: fork_state.json invalid phase {phase!r}")
        drift = data.get("drift_score")
        try:
            drift_f = float(drift) if drift is not None else None
        except (TypeError, ValueError):
            drift_f = None
        info[fid] = {"phase": phase, "drift_score": drift_f}

        drift_path = ud / "drift-report.json"
        if strict and drift_path.is_file():
            try:
                dr = json.loads(drift_path.read_text(encoding="utf-8"))
                age = dr.get("computed_at")
                if not age:
                    warnings.append(f"{fid}: drift-report.json missing computed_at")
            except (json.JSONDecodeError, OSError):
                errors.append(f"{fid}: drift-report.json unreadable")

        if not strict:
            continue
        gate_path = ud / "recursion-gate.md"
        content = _safe_read(gate_path)
        if "## Candidates" not in content:
            continue
        candidates_section, _ = split_gate_sections(content)
        for m in re.finditer(
            r"### (CANDIDATE-\d+).*?```yaml\n(.*?)```", candidates_section, re.DOTALL
        ):
            cid, yaml_block = m.group(1), m.group(2)
            if "status: pending" not in yaml_block:
                continue
            origin = _yaml_scalar(yaml_block, "origin")
            lclass = _yaml_scalar(yaml_block, "lineage_class")
            sid = _yaml_scalar(yaml_block, "session_id")
            ops = _yaml_scalar(yaml_block, "operator_source")
            if not origin or origin not in LIFECYCLE_ORIGINS:
                errors.append(f"{cid}: pending candidate missing or invalid origin (strict-lifecycle)")
            if not lclass or lclass not in LIFECYCLE_CLASSES:
                errors.append(f"{cid}: pending candidate missing or invalid lineage_class (strict-lifecycle)")
            if not sid and not ops:
                errors.append(f"{cid}: pending candidate needs session_id or operator_source (strict-lifecycle)")
    return errors, warnings, info


def run_validation(
    users_dir: Path,
    user: str | None,
    min_evidence_tier: int,
    *,
    require_proposal_class: bool = False,
    strict_self_library: bool = False,
    strict_lifecycle: bool = False,
) -> tuple[list[str], dict]:
    user_dirs = _iter_user_dirs(users_dir, user)
    if not user_dirs:
        msg = f"No user directories found for users_dir={users_dir} user={user or '(all)'}"
        return [msg], {
            "ix_a_violations": [],
            "self_library_missing_warnings": [],
            "surface_layout_warnings": [],
            "ix_a_ok": True,
            "self_library_files_ok": True,
        }

    all_errors: list[str] = []
    all_errors.extend(validate_library_domain_registry(REPO_ROOT))

    ix_boundary: list[str] = []
    for ud in user_dirs:
        ix_boundary.extend(collect_identity_library_violations(ud, repo_root=REPO_ROOT))

    library_warnings: list[str] = []
    for ud in user_dirs:
        library_warnings.extend(collect_self_library_file_warnings(ud, REPO_ROOT))

    surface_layout_warnings: list[str] = []
    for ud in user_dirs:
        surface_layout_warnings.extend(self_skills_layout_warnings(ud))

    all_errors.extend(ix_boundary)
    if strict_self_library:
        all_errors.extend(library_warnings)

    self_errors, evidence_ids = validate_self(user_dirs)
    all_errors.extend(self_errors)
    ev_errors, act_ids = validate_evidence(user_dirs, min_evidence_tier=min_evidence_tier)
    all_errors.extend(ev_errors)
    all_errors.extend(validate_cross_ref(evidence_ids, act_ids))
    all_errors.extend(validate_recursion_gate(user_dirs))
    all_errors.extend(
        validate_gate_proposal_class(user_dirs, require_proposal_class=require_proposal_class)
    )
    all_errors.extend(validate_id_format(user_dirs))
    all_errors.extend(validate_self_sections(user_dirs))
    all_errors.extend(validate_skills_sections(user_dirs))
    all_errors.extend(validate_derived_exports(user_dirs))

    lc_errors, lc_warnings, lc_info = validate_fork_lifecycle(user_dirs, strict=strict_lifecycle)
    all_errors.extend(lc_errors)
    lifecycle_report = {
        "phase": {k: v.get("phase") for k, v in lc_info.items()},
        "drift_score": {k: v.get("drift_score") for k, v in lc_info.items()},
        "errors": lc_errors,
        "warnings": lc_warnings,
    }

    boundary_report = {
        "ix_a_violations": ix_boundary,
        "self_library_missing_warnings": library_warnings,
        "surface_layout_warnings": surface_layout_warnings,
        "ix_a_ok": len(ix_boundary) == 0,
        "self_library_files_ok": len(library_warnings) == 0,
        "fork_lifecycle": lifecycle_report,
    }
    return all_errors, boundary_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Grace-Mar record integrity.")
    parser.add_argument("--users-dir", default=str(DEFAULT_USERS_DIR), help="Users directory path")
    parser.add_argument("--user", default="", help="Validate only one user id")
    parser.add_argument(
        "--min-evidence-tier",
        type=int,
        default=MIN_EVIDENCE_TIER,
        help=f"Minimum allowed evidence_tier (default: {MIN_EVIDENCE_TIER})",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    parser.add_argument("--changed-only", action="store_true", help="Reserved for CI mode")
    parser.add_argument(
        "--require-proposal-class",
        action="store_true",
        help="Fail if any pending gate candidate omits proposal_class (IFP §3.5)",
    )
    parser.add_argument(
        "--strict-self-library",
        action="store_true",
        help="Fail if self.md exists but self-library.md is missing (CMC/LIB surface)",
    )
    parser.add_argument(
        "--strict-lifecycle",
        action="store_true",
        help="Enforce fork_state.json, pending candidate lineage fields, drift report shape",
    )
    args = parser.parse_args()

    users_dir = Path(args.users_dir)
    if not users_dir.exists():
        payload = {"ok": False, "errors": [f"Users dir not found: {users_dir}"]}
        if args.json:
            print(json.dumps(payload))
        else:
            print(payload["errors"][0], file=sys.stderr)
        return 1

    errors, boundary = run_validation(
        users_dir,
        args.user.strip() or None,
        args.min_evidence_tier,
        require_proposal_class=args.require_proposal_class,
        strict_self_library=args.strict_self_library,
        strict_lifecycle=args.strict_lifecycle,
    )
    ok = not errors
    if args.json:
        payload = {
            "ok": ok,
            "errors": errors,
            "identity_library_boundary": boundary,
            "surface_layout_warnings": boundary.get("surface_layout_warnings") or [],
            "fork_lifecycle": boundary.get("fork_lifecycle") or {},
        }
        print(json.dumps(payload, ensure_ascii=True))
    else:
        print("=== Identity / library boundary (SELF-KNOWLEDGE vs SELF-LIBRARY) ===")
        if boundary.get("ix_a_ok"):
            print("  IX-A / SELF-KNOWLEDGE: OK (no corpus dumps or CIV-MEM path leakage in topics).")
        else:
            for v in boundary.get("ix_a_violations") or []:
                print(f"  FAIL: {v}")
        if boundary.get("self_library_files_ok"):
            print("  self-library.md: present for all forks with self.md.")
        else:
            for w in boundary.get("self_library_missing_warnings") or []:
                tag = "FAIL" if args.strict_self_library else "WARN"
                print(f"  {tag}: {w}")
        for w in boundary.get("surface_layout_warnings") or []:
            print(f"  WARN (surface layout): {w}")
        print()
        if ok:
            print("Integrity check passed (all checks).")
        else:
            print("Integrity check FAILED:\n")
            for err in errors:
                print(f"  - {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
