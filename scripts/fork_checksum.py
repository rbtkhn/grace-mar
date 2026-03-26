#!/usr/bin/env python3
"""
Compute a checksum of the fork state (SELF + EVIDENCE + prompt sections).

Provides a verifiable "proof of development" — a hash that uniquely identifies
the fork's documented state at a given moment.

Usage:
    python scripts/fork_checksum.py
    python scripts/fork_checksum.py -u xavier
    python scripts/fork_checksum.py --append   # Append to users/<id>/fork-checksum-log.txt
    python scripts/fork_checksum.py --manifest  # Write users/<id>/fork-manifest.json
    python scripts/fork_checksum.py -u grace-mar --manifest

Default user: GRACE_MAR_USER_ID or grace-mar.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BOT_DIR = REPO_ROOT / "bot"

# Imported after REPO_ROOT so repo_io can load
from repo_io import profile_dir as _profile_dir


def _default_user_id() -> str:
    return (os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text().strip()


def _canonicalize(text: str) -> bytes:
    """Normalize for hashing: strip, Unix line endings."""
    normalized = text.strip().replace("\r\n", "\n").replace("\r", "\n")
    return normalized.encode("utf-8")


def compute_checksum(pd: Path) -> str:
    """Compute SHA-256 of fork state for users/<id>/."""
    parts = []
    parts.append(_read(pd / "self.md"))
    parts.append(_read(pd / "self-archive.md") or _read(pd / "self-evidence.md"))
    # Key prompt sections that embed fork state (shared bot — same extract for all forks)
    prompt_path = BOT_DIR / "prompt.py"
    if prompt_path.exists():
        content = prompt_path.read_text()
        m = re.search(r'SYSTEM_PROMPT\s*=\s*"""(.*?)"""', content, re.DOTALL)
        if m:
            parts.append(m.group(1).strip())
    h = hashlib.sha256()
    for p in parts:
        h.update(_canonicalize(p))
        h.update(b"\n---\n")
    return h.hexdigest()


def _ix_counts(content: str) -> tuple[int, int, int]:
    """Return (ix_a, ix_b, ix_c) from self.md content."""
    a = len(re.findall(r"id:\s+LEARN-\d+", content))
    b = len(re.findall(r"id:\s+CUR-\d+", content))
    c = len(re.findall(r"id:\s+PER-\d+", content))
    return a, b, c


def _pipeline_stats(pd: Path) -> tuple[int, int, str]:
    """Return (applied, rejected, last_applied_ts) from pipeline-events.jsonl."""
    events_path = pd / "pipeline-events.jsonl"
    applied = rejected = 0
    last_ts = ""
    if events_path.exists():
        for line in events_path.read_text().strip().splitlines():
            if not line:
                continue
            try:
                row = json.loads(line)
                e = row.get("event", "")
                ts = row.get("ts", "")
                if e in ("applied", "approved"):
                    applied += 1
                    if ts:
                        last_ts = ts
                elif e == "rejected":
                    rejected += 1
            except json.JSONDecodeError:
                pass
    return applied, rejected, last_ts


def write_manifest(pd: Path, checksum: str) -> None:
    """Write fork-manifest.json with checksum, IX counts, pipeline stats."""
    self_content = _read(pd / "self.md")
    ix_a, ix_b, ix_c = _ix_counts(self_content)
    pipeline_applied, pipeline_rejected, last_applied_ts = _pipeline_stats(pd)
    manifest = {
        "user_id": pd.name,
        "checksum": checksum,
        "ix_a_count": ix_a,
        "ix_b_count": ix_b,
        "ix_c_count": ix_c,
        "pipeline_applied": pipeline_applied,
        "pipeline_rejected": pipeline_rejected,
        "last_applied_ts": last_applied_ts or None,
        "generated_at": datetime.now().isoformat(),
    }
    manifest_path = pd / "fork-manifest.json"
    pd.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute fork state checksum")
    parser.add_argument(
        "-u",
        "--user",
        default=_default_user_id(),
        help="Fork id under users/<id>/ (default: GRACE_MAR_USER_ID or grace-mar)",
    )
    parser.add_argument("--append", "-a", action="store_true", help="Append to fork-checksum-log.txt")
    parser.add_argument("--manifest", "-m", action="store_true", help="Write fork-manifest.json")
    args = parser.parse_args()
    uid = (args.user or "").strip() or "grace-mar"
    pd = _profile_dir(uid)
    checksum = compute_checksum(pd)
    print(checksum)
    log_path = pd / "fork-checksum-log.txt"
    if args.append:
        ts = datetime.now().isoformat()
        pd.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{ts} {checksum}\n")
        print(f"Appended to {log_path}", file=sys.stderr)
    if args.manifest:
        write_manifest(pd, checksum)


if __name__ == "__main__":
    main()
