"""
Shared heuristics for SELF-KNOWLEDGE (IX-A) vs SELF-LIBRARY / CIV-MEM.

Used by validate_identity_library_boundary, validate-integrity, recursion_gate_review
hints, and process_approved_candidates merge-preview blocking.

See docs/boundary-self-knowledge-self-library.md
"""

from __future__ import annotations

import re

TOPIC_MAX = 380
CORPUS_HINT = re.compile(
    r"\b(encyclopedia|corpus|codex|CIV-MEM|CMC|ENCYCLOPEDIA\.md|"
    r"civilization.memory|full.text.of|see\s+docs/civilization-memory)\b",
    re.I,
)
# CIV-MEM / library paths must not appear in IX-A topics (belongs in self-library.md).
PATH_LEAK = re.compile(
    r"docs/civilization-memory[/\"'\s]|artifacts/civ-mem|lib-stubs\.yaml|/civ-mem-encyclopedia|"
    r"\bcivilization-memory[/\"'\s#?]|github\.com/[^/\s]+/[^/\s]+/blob/[^\s]*civilization-memory",
    re.I,
)

CIV_HISTORY_VOCAB = re.compile(
    r"\b(rome|roman|romans|egypt|egyptian|dynasty|empire|empires|civilization|"
    r"civilizations|pharaoh|pharaohs|mesopotamia|byzantine|ottoman|encyclopedia|corpus|codex)\b",
    re.I,
)


def extract_ix_a_block(self_md: str) -> str:
    i = (self_md or "").find("### IX-A")
    if i < 0:
        return ""
    j = self_md.find("### IX-B", i)
    return self_md[i : j if j > 0 else i + 15000]


def collect_ix_a_topic_violations_from_block(ix_a_block: str, *, rel_path: str = "self.md") -> list[str]:
    """Scan IX-A YAML topic lines for corpus/path/length violations."""
    out: list[str] = []
    for m in re.finditer(
        r"topic:\s*[\"']([^\"']{1,8000})[\"']|topic:\s*([^\n]+)",
        ix_a_block,
    ):
        topic = (m.group(1) or m.group(2) or "").strip().strip('"').strip("'")
        long_ = len(topic) > TOPIC_MAX
        corpus = bool(CORPUS_HINT.search(topic))
        path_leak = bool(PATH_LEAK.search(topic))
        if not long_ and not corpus and not path_leak:
            continue
        bits: list[str] = []
        if long_:
            bits.append(f"length {len(topic)}>{TOPIC_MAX}")
        if corpus:
            bits.append("corpus/library keyword")
        if path_leak:
            bits.append("CIV-MEM/library path in identity topic")
        snippet = (topic[:120] + "…") if len(topic) > 120 else topic
        out.append(
            f"{rel_path} IX-A ({', '.join(bits)}): SELF-LIBRARY/CIV-MEM not "
            f"SELF-KNOWLEDGE — {snippet}"
        )
    return out


def collect_ix_a_violations_from_self_md(self_md: str, *, rel_path: str = "self.md") -> list[str]:
    """Run IX-A topic rules on a full self.md body (e.g. merge preview)."""
    return collect_ix_a_topic_violations_from_block(extract_ix_a_block(self_md), rel_path=rel_path)


def gate_suggested_reference_surface(
    text: str,
    *,
    long_ref_threshold: int = 140,
) -> tuple[str | None, list[str]]:
    """
    Heuristic: should this gate candidate text live on SELF-LIBRARY / CIV-MEM instead of IX-A?

    Returns (suggested_surface, reasons). suggested_surface None => default SELF-KNOWLEDGE routing OK.
    """
    text = text or ""
    reasons: list[str] = []
    lib_id = re.search(r"LIB-\d{4}", text, re.I)
    long_ref = len(text.strip()) > long_ref_threshold

    if lib_id:
        return "SELF-LIBRARY", ["mentions LIB- entry"]
    if PATH_LEAK.search(text):
        return "CIV-MEM / SELF-LIBRARY", ["CIV-MEM/library path pattern (boundary rules)"]
    if CORPUS_HINT.search(text) and long_ref:
        return "CIV-MEM / SELF-LIBRARY", ["corpus/library keyword + length (boundary rules)"]
    if CIV_HISTORY_VOCAB.search(text) and long_ref:
        return "CIV-MEM / SELF-LIBRARY", ["civilization/history-domain vocabulary + length"]

    return None, reasons
