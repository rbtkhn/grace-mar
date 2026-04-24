# Portable Emulation

**Purpose:** Formalize Grace-Mar's emulation-ready bundle as a documented, authority-bounded portability contract for foreign runtimes.

**Status:** Contract layer over the existing emulation-ready export. This doc does **not** create a second portability stack and does **not** add merge authority to foreign runtimes.

---

## What Portable Emulation Is

Portable emulation is the practice of loading a governed Grace-Mar export into a foreign runtime so that runtime can:

- read exported Record context in a bounded, read-only way
- construct governed context for answering or assisting
- produce runtime observations
- emit proposal envelopes for durable changes

Portable emulation exists so a foreign runtime can *consume* Grace-Mar's governed state without becoming the system of record.

---

## Why It Exists

Grace-Mar already supports:

- governed Record export
- runtime bundle export
- PRP export
- proposal return to the source repo

Portable emulation names the contract around those pieces so downstream runtimes can act consistently without inventing their own authority model.

This makes the bundle easier to:

- explain
- validate
- hand to a foreign runtime
- audit after use

---

## What It Is Not

Portable emulation is **not**:

- a second Record
- a merge path
- a shortcut around `recursion-gate.md`
- permission to mutate SELF, SELF-LIBRARY, SKILLS, or EVIDENCE
- a replacement for the runtime-complements membrane
- an executable emulator in this PR

---

## Emulation Bundle vs Membrane Bundle

The **emulation-ready bundle** is the broader governed package. It carries the runtime bundle, PRP, fork export, authority references, and proposal return contract for a foreign runtime that needs to load Grace-Mar behavior.

The **runtime-complements membrane bundle** is narrower. It is for bounded runtime context exchange and runtime-only observation import, not full emulation-oriented loading.

Use the membrane when you want a deliberately small, allow-listed exchange surface.

Use portable emulation when you want a foreign runtime to load governed identity context while still remaining non-authoritative.

See also:

- [`../../portability.md`](../../portability.md)
- [`../../runtime/runtime-complements.md`](../../runtime/runtime-complements.md)

---

## Relationship To Existing Docs

- [`../../portability.md`](../../portability.md) — defines the existing emulation-ready bundle at the portability level
- [`../../portable-working-identity.md`](../../portable-working-identity.md) — explains how portable working identity can travel inside an emulation-ready bundle without granting merge authority
- [`../../identity-fork-protocol.md`](../../identity-fork-protocol.md) — source-repo sovereignty, staging, and merge rules still govern durable change
- [`../../state-proposals.md`](../../state-proposals.md) and [`../../../schema-registry/change-proposal.v1.json`](../../../schema-registry/change-proposal.v1.json) — durable change returns through the existing governed proposal path

---

## Current Envelope vs Formal Contract

Grace-Mar already emits a **current narrow envelope** through:

- [`../../../scripts/export_emulation_bundle.py`](../../../scripts/export_emulation_bundle.py)
- [`../../../schema-registry/emulation-bundle-envelope.v1.json`](../../../schema-registry/emulation-bundle-envelope.v1.json)

This PR adds a **formal portable-emulation contract schema** at:

- [`emulation-bundle-schema.v1.json`](emulation-bundle-schema.v1.json)

That contract schema is richer than the current emitted envelope. It documents the intended authority model and behavior-spec slots without changing the exporter in this PR.
In short: [`../../../schema-registry/emulation-bundle-envelope.v1.json`](../../../schema-registry/emulation-bundle-envelope.v1.json) validates what the exporter ships today, while [`emulation-bundle-schema.v1.json`](emulation-bundle-schema.v1.json) describes the fuller downstream contract Grace-Mar intends to converge toward.

---

## Why External Runtimes Cannot Merge

External runtimes cannot merge because the source Grace-Mar repo remains sovereign.

Foreign runtimes may:

- read governed exports
- reason over them
- produce WORK observations
- emit proposal envelopes

Foreign runtimes may **not**:

- approve proposals
- resolve contradictions as truth
- publish canonical state
- merge changes into the Record

Durable change must always return to the source repo through the existing governed review path.

---

## Why WORK / Record Separation Must Survive Export

Portable emulation only remains safe if the foreign runtime preserves the same separation Grace-Mar uses locally:

- **Record** — governed, durable, approved state
- **WORK** — local, runtime-scoped, non-canonical drafts or observations
- **Proposal** — candidate durable change requiring source-repo review

If a foreign runtime collapses WORK into Record, it stops being a bounded consumer and starts acting like an unauthorized writer.

---

## Lifecycle

Portable emulation follows this lifecycle:

1. export governed bundle
2. load into foreign runtime
3. construct governed context
4. produce answer, WORK observation, or proposal envelope
5. preserve contradictions rather than silently resolving them
6. export proposals back to Grace-Mar
7. route them through human review and the existing gate
8. merge approved changes only in the source repo
9. let the next export reflect approved state

---

## Authority Summary

| Action | Status |
|---|---|
| read Record | allowed, read-only |
| write WORK observation | allowed |
| write proposal envelope | allowed |
| write canonical Record | forbidden |
| approve proposal | forbidden |
| resolve contradiction as truth | forbidden |
| merge | forbidden |
| publish new canonical state | forbidden |

Portable emulation therefore has:

- `recordAuthority: none`
- `gateEffect: none`

---

## See Also

- [`portable-emulation-layer.md`](portable-emulation-layer.md)
- [`behavior-spec/v1-core-constitution.md`](behavior-spec/v1-core-constitution.md)
- [`behavior-spec/v1-record-boundaries.md`](behavior-spec/v1-record-boundaries.md)
- [`behavior-spec/v1-contradiction-policy.md`](behavior-spec/v1-contradiction-policy.md)
- [`behavior-spec/v1-proposal-envelope.md`](behavior-spec/v1-proposal-envelope.md)
- [`behavior-spec/v1-work-lane-policy.md`](behavior-spec/v1-work-lane-policy.md)
