"""
Synthesize replay-shaped objects and heuristic answer provenance from existing audit files.

v1 scope: gate / merge / pipeline correlation. Full Voice answer replay requires future
correlation IDs and prompt logging (see docs/harness-replay-spec.md).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grace_mar.replay.loaders import (
    load_compute_ledger,
    load_fork_lineage,
    load_harness_events,
    load_merge_receipts,
    load_pipeline_events,
)

# Heuristic provenance classes for dashboard / brief (not ground-truth attribution).
ANSWER_CLASS_ENUM = (
    "record_backed",
    "runtime_backed",
    "mixed",
    "policy_shaped",
    "audit_only",
    "unresolved",
)


def _synthetic_session_id(row: dict[str, Any]) -> str | None:
    ch = str(row.get("channel_key") or "").strip()
    ts = str(row.get("ts") or "")[:10]
    if not ch and not ts:
        return None
    h = hashlib.sha256(f"{ch}|{ts}".encode()).hexdigest()[:12]
    return f"synth_{h}"


def _user_slug(user_dir: Path) -> str:
    return user_dir.name


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def build_replay_events(
    user_dir: Path,
    repo_root: Path,
    *,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """
    Build harness-replay-event-shaped dicts from recent pipeline rows (newest last truncated).

    Does not duplicate raw JSONL; this is a compact interpretation layer for UI/tools.
    """
    pl = load_pipeline_events(user_dir)
    mr = load_merge_receipts(user_dir)
    cl = load_compute_ledger(user_dir)
    fl = load_fork_lineage(user_dir)
    tail = pl[-limit:] if len(pl) > limit else pl
    out: list[dict[str, Any]] = []
    merge_ids = [f"mr_{i}_{r.get('merged_at', i)}" for i, r in enumerate(mr)]
    ledger_ids = [f"cl_{i}" for i in range(len(cl))]
    lineage_ids = [f"fl_{i}" for i in range(len(fl))]
    user_slug = _user_slug(user_dir)
    for row in tail:
        eid = str(row.get("event_id") or "")
        ev = str(row.get("event") or "unknown")
        ts = str(row.get("ts") or "")
        cid = str(row.get("candidate_id") or "")
        rr = row.get("record_refs") if isinstance(row.get("record_refs"), list) else []
        rt = row.get("runtime_refs") if isinstance(row.get("runtime_refs"), list) else []
        pr = row.get("policy_refs") if isinstance(row.get("policy_refs"), list) else []
        record_refs = [str(x) for x in rr]
        runtime_refs = [str(x) for x in rt] if rt else default_runtime_refs(user_dir, repo_root)
        policy_refs = [str(x) for x in pr] if pr else default_policy_refs(user_dir, repo_root)
        related_mr = [merge_ids[i] for i, r in enumerate(mr) if cid and _merge_has_candidate(r, cid)]
        doc: dict[str, Any] = {
            "schema_version": "1.0.0",
            "event_id": eid or f"hre_synth_{ts}_{ev}_{cid}"[:80],
            "user_slug": user_slug,
            "timestamp": ts or datetime.now(timezone.utc).isoformat(),
            "event_type": ev,
            "session_id": _synthetic_session_id(row),
            "source_refs": {
                "pipeline_event_ids": [eid] if eid else [],
                "merge_receipt_keys": related_mr[:8],
                "compute_ledger_ids": ledger_ids[-5:],
                "lineage_ids": lineage_ids[-5:],
            },
            "record_refs": record_refs,
            "runtime_refs": runtime_refs,
            "policy_refs": policy_refs,
            "artifact_refs": [],
            "summary": f"Pipeline `{ev}`" + (f" for `{cid}`" if cid else "") + ".",
        }
        out.append(doc)
    return out


def _merge_has_candidate(receipt: dict[str, Any], candidate_id: str) -> bool:
    ids = receipt.get("candidate_ids")
    if not isinstance(ids, list):
        return False
    c = candidate_id.strip().upper()
    return any(str(x).upper() == c for x in ids)


def default_runtime_refs(user_dir: Path, repo_root: Path) -> list[str]:
    refs: list[str] = []
    for name in ("self-memory.md", "session-transcript.md", "session-log.md"):
        p = user_dir / name
        if p.is_file():
            refs.append(_repo_relative(p, repo_root))
    return refs


def default_policy_refs(user_dir: Path, repo_root: Path) -> list[str]:
    refs: list[str] = []
    for name in ("intent.md", "intent_snapshot.json"):
        p = user_dir / name
        if p.is_file():
            refs.append(_repo_relative(p, repo_root))
    return refs


def classify_pipeline_row_provenance(row: dict[str, Any]) -> str:
    """Heuristic class for one pipeline row (audit/governance oriented)."""
    ev = str(row.get("event") or "").lower()
    rr = row.get("record_refs") if isinstance(row.get("record_refs"), list) else []
    pr = row.get("policy_refs") if isinstance(row.get("policy_refs"), list) else []
    rt = row.get("runtime_refs") if isinstance(row.get("runtime_refs"), list) else []
    has_rec = len(rr) > 0
    has_pol = len(pr) > 0
    has_rt = len(rt) > 0
    if ev in ("applied", "approved") and has_rec:
        return "record_backed"
    if ev in ("gate_reclassified", "staged") and has_pol and not has_rec:
        return "policy_shaped"
    if ev in ("staged",) and has_rec and has_rt:
        return "mixed"
    if ev in ("staged", "rejected", "deferred") and not has_rec and not has_rt:
        return "audit_only"
    if has_rt and not has_rec:
        return "runtime_backed"
    if has_rec and has_rt:
        return "mixed"
    if has_rec:
        return "record_backed"
    return "unresolved"


def infer_answer_provenance(
    user_dir: Path,
    repo_root: Path,
    *,
    session_window_events: int = 80,
) -> dict[str, Any]:
    """
    Aggregate heuristic provenance from recent pipeline activity (not per chat message).
    """
    pl = load_pipeline_events(user_dir)
    window = pl[-session_window_events:] if len(pl) > session_window_events else pl
    counts: dict[str, int] = {k: 0 for k in ANSWER_CLASS_ENUM}
    for row in window:
        cls = classify_pipeline_row_provenance(row)
        if cls in counts:
            counts[cls] += 1
    total = sum(counts.values()) or 1
    weights = {k: round(counts[k] / total, 4) for k in counts}
    user_slug = _user_slug(user_dir)
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    prov_id = f"prov_{user_slug}_{ts[:10].replace('-', '')}"
    return {
        "schema_version": "1.0.0",
        "provenance_id": prov_id,
        "user_slug": user_slug,
        "timestamp": ts,
        "session_id": None,
        "answer_class": _dominant_class(counts),
        "record_weight_estimated": weights["record_backed"] + 0.5 * weights["mixed"],
        "runtime_weight_estimated": weights["runtime_backed"] + 0.5 * weights["mixed"],
        "policy_weight_estimated": weights["policy_shaped"],
        "audit_weight_estimated": weights["audit_only"] + weights["unresolved"],
        "weights_are_heuristic": True,
        "record_refs": [_repo_relative(user_dir / "self.md", repo_root)] if (user_dir / "self.md").is_file() else [],
        "runtime_refs": default_runtime_refs(user_dir, repo_root),
        "policy_refs": default_policy_refs(user_dir, repo_root),
        "staged_changes": [
            {"candidate_id": r.get("candidate_id"), "ts": r.get("ts"), "event": r.get("event")}
            for r in window
            if str(r.get("event") or "").lower() == "staged"
        ][-5:],
        "class_counts": counts,
        "notes": "Heuristic mix from recent pipeline rows; not token-level model attribution.",
    }


def _dominant_class(counts: dict[str, int]) -> str:
    best = max(counts, key=lambda k: counts[k])
    if counts[best] == 0:
        return "unresolved"
    return best


def replay_provenance_summary(user_dir: Path, repo_root: Path) -> dict[str, Any]:
    """Structured summary for session_brief and metrics (counts + copy lines)."""
    pl = load_pipeline_events(user_dir)
    hv = load_harness_events(user_dir)
    replay_events = build_replay_events(user_dir, repo_root, limit=min(500, max(50, len(pl))))
    prov = infer_answer_provenance(user_dir, repo_root)
    staged_recent = [r for r in pl if str(r.get("event") or "").lower() == "staged"][-3:]
    unresolved_n = sum(
        1 for r in pl[-200:] if classify_pipeline_row_provenance(r) == "unresolved"
    )
    event_types: dict[str, int] = {}
    for r in pl[-500:]:
        e = str(r.get("event") or "?")
        event_types[e] = event_types.get(e, 0) + 1
    top_events = sorted(event_types.items(), key=lambda x: -x[1])[:8]
    return {
        "total_pipeline_rows": len(pl),
        "total_replay_synthesized": len(replay_events),
        "total_harness_rows": len(hv),
        "unresolved_provenance_recent_window": unresolved_n,
        "provenance": prov,
        "top_event_categories": top_events,
        "recent_staged": staged_recent,
    }


def write_replay_artifacts(
    user_dir: Path,
    repo_root: Path,
    *,
    out_dir: Path | None = None,
) -> tuple[Path | None, Path | None]:
    """
    Write timestamped JSON artifacts under users/<id>/artifacts/replay/ (derived only).
    Returns (replay_path, provenance_path) or None if skipped.
    """
    base = out_dir or (user_dir / "artifacts" / "replay")
    base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    replay = build_replay_events(user_dir, repo_root, limit=300)
    prov = infer_answer_provenance(user_dir, repo_root)
    rp = base / f"replay-{stamp}.json"
    pp = base / f"provenance-{stamp}.json"
    rp.write_text(json.dumps(replay, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pp.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return rp, pp


__all__ = [
    "ANSWER_CLASS_ENUM",
    "build_replay_events",
    "classify_pipeline_row_provenance",
    "default_policy_refs",
    "default_runtime_refs",
    "infer_answer_provenance",
    "replay_provenance_summary",
    "write_replay_artifacts",
]
