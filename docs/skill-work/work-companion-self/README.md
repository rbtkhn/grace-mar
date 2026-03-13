# Skill-work-companion-self

**Objective:** Eventually enable Grace-Mar to autonomously manage and improve the companion-self codebase — and to maintain proper sync between companion-self and grace-mar.

Companion-self is both the **concept** (companion's self + self that companions, self-* taxonomy, tricameral mind) and the **template repo** ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)). Grace-Mar is a private instance and working tool built from that template. This submodule scopes: (1) **sync** — keeping grace-mar aligned with companion-self; (2) **contribution back** — proposing improvements upstream.

**Canonical framing:** `companion-self` is the upstream template and public architecture for sovereign, evidence-grounded cognitive forks. `grace-mar` is the private proving ground and active instance: a working tool where structural ideas are tested against real use. Improvements developed in `grace-mar` that are structural, reusable, and instance-agnostic may be merged back into `companion-self`; Record content, private workflows, and instance-specific state remain private to `grace-mar`.

---

## Purpose

| Role | Description |
|------|-------------|
| **Sync (template → instance)** | Maintain proper sync between companion-self and grace-mar. Detect drift; stage or apply template updates per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md). Never overwrite Record or instance-specific content. |
| **Contribution back (instance → template)** | Grace-Mar (via Voice, Record, or agentic layer) identifies improvements, fixes, or enhancements to companion-self and proposes them upstream. |
| **Bidirectional flow** | Template → instance: sync. Instance → template: contributions. Both under companion gate. |

The companion remains sovereign. Autonomous management means Grace-Mar operates within bounds the companion approves; merge into companion-self (or any upstream) still requires human gate.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, purpose, and principles. |
| **[roadmap.md](roadmap.md)** | Phased roadmap: read/audit → suggest → stage PRs → (future) autonomous within bounds. |
| **[audit-report.md](audit-report.md)** | Latest template diff (grace-mar paths). Run: `python scripts/template_diff.py -o docs/skill-work/work-companion-self/audit-report.md` |
| **[audit-report-manifest.md](audit-report-manifest.md)** | Latest template diff (companion-self manifest paths). Run: `python scripts/template_diff.py --use-manifest -o docs/skill-work/work-companion-self/audit-report-manifest.md` |

---

## Principles

1. **Gated pipeline** — Grace-Mar may read, analyze, suggest, and stage. Companion (or template maintainer) approves before merge into companion-self or sync (template→instance). AGENTS: agent may stage; it may not merge.
2. **Sync: never overwrite Record** — When merging template into grace-mar, never overwrite `users/grace-mar/`, instance config, or Record. Per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).
3. **Knowledge boundary** — Grace-Mar contributes only from documented Record and instance experience. No leaking LLM knowledge into template.
4. **Template-first** — Changes proposed to companion-self must align with template governance (concept, self-* taxonomy, tricameral). Instance-specific content stays in grace-mar.
5. **Audit trail** — Proposals, PRs, sync events, and contributions are tracked. Provenance preserved.
6. **Companion sovereignty** — "Autonomous" means Grace-Mar operates within approved scope (e.g., docs only, scripts only, specific paths). Companion sets boundaries.

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
- [COMPANION-SELF-BOOTSTRAP](../../../companion-self-bootstrap.md) — Workspace boundary, sync contract
