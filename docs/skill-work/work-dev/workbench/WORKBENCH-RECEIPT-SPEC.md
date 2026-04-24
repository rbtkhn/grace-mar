# Workbench receipt — JSON spec (v0.1)

**Purpose:** Machine-readable log for a single **run** of a **generated artifact** (code, UI, script). **Not** a merge receipt, **not** an [action receipt](../../../action-receipts.md) (different `receiptKind`, different lifecycle).

**Naming:** In prose you may use snake_case labels as aliases. **Payload on disk** uses **camelCase** keys, aligned with [action-receipts.md](../../../action-receipts.md) (*future* `action-receipt.v1` style).

**Gate disambiguation:** `workbenchRunId` is **not** `CANDIDATE-nnnn` from the recursion-gate. Use **`relatedGateCandidateId`** only when the artifact is explicitly about a specific gate block (e.g. you are visually verifying a handback UI for that candidate).

## Required: `receiptKind`

Every workbench JSON object must include:

```json
"receiptKind": "workbench"
```

## Field list

| Field | Type | Description |
|-------|------|-------------|
| `metaNote` | string (optional) | Human-only label (e.g. `EXAMPLE / HYPOTHETICAL`). Omitted in production receipts. |
| `receiptId` | string | Unique id for this receipt (e.g. `wb-2026-04-23-strategy-viz-01`). |
| `createdAt` | string (ISO-8601) | When the inspection finished (or last revision of this run). |
| `workbenchRunId` | string | Idempotency / grouping for this workbench run (one receipt per run; revise in place or bump `receiptId`). |
| `lane` | string | e.g. `work-dev` — which harness lane is speaking. |
| `artifactType` | string | e.g. `react`, `html`, `cli`, `python-script`, `svg`, `strategy-notebook-view`. |
| `artifactCandidateLabel` | string | **Not** a gate `CANDIDATE-nnnn` unless you also set `relatedGateCandidateId`. Free label: `A`, `round2`, `feature-branch`. |
| `relatedGateCandidateId` | string or null | Optional. Only when tied to a gate block (e.g. `CANDIDATE-0042`). |
| `sourcePromptRef` | string | Reference to the prompt, session, or doc that produced the artifact (file path, URL, or short id). |
| `pathsTouched` | string[] | **Repo-relative** paths (from repository root) read or written during the run. |
| `commandsRun` | string[] | Commands you actually ran (shell strings). |
| `launchCommand` | string | Primary command the operator (or script) used to start the artifact. |
| `inspection` | object | See below. |
| `revisionSummary` | string | What changed between attempts (empty string if first pass). |
| `status` | string | e.g. `pass`, `fail`, `inconclusive`, `revoked` (enum is informal v0.1). |
| `recordAuthority` | string | Must be `"none"` for v0.1 workbench receipts. |
| `gateEffect` | string | Must be `"none"` for v0.1 workbench receipts. |

## `inspection` object

| Field | Type | Description |
|-------|------|-------------|
| `method` | string | How you inspected: e.g. `manual_screenshot`, `playwright`, `smoke`, `none_headless`. |
| `screenshots` | string[] | Repo-relative paths to **saved** images, or `[]` if not applicable. |
| `observedFailures` | string[] | What broke or looked wrong (empty if pass). **Behavioral** notes, not world claims. |
| `acceptanceChecklist` | string[] | Short checklist results (each item can be the check + `ok` / `fail`). |

## Doctrine (defaults)

- **`recordAuthority`:** `none` — the receipt does not assert SELF, EVIDENCE, or Record updates.
- **`gateEffect`:** `none` — no automatic staging, approval, or merge. A future doc could describe a **separate** path that reads workbench output and *then* uses normal gate tools; v0.1 does not define that.

## Minimal example (fragment)

```json
{
  "receiptKind": "workbench",
  "receiptId": "wb-example-001",
  "createdAt": "2026-04-23T12:00:00Z",
  "workbenchRunId": "run-example-001",
  "lane": "work-dev",
  "artifactType": "cli",
  "artifactCandidateLabel": "smoke",
  "relatedGateCandidateId": null,
  "sourcePromptRef": "docs/skill-work/work-dev/workspace.md",
  "pathsTouched": ["scripts/example.py"],
  "commandsRun": ["python3 scripts/example.py --dry-run"],
  "launchCommand": "python3 scripts/example.py --dry-run",
  "inspection": {
    "method": "smoke",
    "screenshots": [],
    "observedFailures": [],
    "acceptanceChecklist": ["Exits 0: ok"]
  },
  "revisionSummary": "",
  "status": "pass",
  "recordAuthority": "none",
  "gateEffect": "none"
}
```

## Full example (fixture)

See [examples/strategy-notebook-visualizer-receipt.example.json](examples/strategy-notebook-visualizer-receipt.example.json) — example data, clearly **non-authoritative** (`metaNote` at top; valid JSON — no `//` comments).
