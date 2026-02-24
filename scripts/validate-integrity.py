#!/usr/bin/env python3
"""
Grace-Mar integrity validator.

Checks:
  1. SELF IX-A/B/C entries include evidence_id
  2. SELF evidence_id references resolve to EVIDENCE ACT-* entries
  3. EVIDENCE ACT entries include required fields and evidence_tier >= minimum
  4. Optional artifact references resolve and sha256 matches when provided
  5. PENDING-REVIEW candidates have required shape
  6. ID format and required section shape checks for SELF/SKILLS

Usage:
  python scripts/validate-integrity.py
  python scripts/validate-integrity.py --user pilot-001
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
        self_path = user_dir / "SELF.md"
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
        ev_path = user_dir / "EVIDENCE.md"
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


def validate_pending_review(user_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    allowed_mind_categories = {"knowledge", "curiosity", "personality"}
    for user_dir in user_dirs:
        pr_path = user_dir / "PENDING-REVIEW.md"
        content = _safe_read(pr_path)
        if "## Candidates" not in content:
            continue
        candidates_section = content.split("## Processed")[0]
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
        for fname in ("SELF.md", "EVIDENCE.md", "PENDING-REVIEW.md"):
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
        path = user_dir / "SELF.md"
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
    required = ["## I. CONTAINER STATUS", "## II. CAPABILITY CLAIMS", "## III. CAPABILITY GAPS"]
    for user_dir in user_dirs:
        path = user_dir / "SKILLS.md"
        content = _safe_read(path)
        if not content:
            continue
        for marker in required:
            if marker not in content:
                errors.append(f"{path.relative_to(REPO_ROOT)} missing required section '{marker}'")
    return errors


def run_validation(users_dir: Path, user: str | None, min_evidence_tier: int) -> list[str]:
    user_dirs = _iter_user_dirs(users_dir, user)
    if not user_dirs:
        return [f"No user directories found for users_dir={users_dir} user={user or '(all)'}"]

    all_errors: list[str] = []
    self_errors, evidence_ids = validate_self(user_dirs)
    all_errors.extend(self_errors)
    ev_errors, act_ids = validate_evidence(user_dirs, min_evidence_tier=min_evidence_tier)
    all_errors.extend(ev_errors)
    all_errors.extend(validate_cross_ref(evidence_ids, act_ids))
    all_errors.extend(validate_pending_review(user_dirs))
    all_errors.extend(validate_id_format(user_dirs))
    all_errors.extend(validate_self_sections(user_dirs))
    all_errors.extend(validate_skills_sections(user_dirs))
    return all_errors


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
    args = parser.parse_args()

    users_dir = Path(args.users_dir)
    if not users_dir.exists():
        payload = {"ok": False, "errors": [f"Users dir not found: {users_dir}"]}
        if args.json:
            print(json.dumps(payload))
        else:
            print(payload["errors"][0], file=sys.stderr)
        return 1

    errors = run_validation(users_dir, args.user.strip() or None, args.min_evidence_tier)
    ok = not errors
    if args.json:
        print(json.dumps({"ok": ok, "errors": errors}, ensure_ascii=True))
    else:
        if ok:
            print("Integrity check passed.")
        else:
            print("Integrity check FAILED:\n")
            for err in errors:
                print(f"  - {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
