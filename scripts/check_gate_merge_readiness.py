#!/usr/bin/env python3
"""Preflight checker for recursion-gate merge readiness.

Focuses on failure modes observed in bookshelf MCQ -> IX-A flows:
- placeholder suggested_entry
- missing IX-A scaffold in self.md
- missing topic anchor in source_exchange for IX-A candidates
- methodology-style wording in IX-A suggested_entry
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    yaml = None

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from gate_block_parser import pending_candidates_region, iter_candidate_yaml_blocks

PLACEHOLDER_RE = re.compile(r"see source_exchange\.operator \(staged paste\)", re.IGNORECASE)
HNSRC_RE = re.compile(r"^HNSRC-\d{4}$")
TOPIC_HINT_RE = re.compile(
    r"(\b\d{3,4}\s*(BCE|CE)?\b|Westphalia|Tanzimat|Fort Sumter|Barbarossa|Marathon|Qing|Ottoman|Decolonization|WWI|World War I|Thucydides|Melian|Mahan|Mearsheimer|deterrence|second-strike)",
    re.IGNORECASE,
)
METHOD_RE = re.compile(r"\b(method|workflow|process|how i work|curation as method|extraction channel)\b", re.IGNORECASE)
INTERNAL_ID_RE = re.compile(r"\b(HNSRC-\d{4}|LIB-\d{4})\b")


def yaml_get(body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", body, re.MULTILINE)
    return (m.group(1).strip().strip('"').strip("'")) if m else ""


def has_ix_a_scaffold(self_md: str) -> bool:
    pat = re.compile(r"#### Facts \(LEARN-nnn\)\s*\n\n```yaml\nentries:\s*\n", re.DOTALL)
    return bool(pat.search(self_md))


def _safe_yaml_load(body: str) -> dict:
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(body) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _load_catalog_ids(catalog_path: Path) -> set[str]:
    if yaml is None or not catalog_path.is_file():
        return set()
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return set()
    return {str(x.get("id")) for x in items if isinstance(x, dict) and x.get("id")}


def _load_anchor_refs(anchors_path: Path) -> set[str]:
    if yaml is None or not anchors_path.is_file():
        return set()
    data = yaml.safe_load(anchors_path.read_text(encoding="utf-8")) or {}
    anchors = data.get("anchors") if isinstance(data, dict) else None
    if not isinstance(anchors, list):
        return set()
    refs: set[str] = set()
    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        shelf_refs = anchor.get("shelf_refs") or []
        if isinstance(shelf_refs, list):
            refs.update(str(x) for x in shelf_refs if isinstance(x, str))
    return refs


def _is_bookshelf_quiz(data: dict, body: str) -> bool:
    channel = str(data.get("channel_key") or yaml_get(body, "channel_key"))
    signal = str(data.get("signal_type") or yaml_get(body, "signal_type"))
    return "bookshelf-mcq" in channel or signal == "operator_quiz_validated" or "quiz_receipt:" in body


def _visible_prompt_text(data: dict) -> str:
    qr = data.get("quiz_receipt")
    if not isinstance(qr, dict):
        return ""
    parts = [
        str(qr.get("visible_prompt") or ""),
        str(qr.get("question_stem") or ""),
        str(qr.get("citation_label") or ""),
    ]
    return "\n".join(x for x in parts if x)


def _receipt_binding_issues(
    cid: str,
    data: dict,
    *,
    catalog_ids: set[str],
    anchor_refs: set[str],
) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []

    shelf_refs = data.get("shelf_refs")
    if shelf_refs is None:
        shelf_refs = []
    if not isinstance(shelf_refs, list):
        blockers.append(f"{cid}: shelf_refs must be a list")
        shelf_refs = []

    refs = [str(x) for x in shelf_refs]
    weak = str(data.get("source_binding_strength") or "").lower() == "weak" or data.get("review_needed") is True
    if not refs:
        msg = f"{cid}: bookshelf MCQ missing shelf_refs"
        (warnings if weak else blockers).append(msg + (" (weak/review-needed)" if weak else ""))
    for ref in refs:
        if not HNSRC_RE.match(ref):
            blockers.append(f"{cid}: invalid shelf_ref {ref!r}")
        elif catalog_ids and ref not in catalog_ids:
            blockers.append(f"{cid}: unknown shelf_ref {ref}")
        elif anchor_refs and ref not in anchor_refs:
            warnings.append(f"{cid}: shelf_ref {ref} is not present in bookshelf-quiz-anchors.yaml")

    qr = data.get("quiz_receipt")
    if not isinstance(qr, dict):
        msg = f"{cid}: bookshelf MCQ missing structured quiz_receipt"
        (warnings if weak else blockers).append(msg + (" (weak/review-needed)" if weak else ""))
        return blockers, warnings

    for key in ("source_kind", "citation_label", "stem_topic", "selected_answer", "correct_answer", "validation_note", "staged_claim"):
        if not str(qr.get(key) or "").strip():
            warnings.append(f"{cid}: quiz_receipt missing {key}")

    if INTERNAL_ID_RE.search(_visible_prompt_text(data)):
        blockers.append(f"{cid}: visible quiz prompt/citation leaks internal source ids")

    return blockers, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero when any blocker exists")
    ap.add_argument("--gate", type=Path, default=None, help="Explicit recursion-gate.md path")
    ap.add_argument("--self", dest="self_path", type=Path, default=None, help="Explicit self.md path")
    ap.add_argument(
        "--catalog",
        type=Path,
        default=REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "research" / "bookshelf-catalog.yaml",
    )
    ap.add_argument(
        "--quiz-anchors",
        type=Path,
        default=REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "research" / "bookshelf-quiz-anchors.yaml",
    )
    args = ap.parse_args()

    gate_path = args.gate or (REPO / "users" / args.user / "recursion-gate.md")
    self_path = args.self_path or (REPO / "users" / args.user / "self.md")
    if not gate_path.is_file():
        print(f"ERROR: missing gate file: {gate_path}")
        return 1
    if not self_path.is_file():
        print(f"ERROR: missing self file: {self_path}")
        return 1

    gate = gate_path.read_text(encoding="utf-8")
    self_md = self_path.read_text(encoding="utf-8")

    blockers: list[str] = []
    warnings: list[str] = []

    if not has_ix_a_scaffold(self_md):
        blockers.append("self.md IX-A scaffold missing `Facts (LEARN-nnn)` entries block")
    catalog_ids = _load_catalog_ids(args.catalog)
    anchor_refs = _load_anchor_refs(args.quiz_anchors)

    region = pending_candidates_region(gate)
    pending = list(iter_candidate_yaml_blocks(region))
    if not pending:
        print("ok: no pending candidates in gate")
        return 0

    for cid, title, body in pending:
        data = _safe_yaml_load(body)
        profile_target = yaml_get(body, "profile_target").upper()
        suggested = yaml_get(body, "suggested_entry")

        if not suggested:
            blockers.append(f"{cid}: missing suggested_entry")
        elif PLACEHOLDER_RE.search(suggested):
            blockers.append(f"{cid}: placeholder suggested_entry")

        if "IX-A" in profile_target:
            if not TOPIC_HINT_RE.search(body):
                warnings.append(f"{cid}: IX-A candidate has weak/absent explicit topic anchor")
            if METHOD_RE.search(suggested):
                blockers.append(f"{cid}: IX-A suggested_entry appears methodology-framed")
            if _is_bookshelf_quiz(data, body):
                b2, w2 = _receipt_binding_issues(
                    cid,
                    data,
                    catalog_ids=catalog_ids,
                    anchor_refs=anchor_refs,
                )
                blockers.extend(b2)
                warnings.extend(w2)

    print(f"pending candidates checked: {len(pending)}")
    if warnings:
        print("warnings:")
        for w in warnings:
            print(f"- {w}")
    if blockers:
        print("blockers:")
        for b in blockers:
            print(f"- {b}")
        return 1 if args.strict else 0

    print("ok: pending candidates pass merge-readiness checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
