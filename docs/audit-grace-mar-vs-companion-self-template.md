# Audit: Grace-Mar vs Companion-Self Template

**Purpose:** Assess how well the grace-mar **instance** aligns with the companion-self **template** specification. Companion-self is the template repo ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)) — concept, protocol, seed, structure — and the origin for Grace-Mar and future instances. The template is defined in [COMPANION-SELF-BOOTSTRAP](../bootstrap/companion-self-bootstrap.md), [COMPANION-SELF-DEVELOPER-PLAN](companion-self-developer-plan.md), and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md). Grace-mar is the reference implementation and the source from which the template was extracted; this audit checks that the instance has the structure, docs, and behavior the template expects. **See also:** [grace-mar vs companion-self](grace-mar-vs-companion-self.md) for a side-by-side instance vs template comparison.

**Scope:** Structure, concept compliance, protocol compliance, schema alignment, governance, and sync readiness. Not a full security or UX audit.

**Date:** March 2026

---

## 1. Template expectations for an instance

From the bootstrap and merge doc, an **instance** (e.g. grace-mar) is expected to:

- Have a **Record** under `users/<id>/`: SELF, SKILLS, EVIDENCE, RECURSION-GATE, and related pipeline/archive files.
- Run a **bot** (or equivalent Voice) and **pipeline** (stage → approve → merge).
- Hold **instance-specific config** (e.g. Telegram, domain, PRP output) that is never overwritten by template sync.
- Maintain **copies of template docs** (concept, protocol, schema templates, AGENTS) that can be updated when the template is updated.
- Follow the **Identity Fork Protocol** (stage only; no merge without approval; evidence linkage).
- Enforce the **knowledge boundary** and **operating modes** in AGENTS.md.

---

## 2. Structure audit

| Expectation | Grace-mar | Status |
|-------------|-----------|--------|
| `users/<id>/` with one companion | `users/grace-mar/` present | ✅ |
| self.md | Present | ✅ |
| skills.md | Present | ✅ |
| self-archive.md | Present — canonical **EVIDENCE** (activity spine + § VIII gated approved log per [canonical-paths.md](canonical-paths.md)) | ✅ |
| self-evidence.md | Optional compatibility pointer only; tooling prefers `self-archive.md` ([AGENTS.md](../AGENTS.md)) | ✅ (if present) |
| recursion-gate.md | Present | ✅ |
| memory.md | Optional; present | ✅ |
| session-transcript.md / SESSION-LOG | Present | ✅ |
| pipeline-events.jsonl | Present | ✅ |
| self-library.md | Present | ✅ |
| Artifacts (CREATE-*, WRITE-* evidence) | `users/grace-mar/artifacts/` | ✅ |
| Bot code | `bot/` (Telegram, WeChat, core, prompt) | ✅ |
| Merge script | `scripts/process_approved_candidates.py` | ✅ |
| PRP export | `scripts/export_prp.py`; output e.g. `grace-mar-llm.txt` | ✅ |
| Validation | `scripts/validate-integrity.py` | ✅ |
| Governance check | `scripts/governance_checker.py` | ✅ |

**Verdict:** Structure is complete. All template-expected instance components exist.

---

## 3. Concept compliance

The template concept (Mind + Record + Voice; cognitive fork; sovereign merge; knowledge boundary) must be reflected in the instance’s design and docs.

| Concept | Where in grace-mar | Status |
|---------|--------------------|--------|
| Record = documented self; Voice = speaks Record | CONCEPTUAL-FRAMEWORK, AGENTS, ARCHITECTURE | ✅ |
| Tricameral mind (Mind, Record, Voice) | AGENTS, CONCEPTUAL-FRAMEWORK, prompt/PRP | ✅ |
| Fork, not twin | CONCEPTUAL-FRAMEWORK, AGENTS | ✅ |
| Knowledge boundary (no LLM leak) | AGENTS §1, KNOWLEDGE-BOUNDARY-FRAMEWORK, prompt | ✅ |
| Sovereign merge (companion gates) | AGENTS §2, IDENTITY-FORK-PROTOCOL | ✅ |
| Evidence linkage | IDENTITY-FORK-PROTOCOL, EVIDENCE-TEMPLATE, File Update Protocol | ✅ |

**Verdict:** Concept is implemented and documented. Instance is suitable as the source for generalizing the template concept doc.

---

## 4. Protocol compliance (Identity Fork Protocol)

| Rule | Implementation | Status |
|------|----------------|--------|
| Agent may stage, may not merge | Analyst stages to RECURSION-GATE; merge only via `process_approved_candidates.py` after human approval | ✅ |
| No direct merge into SELF/EVIDENCE/prompt without staging and approval | AGENTS §2; no code path merges without approval | ✅ |
| Evidence linkage (claims traceable) | EVIDENCE entries, ACT-*, CREATE-*, WRITE-*; provenance in SELF IX entries | ✅ |
| Manual gate only (no autonomous merge) | Documented in AGENTS and IDENTITY-FORK-PROTOCOL; no autonomous merge path | ✅ |

**Verdict:** Protocol is followed. Grace-mar is a valid reference implementation for the template protocol doc.

---

## 5. Schema alignment (template paths)

Template alignment is now best understood in **two layers**:

1. **Concept / protocol alignment** — does grace-mar implement the same governing model?
2. **Manifest / path alignment** — does grace-mar mirror or explicitly account for the live template's current file surface?

