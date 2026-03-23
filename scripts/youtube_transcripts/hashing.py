from __future__ import annotations

import hashlib
import re

from youtube_transcripts.constants import PIPELINE_VERSION


def strip_transcript_header(raw: str) -> str:
    """Remove # comment header block at top of saved .txt files."""
    lines = raw.splitlines()
    i = 0
    while i < len(lines) and (lines[i].startswith("#") or lines[i].strip() == ""):
        i += 1
    return "\n".join(lines[i:]).strip()


def normalize_for_hash(text: str) -> str:
    """Unicode NFKC + collapse whitespace for stable hashing."""
    import unicodedata

    t = unicodedata.normalize("NFKC", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def compute_content_hash(video_id: str, body_text: str, pipeline_version: str = PIPELINE_VERSION) -> str:
    normalized = normalize_for_hash(strip_transcript_header(body_text))
    h = hashlib.sha256()
    h.update(video_id.encode("utf-8"))
    h.update(b"|")
    h.update(pipeline_version.encode("utf-8"))
    h.update(b"|")
    h.update(normalized.encode("utf-8"))
    return h.hexdigest()
