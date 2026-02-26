#!/usr/bin/env python3
"""
Export Record to symbolic, cache-oriented JSON for Intersignal Familiar nodes.

Designed for "cache-level symbolic sharing" and Mesh Cache alignment:
- Identity primitives (interests, values, IX-A/B/C summaries)
- Evidence anchors (ACT-XXXX IDs), not full content
- Checksum for tamper-evidence
- Consent-bound, human_approved provenance

Usage:
    python scripts/export_symbolic.py -u grace-mar
    python scripts/export_symbolic.py -u grace-mar -o ../intersignal-mesh/
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BOT_DIR = REPO_ROOT / "bot"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _compute_checksum(profile_dir: Path) -> str:
    parts = []
    parts.append(_read(profile_dir / "self.md"))
    parts.append(_read(profile_dir / "self-evidence.md"))
    prompt_path = BOT_DIR / "prompt.py"
    if prompt_path.exists():
        content = prompt_path.read_text()
        m = re.search(r'SYSTEM_PROMPT\s*=\s*"""(.*?)"""', content, re.DOTALL)
        if m:
            parts.append(m.group(1).strip())
    h = hashlib.sha256()
    for p in parts:
        normalized = p.strip().replace("\r\n", "\n").replace("\r", "\n")
        h.update(normalized.encode("utf-8"))
        h.update(b"\n---\n")
    return h.hexdigest()


def _extract_yaml_list(content: str, key: str) -> list:
    """Extract list from YAML: movies: [a, b, c] or movies: \\n  - item."""
    pattern = rf"{key}:\s*\[(.*?)\]"
    m = re.search(pattern, content, re.DOTALL)
    if m:
        raw = m.group(1)
        return [x.strip().strip('"\'') for x in re.split(r",|\n", raw) if x.strip()]
    # Bullet format: key:\n  - item
    pattern2 = rf"{key}:\s*\n((?:\s+-\s+[^\n]+\n?)+)"
    m2 = re.search(pattern2, content)
    if m2:
        lines = m2.group(1).strip().split("\n")
        return [re.sub(r"^\s*-\s+", "", ln).split("#")[0].strip().strip('"\'') for ln in lines if ln.strip()]
    return []


def _extract_section(content: str, title: str) -> str | None:
    pattern = rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _ix_summaries(content: str) -> dict:
    """Extract IX-A/B/C entry topic summaries (first 80 chars)."""
    out = {"ix_a": [], "ix_b": [], "ix_c": []}
    for prefix, key in [("LEARN", "ix_a"), ("CUR", "ix_b"), ("PER", "ix_c")]:
        # Match double-quoted or single-quoted topic; content may contain apostrophe
        pattern = rf'id:\s+{prefix}-\d+.*?topic:\s*"([^"]+)"'
        topics = re.findall(pattern, content, re.DOTALL)
        if not topics:
            pattern = rf"id:\s+{prefix}-\d+.*?topic:\s*'([^']+)'"
            topics = re.findall(pattern, content, re.DOTALL)
        out[key] = [t[:80] for t in topics[:20]]
    return out


def _evidence_anchors(content: str) -> list[str]:
    """Extract ACT-XXXX IDs from EVIDENCE."""
    return list(set(re.findall(r"ACT-\d+", content)))[:50]


def export_symbolic(user_id: str = "grace-mar") -> dict:
    """Build cache-oriented symbolic identity for Familiar nodes."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_content = _read(profile_dir / "self.md")
    evidence_content = _read(profile_dir / "self-evidence.md")

    identity_block = _extract_section(self_content, "I. IDENTITY") or ""
    pref_block = _extract_section(self_content, "II. PREFERENCES (Survey Seeded)") or ""

    identity = {}
    m = re.search(r"name:\s*(.+)", identity_block)
    if m:
        identity["name"] = m.group(1).split("#")[0].strip().strip('"\'')
    m = re.search(r"age:\s*(\d+)", identity_block)
    if m:
        identity["age"] = int(m.group(1))
    langs = _extract_yaml_list(identity_block, "languages")
    if langs:
        identity["languages"] = langs
    m = re.search(r"location:\s*(.+)", identity_block)
    if m:
        identity["location"] = m.group(1).split("#")[0].strip().strip('"\'')

    interests = []
    for key in ["movies", "books", "food", "places", "activities", "music"]:
        interests.extend(_extract_yaml_list(pref_block, key))

    values = re.findall(r"values?:\s*\[(.*?)\]", self_content, re.DOTALL)
    values_parsed = []
    if values:
        values_parsed = [x.strip().strip('"\'') for x in re.split(r",|\n", values[0]) if x.strip()]

    ix = _ix_summaries(self_content)
    evidence_anchors = _evidence_anchors(evidence_content)
    checksum = _compute_checksum(profile_dir)

    return {
        "version": "1.0",
        "grace_mar": True,
        "intersignal_familiar_ready": True,
        "user_id": user_id,
        "generated_at": datetime.now().isoformat(),
        "checksum": checksum,
        "provenance": "human_approved",
        "identity": {k: v for k, v in identity.items() if v is not None},
        "interests": list(dict.fromkeys(interests))[:30],
        "values": values_parsed[:15],
        "ix_a": ix["ix_a"],
        "ix_b": ix["ix_b"],
        "ix_c": ix["ix_c"],
        "evidence_anchors": evidence_anchors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Record to symbolic JSON for Intersignal Familiar nodes"
    )
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    args = parser.parse_args()

    data = export_symbolic(user_id=args.user)
    profile_dir = REPO_ROOT / "users" / args.user
    out_dir = Path(args.output) if args.output else profile_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "symbolic_identity.json"
    out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
