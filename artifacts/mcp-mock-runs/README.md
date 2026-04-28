# MCP mock runs (derived)

Markdown packets here are **WORK-layer governance artifacts** produced by **`scripts/mcp_mock_harness.py`** from fixture JSON ([`schemas/mcp-mock-run.v1.json`](../../schemas/mcp-mock-run.v1.json)).

**Mock runs do not execute MCP servers**, do **not** approve credentials or integrations, and do **not** grant live tool access. Each run carries an MCP execution receipt under **`artifacts/mcp-receipts/`** for audit only.

Default generated `*.md` may be **gitignored**; `.gitkeep` preserves the directory. Passing the harness is **not** live MCP approval — see **[`docs/mcp/mcp-mock-execution-harness.md`](../../docs/mcp/mcp-mock-execution-harness.md)**.
