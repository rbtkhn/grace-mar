"""Validate concept dictionary, claims ledger, thesis links, and evidence packs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from arch_chapters import chapters_for_volume_block, top_level_chapters  # noqa: E402


def _evidence_pack_volume_branch(chapter_id: str) -> str:
    if chapter_id.startswith("civ-ch"):
        return "civ"
    if chapter_id.startswith("sh-ch"):
        return "sh"
    if chapter_id.startswith("gt-ch"):
        return "gt"
    return "geo"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_claims() -> list[dict]:
    p = WORK_DIR / "claims" / "registry" / "claims.jsonl"
    if not p.exists():
        return []
    rows = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    errors: list[str] = []

    thesis = load_yaml(WORK_DIR / "metadata" / "thesis-map.yaml").get("thesis") or {}
    subclaims = thesis.get("subclaims") or []
    claim_rows = load_claims()
    claim_by_id = {r["claim_id"]: r for r in claim_rows if r.get("claim_id")}

    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources") or []
    src_by = {s["source_id"]: s for s in sources}

    for sc in subclaims:
        sid = sc.get("id")
        lc = sc.get("linked_claim_ids") or []
        if not lc:
            errors.append(f"Thesis subclaim {sid} has no linked_claim_ids")
        for cid in lc:
            if cid not in claim_by_id:
                errors.append(f"Thesis {sid} references unknown claim_id {cid}")

    for r in claim_rows:
        cid = r.get("claim_id")
        src = r.get("source_id")
        if not src:
            errors.append(f"Claim {cid} missing source_id")
            continue
        if src not in src_by:
            errors.append(f"Claim {cid} unknown source_id {src}")
        st = r.get("status") or ""
        ana = r.get("analysis_id")
        reg = src_by.get(src) if src in src_by else {}
        analysis_complete = (reg.get("status") or {}).get("analysis") == "complete"
        if st == "supported" and analysis_complete and not ana:
            errors.append(f"Claim {cid} marked supported but analysis_id empty while source has analysis")

    arch = load_yaml(WORK_DIR / "metadata" / "book-architecture.yaml")
    # Evidence-pack checks: Volume I + II + III (not Volume IV/VII YAML stubs).
    chapters = (
        top_level_chapters(arch)
        + chapters_for_volume_block(arch, "volume_2_civilization")
        + chapters_for_volume_block(arch, "volume_3_secret_history")
        + chapters_for_volume_block(arch, "volume_4_game_theory")
    )
    for ch in chapters:
        cid = ch.get("id")
        if not cid:
            continue
        pack = WORK_DIR / "evidence-packs" / f"{cid}.md"
        status = (ch.get("status") or "").strip()
        branch = _evidence_pack_volume_branch(cid)
        nested = branch in ("civ", "sh", "gt")
        # Nested volumes: outline_pending packs are scaffold-only (no claims yet).
        if nested and status == "outline_pending":
            if not pack.exists():
                errors.append(f"Missing evidence pack for {cid}: {pack.relative_to(WORK_DIR)}")
            continue

        if not pack.exists():
            errors.append(f"Missing evidence pack for {cid}: {pack.relative_to(WORK_DIR)}")
        text = pack.read_text(encoding="utf-8") if pack.exists() else ""
        if branch == "civ":
            for m in re.findall(r"`(civ-\d\d)`", text):
                if m not in src_by:
                    errors.append(f"Evidence pack {cid} references unknown source {m}")
            if text and len(re.findall(r"`civ-\d\d`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no civ source ids (expected at least one)")
        elif branch == "sh":
            for m in re.findall(r"`(sh-\d\d)`", text):
                if m not in src_by:
                    errors.append(f"Evidence pack {cid} references unknown source {m}")
            if text and len(re.findall(r"`sh-\d\d`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no sh source ids (expected at least one)")
        elif branch == "gt":
            for m in re.findall(r"`(gt-\d\d)`", text):
                if m not in src_by:
                    errors.append(f"Evidence pack {cid} references unknown source {m}")
            if text and len(re.findall(r"`gt-\d\d`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no gt source ids (expected at least one)")
        else:
            for m in re.findall(r"`(geo-\d\d)`", text):
                if m not in src_by:
                    errors.append(f"Evidence pack {cid} references unknown source {m}")
            if text and len(re.findall(r"`geo-\d\d`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no source ids (expected at least one)")
        for m in re.findall(r"`(clm-\d+)`", text):
            if m not in claim_by_id:
                errors.append(f"Evidence pack {cid} references unknown claim {m}")
        claims_deferred = "none with chapter_candidates" in text
        if text and not nested:
            if not claims_deferred and len(re.findall(r"`clm-\d+`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no claim ids (expected at least one)")
        if text and nested and status != "outline_pending":
            if not claims_deferred and len(re.findall(r"`clm-\d+`", text)) < 1:
                errors.append(f"Evidence pack {cid} lists no claim ids (expected at least one)")

    claim_chapter_gaps = [r for r in claim_rows if not r.get("chapter_candidates")]
    for r in claim_chapter_gaps:
        errors.append(f"Claim {r.get('claim_id')} missing chapter_candidates")

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
