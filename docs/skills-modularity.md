# Skill Modularity — Formal Model

**Purpose:** Canonical specification of the Record’s modules (including self-knowledge, self-personality, self-curiosity, self-library, and the Record-bound skill modules THINK/WRITE), their boundaries, their relationship to the Voice, and the rule that outputs (bots, profile) are functions of the Record with WRITE as the linguistic shaper. It also defines the boundary between the Record and the separate work / execution layer.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md), [SKILLS-TEMPLATE](skills-template.md), [ARCHITECTURE](architecture.md)

**Status:** Active

---

## 1. Full module set (companion self / Record)

The Record (and the companion self) is composed of the following modules. Together they define who the companion is and what the Record can evidence about what they can do; the Voice and any written profile are functions of this set.

| Module (standard label) | Location | Scope |
|-------------------------|----------|--------|
| **self-knowledge** | self.md IX-A | Facts that entered awareness (post-seed knowledge) |
| **self-personality** | self.md IX-C | Observed behavioral patterns, values, speech traits, art style |
| **self-curiosity** | self.md IX-B | Topics that catch attention (post-seed curiosity) |
| **self-library** | users/[id]/self-library.md | Curated return-to store of references, canon works, and influential media; reference lane is query-first for answers |
| **self-skill-think** | self-skills.md THINK container | Intake, learning, comprehension (multimodal) |
| **self-skill-write** | self-skills.md WRITE container | Production (text, journal, stories); linguistic style source |
| **self-skill-work** | self-skill-work.md (split template) or embedded | Making and doing — objectives and project capability ([concept.md](concept.md) §4) |
| **self-skill-steward** | self-skill-steward.md (split template) or e.g. skill-steward.md | Governance literacy — gate vocabulary, chat vs Record, consent-aware review; **not** unsupervised merge authority |

