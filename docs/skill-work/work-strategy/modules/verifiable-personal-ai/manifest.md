# Verifiable Personal AI — operator deliberation receipts (WORK-STRATEGY module)

**Status:** WORK only. **Not** crypto infrastructure, not WorldLand/LiberVance integration. Inspired by *verifiable compute* narratives (e.g. thin consensus + heavy useful work): a **thin audit layer** for operator-side “personal AI” workflows so deliberation steps are **traceable** without pretending LLM outputs are cryptographically proven.

## Purpose

1. **Auditable pipeline** — Document *which* steps ran (Perceiver, energy hook, lenses, synthesis), *which* doc versions and sources were used, and *who* signed off—so “reflection gates” are reviewable in WORK artifacts.
2. **No black-box trust** — The receipt does not prove correctness; it proves **process** (same neutral summary fed to all lenses, human synthesis, gate path stated).
3. **Alignment with companion sovereignty** — Nothing here bypasses RECURSION-GATE. Optional ACT- only when the companion approves a candidate that needs an audit line.

## What this is not

- **Not** zkML, on-chain inference, or token economics.
- **Not** a replacement for [work-politics/analytical-lenses](../../../work-politics/analytical-lenses/manifest.md) or [synthesis-engine](../../synthesis-engine.md).
- **Not** permission to append full deliberation dumps to `self-evidence.md`. Use WORK paths per [analytical-lenses manifest § Logging](../../../work-politics/analytical-lenses/manifest.md).

## When to use

- Heavy current-events or persuasive runs where you want a **one-page receipt** next to the draft (e.g. attach to gate candidate summary).
- Multi-session council work where **continuity** matters (“we already locked the neutral summary on date X”).
- Optional: paste receipt block into `recursion-gate.md` candidate `source_exchange` or link to a WORK file path.

## Artifacts

| File | Role |
|------|------|
| [deliberation-receipt-template.md](deliberation-receipt-template.md) | Copy per run; fill IDs, dates, paths, sign-off. |

## Integration points

- [current-events-analysis.md](../../current-events-analysis.md) — After step 5.5, optionally attach a completed receipt.
- [persuasive-content-pipeline.md](../../persuasive-content-pipeline.md) — Before staging for approval, optional receipt.
- [synthesis-engine.md](../../synthesis-engine.md) — Synthesis step IDs belong in the receipt.

## Inspired-by (disclaimer)

“Verifiable” here means **operator-documented traceability**, not ECCVCC-style consensus. External projects (e.g. decentralized AI mainnets) are **not** endorsed; this module is campaign WORK methodology only.
