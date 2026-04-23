#!/usr/bin/env python3
"""Bundle strategy-notebook sources for compiled-view recipes (WORK only).

Emits a deterministic markdown **source bundle**: machine layers, strategy-page
blocks, and optional inbox / chapter tails. Does **not** call an LLM.

Default recipe: expert polyphony (RECIPE-STRATEGY-POLYPHONY-2026-04-22-001).

Usage::

    python3 scripts/compile_strategy_view.py
    python3 scripts/compile_strategy_view.py --notebook-dir docs/.../strategy-notebook
    python3 scripts/compile_strategy_view.py --date 2026-04-21 --experts mercouris,mearsheimer
    python3 scripts/compile_strategy_view.py --out /tmp/bundle.md

Date semantics: ``--date`` selects the calendar day for the output filename and
for resolving ``chapters/YYYY-MM/`` (local **date** string, not UTC shift).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import (  # noqa: E402
    RE_IN_FOLDER_MONTH_THREAD,
    THREAD_MARKER_END,
    THREAD_MARKER_START,
    collect_strategy_thread_paths,
)
from strategy_notebook.receipts import (  # noqa: E402
    NotebookReceipt,
    PageOperation,
    append_receipt,
    rel_posix,
)
from strategy_page_reader import discover_pages  # noqa: E402

RECIPE_ID = "RECIPE-STRATEGY-POLYPHONY-2026-04-22-001"
RE_FLAT_THREAD = re.compile(r"^strategy-expert-(.+)-thread(?:-(\d{4}-\d{2}))?\.md$")


def expert_id_from_thread_path(path: Path, notebook_dir: Path) -> str | None:
    """Best-effort expert/voice id from a thread file path under notebook_dir."""
    try:
        rel = path.resolve().relative_to(notebook_dir.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    if parts[0] in ("experts", "voices") and len(parts) >= 2:
        if parts[-1] == "thread.md":
            return parts[1]
        m = RE_IN_FOLDER_MONTH_THREAD.match(parts[-1])
        if m:
            return m.group(1)
    name = path.name
    m2 = RE_FLAT_THREAD.match(name)
    if m2:
        return m2.group(1)
    return None


def extract_machine_layer(text: str) -> str | None:
    if THREAD_MARKER_START not in text or THREAD_MARKER_END not in text:
        return None
    _, _, rest = text.partition(THREAD_MARKER_START)
    inner, _, _ = rest.partition(THREAD_MARKER_END)
    return inner.strip() or None


def journal_above_machine(text: str, max_chars: int) -> str:
    """Journal layer: content before the machine fence (truncated)."""
    if THREAD_MARKER_START not in text:
        body = text.strip()
    else:
        body = text.split(THREAD_MARKER_START, 1)[0].strip()
    if len(body) > max_chars:
        return body[: max_chars - 20].rstrip() + "\n\n… *[truncated]* …"
    return body


def tail_lines(path: Path, n: int, max_chars: int) -> str:
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    chunk = "\n".join(lines[-n:])
    if len(chunk) > max_chars:
        return chunk[-max_chars:]
    return chunk


def build_bundle(
    notebook_dir: Path,
    bundle_date: date,
    expert_filter: frozenset[str] | None,
    inbox_tail_lines: int,
    max_journal_chars: int,
    max_machine_chars: int,
) -> str:
    """Return full markdown bundle."""
    ymd = bundle_date.isoformat()
    ym = ymd[:7]
    lines: list[str] = []

    lines.append("<!-- compiled-view-bundle: strategy-notebook WORK only; derived; not SSOT -->")
    lines.append("")
    lines.append(f"# Source bundle — expert polyphony ({ymd})")
    lines.append("")
    lines.append(f"**Recipe ID:** `{RECIPE_ID}`")
    lines.append("")
    lines.append(
        "**Disclaimer:** Derived artifact. Do not treat as authoritative. "
        "Canonical state lives in expert `thread.md` files, `strategy-page` blocks, "
        "`days.md`, and `meta.md`. Regenerate after source changes; do not hand-edit "
        "the dated snapshot this bundle feeds."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    inbox = notebook_dir / "daily-strategy-inbox.md"
    if inbox.is_file():
        lines.append(f"## Inbox tail (`{inbox.name}`, last {inbox_tail_lines} lines)")
        lines.append("")
        lines.append("```")
        lines.append(tail_lines(inbox, inbox_tail_lines, 12000))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    days_path = notebook_dir / "chapters" / ym / "days.md"
    meta_path = notebook_dir / "chapters" / ym / "meta.md"
    if days_path.is_file():
        lines.append(f"## Chapter days.md tail (`chapters/{ym}/days.md`)")
        lines.append("")
        lines.append("```")
        lines.append(tail_lines(days_path, 80, 16000))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    if meta_path.is_file():
        lines.append(f"## Chapter meta.md tail (`chapters/{ym}/meta.md`)")
        lines.append("")
        lines.append("```")
        lines.append(tail_lines(meta_path, 120, 16000))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    thread_paths = collect_strategy_thread_paths(notebook_dir)
    filtered: list[Path] = []
    for p in sorted(thread_paths, key=lambda x: str(x)):
        eid = expert_id_from_thread_path(p, notebook_dir)
        if eid is None:
            continue
        if expert_filter is not None and eid.lower() not in expert_filter:
            continue
        filtered.append(p)

    lines.append(f"## Expert / voice threads ({len(filtered)} files)")
    lines.append("")

    for p in filtered:
        eid = expert_id_from_thread_path(p, notebook_dir) or "unknown"
        rel = p.resolve().relative_to(notebook_dir.resolve())
        text = p.read_text(encoding="utf-8")
        lines.append(f"### `{eid}` — `{rel.as_posix()}`")
        lines.append("")

        pages = discover_pages(p, expert_id=eid)
        if pages:
            lines.append("#### strategy-page blocks")
            lines.append("")
            for pg in pages[-5:]:
                lines.append(
                    f"- **id=`{pg.id}`** date=`{pg.date}` watch=`{pg.watch}`"
                )
                body = pg.content.strip()
                if len(body) > max_journal_chars:
                    body = body[: max_journal_chars - 30].rstrip() + "\n\n… *[truncated]* …"
                lines.append("")
                lines.append(body)
                lines.append("")
        else:
            lines.append("*No `strategy-page` blocks discovered in this file.*")
            lines.append("")

        ml = extract_machine_layer(text)
        lines.append("#### Machine layer (`strategy-expert-thread` fence)")
        lines.append("")
        if ml:
            if len(ml) > max_machine_chars:
                ml = ml[: max_machine_chars - 30].rstrip() + "\n\n… *[truncated]* …"
            lines.append("```")
            lines.append(ml)
            lines.append("```")
        else:
            lines.append("*No machine layer fence in this file.*")
        lines.append("")

        j = journal_above_machine(text, max_journal_chars)
        if j:
            lines.append("#### Journal layer (above machine fence, truncated)")
            lines.append("")
            lines.append(j)
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.append("## Symphony Snapshot skeleton (fill per recipe)")
    lines.append("")
    lines.append("Use [expert-polyphony-synthesis.md](recipes/expert-polyphony-synthesis.md) Step 3.")
    lines.append("")
    lines.append(f"## Symphony Snapshot — {ymd}")
    lines.append("")
    lines.append("**Active Experts:** ")
    lines.append("**Time Window:** ")
    lines.append("**Generation Note:** ")
    lines.append("")
    lines.append("### 1. Executive Summary")
    lines.append("")
    lines.append("### 2. Key Convergences")
    lines.append("")
    lines.append("### 3. Preserved Tensions & Contradictions")
    lines.append("")
    lines.append("### 4. Emerging Operator Judgment")
    lines.append("")
    lines.append("### 5. Recommended Next Actions")
    lines.append("")
    lines.append("### 6. Cross-References")
    lines.append("")
    lines.append("### Change Log")
    lines.append("")
    lines.append(f"- Bundle generated `{ymd}` from `{RECIPE_ID}` via `compile_strategy_view.py`")
    lines.append("")

    return "\n".join(lines)


def collect_source_paths_for_bundle(
    notebook_dir: Path,
    bundle_date: date,
    expert_filter: frozenset[str] | None,
) -> list[str]:
    """Paths read when building a bundle (mirrors :func:`build_bundle` file reads)."""
    ymd = bundle_date.isoformat()
    ym = ymd[:7]
    raw: list[Path] = []
    inbox = notebook_dir / "daily-strategy-inbox.md"
    if inbox.is_file():
        raw.append(inbox)
    days_path = notebook_dir / "chapters" / ym / "days.md"
    meta_path = notebook_dir / "chapters" / ym / "meta.md"
    if days_path.is_file():
        raw.append(days_path)
    if meta_path.is_file():
        raw.append(meta_path)
    thread_paths = collect_strategy_thread_paths(notebook_dir)
    filtered: list[Path] = []
    for p in sorted(thread_paths, key=lambda x: str(x)):
        eid = expert_id_from_thread_path(p, notebook_dir)
        if eid is None:
            continue
        if expert_filter is not None and eid.lower() not in expert_filter:
            continue
        filtered.append(p)
    raw.extend(filtered)
    return sorted(
        {rel_posix(REPO_ROOT, p.resolve()) for p in raw},
        key=lambda s: s.lower(),
    )


def default_out_path(notebook_dir: Path, bundle_date: date) -> Path:
    return (
        notebook_dir
        / "compiled-views"
        / f"expert-polyphony-synthesis-{bundle_date.isoformat()}.md"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bundle notebook sources for compiled views.")
    parser.add_argument(
        "--notebook-dir",
        type=Path,
        default=REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook",
        help="Strategy notebook root",
    )
    parser.add_argument(
        "--date",
        type=str,
        default="",
        help="YYYY-MM-DD for output name and chapter folder (default: today local)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output markdown path (default: compiled-views/expert-polyphony-synthesis-DATE.md)",
    )
    parser.add_argument(
        "--experts",
        type=str,
        default="",
        help="Comma-separated expert/voice ids to include (default: all discovered threads)",
    )
    parser.add_argument("--inbox-tail-lines", type=int, default=40)
    parser.add_argument("--max-journal-chars", type=int, default=8000)
    parser.add_argument("--max-machine-chars", type=int, default=12000)
    parser.add_argument(
        "--no-receipt",
        action="store_true",
        help="Do not append a line to strategy notebook receipts JSONL",
    )
    args = parser.parse_args()

    notebook_dir = args.notebook_dir.resolve()
    if not notebook_dir.is_dir():
        raise SystemExit(f"notebook-dir not found: {notebook_dir}")

    if args.date:
        bundle_date = date.fromisoformat(args.date)
    else:
        bundle_date = date.today()

    expert_filter: frozenset[str] | None = None
    if args.experts.strip():
        expert_filter = frozenset(x.strip().lower() for x in args.experts.split(",") if x.strip())

    out_path = args.out.resolve() if args.out else default_out_path(notebook_dir, bundle_date)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    md = build_bundle(
        notebook_dir,
        bundle_date,
        expert_filter,
        inbox_tail_lines=args.inbox_tail_lines,
        max_journal_chars=args.max_journal_chars,
        max_machine_chars=args.max_machine_chars,
    )
    out_path.write_text(md, encoding="utf-8")
    print(out_path)

    if not args.no_receipt:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        sources = collect_source_paths_for_bundle(
            notebook_dir, bundle_date, expert_filter
        )
        out_rel = rel_posix(REPO_ROOT, out_path)
        rec = NotebookReceipt(
            ts=ts,
            entrypoint="compile_strategy_view",
            page_operation=PageOperation.NOOP.value,
            status="ok",
            sources_read=sources,
            outputs_touched=[out_rel],
            decision="wrote compiled-view source bundle (read-only on threads)",
            details={"recipe_id": RECIPE_ID, "bundle_date": bundle_date.isoformat()},
        )
        log = append_receipt(REPO_ROOT, rec)
        print(f"receipt: {log.relative_to(REPO_ROOT)}", flush=True)


if __name__ == "__main__":
    main()