Additional Record components (self-archive, self-memory, evidence logs) are defined in [ID-TAXONOMY](id-taxonomy.md#companion-self-contains). The Voice renders the full Record when it speaks; it draws on all of the above as appropriate.

**Separate but adjacent:** Work territories and instance work contexts are execution surfaces, not Record modules. They may use broader tools and model capability, but they enter the Record only through approved evidence and staged merges.

---

## 2. Record skill module set and labels

| Module | Standard label | Internal identifier | Scope |
|--------|----------------|---------------------|--------|
| **THINK** | self-skill-think | THINK container, READ-nnn | Intake, learning, comprehension (multimodal) |
| **WRITE** | self-skill-write | WRITE container, WRITE-nnn | Production (text, journal, stories, explanations) |
| **WORK** | self-skill-work | WORK container, CREATE-/ACT- as appropriate | Making and doing; project objectives and tasks |
| **STEWARD** | self-skill-steward | STEWARD section / file | Governance literacy — participation at the gate; evidenced, tier-sensitive |

The **formal minimal pair** for Voice linguistics and core capability indexing remains **THINK** and **WRITE**. **WORK** and **STEWARD** are **additional Record-bound capability surfaces** on the companion-self **split template** (and may appear as sections or sibling files under `users/[id]/` per instance layout). All follow the same boundary: capability and evidence in SKILLS; IX-A/B/C only via analyst/operator staging → gate → approval.

**Current shape guidance:** WRITE currently works best as a single pure capability container. THINK may include clearly labeled contextual domain overlays and goal-interpretation overlays when they help adjacent work contexts read the skill state, but those overlays do not create new self-skills. STEWARD should stay **coaching-oriented** — not a compliance scorecard.

### 2a. Work / execution layer

| Surface | Standard label | Location | Scope |
|---------|----------------|----------|-------|
| Work territory | `work-territory` | `docs/skill-work/work-*/` | Reusable execution domain, prompts, doctrine, and operator workflow |
| Instance work context | `work-context` | `users/[id]/work-*.md` | Live project state, goals, planning, and delivery context |

**Historical compatibility:** `BUILD` remains a legacy compatibility term in older docs, evidence references, and analyses. `CREATE-*` and `ACT-*` remain valid evidence IDs and are not renamed by this refactor.

---

## 3. Module boundaries (capability only)

Each Record skill module updates **only** its capability container in SKILLS. Modules do **not** extract or write knowledge, curiosity, or personality into SELF.

| Module | What it captures | What it does not do |
|--------|------------------|----------------------|
| **THINK** | Content consumed, modality, comprehension, inference, vocabulary, interests (intake); learning from doing | Does not stage IX-A / IX-B / IX-C candidates |
| **WRITE** | Vocabulary, complexity, style, expression, logic, growth (production) | Does not stage IX-A / IX-B / IX-C candidates |
| **WORK** | Project goals, tasks, execution habits, shipping evidence | Does not bypass gate for identity truth |
| **STEWARD** | Demonstrated gate vocabulary, review practice, boundary understanding | Does not confer merge authority or replace Mind |

**Work boundary:** Work territories may plan, execute, and use tools outside the Record skill boundary. They may use open-world model capability. But work surfaces do not write Record truth directly; any identity, knowledge, curiosity, personality, or evidence change still goes through RECURSION-GATE and companion approval.

**Analyst vs. modules:** The **analyst** (pipeline) extracts patterns for **self-knowledge (IX-A), curiosity (IX-B), and personality (IX-C)** from inputs and stages candidates to RECURSION-GATE → SELF. So one input can update both (1) a skill container (THINK/WRITE) for *capability*, and (2) SELF (IX-A/B/C) via analyst-staged candidates. The analyst serves SELF; the skill modules serve SKILLS. Work activity can also produce staged candidates or evidence, but only through the same gate. See [SKILLS-TEMPLATE § III](skills-template.md#iii-skill-interactions-and-the-self), [ARCHITECTURE § Multi-Dimension Signals](architecture.md#multi-dimension-signals).

---

## 4. Outputs as functions of the Record

### 4.1 Voice (Telegram bot, WeChat bot)

The **Voice** is the emulation layer that speaks when queried. Its output is a **function of the Record** (SELF, SKILLS, EVIDENCE, prompt). Within that:

- **Skill-write is the primary shaper of the linguistic layer.** The system prompt embeds WRITE-derived content: Lexile ceiling, “how you talk” rules, and literal writing samples that define voice. So the Telegram bot and WeChat bot outputs are **a function of skill-write** (and SELF, MEMORY, retrieval). WRITE does not *equal* the Voice; the Voice is a function of the whole Record, with WRITE supplying the style and level.

**Operator-facing WRITE doctrine** (calibrating **system outputs** to **Locals / X / YouTube comments** — preferences, craft rules — separate from instance `skill-write.md` evidence): [skill-write/README.md](skill-write/README.md) → [write-operator-preferences.md](skill-write/write-operator-preferences.md).

**Identity vs capability qualification:** `SELF` remains authoritative for **identity-facing truth** (personality, values, expressive feel, how Grace-Mar comes across). `SKILLS`, especially WRITE, remains authoritative for **capability-facing truth** (what she can reliably produce, at what level, under what constraints). So the linguistic layer may be primarily shaped by `skill-write` without turning WRITE into the owner of identity.

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

Skill-think adds **content and scope** (what the companion has taken in and can discuss inside the Record); approved evidence from work territories can add adjacent context. **Skill-write drives voice and written presentation** across bots and profile.

When the same pattern appears in both surfaces, read it by job:

- `SELF` owns the pattern as **identity / expressive style**
- `SKILLS.WRITE` owns the pattern as **demonstrated production capability**
- `EVIDENCE` anchors the artifact or event that justified both readings

---

## 5. Data flow (concise)

**One sentence:** **THINK and READ evidence** update **SKILLS + EVIDENCE** directly; **SELF IX-A/B/C** updates only through **RECURSION-GATE + approval** (analyst or operator). There is no automatic THINK → IX merge.

```
                    ┌── THINK / READ path (no gate to SELF IX) ──────────────────┐
                    │  skill-think.md + READ-* in self-evidence.md               │
"we read X" /       │       │                                                    │
operator log READ   │       ▼                                                    │
                    │  SKILLS.md THINK · interests / comprehension                │
                    └──────────────────────────────────────────────────────────────┘
                                          │
                    (same session may ALSO stage IX candidates — separate step)
                                          ▼
Input (conversation, artifact, "we did X")
    │
    ├──► Analyst or operator ──► RECURSION-GATE ──► [companion approval] ──► SELF (IX-A, IX-B, IX-C), ACT-*, prompt
    │
    ├──► Skill path (operator) ──► SKILLS (THINK / WRITE) + EVIDENCE (READ-*, WRITE-*)
    │
    └──► Work path (territory / operator / tool loop) ──► work-context + artifacts + optional staged candidates / evidence
```

**Optional on gate candidates:** When IX merge should trace to intake, include `intake_evidence_id: READ-XXXX` (or `evidence_ref`, same meaning) on the candidate YAML; merge writes it into the IX entry. Primary `evidence_id` on IX rows remains the pipeline **ACT-*** from approval.

- **Record** = SELF + SKILLS + EVIDENCE (and related pipeline files). The Record belongs to the companion.
- **Voice** = f(Record). Implemented by bot (e.g. Telegram, WeChat) + prompt + retrieval. Linguistic output = f(skill-write).
- **Work layer** = designated integration point for external APIs, agent loops, planning systems, delivery tooling, and **`docs/skill-work/**` territories**. It is adjacent to the Record, not a self-skill.
- **WORK execution layer** = operator + tooling + AI assistant that **executes** work-layer and skill-work tasks (draft, mirror, template diff). Same **stage-only** rule for Record: no direct merge into SELF / EVIDENCE / prompt without companion approval.

**Discipline as a capability surface.** The companion's value in WORK execution includes superhuman consistency — maintaining runbooks, mirrors, and protocol adherence without fatigue or emotional drift. The transcript evidence: bots on Polymarket won not with better strategies but with flawless execution (no fatigue at 3 a.m., no oversized positions on confident bets, no missed trades during lunch). When auditing skill-work patterns, track not just what the system can do but how reliably it does it. Execution discipline gaps are a primary leverage point.

---

## 5a. Identity vs instrument: Record skills and work

**self-knowledge** (IX-A) is an aspect of **identity** — what the companion knows (who they are). **Work** is an **instrument** for accomplishing tasks and projects.

- **IX-A shapes Record skill boundaries.** THINK (intake, comprehension) and WRITE (production, expression) are Record-bound and should stay aligned with what the companion knows and how the companion writes.
- **IX-A does not bound the work layer in the same way.** Work territories may use broader model capability, tools, APIs, and external systems to help plan or execute tasks.
- **The gate still applies.** Work outputs do not become Record truth unless they are written down, staged as needed, and approved into SELF / EVIDENCE / prompt.
- The **WORK execution layer** implements the work layer day to day (runbooks, mirrors, sync). Optional **pattern** sync stays in **operator / tooling space** until it would change **protocol, merged Record truth, or Voice** — then it must go through the same gate (or explicit companion policy), not silent file copy.

## 5b. Reference assist in WORK territories

`SELF-LIBRARY` (including `CIV-MEM`) may assist **WORK** execution as a governed reference layer. This is a **lookup / grounding** function for work outputs, not a transfer of ownership into `SKILLS` or `SELF`.

- **Who uses it:** The **work layer** and **WORK execution layer** may call CMC or other SELF-LIBRARY routing while planning, drafting, or synthesizing work artifacts.
- **What it is for:** Better factual grounding, stronger analogies, richer synthesis, and clearer provenance in instrumental outputs.
- **What it is not:** It does not make `WRITE` the owner of reference access, and it does not turn a library lookup into Record truth by itself.

When work outputs involve `WRITE`, read the roles separately:

- `SELF` still owns identity and Voice-facing expressive style
- `SKILLS.WRITE` still owns demonstrated writing capability and current ceiling
- `SELF-LIBRARY` / `CIV-MEM` supplies governed reference material
- `EVIDENCE` anchors any approved artifact or activity that should persist

Operational constraints:

- Reference access is **lookup-only** unless a separate gated merge writes something into the Record.
- Work use of `SELF-LIBRARY` does **not** automatically create `READ-*` evidence.
- Any durable `SKILLS`, `SELF`, or `EVIDENCE` update remains a separate pipeline decision under the same gate.
- Citations and provenance rules should be enforced by the relevant work harness or export path, not assumed to already exist everywhere in the Record pipeline.

---

## 6. Invariants

1. **Stage-only for Record updates.** No skill module, work territory, or analyst merges directly into SELF, EVIDENCE, or prompt. All merges go through companion approval (RECURSION-GATE → process_approved_candidates).
2. **Evidence-linked.** Every capability claim in SKILLS traces to evidence. Historical `CREATE-*` / `ACT-*` references remain valid; new work evidence may still use them where appropriate.
3. **Knowledge boundary.** No undocumented facts enter the Record. The Voice abstains when outside documented knowledge and offers to look up.
4. **Work is broader than the Record.** Work territories may use broader tools and knowledge sources, but they do not redefine the Record without the gate.
5. **Record vs. Voice.** The Record is the documented self; the Voice speaks the Record when queried. WRITE is part of the Record that shapes the Voice; WRITE is not the Voice itself.

---

## 7. Cross-references

| Topic | Where defined |
|-------|----------------|
| Full module set (self-knowledge, self-personality, self-curiosity, self-library, self-skill-*) | This doc §1; [ID-TAXONOMY § Companion self contains](id-taxonomy.md#companion-self-contains) |
| Record skill modules (THINK, WRITE) | [SKILLS-TEMPLATE § II](skills-template.md#ii-the-record-bound-skill-modules), [ARCHITECTURE § The Record-Bound Skill Modules](architecture.md#the-record-bound-skill-modules) |
| Work layer | This doc §2a, §5a; [SKILLS-TEMPLATE § II-A](skills-template.md#ii-a-separate-work--execution-layer), [ID-TAXONOMY](id-taxonomy.md#work-layer-labels) |
| Standard labels (self-skill-*) | [ID-TAXONOMY](id-taxonomy.md#standard-capability-labels-self-skill-) |
| Analyst vs. skill modules (IX-A/B/C) | [SKILLS-TEMPLATE § III](skills-template.md#iii-skill-interactions-and-the-self), [ARCHITECTURE § Multi-Dimension Signals](architecture.md#multi-dimension-signals) |
| Record and Voice | [CONCEPTUAL-FRAMEWORK](conceptual-framework.md), [AGENTS](AGENTS.md) |
| Pipeline and merge | [PIPELINE-MAP](pipeline-map.md), [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md) |
| THINK/READ vs SELF IX (no auto-merge) | This doc §5; [we-read-think-self-pipeline.md](we-read-think-self-pipeline.md) |

---

*Last updated: March 2026*
