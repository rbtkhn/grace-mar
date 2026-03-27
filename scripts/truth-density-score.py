#!/usr/bin/env python3
"""
Heuristic: among users/**/*.md, fraction containing 'must-persist' (case-insensitive).
Document the convention in docs/system-tensions-and-mysteries.md or skill-work docs.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
users = ROOT / "users"
must_persist = 0
total = 0
if users.is_dir():
    for f in users.rglob("*.md"):
        total += 1
        if "must-persist" in f.read_text(encoding="utf-8").lower():
            must_persist += 1
pct = (must_persist / total * 100) if total else 0.0
print(f"Truth density: {pct:.1f}% files with must-persist token ({must_persist}/{total})")
if pct > 30:
    print("Warning: high density — consider pruning transient items (heuristic only).")
