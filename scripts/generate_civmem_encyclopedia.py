#!/usr/bin/env python3
"""
Build hybrid civ-mem encyclopedia: one fat ENCYCLOPEDIA.md + lib-stubs.yaml.

Default CMC root: repos/civilization_memory (sibling to scripts from repo root).
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CMC = REPO_ROOT / "repos" / "civilization_memory"
OUT_DIR_DEFAULT = REPO_ROOT / "users" / "grace-mar" / "artifacts" / "civ-mem-encyclopedia"
SKIP_DIRS = {".git", "node_modules", ".cache", ".skeleton", "apps"}


def collect_md(cmc: Path, include_content: bool, essays_only: bool) -> list[Path]:
    """Default: docs/ only. --essays-only: docs/essays only (small, committable). --include-content: + content/."""
    out: list[Path] = []
    if essays_only:
        d = cmc / "docs" / "essays"
        if d.is_dir():
            for p in sorted(d.glob("*.md")):
                out.append(p)
        return out
    for sub in ("docs", "content") if include_content else ("docs",):
        d = cmc / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            out.append(p)
    return sorted(set(out))


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:120]
    return ""


def blurb(text: str, n: int = 200) -> str:
    body = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
    body = re.sub(r"#[^\n]+\n", "", body)
    one = " ".join(body.split())[:n]
    return one + ("…" if len(one) >= n else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmc", type=Path, default=DEFAULT_CMC, help="Civilization_memory repo root")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("-o", "--out", type=Path, default=None)
    ap.add_argument(
        "--include-content",
        action="store_true",
        help="Also scan content/ (very large; local regen only)",
    )
    ap.add_argument(
        "--essays-only",
        action="store_true",
        help="Only docs/essays/*.md — small fat file + few LIB stubs (default for first commit)",
    )
    args = ap.parse_args()
    cmc: Path = args.cmc
    out_dir = args.out or (REPO_ROOT / "users" / args.user / "artifacts" / "civ-mem-encyclopedia")
    out_dir.mkdir(parents=True, exist_ok=True)
    enc_path = out_dir / "ENCYCLOPEDIA.md"
    stubs_path = out_dir / "lib-stubs.yaml"

    if not cmc.is_dir():
        print(f"CMC root missing: {cmc}", flush=True)
        return 1

    files = collect_md(cmc, args.include_content, args.essays_only)
    lines = [
        f"# Civ-mem encyclopedia (generated {date.today().isoformat()})",
        "",
        f"_Source repo: `{cmc}` — do not edit by hand; regen with `generate_civmem_encyclopedia.py`._",
        "",
    ]
    stub_lines = [
        "# Paste under self-library.md entries: (renumber id LIB-#### if needed; gate before merge)",
        "# status draft until merged",
        "",
    ]
    rel_base = cmc.resolve()

    for i, path in enumerate(files):
        rel = path.relative_to(rel_base)
        text = path.read_text(encoding="utf-8", errors="replace")
        anchor = f"CMC:{rel.as_posix()}"
        title = first_heading(text) or rel.stem.replace("-", " ").title()
        scope_bits = [rel.parts[0], rel.stem.lower().replace("_", "-")]
        if "essays" in rel.parts:
            scope_bits.append("essays")
        scope_bits.append("civilization_memory")
        scope_unique = []
        for s in scope_bits:
            if s and s not in scope_unique:
                scope_unique.append(s)
        scopes = ", ".join(f'"{s}"' for s in scope_unique[:8])
        bl = blurb(text).replace('"', "'")

        lines.append(f"## {anchor}")
        lines.append("")
        lines.append(f"*Path:* `{rel.as_posix()}`")
        lines.append("")
        lines.append(text.strip())
        lines.append("")
        lines.append("---")
        lines.append("")

        gh = f"https://github.com/rbtkhn/civilization_memory/blob/main/{rel.as_posix()}"
        stub_lines.append(f"  # --- CMC stub {i + 1}: {rel.as_posix()} ---")
        stub_lines.append("  - id: LIB-NNNN  # assign next free id")
        stub_lines.append(f'    title: "CMC — {title}"')
        stub_lines.append('    author: "civilization_memory"')
        stub_lines.append('    lane: "reference"')
        stub_lines.append('    type: "article"')
        stub_lines.append('    status: "active"')
        stub_lines.append('    engagement_status: "trusted"')
        stub_lines.append('    lookup_priority: "medium"')
        stub_lines.append(f"    scope: [{scopes}]")
        stub_lines.append('    source: "path"')
        stub_lines.append(f'    url: "{gh}"')
        stub_lines.append(f"    added_at: {date.today().isoformat()}")
        stub_lines.append(f'    notes: "Anchor ## {anchor} in ENCYCLOPEDIA.md. {bl}"')
        stub_lines.append("")

    enc_path.write_text("\n".join(lines), encoding="utf-8")
    stubs_path.write_text("\n".join(stub_lines), encoding="utf-8")
    print(f"Wrote {enc_path} ({len(files)} sources)")
    print(f"Wrote {stubs_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
