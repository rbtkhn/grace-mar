# Skill-work-companion-self

**Objective:** Eventually enable Grace-Mar to autonomously manage and improve the companion-self codebase — and to maintain proper sync between companion-self and grace-mar.

Companion-self is both the **concept** (companion's self + self that companions, self-* taxonomy, triadic cognition) and the **template repo** ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)). Grace-Mar is a private instance and working tool built from that template. This submodule scopes: (1) **sync** — keeping grace-mar aligned with companion-self; (2) **contribution back** — proposing improvements upstream.

**Canonical framing:** `companion-self` is the upstream template and public architecture for sovereign, evidence-grounded cognitive forks. `grace-mar` is the private proving ground and active instance: a working tool where structural ideas are tested against real use. Improvements developed in `grace-mar` that are structural, reusable, and instance-agnostic may be merged back into `companion-self`; Record content, private workflows, and instance-specific state remain private to `grace-mar`.

## Related territory: integration / OpenClaw (not template merge)

**[`work-dev`](../work-dev/README.md)** — Record export, OpenClaw handback (stage-only), session continuity contract, integration status, provenance. Template sync does **not** replace integration work; cross-check exports after material template merges per [INTEGRATION-PROGRAM.md](../work-dev/INTEGRATION-PROGRAM.md) if exports or hooks drift.

---

## Purpose

| Role | Description |
|------|-------------|
| **Sync (template → instance)** | Maintain proper sync between companion-self and grace-mar. Detect drift; stage or apply template updates per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md). Never overwrite Record or instance-specific content. |
| **Contribution back (instance → template)** | Grace-Mar (via Voice, Record, or agentic layer) identifies improvements, fixes, or enhancements to companion-self and proposes them upstream. |
| **Bidirectional flow** | Template → instance: sync. Instance → template: contributions. Both under companion gate. |

The companion remains sovereign. Autonomous management means Grace-Mar operates within bounds the companion approves; merge into companion-self (or any upstream) still requires human gate.

**Open Brain / Nate Jones stack?** If you use **capture + embeddings + semantic search** (MCP, Slack, etc.) and are new to companion-self, read **[companion-self-for-open-brain-users.md](companion-self-for-open-brain-users.md)** first — it maps **retrieval** vs **gated Record** so you do not merge identity by accident.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, purpose, and principles. |
| **[roadmap.md](roadmap.md)** | Phased roadmap: read/audit → suggest → stage PRs → (future) autonomous within bounds. |
| **[audit-report.md](audit-report.md)** | Latest template diff (grace-mar paths). Run: `python scripts/template_diff.py -o docs/skill-work/work-companion-self/audit-report.md` (default template path: `./companion-self`; see [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md) §0) |
| **[audit-report-manifest.md](audit-report-manifest.md)** | Latest template diff (companion-self manifest paths). Run: `python scripts/template_diff.py --use-manifest -o docs/skill-work/work-companion-self/audit-report-manifest.md` (add `--include-skill-work` only for the broader WORK-tree audit). |
| **[TEMPLATE-BASELINE.md](TEMPLATE-BASELINE.md)** | Historical governance baseline, useful as context but no longer the primary machine pin once `instance-contract.json` / `template-source.json` are current. |
| **[COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md](COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md)** | SELF-LIBRARY template alignment notes (merged upstream). |
| **[CURSOR-PERSONAS-RULES-SKILLS.md](CURSOR-PERSONAS-RULES-SKILLS.md)** | Product spec: **template contributor** vs **new instance owner** — which `.cursor` rules and skills to add in companion-self (phase 1 vs 2). |
| **[companion-self-for-open-brain-users.md](companion-self-for-open-brain-users.md)** | Bridge for **Open Brain** / capture+MCP+search users: comparison table, anti-patterns, gate vs retrieval. |
| **§ [Three-track alignment](#three-track-alignment-operator-policy)** | Operator policy: governance/protocol diffs, manifest rhythm, optional DESIGN upstream. |

---

## Principles

1. **Gated pipeline** — Grace-Mar may read, analyze, suggest, and stage. Companion (or template maintainer) approves before merge into companion-self or sync (template→instance). AGENTS: agent may stage; it may not merge.
2. **Sync: never overwrite Record** — When merging template into grace-mar, never overwrite `users/grace-mar/`, instance config, or Record. Per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).
3. **Knowledge boundary** — Grace-Mar contributes only from documented Record and instance experience. No leaking LLM knowledge into template.
4. **Template-first** — Changes proposed to companion-self must align with template governance (concept, self-* taxonomy, triadic cognition). Instance-specific content stays in grace-mar.
5. **Audit trail** — Proposals, PRs, sync events, and contributions are tracked. Provenance preserved.
6. **Companion sovereignty** — "Autonomous" means Grace-Mar operates within approved scope (e.g., docs only, scripts only, specific paths). Companion sets boundaries.

---

## Three-track alignment (operator policy)

Grace-mar and companion-self are **not** chasing full file parity. Use these three tracks when the template moves or when you audit drift.

### Track 1 — Shared governance and protocol

**Goal:** No silent **behavioral** drift on gate semantics, merge rules, evidence linkage, or knowledge boundary — so new instances that fork the template are not misled.

