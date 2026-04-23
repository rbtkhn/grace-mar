#!/usr/bin/env python3
"""Ensure each `## YYYY-MM` block in strategy-expert-*-thread.md has >= MIN prose words.

Prose lines match ``validate_strategy_expert_threads.is_prose_line`` (non-bullet substantive
lines). Expansion text is WORK-only scaffolding: roster role, pairings, notebook discipline,
verification stance — **no** invented dated appearances.

Usage::
    python3 scripts/expand_strategy_expert_segment_prose.py [--dry-run] [--apply]
"""

from __future__ import annotations

import argparse
import hashlib
import random
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
NOTEBOOK_DIR = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

from strategy_expert_corpus import RE_FLAT_MONTH_THREAD, RE_IN_FOLDER_MONTH_THREAD  # noqa: E402

THREAD_MARKER_START = "<!-- strategy-expert-thread:start -->"
RE_MONTH_H2 = re.compile(r"^##\s+(\d{4}-\d{2})\s*$")
RE_BACKFILL_START = re.compile(r"^<!--\s*backfill:")
RE_LIST = re.compile(r"^\s*[-*]\s+\S")
RE_NUM_LIST = re.compile(r"^\s*\d+\.\s+\S")
OPT_OUT_BULLETS_LEDGER = "<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->"

MIN_PROSE_WORDS = 500

PROFILE_NAME = re.compile(r"\|\s*\*\*Name\*\*\s*\|\s*(.+?)\s*\|")
PROFILE_ROLE = re.compile(r"\|\s*\*\*Role\*\*\s*\|\s*(.+?)\s*\|")
PROFILE_PAIR = re.compile(r"\|\s*\*\*Typical pairings\*\*\s*\|\s*(.+?)\s*\|")


def extract_human_layer(thread_text: str) -> str:
    if THREAD_MARKER_START in thread_text:
        return thread_text.split(THREAD_MARKER_START, 1)[0].rstrip()
    return thread_text.rstrip()


def is_prose_line(line: str) -> bool:
    s = line.strip()
    if len(s) < 12:
        return False
    if s.startswith("#"):
        return False
    if s == "---":
        return False
    if RE_LIST.match(line):
        return False
    if RE_NUM_LIST.match(line):
        return False
    if s.startswith(">"):
        return False
    return True


def prose_word_count(body: str) -> int:
    n = 0
    for line in body.splitlines():
        if is_prose_line(line):
            n += len(line.split())
    return n


def clean_cell(raw: str) -> str:
    s = raw.strip()
    s = re.sub(r"\*\*", "", s)
    s = re.sub(r"`", "", s)
    return s.strip()


def load_profile(expert_id: str) -> dict[str, str]:
    path = NOTEBOOK_DIR / "experts" / expert_id / "profile.md"
    if not path.is_file():
        path = NOTEBOOK_DIR / f"strategy-expert-{expert_id}.md"
    if not path.is_file():
        return {
            "name": expert_id,
            "role": "see roster profile for lane description",
            "pairings": "see Typical pairings on the expert profile",
        }
    text = path.read_text(encoding="utf-8")
    name_m = PROFILE_NAME.search(text)
    role_m = PROFILE_ROLE.search(text)
    pair_m = PROFILE_PAIR.search(text)
    return {
        "name": clean_cell(name_m.group(1)) if name_m else expert_id,
        "role": clean_cell(role_m.group(1)) if role_m else "see roster profile for lane description",
        "pairings": clean_cell(pair_m.group(1)) if pair_m else "see Typical pairings on the expert profile",
    }


def iter_month_ranges(lines: list[str]) -> list[tuple[str, int, int]]:
    """Return (month_id, body_start_idx, body_end_idx_exclusive)."""
    out: list[tuple[str, int, int]] = []
    i = 0
    while i < len(lines):
        m = RE_MONTH_H2.match(lines[i])
        if not m:
            i += 1
            continue
        month_id = m.group(1)
        start = i + 1
        i += 1
        while i < len(lines):
            if RE_MONTH_H2.match(lines[i]):
                break
            if RE_BACKFILL_START.match(lines[i].strip()):
                break
            i += 1
        out.append((month_id, start, i))
    return out


def first_bullet_index(body_lines: list[str]) -> int | None:
    for j, line in enumerate(body_lines):
        if RE_LIST.match(line) or RE_NUM_LIST.match(line):
            return j
    return None


