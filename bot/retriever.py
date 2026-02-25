"""
Lightweight retriever over SELF, SKILLS, EVIDENCE.

Used for grounded answering: fetch relevant chunks so responses can cite source IDs.
Keyword + section heuristics — no embeddings.
"""

import os
import re
from pathlib import Path

USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / USER_ID
SELF_PATH = PROFILE_DIR / "SELF.md"
SKILLS_PATH = PROFILE_DIR / "SKILLS.md"
EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_chunks(content: str, source: str) -> list[tuple[str, str]]:
    """Extract compact chunk strings for each record id block."""
    chunks: list[tuple[str, str]] = []
    id_pattern = re.compile(
        r"id:\s+(LEARN-\d+|CUR-\d+|PER-\d+|ACT-\d+|READ-\d+|WRITE-\d+|CREATE-\d+)",
        re.IGNORECASE,
    )
    matches = list(id_pattern.finditer(content))
    if not matches:
        return chunks
    for i, m in enumerate(matches):
        chunk_id = m.group(1).upper()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else min(len(content), start + 1200)
        block = content[start:end].strip()
        compact = re.sub(r"\s+", " ", block)
        if compact:
            text = compact[:700]
            chunks.append((chunk_id, f"[{chunk_id}] ({source}) {text}"))
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


_STOPWORDS = {
    "what", "when", "where", "which", "who", "why", "how", "about", "with", "from",
    "this", "that", "your", "have", "has", "had", "into", "for", "the", "and", "are",
    "was", "were", "can", "could", "tell", "show", "me", "you",
}


def _tokenize(text: str) -> list[str]:
    return [
        t for t in re.findall(r"\b[a-zA-Z0-9]{2,}\b", (text or "").lower())
        if t not in _STOPWORDS
    ]


def _score_chunk(query: str, query_tokens: set[str], chunk_id: str, text: str) -> float:
    text_lower = text.lower()
    text_tokens = set(_tokenize(text))
    if not text_tokens:
        return 0.0
    overlap = len(query_tokens & text_tokens)
    if overlap == 0:
        return 0.0

    score = float(overlap)
    # Reward dense overlap rather than one accidental shared token.
    score += overlap / max(8.0, float(len(query_tokens)))

    # Reward exact phrase presence for short/important queries.
    q = (query or "").strip().lower()
    if len(q) >= 4 and q in text_lower:
        score += 3.0

    # Prefer canonical knowledge entries when user asks factual "what do you know" questions.
    if any(x in q for x in ("know", "learned", "knowledge")) and chunk_id.startswith("LEARN-"):
        score += 1.5
    if any(x in q for x in ("curious", "interest")) and chunk_id.startswith("CUR-"):
        score += 1.2
    if any(x in q for x in ("personality", "how am i", "what am i like")) and chunk_id.startswith("PER-"):
        score += 1.2

    # Light recency preference within same id family.
    m = re.search(r"-(\d+)$", chunk_id)
    if m:
        score += int(m.group(1)) / 10000.0
    return score


def retrieve(query: str, top_k: int = 5) -> list[tuple[str, str]]:
    """Return top_k record chunks using weighted lexical scoring."""
    chunks = load_record_chunks()
    if not chunks:
        return []
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return []
    scored: list[tuple[float, str, str]] = []
    for chunk_id, text in chunks:
        score = _score_chunk(query, query_tokens, chunk_id, text)
        if score > 0:
            scored.append((score, chunk_id, text))
    scored.sort(key=lambda x: (-x[0], x[1]))
    # Keep first occurrence per id and cap size.
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for _, chunk_id, text in scored:
        if chunk_id in seen:
            continue
        seen.add(chunk_id)
        out.append((chunk_id, text))
        if len(out) >= top_k:
            break
    return out
