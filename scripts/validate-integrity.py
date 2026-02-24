#!/usr/bin/env python3
"""
Grace-Mar integrity validator.

Checks:
  1. SELF IX-A/B/C entries have evidence_id (LLM-leak guard)
  2. evidence_id references exist in EVIDENCE Activity Log
  3. ACT-* entries have required structure (id, date, source)
  4. PENDING-REVIEW pending candidates have status + required fields

Usage:
  python scripts/validate-integrity.py [users_dir]
  python scripts/validate-integrity.py --changed-only   # validate only if files changed (for CI)

Cron: Run nightly to catch integrity issues early:
  0 3 * * * cd /path/to/grace-mar && python3 scripts/validate-integrity.py || alert_on_failure

Exit: 0 if pass, 1 if any check fails.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"


def extract_yaml_blocks(content: str, section_marker: str | None = None) -> list[str]:
    """Extract YAML blocks from markdown. If section_marker given, only blocks after it."""
    if section_marker:
        idx = content.find(section_marker)
        if idx >= 0:
            content = content[idx:]
    pattern = r"```(?:yaml|yml)?\s*\n(.*?)```"
    return re.findall(pattern, content, re.DOTALL)


def parse_yaml_entries(block: str) -> list[dict]:
    """Naive YAML parsing for entries list. Returns list of dicts with id, evidence_id, etc."""
    entries = []
    current = {}
    for line in block.splitlines():
        if line.strip().startswith("- "):
            if current and "id" in current:
                entries.append(current)
            current = {}
            # Parse first line of entry, e.g. "  - id: LEARN-0001"
            match = re.match(r'\s*-\s+(\w+):\s*(.+)', line)
            if match:
                k, v = match.groups()
                current[k] = v.strip().strip('"\'')
        elif current and line.strip() and ":" in line and not line.strip().startswith("#"):
            match = re.match(r'\s*(\w+):\s*(.+)', line)
            if match:
                k, v = match.groups()
                current[k] = v.strip().strip('"\'')
    if current and "id" in current:
        entries.append(current)
    return entries


def validate_self(users_dir: Path) -> tuple[list[str], set[str]]:
    """Validate SELF.md. Returns (errors, evidence_ids_referenced)."""
    errors = []
    evidence_ids = set()

    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir():
            continue
        self_path = user_dir / "SELF.md"
        if not self_path.exists():
            continue

        content = self_path.read_text()

        for section, marker in [
            ("IX-A. KNOWLEDGE", "### IX-A. KNOWLEDGE"),
            ("IX-B. CURIOSITY", "### IX-B. CURIOSITY"),
            ("IX-C. PERSONALITY", "### IX-C. PERSONALITY"),
        ]:
            if marker not in content:
                continue
            blocks = extract_yaml_blocks(content, marker)
            for block in blocks:
                entries = parse_yaml_entries(block)
                for e in entries:
                    eid = e.get("id", "?")
                    if "evidence_id" not in e:
                        errors.append(f"SELF {section}: {eid} missing evidence_id (LLM-leak risk)")
                    else:
                        evidence_ids.add(e["evidence_id"])

    return errors, evidence_ids


def validate_evidence(users_dir: Path) -> tuple[list[str], set[str]]:
    """Validate EVIDENCE.md Activity Log. Returns (errors, act_ids)."""
    errors = []
    act_ids = set()

    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir():
            continue
        ev_path = user_dir / "EVIDENCE.md"
        if not ev_path.exists():
            continue

        content = ev_path.read_text()
        if "## V. ACTIVITY LOG" not in content:
            continue

        # Find activities YAML block
        idx = content.find("## V. ACTIVITY LOG")
        blocks = extract_yaml_blocks(content[idx:])
        for block in blocks:
            # Parse ACT-* entries
            for m in re.finditer(r"id:\s*(ACT-\d+)", block):
                act_ids.add(m.group(1))
            for m in re.finditer(r"-\s+id:\s*(ACT-\d+)", block):
                act_id = m.group(1)
                # Get the chunk for this entry
                start = m.start()
                end = block.find("\n  - id:", start + 1)
                if end < 0:
                    end = len(block)
                chunk = block[start:end]
                if "date:" not in chunk and "source:" not in chunk and "activity_type:" not in chunk:
                    errors.append(f"EVIDENCE: {act_id} missing required fields (date, source, or activity_type)")

    return errors, act_ids


def validate_pending_review(users_dir: Path) -> list[str]:
    """Validate PENDING-REVIEW.md. Returns errors."""
    errors = []

    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir():
            continue
        pr_path = user_dir / "PENDING-REVIEW.md"
        if not pr_path.exists():
            continue

        content = pr_path.read_text()

        # Find Candidates section
        if "## Candidates" not in content:
            continue

        candidates_section = content.split("## Processed")[0]
        # Each candidate block
        allowed_mind_categories = {"knowledge", "curiosity", "personality"}
        for m in re.finditer(r"### (CANDIDATE-\d+)\s*\n```yaml\s*\n(.*?)```", candidates_section, re.DOTALL):
            cid, yaml_block = m.groups()
            if "status:" not in yaml_block:
                errors.append(f"PENDING-REVIEW: {cid} missing status")
            elif "status: pending" in yaml_block:
                if "mind_category:" not in yaml_block and "summary:" not in yaml_block:
                    errors.append(f"PENDING-REVIEW: {cid} (pending) missing mind_category or summary")
            mind_m = re.search(r"^mind_category:\s*([^\n]+)", yaml_block, re.MULTILINE)
            if mind_m:
                mind_category = mind_m.group(1).strip().strip('"\'').lower()
                if mind_category not in allowed_mind_categories:
                    errors.append(
                        f"PENDING-REVIEW: {cid} invalid mind_category '{mind_category}' "
                        f"(allowed: knowledge, curiosity, personality)"
                    )

    return errors


def validate_cross_ref(evidence_ids: set[str], act_ids: set[str]) -> list[str]:
    """Check evidence_id references point to existing ACT-* entries."""
    errors = []
    for eid in evidence_ids:
        if eid not in act_ids:
            errors.append(f"Orphan reference: evidence_id {eid} not found in EVIDENCE Activity Log")
    return errors


# ID format per docs/ID-TAXONOMY.md: 4-digit zero-padded
ID_PATTERNS = {
    "LEARN": re.compile(r"LEARN-\d{4}$"),
    "CUR": re.compile(r"CUR-\d{4}$"),
    "PER": re.compile(r"PER-\d{4}$"),
    "ACT": re.compile(r"ACT-\d{4}$"),
    "CANDIDATE": re.compile(r"CANDIDATE-\d{4}$"),
}


def validate_id_format(users_dir: Path) -> list[str]:
    """Validate ID format (4-digit per ID-TAXONOMY). Returns errors."""
    errors = []

    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir():
            continue
        for fname in ("SELF.md", "EVIDENCE.md", "PENDING-REVIEW.md"):
            path = user_dir / fname
            if not path.exists():
                continue
            content = path.read_text()
            for prefix, pat in ID_PATTERNS.items():
                for m in re.finditer(rf"\b{prefix}-(\d+)\b", content):
                    full = f"{prefix}-{m.group(1)}"
                    if not pat.match(full):
                        errors.append(f"{path.relative_to(REPO_ROOT)}: {full} — ID must be 4-digit (e.g. {prefix}-0001)")

    return errors


def validate_self_sections(users_dir: Path) -> list[str]:
    """Validate SELF.md has required sections (I, II, IX or equivalent)."""
    errors = []
    required = ["## I.", "## II."]  # Identity, Preferences minimum
    ix_sections = ["### IX-A.", "### IX-B.", "### IX-C."]

    for user_dir in users_dir.iterdir():
        if not user_dir.is_dir():
            continue
        path = user_dir / "SELF.md"
        if not path.exists():
            continue
        content = path.read_text()
        for r in required:
            if r not in content:
                errors.append(f"{path.relative_to(REPO_ROOT)}: missing required section {r.strip()}")
        if "## IX." in content or "### IX-A." in content:
            for ix in ix_sections:
                if ix not in content:
                    errors.append(f"{path.relative_to(REPO_ROOT)}: IX present but missing {ix.strip()}")

    return errors


def main() -> int:
    users_dir = DEFAULT_USERS_DIR
    if len(sys.argv) > 1:
        if sys.argv[1] == "--changed-only":
            # For CI: could integrate with git diff; for now just run full validation
            pass
        else:
            users_dir = Path(sys.argv[1])

    if not users_dir.exists():
        print(f"Users dir not found: {users_dir}")
        return 1

    all_errors: list[str] = []

    self_errors, evidence_ids = validate_self(users_dir)
    all_errors.extend(self_errors)

    ev_errors, act_ids = validate_evidence(users_dir)
    all_errors.extend(ev_errors)

    all_errors.extend(validate_cross_ref(evidence_ids, act_ids))
    all_errors.extend(validate_pending_review(users_dir))
    all_errors.extend(validate_id_format(users_dir))
    all_errors.extend(validate_self_sections(users_dir))

    if all_errors:
        print("Integrity check FAILED:\n")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("Integrity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
