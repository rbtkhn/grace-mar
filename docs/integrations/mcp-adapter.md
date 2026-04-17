# MCP adapter

Read-only Model Context Protocol adapter over Grace-Mar's governed export surface.

---

## What this is

A thin MCP server that lets external AI tools (Cursor, Claude Desktop, etc.) retrieve governed export views from Grace-Mar using the standard MCP protocol (stdio transport). It wraps the existing export machinery — `export_prp.py`, `export_runtime_bundle.py`, `export_fork.py` — and returns structured JSON responses.

## What this is NOT

- Not a second export system (wraps the existing [export contract](../portable-record/export-contract.md))
- Not a write-back channel (no candidate submission, no Record mutation)
- Not a raw file browser (only governed export views are returned)
- Not a gate bypass (content has already passed through companion-approved pipeline)

---

## Supported export classes

| Class | Status | What it returns |
|---|---|---|
| `tool_bootstrap` | Operational | Compact PRP string for bootstrapping a new tool session |
| `full` | Operational | Broad governed profile bundle (metadata + primary artifact + file manifest) |
| `task_limited` | Operational | Filtered fork export for a specific task or role |
| `capability` | Not yet wired | Rationale format exists; dedicated exporter is future |
| `internal` | Not exportable | Internal-only content stays in the governed Record |

Unsupported classes return a clear error with explanation.

---

## Installation

The MCP adapter requires the optional `mcp` dependency:

```bash
pip install -e ".[mcp]"
```

Core retrieval functions (`health`, `list_export_classes`, `retrieve_export`) remain importable without the `mcp` package for use in tests or other Python code.

---

## Configuration

### Cursor

Add to your MCP configuration (`.cursor/mcp.json` or workspace settings):

```json
{
  "mcpServers": {
    "grace-mar-export": {
      "command": "python",
      "args": ["integrations/mcp_adapter.py"],
      "cwd": "/path/to/grace-mar"
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "grace-mar-export": {
      "command": "python",
      "args": ["/path/to/grace-mar/integrations/mcp_adapter.py"]
    }
  }
}
```

---

## Available tools

### `mcp_health`

Returns adapter status, version, and supported export classes.

### `mcp_list_export_classes`

Enumerates all known export classes with descriptions and operational status.

### `mcp_get_export`

Retrieves a governed export view.

Parameters:
- `user_id` (string, default `"grace-mar"`) — user profile to export
- `export_class` (string, default `"tool_bootstrap"`) — which export class to retrieve

---

## Response shape

Successful retrieval returns:

```json
{
  "user": "grace-mar",
  "export_class": "tool_bootstrap",
  "content_type": "text/plain",
  "content": "...",
  "generated_via": "export_prp",
  "warnings": []
}
```

For `full`, the `content` field is a JSON object with `metadata`, `primary_artifact` (USER.md text), and `bundle_files` (list of generated file paths).

Error responses return:

```json
{
  "error": "export class 'capability' is not yet wired — ...",
  "supported_classes": ["full", "task_limited", "tool_bootstrap"]
}
```

---

## Governance

All exported content has already passed through the gated pipeline (companion approval via `recursion-gate.md`). The adapter does not expose:

- Raw canonical files directly
- Unreviewed candidate queues
- Runtime scratch surfaces
- Internal-only content

---

## Related

- [export-contract.md](../portable-record/export-contract.md) — export classes and policy
- [portable-working-identity.md](../portable-working-identity.md) — portability doctrine
- [runtime-vs-record.md](../runtime-vs-record.md) — canonical vs derived
- [EXPORT-CLI.md](../EXPORT-CLI.md) — CLI reference
