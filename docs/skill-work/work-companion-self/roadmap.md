# Skill-work-companion-self — Roadmap

**Status:** Aspirational. Current state: manual template sync (instance pulls from companion-self). Phases 1–4 describe a path toward Grace-Mar autonomously managing/improving companion-self and maintaining proper sync within companion-approved bounds.

---

## Phase 0 — Current state

**Scope:** Manual. Operator merges from companion-self into grace-mar per [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md). No automated sync or contribution back.

| Deliverable | Status | Description |
|-------------|--------|-------------|
| **Sync (template → instance)** | Manual | Merge checklist, template paths, sync log. Operator performs merge. |
| **Audits** | Done | AUDIT-COMPANION-SELF (concept), AUDIT-GRACE-MAR-VS-COMPANION-SELF-TEMPLATE (structure). |
| **Instance → template** | None | No automated or agentic contribution flow. |

---

## Phase 1 — Read and audit

**Scope:** Grace-Mar (Voice or agentic layer) can read companion-self and run audits. Read-only; no writes. Foundation for sync and contribution.

| Deliverable | Description |
|-------------|-------------|
| **Template access** | Companion-self clone or API access for read. Grace-Mar reads template paths (docs, scripts, schema). |
| **Audit automation** | Script or agent: run AUDIT-COMPANION-SELF and AUDIT-GRACE-MAR-VS-COMPANION-SELF-TEMPLATE; report drift, concept alignment, structure gaps. |
| **Diff report (sync)** | Compare grace-mar vs companion-self on template paths. Report: (a) what template has that instance lacks (pull needed); (b) what instance has diverged. Enables sync prioritization. |
| **Placeholder script** | `scripts/template_diff.py` (mentioned in MERGING-FROM-COMPANION-SELF §4) — implement for diff report. |

**Output:** Reports only. No changes to either repo. Human performs sync (template → instance) manually using reports.

---

## Phase 2 — Suggest

**Scope:** Grace-Mar analyzes and suggests improvements. Suggestions staged in grace-mar (e.g., PENDING-REVIEW or a dedicated companion-self-contributions queue). Companion reviews; operator applies manually to companion-self.

| Deliverable | Description |
|-------------|-------------|
| **Suggestion schema** | Structured proposal: path, change type (fix, enhancement, doc update), rationale (from Record or instance evidence), diff or patch. |
| **Staging location** | `users/grace-mar/companion-self-proposals.md` or recursion-gate extension — proposals for companion review. |
| **Rationale from Record** | "Instance X shows drift in Y; template could add Z." Evidence-linked. Knowledge boundary: no LLM facts; only documented instance experience. |
| **Companion gate** | Companion approves or rejects. Approved → operator opens PR or patch to companion-self manually. |

**Output:** Proposals in grace-mar. Human performs actual contribution to companion-self.

---

## Phase 3 — Stage PRs / patches; stage sync

**Scope:** Grace-Mar generates patches or PR content for companion-self. For sync: stages template→instance merge (diff, paths to update); companion approves; operator applies. Companion approves; operator (or automation with companion approval) submits to companion-self.

| Deliverable | Description |
|-------------|-------------|
| **Patch generation** | Agent produces valid diff/patch for companion-self paths. Validated (schema, concept alignment) before staging. |
| **Sync staging** | Agent stages template→instance merge: diff report, paths to update, merge plan. Never overwrite users/grace-mar/, instance config, or Record. Companion approves; operator applies per MERGING-FROM-COMPANION-SELF. |
| **PR draft** | For GitHub: draft PR body, branch, commit message. Companion reviews; operator pushes. |
| **Contribution log** | Track: proposal ID, companion-self path, status (proposed, approved, submitted, merged), provenance. |
| **Bounds** | Companion defines scope: e.g., docs only, or scripts only, or specific paths. Grace-Mar does not touch users/, instance config, or governance core without explicit approval. |

**Output:** Ready-to-submit patches or PR drafts; sync staging for template→instance. Human still performs submission and sync apply.

---

## Phase 4 — Autonomous within bounds (future)

**Scope:** Grace-Mar autonomously proposes and, within approved bounds, may submit contributions to companion-self. Companion sets scope; approval gate remains for high-risk or governance-sensitive changes.

| Deliverable | Description |
|-------------|-------------|
| **Approved scope** | Companion defines: e.g., "docs/ only, no agents.md or identity-fork-protocol" or "typos, formatting, non-governance doc updates only." |
| **Sync detection** | Grace-Mar detects template changes; proposes sync (diff, paths). Companion approves; Grace-Mar applies to grace-mar (or stages for operator). Never overwrites Record or instance-specific content. |
| **Autonomous submit** | Within scope: Grace-Mar opens PRs or pushes to fork; companion-self maintainer (or CI) reviews. Grace-Mar does not merge; human gate upstream. |
| **Escalation** | Changes outside scope → Phase 2/3 flow (proposal, companion approval). |
| **Audit continuity** | After each contribution or sync, re-run audits to ensure alignment. |

**Constraints:**
- Grace-Mar never merges to companion-self main. PRs require human review upstream.
- Companion retains override: "pause companion-self contributions," "narrow scope," "reject all."
- Provenance on every change: which proposal, which evidence, companion approval ID.

---

## Summary

| Phase | Scope | Grace-Mar role | Human role |
|-------|-------|----------------|------------|
| **0 — Current** | Manual sync | None | Merge template → instance (sync); no contribution back |
| **1 — Read/audit** | Read companion-self | Run audits, diff reports (sync + contribution) | Review reports; perform sync manually |
| **2 — Suggest** | Analyze, propose | Stage proposals in grace-mar | Approve; operator submits to companion-self |
| **3 — Stage PRs** | Generate patches/PRs; sync staging | Produce ready-to-submit content; stage template→instance merges | Review; submit; approve sync |
| **4 — Autonomous** | Sync + contribution within bounds | Detect sync gaps; propose sync; open PRs to template | Set scope; approve sync; upstream review |

---

## Design guardrails (all phases)

1. **Gated pipeline** — Grace-Mar stages; companion approves. Merge into companion-self requires human gate. Sync (template→instance) also requires companion approval before apply.
2. **Sync: never overwrite Record** — Template merge into grace-mar never overwrites `users/grace-mar/`, instance config, or Record. Per MERGING-FROM-COMPANION-SELF.
3. **Knowledge boundary** — Contributions based on Record and instance evidence only. No LLM knowledge leak.
4. **Template governance** — Proposals align with companion-self concept, self-* taxonomy, tricameral framing.
5. **Instance/template boundary** — Instance-specific content stays in grace-mar. Template gets only generic improvements.
6. **Companion sovereignty** — Companion sets scope, pause, override. "Autonomous" = within approved bounds.
