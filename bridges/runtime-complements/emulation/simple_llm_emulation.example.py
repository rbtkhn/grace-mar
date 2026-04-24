#!/usr/bin/env python3
"""Minimal example loader for a Grace-Mar emulation bundle.

Example-only: loads the governed bundle, composes a system prompt, and shows the
two safe return channels:
1. runtime-only observation payloads for the membrane
2. durable change proposals for existing review surfaces
"""

from __future__ import annotations

import json
from pathlib import Path


def load_emulation_bundle(bundle_dir: str | Path) -> dict:
    root = Path(bundle_dir)
    envelope = json.loads((root / "emulation-bundle.json").read_text(encoding="utf-8"))
    prp = (root / envelope["references"]["prpPath"]).read_text(encoding="utf-8")
    fork_export = json.loads((root / envelope["references"]["forkExportPath"]).read_text(encoding="utf-8"))
    return {
        "root": root,
        "envelope": envelope,
        "prp": prp,
        "fork_export": fork_export,
    }


def build_system_prompt(bundle: dict) -> str:
    envelope = bundle["envelope"]
    return (
        f"{bundle['prp']}\n\n"
        "## Boundary notice\n"
        f"{envelope['boundaryNotice']}\n\n"
        "## Durable changes\n"
        "Return durable changes as reviewed change-proposal objects; do not edit canonical files directly.\n\n"
        "## Runtime-only notes\n"
        "Return runtime-only observations for the membrane import path when the result is continuity or session residue.\n"
    )


def build_runtime_observation_payload(summary: str) -> dict:
    return {
        "type": "session_summary",
        "summary": summary,
        "human_review_required": True,
        "canonical_surfaces_touched": False,
    }


def build_durable_change_stub(topic: str, summary: str) -> dict:
    return {
        "schema_hint": "policy/change-proposal.v1.json",
        "topic": topic,
        "summary": summary,
        "human_review_required": True,
        "canonical_surfaces_touched": False,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load and inspect a Grace-Mar emulation bundle")
    parser.add_argument("bundle_dir", help="Directory produced by export.py emulation")
    args = parser.parse_args()

    bundle = load_emulation_bundle(args.bundle_dir)
    print(build_system_prompt(bundle))
