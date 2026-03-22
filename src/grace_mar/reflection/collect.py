"""Read-only aggregation of operator/Record files for reflection cycles."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class TextSlice:
    """A file excerpt with 1-based line numbers for citations."""

    path: str  # repo-relative, posix
    start_line: int
    end_line: int
    text: str
    note: str = ""


@dataclass
class ReflectionBundle:
    """Inputs passed to the reflection engine."""

    user_id: str
    lookback_days: int
    repo_root: Path
    slices: list[TextSlice] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

    def as_prompt_context(self, max_chars: int = 120_000) -> str:
        """Concatenate slices with headers; trim if needed."""
        parts: list[str] = []
        for sl in self.slices:
            header = f"### {sl.path} (lines {sl.start_line}-{sl.end_line})"
            if sl.note:
                header += f" — {sl.note}"
            parts.append(header + "\n" + sl.text)
        out = "\n\n---\n\n".join(parts)
        if len(out) <= max_chars:
            return out
        return out[: max_chars - 20] + "\n… [truncated]"


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8", errors="replace")
    return raw.splitlines()


def _tail_lines(lines: list[str], max_lines: int) -> tuple[list[str], int, int]:
    if not lines:
        return [], 0, 0
    n = min(max_lines, len(lines))
    chunk = lines[-n:]
    start = len(lines) - n + 1
    end = len(lines)
    return chunk, start, end


def _split_gate_processed(full: str) -> tuple[str, str]:
    marker = re.search(r"^## Processed\s*$", full, re.MULTILINE)
    if not marker:
        return "", full
    return full[: marker.start()], full[marker.start() :]


def collect_bundle(
    *,
    user_id: str,
    repo_root: Path,
    lookback_days: int,
    transcript_tail_chars: int,
    max_jsonl_lines: int,
    max_processed_chars: int,
    negative_examples_max_chars: int,
) -> ReflectionBundle:
    from grace_mar.reflection.constants import (
        MAX_NEGATIVE_EXAMPLES_CHARS,
        MAX_PROCESSED_GATE_CHARS,
    )

    neg_cap = min(negative_examples_max_chars, MAX_NEGATIVE_EXAMPLES_CHARS)
    proc_cap = min(max_processed_chars, MAX_PROCESSED_GATE_CHARS)

    profile = repo_root / "users" / user_id
    bundle = ReflectionBundle(
        user_id=user_id,
        lookback_days=lookback_days,
        repo_root=repo_root,
        meta={
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "lookback_days": lookback_days,
        },
    )

    # session-transcript — tail by char budget (approximate line tail)
    st_path = profile / "session-transcript.md"
    if st_path.exists():
        raw = st_path.read_text(encoding="utf-8", errors="replace")
        tail = raw[-transcript_tail_chars:] if len(raw) > transcript_tail_chars else raw
        lines = tail.splitlines()
        # recompute start line in file
        prefix = raw[: len(raw) - len(tail)]
        start_line = prefix.count("\n") + 1 if tail else 1
        end_line = start_line + len(lines) - 1 if lines else start_line
        rel = f"users/{user_id}/session-transcript.md"
        bundle.slices.append(
            TextSlice(rel, start_line, end_line, "\n".join(lines), note="tail for lookback")
        )

    # JSONL tails
    for name in ("pipeline-events.jsonl", "merge-receipts.jsonl", "compute-ledger.jsonl"):
        p = profile / name
        if not p.exists():
            continue
        lines = _read_lines(p)
        chunk, start, end = _tail_lines(lines, max_jsonl_lines)
        rel = f"users/{user_id}/{name}"
        bundle.slices.append(TextSlice(rel, start, end, "\n".join(chunk), note=f"last {len(chunk)} lines"))

    # self-evidence — last ~120 lines
    se_path = profile / "self-evidence.md"
    if se_path.exists():
        lines = _read_lines(se_path)
        chunk, start, end = _tail_lines(lines, 120)
        bundle.slices.append(
            TextSlice(
                f"users/{user_id}/self-evidence.md",
                start,
                end,
                "\n".join(chunk),
                note="recent activity log",
            )
        )

    # recursion-gate — processed section only (reject/approve patterns)
    gate_path = profile / "recursion-gate.md"
    if gate_path.exists():
        full = gate_path.read_text(encoding="utf-8", errors="replace")
        _active, processed = _split_gate_processed(full)
        if processed:
            proc = processed
            if len(proc) > proc_cap:
                proc = proc[: proc_cap] + "\n… [truncated processed section]"
            bundle.slices.append(
                TextSlice(
                    f"users/{user_id}/recursion-gate.md",
                    1,
                    1,
                    "## Processed (excerpt)\n" + proc,
                    note="processed candidates excerpt",
                )
            )

    # Optional small JSON snapshots (full file if small)
    for jname in ("intent_snapshot.json", "symbolic_identity.json", "curriculum_profile.json"):
        jp = profile / jname
        if jp.exists() and jp.stat().st_size < 80_000:
            try:
                data = json.loads(jp.read_text(encoding="utf-8"))
                text = json.dumps(data, indent=2, ensure_ascii=False)[:25_000]
            except json.JSONDecodeError:
                text = jp.read_text(encoding="utf-8", errors="replace")[:25_000]
            lines = text.splitlines()
            bundle.slices.append(
                TextSlice(
                    f"users/{user_id}/{jname}",
                    1,
                    len(lines),
                    text,
                    note="snapshot",
                )
            )

    slib = profile / "self-library.md"
    if slib.exists() and slib.stat().st_mtime:
        # excerpt head + tail if large
        raw = slib.read_text(encoding="utf-8", errors="replace")
        if len(raw) > 40_000:
            excerpt = raw[:20_000] + "\n…\n" + raw[-15_000:]
        else:
            excerpt = raw
        lines = excerpt.splitlines()
        bundle.slices.append(
            TextSlice(
                f"users/{user_id}/self-library.md",
                1,
                len(lines),
                "\n".join(lines),
                note="SELF-LIBRARY excerpt",
            )
        )

    # journal tail
    jpath = profile / "journal.md"
    if jpath.exists():
        lines = _read_lines(jpath)
        chunk, start, end = _tail_lines(lines, 80)
        bundle.slices.append(
            TextSlice(f"users/{user_id}/journal.md", start, end, "\n".join(chunk), note="journal tail")
        )

    # Negative learning
    neg_path = profile / "reflection-proposals" / "negative-examples.md"
    if neg_path.exists():
        raw = neg_path.read_text(encoding="utf-8", errors="replace")
        if len(raw) > neg_cap:
            raw = raw[-neg_cap:]
        ls = raw.splitlines()
        bundle.slices.append(
            TextSlice(
                f"users/{user_id}/reflection-proposals/negative-examples.md",
                1,
                len(ls),
                raw,
                note="rejected reflection hints",
            )
        )

    return bundle
