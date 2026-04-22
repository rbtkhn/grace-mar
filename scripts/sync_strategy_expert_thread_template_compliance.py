#!/usr/bin/env python3
"""Normalize ``strategy-expert-*-thread.md`` to the journal-layer contract in
``strategy-expert-template.md`` (thread section).

Preserves each file's existing **Source:** line (template default if missing).
Replaces **Process** / **Updated** / **Companion** and the full block from
``## Journal layer — Narrative (operator)`` through just before the first
``## YYYY-MM`` or ``<!-- backfill:`` line.

Keeps all calendar-month narrative and the machine layer (between HTML markers)
unchanged.

Run from repo root::

    python3 scripts/sync_strategy_expert_thread_template_compliance.py --apply

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
NOTEBOOK = REPO / "docs/skill-work/work-strategy/strategy-notebook"

from strategy_expert_corpus import (  # noqa: E402
    RE_FLAT_MONTH_THREAD,
    RE_IN_FOLDER_MONTH_THREAD,
    collect_strategy_thread_paths,
)
MARKER_START = "<!-- strategy-expert-thread:start -->"
# Split only on marker as its own line — never match the substring inside **Process:** prose.
MARKER_BLOCK_START = "\n" + MARKER_START + "\n"

RE_SOURCE = re.compile(r"^\*\*Source:\*\*.*$", re.M)
RE_MONTH_H2 = re.compile(r"^## \d{4}-\d{2}\s*$")


def canonical_process_updated() -> str:
    # Do not embed `<!-- … -->` in this line — it can be mistaken for the real marker by naive splits.
    return (
        "**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, "
        "then fills **only** the **machine layer** between the **strategy-expert-thread** HTML "
        "start and end comments. Operator / assistant maintains the **journal layer** above the "
        "start marker in **readable prose** (optional **ledger** after the end marker).\n"
        "**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**."
    )


def canonical_journal_intro(expert_id: str, *, month_ym: str | None = None) -> str:
    lines: list[str] = [
        "## Journal layer — Narrative (operator)",
        "",
        "_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). "
        "Cover: what this voice did this week, how it **intersects** named **knots**, "
        "convergence/tension with other **`thread:`** experts, and **Open** pins. "
        "The **journal layer** is **not** overwritten by the **`thread`** script._",
        "",
    ]
    if month_ym:
        lines += [
            "**Layout:** This file is **one calendar month** "
            f"(`{month_ym}`): `experts/{expert_id}/{expert_id}-thread-{month_ym}.md` "
            "(or flat `strategy-expert-"
            f"{expert_id}-thread-{month_ym}.md`). Optional **`## {month_ym}`** matches the "
            "filename for grep / validators. The **machine layer** (script-maintained) is **only** "
            "the fenced block between the **strategy-expert-thread** HTML start and end comments.",
            "",
        ]
    else:
        lines += [
            "**Layout:** Stay on **one** `strategy-expert-"
            f"{expert_id}-thread.md` file (or legacy `experts/{expert_id}/thread.md`). "
            "Within the **journal layer**, each **`## YYYY-MM`** "
            "heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), "
            "**Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), "
            "**Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) "
            "is **only** the fenced block between the **strategy-expert-thread** HTML start and end "
            'comments — do not call that "Segment 2" in the month sense.',
            "",
        ]
    if expert_id == "pape":
        lines += [
            "**Expert note (pape):** **`## 2026-04`** may also hold a partial-month ledger + "
            "optional **`### Distilled thread`** subsection.",
            "",
        ]
    elif expert_id == "jiang":
        lines += [
            "**Expert note (PH / work-jiang):** **Predictive History** notebook-facing ingest routes "
            "here only — see [strategy-commentator-threads](strategy-commentator-threads.md) special "
            "routing rule; corpus lives under `research/external/work-jiang/` (operator scope).",
            "",
        ]
    lines += [
        "_(No narrative distillation yet — add prose above the markers, not inside them.)_",
        "",
        "**Optional journal-layer extensions (still above the thread start HTML comment):**",
        "",
        "- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the "
        "readable journal (one segment per file when using **monthly thread files**). "
        "**Default:** **at least ~500 words** of "
        "**prose** per month-segment (words on non-bullet substantive lines; see "
        "`validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not "
        "enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are "
        "**compressed ledger** material — fine for lattice discipline — but they **do not** count "
        "toward the prose minimum and are **not** an equally canonical substitute for the "
        "prose-first journal unless the operator opts into ledger-only months (see HTML comment "
        "below). To scaffold prose to the minimum from roster metadata, run "
        "`python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.",
        "",
        "- **Historical expert context (optional rebuild)** — "
        f"`python3 scripts/strategy_historical_expert_context.py --expert-id {expert_id} "
        "--start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under "
        "`artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** "
        f"(`{expert_id}-<start>-to-<end>.md`) plus **per-month** files (`{expert_id}/<YYYY-MM>.md`). "
        "[`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_"
        "with_history.py) loads **per-month** artifacts when every month in the requested window "
        "exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that "
        "folder.",
        "",
        "- **`<!-- backfill:"
        f"{expert_id}:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo "
        "URLs; not contemporaneous journal prose; keep scope/rules inside the block.",
        "",
        "- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns "
        "when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional "
        "`--month MM` to audit one month only). For a **whole file** where month bullets-only is "
        "intentional (transitional ledger), add once in the human layer: "
        "`<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: "
        "`.cursor/rules/strategy-expert-thread-journal-layer.mdc`.",
        "",
    ]
    return "\n".join(lines)


def extract_source_line(preamble: str) -> str | None:
    m = RE_SOURCE.search(preamble)
    return m.group(0).strip() if m else None


def default_source_line(expert_id: str) -> str:
    return (
        f"**Source:** Human **narrative journal** (below) + [`strategy-expert-{expert_id}"
        f"-transcript.md`](strategy-expert-{expert_id}-transcript.md) (verbatim ingests) + "
        "relevant **knot** files (where this expert's material was used)."
    )


def companion_line(expert_id: str) -> str:
    return (
        f"**Companion files:** [`strategy-expert-{expert_id}.md`](strategy-expert-{expert_id}.md) "
        f"(profile) and [`strategy-expert-{expert_id}-transcript.md`]"
        f"(strategy-expert-{expert_id}-transcript.md) (7-day verbatim)."
    )


def split_file(text: str) -> tuple[str, str, str] | None:
    idx = text.find(MARKER_BLOCK_START)
    if idx == -1:
        return None
    head = text[:idx]
    machine_suffix = text[idx + 1 :]  # drop leading newline; starts with <!-- …
    lines = head.splitlines()
    journal_idx = None
    for i, line in enumerate(lines):
        if line.startswith("## Journal layer") or line.startswith("## Segment 1"):
            journal_idx = i
            break
    if journal_idx is None:
        return None
    preamble = "\n".join(lines[:journal_idx]).rstrip() + "\n"
    month_idx = None
    for i in range(journal_idx + 1, len(lines)):
        line = lines[i]
        if RE_MONTH_H2.match(line) or line.startswith("<!-- backfill:"):
            month_idx = i
            break
    if month_idx is None:
        month_onward = ""
    else:
        month_onward = "\n".join(lines[month_idx:])
    return preamble, month_onward, machine_suffix


def rebuild_preamble(old_preamble: str, expert_id: str) -> str:
    lines = old_preamble.strip().splitlines()
    h1 = lines[0] if lines else f"# Expert thread — `{expert_id}`"
    if not h1.startswith("# Expert thread"):
        h1 = f"# Expert thread — `{expert_id}`"
    src = extract_source_line(old_preamble) or default_source_line(expert_id)
    parts = [
        h1,
        "",
        "WORK only; not Record.",
        "",
        src,
        canonical_process_updated(),
        companion_line(expert_id),
        "",
        "---",
        "",
    ]
    return "\n".join(parts)


def process_file(path: Path, apply: bool) -> bool:
    month_ym: str | None = None
    if path.name == "thread.md" and path.parent.parent.name in ("experts", "voices"):
        expert_id = path.parent.name
    else:
        m = re.match(r"^strategy-expert-(.+)-thread\.md$", path.name)
        if m:
            expert_id = m.group(1)
        else:
            m2 = RE_IN_FOLDER_MONTH_THREAD.match(path.name)
            if m2 and m2.group(1) == path.parent.name:
                expert_id = m2.group(1)
                month_ym = m2.group(2)
            else:
                m3 = RE_FLAT_MONTH_THREAD.match(path.name)
                if not m3:
                    return False
                expert_id = m3.group(1)
                month_ym = m3.group(2)
    text = path.read_text(encoding="utf-8")
    parts = split_file(text)
    if parts is None:
        print(f"skip (no {MARKER_START}): {path.name}", file=sys.stderr)
        return False
    preamble_old, month_onward, machine_suffix = parts
    preamble_new = rebuild_preamble(preamble_old, expert_id)
    intro = canonical_journal_intro(expert_id, month_ym=month_ym)
    new_text = preamble_new + intro
    if month_onward.strip():
        new_text += month_onward.rstrip() + "\n"
    new_text += machine_suffix
    if new_text == text:
        return False
    if apply:
        path.write_text(new_text, encoding="utf-8")
    print(f"{'wrote' if apply else 'would update'}: {path.name}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Write files (default is dry-run: print only)",
    )
    args = ap.parse_args()
    updated = 0
    paths = collect_strategy_thread_paths(NOTEBOOK)
    for path in paths:
        if process_file(path, args.apply):
            updated += 1
    print(f"summary: {updated} file(s) " + ("updated" if args.apply else "would change"), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
