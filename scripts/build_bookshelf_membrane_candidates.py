#!/usr/bin/env python3
"""Build bookshelf membrane quiz rounds and claim-first candidate drafts.

WORK-only helper for Coffee E self-knowledge quiz sessions.
Generates deterministic MCQ rounds and emits:
- BOOKSHELF-MEMBRANE-REPORT.md
- BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md

Primary decision path is claim quality and evidence fitness, not numeric optimization.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")


REPO = Path(__file__).resolve().parent.parent
CATALOG_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
ROUND_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-membrane-round.json"
)
RESPONSES_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-membrane-responses.json"
)
REPORT_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "BOOKSHELF-MEMBRANE-REPORT.md"
)
DRAFTS_PATH = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md"
)

MIN_ROUND_SIZE = 5
MAX_ROUND_SIZE = 10

OPTION_STANCE = {
    "enduring-core": "enduring",
    "active-focus": "active",
    "light-interest": "context",
    "not-now": "deferred",
}


@dataclass
class TagCluster:
    tag: str
    ids: list[str]
    authors: set[str]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _load_catalog(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _build_clusters(catalog: dict[str, Any]) -> list[TagCluster]:
    rows = catalog.get("items") or []
    by_tag: dict[str, TagCluster] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("id") or "").strip()
        author = str(row.get("author") or "Unknown").strip() or "Unknown"
        tags = row.get("tags") or []
        if not rid or not isinstance(tags, list):
            continue
        for raw_tag in tags:
            if not isinstance(raw_tag, str):
                continue
            tag = raw_tag.strip()
            if not tag:
                continue
            lowered = tag.lower()
            if (
                "shelf photo" in lowered
                or "batch" in lowered
                or re.search(r"\b20\d{2}\b", lowered)
            ):
                continue
            cluster = by_tag.setdefault(tag, TagCluster(tag=tag, ids=[], authors=set()))
            cluster.ids.append(rid)
            cluster.authors.add(author)
    clusters = []
    for cluster in by_tag.values():
        unique_ids = sorted(set(cluster.ids))
        if len(unique_ids) < 2:
            continue
        clusters.append(TagCluster(tag=cluster.tag, ids=unique_ids, authors=cluster.authors))
    clusters.sort(key=lambda c: (-len(c.ids), c.tag.lower()))
    return clusters


def _generate_round(clusters: list[TagCluster], round_index: int, round_size: int) -> dict[str, Any]:
    if not clusters:
        raise ValueError("No tag clusters available in catalog.")
    if round_size < MIN_ROUND_SIZE or round_size > MAX_ROUND_SIZE:
        raise ValueError(f"round_size must be {MIN_ROUND_SIZE}-{MAX_ROUND_SIZE}")
    start = ((round_index - 1) * round_size) % len(clusters)
    selected = [clusters[(start + i) % len(clusters)] for i in range(round_size)]
    questions: list[dict[str, Any]] = []
    for i, cluster in enumerate(selected, start=1):
        qid = f"q{i:02d}-{_slug(cluster.tag)}"
        questions.append(
            {
                "id": qid,
                "tag": cluster.tag,
                "prompt": f'Which option best matches your current relationship to the "{cluster.tag}" subject cluster?',
                "support_ids": cluster.ids[:8],
                "support_authors_count": len(cluster.authors),
                "options": [
                    {
                        "id": "enduring-core",
                        "label": "This is a durable core lens I actively carry.",
                    },
                    {
                        "id": "active-focus",
                        "label": "This is active right now and shaping current thinking.",
                    },
                    {
                        "id": "light-interest",
                        "label": "Useful context, but not a current self-defining focus.",
                    },
                    {
                        "id": "not-now",
                        "label": "Not a present focus in this phase.",
                    },
                ],
            }
        )
    return {
        "round_index": round_index,
        "round_size": round_size,
        "questions": questions,
        "continue_prompt": "Continue to another round or stop and emit session summary?",
    }


def _load_responses(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("responses file must be a JSON object")
    rounds = data.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("responses file must include non-empty rounds[]")
    return data


def _claim_line(tag: str, stance: str) -> str:
    if stance == "enduring":
        return (
            f"Sustained engagement with {tag} is part of how knowledge is organized and interpreted "
            "across sessions."
        )
    if stance == "active":
        return (
            f"{tag} is a live knowledge track in the current phase and should remain explicit in the "
            "self-knowledge map."
        )
    if stance == "context":
        return (
            f"{tag} is supportive context knowledge right now, useful but not currently a primary "
            "organizing track."
        )
    return f"{tag} is currently a deferred track rather than an active self-knowledge focus."


def _tier_for_claim(*, stance: str, evidence_count: int, authors_count: int, affirmed_tags: int) -> str:
    if stance == "deferred":
        return "low"
    if stance == "enduring" and evidence_count >= 4 and authors_count >= 4:
        return "high" if affirmed_tags >= 3 else "medium"
    if stance == "active" and evidence_count >= 3 and authors_count >= 3:
        return "medium"
    if stance == "context" and evidence_count >= 2:
        return "low"
    return "low"


def _extract_claims(clusters: list[TagCluster], responses: dict[str, Any], round_size: int) -> dict[str, Any]:
    cluster_by_tag = {c.tag: c for c in clusters}
    claims: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    affirmed_tags: set[str] = set()
    rows: list[dict[str, Any]] = []

    for block in responses.get("rounds") or []:
        if not isinstance(block, dict):
            continue
        round_index = int(block.get("round_index", 1))
        expected = _generate_round(clusters, round_index=round_index, round_size=round_size)
        question_map = {q["id"]: q for q in expected["questions"]}
        for answer in block.get("answers") or []:
            if not isinstance(answer, dict):
                continue
            qid = str(answer.get("question_id") or "").strip()
            option_id = str(answer.get("option_id") or "").strip()
            question = question_map.get(qid)
            if not question:
                continue
            stance = OPTION_STANCE.get(option_id, "deferred")
            cluster = cluster_by_tag.get(question["tag"])
            support_ids = list(question.get("support_ids") or [])
            authors_count = len(cluster.authors) if cluster else 0
            evidence_count = len(support_ids)
            if stance != "deferred":
                affirmed_tags.add(question["tag"])
            rows.append(
                {
                    "round_index": round_index,
                    "question_id": qid,
                    "tag": question["tag"],
                    "option_id": option_id,
                    "stance": stance,
                    "support_ids": support_ids,
                }
            )
            claim = {
                "round_index": round_index,
                "tag": question["tag"],
                "question_id": qid,
                "stance": stance,
                "proposed_statement": _claim_line(question["tag"], stance),
                "evidence_ids": support_ids,
                "evidence_count": evidence_count,
                "authors_count": authors_count,
            }
            if stance == "deferred":
                claim["tier"] = "low"
                deferred.append(claim)
                continue
            claims.append(claim)

    for claim in claims:
        claim["tier"] = _tier_for_claim(
            stance=claim["stance"],
            evidence_count=claim["evidence_count"],
            authors_count=claim["authors_count"],
            affirmed_tags=len(affirmed_tags),
        )

    high = [c for c in claims if c["tier"] == "high"]
    medium = [c for c in claims if c["tier"] == "medium"]
    low = [c for c in claims if c["tier"] == "low"]
    accepted = high + medium

    return {
        "rows": rows,
        "accepted_claims": accepted,
        "deferred_claims": deferred + low,
        "all_claims": claims + deferred,
        "affirmed_tags": sorted(affirmed_tags),
        "tier_counts": {
            "high": len(high),
            "medium": len(medium),
            "low": len(low) + len(deferred),
        },
    }


def _render_report(responses_path: Path, extracted: dict[str, Any], round_size: int) -> str:
    tier_counts = extracted["tier_counts"]
    lines = [
        "# Bookshelf membrane report (generated)",
        "",
        "**Do not edit by hand.**",
        "Regenerate: `python3 scripts/build_bookshelf_membrane_candidates.py --responses-file <path>`",
        "",
        "## Session summary",
        "",
        f"- Source responses: `{responses_path}`",
        f"- Round size contract: `{round_size}` questions per round",
        f"- Affirmed subject tags: `{len(extracted['affirmed_tags'])}`",
        f"- Claim decisions: high `{tier_counts['high']}`, medium `{tier_counts['medium']}`, low/deferred `{tier_counts['low']}`",
        "- Decision rule: claim specificity and evidence fitness, not numeric ranking.",
        "",
        "## Claim ledger",
        "",
        "| Round | Tag | Selection | Proposed self-knowledge statement | Tier | Evidence IDs |",
        "|---:|---|---|---|---|---|",
    ]
    for row in extracted["all_claims"]:
        lines.append(
            f"| {row['round_index']} | {row['tag']} | `{row['stance']}` | {row['proposed_statement']} | "
            f"`{row['tier']}` | {', '.join(f'`{x}`' for x in row['evidence_ids'][:4])} |"
        )
    lines.extend(
        [
            "",
            "## Accepted for draft promotion (high/medium)",
            "",
        ]
    )
    if not extracted["accepted_claims"]:
        lines.append("- *(none)*")
    for claim in extracted["accepted_claims"]:
        lines.append(
            f"- `{claim['tag']}` (`{claim['tier']}`): {claim['proposed_statement']} "
            f"(evidence: {', '.join(claim['evidence_ids'][:4])})"
        )
    lines.extend(
        [
            "",
            "## Deferred or low-confidence claims",
            "",
        ]
    )
    if not extracted["deferred_claims"]:
        lines.append("- *(none)*")
    for claim in extracted["deferred_claims"]:
        lines.append(f"- `{claim['tag']}`: {claim['proposed_statement']}")
    lines.extend(
        [
            "",
            "## Continue control",
            "",
            "If continuing, append next round to `rounds[]` in responses JSON and rerun.",
            "If stopping, use this report + draft file for companion review.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_drafts(extracted: dict[str, Any], session_id: str) -> str:
    lines = [
        "# Bookshelf membrane candidate drafts (generated)",
        "",
        "**Draft-only.** Not auto-merged. Do not paste into gate without companion review.",
        "",
    ]
    accepted = extracted["accepted_claims"]
    if not accepted:
        lines.extend(
            [
                "No high/medium claims were promoted this run.",
                "",
                "Use another round or refine answer selections before staging gate-ready drafts.",
                "",
            ]
        )
        return "\n".join(lines)

    for idx, claim in enumerate(accepted, start=1):
        cid = f"CANDIDATE-{9700 + idx:04d}"
        summary = f"{claim['tag']} appears as a {claim['tier']}-confidence self-knowledge pattern."
        if claim["tier"] == "high":
            summary = f"{claim['tag']} is a stable self-knowledge pattern with broad shelf support."
        elif claim["tier"] == "medium":
            summary = f"{claim['tag']} is an active self-knowledge pattern with bounded evidence support."
        lines.extend(
            [
                f"## {cid}",
                "",
                "```yaml",
                f"id: {cid}",
                "status: pending",
                f"summary: \"{summary}\"",
                "kind: self_knowledge_refinement",
                "profile_target_suggestion: ix-b",
                f"session_id: {session_id}",
                f"tier: {claim['tier']}",
                f"proposed_statement: \"{claim['proposed_statement']}\"",
                "evidence:",
            ]
        )
        for sid in claim["evidence_ids"][:8]:
            lines.append(f"  - {sid}")
        if not claim["evidence_ids"]:
            lines.append("  - none")
        lines.extend(
            [
                "rationale: |",
                "  Draft grounded in explicit companion selection and shelf-linked evidence.",
                f"  Stance={claim['stance']}, evidence_count={claim['evidence_count']}, authors_count={claim['authors_count']}.",
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def _ensure_match(path: Path, expected: str) -> int:
    if not path.is_file():
        print(f"CHECK: missing {path}", file=sys.stderr)
        return 1
    current = path.read_text(encoding="utf-8")
    if current != expected:
        print(f"CHECK: stale {path}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    ap.add_argument("--responses-file", type=Path, default=RESPONSES_PATH)
    ap.add_argument("--round-out", type=Path, default=ROUND_PATH)
    ap.add_argument("--report-out", type=Path, default=REPORT_PATH)
    ap.add_argument("--drafts-out", type=Path, default=DRAFTS_PATH)
    ap.add_argument("--round-index", type=int, default=1)
    ap.add_argument("--round-size", type=int, default=7)
    ap.add_argument("--session-id", default="bookshelf-membrane-session")
    ap.add_argument("--emit-round", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not args.catalog.is_file():
        print(f"ERROR: missing catalog file: {args.catalog}", file=sys.stderr)
        return 1
    if args.round_size < MIN_ROUND_SIZE or args.round_size > MAX_ROUND_SIZE:
        print(f"ERROR: --round-size must be between {MIN_ROUND_SIZE} and {MAX_ROUND_SIZE}", file=sys.stderr)
        return 1

    clusters = _build_clusters(_load_catalog(args.catalog))
    if not clusters:
        print("ERROR: no usable tag clusters found in catalog", file=sys.stderr)
        return 1

    if args.emit_round:
        round_payload = _generate_round(clusters, round_index=args.round_index, round_size=args.round_size)
        rendered = json.dumps(round_payload, indent=2) + "\n"
        if args.check:
            return _ensure_match(args.round_out, rendered)
        args.round_out.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.round_out}")
        return 0

    if not args.responses_file.is_file():
        print(f"ERROR: missing responses file: {args.responses_file}", file=sys.stderr)
        return 1
    responses = _load_responses(args.responses_file)
    extracted = _extract_claims(clusters, responses, round_size=args.round_size)
    report = _render_report(args.responses_file, extracted, round_size=args.round_size)
    drafts = _render_drafts(extracted, session_id=args.session_id)

    if args.check:
        rc1 = _ensure_match(args.report_out, report)
        rc2 = _ensure_match(args.drafts_out, drafts)
        if rc1 or rc2:
            print("Run: python3 scripts/build_bookshelf_membrane_candidates.py --responses-file <path>", file=sys.stderr)
            return 1
        print("ok: bookshelf membrane artifacts up to date")
        return 0

    args.report_out.write_text(report + ("\n" if not report.endswith("\n") else ""), encoding="utf-8")
    args.drafts_out.write_text(drafts + ("\n" if not drafts.endswith("\n") else ""), encoding="utf-8")
    print(f"wrote {args.report_out}")
    print(f"wrote {args.drafts_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
