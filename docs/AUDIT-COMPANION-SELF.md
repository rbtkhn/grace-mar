# Audit: Grace-Mar vs Companion-Self Concept

> Audit timestamp note: this audit predates the work-layer refactor. Where it lists `self-skill-work`, read that as the older taxonomy snapshot rather than current canon.

**Purpose:** Assess how well Grace-Mar (docs, prompts, code, profile) aligns with the **companion-self** concept: the dual meaning (companion's self + self that companions), the **self-\*** taxonomy (self-knowledge, self-curiosity, self-personality, self-skill-*, self-archive, self-library, self-memory, self-voice), and **triadic cognition** (Mind, Record, Voice; synonym tricameral mind). Companion-self is both the concept and the **template repository** ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)), the origin for Grace-Mar and future instances.

**Scope:** Conceptual and terminology alignment. Structure/template compliance (instance vs repo) is in [AUDIT-GRACE-MAR-VS-COMPANION-SELF-TEMPLATE](audit-grace-mar-vs-companion-self-template.md).

**Authority:** CONCEPTUAL-FRAMEWORK § companion self; AGENTS.md § Record and Voice; [ID-TAXONOMY § Companion self contains](id-taxonomy.md#companion-self-contains).

**Date:** 2026-02-26

---

## 1. Canonical Definition (Reference)

- **Companion self** = (1) the companion's self (human's self, externalized in the Record) + (2) the self that companions (Record + Voice that accompany the human). Ambiguity intentional. **Companion self = human–computer triadic cognition** (synonym: *tricameral mind*).
- **Companion self contains:** **self-knowledge** (IX-A), **self-curiosity** (IX-B), **self-personality** (IX-C), **self-skill-think**, **self-skill-write**, **self-archive**, **self-library**, **self-memory**, **self-voice** — see [ID-TAXONOMY](id-taxonomy.md) § Companion self contains and § Capitalization. (Legacy docs may cite **self-skill-work**; current canon uses work territories and `work-*.md`, not a self-skill for WORK.)

---

## 2. Doc and Governance Alignment

| Location | Companion self / self-* usage | Status |
|----------|-------------------------------|--------|
| **AGENTS.md** | Defines companion self, lists self-* components, points to ID-TAXONOMY; triadic cognition | ✅ Strong |
| **CONCEPTUAL-FRAMEWORK** | § companion self, "Companion self contains" list, self-voice as output channel; §8 triadic cognition | ✅ Strong |
| **ID-TAXONOMY** | "Companion self contains" table; standard labels self-skill-*, self-library, self-archive, self-memory, self-voice | ✅ Canonical |
| **SKILLS-MODULARITY** | Full module set (self-knowledge, self-personality, self-curiosity, self-library, self-skill-*); links to ID-TAXONOMY | ✅ Strong |
| **GRACE-MAR-CORE** | companion-self.com reference | ✅ Present |
| **IDENTITY-FORK-PROTOCOL** | self-skill-* labels; no "companion self" phrase (protocol is mechanism-focused) | ✅ Adequate |
| **ARCHITECTURE** | self-skill-*, self-memory, self-archive, self-library in file map | ✅ Adequate |
| **SKILLS-TEMPLATE** | self-skill-* and self-knowledge/curiosity/personality in analyst context | ✅ Adequate |
| **OPERATOR-WEEKLY-REVIEW** | "companion-self (template)" in template-sync step | ✅ Clear |

**Verdict:** Core docs and governance are aligned with the companion-self concept and self-* taxonomy. ID-TAXONOMY is the single source of truth for "companion self contains."

---

## 3. Bot and Prompt Alignment

| Surface | Findings | Status |
|---------|----------|--------|
| **bot/prompt.py — SYSTEM_PROMPT** | "Record", "Voice", "triadic cognition (MIND, RECORD, VOICE)", "companion", "Knowledge boundary"; "the user documents" / "we recall" in one line (could use "companion" for consistency) | ✅ Aligned; minor wording |
| **bot/prompt.py — ANALYST** | "companion gates", "Record (Grace-Mar)", "triadic cognition"; one explicit "self-personality / BUILD context" | ✅ Aligned |
| **bot/prompt.py — LOOKUP/REPHRASE** | No companion-self phrasing required | ✅ N/A |
| **PRP / profile LLM snippet** | "Triadic cognition (when explaining Grace-Mar): Mind, Record, Voice" | ✅ Aligned |

**Verdict:** Prompts reinforce Record, Voice, triadic cognition, and companion. They do not need to use the phrase "companion self" or every self-* label; the structure (Record = documented self, Voice = speaks when queried) is clear.

---

## 4. Profile and Public Surfaces

| Surface | Findings | Status |
|---------|----------|--------|
| **profile/index.html** | Tagline "Record · Voice · You" (triadic: You = Mind). No "companion self" — acceptable for minimal public page | ✅ Aligned |
| **README** | grace-mar.com + companion-self.com; "companion self concept / product" | ✅ Present |

**Verdict:** Public copy is consistent with triadic framing. "Companion self" is not required on the profile page.

---

## 5. Code and Scripts

| Location | Findings | Status |
|----------|----------|--------|
| **scripts/test_voice_linguistic_authenticity.py** | Describes "self-voice linguistic authenticity" | ✅ Taxonomy-aware |
| **Other scripts** | user_id, --user, etc. — technical identifiers; no need for "companion self" in code | ✅ Acceptable |

**Verdict:** Code uses Record/Voice/companion where relevant (prompts); self-* appears in test script naming. No code changes required for companion-self alignment.

---

## 6. Gaps and Optional Improvements

| Item | Severity | Recommendation |
|------|----------|----------------|
| **prompt.py** line ~11 | Low | Optional: use "the companion" instead of "the user" in the design-philosophy line ("the Record holds what the companion documents") for prose consistency. |
| **Narrative docs** (WHITE-PAPER, BUSINESS-PROSPECTUS, LETTER-TO-USER) | Low | Optionally introduce "companion self" once where explaining the product (e.g. "the companion self is Mind + Record + Voice") for narrative coherence. |
| **ID-TAXONOMY anchor** | — | CONCEPTUAL-FRAMEWORK and AGENTS already link to ID-TAXONOMY § Companion self contains. No change needed. |

---

## 7. Summary

| Dimension | Alignment |
|-----------|-----------|
| **Companion self (dual meaning)** | Defined and used in AGENTS, CONCEPTUAL-FRAMEWORK, ID-TAXONOMY; triadic framing in prompt and profile. |
| **self-* taxonomy** | ID-TAXONOMY is canonical; SKILLS-MODULARITY, SKILLS-TEMPLATE, ARCHITECTURE, prompt use the labels where relevant. |
| **Record / Voice / Mind** | Consistent in docs and prompts; profile tagline "Record · Voice · You" reinforces triadic cognition. |
| **Template vs concept** | Template audit (instance vs companion-self repo) is separate. This audit is conceptual only. |

**Conclusion:** Grace-Mar is **aligned** with the companion-self concept. The companion self (companion's self + self that companions) and the self-* taxonomy are documented, cross-referenced, and reflected in prompts and profile. Optional tweaks are minor (one prompt line, optional narrative use of "companion self" in business/operator docs).

---

*Audit performed per CONCEPTUAL-FRAMEWORK (companion self), AGENTS.md, and ID-TAXONOMY. Re-run after material changes to concept or taxonomy.*
