#!/usr/bin/env python3
"""
Prune users/<id>/self-memory.md when it exceeds a character budget (larger than
strategy / Xavier inbox buffers). Removed text is written to
users/<id>/artifacts/memory-prune/ and optionally appended to self-archive.md
§ IX (continuity housekeeping), not merged via the gate.

Operator-run; does not replace process_approved_candidates for Record merges.
See docs/memory-template.md § Lifespan & decay.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from repo_io import resolve_self_memory_path  # noqa: E402

HORIZON_HEADER = re.compile(r"^##\s*(Short|Medium|Long)-term\s*$", re.IGNORECASE)
DEFAULT_MAX_CHARS = 16000
DEFAULT_TARGET_CHARS = 12000
ARCHIVE_MARKER = "END OF FILE — EVIDENCE"
ARCHIVE_SECTION_TITLE = "## IX. MEMORY PRUNE ARCHIVE (continuity housekeeping)"
MAX_APPEND_CHARS = 50000


def _user_dir(args: argparse.Namespace) -> Path:
    uid = args.user.strip()
    return REPO_ROOT / "users" / uid


def _split_horizons(text: str) -> tuple[str, list[tuple[str, str]]] | None:
    """
    Returns (preamble, [(name, body), ...]) for Short/Medium/Long-term, or None if no horizons.
    Bodies include trailing newline semantics preserved via join.
    """
    lines = text.splitlines(keepends=True)
    idxs: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = HORIZON_HEADER.match(line.rstrip("\n"))
        if m:
            idxs.append((i, m.group(1).lower()))
    if not idxs:
        return None

    preamble = "".join(lines[: idxs[0][0]])
    sections: list[tuple[str, str]] = []
    for j, (start, name) in enumerate(idxs):
        end = idxs[j + 1][0] if j + 1 < len(idxs) else len(lines)
        body = "".join(lines[start + 1 : end])
        sections.append((name, body))
    return preamble, sections


def _total_len(preamble: str, sections: list[tuple[str, str]]) -> int:
    n = len(preamble)
    for name, body in sections:
        n += len(f"## {name.title()}-term\n") + len(body)
    return n


def _rebuild(preamble: str, sections: list[tuple[str, str]]) -> str:
    """Rebuild file preserving the order of horizons as in `sections`."""
    title_for = {"short": "Short", "medium": "Medium", "long": "Long"}
    parts: list[str] = [preamble]
    for key, body in sections:
        parts.append(f"## {title_for[key]}-term\n")
        parts.append(body)
    return "".join(parts)


def _prune_sections_free_budget(
    sections: list[tuple[str, str]],
    budget: int,
) -> tuple[list[tuple[str, str]], str]:
    """
    Remove line-paragraphs from the start of short, then medium, until `budget` chars collected.
    Returns (new_sections, pruned_text).
    """
    collected: list[str] = []
    remaining_budget = budget
    new_sections: list[tuple[str, str]] = []

    def strip_from_body(body: str) -> tuple[str, str]:
        nonlocal remaining_budget
        if remaining_budget <= 0:
            return body, ""
        lines = body.splitlines(keepends=True)
        taken: list[str] = []
        i = 0
        while i < len(lines) and remaining_budget > 0:
            line = lines[i]
            # drop leading empties only after we've started taking
            if not taken and line.strip() == "":
                i += 1
                continue
            if len(line) <= remaining_budget or not taken:
                taken.append(line)
                remaining_budget -= len(line)
                i += 1
            else:
                break
        pruned_part = "".join(taken)
        rest = "".join(lines[i:])
        return rest, pruned_part

    order_keys = [s[0] for s in sections]
    bodies = {k: v for k, v in sections}

    for key in ("short", "medium", "long"):
        if key not in bodies or remaining_budget <= 0:
            continue
        body = bodies[key]
        new_body, chunk = strip_from_body(body)
        if chunk:
            collected.append(f"## {key.upper()} (excerpt pruned)\n" + chunk)
        bodies[key] = new_body

    new_sections = [(k, bodies[k]) for k in order_keys if k in bodies]
    return new_sections, "\n\n".join(collected)


def _prune_legacy(text: str, budget: int) -> tuple[str, str]:
    """No horizon headers: remove from start of file until budget chars freed."""
    if budget <= 0:
        return text, ""
    lines = text.splitlines(keepends=True)
    taken: list[str] = []
    remaining = budget
    i = 0
    while i < len(lines) and remaining > 0:
        line = lines[i]
        taken.append(line)
        remaining -= len(line)
        i += 1
    pruned = "".join(taken)
    rest = "".join(lines[i:])
    return rest, pruned


def run_prune(
    user_dir: Path,
    max_chars: int,
    target_chars: int,
) -> tuple[str, str, str, bool]:
    """
    Returns (new_full_text, pruned_blob, message, used_horizons).
    """
    mem = resolve_self_memory_path(user_dir)
    if not mem.is_file():
        raise FileNotFoundError(f"Missing self-memory: {mem}")
    original = mem.read_text(encoding="utf-8")
    n = len(original)
    if n <= max_chars:
        return original, "", f"OK: {n} chars <= max {max_chars} (no prune)", False

    need = n - target_chars
    split = _split_horizons(original)
    if split is None:
        new_text, pruned = _prune_legacy(original, need)
        return new_text, pruned, "legacy (no horizon headers)", False

    preamble, sections = split
    new_sections, pruned = _prune_sections_free_budget(sections, need)
    # Ensure we actually shrink; if still over (edge), strip more from short body aggressively
    rebuilt = _rebuild(preamble, new_sections)
    guard = 0
    while len(rebuilt) > target_chars and guard < 5000:
        guard += 1
        new_sections, extra = _prune_sections_free_budget(new_sections, len(rebuilt) - target_chars)
        pruned = pruned + ("\n\n" if pruned and extra else "") + extra
        rebuilt = _rebuild(preamble, new_sections)

    stub = (
        f"\n- _(Buffer pruned {datetime.now(timezone.utc).date().isoformat()} — "
        f"excerpt in `artifacts/memory-prune/`; if you used `--archive`, also `self-archive.md` § IX.)_\n"
    )
    short_body = dict(new_sections).get("short", "")
    if "short" in dict(new_sections) and len(short_body.strip()) < 20:
        for i, (k, b) in enumerate(new_sections):
            if k == "short":
                new_sections[i] = (k, stub + b)
                break
    rebuilt = _rebuild(preamble, new_sections)
    return rebuilt, pruned, "horizons", True


def _write_artifact(user_dir: Path, pruned: str, stamp: str) -> Path:
    out_dir = user_dir / "artifacts" / "memory-prune"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{stamp}-prune.md"
    header = (
        f"# MEMORY prune excerpt\n\n"
        f"**Generated:** {stamp} (UTC)\n\n"
        f"---\n\n"
    )
    path.write_text(header + pruned, encoding="utf-8")
    return path


def _append_archive(user_dir: Path, pruned: str, stamp: str, chars_removed: int) -> None:
    arch = user_dir / "self-archive.md"
    if not arch.is_file():
        raise FileNotFoundError(f"Missing self-archive: {arch}")
    text = arch.read_text(encoding="utf-8")
    if ARCHIVE_MARKER not in text:
        raise ValueError(f"Expected footer marker {ARCHIVE_MARKER!r} in self-archive.md")
    blob = pruned
    if len(blob) > MAX_APPEND_CHARS:
        blob = blob[:MAX_APPEND_CHARS] + f"\n\n... [truncated at {MAX_APPEND_CHARS} chars for archive safety]\n"

    block = (
        f"\n#### {stamp} — bytes removed (approx): {chars_removed}\n\n"
        f"~~~\n{blob.rstrip()}\n~~~\n"
    )

    if ARCHIVE_SECTION_TITLE not in text:
        insert = (
            f"\n{ARCHIVE_SECTION_TITLE}\n\n"
            f"> Pruned excerpts from `self-memory.md` (continuity buffer). "
            f"Housekeeping / operator; not a gated identity merge.\n"
            f"{block}"
        )
    else:
        insert = block

    new_text = text.replace(
        ARCHIVE_MARKER,
        insert + "\n" + ARCHIVE_MARKER,
        1,
    )
    arch.write_text(new_text, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-u", "--user", required=True, help="Instance id (e.g. grace-mar)")
    p.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help=f"Prune if file larger than this (default {DEFAULT_MAX_CHARS})",
    )
    p.add_argument(
        "--target-chars",
        type=int,
        default=DEFAULT_TARGET_CHARS,
        help=f"Target size after prune (default {DEFAULT_TARGET_CHARS})",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print sizes and would-remove estimate; do not write",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite self-memory.md and write artifact under artifacts/memory-prune/",
    )
    p.add_argument(
        "--archive",
        action="store_true",
        help=f"Append excerpt to self-archive.md before {ARCHIVE_MARKER!r} (requires --apply)",
    )
    args = p.parse_args()
    user_dir = _user_dir(args)

    if args.target_chars >= args.max_chars:
        print("error: --target-chars must be < --max-chars", file=sys.stderr)
        return 2
    if args.archive and not args.apply:
        print("error: --archive requires --apply", file=sys.stderr)
        return 2

    mem = resolve_self_memory_path(user_dir)
    if not mem.is_file():
        print(f"error: {mem} not found", file=sys.stderr)
        return 1

    orig = mem.read_text(encoding="utf-8")
    new_text, pruned, note, _hz = run_prune(user_dir, args.max_chars, args.target_chars)
    removed = len(orig) - len(new_text) if pruned else 0

    print(f"self-memory: {len(orig)} chars -> would be {len(new_text)} chars ({note})")
    if pruned:
        print(f"pruned blob: {len(pruned)} chars (excerpt stored on --apply)")

    if args.dry_run:
        if pruned:
            print("--- pruned excerpt preview (800 chars) ---")
            print(pruned[:800] + ("..." if len(pruned) > 800 else ""))
        return 0

    if not args.apply:
        print("No --apply: no files written. Use --dry-run or --apply.")
        return 0

    if not pruned:
        print("Nothing to prune.")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    art = _write_artifact(user_dir, pruned, stamp)
    mem.write_text(new_text, encoding="utf-8")
    print(f"Wrote {mem} ({len(new_text)} chars)")
    print(f"Artifact: {art}")

    if args.archive:
        _append_archive(user_dir, pruned, stamp, removed)
        print(f"Appended prune block to {user_dir / 'self-archive.md'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
