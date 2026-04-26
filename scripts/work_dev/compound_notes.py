"""
Shared parsing for work-dev compound notes. Stdlib only.
Used by work_dev_compound_refresh.py and export_work_dev_compound_gate_candidates.py.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "compound-notes"


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
