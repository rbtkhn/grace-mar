# Local read-only MCP-shaped adapter

**Status:** Narrow **live data-plane** step — **`scripts/mcp_local_readonly.py`** reads repo files as UTF-8 under **[`config/mcp-local-read-allowlist.yaml`](../../config/mcp-local-read-allowlist.yaml)** only. **No MCP servers**, **no credentials**, **no network**, **no shell**.

**Related:** [`schemas/mcp-local-read-request.v1.json`](../../schemas/mcp-local-read-request.v1.json), [`docs/mcp/governed-mcp-layer.md`](governed-mcp-layer.md), capability **`filesystem_readonly`** in [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml).

---

## Why this is the first “narrow live” adapter

Earlier MCP tooling here was planning-first ([**manifest admission**](mcp-manifest-admission.md)) or fixture-only ([**mock harness**](mcp-mock-execution-harness.md)). This adapter performs **one real bounded IO**: reading bytes from disk inside declared roots with deterministic rejection rules — enough to exercise receipts + bindings against **`filesystem_readonly`** without implying broader MCP enablement.

---

## How this differs from the mock harness

| Aspect | Mock harness ([`mcp_mock_harness.py`](../../scripts/mcp_mock_harness.py)) | Local read adapter (`mcp_local_readonly.py`) |
|--------|--------------------------------------------------------------------------|----------------------------------------------|
| Data source | Declared **`mock_request`** / **`mock_response`** in JSON only | Actual **`path`** read from repo workspace |
| Receipt **`capability.id`** | **`mcp_mock_harness`** | **`filesystem_readonly`** |
| Purpose | Simulate posture vs registry | Enforce allowlist + emit metrics + excerpt |

---

## How this differs from general MCP

- **No MCP host/server**: invocation is **`python scripts/mcp_local_readonly.py`** reading JSON + YAML configs — no STDIO MCP socket/process graph from IDEs.
- **No remote identifiers**: paths must resolve inside **`repo-root`** after symlink-resolution containment checks.

---

## Allowlist model

[`config/mcp-local-read-allowlist.yaml`](../../config/mcp-local-read-allowlist.yaml) defines:

- **`allowed_roots`** — repo-relative prefixes permitted for reads (e.g. **`docs/`**, **`schemas/`**, named **`artifacts/…`** buckets).
- **`blocked_roots`** — hard deny prefixes (**`users/grace-mar/`**, **`venv/`**, **`.git/`**, …).
- **`blocked_files`** — basename denylist (**`.env`**, **`id_rsa`**, …).
- **`blocked_name_patterns`** — **`fnmatch`** on basename (**`*secret*`**, **`*.pem`**, …).
- **`max_file_bytes`** — read refusal beyond size.

Rejected paths fail closed (**exit 1**) **before** any receipt emission.

---

## Receipt behavior

- Receipt **`capability.id`** = **`filesystem_readonly`** (registry **`output_lane`:** **`runtime_only`**).
- Registry **`writes: []`** implies **`access.resources_written`** must be **empty** for validated receipts — packet paths appear under **`result.artifacts`** only; **`access.resources_read`** lists request JSON path + resolved target path.

See packet footer note under **`artifacts/mcp-local-read/`**.

---

## Forbidden paths (high level)

- Absolute paths, **`..`**, **`users/grace-mar/`**, blocked roots/files/globs.

Symlinks are only acceptable when **`resolve()`** stays strictly inside **`repo-root`** (outside escapes **`relative_to`** rejection).

---

## Why passing local read does not approve broader MCP

Successful adapter runs prove **allowlisted filesystem reads + receipt emission** for **`filesystem_readonly`**. They do **not**:

- configure Cursor/Godot MCP connectors,
- grant credential-backed SCM/Git APIs,
- or weaken recursion-gate / AGENTS boundary.

Promotion of insight into canonical Record remains **`recursion-gate.md`** + companion-approved merges only.

---

## CLI

```bash
python3 scripts/mcp_local_readonly.py \
  --input examples/mcp-local-read-request.example.json \
  --output artifacts/mcp-local-read/read-example.md
```