Grace-mar remains strongly aligned on the first layer. The second layer is now **partial**, because the live companion-self repo has added template files and path names that are not yet fully reflected in grace-mar's local sync docs.

| Template path | In grace-mar | Notes |
|---------------|--------------|--------|
| `docs/identity-fork-protocol.md` | ✅ | Present, but differs from template copy |
| `docs/concept.md` | ⚠️ | No same-name file; concept is covered across `docs/conceptual-framework.md` and `docs/architecture.md` |
| `docs/seed-phase.md` | ⚠️ | No same-name file; seed phase is covered in ARCHITECTURE and operator docs |
| `docs/long-term-objective.md` | ❌ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `docs/two-hour-screentime-target.md` | ❌ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `docs/instance-patterns.md` | ❌ | Template-only path; not yet mirrored or explicitly mapped in grace-mar |
| `users/_template/` | Reference only | Correctly absent as a live instance path; should remain template-side |
| `template-manifest.json` / `template-version.json` | ⚠️ | Not tracked locally as sync anchors; no recorded baseline yet |
| Grace-mar schema mirrors (`docs/self-template.md`, `docs/skills-template.md`, `docs/evidence-template.md`, `docs/memory-template.md`, `AGENTS.md`) | ✅ | Present and still valid instance-side mirrors / elaborations |

**Verdict:** Grace-mar is **conceptually aligned** with the companion-self template, but **path / manifest alignment is partial**. The local instance still matches the template's governing model, yet the sync contract and audit docs lag the live template surface.

---

## 6. Governance and operating modes

| Item | Status |
|------|--------|
| Operating modes (Session, Pipeline, Query) defined in AGENTS | ✅ |
| Session: no merge; pipeline only on "we [did X]" or explicit processing | ✅ |
| Pipeline: stage to RECURSION-GATE; process approved via script | ✅ |
| Query: read-only | ✅ |
| Knowledge boundary rule (no undocumented facts in Record) | ✅ |
| Lexile / WRITE-derived voice (skill-write) | ✅ (prompt, SKILLS-MODULARITY) |
| No "parent" language; companion terminology | ✅ |

**Verdict:** Governance and operating modes match the template’s expectations.

---

## 7. Gaps and recommendations

### 7.1 Audit drift to fix

- **Local audit verdict is too strong:** Earlier wording said all template paths exist in grace-mar. That is no longer accurate against the live template manifest.
- **Template sync log / manifest diff:** [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md) §3 now records governance merges and manifest-diff refreshes; [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) is regenerated with `template_diff.py --use-manifest`. Governance baseline remains pinned in [TEMPLATE-BASELINE.md](skill-work/work-xavier/TEMPLATE-BASELINE.md) (`288b438`) while `main` may move — re-run the diff after pulls.
- **Manifest-first sync contract not yet fully internalized:** Grace-mar now acknowledges manifest-driven sync, but operator habit should treat `template-manifest.json` + diff report as the first stop on each sync.
- **users/_template/ in template repo:** Correctly absent in grace-mar as a live instance path. This is not a defect, but the audit should distinguish template-only scaffolds from missing instance mirrors.

### 7.2 Instance-only vs template

- Grace-mar contains **instance-only** docs (PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW, instance/operator workflows, etc.). This is correct: they stay in the instance and are not overwritten by template sync. No change needed.
- **`bootstrap/companion-self-bootstrap.md`** in grace-mar is the reference copy for the companion-self template. That’s intentional per §6: “This file can live in grace-mar; the companion-self repo now exists at https://github.com/rbtkhn/companion-self.” No change needed.

### 7.3 Naming and consistency

- **WORK vs BUILD:** Prose and standard labels use WORK; internal IDs (BUILD container, CREATE-nnn, ACT-nnn) unchanged. Aligns with the deliberate design; template, when extracted, should use the same convention (WORK in prose, BUILD as internal identifier where relevant).
- **SKILLS-MODULARITY:** Formal module set (including self-knowledge, self-personality, self-curiosity, self-library, self-skill-*) is documented. Template concept doc could reference this structure when generalizing.

### 7.4 Seed phase

- Seed phase is **defined** in ARCHITECTURE (Fork Lifecycle, Seeding) and **operationalized** in OPERATOR-BRIEF and in grace-mar’s SEED-PHASE-2-SURVEY, SEED-PHASE-3-SURVEY. The template’s seed-phase doc can be derived from these. No gap.

---

## 8. Summary

| Area | Result |
|------|--------|
| Structure | ✅ Complete |
| Concept compliance | ✅ Aligned |
| Protocol compliance | ✅ Aligned |
| Schema / template paths | ⚠️ Partial |
| Governance & operating modes | ✅ Aligned |
| Gaps | Path-level parity with template `main` remains partial; manifest diff report is refreshed on a schedule or after template pulls |

**Conclusion:** Grace-mar remains a valid **reference implementation** of the companion-self model, and it is still aligned on concept, protocol, and governance. **Path-level** alignment is partial by design (instance WORK tree is much larger than the template). The operator refreshes [audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) against companion-self `main` to see drift; governance merges stay pinned per [TEMPLATE-BASELINE.md](skill-work/work-xavier/TEMPLATE-BASELINE.md) until a new merge is recorded.

---

*Audit performed per COMPANION-SELF-BOOTSTRAP and COMPANION-SELF-DEVELOPER-PLAN. Re-run after material changes to structure, protocol, or template expectations.*
