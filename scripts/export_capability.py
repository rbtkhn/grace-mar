#!/usr/bin/env python3
"""
Export a demonstrated-capability profile from Grace-Mar.

Filters SKILLS + EVIDENCE into a portfolio-shaped view with optional
artifact-rationale companions.  SELF is included as minimal identity
context only (name, age, lexile).  SELF-LIBRARY and Runtime are excluded.

Per the export contract, SKILLS and EVIDENCE are primary surfaces for
the ``capability`` export class.

Usage:
    python scripts/export_capability.py -u grace-mar
    python scripts/export_capability.py -u grace-mar -o capability.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from repo_io import read_path, REPO_ROOT, profile_dir, resolve_surface_markdown_path
except ImportError:
    from scripts.repo_io import read_path, REPO_ROOT, profile_dir, resolve_surface_markdown_path

RATIONALE_DIR = REPO_ROOT / "artifacts" / "rationales"
RATIONALE_REQUIRED_FIELDS = {"artifact_name", "task_type", "why_good", "transferable_pattern"}

CAPABILITY_ENTRY_PREFIXES = ("WRITE-", "CREATE-", "ACT-")
EXCLUDED_ENTRY_PREFIXES = ("READ-", "MEDIA-")

EXCLUDED_SENSITIVITY = {"non_portable", "non_exportable"}


# ── identity context (minimal) ─────────────────────────────────────────

def _parse_identity_context(self_content: str) -> dict:
    data: dict[str, str | int] = {"name": "?", "age": 0, "lexile_output": "?"}
    if m := re.search(r"name:\s*(\S+)", self_content):
        data["name"] = m.group(1)
    if m := re.search(r"age:\s*(\d+)", self_content):
        data["age"] = int(m.group(1))
    if m := re.search(r'lexile_output:\s*["\']?([^"\'\n]+)', self_content):
        data["lexile_output"] = m.group(1).strip()
    return data


# ── skills extraction ───────────────────────────────────────────────────

def _extract_yaml_list(content: str, section_heading: str) -> list[str]:
    """Extract items from a YAML list block under a markdown section."""
    start = content.find(section_heading)
    if start < 0:
        return []
    block = content[start:]
    end_match = re.search(r"\n## ", block[len(section_heading):])
    if end_match:
        block = block[:len(section_heading) + end_match.start()]

    yaml_match = re.search(r"```yaml\s*\n(.*?)```", block, re.DOTALL)
    if not yaml_match:
        return []
    yaml_body = yaml_match.group(1)

    list_match = re.search(r"\w+:\s*\[\s*\]", yaml_body)
    if list_match:
        return []

    items: list[str] = []
    for line in yaml_body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and not stripped.startswith("# "):
            items.append(stripped[2:].strip())
    return items


def _parse_skills(skills_content: str) -> dict:
    return {
        "claims": _extract_yaml_list(skills_content, "## II. CAPABILITY CLAIMS"),
        "gaps": _extract_yaml_list(skills_content, "## III. CAPABILITY GAPS"),
        "milestones": _extract_yaml_list(skills_content, "## V. MILESTONES"),
    }


# ── evidence extraction ─────────────────────────────────────────────────

def _extract_entries_by_prefix(evidence_content: str, prefix: str) -> list[dict]:
    """Extract YAML entry blocks for a given id prefix (e.g. WRITE-, CREATE-)."""
    entries: list[dict] = []
    pattern = re.compile(
        rf"  - id:\s+({re.escape(prefix)}\d+)\s*\n(.*?)(?=\n  - id:|\n```|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(evidence_content):
        entry_id = m.group(1)
        body = m.group(2)

        if _is_sensitivity_excluded(body):
            continue

        entry: dict[str, str | None] = {"id": entry_id}

        for field in ("date", "created_at", "type", "title", "description",
                      "evidence_tier", "activity_type", "topic", "evidence_subtype"):
            field_match = re.search(rf"^\s*{field}:\s*(.+)$", body, re.MULTILINE)
            if field_match:
                val = field_match.group(1).strip().strip("\"'")
                entry[field] = val

        summary_match = re.search(r"^\s*summary:\s*[>|]?\s*\n(\s+.+(?:\n\s+.+)*)", body, re.MULTILINE)
        if summary_match:
            entry["summary"] = " ".join(
                line.strip() for line in summary_match.group(1).splitlines() if line.strip()
            )
        elif sm := re.search(r"^\s*summary:\s*(.+)$", body, re.MULTILINE):
            entry["summary"] = sm.group(1).strip().strip("\"'")

        decoded_match = re.search(r"^\s*decoded_text:\s*\"(.+?)\"", body, re.MULTILINE)
        if decoded_match:
            entry["decoded_text"] = decoded_match.group(1)

        entries.append(entry)
    return entries


def _is_sensitivity_excluded(body: str) -> bool:
    for field in ("sensitivity_class", "portability_class"):
        m = re.search(rf"^\s*{field}:\s*(\S+)", body, re.MULTILINE)
        if m and m.group(1).strip() in EXCLUDED_SENSITIVITY:
            return True
    return False


def _extract_evidence(evidence_content: str) -> dict[str, list[dict]]:
    return {
        "write": _extract_entries_by_prefix(evidence_content, "WRITE-"),
        "create": _extract_entries_by_prefix(evidence_content, "CREATE-"),
        "act": _extract_entries_by_prefix(evidence_content, "ACT-"),
    }


# ── rationale loading ───────────────────────────────────────────────────

def _load_rationales(rationale_dir: Path | None = None) -> list[dict]:
    """Load artifact-rationale JSON files from artifacts/rationales/."""
    d = rationale_dir or RATIONALE_DIR
    if not d.is_dir():
        return []
    rationales: list[dict] = []
    for f in sorted(d.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        if RATIONALE_REQUIRED_FIELDS.issubset(data.keys()):
            rationales.append(data)
    return rationales


# ── main export ─────────────────────────────────────────────────────────

def export_capability(user_id: str = "grace-mar") -> dict:
    """Build the capability export structure.

    Returns a dict suitable for JSON serialization.
    """
    user_dir = profile_dir(user_id)
    self_path = user_dir / "self.md"
    skills_path = resolve_surface_markdown_path(user_dir, "self_skills")
    evidence_path = resolve_surface_markdown_path(user_dir, "self_evidence")

    self_content = read_path(self_path) or ""
    skills_content = read_path(skills_path) or ""
    evidence_content = read_path(evidence_path) or ""

    identity = _parse_identity_context(self_content)
    skills = _parse_skills(skills_content)
    evidence = _extract_evidence(evidence_content)
    rationales = _load_rationales()

    evidence_total = sum(len(v) for v in evidence.values())
    claims_count = len(skills["claims"])

    return {
        "version": "1.0",
        "format": "grace-mar-capability-export",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "identity_context": identity,
        "skills": skills,
        "evidence": evidence,
        "rationales": rationales,
        "counts": {
            "evidence_total": evidence_total,
            "rationale_total": len(rationales),
            "skills_claims": claims_count,
        },
    }


# ── CLI ─────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Export demonstrated-capability profile")
    parser.add_argument("-u", "--user", default="grace-mar", help="User id")
    parser.add_argument("-o", "--output", default=None, help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    result = export_capability(user_id=args.user)
    text = json.dumps(result, indent=2, default=str, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"Capability export written to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
