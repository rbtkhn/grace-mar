"""
Query Civilization Memory Codex (CMC) for historical/civilizational lookup.

When the question touches civilizational history, Rome, China, ancient civilizations,
or similar topics, the bot can query CMC as an approved external source (LIB-0064).

Routing: Only attempt CMC when the question matches CMC scope (LIB-0064). Otherwise
skip straight to full LLM lookup — avoids wasted subprocess calls and wrong-source answers.

Requires:
  - CMC repo at CIVILIZATION_MEMORY_PATH or ../civilization_memory (sibling to grace-mar)
  - Index built: cd CMC && python3 tools/cmc-index-search.py build

Returns combined snippet text for REPHRASE, or None if CMC unavailable or no matches.
"""

import logging
import os
import re
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CMC_PATH = REPO_ROOT.parent / "civilization_memory"


def _get_cmc_path() -> Path | None:
    """Resolve CMC repo path. Returns None if not found."""
    path = os.getenv("CIVILIZATION_MEMORY_PATH", "").strip()
    if path:
        p = Path(path).resolve()
        if p.is_dir():
            return p
    p = DEFAULT_CMC_PATH.resolve()
    return p if p.is_dir() else None


# Negative triggers: if question matches, never route to CMC.
_NEGATIVE_PHRASES = (
    "how do you spell",
    "how to spell",
    "what's the spelling",
    "spell the word",
)
_NEGATIVE_WORDS = frozenset(
    "spell spelling math maths arithmetic add subtract multiply divide calculator equation formula"
    .split()
)

# Strong terms: civilization/region names + high-value historical/cultural terms.
# One match (+ no negative) = route.
# Includes US history (America, Lincoln), classical music/ballet (Nutcracker, Tchaikovsky, Schubert, Austria).
_STRONG_TERMS = frozenset(
    "rome roman romans china chinese greece greek greeks egypt egyptian persia persian india indian "
    "russia russian anglia britain british england english mongol ottoman byzantine islam islamic "
    "french france germany german africa african maya mayan aztec inca mesopotamia babylon "
    "america american americans austria austrian vienna "
    "lincoln nutcracker tchaikovsky schubert ballet president presidents"
    .split()
)

# Weak terms: historical concepts. Need strong term OR 2+ weak (avoids "history of Pokemon").
_WEAK_TERMS = frozenset(
    "ancient dynasty emperor empress empire empires civilization civilizations conquest war treaty "
    "medieval renaissance colonial revolution strategy political politics culture pharaoh pharaohs "
    "aqueduct aqueducts roman empire composer composers symphony"
    .split()
)


def should_route_to_cmc(question: str) -> bool:
    """
    Return True if the question likely touches CMC scope (civilizational/historical).

    Combination routing:
    - Negative triggers: skip if question indicates spelling, math, etc.
    - Strong terms (civilization names): one match → route
    - Weak terms (concepts): route only if 2+ weak terms (avoids "history of Pokemon")
    """
    q = question.lower().strip()
    words = set(re.findall(r"[a-zA-Z]{3,}", q))

    # Negative: explicit skip
    if words & _NEGATIVE_WORDS:
        return False
    for phrase in _NEGATIVE_PHRASES:
        if phrase in q:
            return False

    # Strong: civilization/region → route
    if words & _STRONG_TERMS:
        return True

    # Weak: need 2+ concepts to avoid overly broad matches
    weak_matches = words & _WEAK_TERMS
    return len(weak_matches) >= 2


_FTS_STOPWORDS = frozenset(
    "the and for are but not you all can had her was one our out day get has him his how man new now old see way who boy did its let put say she too use what when where why"
    .split()
)


def _safe_query(question: str) -> str:
    """Extract FTS5-safe terms: alphanumeric words 3+ chars, drop stopwords."""
    words = re.findall(r"[a-zA-Z0-9]{3,}", question.lower())
    keep = [w for w in words if w not in _FTS_STOPWORDS][:10]
    return " ".join(keep) if keep else " ".join(words[:8])


def _index_exists(cmc_root: Path) -> bool:
    """Check if CMC search index exists."""
    db = cmc_root / ".cache" / "cmc_search.db"
    return db.is_file()


def query_cmc(question: str, limit: int = 5, skip_routing: bool = False) -> str | None:
    """
    Query CMC index. Returns combined snippet text, or None.

    If skip_routing=False, returns None immediately when should_route_to_cmc(question)
    is False (avoids subprocess for off-scope questions).

    Runs: python3 tools/cmc-index-search.py query "..." --limit N
    from CMC repo root. Parses output and returns text suitable for REPHRASE.
    """
    if not skip_routing and not should_route_to_cmc(question):
        logger.debug("CMC: skip (question outside scope)")
        return None
    cmc_root = _get_cmc_path()
    if not cmc_root:
        logger.debug("CMC: repo not found (set CIVILIZATION_MEMORY_PATH or clone sibling)")
        return None
    if not _index_exists(cmc_root):
        logger.debug("CMC: index not built (run: cd %s && python3 tools/cmc-index-search.py build)", cmc_root)
        return None

    script = cmc_root / "tools" / "cmc-index-search.py"
    if not script.is_file():
        logger.debug("CMC: cmc-index-search.py not found at %s", script)
        return None

    safe_q = _safe_query(question)
    if not safe_q:
        return None
    try:
        proc = subprocess.run(
            ["python3", str(script), "query", safe_q, "--limit", str(limit)],
            cwd=str(cmc_root),
            capture_output=True,
            text=True,
            timeout=15,
        )
        if proc.returncode != 0:
            logger.warning("CMC query failed: %s", proc.stderr[:200] if proc.stderr else "unknown")
            return None
        out = (proc.stdout or "").strip()
        if not out or "No matches" in out:
            return None

        # Parse: "1. path" / "  title" / "  snippet" blocks
        parts = []
        for block in re.split(r"\n(?=\d+\.\s)", out):
            block = block.strip()
            if not block:
                continue
            lines = block.splitlines()
            if len(lines) >= 3:
                # path, title, snippet
                snippet = lines[2].strip()
                if snippet:
                    parts.append(snippet)
        if not parts:
            return None
        combined = "\n\n".join(parts[:limit])
        logger.info("CMC: hit for %s (%d snippets)", question[:50], len(parts))
        return combined
    except subprocess.TimeoutExpired:
        logger.warning("CMC query timeout")
        return None
    except Exception:
        logger.exception("CMC query error")
        return None
