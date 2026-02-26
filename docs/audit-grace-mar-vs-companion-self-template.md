# Audit: Grace-Mar vs Companion-Self Template

**Purpose:** Assess how well the grace-mar **instance** aligns with the companion-self **template** specification. Companion-self is the template repo ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)) — concept, protocol, seed, structure — and the origin for Grace-Mar and future instances. The template is defined in [COMPANION-SELF-BOOTSTRAP](../companion-self-bootstrap.md), [COMPANION-SELF-DEVELOPER-PLAN](companion-self-developer-plan.md), and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md). Grace-mar is the reference implementation and the source from which the template was extracted; this audit checks that the instance has the structure, docs, and behavior the template expects.

**Scope:** Structure, concept compliance, protocol compliance, schema alignment, governance, and sync readiness. Not a full security or UX audit.

**Date:** February 2026

---

## 1. Template expectations for an instance

From the bootstrap and merge doc, an **instance** (e.g. grace-mar) is expected to:

- Have a **Record** under `users/<id>/`: SELF, SKILLS, EVIDENCE, PENDING-REVIEW, and related pipeline/archive files.
- Run a **bot** (or equivalent Voice) and **pipeline** (stage → approve → merge).
- Hold **instance-specific config** (e.g. Telegram, domain, PRP output) that is never overwritten by template sync.
- Maintain **copies of template docs** (concept, protocol, schema templates, AGENTS) that can be updated when the template is updated.
- Follow the **Identity Fork Protocol** (stage only; no merge without approval; evidence linkage).
- Enforce the **knowledge boundary** and **operating modes** in agents.md.

---

## 2. Structure audit

| Expectation | Grace-mar | Status |
|-------------|-----------|--------|
| `users/<id>/` with one companion | `users/grace-mar/` present | ✅ |
| self.md | Present | ✅ |
| skills.md | Present | ✅ |
| self-evidence.md | Present | ✅ |
| pending-review.md | Present | ✅ |
| memory.md | Optional; present | ✅ |
| self-archive.md | Present (gated; written only on merge) | ✅ |
| session-transcript.md / SESSION-LOG | Present | ✅ |
| pipeline-events.jsonl | Present | ✅ |
| library.md | Present | ✅ |
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
| Agent may stage, may not merge | Analyst stages to PENDING-REVIEW; merge only via `process_approved_candidates.py` after human approval | ✅ |
| No direct merge into SELF/EVIDENCE/prompt without staging and approval | AGENTS §2; no code path merges without approval | ✅ |
| Evidence linkage (claims traceable) | EVIDENCE entries, ACT-*, CREATE-*, WRITE-*; provenance in SELF IX entries | ✅ |
| Manual gate only (no autonomous merge) | Documented in AGENTS and IDENTITY-FORK-PROTOCOL; no autonomous merge path | ✅ |

**Verdict:** Protocol is followed. Grace-mar is a valid reference implementation for the template protocol doc.

---

## 5. Schema alignment (template paths)

Template paths that instances sync *from* companion-self (grace-mar holds copies received via sync) are listed in MERGING-FROM-COMPANION-SELF §1. Grace-mar should have these files so it can receive template updates from companion-self.

| Template path | In grace-mar | Notes |
|---------------|--------------|--------|
| docs/conceptual-framework.md | ✅ | Present |
| docs/architecture.md | ✅ | Present |
| docs/identity-fork-protocol.md | ✅ | Present |
| docs/self-template.md | ✅ | Present |
| docs/skills-template.md | ✅ | Present (WORK rename reflected) |
| docs/evidence-template.md | ✅ | Present |
| docs/memory-template.md | ✅ | Present |
| agents.md | ✅ | Present (self-skill-work, SKILLS-MODULARITY ref) |
| Seed-phase definition | ✅ | ARCHITECTURE (Fork Lifecycle, Seeding), OPERATOR-BRIEF; SEED-PHASE-2/3 in users/grace-mar |

**Verdict:** All template paths exist in grace-mar. Schema and governance docs are in place (synced from companion-self; grace-mar receives updates, does not originate templates).

---

## 6. Governance and operating modes

| Item | Status |
|------|--------|
| Operating modes (Session, Pipeline, Query) defined in AGENTS | ✅ |
| Session: no merge; pipeline only on "we [did X]" or explicit processing | ✅ |
| Pipeline: stage to PENDING-REVIEW; process approved via script | ✅ |
| Query: read-only | ✅ |
| Knowledge boundary rule (no undocumented facts in Record) | ✅ |
| Lexile / WRITE-derived voice (skill-write) | ✅ (prompt, SKILLS-MODULARITY) |
| No "parent" language; companion terminology | ✅ |

**Verdict:** Governance and operating modes match the template’s expectations.

---

## 7. Gaps and recommendations

### 7.1 Minor / optional

- **Template sync log (MERGING-FROM-COMPANION-SELF §3):** Still empty (“none yet”). Acceptable until the first pull from a live companion-self repo; then log each sync.
- **Optional diff script (MERGING-FROM-COMPANION-SELF §4):** Not implemented. Low priority until companion-self has stable content to diff against.
- **users/_template/ in template repo:** Not applicable to grace-mar; that’s for companion-self to add. Grace-mar correctly does not contain a generic _template/ (it has a real user, grace-mar).

### 7.2 Instance-only vs template

- Grace-mar contains **instance-only** docs (PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW, pilot/operator workflows, etc.). This is correct: they stay in the instance and are not overwritten by template sync. No change needed.
- **companion-self-bootstrap.md** lives in grace-mar root as the bootstrap for the companion-self repo. That’s intentional per §6: “This file can live in grace-mar; the companion-self repo now exists at https://github.com/rbtkhn/companion-self.” No change needed.

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
| Schema / template paths | ✅ Present |
| Governance & operating modes | ✅ Aligned |
| Gaps | Minor only (sync log empty until first sync; optional diff script) |

**Conclusion:** Grace-mar is **compliant** with the companion-self template specification. The template repo is live at [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self). Grace-mar is the first **instance**; companion-self is the **template** (concept, protocol, seed, users/_template/). Grace-mar receives template updates via the merge checklist in MERGING-FROM-COMPANION-SELF without overwriting the Record or instance config.

---

*Audit performed per COMPANION-SELF-BOOTSTRAP and COMPANION-SELF-DEVELOPER-PLAN. Re-run after material changes to structure, protocol, or template expectations.*
