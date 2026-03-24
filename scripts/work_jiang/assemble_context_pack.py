#!/usr/bin/env python3
"""
Assemble a minimal context pack for a work-jiang task.

Copies the files an agent needs into an output directory, writes a
CONTEXT-MANIFEST.md summarizing what's included.

Usage:
    python3 scripts/work_jiang/assemble_context_pack.py --task draft-ch07 -o /tmp/ch07-ctx/
    python3 scripts/work_jiang/assemble_context_pack.py --chapter ch07 -o /tmp/ch07-ctx/
    python3 scripts/work_jiang/assemble_context_pack.py --lecture "secret-history-08-*" -o /tmp/sh08-ctx/
"""

from __future__ import annotations

import argparse
import glob as globmod
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORK_JIANG = REPO_ROOT / "research" / "external" / "work-jiang"
TASKS_PATH = WORK_JIANG / "tasks.jsonl"
ARCH_PATH = WORK_JIANG / "metadata" / "book-architecture.yaml"

ALWAYS_INCLUDE = [
    "MULTI-AGENT.md",
]


def read_task_states() -> dict[str, dict]:
    states: dict[str, dict] = {}
    if not TASKS_PATH.exists():
        return states
    for line in TASKS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        tid = rec["task_id"]
        if tid not in states:
            states[tid] = {}
        states[tid].update(rec)
    return states


def resolve_globs(patterns: list[str], base: Path) -> list[Path]:
    """Resolve glob patterns relative to base directory."""
    resolved: list[Path] = []
    for pat in patterns:
        full = base / pat
        matches = sorted(globmod.glob(str(full)))
        if matches:
            resolved.extend(Path(m) for m in matches)
        else:
            candidate = base / pat
            if candidate.exists():
                resolved.append(candidate)
    return resolved


def get_chapter_context(ch_id: str) -> tuple[list[str], str | None]:
    """Derive context_files and previous chapter draft from architecture."""
    if not ARCH_PATH.exists():
        return [], None

    with open(ARCH_PATH, encoding="utf-8") as f:
        arch = yaml.safe_load(f)

    chapters = arch.get("book", {}).get("chapters", [])
    prev_draft = None

    for i, ch in enumerate(chapters):
        if ch["id"] == ch_id:
            source_ids = ch.get("source_ids", [])
            outline = ch.get("outline_path", f"chapters/{ch_id}/outline.md")
            draft = ch.get("draft_path", f"chapters/{ch_id}/draft.md")

            prefix_map = {
                "geo": "geo-strategy", "civ": "civilization",
                "sh": "secret-history", "gt": "game-theory", "gb": "great-books",
            }
            lecture_globs = []
            for sid in source_ids:
                parts = sid.split("-")
                if len(parts) == 2:
                    series = prefix_map.get(parts[0], parts[0])
                    lecture_globs.append(f"lectures/{series}-{parts[1]}-*.md")

            context = lecture_globs + [
                outline, draft,
                "prediction-tracking/registry/predictions.jsonl",
                "divergence-tracking/registry/divergences.jsonl",
            ]

            if i > 0:
                prev = chapters[i - 1]
                prev_draft = prev.get("draft_path", f"chapters/{prev['id']}/draft.md")

            return context, prev_draft

    return [], None


def copy_to_output(files: list[Path], out_dir: Path, base: Path) -> list[str]:
    """Copy files preserving relative paths. Returns list of relative paths."""
    copied = []
    for f in files:
        if not f.exists():
            continue
        try:
            rel = f.relative_to(base)
        except ValueError:
            rel = Path(f.name)
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        copied.append(str(rel))
    return copied


def write_manifest(out_dir: Path, copied: list[str], source: str) -> None:
    lines = [
        "# Context Pack Manifest",
        "",
        f"**Assembled:** {datetime.now(timezone.utc).isoformat()}",
        f"**Source:** {source}",
        "",
        "## Included files",
        "",
    ]
    for p in sorted(copied):
        lines.append(f"- `{p}`")
    lines.append("")
    (out_dir / "CONTEXT-MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble context pack for a work-jiang task.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", help="Task ID from tasks.jsonl")
    group.add_argument("--chapter", help="Chapter ID (e.g. ch07)")
    group.add_argument("--lecture", help="Lecture file glob (e.g. 'secret-history-08-*')")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    context_patterns: list[str] = []
    prev_draft: str | None = None
    source_label = ""

    if args.task:
        states = read_task_states()
        task = states.get(args.task)
        if not task:
            print(f"Task '{args.task}' not found in tasks.jsonl", file=sys.stderr)
            sys.exit(1)
        context_patterns = task.get("context_files", [])
        scope = task.get("scope", "")
        if scope.startswith("ch"):
            _, prev_draft = get_chapter_context(scope)
        source_label = f"task={args.task}"

    elif args.chapter:
        context_patterns, prev_draft = get_chapter_context(args.chapter)
        if not context_patterns:
            print(f"Chapter '{args.chapter}' not found in architecture", file=sys.stderr)
            sys.exit(1)
        source_label = f"chapter={args.chapter}"

    elif args.lecture:
        context_patterns = [f"lectures/{args.lecture}"]
        source_label = f"lecture={args.lecture}"

    files = resolve_globs(context_patterns, WORK_JIANG)

    for inc in ALWAYS_INCLUDE:
        p = WORK_JIANG / inc
        if p.exists() and p not in files:
            files.append(p)

    if prev_draft:
        prev_path = WORK_JIANG / prev_draft
        if prev_path.exists() and prev_path not in files:
            files.append(prev_path)

    if not files:
        print("No files resolved. Check patterns.", file=sys.stderr)
        sys.exit(1)

    copied = copy_to_output(files, out_dir, WORK_JIANG)
    write_manifest(out_dir, copied, source_label)

    print(f"Context pack assembled: {len(copied)} file(s) → {out_dir}")
    for p in sorted(copied):
        print(f"  {p}")


if __name__ == "__main__":
    main()
