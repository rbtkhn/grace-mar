"""
Optional constitutional self-critique pass after the main Voice reply.

Governance: Does not add Record facts. Operator enables via runtime_config.json
(copy from runtime_config.example.json). Constitution text comes from
users/<id>/seed-phase/seed_constitution.json (seed-phase artifact), not from
LLM invention. Disabled by default (constitutional_critique.enabled: false).

See docs/seed-phase-validation.md and runtime_config.example.json.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

import cachetools
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

_l1: cachetools.TTLCache = cachetools.TTLCache(maxsize=2000, ttl=3600)
_cache_hits = 0
_cache_misses = 0
_redis_client: Any = None
_cfg_mtime: float | None = None
_cfg_cache: dict | None = None
_const_cache: tuple[float, dict | None] | None = None


class CritiqueOutput(BaseModel):
    violations: list[str] = Field(default_factory=list)
    score: float = Field(ge=0.0, le=1.0)
    suggestion: str = ""
    early_exit: bool = False


def _load_runtime_config(repo_root: Path) -> dict:
    global _cfg_mtime, _cfg_cache
    path = repo_root / "runtime_config.json"
    if not path.is_file():
        return {}
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return {}
    if _cfg_cache is not None and _cfg_mtime == mtime:
        return _cfg_cache
    _cfg_cache = json.loads(path.read_text(encoding="utf-8"))
    _cfg_mtime = mtime
    return _cfg_cache


def _load_constitution(profile_dir: Path) -> dict | None:
    global _const_cache
    path = profile_dir / "seed-phase" / "seed_constitution.json"
    if not path.is_file():
        return None
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return None
    if _const_cache and _const_cache[0] == mtime:
        return _const_cache[1]
    data = json.loads(path.read_text(encoding="utf-8"))
    _const_cache = (mtime, data)
    return data


def _redis():
    global _redis_client
    if _redis_client is not False and _redis_client is None:
        url = os.getenv("CONSTITUTIONAL_REDIS_URL", "").strip()
        if not url:
            _redis_client = False
            return None
        try:
            import redis

            r = redis.from_url(url, decode_responses=True, socket_timeout=2.0)
            r.ping()
            _redis_client = r
        except Exception:
            logger.warning("Constitutional Redis unavailable; using L1 cache only")
            _redis_client = False
            return None
    if _redis_client is False:
        return None
    return _redis_client


def _cache_key(
    user_message: str, assistant_excerpt: str, constitution_version: str, model: str
) -> str:
    raw = f"{user_message[:400]}\n{assistant_excerpt[:400]}\n{constitution_version}\n{model}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _should_apply(
    cc: dict,
    confidence: float,
    assistant_text: str,
    trigger_flags: frozenset[str] | None,
) -> bool:
    if not cc.get("enabled"):
        return False
    threshold = float(cc.get("trigger_threshold", 0.78))
    long_len = int(cc.get("long_response_chars", 800))
    scope = set(cc.get("scope_flags", []))
    flags = trigger_flags or frozenset()
    if confidence < threshold:
        return True
    if len(assistant_text or "") > long_len:
        return True
    if flags and (flags & scope):
        return True
    return False


def _build_critique_messages(constitution: dict, assistant_text: str) -> list[dict]:
    proto = constitution.get("self_critique_protocol") or {}
    tmpl = (proto.get("critique_prompt_template") or "").strip()
    hier = constitution.get("hierarchy", [])
    names = [p.get("name", "") for p in (constitution.get("principles") or [])[:8]]
    static = (
        tmpl
        or (
            "Critique the assistant reply against the constitution hierarchy (memory_contract first). "
            'Return JSON only: {"violations":[],"score":0.0-1.0,"suggestion":"","early_exit":false}'
        )
    )
    static = f"{static}\n\nHierarchy (highest first): {hier}\nPrinciple names: {names}"
    excerpt = (assistant_text or "")[:700]
    return [
        {"role": "system", "content": static},
        {"role": "user", "content": f"Assistant reply to critique:\n{excerpt}"},
    ]


def _log_metric(
    profile_dir: Path, monitoring: dict, row: dict
) -> None:
    if not monitoring.get("log_critique_decisions"):
        return
    name = monitoring.get("metrics_filename") or "constitutional_metrics.jsonl"
    path = profile_dir / name
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
    except OSError:
        logger.exception("Failed to append constitutional metric")


def maybe_apply_constitutional_critique(
    *,
    repo_root: Path,
    profile_dir: Path,
    user_message: str,
    assistant_text: str,
    channel_key: str,
    client: Any,
    confidence: float = 1.0,
    trigger_flags: frozenset[str] | None = None,
    main_model: str | None = None,
) -> str:
    """Return possibly revised assistant text. On any failure, returns original."""
    if not assistant_text or not assistant_text.strip():
        return assistant_text

    cfg = _load_runtime_config(repo_root)
    cc = cfg.get("constitutional_critique") or {}
    if not _should_apply(cc, confidence, assistant_text, trigger_flags):
        return assistant_text

    constitution = _load_constitution(profile_dir)
    if not constitution:
        return assistant_text

    ver = str(constitution.get("version", "1.0"))
    crit_model = os.getenv("OPENAI_CRITIQUE_MODEL", "").strip() or main_model
    main_m = main_model or os.getenv("OPENAI_MODEL", "gpt-4o")
    crit_model = crit_model or main_m
    if cc.get("use_cheaper_model") is False:
        crit_model = main_m

    excerpt = assistant_text[:300]
    key = _cache_key(user_message, excerpt, ver, crit_model)
    ttl = int(cc.get("cache_ttl_seconds", 3600))

    global _cache_hits, _cache_misses
    if key in _l1:
        _cache_hits += 1
        return _l1[key]

    r = _redis()
    if r:
        try:
            got = r.get(f"c:{key}")
            if got:
                _cache_hits += 1
                return json.loads(got)
        except Exception:
            pass
    _cache_misses += 1

    t0 = time.perf_counter()
    monitoring = cfg.get("monitoring") or {}
    try:
        resp = client.chat.completions.create(
            model=crit_model,
            messages=_build_critique_messages(constitution, assistant_text),
            max_tokens=min(int(cc.get("max_added_tokens", 400)), 800),
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        raw = (resp.choices[0].message.content or "").strip()
        critique = CritiqueOutput.model_validate_json(raw)
    except Exception as e:
        logger.warning("Constitutional critique failed (using original reply): %s", e)
        _log_metric(
            profile_dir,
            monitoring,
            {
                "event": "critique_error",
                "channel_key": channel_key,
                "error": str(e)[:200],
            },
        )
        return assistant_text

    if critique.early_exit or critique.score >= 0.92:
        _l1[key] = assistant_text
        if r:
            try:
                r.setex(f"c:{key}", ttl, json.dumps(assistant_text))
            except Exception:
                pass
        _log_metric(
            profile_dir,
            monitoring,
            {
                "event": "critique_skip_revision",
                "channel_key": channel_key,
                "score": critique.score,
                "ms": round((time.perf_counter() - t0) * 1000, 2),
            },
        )
        return assistant_text

    proto = constitution.get("self_critique_protocol") or {}
    rev_intro = (proto.get("revision_prompt_template") or "").strip() or (
        "Revise the reply to fix violations; keep simple vocabulary and respect abstention when uncertain."
    )
    try:
        rev = client.chat.completions.create(
            model=crit_model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"{rev_intro}\nFix: {critique.suggestion}\n\nOriginal:\n{assistant_text[:1200]}"
                    ),
                }
            ],
            max_tokens=min(int(cc.get("max_added_tokens", 400)), 600),
            temperature=0.4,
        )
        revised = (rev.choices[0].message.content or "").strip() or assistant_text
    except Exception as e:
        logger.warning("Constitutional revision failed: %s", e)
        return assistant_text

    _l1[key] = revised
    if r:
        try:
            r.setex(f"c:{key}", ttl, json.dumps(revised))
        except Exception:
            pass

    _log_metric(
        profile_dir,
        monitoring,
        {
            "event": "critique_revised",
            "channel_key": channel_key,
            "score": critique.score,
            "violations": len(critique.violations),
            "ms": round((time.perf_counter() - t0) * 1000, 2),
        },
    )
    return revised


def cache_stats() -> dict:
    return {"l1_hits": _cache_hits, "l1_misses": _cache_misses, "l1_size": len(_l1)}
