# MCP mock execution harness

**Status:** WORK-layer fixture runner only. **`scripts/mcp_mock_harness.py`** does **not** execute MCP servers, load credentials, open network connections, run shell commands, or enable integrations.

**See also:** [`governed-mcp-layer.md`](governed-mcp-layer.md), [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml), [`schemas/mcp-mock-run.v1.json`](../../schemas/mcp-mock-run.v1.json).

---

## Why this harness exists

Grace-Mar already maintains capability classes, authority bindings, risk policy, and MCP receipts for planning. Before anyone considers **live** MCP wiring, the mock harness lets operators replay **MCP-shaped** tool calls against **local JSON fixtures**: same registry lookup, binding summary, and risk scoring overlay—without a running server.

Mock execution answers: **Given a declared capability id and mock access posture, does the fixture stay within registry limits, and what does the risk scanner say when we overlay the mock request onto the simulated capability row?**

---

## How this differs from manifest admission

| Aspect | [`mcp_manifest_admission.py`](../../scripts/mcp_manifest_admission.py) | Mock harness (`mcp_mock_harness.py`) |
|--------|----------------------------------------------------------------------|--------------------------------------|
| Input | Declared **server manifest** (YAML/JSON) — tools/permissions narrative | **Single mock run** — explicit tool name, mock request/response, governance flags |
| Classification | Infers best-matching capability id from heuristics | **`run.capability_id`** must match a registry id exactly |
| Receipt **`capability.id`** | **`mcp_manifest_admission`** | **`mcp_mock_harness`** |

Both emit **`work_artifact`** Markdown under **`artifacts/`** plus validated receipts under **`artifacts/mcp-receipts/`**. Neither approves live MCP.

---

## How this differs from live MCP integration

| Mock harness | Live integration (out of scope here) |
|----------------|-------------------------------------|
| Reads fixture JSON from disk | Host launches MCP server processes |
| **`mock://`** URIs and repo-relative fixture paths only | Real URIs, credentials, network I/O |
| **`mock_response.data`** is opaque fixture payload | Tool returns bind to runtime behavior |

Passing the mock harness **does not** authorize IDE MCP configs, API tokens, or automated posting.

---

## Input format

Validated against **[`schemas/mcp-mock-run.v1.json`](../../schemas/mcp-mock-run.v1.json)**:

- **`run`:** `id`, `capability_id` (registry id), `tool_name`, `declared_intent`
- **`mock_request`:** `resources_read`, `resources_written`, `network_access`, `credential_use`
- **`mock_response`:** `status`, `summary`, `data`
- **`governance_expectations`:** review flags plus **`durable_state_write_attempted`** and **`canonical_record_touched`** (must remain **`false`** for harness acceptance)

**Resource strings** must be **`mock://...`** URIs or repo-relative paths (no `..`, no absolute paths, no `http(s)://`, no `users/grace-mar/`).

---

## Output format

1. **Markdown packet** under **`artifacts/mcp-mock-runs/`** with YAML front matter (`receipt_id`, `mock_run_id`, `simulated_capability_id`) and banner line:
   `MOCK MCP RUN · WORK ARTIFACT · NO LIVE SERVER · NOT APPROVED INTEGRATION`
2. **MCP execution receipt** JSON (`capability.id` = **`mcp_mock_harness`**, **`output_lane`:** **`work_artifact`**) — receipt **`access`** fields follow the **adapter** registry row (network/credential **`none`**), not the simulated GitHub read posture.

---

## Capability / authority / risk / receipt chain

1. Resolve **`run.capability_id`** from **[`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml)** (simulated capability).
2. Enforce mock request versus simulated registry limits (writes empty when registry writes empty; network and credential ranks; prohibited lane cannot claim **`success`**; shell-shaped **`tool_name`** cannot pair with **`success`**).
3. Overlay mock request onto a copy of the simulated capability row and run **`evaluate_capability`** against **[`config/mcp-risk-policy.yaml`](../../config/mcp-risk-policy.yaml)** for the Markdown risk section.
4. Summarize authority binding for the **simulated** **`output_lane`** via **[`bindings_lane_map`](../../scripts/mcp_receipt_lib.py)**.
5. Emit receipt via **`build_receipt`** + **`validate_mcp_receipt`** using adapter capability **`mcp_mock_harness`**.

---

## Blocked-action behavior

Fixtures may declare **`mock_response.status`** **`blocked`** or **`failed`** (for example a simulated shell refusal). The harness still emits packet + receipt when limits pass; receipt **`result.status`** echoes the mock status. **`governance.prohibited_action_attempted`** is set when the outcome is blocked/failed or when shell-shaped tools are detected outside a pure-success story.

Unsafe fixtures (bad paths, exceeding registry posture, prohibited **`success`**, governance flags true) **fail closed** with **`exit 1`** and **no** packet write.

---

## Why passing does not approve live use

The harness validates **fixture discipline** and **registry consistency** against policy text. It does **not** observe real host behavior, secret handling, or runtime MCP semantics. Live integration remains a **separate**, explicitly gated decision.

---

## CLI

```bash
python3 scripts/mcp_mock_harness.py \
  --input examples/mcp-mock-run.github-readonly.example.json \
  --output artifacts/mcp-mock-runs/demo.md
```

See **[`artifacts/mcp-mock-runs/README.md`](../../artifacts/mcp-mock-runs/README.md)** for bucket policy.