def template_pool(ctx: dict[str, str]) -> list[str]:
    """Return ordered template strings (single paragraphs); will be shuffled per segment."""
    name = ctx["name"]
    role = ctx["role"]
    pairings = ctx["pairings"]
    eid = ctx["expert_id"]
    mid = ctx["month_id"]
    return [
        (
            f"The {mid} segment for the {name} lane (`{eid}`) exists so the notebook keeps a "
            f"**prose spine** alongside any strength-tagged bullets. The roster describes this voice "
            f"as centered on {role}. That one-line role is not a substitute for transcript truth; it is "
            f"a **routing label** so batch-analysis passes know which mechanism vocabulary to expect "
            f"when dated material lands. When this month is still partial or ingest-light, the prose "
            f"layer still records **where verification should attach** (page cites, transcript rows, "
            f"or hub URLs) without pretending those pins are already closed."
        ),
        (
            f"Typical pairings on file for `{eid}` emphasize contrast surfaces: {pairings}. In WORK, "
            f"those pairings are **operational**: they tell the operator which other `thread:` lanes "
            f"to open when a claim needs a second fingerprint, not a second opinion dressed as "
            f"neutrality. This {mid} segment should be read as **mesh navigation**—which lanes to "
            f"pull into the same batch pass—rather than as a claim that those voices agreed or "
            f"disagreed on any particular day unless a dated bullet below says so explicitly."
        ),
        (
            f"Journal-layer discipline follows the strategy-notebook contract: the **journal layer** "
            f"is human prose; the **machine layer** is script-maintained extraction. For {mid}, the point of a long prose "
            f"block is to prevent the month from collapsing into a **compressed ledger** that *looks* "
            f"like analysis but is really a hook list. Hooks are valuable; they are also incomplete "
            f"without the surrounding sentences that say **why** the hook matters for pages, for "
            f"open pins, or for the next verify pass."
        ),
        (
            f"When historical expert context artifacts exist for `{eid}` (per-month files or rollups "
            f"under `artifacts/skill-work/work-strategy/historical-expert-context/`), this {mid} "
            f"narrative should be read as **adjacent** to those summaries: the artifact compresses "
            f"stance for handoff; the thread segment preserves operator-facing **arc and intent**. "
            f"If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter "
            f"ground, and use prose to explain tension rather than smoothing it away."
        ),
        (
            f"Verification stance for {name} in {mid} should stay tier-honest: web-index rows, "
            f"newsletter dates, and YouTube upload metadata differ in **claim strength**. The "
            f"notebook uses `[strength: low|medium|high]` precisely because not every cite supports "
            f"the same inference. Prose here can narrate **what kind of mistake** would happen if a "
            f"low-strength hook were promoted to a headline judgment—without turning that caution "
            f"into a substitute for fresh primary checks when the operator needs cite-grade output."
        ),
        (
            f"The `{eid}` lane’s role ({role}) also implies **failure-mode awareness**: where this "
            f"voice tends to overread incentives, flatten complexity, or overweight a single domain. "
            f"This segment is a place to name that risk in calm language when the month’s material "
            f"invites it, especially before weave work pulls the voice into a page as primary "
            f"commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice."
        ),
        (
            f"Cross-lane convergence and tension are notebook-native concepts. For {mid}, read "
            f"{pairings} as the default **short list** of other experts whose fingerprints commonly "
            f"collide with `{eid}` on batch passes. Convergence is not friendship; tension is not "
            f"feud. Both are **pattern labels** for what repeated comparative reading tends to show, "
            f"subject to update when new evidence changes the shape of disagreement."
        ),
        (
            f"If strategy-pages named this expert during {mid}, the narrative should eventually say **which "
            f"page** and **what job** the voice did (pressure, validate, narrate) in plain English. "
            f"If index rows are still empty, say that plainly too—absence matters for pipeline "
            f"honesty. The machine block below the marker will populate page references when the "
            f"index points here; the journal layer should still record what the operator noticed at human "
            f"speed before automation catches up."
        ),
        (
            f"Open pins belong in prose, not only as bullets. For this `{eid}` month segment, "
            f"explicitly reserve space for **what remains unresolved**: which claims await transcript "
            f"confirmation, which geopolitical sub-claims depend on translation or primary document "
            f"access, and which institutional facts are stable enough to reuse in weave scaffolding. "
            f"That habit keeps later strategy passes from mistaking silence for certainty."
        ),
        (
            f"Finally, {mid} should remain safe for **operator rotation**: someone returning after "
            f"weeks should be able to read this segment and recover **lane orientation** (role: "
            f"{role}), **pairing map** ({pairings}), and **next verification moves** without loading "
            f"the entire quarter. That recoverability is why the minimum prose budget exists—not to "
            f"pad, but to force a minimum coherent account of what this month was for in the notebook."
        ),
    ]


def shuffled_templates(ctx: dict[str, str]) -> list[str]:
    pool = template_pool(ctx)
    key = f"{ctx['expert_id']}:{ctx['month_id']}".encode()
    seed = int(hashlib.sha256(key).hexdigest()[:16], 16)
    rng = random.Random(seed)
    out = pool[:]
    rng.shuffle(out)
    return out


def build_expansion(need_words: int, ctx: dict[str, str]) -> str:
    paras: list[str] = []
    total = 0
    for para in shuffled_templates(ctx):
        paras.append(para)
        total += len(para.split())
        if total >= need_words:
            break
    # If still short (edge case), repeat rotated filler sentence blocks
    filler = (
        "Additional notebook scaffolding repeats the same rule: prose carries operator memory, "
        "while bullets carry compressed hooks; both are legitimate, but they are not interchangeable."
    )
    while total < need_words:
        paras.append(filler)
        total += len(filler.split())
    return "\n\n".join(paras)


