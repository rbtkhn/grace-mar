# Workbench Harness (work-dev)

**Status:** WORK-only. **Markdown-first**, repo-native. **Not** a merge path, **not** Record, **not** EVIDENCE truth.

## What it is

The **Workbench Harness** is a narrow **artifact execution and inspection** layer for **generated** code, UI, HTML/React/SVG, CLI tools, scripts, and strategy-notebook views. It makes a **repeatable loop** legible: generate → run → inspect → revise → **workbench receipt** → operator review.

Workbench answers: *“Did this artifact run, render, and behave as intended in this environment?”* It does **not** answer *“Is this claim about the world true?”*

## What it is not

- **Not** the [Record](../../../../AGENTS.md) or a path into it. Workbench receipts have **`recordAuthority: "none"`** and **`gateEffect: "none"`** unless you separately stage work through [recursion-gate.md](../../../../users/grace-mar/recursion-gate.md) using existing workflows.
- **Not** [action receipts](../../../action-receipts.md) (audit stubs for meaningful system actions like proposals or merges).
- **Not** merge or pipeline receipts ([harness-inventory](../../../harness-inventory.md) / `merge-receipts.jsonl` — proof of **approved** pipeline/gate processing).
- **Not** continuity / handback receipts (OpenClaw preflight, session continuity).
- **Not** a replacement for [harness replay](../../../harness-replay.md) (event/candidate correlation across `pipeline-events.jsonl`, gate blocks, etc.).
- **Not** a replacement for [observability](../../../observability.md) aggregates.

## How it fits (one sentence each)

| Surface | Role |
|--------|------|
| [Action receipts](../../../action-receipts.md) | Makes **system actions** (e.g. change proposals) inspectable; not the Record, not a second merge path. |
| [Observability](../../../observability.md) | Aggregates over proposals, validators, operational counts. |
| [Harness replay](../../../harness-replay.md) | Replays **gate/candidate** and pipeline **events**; does not substitute for “did the UI work?” |
| [Verification runs](../verification-runs/README.md) | Dated **manual or script** verification for [claim–proof](../claim-proof-standard.md) on capabilities. |
| **Workbench** | **Artifact** run/inspect/revise with a **workbench receipt**; proves **build/runtime behavior** under stated conditions, not world truth. |

Runtime vs Record: treat Workbench as **work-dev / runtime lab** work. Nothing here auto-writes SELF, EVIDENCE, or the gate.

## When to use it

- Generated dashboards, visualizers, or storybook-style views.
- HTML/React/SVG, CLI tools, or scripts the agent (or you) just produced.
- Strategy-notebook or similar **WORK** UIs you need to **see** before trusting.

## Core loop

1. **Generate** — code or assets land under repo paths (or a bounded scratch path).
2. **Run** — `launchCommand` (and `commandsRun` as needed).
3. **Inspect** — see [VISUAL-INSPECTION-PROTOCOL.md](VISUAL-INSPECTION-PROTOCOL.md) for visuals; adapt for headless CLIs.
4. **Revise** — record what changed; summarize in the receipt.
5. **Receipt** — write a [WORKBENCH-RECEIPT-SPEC](WORKBENCH-RECEIPT-SPEC.md) JSON object; store under [default output path](#where-to-store-receipts) or a team convention.
6. **Operator review** — human decides what ships, what gets a gate candidate, or what to discard.

## Doctrine (non-negotiable)

- **`recordAuthority`:** `none` for workbench receipts — they do not assert Record or EVIDENCE authority.
- **`gateEffect`:** `none` — a workbench receipt does not approve, merge, or stage candidates. Staging still uses the normal gate pipeline if you choose to.
- **Truth scope:** Screenshots, logs, and tests in a receipt show **artifact behavior** under the described setup; they do not prove **external** facts. Same spirit as [action-receipts.md](../../../action-receipts.md): *inspectable*, not *oracular*.

## Where to store receipts

- **Default suggested path for real runs:** [artifacts/work-dev/workbench-receipts/](../../../../artifacts/work-dev/workbench-receipts/README.md) (create JSON files there; add to `.gitignore` locally if some runs must not be committed).
- **Examples and fixtures:** [examples/](examples/) under this folder.

v1 does **not** require placing receipts under `users/<id>/` canonical files.

## Non-goals (explicit)

- Does **not** by itself satisfy [claim-proof-standard.md](../claim-proof-standard.md) for an **implemented** capability row — use tests, [verification-runs](../verification-runs/README.md), or demos when elevating that claim. Workbench can still be cited as *supporting* “we ran it and saw X.”
- Does **not** replace harness replay, observability, or gate hygiene.

## Specs and protocols

| Doc | Role |
|-----|------|
| [WORKBENCH-RECEIPT-SPEC.md](WORKBENCH-RECEIPT-SPEC.md) | JSON field definitions (`receiptKind: "workbench"`, camelCase). |
| [VISUAL-INSPECTION-PROTOCOL.md](VISUAL-INSPECTION-PROTOCOL.md) | Required steps for **visual** artifacts. |
| [CANDIDATE-COMPARISON-PROTOCOL.md](CANDIDATE-COMPARISON-PROTOCOL.md) | Compare multiple generated **candidates** (A/B) before choosing a path. |

## Related (optional)

- [claim-proof-standard.md](../claim-proof-standard.md) — what counts as proof for work-dev **implemented** claims.
- [harness-inventory.md](../../../harness-inventory.md) — audit lane, merge-receipts, `harness-events.jsonl`.
- [control-plane/capability-contract-template.yaml](../control-plane/capability-contract-template.yaml) — integration **receipt shape** (different subject; cross-domain naming awareness).

---

*Workbench Harness — work-dev artifact inspection only.*
