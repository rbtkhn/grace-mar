# MCP local read-only packets (derived)

Markdown packets here are **WORK-layer artifacts** from **`scripts/mcp_local_readonly.py`**, which performs **bounded UTF-8 reads** of repo files under **[`config/mcp-local-read-allowlist.yaml`](../../config/mcp-local-read-allowlist.yaml)** only.

**No MCP servers**, **no credentials**, **no network**, **no shell**, and **no canonical Record reads/writes**. Each run emits an MCP execution receipt under **`artifacts/mcp-receipts/`** with capability **`filesystem_readonly`** (see **[`docs/mcp/mcp-local-readonly-adapter.md`](../../docs/mcp/mcp-local-readonly-adapter.md)**).

Default generated `*.md` may be **gitignored**; `.gitkeep` preserves the directory. Passing this adapter does **not** approve broader live MCP integration.
