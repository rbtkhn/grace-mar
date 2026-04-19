#!/usr/bin/env python3
"""
Validate docs/skill-work/work-strategy/strategy-notebook/strategy-expert-predictions.md:
  - expert_id in the main roster table of strategy-commentator-threads.md (not other tables)
  - topic_slug in the numbered prediction-topic registry (+ EXTENDED_TOPIC_SLUGS)
  - pred_id rows: expert_id and topic_slug recognized

Exit 0 if OK; stderr + exit 1 on error.
WORK-only artifact; not Record.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO / "docs/skill-work/work-strategy/strategy-notebook"
THREADS = NOTEBOOK / "strategy-commentator-threads.md"
PREDICTIONS = NOTEBOOK / "strategy-expert-predictions.md"

# Documented in predictions file but not necessarily in the numbered top-10 table.
EXTENDED_TOPIC_SLUGS = frozenset({"rome-legitimacy"})

ROSTER_END = "**Special routing rule — Predictive History:**"

RE_ROSTER_ROW = re.compile(r"^\|\s*`([a-z0-9_-]+)`\s*\|")
RE_REGISTRY_SLUG = re.compile(r"^\|\s*\d+\s*\|\s*`([a-z0-9-]+)`\s*\|")
RE_PRED_ROW = re.compile(
    r"^\|\s*`(pred-[^`]+)`\s*\|\s*`([a-z0-9_-]+)`\s*\|\s*`([a-z0-9-]+)`\s*\|",
    re.MULTILINE,
)


def extract_main_roster_block(text: str) -> str:
    """Slice the Name/Role roster table only (avoids deprecated topic-slug rows, etc.)."""
    needle = "| expert_id | Name | Role (one line) |"
    start = text.find(needle)
    if start == -1:
        print(
            "validate_expert_predictions: could not find main expert roster header "
            f"({needle!r}) in strategy-commentator-threads.md",
            file=sys.stderr,
        )
        sys.exit(1)
    end = text.find(ROSTER_END, start)
    if end == -1:
        print(
            "validate_expert_predictions: could not find roster end anchor after main table",
            file=sys.stderr,
        )
        sys.exit(1)
    return text[start:end]


def load_expert_ids() -> set[str]:
    text = extract_main_roster_block(THREADS.read_text(encoding="utf-8"))
    ids: set[str] = set()
    for line in text.splitlines():
        m = RE_ROSTER_ROW.match(line)
        if m:
            ids.add(m.group(1))
    if not ids:
        print(
            "validate_expert_predictions: no expert_id rows parsed from main roster table",
            file=sys.stderr,
        )
        sys.exit(1)
    return ids


def load_registry_topic_slugs() -> set[str]:
    text = PREDICTIONS.read_text(encoding="utf-8")
    slugs: set[str] = set()
    for line in text.splitlines():
        m = RE_REGISTRY_SLUG.match(line)
        if m:
            slugs.add(m.group(1))
    slugs |= EXTENDED_TOPIC_SLUGS
    if len(slugs) < 5:
        print(
            "validate_expert_predictions: too few topic_slug rows in prediction-topic registry",
            file=sys.stderr,
        )
        sys.exit(1)
    return slugs


def validate_pred_rows(expert_ids: set[str], topic_slugs: set[str]) -> None:
    text = PREDICTIONS.read_text(encoding="utf-8")
    errors: list[str] = []
    for m in RE_PRED_ROW.finditer(text):
        pred_id, eid, tid = m.group(1), m.group(2), m.group(3)
        if eid not in expert_ids:
            errors.append(f"unknown expert_id `{eid}` in row `{pred_id}`")
        if tid not in topic_slugs:
            errors.append(
                f"unknown topic_slug `{tid}` in row `{pred_id}` "
                "(append to registry table or add slug to EXTENDED_TOPIC_SLUGS in this script)"
            )
    if errors:
        for e in errors:
            print(f"validate_expert_predictions: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    if not PREDICTIONS.is_file():
        print(f"validate_expert_predictions: missing {PREDICTIONS}", file=sys.stderr)
        sys.exit(1)
    if not THREADS.is_file():
        print(f"validate_expert_predictions: missing {THREADS}", file=sys.stderr)
        sys.exit(1)
    expert_ids = load_expert_ids()
    topic_slugs = load_registry_topic_slugs()
    validate_pred_rows(expert_ids, topic_slugs)
    print(
        "validate_expert_predictions: OK "
        f"({len(topic_slugs)} topic slugs, {len(expert_ids)} roster expert ids)"
    )


if __name__ == "__main__":
    main()
