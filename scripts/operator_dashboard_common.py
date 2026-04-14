"""Shared helpers for operator Markdown dashboards (derived artifacts only)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def extract_yaml_scalar(blob: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", blob, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    return val or None


def load_self_library_entries(repo_root: Path, user_id: str) -> list[dict[str, Any]]:
    path = repo_root / "users" / user_id / "self-library.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    idx = text.find("## Entries")
    if idx < 0:
        return []
    j = text.find("```yaml", idx)
    if j < 0:
        return []
    j += len("```yaml")
    if j < len(text) and text[j] == "\n":
        j += 1
    k = text.find("\n```", j)
    if k < 0:
        return []
    block = text[j:k]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    entries = data.get("entries")
    if not isinstance(entries, list):
        return []
    return [e for e in entries if isinstance(e, dict) and e.get("id")]
