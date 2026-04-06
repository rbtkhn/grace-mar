#!/usr/bin/env python3
"""
Synthesize seed_constitution.json from existing seed-phase JSON scaffolds.

Deterministic (no LLM). Run after strict validation succeeds:
  python3 scripts/validate-seed-phase.py <dir>
  python3 scripts/generate-constitution.py <dir>
  python3 scripts/validate-constitution.py <dir>

Does not modify other artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

from seed_phase_artifacts import SCHEMA_BY_FILE

# Inputs (all strict seed JSON except the constitution output itself).
SCAFFOLD_FILES = [k for k in SCHEMA_BY_FILE if k != "seed_constitution.json"]


def _load_seed_dir(seed_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in SCAFFOLD_FILES:
        p = seed_dir / name
        if not p.is_file():
            raise FileNotFoundError(f"Missing {p}")
        out[name] = json.loads(p.read_text(encoding="utf-8"))
    return out


def _source_scaffolds(data: dict[str, dict]) -> dict[str, str]:
    keys = [k.replace(".json", "") for k in SCAFFOLD_FILES]
    return {k: "referenced" for k in keys}


def _build_principles(data: dict[str, dict]) -> list[dict]:
    intent = data.get("seed_intent.json") or {}
    purpose = (intent.get("companion_purpose") or "").strip()[:200]
    mem = (data.get("seed_memory_contract.json") or {}).get("memory_contract") or {}
    mo = data.get("memory_ops_contract.json") or {}

    principles: list[dict] = [
        {
            "name": "Memory contract fidelity",
            "description": "Honor seed memory governance, regions, and MemoryOps retention and rights policy.",
            "why": "Trust and user sovereignty depend on consistent memory behavior aligned with seed artifacts.",
            "examples": [
                "Respect protected_regions and deletion_rules from seed_memory_contract.",
                "Align with memory_ops_contract rights and drift_protection when applicable.",
            ],
        },
        {
            "name": "User sovereignty",
            "description": "Respect companion and operator authority over the Record; gated pipeline for durable changes.",
            "why": "The Voice reflects documented self; integration moments require explicit approval.",
        },
    ]
    if purpose:
        principles.append(
            {
                "name": "Seed intent alignment",
                "description": f"Stay aligned with stated companion purpose: {purpose}",
                "why": "Intent from seed_intent.json guides supported workflows and boundaries.",
            }
        )
    if mem.get("sensitive_categories"):
        principles.append(
            {
                "name": "Sensitive data care",
                "description": "Treat declared sensitive categories with extra caution in recall and suggestions.",
                "why": "seed_memory_contract lists categories requiring careful handling.",
                "examples": [str(x) for x in (mem.get("sensitive_categories") or [])[:5]],
            }
        )
    if mo.get("rights", {}).get("right_to_be_forgotten") is True:
        principles.append(
            {
                "name": "Right to be forgotten",
                "description": "Support user-initiated deletion pathways consistent with MemoryOps rights.",
                "why": "memory_ops_contract records RTBF policy for the instance.",
            }
        )
    return principles


def synthesize_constitution(seed_dir: Path) -> dict:
    data = _load_seed_dir(seed_dir)
    manifest = data["seed-phase-manifest.json"]
    user_slug = manifest.get("user_slug") or "unknown"
    return {
        "version": "1.0",
        "user_slug": user_slug,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt_cache_friendly": True,
        "principles": _build_principles(data),
        "hierarchy": [
            "memory_contract",
            "user_sovereignty",
            "safety",
            "curiosity",
            "pedagogy",
            "expression_fidelity",
            "helpfulness",
        ],
        "self_critique_protocol": {
            "critique_prompt_template": (
                "Critique the assistant reply against the constitution hierarchy (memory_contract first). "
                'Return JSON only: {"violations":[],"score":0.0-1.0,"suggestion":"","early_exit":false}'
            ),
            "revision_prompt_template": (
                "Revise the reply to fix violations; keep simple vocabulary and respect abstention when uncertain."
            ),
            "max_revision_steps": 1,
            "output_format": "json",
        },
        "source_scaffolds": _source_scaffolds(data),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate seed_constitution.json from seed-phase directory")
    ap.add_argument("directory", type=Path, help="e.g. users/demo/seed-phase")
    args = ap.parse_args()
    seed_dir = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    if not seed_dir.is_dir():
        print(f"Not a directory: {seed_dir}", file=sys.stderr)
        return 1
    try:
        doc = synthesize_constitution(seed_dir)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e, file=sys.stderr)
        return 1
    out = seed_dir / "seed_constitution.json"
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    try:
        display = out.relative_to(REPO_ROOT)
    except ValueError:
        display = out
    print(f"Wrote {display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
