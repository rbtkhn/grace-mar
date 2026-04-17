#!/usr/bin/env python3
"""
Read-only MCP adapter over Grace-Mar's governed export surface.

Exposes operational export classes (tool_bootstrap, full, task_limited) as MCP
tools so external AI systems can retrieve governed views of the Record without
bypassing the gate or touching raw files.

This adapter wraps the existing export machinery — it does not create a second
export stack.  Policy comes from scripts/export.py and the child exporters.

Usage (stdio transport — configure in Cursor / Claude Desktop MCP settings):
    python integrations/mcp_adapter.py

Requires the optional ``mcp`` dependency:
    pip install -e ".[mcp]"

See docs/integrations/mcp-adapter.md for configuration and response shapes.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# --- Import export machinery (same pattern as integrations/export_hook.py) ---

try:
    from export_prp import export_prp
except ImportError:
    from scripts.export_prp import export_prp  # type: ignore[no-redef]

try:
    from export_runtime_bundle import export_runtime_bundle
except ImportError:
    from scripts.export_runtime_bundle import export_runtime_bundle  # type: ignore[no-redef]

try:
    from export_fork import export_fork
except ImportError:
    from scripts.export_fork import export_fork  # type: ignore[no-redef]

# --- Constants (derived from scripts/export.py to stay in sync) ----------

SUPPORTED_CLASSES: dict[str, str] = {
    "tool_bootstrap": "Compact prompt encoding the Record for bootstrapping a new tool session",
    "full": "Broad governed profile across all approved surfaces (portable bundle)",
    "task_limited": "Filtered fork export for a specific task or role (coach handoff)",
}

UNSUPPORTED_CLASSES: dict[str, str] = {
    "capability": "not yet wired — rationale format exists but dedicated export filtering is future",
    "internal": "not exportable by definition — internal-only content stays in the governed Record",
}

ADAPTER_VERSION = "1.0.0"


# =========================================================================
# Layer 1 — Core retrieval functions (no MCP dependency)
# =========================================================================

def _default_user_id() -> str:
    env = os.environ.get("GRACE_MAR_USER_ID", "").strip()
    if env:
        return env
    if (REPO_ROOT / "users" / "grace-mar").is_dir():
        return "grace-mar"
    return "_template"


def health() -> dict:
    """Adapter status and capabilities."""
    return {
        "status": "ok",
        "adapter": "grace-mar-mcp",
        "version": ADAPTER_VERSION,
        "read_only": True,
        "supported_classes": sorted(SUPPORTED_CLASSES),
        "repo_root": str(REPO_ROOT),
    }


def list_export_classes() -> dict:
    """Enumerate export classes with status and descriptions."""
    return {
        "supported": {
            name: {"description": desc, "operational": True}
            for name, desc in SUPPORTED_CLASSES.items()
        },
        "unsupported": {
            name: {"description": desc, "operational": False}
            for name, desc in UNSUPPORTED_CLASSES.items()
        },
    }


def _retrieve_tool_bootstrap(user_id: str) -> dict:
    content = export_prp(user_id=user_id)
    return {
        "user": user_id,
        "export_class": "tool_bootstrap",
        "content_type": "text/plain",
        "content": content,
        "generated_via": "export_prp",
        "warnings": [],
    }


def _retrieve_full(user_id: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="gm_mcp_full_") as tmpdir:
        bundle_dir = Path(tmpdir)
        payload = export_runtime_bundle(
            user_id=user_id,
            output_dir=bundle_dir,
            runtime_mode="portable_bundle_only",
        )

        primary_artifact = ""
        user_md_path = bundle_dir / "record" / "USER.md"
        if user_md_path.exists():
            primary_artifact = user_md_path.read_text(encoding="utf-8")

        bundle_files: list[str] = []
        for p in sorted(bundle_dir.rglob("*")):
            if p.is_file():
                bundle_files.append(str(p.relative_to(bundle_dir)))

    return {
        "user": user_id,
        "export_class": "full",
        "content_type": "application/json",
        "content": {
            "metadata": payload,
            "primary_artifact": primary_artifact,
            "bundle_files": bundle_files,
        },
        "generated_via": "export_runtime_bundle",
        "warnings": [],
    }


def _retrieve_task_limited(user_id: str) -> dict:
    content = export_fork(user_id=user_id, include_raw=True)
    return {
        "user": user_id,
        "export_class": "task_limited",
        "content_type": "application/json",
        "content": content,
        "generated_via": "export_fork",
        "warnings": [],
    }


_RETRIEVERS: dict[str, object] = {
    "tool_bootstrap": _retrieve_tool_bootstrap,
    "full": _retrieve_full,
    "task_limited": _retrieve_task_limited,
}


def retrieve_export(user_id: str | None = None, export_class: str = "") -> dict:
    """
    Retrieve a governed export view by export class.

    Returns a structured dict on success, or an error dict with reason.
    """
    resolved_user = user_id or _default_user_id()

    if export_class in UNSUPPORTED_CLASSES:
        return {
            "error": f"export class {export_class!r} is {UNSUPPORTED_CLASSES[export_class]}",
            "supported_classes": sorted(SUPPORTED_CLASSES),
        }

    if export_class not in SUPPORTED_CLASSES:
        return {
            "error": f"unknown export class {export_class!r}",
            "supported_classes": sorted(SUPPORTED_CLASSES),
        }

    retriever = _RETRIEVERS[export_class]
    return retriever(resolved_user)  # type: ignore[operator]


# =========================================================================
# Layer 2 — MCP server (requires ``mcp`` package)
# =========================================================================

def _build_mcp_server():  # noqa: ANN202
    """Construct the MCP server with tools registered.  Raises ImportError
    if the ``mcp`` package is not installed."""
    from mcp.server.fastmcp import FastMCP  # type: ignore[import-untyped]

    server = FastMCP(
        "grace-mar-export",
        version=ADAPTER_VERSION,
    )

    @server.tool()
    def mcp_health() -> str:
        """Return adapter health and supported export classes."""
        return json.dumps(health(), indent=2)

    @server.tool()
    def mcp_list_export_classes() -> str:
        """List available export classes with status and descriptions."""
        return json.dumps(list_export_classes(), indent=2)

    @server.tool()
    def mcp_get_export(user_id: str = "grace-mar", export_class: str = "tool_bootstrap") -> str:
        """Retrieve a governed export view by export class.

        Supported classes: tool_bootstrap, full, task_limited.
        Returns JSON with the export content or an error explanation.
        """
        result = retrieve_export(user_id=user_id, export_class=export_class)
        return json.dumps(result, indent=2, default=str)

    return server


if __name__ == "__main__":
    try:
        server = _build_mcp_server()
    except ImportError:
        print(
            "mcp_adapter: the 'mcp' package is required to run as a server.\n"
            "Install with: pip install -e '.[mcp]'\n"
            "Core functions (health, list_export_classes, retrieve_export) "
            "remain importable without the mcp package.",
            file=sys.stderr,
        )
        sys.exit(1)
    server.run()
