"""
Lightweight retriever over SELF, SKILLS, EVIDENCE.

Used for grounded answering: fetch relevant chunks so responses can cite source IDs.
Keyword + section heuristics — no embeddings.

Tier 1.3 (`run_perf_suite.py`) benchmarks this module. Vector / Chroma indexing for
semantic search is separate — see `scripts/index_record.py`.
"""

import os
import pickle
import re
from pathlib import Path

USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
PROFILE_DIR = Path(__file__).resolve().parent.parent / "users" / USER_ID
SELF_PATH = PROFILE_DIR / "self.md"
SKILLS_PATHS = [
    PROFILE_DIR / "skills.md",
    PROFILE_DIR / "skill-think.md",
    PROFILE_DIR / "skill-write.md",
]
WORK_PATHS = [
    PROFILE_DIR / "work-alpha-school.md",
    PROFILE_DIR / "work-jiang.md",
]
EVIDENCE_PATH = PROFILE_DIR / "self-evidence.md"

DISK_CACHE_PATH = PROFILE_DIR / ".cache" / "retriever_chunks.pkl"

# In-process cache for load_record_chunks (invalidated when any source file mtime changes)
_chunks_cache: list[tuple[str, str]] | None = None
_chunks_mtime: float = 0.0
# token -> chunk row indices (aligned with _chunks_cache); rebuilt with chunks
_chunks_inv: dict[str, set[int]] | None = None


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _max_mtime(paths: list[Path]) -> float:
    """Max mtime of paths that exist; 0 if none exist."""
    mt = 0.0
    for p in paths:
        if p.exists():
            mt = max(mt, p.stat().st_mtime)
    return mt


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


def _all_record_paths() -> list[Path]:
    return [SELF_PATH] + list(SKILLS_PATHS) + list(WORK_PATHS) + [EVIDENCE_PATH]


def _source_fingerprint(paths: list[Path]) -> tuple[tuple[str, float, int], ...]:
    """Stable fingerprint from path, mtime, size — invalidates disk cache when Record files change."""
    out: list[tuple[str, float, int]] = []
    for p in sorted(paths, key=lambda x: str(x)):
        if p.exists():
            st = p.stat()
            out.append((str(p.resolve()), st.st_mtime, st.st_size))
        else:
            out.append((str(p.resolve()), 0.0, 0))
    return tuple(out)


def _build_inverted_index(chunks: list[tuple[str, str]]) -> dict[str, set[int]]:
    inv: dict[str, set[int]] = {}
    for i, (_, text) in enumerate(chunks):
        for t in _tokenize(text):
            inv.setdefault(t, set()).add(i)
    return inv


def load_record_chunks() -> list[tuple[str, str]]:
    """Load all chunks from SELF, SKILLS, EVIDENCE.

    Caching: in-process (``GRACE_MAR_RETRIEVER_CACHE=0`` disables); optional disk
    pickle under ``users/<id>/.cache/retriever_chunks.pkl`` (``GRACE_MAR_RETRIEVER_DISK_CACHE=0`` disables).
    """
    global _chunks_cache, _chunks_mtime, _chunks_inv
    paths = _all_record_paths()
    max_mt = _max_mtime(paths)
    fp = _source_fingerprint(paths)

    if (
        os.getenv("GRACE_MAR_RETRIEVER_CACHE", "1") != "0"
        and _chunks_cache is not None
        and max_mt > 0
        and max_mt == _chunks_mtime
    ):
        if _chunks_inv is None:
            _chunks_inv = _build_inverted_index(_chunks_cache)
        return _chunks_cache

    disk_ok = os.getenv("GRACE_MAR_RETRIEVER_DISK_CACHE", "1") != "0"
    if disk_ok and DISK_CACHE_PATH.exists():
        try:
            payload = pickle.loads(DISK_CACHE_PATH.read_bytes())
            if payload.get("fp") == fp:
                _chunks_cache = payload["chunks"]
                _chunks_inv = payload.get("inv")
                if not _chunks_inv:
                    _chunks_inv = _build_inverted_index(_chunks_cache)
                _chunks_mtime = max_mt
                return _chunks_cache
        except (OSError, pickle.UnpicklingError, TypeError, KeyError, AttributeError):
            pass

    chunks: list[tuple[str, str]] = []
    if SELF_PATH.exists():
        chunks.extend(_extract_chunks(_read(SELF_PATH), "SELF"))
    for p in SKILLS_PATHS:
        if p.exists():
            chunks.extend(_extract_chunks(_read(p), "SKILLS"))
    for p in WORK_PATHS:
        if p.exists():
            chunks.extend(_extract_chunks(_read(p), "WORK"))
    if EVIDENCE_PATH.exists():
        chunks.extend(_extract_chunks(_read(EVIDENCE_PATH), "EVIDENCE"))

    _chunks_inv = _build_inverted_index(chunks)
    _chunks_cache = chunks
    _chunks_mtime = max_mt

    if disk_ok:
        try:
            DISK_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            DISK_CACHE_PATH.write_bytes(
                pickle.dumps(
                    {"fp": fp, "chunks": chunks, "inv": _chunks_inv},
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
            )
        except OSError:
            pass

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

    use_inv = os.getenv("GRACE_MAR_RETRIEVER_INVERTED_INDEX", "1") != "0"
    global _chunks_inv
    if _chunks_inv is None:
        _chunks_inv = _build_inverted_index(chunks)

    if use_inv:
        cand_idx: set[int] = set()
        for t in query_tokens:
            cand_idx |= _chunks_inv.get(t, set())
        if not cand_idx:
            return []
        to_score = [chunks[i] for i in sorted(cand_idx)]
    else:
        to_score = chunks

    scored: list[tuple[float, str, str]] = []
    for chunk_id, text in to_score:
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
