#!/usr/bin/env python3
"""
Validate MCP execution receipts under artifacts/mcp-receipts/*.json against
schemas/mcp-execution-receipt.v1.json and current MCP configs.

  python3 scripts/mcp_receipt_audit.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from mcp_receipt_lib import (  # noqa: E402
    BINDINGS_PATH,
    CAPABILITIES_PATH,
    load_yaml,
    validate_mcp_receipt,
)

DEFAULT_RECEIPTS_DIR = REPO_ROOT / "artifacts" / "mcp-receipts"
DEFAULT_REPORT = REPO_ROOT / "artifacts" / "mcp-receipt-report.md"


def _git_short_hash(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.TimeoutError, subprocess.TimeoutExpired):
        pass
    return "unknown"


def _safe_rel(path: Path, root: Path) -> Path | str:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit MCP execution receipt JSON files.")
    ap.add_argument("--receipts-dir", type=Path, default=DEFAULT_RECEIPTS_DIR)
    ap.add_argument("--capabilities", type=Path, default=CAPABILITIES_PATH)
    ap.add_argument("--bindings", type=Path, default=BINDINGS_PATH)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    root = args.repo_root.resolve()
    rdir = args.receipts_dir.resolve()
    caps_doc = load_yaml(args.capabilities.resolve())
    bind_doc = load_yaml(args.bindings.resolve())

    files = sorted(rdir.glob("*.json")) if rdir.is_dir() else []
    rows: list[tuple[str, str, list[str]]] = []
    any_fail = False

    for fp in files:
        rel = str(_safe_rel(fp, root))
        try:
            receipt = json.loads(fp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rows.append((rel, "FAIL", [f"JSON parse: {e}"]))
            any_fail = True
            continue

        viols, warns = validate_mcp_receipt(receipt, caps_doc, bind_doc)
        combine = list(viols)
        if warns:
            combine.extend([f"(warning) {w}" for w in warns])
        if viols:
            any_fail = True
            rows.append((rel, "FAIL", combine))
        else:
            rows.append((rel, "PASS", combine))

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    git_ref = _git_short_hash(root)

    passed = sum(1 for _r, st, _v in rows if st == "PASS")
    failed = sum(1 for _r, st, _v in rows if st == "FAIL")

    lines = [
        "# MCP execution receipt audit",
        "",
        f"- **Generated (UTC):** {ts}",
        f"- **Git:** `{git_ref}`",
        f"- **Status:** {'**FAIL**' if any_fail else '**PASS**'}",
        "",
        "## Summary",
        "",
        f"- Files scanned: **{len(files)}**",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        "",
        "## Results",
        "",
    ]

    if not files:
        lines.append("_No `*.json` files under receipts directory._")
        lines.append("")
    else:
        for rel, st, msgs in rows:
            lines.append(f"### `{rel}` — {st}")
            if msgs:
                for m in msgs:
                    lines.append(f"- {m}")
            lines.append("")

    lines.append("")
    out_path = args.output.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {_safe_rel(out_path, root)} — scanned={len(files)} failed={failed}", file=sys.stderr)

    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
