#!/usr/bin/env python3
"""
Compute a checksum of the fork state (SELF + EVIDENCE + prompt sections).

Provides a verifiable "proof of development" — a hash that uniquely identifies
the fork's documented state at a given moment.

Usage:
    python scripts/fork_checksum.py
    python scripts/fork_checksum.py --append   # Append (ts, checksum) to FORK-CHECKSUM-LOG.txt
    python scripts/fork_checksum.py --manifest  # Write FORK-MANIFEST.json (checksum, IX counts, pipeline stats)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "users" / "grace-mar"
BOT_DIR = REPO_ROOT / "bot"
LOG_PATH = PROFILE_DIR / "FORK-CHECKSUM-LOG.txt"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text().strip()


def _canonicalize(text: str) -> bytes:
    """Normalize for hashing: strip, Unix line endings."""
    normalized = text.strip().replace("\r\n", "\n").replace("\r", "\n")
    return normalized.encode("utf-8")


def compute_checksum() -> str:
    """Compute SHA-256 of fork state."""
    parts = []
    parts.append(_read(PROFILE_DIR / "SELF.md"))
    parts.append(_read(PROFILE_DIR / "EVIDENCE.md"))
    # Key prompt sections that embed fork state
    prompt_path = BOT_DIR / "prompt.py"
    if prompt_path.exists():
        content = prompt_path.read_text()
        # Extract SYSTEM_PROMPT content (between triple quotes)
        m = re.search(r'SYSTEM_PROMPT\s*=\s*"""(.*?)"""', content, re.DOTALL)
        if m:
            parts.append(m.group(1).strip())
    h = hashlib.sha256()
    for p in parts:
        h.update(_canonicalize(p))
        h.update(b"\n---\n")
    return h.hexdigest()


def _ix_counts(content: str) -> tuple[int, int, int]:
    """Return (ix_a, ix_b, ix_c) from SELF.md content."""
    a = len(re.findall(r"id:\s+LEARN-\d+", content))
    b = len(re.findall(r"id:\s+CUR-\d+", content))
    c = len(re.findall(r"id:\s+PER-\d+", content))
    return a, b, c


def _pipeline_stats() -> tuple[int, int, str]:
    """Return (applied, rejected, last_applied_ts) from PIPELINE-EVENTS.jsonl."""
    events_path = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"
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


def write_manifest(checksum: str) -> None:
    """Write FORK-MANIFEST.json with checksum, IX counts, pipeline stats."""
    self_content = _read(PROFILE_DIR / "SELF.md")
    ix_a, ix_b, ix_c = _ix_counts(self_content)
    pipeline_applied, pipeline_rejected, last_applied_ts = _pipeline_stats()
    manifest = {
        "checksum": checksum,
        "ix_a_count": ix_a,
        "ix_b_count": ix_b,
        "ix_c_count": ix_c,
        "pipeline_applied": pipeline_applied,
        "pipeline_rejected": pipeline_rejected,
        "last_applied_ts": last_applied_ts or None,
        "generated_at": datetime.now().isoformat(),
    }
    manifest_path = PROFILE_DIR / "FORK-MANIFEST.json"
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute fork state checksum")
    parser.add_argument("--append", "-a", action="store_true", help="Append to FORK-CHECKSUM-LOG.txt")
    parser.add_argument("--manifest", "-m", action="store_true", help="Write FORK-MANIFEST.json")
    args = parser.parse_args()
    checksum = compute_checksum()
    print(checksum)
    if args.append:
        ts = datetime.now().isoformat()
        PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(f"{ts} {checksum}\n")
        print(f"Appended to {LOG_PATH}", file=sys.stderr)
    if args.manifest:
        write_manifest(checksum)


if __name__ == "__main__":
    main()
