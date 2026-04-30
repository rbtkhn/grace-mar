#!/usr/bin/env python3
"""Generate the Strategy Notebook browser fixture from the live notebook tree.

The fixture is intentionally small: it indexes dates, raw-input files, and
per-expert file groups. The browser fetches the selected Markdown file directly
from the local HTTP server, so the JSON does not duplicate the notebook body.

WORK only. Does not touch Record, gate, or users/ paths.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_NOTEBOOK = "docs/skill-work/work-strategy/strategy-notebook"
DEFAULT_OUT = (
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/"
    "workbench-visualizer/strategy-notebook-visualizer.fixture.json"
)
SCHEMA_VERSION = "strategy-notebook-browser-fixture/v2"
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
THREAD_FIELD_RE = re.compile(
    r"^-\s+\*\*(?P<field>Thread file|Thread month|Thread role|Continuity delta):\*\*\s*(?P<value>.*)$",
    re.MULTILINE,
)
LINK_RE = re.compile(r"\[[^\]]+\]\((?P<href>[^)]+)\)")


def _repo_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def _notebook_rel(path: Path, notebook: Path) -> str:
    return path.resolve().relative_to(notebook.resolve()).as_posix()


def _read_head(path: Path, limit: int = 12000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def _heading(text: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _thread_binding_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for m in THREAD_FIELD_RE.finditer(text):
        key = m.group("field").lower().replace(" ", "")
        value = m.group("value").strip().strip("`")
        if key == "threadfile":
            link = LINK_RE.search(value)
            if link:
                value = link.group("href")
        fields[key] = value
    return fields


def _title_for(path: Path) -> str:
    text = _read_head(path, 4000)
    fm = _frontmatter(text)
    return fm.get("title") or _heading(text) or path.stem.replace("-", " ")


def _meta_for(path: Path, notebook: Path) -> dict[str, Any]:
    text = _read_head(path)
    fm = _frontmatter(text)
    dates = sorted(set(DATE_RE.findall(path.name) + DATE_RE.findall(text[:3000])))
    binding = _thread_binding_fields(text)
    meta = {
        "name": path.name,
        "title": fm.get("title") or _heading(text) or path.name,
        "path": _notebook_rel(path, notebook),
        "repoPath": _repo_rel(path),
        "kind": fm.get("kind") or _kind_from_name(path.name),
        "thread": fm.get("thread") or _thread_from_name(path.name),
        "pubDate": fm.get("pub_date") or (dates[0] if dates else None),
        "ingestDate": fm.get("ingest_date"),
        "sourceUrl": fm.get("source_url"),
        "bytes": path.stat().st_size,
    }
    if binding:
        meta["threadBinding"] = binding
    return meta


def _kind_from_name(name: str) -> str:
    lo = name.lower()
    if lo.startswith("transcript-") or "transcript" in lo:
        return "transcript"
    if lo.startswith("substack-"):
        return "substack"
    if lo.startswith("youtube-"):
        return "youtube"
    if lo.startswith("x-"):
        return "x"
    if lo.endswith(".yaml") or lo.endswith(".yml"):
        return "manifest"
    return "note"


def _thread_from_name(name: str) -> str | None:
    bits = name.lower().replace(".md", "").split("-")
    for prefix in ("substack", "transcript", "youtube", "duran", "x"):
        if len(bits) > 1 and bits[0] == prefix:
            return bits[1]
    return None


def _profile_name(profile: Path, fallback: str) -> str:
    text = _read_head(profile, 6000)
    for line in text.splitlines():
        if "| **Name** |" in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                return re.sub(r"`([^`]+)`", r"\1", parts[1]).strip()
    h = _heading(text)
    if h:
        return h.replace("Strategy expert -", "").replace("Strategy expert --", "").strip()
    return fallback


def _group_expert_file(path: Path, expert_id: str) -> str:
    name = path.name.lower()
    if name == "profile.md":
        return "bio"
    if name == "thread.md" or re.fullmatch(rf"{re.escape(expert_id)}-thread-\d{{4}}-\d{{2}}\.md", name):
        return "threads"
    if name == "transcript.md" or "transcript" in name:
        return "transcripts"
    if name == "mind.md" or name.endswith("-mind.md"):
        return "minds"
    if "-page-" in name and "template" not in name:
        return "pages"
    if "template" in name:
        return "templates"
    if name.endswith((".yaml", ".yml", ".json")) or "manifest" in name:
        return "manifests"
    if name.startswith(f"{expert_id}-page-"):
        return "pages"
    return "other"


def _build_fixture(notebook_rel: str) -> dict[str, Any]:
    notebook = (REPO_ROOT / notebook_rel).resolve()
    if not notebook.is_dir():
        raise SystemExit(f"error: missing notebook directory: {notebook}")

    raw_root = notebook / "raw-input"
    dates: list[dict[str, Any]] = []
    if raw_root.is_dir():
        for day in sorted(raw_root.iterdir()):
            if not day.is_dir() or not DATE_RE.fullmatch(day.name):
                continue
            files = [
                _meta_for(p, notebook)
                for p in sorted(day.iterdir())
                if p.is_file() and not p.name.startswith(".")
            ]
            dates.append({"date": day.name, "count": len(files), "files": files})

    experts: list[dict[str, Any]] = []
    experts_root = notebook / "experts"
    if experts_root.is_dir():
        for expert_dir in sorted(experts_root.iterdir()):
            if not expert_dir.is_dir() or expert_dir.name.startswith("."):
                continue
            expert_id = expert_dir.name
            groups: dict[str, list[dict[str, Any]]] = {
                "bio": [],
                "threads": [],
                "transcripts": [],
                "minds": [],
                "pages": [],
                "templates": [],
                "manifests": [],
                "other": [],
            }
            for path in sorted(expert_dir.iterdir()):
                if not path.is_file() or path.name.startswith("."):
                    continue
                group = _group_expert_file(path, expert_id)
                groups[group].append(_meta_for(path, notebook))
            profile = expert_dir / "profile.md"
            experts.append(
                {
                    "id": expert_id,
                    "label": _profile_name(profile, expert_id) if profile.is_file() else expert_id,
                    "path": _notebook_rel(expert_dir, notebook) + "/",
                    "repoPath": _repo_rel(expert_dir),
                    "counts": {k: len(v) for k, v in groups.items()},
                    "files": groups,
                }
            )

    return {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "recordAuthority": "none",
        "gateEffect": "none",
        "truthScope": "local strategy-notebook file index only",
        "notebookRoot": notebook_rel,
        "launchPath": "demo-runs/workbench-visualizer/strategy-notebook-visualizer.html",
        "dates": dates,
        "experts": experts,
    }


def _stable_for_compare(data: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    normalized = copy.deepcopy(data)
    if existing and isinstance(existing.get("generatedAt"), str):
        normalized["generatedAt"] = existing["generatedAt"]
    return normalized


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--notebook", default=DEFAULT_NOTEBOOK)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    out = (REPO_ROOT / args.out).resolve()
    fixture = _build_fixture(args.notebook)

    if args.check:
        if not out.is_file():
            print(f"check: missing fixture: {out}", file=sys.stderr)
            return 1
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"check: cannot parse fixture: {e}", file=sys.stderr)
            return 1
        expected = _stable_for_compare(fixture, existing)
        if existing != expected:
            print("check: fixture would change", file=sys.stderr)
            print(
                f"  dates: was {len(existing.get('dates', []))} now {len(expected.get('dates', []))}",
                file=sys.stderr,
            )
            print(
                f"  experts: was {len(existing.get('experts', []))} now {len(expected.get('experts', []))}",
                file=sys.stderr,
            )
            return 1
        print(
            f"ok: fixture up to date ({len(existing.get('dates', []))} dates, "
            f"{len(existing.get('experts', []))} experts)"
        )
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote fixture: {out} "
        f"(dates: {len(fixture['dates'])}, experts: {len(fixture['experts'])})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
