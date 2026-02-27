#!/usr/bin/env python3
"""
Export Record to curriculum-oriented JSON for adaptive curriculum engines.

Provides a snapshot for homeschool bots, Glide/Zapier stacks, Khan, IXL, etc.:
- Curiosity (IX-B), knowledge (IX-A), skills edge, Lexile
- Recent evidence anchors (IDs only)
- Does NOT expose full Record content

Usage:
    python scripts/export_curriculum.py -u grace-mar
    python scripts/export_curriculum.py -u grace-mar -o ../curriculum-stack/
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _extract_yaml_list(content: str, key: str) -> list:
    """Extract list from YAML: key: [a, b, c] or key: \\n  - item."""
    pattern = rf"{key}:\s*\[(.*?)\]"
    m = re.search(pattern, content, re.DOTALL)
    if m:
        raw = m.group(1)
        return [x.strip().strip('"\'') for x in re.split(r",|\n", raw) if x.strip()]
    pattern2 = rf"{key}:\s*\n((?:\s+-\s+[^\n]+\n?)+)"
    m2 = re.search(pattern2, content)
    if m2:
        lines = m2.group(1).strip().split("\n")
        return [re.sub(r"^\s*-\s+", "", ln).split("#")[0].strip().strip('"\'') for ln in lines if ln.strip()]
    return []


def _ix_summaries(content: str) -> dict:
    out = {"ix_a": [], "ix_b": [], "ix_c": []}
    for prefix, key in [("LEARN", "ix_a"), ("CUR", "ix_b"), ("PER", "ix_c")]:
        pattern = rf'id:\s+{prefix}-\d+.*?topic:\s*"([^"]+)"'
        topics = re.findall(pattern, content, re.DOTALL)
        if not topics:
            pattern = rf"id:\s+{prefix}-\d+.*?topic:\s*'([^']+)'"
            topics = re.findall(pattern, content, re.DOTALL)
        out[key] = [t[:80] for t in topics[:25]]
    return out


def _extract_lexile(self_content: str) -> str | None:
    m = re.search(r'lexile_output:\s*["\']?(\d+L)["\']?', self_content)
    return m.group(1) if m else None


def _extract_access_needs(self_content: str, lexile: str | None) -> dict:
    """Extract access needs for assistive tools (reading pens, etc.). Optional SELF section; falls back to Lexile-derived explanation level."""
    needs: dict = {}
    # Lexile → approximate grade for "explain at X level" (tools like World Pen Scan)
    if lexile:
        needs["explanation_level_lexile"] = lexile
        # Rough mapping: 400L≈1st, 500L≈2nd, 600L≈2nd-3rd, 700L≈3rd
        num = int(lexile.replace("L", "")) if lexile else 0
        if num <= 400:
            needs["explanation_grade"] = "1st"
        elif num <= 500:
            needs["explanation_grade"] = "2nd"
        elif num <= 600:
            needs["explanation_grade"] = "2nd"
        elif num <= 700:
            needs["explanation_grade"] = "3rd"
        else:
            needs["explanation_grade"] = "4th"
    # Optional: extract from SELF section "## ACCESS NEEDS" or "## LEARNING PREFERENCES" if present
    section = re.search(r"## (?:ACCESS NEEDS|LEARNING PREFERENCES)(.*?)(?=## |\Z)", self_content, re.DOTALL | re.IGNORECASE)
    if section:
        block = section.group(1)
        if re.search(r"dyslexia|dyslexic", block, re.IGNORECASE):
            needs["dyslexia_friendly_font"] = True
        m = re.search(r"read_aloud_speed|read_speed|speed:\s*(\w+)", block, re.IGNORECASE)
        if m:
            needs["preferred_read_speed"] = m.group(1).lower()
    return needs


def _extract_skills_edge(skills_content: str) -> dict:
    """Extract edge from each container: THINK, WRITE, WORK, MATH, CHINESE."""
    edges = {}
    blocks = re.split(r"\n#{2,3} ", skills_content)
    for block in blocks[1:]:  # skip header
        name_match = re.match(r"(\w+)", block)
        if not name_match:
            continue
        name = name_match.group(1).lower()
        m = re.search(r'edge:\s*["\']([^"\']+)["\']', block)
        if not m:
            m = re.search(r"edge:\s*(\S.+?)(?=\n\s+\w+:|\n\s*#|\n```|\Z)", block, re.DOTALL)
        if m:
            val = m.group(1).strip().strip('"\'')
            if val.lower() != "null" and not val.lower().startswith("null"):
                edges[name] = val
    return edges


def _evidence_anchors(content: str, limit: int = 30) -> list[str]:
    ids = list(set(re.findall(r"ACT-\d+", content)))
    ids.sort(key=lambda x: int(x.split("-")[1]), reverse=True)
    return ids[:limit]


def _library_titles(library_content: str, limit: int = 15) -> list[dict]:
    """Extract title + scope from LIBRARY for curriculum relevance."""
    entries = []
    for m in re.finditer(r'title:\s*["\']([^"\']+)["\'].*?scope:\s*\[(.*?)\]', library_content, re.DOTALL):
        title = m.group(1).strip()
        scope_raw = m.group(2)
        scope = [x.strip().strip('"\'') for x in re.split(r",", scope_raw) if x.strip()]
        entries.append({"title": title, "scope": scope[:5]})
        if len(entries) >= limit:
            break
    return entries


def export_curriculum(user_id: str = "grace-mar") -> dict:
    """Build curriculum-oriented export for adaptive curriculum engines."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_content = _read(profile_dir / "self.md")
    skills_content = "\n".join(
        _read(profile_dir / p)
        for p in ["skills.md", "skill-think.md", "skill-write.md", "skill-work.md"]
    )
    evidence_content = _read(profile_dir / "self-evidence.md")
    library_content = _read(profile_dir / "self-library.md")

    identity_block = re.search(r"## I\. IDENTITY(.*?)(?=## |\Z)", self_content, re.DOTALL)
    identity_block = identity_block.group(1) if identity_block else ""
    pref_block = re.search(r"## II\. PREFERENCES(.*?)(?=## |\Z)", self_content, re.DOTALL)
    pref_block = pref_block.group(1) if pref_block else ""

    name = None
    m = re.search(r"name:\s*(.+)", identity_block)
    if m:
        name = m.group(1).split("#")[0].strip().strip('"\'')
    age = None
    m = re.search(r"age:\s*(\d+)", identity_block)
    if m:
        age = int(m.group(1))

    interests = []
    for key in ["movies", "books", "food", "places", "activities", "music"]:
        interests.extend(_extract_yaml_list(pref_block, key))
    interests = list(dict.fromkeys(interests))[:25]

    ix = _ix_summaries(self_content)
    lexile = _extract_lexile(self_content)
    access_needs = _extract_access_needs(self_content, lexile)
    skills_edge = _extract_skills_edge(skills_content)
    evidence_anchors = _evidence_anchors(evidence_content)
    library = _library_titles(library_content)

    return {
        "version": "1.0",
        "grace_mar": True,
        "curriculum_ready": True,
        "user_id": user_id,
        "generated_at": datetime.now().isoformat(),
        "provenance": "human_approved",
        "lexile_output": lexile,
        "access_needs": access_needs,
        "identity": {"name": name, "age": age} if name or age else {},
        "knowledge": ix["ix_a"],
        "curiosity": ix["ix_b"],
        "personality": ix["ix_c"][:10],
        "skills_edge": skills_edge,
        "interests": interests,
        "evidence_anchors": evidence_anchors,
        "library": library,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Record to curriculum-oriented JSON for adaptive curriculum engines"
    )
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    args = parser.parse_args()

    data = export_curriculum(user_id=args.user)
    profile_dir = REPO_ROOT / "users" / args.user
    out_dir = Path(args.output) if args.output else profile_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "curriculum_profile.json"
    out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
