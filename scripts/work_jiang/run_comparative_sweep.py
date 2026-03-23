#!/usr/bin/env python3
"""
Comparative sweep: summarize new analysis JSON sidecars vs claims registry; emit operator memo + gate staging YAML.
Does not call LLMs by default. Does not merge into recursion-gate.md automatically.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
_WJ_SCRIPTS = ROOT / "scripts" / "work_jiang"
if str(_WJ_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_WJ_SCRIPTS))
STATE_PATH = WORK_DIR / "metadata" / "comparative_sweep_state.yaml"
ANALYSIS_DIR = WORK_DIR / "analysis"
CLAIMS_PATH = WORK_DIR / "claims" / "registry" / "claims.jsonl"
GATE_STAGING = ROOT / "users" / "grace-mar" / "recursion-gate-staging"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def find_analysis_json_files() -> list[Path]:
    if not ANALYSIS_DIR.exists():
        return []
    return sorted(ANALYSIS_DIR.glob("*-analysis.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print paths only")
    parser.add_argument("--since", type=str, default="", help="Only include files modified after this ISO date (optional)")
    args = parser.parse_args()

    state: dict = {}
    if STATE_PATH.exists():
        state = yaml.safe_load(STATE_PATH.read_text(encoding="utf-8")) or {}

    files = find_analysis_json_files()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts_full = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    claims = load_jsonl(CLAIMS_PATH)
    claim_ids = {c.get("claim_id") for c in claims if c.get("claim_id")}

    from extractors.registry import instantiate_extractor

    sections: list[str] = [
        f"# Comparative sweep — {ts}",
        "",
        f"- **generated_at_utc:** {ts_full}",
        "- **operator lane:** not Record until gated",
        "",
        "## Extractor dispatch (registry)",
        "",
    ]
    for p in files:
        try:
            doc0 = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        src = doc0.get("source") or {}
        ex = instantiate_extractor(
            series_id=(src.get("series") or None),
            source_id=(src.get("source_id") or None),
        )
        sections.append(f"- `{p.name}` → **{ex.__class__.__name__}** (`{ex.series_id}`)")
    sections += ["", "## Analysis JSON files scanned", "",]
    for p in files:
        sections.append(f"- `{p.relative_to(ROOT)}`")

    sections += ["", "## Cross-check vs claims registry", "", f"- **claim_ids loaded:** {len(claim_ids)}", ""]

    for p in files:
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            sections.append(f"### {p.name} — **parse error:** {e}")
            continue
        preds = doc.get("predictions") or []
        kc = doc.get("key_claims") or []
        sections.append(f"### {p.name}")
        sections.append(f"- **summary (snippet):** {(doc.get('summary') or '')[:200]}…")
        sections.append(f"- **key_claims:** {len(kc)} | **predictions:** {len(preds)}")
        sections.append("")

    out_md = WORK_DIR / "analysis" / f"comparative-sweep-{ts}.md"
    gate_yaml = GATE_STAGING / f"work-jiang-sweep-{ts}.yaml"

    gate_body = "\n".join(
        [
            f"# Draft gate blocks — work-jiang sweep {ts}",
            "# Paste into recursion-gate.md Candidates after review.",
            "",
            "blocks:",
            "  - id: work-jiang-sweep-placeholder",
            "    channel_key: operator:work-jiang",
            "    priority_score: 8",
            "    summary: Comparative sweep generated; replace with concrete SELF/SELF-LIBRARY candidates after review.",
            "    territory: companion",
            "    status: draft_not_for_merge",
        ]
    )

    if args.dry_run:
        print(f"Would write: {out_md}")
        print(f"Would write: {gate_yaml}")
        return 0

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(sections) + "\n", encoding="utf-8")
    GATE_STAGING.mkdir(parents=True, exist_ok=True)
    gate_yaml.write_text(gate_body + "\n", encoding="utf-8")

    state["last_sweep_at_utc"] = ts_full
    state["last_source_id_processed"] = state.get("last_source_id_processed")
    STATE_PATH.write_text(yaml.safe_dump(state, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"Wrote {out_md}")
    print(f"Wrote {gate_yaml}")
    print(f"Updated {STATE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