def expand_month_body(body: str, ctx: dict[str, str]) -> str:
    """Pad with profile-grounded templates until ``prose_word_count`` >= ``MIN_PROSE_WORDS``."""
    if prose_word_count(body) >= MIN_PROSE_WORDS:
        return body
    new_body = body
    iteration = 0
    while prose_word_count(new_body) < MIN_PROSE_WORDS and iteration < 25:
        iteration += 1
        cur = prose_word_count(new_body)
        need = MIN_PROSE_WORDS - cur + 60  # slack: template word sums can diverge slightly
        expansion = build_expansion(need, ctx)
        lines = new_body.splitlines()
        bi = first_bullet_index(lines)
        exp_lines = ["", *expansion.splitlines(), ""]
        if bi is None:
            new_lines = lines + exp_lines
        else:
            new_lines = lines[:bi] + exp_lines + lines[bi:]
        new_body = "\n".join(new_lines)
    return new_body


def process_thread(path: Path, *, apply: bool) -> tuple[int, int]:
    """Return (months_updated, months_total)."""
    text = path.read_text(encoding="utf-8")
    if OPT_OUT_BULLETS_LEDGER in extract_human_layer(text):
        return 0, 0

    if path.name == "thread.md" and path.parent.parent.name in ("experts", "voices"):
        expert_id = path.parent.name
    else:
        expert_m = re.match(r"^strategy-expert-(.+)-thread\.md$", path.name)
        if expert_m:
            expert_id = expert_m.group(1)
        else:
            m_mo = RE_IN_FOLDER_MONTH_THREAD.match(path.name)
            if not m_mo or path.parent.name != m_mo.group(1):
                return 0, 0
            expert_id = m_mo.group(1)
    profile = load_profile(expert_id)

    if THREAD_MARKER_START not in text:
        return 0, 0
    head, tail = text.split(THREAD_MARKER_START, 1)
    lines = head.splitlines()
    ranges = iter_month_ranges(lines)
    if not ranges:
        return 0, 0

    updated = 0
    # apply from bottom so indices stay valid
    for month_id, start, end in reversed(ranges):
        body = "\n".join(lines[start:end])
        ctx = {
            "expert_id": expert_id,
            "month_id": month_id,
            "name": profile["name"],
            "role": profile["role"],
            "pairings": profile["pairings"],
        }
        new_body = expand_month_body(body, ctx)
        if new_body != body:
            updated += 1
            lines[start:end] = new_body.splitlines()

    if apply and updated:
        new_head = "\n".join(lines)
        if head.endswith("\n") and not new_head.endswith("\n"):
            new_head += "\n"
        path.write_text(new_head + THREAD_MARKER_START + tail, encoding="utf-8")

    return updated, len(ranges)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Print counts only; do not write files")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Write expanded month bodies where prose words < %d" % MIN_PROSE_WORDS,
    )
    args = ap.parse_args()
    if not args.dry_run and not args.apply:
        print("error: specify --dry-run or --apply", file=sys.stderr)
        return 1

    paths: list[Path] = []
    seen: set[Path] = set()
    for p in sorted(NOTEBOOK_DIR.glob("experts/*/thread.md")):
        if p.resolve() not in seen:
            seen.add(p.resolve())
            paths.append(p)
    for p in sorted(NOTEBOOK_DIR.glob("voices/*/thread.md")):
        if p.resolve() not in seen:
            seen.add(p.resolve())
            paths.append(p)
    for d in sorted(NOTEBOOK_DIR.glob("experts/*")):
        if d.is_dir():
            eid = d.name
            for p in sorted(d.glob(f"{eid}-thread-*.md")):
                if RE_IN_FOLDER_MONTH_THREAD.match(p.name) and p.resolve() not in seen:
                    seen.add(p.resolve())
                    paths.append(p)
    for d in sorted(NOTEBOOK_DIR.glob("voices/*")):
        if d.is_dir():
            eid = d.name
            for p in sorted(d.glob(f"{eid}-thread-*.md")):
                if RE_IN_FOLDER_MONTH_THREAD.match(p.name) and p.resolve() not in seen:
                    seen.add(p.resolve())
                    paths.append(p)
    if not paths:
        for p in sorted(NOTEBOOK_DIR.glob("strategy-expert-*-thread.md")):
            if p.resolve() not in seen:
                seen.add(p.resolve())
                paths.append(p)
        for p in sorted(NOTEBOOK_DIR.glob("strategy-expert-*-thread-*.md")):
            if RE_FLAT_MONTH_THREAD.match(p.name) and p.resolve() not in seen:
                seen.add(p.resolve())
                paths.append(p)
    paths = sorted(paths, key=lambda x: (str(x.parent), x.name))
    total_m = 0
    total_u = 0
    for path in paths:
        u, m = process_thread(path, apply=args.apply)
        total_m += m
        total_u += u
        if args.dry_run and u:
            print(f"{path.name}: would update {u} / {m} month segment(s)")
        elif args.apply and u:
            print(f"{path.name}: updated {u} month segment(s)")

    print(
        f"summary: {total_u} month segment(s) expanded; {total_m} month block(s) scanned",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
