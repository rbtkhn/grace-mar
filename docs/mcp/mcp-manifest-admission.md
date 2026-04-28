# MCP manifest admission adapter

**Status:** Planning-only WORK artifact generator. **This adapter does not execute MCP servers**, enable integrations, read credential stores, or touch canonical Record surfaces.

**See also:** [`governed-mcp-layer.md`](governed-mcp-layer.md) (context), [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml) (capability classes), [`schemas/mcp-server-manifest.v1.json`](../../schemas/mcp-server-manifest.v1.json) (manifest schema).

---

## Why admission exists

Before wiring a proposed MCP server into an IDE or assistant host, the operator can **declare** tools, permissions, and intent in a **manifest** (YAML or JSON). The admission script **`scripts/mcp_manifest_admission.py`** ingests that file **from disk only**, validates it against the manifest schema, and produces:

1. A **Markdown packet** under **`artifacts/mcp-admission/`** (WORK-layer draft — inspectable, not canonical Record).
2. An **MCP execution receipt** under **`artifacts/mcp-receipts/`**, stamped with registry capability **`mcp_manifest_admission`** (**`output_lane: work_artifact`**).

Admission answers: **Which Grace-Mar capability class does this declaration resemble**, **what authority lane binds**, **whether structured risk rules trip**, and **whether declared posture violates hard gates**. It does **not** attest that the live server behaves as declared.

---

## Manifest vs live MCP

| Aspect | Declared manifest (this adapter) | Live MCP integration |
|--------|-----------------------------------|----------------------|
| Source | Static YAML/JSON on disk | Running server process |
| Risk signal | Registry overlay + policy scan over declared strings | Runtime behavior, credentials, network calls |
| Output | Markdown packet + receipt (`work_artifact` lane) | Tool execution, runtime receipts under whatever lane the capability permits |

**Passing admission does not approve enabling** the server in a host configuration.

---

## Matching table (informal)

Heuristic classification maps common declaration shapes to **`config/mcp-capabilities.yaml`** ids (examples): **`github_readonly`**, **`github_patch_proposal`**, **`filesystem_readonly`**, **`web_research`**, **`database_readonly`**, **`coding_agent_patch_intake`**, prohibition templates such as **`shell_execution_prohibited`** / **`memory_external_prohibited_by_default`**, or **`needs_manual_classification`** when no fingerprint fits.

Danger-first ordering applies (for example shell verbs or merge-to-main in **`allowed_actions`** before benign SCM reads).

---

## Authority and risk

- **Authority:** The matched capability’s **`output_lane`** is summarized against **`config/mcp-authority-bindings.yaml`** (same join table as other MCP receipts).
- **Risk:** The script builds a **registry-shaped overlay** from the matched capability row plus manifest **`permissions`** fields where safe, then runs **`evaluate_capability`** from **`scripts/mcp_risk_scan.py`** against **`config/mcp-risk-policy.yaml`**. Hard blockers from the risk scan contribute to **blocked** admission status.

---

## Operator intent and lanes

If **`operator.requested_output_lane`** is present, it must not **widen** beyond the matched capability’s lane under the ranked ordering:

**`runtime_only` → `work_artifact` → `evidence_stub` → `candidate_proposal`**

Requesting a wider lane than the classifier matched produces a **lane gate** blocker.

---

## Receipt semantics

Receipt **`capability.id`** defaults to **`mcp_manifest_admission`**. **`result.status`** is **`blocked`** when admission gates fail (including manual classification required); otherwise **`success`** for successful packet emission — **not** “approved integration.” **`governance.canonical_record_touched`** remains **`false`** unless path gates imply Record surfaces (normally **`false`**).

---

## CLI

```bash
python3 scripts/mcp_manifest_admission.py \
  --input examples/mcp-server-manifest.example.yaml \
  --output artifacts/mcp-admission/example.md
```

Paths **`--capabilities`**, **`--bindings`**, **`--policy`** default to repo **`config/`** files. **`--repo-root`** defaults to the repository root. **`--output`** must resolve under **`artifacts/mcp-admission/`**.

---

## Definition of done (operator)

- Admission Markdown and receipt emitted under the artifact buckets.
- **`python3 scripts/mcp_receipt_audit.py`** still validates committed receipts when you add JSON under **`artifacts/mcp-receipts/`**.
- Registry edits remain consistent: **`python3 scripts/mcp_capability_audit.py`** and **`python3 scripts/mcp_authority_check.py`**.
