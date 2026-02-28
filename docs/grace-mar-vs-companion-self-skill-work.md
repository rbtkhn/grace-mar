# Grace-Mar vs Companion-Self: Skill-Work (WORK / BUILD) Comparison

**Purpose:** Compare how **skill-work** (self-skill-work, WORK module, BUILD container) is defined in the **companion-self template** vs how it is **instantiated** in the **grace-mar** pilot. Template = schema, intent, and governance; instance = concrete Record with evidence and levels.

**References:** Template: [SKILLS-TEMPLATE](skills-template.md) § WORK, [SKILLS-MODULARITY](skills-modularity.md). Instance: [users/grace-mar/skill-work.md](../users/grace-mar/skill-work.md), [analysis-grace-mar-skill-work](analysis-grace-mar-skill-work.md).

---

## 1. Role and label (same in both)

| Aspect | Template (companion-self) | Instance (grace-mar) |
|--------|---------------------------|----------------------|
| **Prose name** | WORK | WORK |
| **Standard label** | self-skill-work | self-skill-work |
| **Internal id** | BUILD container | BUILD container |
| **Evidence IDs** | CREATE-nnn, ACT-nnn | CREATE-nnn, ACT-nnn (e.g. CREATE-0001–0008, ACT-0035, ACT-0036) |
| **Scope** | Making, planning, execution, exchange, creation | Same; populated from evidence |

---

## 2. Module intent (aligned)

**Template:** WORK serves as tutor for the companion in the making, planning, execution, and creation domain — proposing activities at the container edge, answering questions, scaffolding next steps, aligned with work goals and life mission.

**Instance:** Same intent stated in `users/grace-mar/skill-work.md`; behavior implemented via bot, pipeline, and profile tooling.

---

## 3. What gets captured

| Dimension / area | Template (SKILLS-TEMPLATE) | Instance (grace-mar skill-work.md) |
|------------------|----------------------------|-------------------------------------|
| **Planning** | Goals, timelines, milestones | `planning_level: 1-2` (evidenced by ACT-0035: step order for drawing, lemonade stand) |
| **Execution** | Follow-through, deliverables | `execution_level: 1` (next step in sequence, e.g. Lego step 5) |
| **Making** | Following instructions, assembly | `making_level: 1` (Legos — instructions + box) |
| **Creation** | Originality, elaboration, flexibility (1–5) | `originality_level: 4`, `elaboration_level: 4`, `flexibility_level: 3` from CREATE-0001–0008 |
| **Decision-making** | Trade-offs, prioritization | `decision_making: 1` (can give reason for choice; ACT-0035) |
| **Financial** | P&L, budgeting, allowance | Template: yes. Instance: `financial_level: null` (no evidence yet) |
| **Collaboration** | Teamwork, roles, delegation | Template: yes. Instance: `collaboration_level: null` (no evidence yet) |
| **Marketing / audience** | Telling your story, reach | Template: yes. Instance: not yet a separate field; creation sharing in companion_creative_context |
| **Companion creative context** | — | Instance-only: household artistic style (ACT-0036) — context, not child capability |
| **SCHOOL** | — | Instance: `grade: first grade`, `school_type: not specified` |

Template defines the full schema and example activities (lemonade stand, food truck, allowance, Legos, content creation, drawing/art). Instance fills in only what evidence supports; nulls where no evidence yet.

---

## 4. Work goals and life mission

| Item | Template | Instance |
|------|----------|----------|
| **work_goals** | `near_term: []`, `horizon: []`, `source:` (evidence ID when captured); gated | `near_term: []`, `horizon: ["SAT score ≥ 1200"]`, `source: null` |
| **life_mission** | In SELF (self.md § VI VALUES); WORK goals align with it | `life_mission_ref: "self.md § VI VALUES (life_mission)"`; SELF has `life_mission: null` |
| **Governance** | Evidence-linked when captured; human-gated | Same; horizon goal present, not yet tied to an evidence ID |

---

## 5. Structure of the file

| Section | Template (schema) | Instance (grace-mar) |
|---------|-------------------|----------------------|
| **Header** | Module intent, link to skill-think/skill-write | Same + PILOT-001 |
| **Module objectives** | Example: bots, web app, self-library | Same three (grace-mar-specific) |
| **WORK Container** | YAML schema: status, levels (originality, elaboration, flexibility, planning, execution, making, financial, collaboration, decision_making), edge, gaps, notes | Populated: status ACTIVE, levels from CREATE/ACT, edge text, gaps [], notes with evidence refs |
| **Companion creative context** | Not in template | YAML from ACT-0036 (medium, frequency, finishing, sharing, one_word_style, etc.) |
| **SCHOOL** | Optional contextual block in instance | `grade: first grade` |
| **WORK GOALS** | work_goals schema | work_goals with horizon SAT ≥ 1200 |
| **LIFE MISSION REF** | Pointer to SELF | Pointer to self.md § VI VALUES |

---

## 6. Evidence and growth

| Aspect | Template | Instance |
|--------|----------|----------|
| **Starts from zero** | BUILD container empty until pipeline adds evidence | Was empty; now ACTIVE with CREATE-0001–0008, ACT-0035, ACT-0036 |
| **Creation evidence** | CREATE-nnn (artwork, making); dimensions 1–5 | 8 CREATE entries (drawings, collages); levels 3–4 for originality/elaboration/flexibility |
| **Planning/execution evidence** | ACT-nnn (probes, projects) | ACT-0035 (BUILD probe): planning, execution, making, decision-making; ACT-0036 (companion artistic style) |
| **Gap log** | BUILD gaps (e.g. ideas close to source, struggles with “what if”) | `gaps: []` in container; analysis doc calls out financial_level, collaboration_level as null |
| **Edge** | “Propose activities at the edge” | Narrative creation from prompts; cross-language creative tasks; planning/execution at 1–2 |

---

## 7. Cross-references

| Link | Template | Instance |
|------|----------|----------|
| **THINK (SAT)** | When WORK has SAT goal, THINK can have sat_readiness block; WORK reads for progress | skill-think.md § SAT READINESS; work_goals.horizon includes SAT ≥ 1200 |
| **SELF** | life_mission in self.md; WORK goals align | life_mission_ref in skill-work; self.md § VI VALUES |
| **Analyst / IX-A,B,C** | Analyst stages knowledge/curiosity/personality from same inputs; WORK does not stage | Same; CREATE/ACT yield self_signals that go to SELF via pipeline |

---

## 8. Summary

- **Template (companion-self) skill-work** = Definition of WORK: scope (making, planning, execution, exchange, creation), schema (BUILD container, CREATE/ACT), dimensions (planning, execution, making, financial, collaboration, originality, elaboration, flexibility, decision-making), work_goals and life_mission ref, module intent, and rules (starts from zero, human-gated, no staging to SELF).
- **Instance (grace-mar) skill-work** = Same structure and intent, filled with pilot data: evidence-linked levels, 8 CREATE entries, 2 ACT entries, work_goals (horizon SAT), SCHOOL, companion_creative_context, and explicit nulls (financial, collaboration) where evidence is missing.

Grace-mar’s skill-work is a valid instantiation of the template: it uses the same labels, container shape, and evidence types; it omits or leaves null only where the template allows (e.g. optional financial/collaboration until evidence exists).
