#!/usr/bin/env python3
"""Build a derived contradiction digest from canonical gate/profile surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USERS_DIR = REPO_ROOT / "users"
DEFAULT_USER = "grace-mar"
RULES_PATH = REPO_ROOT / "bot" / "conflict_rules.yaml"
SELF_PROPOSALS_DIR = REPO_ROOT / "auto-research" / "self-proposals"
SWARM_ACCEPTED_DIR = REPO_ROOT / "auto-research" / "swarm" / "accepted"

for path in (REPO_ROOT / "scripts", SELF_PROPOSALS_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from gate_block_parser import iter_candidate_yaml_blocks, split_gate_sections
from proposal_io import validate_grounding, validate_payload

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "because",
    "for",
    "from",
    "has",
    "have",
    "how",
    "in",
    "is",
    "it",
    "its",
    "not",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "with",
    "you",
    "your",
}


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _strip_quotes(value: str) -> str:
    return value.strip().strip("\"'")


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _tokenize(text: str) -> list[str]:
    out: list[str] = []
    for token in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if len(token) < 4 or token in _STOPWORDS:
            continue
        out.append(token)
    return out


def _extract_scalar(yaml_body: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    if not match:
        return ""
    return _strip_quotes(match.group(1))


def _extract_block(yaml_body: str, key: str) -> str:
    lines = yaml_body.splitlines()
    out: list[str] = []
    start_idx: int | None = None
    base_indent = 0
    for idx, line in enumerate(lines):
        match = re.match(rf"^(\s*){re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        tail = match.group(2).strip()
        if tail:
            return _strip_quotes(tail)
        start_idx = idx + 1
        base_indent = len(match.group(1))
        break
    if start_idx is None:
        return ""
    for line in lines[start_idx:]:
        if not line.strip():
            if out:
                out.append("")
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= base_indent and re.match(r"^\s*[A-Za-z0-9_-]+:", line):
            break
        out.append(line[base_indent + 2 :] if indent >= base_indent + 2 else line.strip())
    return "\n".join(out).strip()


def _load_personality_opposites() -> list[tuple[str, str]]:
    if not RULES_PATH.exists():
        return []
    content = RULES_PATH.read_text(encoding="utf-8")
    pairs: list[tuple[str, str]] = []
    for match in re.finditer(r"-\s*\[\s*([^,\]]+)\s*,\s*([^\]\]]+)\s*\]", content):
        left = match.group(1).strip().strip("\"'")
        right = match.group(2).strip().strip("\"'")
        if left and right:
            pairs.append((left.lower(), right.lower()))
    return pairs


def _self_personality_summary(self_text: str) -> str:
    parts: list[str] = []
    for match in re.finditer(r"trait:\s*([^\n]+)", self_text, re.IGNORECASE):
        parts.append(match.group(1).strip().lower())

    match = re.search(r"Personality:\s*([^\n]+)", self_text, re.IGNORECASE)
    if match:
        parts.append(match.group(1).strip().lower())

    ix_c = re.search(r"### IX-C\. PERSONALITY.*?```yaml\n(.*?)```", self_text, re.DOTALL)
    if ix_c:
        for obs in re.finditer(r"observation:\s*[\"']?([^\"'\n]+)", ix_c.group(1)):
            parts.append(obs.group(1).strip().lower())
    return " ".join(parts)


def _word_present(word: str, text: str) -> bool:
    return bool(re.search(rf"\b{re.escape(word)}\b", text))


def _parse_candidate_rows(users_dir: Path, user_id: str) -> tuple[list[dict[str, Any]], str]:
    gate_path = users_dir / user_id / "recursion-gate.md"
    self_text = _read(users_dir / user_id / "self.md")
    active, _ = split_gate_sections(_read(gate_path))
    rows: list[dict[str, Any]] = []
    for candidate_id, title, yaml_body in iter_candidate_yaml_blocks(active):
        status = (_extract_scalar(yaml_body, "status") or "pending").lower()
        if status != "pending":
            continue
        rows.append(
            {
                "candidate_id": candidate_id,
                "title": title,
                "status": status,
                "timestamp": _extract_scalar(yaml_body, "timestamp"),
                "summary": _extract_scalar(yaml_body, "summary"),
                "mind_category": _extract_scalar(yaml_body, "mind_category"),
                "profile_target": _extract_scalar(yaml_body, "profile_target"),
                "prompt_section": _extract_scalar(yaml_body, "prompt_section"),
                "proposal_class": _extract_scalar(yaml_body, "proposal_class"),
                "priority_score": _extract_scalar(yaml_body, "priority_score"),
                "channel_key": _extract_scalar(yaml_body, "channel_key"),
                "suggested_entry": _extract_block(yaml_body, "suggested_entry"),
                "prompt_addition": _extract_block(yaml_body, "prompt_addition"),
                "example_from_exchange": _extract_block(yaml_body, "example_from_exchange"),
                "source_exchange": _extract_block(yaml_body, "source_exchange"),
                "raw_block": yaml_body,
            }
        )
    return rows, self_text


def _duplicate_hints(row: dict[str, Any], self_text: str) -> list[str]:
    hints: list[str] = []
    summary = str(row.get("summary") or "")
    lower_summary = summary.lower()
    if any(marker in lower_summary for marker in ("duplicate", "overlap", "already in record", "already in ix", "skip prompt")):
        hints.append(summary)
    for key in ("suggested_entry", "prompt_addition"):
        value = str(row.get(key) or "").strip()
        if not value or value.lower() == "none":
            continue
        normalized = _normalize(value)
        if len(normalized) > 24 and normalized in _normalize(self_text):
            hints.append(f"{key} overlaps existing Record text")
            continue
        keywords = _tokenize(value)
        if keywords:
            overlap = sum(1 for keyword in keywords[:5] if keyword in _normalize(self_text))
            if overlap >= 3:
                hints.append(f"{key} likely overlaps existing Record knowledge/personality")
    deduped: list[str] = []
    seen = set()
    for hint in hints:
        if hint in seen:
            continue
        seen.add(hint)
        deduped.append(hint)
    return deduped[:3]


def _personality_conflicts(row: dict[str, Any], self_text: str) -> list[dict[str, Any]]:
    if str(row.get("mind_category") or "").lower() != "personality":
        return []
    existing_text = _self_personality_summary(self_text)
    if not existing_text:
        return []
    new_text = " ".join(
        str(row.get(key) or "")
        for key in ("suggested_entry", "summary", "prompt_addition")
    ).lower()
    if not new_text:
        return []
    conflicts: list[dict[str, Any]] = []
    for left, right in _load_personality_opposites():
        left_existing = _word_present(left, existing_text)
        right_existing = _word_present(right, existing_text)
        left_new = _word_present(left, new_text)
        right_new = _word_present(right, new_text)
        if (left_existing and right_new) or (right_existing and left_new):
            existing_word = left if left_existing else right
            new_word = right if left_existing else left
            conflicts.append(
                {
                    "rule": "personality_opposites",
                    "pair": [left, right],
                    "existing_hint": f"profile has '{existing_word}'",
                    "new_hint": f"candidate has '{new_word}'",
                }
            )
    return conflicts


def _overlap_summary(row: dict[str, Any], self_text: str) -> dict[str, Any]:
    candidate_text = " ".join(
        str(row.get(key) or "")
        for key in ("summary", "suggested_entry", "prompt_addition")
    )
    candidate_tokens = sorted(set(_tokenize(candidate_text)))
    if not candidate_tokens:
        return {"count": 0, "ratio": 0.0, "keywords": []}
    self_norm = _normalize(self_text)
    overlap = [token for token in candidate_tokens if token in self_norm]
    ratio = len(overlap) / len(candidate_tokens)
    return {
        "count": len(overlap),
        "ratio": round(ratio, 4),
        "keywords": overlap[:8],
    }


def _classify_relation(
    row: dict[str, Any],
    self_text: str,
    *,
    strict_mode: bool = False,
) -> tuple[str, list[str], list[str], list[dict[str, Any]], dict[str, Any]]:
    duplicate_hints = _duplicate_hints(row, self_text)
    personality_conflicts = _personality_conflicts(row, self_text)
    overlap = _overlap_summary(row, self_text)
    explicit_conflict = bool(re.search(r"conflicts?:|contradiction|advisory_flagged", row["raw_block"], re.IGNORECASE))

    reasons: list[str] = []
    if duplicate_hints:
        reasons.extend(duplicate_hints)
        return "duplicate", reasons[:4], duplicate_hints, personality_conflicts, overlap

    if explicit_conflict or personality_conflicts:
        if explicit_conflict:
            reasons.append("candidate already carries conflict markers")
        for conflict in personality_conflicts:
            reasons.append(f"{conflict['existing_hint']} vs {conflict['new_hint']}")
        return "contradiction", reasons[:4], duplicate_hints, personality_conflicts, overlap

    overlap_count = overlap["count"]
    overlap_ratio = overlap["ratio"]
    if strict_mode and overlap_count >= 4 and overlap_ratio >= 0.35:
        reasons.append("strict mode escalated dense overlap to contradiction-level review")
        if overlap["keywords"]:
            reasons.append("shared keywords: " + ", ".join(overlap["keywords"][:5]))
        return "contradiction", reasons[:4], duplicate_hints, personality_conflicts, overlap

    if overlap_count >= 3 and overlap_ratio >= (0.2 if strict_mode else 0.3):
        reasons.append("candidate text overlaps existing Record language without direct duplication")
        if overlap["keywords"]:
            reasons.append("shared keywords: " + ", ".join(overlap["keywords"][:5]))
        return "refinement", reasons[:4], duplicate_hints, personality_conflicts, overlap

    return "reinforcement", reasons[:4], duplicate_hints, personality_conflicts, overlap


def default_digest_path(*, users_dir: Path = DEFAULT_USERS_DIR, user_id: str = DEFAULT_USER) -> Path:
    return users_dir / user_id / "derived" / "contradictions" / "auto-dream-digest.json"


def generate_contradiction_digest(
    *,
    user_id: str = DEFAULT_USER,
    users_dir: Path = DEFAULT_USERS_DIR,
    write_path: Path | None = None,
    strict_mode: bool = False,
) -> dict[str, Any]:
    rows, self_text = _parse_candidate_rows(users_dir, user_id)
    entries: list[dict[str, Any]] = []
    relation_counts = {
        "duplicate": 0,
        "refinement": 0,
        "contradiction": 0,
        "reinforcement": 0,
    }
    for row in rows:
        relation_type, reasons, duplicate_hints, personality_conflicts, overlap = _classify_relation(
            row,
            self_text,
            strict_mode=strict_mode,
        )
        relation_counts[relation_type] += 1
        entry = {
            "candidate_id": row["candidate_id"],
            "title": row["title"],
            "timestamp": row["timestamp"],
            "mind_category": row["mind_category"],
            "profile_target": row["profile_target"],
            "proposal_class": row["proposal_class"] or None,
            "prompt_section": row["prompt_section"] or None,
            "priority_score": row["priority_score"] or None,
            "channel_key": row["channel_key"] or None,
            "summary": row["summary"],
            "suggested_entry": row["suggested_entry"],
            "prompt_addition": row["prompt_addition"],
            "source_exchange": row["source_exchange"],
            "example_from_exchange": row["example_from_exchange"],
            "relationship_type": relation_type,
            "recommended_resolution": (
                "explicit_review"
                if relation_type == "contradiction"
                else ("dedupe_or_reject" if relation_type == "duplicate" else "contextual_review")
            ),
            "why_flagged": reasons,
            "duplicate_hints": duplicate_hints,
            "personality_conflicts": personality_conflicts,
            "overlap": overlap,
            "has_conflict_markers": bool(personality_conflicts)
            or bool(re.search(r"conflicts?:|contradiction|advisory_flagged", row["raw_block"], re.IGNORECASE)),
        }
        entries.append(entry)

    digest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "strict_mode": strict_mode,
        "pending_candidate_count": len(rows),
        "reviewable_count": sum(1 for entry in entries if entry["relationship_type"] != "reinforcement"),
        "relation_counts": relation_counts,
        "entries": entries,
    }
    if write_path is not None:
        write_path.parent.mkdir(parents=True, exist_ok=True)
        write_path.write_text(json.dumps(digest, indent=2) + "\n", encoding="utf-8")
        digest["digest_path"] = str(write_path)
    return digest


def _default_prompt_section(entry: dict[str, Any]) -> str:
    prompt_section = str(entry.get("prompt_section") or "").strip()
    if prompt_section:
        return prompt_section
    mind_category = str(entry.get("mind_category") or "").lower()
    if mind_category == "curiosity":
        return "YOUR CURIOSITY"
    if mind_category == "personality":
        return "YOUR PERSONALITY"
    return "YOUR KNOWLEDGE"


def _default_profile_target(entry: dict[str, Any]) -> str:
    profile_target = str(entry.get("profile_target") or "").strip()
    if profile_target:
        return profile_target
    mind_category = str(entry.get("mind_category") or "").lower()
    if mind_category == "curiosity":
        return "IX-B. CURIOSITY"
    if mind_category == "personality":
        return "IX-C. PERSONALITY"
    return "IX-A. KNOWLEDGE"


def _priority_score(value: Any) -> int:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return 3
    return min(5, max(1, parsed))


def _source_exchange_map(entry: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    source_exchange = str(entry.get("source_exchange") or "").strip()
    example = str(entry.get("example_from_exchange") or "").strip()
    if source_exchange:
        out["candidate_source_exchange"] = source_exchange
    if example and example != source_exchange:
        out["candidate_example"] = example
    return out


def build_promotable_artifact(entry: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    source_exchange = _source_exchange_map(entry)
    if not source_exchange:
        return None, ["missing source_exchange/example_from_exchange for strict grounding"]

    summary = str(entry.get("summary") or "").strip()
    suggested_entry = str(entry.get("suggested_entry") or "").strip() or summary
    prompt_addition = str(entry.get("prompt_addition") or "").strip() or (
        "No prompt change proposed until contradiction review is resolved."
    )
    payload: dict[str, Any] = {
        "hypothesis": (
            f"Derived contradiction review for {entry['candidate_id']} should preserve the gate while "
            "making the relationship to the existing Record explicit."
        ),
        "expected_delta": 0.02,
        "grounding_mode": "strict",
        "proposal_type": "recursion_gate_candidate",
        "target_surface": "self",
        "candidate_bundle": {
            "title": f"autoDream contradiction follow-up for {entry['candidate_id']}",
            "summary": (
                f"Derived contradiction digest flagged {entry['candidate_id']} as "
                f"{entry['relationship_type']} and requests governed review."
            ),
            "source": f"operator - contradiction digest for {entry['candidate_id']}",
            "source_exchange": source_exchange,
            "mind_category": str(entry.get("mind_category") or "knowledge").lower(),
            "signal_type": "auto_dream_contradiction_digest",
            "priority_score": _priority_score(entry.get("priority_score")),
            "profile_target": _default_profile_target(entry),
            "suggested_entry": suggested_entry,
            "prompt_section": _default_prompt_section(entry),
            "prompt_addition": prompt_addition,
            "new_vs_record": (
                f"Derived digest classified {entry['candidate_id']} as {entry['relationship_type']} "
                "against the active Record."
            ),
            "proposal_class": str(entry.get("proposal_class") or "SIMULATION_RESULT"),
            "channel_key": str(entry.get("channel_key") or "operator:cursor"),
        },
        "evaluation_notes": (
            "Derived from contradiction digest; not auto-staged. Promotion still requires the shared "
            "artifact bridge and operator review."
        ),
    }
    errors = validate_payload(payload)
    errors.extend(validate_grounding(payload, strict=True))
    if errors:
        return None, errors
    return {
        "proposal": payload,
        "scalar_at_accept": 0.0,
        "artifact_schema_version": 1,
        "raw_source_exchange": source_exchange,
    }, []


def write_artifact_drafts(
    digest: dict[str, Any],
    *,
    accepted_dir: Path = SWARM_ACCEPTED_DIR,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    accepted_dir.mkdir(parents=True, exist_ok=True)
    for entry in digest.get("entries") or []:
        if entry.get("relationship_type") != "contradiction":
            continue
        artifact, errors = build_promotable_artifact(entry)
        if artifact is None:
            results.append(
                {
                    "candidate_id": entry["candidate_id"],
                    "artifact_path": None,
                    "promotable": False,
                    "errors": errors,
                }
            )
            continue
        artifact_path = accepted_dir / f"accepted-contradiction-{entry['candidate_id'].lower()}.json"
        artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
        results.append(
            {
                "candidate_id": entry["candidate_id"],
                "artifact_path": str(artifact_path),
                "promotable": True,
                "errors": [],
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a derived contradiction digest from recursion-gate.")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id (default: grace-mar)")
    parser.add_argument("--users-dir", type=Path, default=DEFAULT_USERS_DIR, help="Users directory root")
    parser.add_argument("--json", action="store_true", help="Emit the digest JSON to stdout")
    parser.add_argument("--write-derived", action="store_true", help="Write users/<id>/derived/contradictions digest")
    parser.add_argument(
        "--write-artifact-drafts",
        action="store_true",
        help="Write promotable contradiction artifact drafts under auto-research/swarm/accepted",
    )
    args = parser.parse_args()

    write_path = default_digest_path(users_dir=args.users_dir, user_id=args.user) if args.write_derived else None
    digest = generate_contradiction_digest(user_id=args.user, users_dir=args.users_dir, write_path=write_path)
    if args.write_artifact_drafts:
        digest["artifact_drafts"] = write_artifact_drafts(digest)
    if args.json:
        print(json.dumps(digest, indent=2))
    else:
        relation_counts = digest["relation_counts"]
        print(
            "contradiction digest "
            f"pending={digest['pending_candidate_count']} reviewable={digest['reviewable_count']} "
            f"duplicate={relation_counts['duplicate']} refinement={relation_counts['refinement']} "
            f"contradiction={relation_counts['contradiction']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
