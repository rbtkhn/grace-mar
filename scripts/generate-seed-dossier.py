#!/usr/bin/env python3
"""
Generate seed_dossier.md from seed JSON artifacts in a directory.

Usage:
  python3 scripts/generate-seed-dossier.py users/demo/seed-phase
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

JSON_FILES = [
    "seed-phase-manifest.json",
    "seed_intake.json",
    "seed_identity.json",
    "seed_curiosity.json",
    "seed_pedagogy.json",
    "seed_expression.json",
    "seed_memory_contract.json",
    "seed_trial_report.json",
    "seed_readiness.json",
    "seed_confidence_map.json",
    "work_business_seed.json",
    "work_dev_seed.json",
]


def load_dir(d: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in JSON_FILES:
        p = d / name
        if not p.is_file():
            raise FileNotFoundError(p)
        out[name] = json.loads(p.read_text(encoding="utf-8"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", type=Path)
    args = ap.parse_args()
    target = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    data = load_dir(target)

    mid = data["seed_identity.json"].get("identity", {})
    rd = data["seed_readiness.json"].get("readiness", {})
    cm = data["seed_confidence_map.json"].get("confidence_map", {})
    man = data["seed-phase-manifest.json"]
    cadence = data["seed_intake.json"].get("cadence_preference", {})

    lines = [
        "# Seed Dossier",
        "",
        f"**user_slug:** {data['seed_readiness.json'].get('user_slug', '')}",
        "",
        "## Status",
        "",
        f"Manifest status: **{man.get('status', '')}**. Readiness decision: **{rd.get('decision', '')}** (score {rd.get('readiness_score', '')}).",
        "",
    ]
    if cadence:
        rename_offer = cadence.get("rename_offer", {})
        thresholds = []
        if rename_offer.get("offer_after_successful_uses") is not None:
            thresholds.append(f"{rename_offer['offer_after_successful_uses']} successful uses")
        if rename_offer.get("offer_after_distinct_days") is not None:
            thresholds.append(f"{rename_offer['offer_after_distinct_days']} distinct days")
        if rename_offer.get("minimum_successful_followthrough_uses") is not None:
            thresholds.append(
                f"{rename_offer['minimum_successful_followthrough_uses']} successful follow-through uses"
            )
        lines.extend(
            [
                "## Cadence Ritual",
                "",
                f"Default **{cadence.get('default_trigger_word', 'coffee')}**; active **{cadence.get('active_trigger_word', 'coffee')}**; "
                f"source **{cadence.get('word_source', 'default')}**.",
                "",
                f"Personalization timing **{cadence.get('personalization_timing', 'post_adoption_optional')}**; "
                f"rename offer status **{rename_offer.get('status', 'not_yet_eligible')}**.",
            ]
        )
        if thresholds:
            lines.extend(["", "Offer threshold: " + "; ".join(thresholds) + "."])
        lines.append("")
    lines.extend(["## Stage Progress", ""])
    for s in man.get("stages", []):
        lines.append(f"- **{s.get('id')}**: {s.get('status')}")
    lines.extend(
        [
            "",
            "## Identity Summary",
            "",
            f"**{mid.get('companion_name', '')}** — {mid.get('role_definition', '')}",
            "",
            "## Curiosity Summary",
            "",
        ]
    )
    cur = data["seed_curiosity.json"].get("curiosity", {})
    lines.append(", ".join(cur.get("domains", [])) or "—")
    lines.extend(["", "## Pedagogy Summary", ""])
    ped = data["seed_pedagogy.json"].get("pedagogy", {})
    lines.append(ped.get("explanation_style", "—"))
    lines.extend(["", "## Expression Summary", ""])
    ex = data["seed_expression.json"].get("expression", {})
    lines.append(ex.get("writing_cadence", "—"))
    lines.extend(["", "## Memory Governance Summary", ""])
    mem = data["seed_memory_contract.json"].get("memory_contract", {})
    lines.append(", ".join(mem.get("memory_classes", [])) or "—")
    lines.extend(
        [
            "",
            "## Confidence Map",
            "",
            f"Overall **{cm.get('overall', '')}**.",
            "",
            "## Work dev context",
            "",
        ]
    )
    wd = data["work_dev_seed.json"]
    lines.append(
        f"Status **{wd.get('status', '')}**; involvement **{wd.get('development_involvement', '')}**; "
        f"evidence_basis **{wd.get('evidence_basis', '')}**."
    )
    if wd.get("active_focuses"):
        lines.append("")
        lines.append("Focuses: " + "; ".join(wd["active_focuses"]))
    if wd.get("notes"):
        lines.extend(["", wd["notes"].strip()])
    lines.extend(
        [
            "",
            "## Work business context",
            "",
        ]
    )
    wb = data["work_business_seed.json"]
    lines.append(
        f"Status **{wb.get('status', '')}**; involvement **{wb.get('business_involvement', '')}**; "
        f"evidence_basis **{wb.get('evidence_basis', '')}**."
    )
    if wb.get("active_focuses"):
        lines.append("")
        lines.append("Focuses: " + "; ".join(wb["active_focuses"]))
    if wb.get("notes"):
        lines.extend(["", wb["notes"].strip()])
    lines.extend(
        [
            "",
            "## Blocking Issues",
            "",
        ]
    )
    for issue in rd.get("blocking_issues", []):
        lines.append(f"- {issue}")
    if not rd.get("blocking_issues"):
        lines.append("- None")
    lines.extend(["", "## Recommended Next Actions", ""])
    for a in rd.get("recommended_next_actions", []):
        lines.append(f"- {a}")
    if not rd.get("recommended_next_actions"):
        lines.append("- —")
    lines.extend(["", "## Activation Recommendation", ""])
    dec = rd.get("decision", "fail")
    if dec == "pass":
        lines.append("**Pass** — eligible for activation per operator policy.")
    elif dec == "conditional_pass":
        lines.append("**Conditional pass** — activate only with documented follow-ups.")
    else:
        lines.append("**Do not activate** until blocking issues are resolved.")

    out_path = target / "seed_dossier.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        shown_path = out_path.relative_to(REPO_ROOT)
    except ValueError:
        shown_path = out_path
    print(f"Wrote {shown_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