- After each **material** companion-self bump, review the **“Differ (both exist, content differs)”** section in the manifest report (especially `docs/identity-fork-protocol.md` and related gate / boundary docs).
- **Prioritize diffs that change behavior** (what companions, operators, or tooling must *do*). Defer or batch **wording-only** cleanups unless they remove ambiguity about behavior.
- When grace-mar uses a **different filename** than the template but the same idea (e.g. `conceptual-framework.md` vs `concept.md`), prefer an explicit **mapping sentence** in the sync log or merge slice notes over duplicating files.

### Track 2 — Manifest-first rhythm

**Goal:** Template inventory drives what to compare; audits stay current without merge theater.

1. Pull or pin companion-self `main` (or your target tag); note `HEAD` / `template-version.json`.
2. Refresh the audit artifact:
   `python3 scripts/template_diff.py --use-manifest -o docs/skill-work/work-companion-self/audit-report-manifest.md`
   Add `--include-skill-work` only when you intentionally want the larger WORK-tree comparison.
3. Reconcile **only** slices that matter for **protocol, schemas, validators, or operator-facing contract** — per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md) §2a (small merges, hand merge, log §3).
4. Do not treat a long **“instance additions”** list as debt; instance-only `docs/skill-work/**` is expected.

**Pin rule:** treat `instance-contract.json` as the **target** contract and `template-source.json` as the **applied** provenance record. Audit work should report both when they differ instead of assuming one file can do both jobs.

### Track 3 — DESIGN.md and `validate-design-md.py` (optional upstream)

**Goal:** Either promote instance-proven UI spec to the template **once**, or keep it **instance-local** without implied parity.

- **Upstream port:** If new instances should share the same agent-readable UI tokens and checks, open a single companion-self change set: template-appropriate `DESIGN.md` (e.g. under `users/_template/` or `docs/`) + optional validator under `scripts/`, wired in template CI if desired.
- **Instance-local:** Keep [`users/grace-mar/DESIGN.md`](../../../users/grace-mar/DESIGN.md) and [`scripts/validate-design-md.py`](../../../scripts/validate-design-md.py) only in grace-mar; do not block template sync on DESIGN parity.

This track is **discretionary** — unlike Track 1 and 2, it is not a recurring merge obligation.

---

## Reconciliation code audit (upstream and downstream)

Any **template + boundary audit** (including [coffee](../../../.cursor/skills/coffee/SKILL.md) **A**; legacy hey **A** still works) should end with an explicit **reconciliation code** subsection — not only doc drift. **Reconciliation code** means scripts, validators, CI recipes, manifest/index tooling, or hooks that **compare, merge, validate, or sync** template ↔ instance.

| Direction | Question | Be specific |
|-----------|----------|-------------|
| **Upstream** (grace-mar → companion-self) | What instance-hardened tooling should **all** template consumers get? | Repo-relative paths in **grace-mar** (e.g. `scripts/…`), one-line **why**, suggested **companion-self** target path if known (e.g. `scripts/`, `.github/workflows/`). |
| **Downstream** (companion-self → grace-mar) | What does the template ship that grace-mar should **adopt** to stay aligned? | Paths in **companion-self** (e.g. `node scripts/validate-template.js`), **how** to pull (merge slice, copy, flag parity), and any **command** the operator should run. |

If there is **no** tooling delta this pass, state **`Reconciliation code: none`** and one line (e.g. “manifest diff was docs-only; `template_diff.py` unchanged on both sides”).

This block is **advisory** — it does not merge or open PRs; it gives the operator a checklist for the next sync or upstream PR.

---

## Upstreamability Test

Before proposing a `grace-mar` change back to `companion-self`, ask:

1. **Is it structural?** Docs, schema, tooling, governance, bootstrap, sync process, and reusable architecture are candidates for upstreaming.
2. **Is it instance-agnostic?** If it depends on `users/grace-mar/`, private operator workflow, local deployment details, or Grace-Mar-specific state, keep it in `grace-mar`.
3. **Does it preserve template purity?** `companion-self` must stay free of live Record data, private artifacts, and instance-only assumptions.
4. **Can it be generalized cleanly?** If the change is mixed, separate the reusable part before proposing it upstream.
5. **Is provenance clear?** Note whether the idea came from instance operation, a sync audit, or a private workflow that was later generalized.

---

## Operator Instruction Pattern

When the operator wants work to happen in `grace-mar` first and then flow back into the template, the canonical instruction is:

`Implement this in grace-mar first, then promote the reusable template layer to companion-self.`

Short form:

`Upstream this from grace-mar to companion-self.`

Implied meaning:

1. Build or refine the change in `grace-mar`.
2. Apply the upstreamability test.
3. Separate reusable structure from instance-specific material.
4. Keep `users/grace-mar/`, private workflows, deployment quirks, and live Record state in `grace-mar`.
5. Prepare only the structural, instance-agnostic layer for `companion-self`.

---

## Cross-references

- [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md) — Template → instance flow
- [AUDIT-COMPANION-SELF](../../AUDIT-COMPANION-SELF.md) — Concept alignment
- [audit-grace-mar-vs-companion-self-template](../../audit-grace-mar-vs-companion-self-template.md) — Instance vs template
- [COMPANION-SELF-BOOTSTRAP](../../../bootstrap/companion-self-bootstrap.md) — Workspace boundary, sync contract
