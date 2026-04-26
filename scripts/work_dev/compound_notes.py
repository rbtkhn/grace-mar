"""
Shared parsing for work-dev compound notes. Stdlib only.
Used by work_dev_compound_refresh.py, export_work_dev_compound_gate_candidates.py,
and build_work_dev_compound_dashboard.py.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "compound-notes"
# Stale and duplicate heuristics — keep in sync with work_dev_compound_refresh / dashboard
STALE_DAYS = 90


def derived_compound_artifact_preamble(artifact_kind: str) -> str:
    """
    YAML front matter for derived work-dev compound markdown artifacts.
    Aligns vocabulary with work-dev JSON surfaces (recordAuthority / gateEffect none), not a JSON schema.
    """
    k = (artifact_kind or "").strip()
    if not k or not re.match(r"^[A-Za-z0-9_\-]+$", k):
        k = "unknown"
    return (
        "---\n"
        "derived: true\n"
        "recordAuthority: none\n"
        "gateEffect: none\n"
        f"artifact_kind: {k}\n"
        "---\n"
    )


def parse_front_matter(text: str) -> dict[str, Any]:
    """Parse first --- ... --- block. Handles generated notes; no PyYAML."""
    if not text.lstrip().startswith("---"):
        return {}
    first = text.find("\n", text.index("---")) + 1
    end_idx = text.find("\n---\n", first)
    if end_idx == -1:
        return {}
    block = text[first:end_idx]
    data: dict[str, Any] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" not in line or not line.split(":", 1)[0].strip():
            i += 1
            continue
        key, rest = line.split(":", 1)
        key = key.strip()
        val = rest.strip()
        if key == "affected_files" and not val:
            j = i + 1
            acc: list[str] = []
            while j < len(lines) and lines[j].lstrip().startswith("- "):
                raw = lines[j].lstrip()
                if raw.startswith("- "):
                    acc.append(raw[2:].strip().strip("'\""))
                j += 1
            i = j
            data[key] = acc
            continue
        if key == "affected_files" and val == "[]":
            data[key] = []
        elif val == "[]":
            data[key] = []
        elif val == "true" or val == "false":
            data[key] = val == "true"
        else:
            s = val
            if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
                s = s[1:-1]
            data[key] = s
        i += 1
    return data


def gate_candidate_truthy(value: Any) -> bool:
    """True for gate_candidate when operator intends staging consideration."""
    if value is True:
        return True
    if value is False or value is None:
        return False
    s = str(value).strip()
    if not s:
        return False
    return s.lower() in (
        "true",
        "1",
        "yes",
        "y",
    )


def body_after_front_matter(text: str) -> str:
    """Return markdown body after the first closing --- of front matter."""
    if not text.lstrip().startswith("---"):
        return text
    end_idx = text.find("\n---\n", text.find("---") + 3)
    if end_idx == -1:
        return ""
    return text[end_idx + 5 :].lstrip("\n")


def extract_h2_section(body: str, title: str) -> str:
    """
    Return content under ## {title} until the next ## line (H2). Case-sensitive title.
    """
    lines = body.splitlines()
    header = f"## {title}"
    started = False
    buf: list[str] = []
    for line in lines:
        if not started:
            if line == header:
                started = True
            continue
        if line.startswith("## "):
            break
        buf.append(line)
    return "\n".join(buf).strip()


def load_note_file(
    path: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """
    Return meta from front matter, body text, and paths relative to repo root.
    `path` and `source_path` are the same relative path (duplicate keys for callers).
    When repo_root is None, uses the package REPO_ROOT.
    """
    root = (repo_root or REPO_ROOT).resolve()
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_front_matter(text)
    rel = str(path.resolve().relative_to(root))
    return {
        "path": rel,
        "source_path": rel,
        "name": path.name,
        "meta": meta,
        "body": body_after_front_matter(text),
    }


def parse_compound_note_record(
    path: Path,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    """Record shape for refresh report aggregation."""
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_front_matter(text)
    gate = gate_candidate_truthy(meta.get("gate_candidate", False))
    return {
        "path": str(path.resolve().relative_to(repo_root)),
        "name": path.name,
        "title": str(meta.get("title", path.stem)).strip("'\"") or path.stem,
        "date": str(meta.get("date", "")),
        "problem_type": str(meta.get("problem_type", "")).strip("'\""),
        "reusable_pattern": str(meta.get("reusable_pattern", "")).strip("'\""),
        "self_catching_test": str(meta.get("self_catching_test", "unknown")).strip("'\""),
        "gate_candidate": gate,
        "record_status": str(meta.get("record_status", "")).strip("'\""),
    }


def parse_date_ymd(s: str) -> date | None:
    """Parse YYYY-MM-DD from the first 10 chars; None if invalid."""
    s = (s or "")[:10]
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def normalize_dup_key(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower()) if s else ""


def compound_note_paths(notes_dir: Path) -> list[Path]:
    if not notes_dir.is_dir():
        return []
    return sorted(notes_dir.glob("*.md"))


def load_compound_records(notes_dir: Path, repo_root: Path) -> list[dict[str, Any]]:
    return [parse_compound_note_record(p, repo_root) for p in compound_note_paths(notes_dir)]


def duplicate_title_groups(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    title_groups: dict[str, list[str]] = {}
    for r in records:
        nk = normalize_dup_key(str(r.get("title", "")))
        if nk and nk not in ("compound note", "untitled"):
            title_groups.setdefault(nk, []).append(str(r.get("name", "")))
    return {k: v for k, v in title_groups.items() if len(v) > 1}


def duplicate_pattern_groups(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    pat_groups: dict[str, list[str]] = {}
    for r in records:
        p = str(r.get("reusable_pattern", "") or "")
        if p:
            pk = normalize_dup_key(p)
            pat_groups.setdefault(pk, []).append(str(r.get("name", "")))
    return {k: v for k, v in pat_groups.items() if len(v) > 1}


def name_to_path_map(notes_dir: Path) -> dict[str, Path]:
    return {p.name: p for p in compound_note_paths(notes_dir)}


def stale_non_gate_records(
    records: list[dict[str, Any]],
    notes_dir: Path,
    today: date,
    *,
    stale_days: int = STALE_DAYS,
    mtime_if_no_date: bool = False,
) -> list[dict[str, Any]]:
    """
    Notes with gate_candidate false and age > stale_days.
    If mtime_if_no_date, use file mtime when front matter date is missing or unparseable.
    Each item is the record plus _effective_date (ISO) and _date_source ('front matter' | 'file mtime').
    """
    nmap = name_to_path_map(notes_dir)
    out: list[dict[str, Any]] = []
    for r in records:
        if r.get("gate_candidate"):
            continue
        d = parse_date_ymd(str(r.get("date") or ""))
        src = "front matter"
        if d is None and mtime_if_no_date:
            p = nmap.get(str(r.get("name", "")))
            if p is None or not p.is_file():
                continue
            d = date.fromtimestamp(p.stat().st_mtime)
            src = "file mtime"
        elif d is None:
            continue
        if (today - d).days > stale_days:
            row = dict(r)
            row["_effective_date"] = d.isoformat()
            row["_date_source"] = src
            out.append(row)
    return sorted(out, key=lambda x: str(x.get("date") or x.get("_effective_date", "")))


def _affected_list(meta: dict[str, Any]) -> list[str]:
    raw = meta.get("affected_files", [])
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw]
    if isinstance(raw, str) and raw.strip() == "[]":
        return []
    return [str(raw)] if raw else []


def parse_note_for_export(
    path: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """
    Rich record for gate export: meta, body, affected_files list, gate flag.
    """
    raw = load_note_file(path, repo_root=repo_root)
    meta = raw["meta"]
    body = raw["body"]
    if not meta and not body.strip() and not path.name.startswith("."):
        return {}
    gate = gate_candidate_truthy(meta.get("gate_candidate", False))
    return {
        "path": raw["path"],
        "name": raw["name"],
        "title": str(meta.get("title", path.stem)).strip("'\"") or path.stem,
        "date": str(meta.get("date", "")),
        "source_pr": str(meta.get("source_pr", "")).strip("'\""),
        "source_commit": str(meta.get("source_commit", "")).strip("'\""),
        "affected_files": _affected_list(meta),
        "problem_type": str(meta.get("problem_type", "")).strip("'\""),
        "reusable_pattern": str(meta.get("reusable_pattern", "")).strip("'\""),
        "self_catching_test": str(meta.get("self_catching_test", "unknown")).strip("'\""),
        "gate_candidate": gate,
        "body": body,
        "meta": meta,
    }
