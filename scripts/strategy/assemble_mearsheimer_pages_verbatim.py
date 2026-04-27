#!/usr/bin/env python3
"""Rewrite mearsheimer-page-*.md: ~80% expert verbatim (Verbatim section) + ~20% WORK (Reflection/Foresight).

Reads mearsheimer-pages-manifest.yaml; pulls capture body from each raw-input file (YAML frontmatter
stripped); embeds full body under ### Verbatim.

Inserts a preamble **`**Words:**`** line (full-file count). There is **no** notebook word ceiling.

Run from repo root:
  python3 scripts/strategy/assemble_mearsheimer_pages_verbatim.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
MEARSHEIMER = NOTEBOOK / "experts" / "mearsheimer"
MANIFEST_PATH = MEARSHEIMER / "mearsheimer-pages-manifest.yaml"
# Pruning hint threshold for generated Mearsheimer pages (finalize_page / soft-cap notes).
SOFT_CAP_WORDS = 8000


def _word_count(s: str) -> int:
    return len(re.findall(r"\S+", s))


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    if yaml is None:
        return {}, parts[2].lstrip("\n")
    data = yaml.safe_load(parts[1])
    fm = data if isinstance(data, dict) else {}
    return fm, parts[2].lstrip("\n")


def _lanes(body: str) -> list[str]:
    b = body.lower()
    out: list[str] = []
    if "iran" in b or "hormuz" in b or "irgc" in b:
        out.append("Iran / Gulf / Hormuz seam")
    if "russia" in b or "putin" in b or "ukrain" in b or "nato" in b:
        out.append("Russia–U.S. / Ukraine / NATO")
    if "venezuel" in b or "maduro" in b or "greenland" in b:
        out.append("Americas / coercion / alliance politics")
    if "israel" in b or "gaza" in b or "zion" in b or "palestin" in b:
        out.append("Israel–Palestine / legitimacy reads")
    if "china" in b or "taiwan" in b:
        out.append("China / U.S. competition")
    if "nuclear" in b or "jcpoa" in b or "enrichment" in b:
        out.append("Nuclear / proliferation framing")
    if not out:
        out.append("General realism / cross-check in woven `days.md`")
    return out


def _mode_para(mode: str) -> str:
    if mode == "B":
        return (
            "Format: interview transcript. Attribute lines to speakers; treat Mearsheimer’s spoken "
            "segments as structural-realist argument, not independent confirmation of operational facts. "
            "Pin canonical `watch?v=` in appendix when published."
        )
    if mode == "C":
        return (
            "Format: monologue / solo video. Preserve expert argument in Verbatim; corroborate "
            "load-bearing factual claims before wire-style use."
        )
    return (
        "Format: Substack-style essay. Historical and theoretical passages reflect Mearsheimer’s read; "
        "verify dates, quotes, and figures against primary or scholarly sources if promoted."
    )


def _topic_paragraphs(body: str) -> str:
    b = body.lower()
    chunks: list[str] = []
    if "bucharest" in b or "nato expansion" in b or "april 2008" in b:
        chunks.append(
            "NATO expansion / 2008 Bucharest: keep alliance-politics causality in commentator tier; "
            "separate from battlefield ORBAT if elevating to chapter judgment."
        )
    if "liberal hegemony" in b or "rules-based" in b or "monroe" in b:
        chunks.append(
            "Order / institutions language: label as Mearsheimer framework; not standalone proof of outcomes."
        )
    if "war crime" in b or "ihl" in b or "geneva" in b:
        chunks.append(
            "IHL content: notebook seam only; adjudication belongs to courts or commissions, not WORK pages."
        )
    return "\n\n".join(chunks[:3])


def _fm_note_series(fm: dict) -> tuple[str, str]:
    note = (fm.get("capture_note") or fm.get("source_note") or "").strip()
    series = (fm.get("episode_title") or fm.get("series") or "").strip()
    return note, series


def _build_judgment(fm: dict, body: str, mode: str, verbatim_w: int) -> str:
    j_target = max(55, min(950, int(verbatim_w * 0.25) - 26))
    if verbatim_w < 700:
        j_target = max(50, min(j_target, int(verbatim_w * 0.18)))
    note, series = _fm_note_series(fm)
    lanes = _lanes(body)
    lane_lines = "\n".join(f"- {x}" for x in lanes[:5])

    if verbatim_w < 650:
        lane_one = ", ".join(lanes[:3])
        bits = []
        if note:
            nw = note.split()
            if len(nw) > 35:
                note = " ".join(nw[:35]) + "…"
            bits.append(f"**Operator note:** {note}")
        bits.append(
            f"**WORK:** {series or '—'} · {_mode_para(mode)} "
            f"Lanes: {lane_one}. Commentator tier; verify before wire-use. "
            "Prompts: falsifiers, delta vs prior Mearsheimer, wire boundary for `days.md`."
        )
        return "\n\n".join(bits)

    parts: list[str] = []
    if note:
        parts.append(f"**Operator note:** {note}")
    parts.append(
        "**WORK read.** Verbatim is expert verbatim from capture; this block is notebook analysis only—"
        "tier discipline and seams, not a substitute for wire."
    )
    parts.append(f"**Capture:** {series or '(see title)'} · {_mode_para(mode)}")
    parts.append(f"**Lanes:**\n{lane_lines}")
    tp = _topic_paragraphs(body)
    if tp:
        parts.append("**Hooks:**\n\n" + tp)
    parts.append(
        "**Tier.** Commentator default; promote claims with inbox `verify:` or independent sources. "
        "Cite this page + `raw-input` when pasting into `days.md`."
    )
    parts.append(
        "**Prompts:** Falsifiable claim this week? Delta vs prior Mearsheimer on same lane? "
        "Wire boundary before chapter synthesis?"
    )

    text = "\n\n".join(parts)
    if _word_count(text) > j_target + 50 and note:
        words = note.split()
        if len(words) > 40:
            short_note = " ".join(words[:40]) + "…"
            parts[0] = f"**Operator note:** {short_note}"
            text = "\n\n".join(parts)
    return text


def _build_open(mode: str) -> str:
    return "\n".join(
        [
            "- **Falsifiers:** Wire/primary items that would change the thesis.",
            "- **Resume:** Next capture, `days.md` seam, chapter meta.",
            f"- **Tier:** Verbatim = expert ({mode}); Reflection/Foresight = WORK.",
        ]
    )


def render_page(entry: dict, fm: dict, body: str) -> str:
    vd = entry["voice_date"]
    display_title = (entry.get("display_title") or "").strip()
    title_suffix = f" (*{display_title}*)" if display_title else ""
    prem = entry["preamble_label"]
    pdate = entry["preamble_date"]
    cap = entry["capture_mode"]
    mode = entry.get("mode") or "A"
    raw_rel = entry["raw_input_relative"]
    href = entry["href_verbatim"]
    src_url = entry.get("source_url") or "Not yet pinned"

    verbatim_w = _word_count(body)
    judgment = _build_judgment(fm, body, mode, verbatim_w)
    open_sec = _build_open(mode)

    lines = [
        f"# Mearsheimer strategy page — {vd}{title_suffix}",
        "",
        "WORK only; not Record.",
        "",
        f"**Expert:** `mearsheimer` · **{prem}:** {pdate} · **Capture:** {cap} · **Artifact:** "
        "strategy-page file (`mearsheimer-page-…` under `experts/mearsheimer/`). Optional: echo in "
        "`thread.md` fence for watches / cross-expert duplication.",
        "",
        "---",
        "",
        "### Verbatim",
        "",
        "Expert capture (verbatim body from linked `raw-input`; operator-ingested).",
        "",
        body.rstrip() + "\n",
        "",
        "### Reflection",
        "",
        judgment.strip() + "\n",
        "",
        "### Foresight",
        "",
        open_sec + "\n",
        "",
        "---",
        "",
        "### Appendix",
        "",
        f"- **Full verbatim (capture):** [{raw_rel}]({href})",
        "- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:mearsheimer`, "
        + vd
        + ")",
        "- **`thread:mearsheimer`** · **verify:** primary capture on disk + voice date + inbox row (YT | / SS | as applicable)",
        f"- **Canonical primary:** {src_url}",
        "",
    ]
    return "\n".join(lines)


def _soft_cap_paragraph(total_w_before: int) -> str:
    return (
        f"\n**Soft cap — pruning.** This file is about **{total_w_before}** words before this note; "
        f"the notebook **soft cap is {SOFT_CAP_WORDS}**. Linked `raw-input` remains the SSOT for the "
        "full capture. To bring this page under cap, consider: **remove** paragraphs that restate the "
        "same beat; **consolidate** overlapping arguments into one passage; **trim** side trails you "
        "will not weave into `days.md`; **avoid** duplicating long quotations already in `raw-input`; "
        "**relocate** extended material to a `thread.md` "
        "`<!-- strategy-page:start … -->` fence or a sibling note. Keep one sharp through-line for "
        "cross-expert work.\n"
    )


def _inject_soft_cap_judgment(page: str, total_w: int) -> str:
    if total_w <= SOFT_CAP_WORDS:
        return page
    sep = "\n### Foresight\n"
    if sep not in page:
        return page
    head, tail = page.split(sep, 1)
    return head + _soft_cap_paragraph(total_w) + sep + tail


def _inject_header_word_count(page: str, total_w: int) -> str:
    marker = "\n\n---\n\n### Verbatim\n"
    if marker not in page:
        return page
    extra = ""
    if total_w > SOFT_CAP_WORDS:
        extra = "; **over cap** — see **Soft cap — pruning** in Reflection"
    replacement = (
        f"\n\n**Words:** {total_w} (soft cap {SOFT_CAP_WORDS}{extra})\n\n"
        "---\n\n### Verbatim\n"
    )
    return page.replace(marker, replacement, 1)


def finalize_page(page: str) -> str:
    w0 = _word_count(page)
    page = _inject_soft_cap_judgment(page, w0)
    w1 = _word_count(page)
    return _inject_header_word_count(page, w1)


def main() -> int:
    if yaml is None:
        print("assemble_mearsheimer_pages_verbatim: need PyYAML", file=sys.stderr)
        return 1
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    pages = manifest.get("pages") or []
    for entry in pages:
        if entry.get("skip_assembly"):
            print(
                f"skip_assembly: {entry.get('page_filename', entry.get('raw_input_relative', '?'))}"
            )
            continue
        raw_rel = entry["raw_input_relative"]
        page_fn = entry["page_filename"]
        raw_path = NOTEBOOK / raw_rel
        if not raw_path.is_file():
            print(f"missing raw-input: {raw_rel}", file=sys.stderr)
            return 1
        text = raw_path.read_text(encoding="utf-8")
        fm, body = _split_frontmatter(text)
        if not body.strip():
            print(f"empty body: {raw_rel}", file=sys.stderr)
            return 1
        out = MEARSHEIMER / page_fn
        final = finalize_page(render_page(entry, fm, body))
        out.write_text(final, encoding="utf-8")
        vw = _word_count(body)
        tw = _word_count(final)
        print(f"Wrote {out.relative_to(REPO_ROOT)} ({vw} verbatim words, {tw} on-page words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
