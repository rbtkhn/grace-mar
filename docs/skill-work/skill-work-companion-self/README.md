# Skill-work-companion-self

**Objective:** Eventually enable Grace-Mar to autonomously manage and improve the companion-self codebase — and to maintain proper sync between companion-self and grace-mar.

Companion-self is both the **concept** (companion's self + self that companions, self-* taxonomy, tricameral mind) and the **template repo** ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)). Grace-Mar is an instance. This submodule scopes: (1) **sync** — keeping grace-mar aligned with companion-self; (2) **contribution back** — proposing improvements upstream.

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
| **[audit-report.md](audit-report.md)** | Latest template diff (grace-mar paths). Run: `python scripts/template_diff.py -o docs/skill-work/skill-work-companion-self/audit-report.md` |
| **[audit-report-manifest.md](audit-report-manifest.md)** | Latest template diff (companion-self manifest paths). Run: `python scripts/template_diff.py --use-manifest -o docs/skill-work/skill-work-companion-self/audit-report-manifest.md` |

---

## Principles

1. **Gated pipeline** — Grace-Mar may read, analyze, suggest, and stage. Companion (or template maintainer) approves before merge into companion-self or sync (template→instance). AGENTS: agent may stage; it may not merge.
2. **Sync: never overwrite Record** — When merging template into grace-mar, never overwrite `users/grace-mar/`, instance config, or Record. Per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).
3. **Knowledge boundary** — Grace-Mar contributes only from documented Record and instance experience. No leaking LLM knowledge into template.
4. **Template-first** — Changes proposed to companion-self must align with template governance (concept, self-* taxonomy, tricameral). Instance-specific content stays in grace-mar.
5. **Audit trail** — Proposals, PRs, sync events, and contributions are tracked. Provenance preserved.
6. **Companion sovereignty** — "Autonomous" means Grace-Mar operates within approved scope (e.g., docs only, scripts only, specific paths). Companion sets boundaries.

---

## Cross-references

- [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md) — Template → instance flow
- [AUDIT-COMPANION-SELF](../../AUDIT-COMPANION-SELF.md) — Concept alignment
- [audit-grace-mar-vs-companion-self-template](../../audit-grace-mar-vs-companion-self-template.md) — Instance vs template
- [COMPANION-SELF-BOOTSTRAP](../../../companion-self-bootstrap.md) — Workspace boundary, sync contract
