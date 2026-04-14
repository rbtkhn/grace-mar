"""Shared helpers for new_work_note / new_evidence_stub / new_candidate_draft."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def slugify(title: str, *, max_len: int = 60) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "note"
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s


def resolve_repo_root(explicit: Path | None) -> Path:
    return explicit.resolve() if explicit else REPO_ROOT


def ensure_output_dir_under_repo(output_dir: Path, repo_root: Path) -> Path:
    out = output_dir.resolve()
    root = repo_root.resolve()
    try:
        out.relative_to(root)
    except ValueError as e:
        raise ValueError(f"Output directory must be under repo root {root}: {out}") from e
    if ".." in str(output_dir):
        raise ValueError("Output path must not contain '..'")
    out.mkdir(parents=True, exist_ok=True)
    return out


def today_iso() -> str:
    return date.today().isoformat()


def set_header_field(body: str, key: str, value: str) -> str:
    """Set first `Key: ...` line under the title block (key matches case-insensitive key + colon)."""
    prefix = f"{key}:"
    lines = body.splitlines(keepends=True)
    out: list[str] = []
    done = False
    for line in lines:
        stripped = line.lstrip()
        if not done and stripped.lower().startswith(prefix.lower()):
            nl = "\n" if line.endswith("\n") else ""
            out.append(f"{prefix} {value}{nl}")
            done = True
        else:
            out.append(line)
    if not done:
        raise ValueError(f"Template missing header field {prefix!r}")
    return "".join(out)


def write_from_template(
    *,
    template_rel: str,
    output_dir: Path,
    repo_root: Path,
    filename: str,
    fields: list[tuple[str, str]],
) -> Path:
    tpl = (repo_root / "docs" / "templates" / template_rel).resolve()
    try:
        tpl.relative_to(repo_root.resolve())
    except ValueError as e:
        raise ValueError(f"Template must live under repo: {tpl}") from e
    body = tpl.read_text(encoding="utf-8")
    for key, value in fields:
        body = set_header_field(body, key, value)
    out_dir = ensure_output_dir_under_repo(output_dir, repo_root)
    dest = out_dir / filename
    dest.write_text(body, encoding="utf-8")
    return dest
