# Skill Modularity — Formal Model

**Purpose:** Canonical specification of the Record’s modules (including self-knowledge, self-personality, self-curiosity, self-library, and the three skill modules READ/WRITE/WORK), their boundaries, their relationship to the Voice, and the rule that outputs (bots, profile) are functions of the Record with WRITE as the linguistic shaper.

**Governed by:** [GRACE-MAR-CORE](grace-mar-core.md), [SKILLS-TEMPLATE](skills-template.md), [ARCHITECTURE](architecture.md)

**Status:** Active

---

## 1. Full module set (companion self / Record)

The Record (and the companion self) is composed of the following modules. Together they define who the companion is and what they can do; the Voice and any written profile are functions of this set.

| Module | Standard label | Location | Scope |
|--------|----------------|----------|--------|
| **Self-knowledge** | self-knowledge | self.md IX-A | Facts that entered awareness (post-seed knowledge) |
| **Self-personality** | self-personality | self.md IX-C | Observed behavioral patterns, values, speech traits, art style |
| **Self-curiosity** | self-curiosity | self.md IX-B | Topics that catch attention (post-seed curiosity) |
| **Self-library** | self-library | users/[id]/library.md | Curated lookup sources (books, reference works, videos); query-first for answers |
| **Self-skill-read** | self-skill-read | skills.md READ container | Intake, comprehension (multimodal) |
| **Self-skill-write** | self-skill-write | skills.md WRITE container | Production (text, journal, stories); linguistic style source |
| **Self-skill-work** | self-skill-work | skills.md BUILD container | Making, planning, execution, exchange, creation |

