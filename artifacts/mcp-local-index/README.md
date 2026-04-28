# MCP local directory index packets (derived)

Markdown packets here are **WORK-layer artifacts** from **`scripts/mcp_local_index.py`**, which emits **metadata only** (paths, kinds, sizes; optional line counts and hashes) for files and directories under **[`config/mcp-local-read-allowlist.yaml`](../../config/mcp-local-read-allowlist.yaml)** roots — **no file contents or excerpts**.

**No MCP servers**, **no credentials**, **no network**, **no shell**, and **no canonical Record reads/writes**. Each run emits an MCP execution receipt under **`artifacts/mcp-receipts/`** with capability **`filesystem_readonly`** (see **[`docs/mcp/mcp-local-index-adapter.md`](../../docs/mcp/mcp-local-index-adapter.md)**).

Default generated `*.md` may be **gitignored**; `.gitkeep` preserves the directory. Passing this adapter does **not** approve broader live MCP integration.
