#!/usr/bin/env python3
"""
Generate agent-consumable manifest (llms.txt-style) for Grace-Mar Record.

Enables discoverability: agents can query what's readable/writable without full access.
Aligns with white paper: "Future: Agent manifest — llms.txt-style discoverability."

Outputs:
  - users/[id]/manifest.json — Machine-readable (readable/writable surfaces, checksum, schema hints)
  - users/[id]/llms.txt — Human- and agent-readable discoverability file

Usage:
    python scripts/export_manifest.py --user pilot-001
    python scripts/export_manifest.py -u pilot-001 -o ../openclaw/
"""

import argparse
import hashlib
import json
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
    """Reuse fork_checksum logic."""
    import re

    parts = []
    parts.append(_read(profile_dir / "SELF.md"))
    parts.append(_read(profile_dir / "EVIDENCE.md"))
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


def generate_manifest(user_id: str = "pilot-001") -> dict:
    """
    Build agent manifest: readable/writable surfaces, schema hints, checksum.

    Aligns with white paper staging contract: agents may stage, never merge.
    """
    profile_dir = REPO_ROOT / "users" / user_id
    checksum = _compute_checksum(profile_dir)

    manifest = {
        "version": "1.0",
        "grace_mar": True,
        "user_id": user_id,
        "generated_at": datetime.now().isoformat(),
        "checksum": checksum,
        "readable": [
            "SELF/identity",
            "SELF/preferences",
            "SELF/linguistic_style",
            "SELF/personality",
            "SELF/interests",
            "SELF/values",
            "SELF/reasoning",
            "SELF/narrative",
            "SELF/IX-A",
            "SELF/IX-B",
            "SELF/IX-C",
            "SKILLS/READ",
            "SKILLS/WRITE",
            "SKILLS/BUILD",
            "EVIDENCE/activity_log",
            "EVIDENCE/writing_log",
            "EVIDENCE/creation_log",
            "LIBRARY/entries",
        ],
        "writable": [
            "PENDING-REVIEW/candidates",
        ],
        "writable_note": "Agents may stage candidates only. Merge requires user approval.",
        "schema_hints": {
            "SELF": {"type": "object", "description": "Identity, personality, post-seed growth (IX-A, IX-B, IX-C)"},
            "SKILLS": {"type": "object", "description": "Capability containers (READ, WRITE, BUILD)"},
            "EVIDENCE": {"type": "object", "description": "Activity log, writing, creation; immutable once captured"},
            "PENDING-REVIEW": {"type": "object", "description": "Staging area; format documented in AGENTS.md"},
        },
        "exports": {
            "USER.md": "python scripts/export_user_identity.py -u " + user_id,
            "manifest": "python scripts/export_manifest.py -u " + user_id,
            "fork_json": "python scripts/export_fork.py -o fork-export.json",
        },
    }

    return manifest


def generate_llms_txt(manifest: dict, user_id: str) -> str:
    """Human- and agent-readable llms.txt-style discoverability."""
    lines = [
        "# Grace-Mar Record — Agent Manifest",
        "",
        f"User: {user_id}",
        f"Checksum: {manifest['checksum']}",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Readable",
        "Agents may read (for personalization, session continuity):",
        "",
    ]
    for r in manifest["readable"]:
        lines.append(f"  - {r}")
    lines.extend([
        "",
        "## Writable",
        manifest["writable_note"],
        "",
    ])
    for w in manifest["writable"]:
        lines.append(f"  - {w}")
    lines.extend([
        "",
        "## Exports",
        "",
    ])
    for name, cmd in manifest["exports"].items():
        lines.append(f"  {name}: {cmd}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate agent-consumable manifest for Grace-Mar Record"
    )
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument(
        "--output", "-o", default=None, help="Output directory (default: users/[id]/)"
    )
    parser.add_argument(
        "--llms-txt", action="store_true", default=True, help="Write llms.txt (default: true)"
    )
    parser.add_argument("--no-llms-txt", action="store_true", help="Skip llms.txt")
    args = parser.parse_args()

    manifest = generate_manifest(user_id=args.user)
    profile_dir = REPO_ROOT / "users" / args.user
    out_dir = Path(args.output) if args.output else profile_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path}", file=sys.stderr)

    if args.llms_txt and not args.no_llms_txt:
        llms_path = out_dir / "llms.txt"
        llms_path.write_text(
            generate_llms_txt(manifest, args.user), encoding="utf-8"
        )
        print(f"Wrote {llms_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