Additional Record components (self-archive, self-memory, evidence logs) are defined in [ID-TAXONOMY](id-taxonomy.md#companion-self-contains). The Voice renders the full Record when it speaks; it draws on all of the above as appropriate.

---

## 2. Skill module set and labels

| Module | Standard label | Internal identifier | Scope |
|--------|----------------|---------------------|--------|
| **READ** | self-skill-read | READ container, READ-nnn | Intake, comprehension (multimodal) |
| **WRITE** | self-skill-write | WRITE container, WRITE-nnn | Production (text, journal, stories, explanations) |
| **WORK** | self-skill-work | BUILD container, CREATE-nnn, ACT-nnn | Making, planning, execution, exchange, creation |

The third skill module is **WORK** in prose and design. The **BUILD** container name and evidence prefixes (CREATE-, ACT-) remain for compatibility and are not renamed in skills.md or EVIDENCE.

---

## 3. Module boundaries (capability only)

Each module updates **only** its capability container in SKILLS. Modules do **not** extract or write knowledge, curiosity, or personality into SELF.

| Module | What it captures | What it does not do |
|--------|------------------|----------------------|
| **READ** | Content consumed, modality, comprehension, inference, vocabulary, interests (intake) | Does not stage IX-A / IX-B / IX-C candidates |
| **WRITE** | Vocabulary, complexity, style, expression, logic, growth (production) | Does not stage IX-A / IX-B / IX-C candidates |
| **WORK** | Planning, execution, making, creation (originality, elaboration, flexibility), decision-making, financial, collaboration | Does not stage IX-A / IX-B / IX-C candidates |

**Analyst vs. modules:** The **analyst** (pipeline) extracts patterns for **self-knowledge (IX-A), curiosity (IX-B), and personality (IX-C)** from inputs and stages candidates to PENDING-REVIEW → SELF. So one input can update both (1) a skill container (READ/WRITE/WORK) for *capability*, and (2) SELF (IX-A/B/C) via analyst-staged candidates. The analyst serves SELF; the skill modules serve SKILLS. See [SKILLS-TEMPLATE § III](skills-template.md#skill-modules-vs-self-ix-abc), [ARCHITECTURE § Multi-Dimension Signals](architecture.md#multi-dimension-signals).

---

## 4. Outputs as functions of the Record

### 4.1 Voice (Telegram bot, WeChat bot)

The **Voice** is the emulation layer that speaks when queried. Its output is a **function of the Record** (SELF, SKILLS, EVIDENCE, prompt). Within that:

- **Skill-write is the primary shaper of the linguistic layer.** The system prompt embeds WRITE-derived content: Lexile ceiling, “how you talk” rules, and literal writing samples that define voice. So the Telegram bot and WeChat bot outputs are **a function of skill-write** (and SELF, MEMORY, retrieval). WRITE does not *equal* the Voice; the Voice is a function of the whole Record, with WRITE supplying the style and level.

### 4.2 Written / HTML profile

Any **written or HTML profile** that displays the companion’s identity (interests, style, writing samples, capability summary) is also a **function of the Record**. The *written presentation* (language level, tone, excerpts) is **a function of skill-write**, because WRITE provides the linguistic style and the artifacts (journal, samples) that are shown. So:

- **Telegram bot output** = f(Record); linguistic layer = f(skill-write).
- **WeChat bot output** = f(Record); linguistic layer = f(skill-write).
- **HTML (or any written) profile** = f(Record); written presentation = f(skill-write).

### 4.3 Summary

| Output | Function of | Linguistic / written layer |
|--------|-------------|----------------------------|
| Voice (Telegram, WeChat) | Record (SELF, SKILLS, EVIDENCE, prompt) | f(skill-write) |
| HTML / written profile | Record | f(skill-write) |

Skill-read and skill-work add **content and scope** (what to talk about, what the companion can do); **skill-write drives voice and written presentation** across bots and profile.

---

## 5. Data flow (concise)

```
Input (conversation, artifact, "we did X")
    │
    ├──► Analyst ──► PENDING-REVIEW ──► [companion approval] ──► SELF (IX-A, IX-B, IX-C), EVIDENCE, prompt
    │
    └──► Skill path (operator or pipeline) ──► SKILLS (READ / WRITE / WORK container) + EVIDENCE (READ-nnn, WRITE-nnn, CREATE-nnn, ACT-nnn)
```

- **Record** = SELF + SKILLS + EVIDENCE (and related pipeline files). The Record belongs to the companion.
- **Voice** = f(Record). Implemented by bot (e.g. Telegram, WeChat) + prompt + retrieval. Linguistic output = f(skill-write).
- **WORK (BUILD container)** = designated integration point for future external APIs (marketplaces, creation tools, planning/financial systems, content platforms). See [SKILLS-TEMPLATE § WORK](skills-template.md#work-making-planning-execution-exchange).

---

## 6. Invariants

1. **Stage-only for modules and analyst.** No skill module and no analyst merges directly into SELF, EVIDENCE, or prompt. All merges go through companion approval (PENDING-REVIEW → process_approved_candidates).
2. **Evidence-linked.** Every capability claim in SKILLS traces to evidence (WRITE-nnn, READ-nnn, CREATE-nnn, ACT-nnn).
3. **Knowledge boundary.** No undocumented facts enter the Record. The Voice abstains when outside documented knowledge and offers to look up.
4. **Record vs. Voice.** The Record is the documented self; the Voice speaks the Record when queried. WRITE is part of the Record that shapes the Voice; WRITE is not the Voice itself.

---

## 7. Cross-references

| Topic | Where defined |
|-------|----------------|
| Full module set (self-knowledge, self-personality, self-curiosity, self-library, self-skill-*) | This doc §1; [ID-TAXONOMY § Companion self contains](id-taxonomy.md#companion-self-contains) |
| Three skill modules (READ, WRITE, WORK) | [SKILLS-TEMPLATE § II](skills-template.md#ii-the-three-modules), [ARCHITECTURE § The Three Modules](architecture.md#the-three-modules) |
| Standard labels (self-skill-*) | [ID-TAXONOMY](id-taxonomy.md#standard-capability-labels-self-skill-) |
| Analyst vs. skill modules (IX-A/B/C) | [SKILLS-TEMPLATE § III](skills-template.md#skill-modules-vs-self-ix-abc), [ARCHITECTURE § Multi-Dimension Signals](architecture.md#multi-dimension-signals) |
| Record and Voice | [CONCEPTUAL-FRAMEWORK](conceptual-framework.md), [AGENTS](agents.md) |
| Pipeline and merge | [PIPELINE-MAP](pipeline-map.md), [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md) |

---

*Last updated: February 2026*
