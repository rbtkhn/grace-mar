"""
Lightweight retriever over SELF, SKILLS, EVIDENCE.

Used for grounded answering: fetch relevant chunks so responses can cite source IDs.
Keyword + section heuristics — no embeddings.
"""

import re
from pathlib import Path

PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / "pilot-001"
SELF_PATH = PROFILE_DIR / "SELF.md"
SKILLS_PATH = PROFILE_DIR / "SKILLS.md"
EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_chunks(content: str, source: str) -> list[tuple[str, str]]:
    """Extract (id, text) chunks. Id pattern: LEARN-0001, CUR-0001, PER-0001, ACT-0001, WRITE-0001, READ-0001, CREATE-0001."""
    chunks: list[tuple[str, str]] = []
    id_pattern = re.compile(
        r"id:\s+(LEARN-\d+|CUR-\d+|PER-\d+|ACT-\d+|READ-\d+|WRITE-\d+|CREATE-\d+)",
        re.IGNORECASE,
    )
    for m in id_pattern.finditer(content):
        chunk_id = m.group(1)
        start = m.start()
        end = min(start + 800, len(content))
        block = content[start:end]
        text = block.replace("\n", " ")[:500].strip()
        if text:
            chunks.append((chunk_id, f"[{chunk_id}] {text}"))
    return chunks


def load_record_chunks() -> list[tuple[str, str]]:
    """Load all chunks from SELF, SKILLS, EVIDENCE."""
    chunks: list[tuple[str, str]] = []
    if SELF_PATH.exists():
        chunks.extend(_extract_chunks(_read(SELF_PATH), "SELF"))
    if SKILLS_PATH.exists():
        chunks.extend(_extract_chunks(_read(SKILLS_PATH), "SKILLS"))
    if EVIDENCE_PATH.exists():
        chunks.extend(_extract_chunks(_read(EVIDENCE_PATH), "EVIDENCE"))
    return chunks


def retrieve(query: str, top_k: int = 5) -> list[tuple[str, str]]:
    """
    Return top_k chunks most relevant to query. Simple keyword overlap scoring.
    Returns list of (chunk_id, text).
    """
    chunks = load_record_chunks()
    if not chunks:
        return []
    query_words = set(re.findall(r"\b\w{2,}\b", query.lower()))
    scored: list[tuple[float, tuple[str, str]]] = []
    for chunk_id, text in chunks:
        text_lower = text.lower()
        text_words = set(re.findall(r"\b\w{2,}\b", text_lower))
        overlap = len(query_words & text_words)
        if overlap > 0:
            scored.append((overlap, (chunk_id, text)))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:top_k]]
