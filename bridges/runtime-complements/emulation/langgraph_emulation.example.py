#!/usr/bin/env python3
"""Example graph-style node for a Grace-Mar emulation bundle.

This file avoids a hard LangGraph dependency on purpose. It shows the shape of a
node callable that a graph runtime could wrap around the existing bundle.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


def load_boundary_context(bundle_dir: str | Path) -> dict[str, Any]:
    root = Path(bundle_dir)
    envelope = json.loads((root / "emulation-bundle.json").read_text(encoding="utf-8"))
    prp = (root / envelope["references"]["prpPath"]).read_text(encoding="utf-8")
    return {
        "boundary_notice": envelope["boundaryNotice"],
        "proposal_schema": envelope["proposalReturn"]["schemaPath"],
        "prp": prp,
    }


def emulation_node(state: dict[str, Any], llm_call: Callable[[str], str]) -> dict[str, Any]:
    context = load_boundary_context(state["bundle_dir"])
    latest_user_turn = state.get("latest_user_turn", "")
    prompt = (
        f"{context['prp']}\n\n"
        f"Boundary notice: {context['boundary_notice']}\n\n"
        "You may reason and draft. You may not claim canonical mutation authority.\n\n"
        f"User turn: {latest_user_turn}\n"
    )
    response = llm_call(prompt)
    return {
        "assistant_response": response,
        "return_paths": {
            "runtime_observation": "scripts/runtime/import_runtime_observation.py",
            "durable_change_schema": context["proposal_schema"],
        },
    }
