# RECURSION GATE — grace-mar

> Staging file for the gated profile pipeline — **one queue per companion, every channel.**
> Writers include **Telegram**, **WeChat**, **operator/Cursor** (activity reports, `calibrate_from_miss`, `parse_we_did`), **Mini App** (when wired), and **test/harness** runs. Each candidate carries **`channel_key`** (e.g. `telegram:…`, `operator:cursor`, `test:…`) so you can see the source. **Same gate, same merge** — not Telegram-only.
>
> **Workflow (one gate):**
> 1. Review each candidate below
> 2. Change `status: pending` to `status: approved` or `status: rejected`
> 3. Tell the assistant: **"approve"** — the agent immediately processes approved candidates into self.md, self-evidence.md, session-log.md, and prompt.py. No separate "process the review queue" step.
>
> **Merge checklist (correctness before approve):**
> 1. **Grounded** — Tied to something the companion actually said or did (or artifact), not invented or world-knowledge leakage.
> 2. **Merge-ready** — Would you ship this to SELF/EVIDENCE without embarrassment? If it feels like filler or duplicate IX, reject or edit.
> 3. **No duplicate lane** — Same fact already in IX-A/B/C? Reject or fold into existing entry instead of piling candidates.
> 4. **Human pass** — If only the analyst saw the exchange, one quick re-read of `example_from_exchange` / source lines.
> 5. **Portability** — For `portable-working-identity` candidates, also check [portability review checklist](../../docs/portable-record/portability-review-checklist.md).
>
> **Review checklist** (legacy one-liner): Grounded in the exchange? No LLM inference beyond it? No contradiction with existing Record?
>
> **Intent (before approve — long agents / optimization framing):** Models optimize toward task completion; constraints must be explicit. Ask: (1) **What would I not want** even if this candidate "succeeds"? (2) **When should we stop and ask** the companion? (3) **If this conflicts with INTENT**, companion + INTENT win — reject or revise. See **design-notes §11.9** (Misalignment at the interface).
>
> Machine-written by **`bot/core.py`** (Telegram, WeChat, activity reports) and by **operator scripts** that stage here — only edit the `status` field (and optional rejection notes).
>
> **Territory (work-politics vs companion):** For **work-politics** candidates, set **`territory: work-politics`** or **`channel_key: operator:wap`** (optionally `operator:wap:brief-name`). Operator tools then filter: `python scripts/operator_blocker_report.py -u grace-mar --territory wap` (work-politics territory only) or `--territory companion` (Record only). Same file, different lens.
>
> **Invariant:** Every **pending** or **approved-not-yet-merged** candidate must sit **above** `## Processed`. The bot inserts new blocks immediately before `## Processed`. If anything pending appears below Processed, move it up or merge will not see it.

---

## Candidate classification (Comprehension Envelope)

Optional YAML keys on each `### CANDIDATE-…` fenced block. **Orthogonal** to traffic **`risk_tier`** (`quick_merge_eligible` / `review_batch` / `manual_escalate` from [recursion-gate-three-tier.md](../../docs/recursion-gate-three-tier.md) and [recursion_gate_review.py](../../scripts/recursion_gate_review.py)) — do **not** reuse `risk_tier` for a `low`/`medium`/`high` blast-radius ladder.

| Field | Values | Role |
|-------|--------|------|
| **`impact_tier`** | `low` \| `medium` \| `high` \| `boundary` | Blast radius / promotion sensitivity of **this** merge (content), not review traffic. |
| **`envelope_class`** | `none` \| `optional` \| `required` | Whether a **Comprehension Envelope** block is omitted, recommended, or required. |

**Intended pairing:** `low` → `none`; `medium` → `optional`; `high` or `boundary` → `required`. Full vocabulary: [comprehension-envelope-gate.md](../../docs/governance/comprehension-envelope-gate.md).

**Authority map (advisory):** When you can name a [surface key](../../docs/authority-map.md) for the change (e.g. `memory_governance`, `prepared_context`), run `python3 scripts/check-authority.py --surface <key> --json` for **recommended** `impact_tier`, `envelope_class`, and Reflection Gate label derived from write authority — not a substitute for judgment; companion may override in YAML.

**Optional check:** `python3 scripts/validate_gate_comprehension_envelope.py -u grace-mar` (warns if `envelope_class: required` but envelope missing; `--strict` exits non-zero).

### Comprehension Envelope template

Place **below** the closing YAML fence of the candidate block, still under the same `### CANDIDATE-…` section:

```markdown
### Comprehension Envelope
- What this is:
- Why this path:
- Why not the next-best option:
- Blast radius:
- Assumptions / fragile points:
- Human override applied:
```

**Authoring:** 1–2 sentences per bullet; name concrete surfaces; `unknown` allowed; no motivational filler; reviewer scannable in ~30 seconds.

### Examples (illustrative)

Not live candidates — copy the shape when adding real **pending** blocks above `## Processed`.

**Example A — low impact, no envelope**

```yaml
impact_tier: low
envelope_class: none
status: pending
# … other required candidate keys …
```

*(No `### Comprehension Envelope` block for this class.)*

**Example B — boundary impact, envelope required**

```yaml
impact_tier: boundary
envelope_class: required
status: pending
# … other required candidate keys …
```

```markdown
### Comprehension Envelope
- What this is: One IX-A line from a daily-brief claim already verified under Links with dated citations.
- Why this path: Knowledge belongs in SELF when stable; the brief was intake only.
- Why not the next-best option: Pasting the full brief into SELF would bloat IX-A; leaving it only in days.md would skip the Record.
- Blast radius: Single IX-A bullet; no prompt or abstention rule change.
- Assumptions / fragile points: Source may need refresh if the situation moves; companion may narrow wording on approve.
- Human override applied: none.
```

---

## Reflection Gates (v1)

**Reflection Gates** are a **process-control label** at the **promotion boundary** only. They scale how much deliberate review to apply; they do **not** change runtime generation or bot staging speed.

**Triggers use `impact_tier`**, not traffic **`risk_tier`**. Traffic tiers (`quick_merge_eligible` / `review_batch` / `manual_escalate`) remain the machine UX lane from [recursion-gate-three-tier.md](../../docs/recursion-gate-three-tier.md).

| Gate | When (`impact_tier`) | Comprehension Envelope | v1 enforcement |
|------|----------------------|------------------------|----------------|
| *(none)* | `low` or unset | `envelope_class: none` typical | Fast path; no extra friction |
| **Light Gate** | `medium` | `envelope_class: optional` (recommended) | **Advisory only** — no hard block if omitted early on; ~30s scan of purpose + blast radius (summary or envelope) |
| **Heavy Gate** | `high` or `boundary` | `envelope_class: required` | Envelope required; **Blast radius** and **Human override applied** bullets must be honestly filled (`unknown` ok). **Advisory-first** warnings from `validate_gate_comprehension_envelope.py`; optional `--strict` only where documented |

**Dynamic Gate** (observability-driven escalation) is **not** in v1 — reserved for a later PR.

**Optional acknowledgment (Heavy):** You may set `reflection_ack: heavy` on the candidate YAML when the companion has done an explicit Heavy Gate read (still one human approver in v1).

**Suggested YAML (Heavy example)**

```yaml
impact_tier: boundary
envelope_class: required
reflection_ack: heavy
# … status, summary, mind_category, profile_target, suggested_entry, …
```

---

## Candidates

## Processed

### CANDIDATE-0031 (IX-C — remove PERS-004; cadence stays WORK-only)

```yaml
proposal_class: RUNTIME_OBSERVATION_PROPOSAL
status: approved
timestamp: 2026-04-24 18:45:00
channel_key: operator:cursor:cadence-boundary-ix-c
source: operator — cursor session (Record boundary)
mind_category: personality
signal_type: operator_directive
profile_target: IX-C. PERSONALITY
priority_score: 4
summary: "IX-C: delete PERS-004 — work rhythm / cadence belongs in skill-work + work-dev, not Record"
target_surface: SELF_IX_C
target_path: users/grace-mar/self.md
proposed_change: |
  In users/grace-mar/self.md IX-C `entries`, remove the entire list item with id PERS-004
  ("Work rhythm — punctuated resets" / coffee / thanks / dream wording).
  Do not replace it with another IX-C row for cadence — ritual choices, frequencies, and
  work-cadence-events.md telemetry stay under docs/skill-work/work-cadence/, work-coffee/,
  .cursor/skills (coffee, dream, bridge, conductor, thanks), and work-dev scripts (see
  docs/skill-work/work-dev/ for runners and logging).
  Renumbering other PERS-* ids is not required; only remove the PERS-004 block.
suggested_entry: "Manual apply: delete PERS-004 from self.md IX-C per proposed_change."
prompt_section: YOUR PERSONALITY
prompt_addition: none
impact_tier: low
envelope_class: none
source_exchange:
  operator: |
    Cadence events and operator ritual habits are WORK (skill-work doctrine + work-dev tooling), not IX-C personality.
    Operator: keep cadence only in work; remove PERS-004 from Record on approve.
```

### CANDIDATE-0025 (IX-A fact — U.S. constitutional order from founding canon)

```yaml
status: approved
timestamp: 2026-04-26 10:00:00
channel_key: operator:cursor:bookshelf-ix-a
source: operator — manual merge-ready candidate (A)
source_exchange:
  operator: |
    Knowledge claim (not methodology): the companion affirms a stable, testable set of U.S. constitutional facts/patterns
    from founding-era canonical shelf material, grounded in the America-focused HNSRC cluster.

    Evidence: HNSRC-0087, HNSRC-0088, HNSRC-0089, HNSRC-0090, HNSRC-0091, HNSRC-0092, HNSRC-0093, HNSRC-0094
mind_category: knowledge
signal_type: operator_paste
priority_score: 5
summary: "IX-A: U.S. separation of powers, federalism, and Great Compromise (founding shelf)"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: the U.S. order combines separated federal powers, bicameralism, and a federalist division of authority; the Connecticut Compromise (Great Compromise) created dual representation; Federalist 10/51 classically argue the extended-republic and checks design against factional domination. Evidence: HNSRC-0087–HNSRC-0094."
warrant: "Revisit if I materially stop treating this founding canon as my reference set for U.S. constitutional questions."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```
### CANDIDATE-0026 (IX-A fact — American literary-historical canon via Library of America set)

```yaml
status: approved
timestamp: 2026-04-26 10:00:00
channel_key: operator:cursor:bookshelf-ix-a
source: operator — manual merge-ready candidate (A)
source_exchange:
  operator: |
    Knowledge claim: the LOA-anchored shelf set supports an internal map of the American story through primary narrative-historical
    texts, not a statement about curation as a "method" — it is the substantive canon the companion is reading.

    Evidence: HNSRC-0101, HNSRC-0102, HNSRC-0103, HNSRC-0104, HNSRC-0105, HNSRC-0106, HNSRC-0107, HNSRC-0108
mind_category: knowledge
signal_type: operator_paste
priority_score: 5
summary: "IX-A: American narrative-historical LOA set as reference canon (not a method claim)"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: the Library-of-America-anchored shelf is my primary American narrative-historical reference spine (HNSRC-0101–HNSRC-0108), used as canonical primary-text support for U.S. cultural and political history, distinct from the founding-law cluster (HNSRC-0087–HNSRC-0094)."
warrant: "Revisit if the LOA-anchored shelf is materially re-sorted or deprioritized as my American narrative spine."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0022 (Bookshelf MCQ claim — biography as primary pattern extr…)

```yaml
status: rejected
reason: "methodology-leaning (extraction channel) vs knowledge fact/pattern; superseded if replaced by fact-first biography cluster"
timestamp: 2026-04-26 02:50:06
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ round source: Library-Bookshelf -> Recursion-Gate MCQ (2026-04-25)
    Companion selections:
    - Biography role: primary vehicle for institutional/personality pattern extraction
    - Promotion strictness: strict top2
    - Target default: IX-A knowledge
    
    Proposed entry (candidate text):
    Biographical history is a primary extraction channel in the companion's knowledge model, especially for linking institutional behavior with leader-level decision patterns.
    
    Evidence cluster:
    HNSRC-0011, HNSRC-0019, HNSRC-0027, HNSRC-0028, HNSRC-0031, HNSRC-0032, HNSRC-0033, HNSRC-0063
    
    Boundary note:
    This candidate is claim-first and bounded to explicit MCQ response + listed shelf evidence; no auto-merge requested.
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Bookshelf MCQ claim — biography as primary pattern extractor"
convergence: recurring
convergence_prior: CANDIDATE-0019, CANDIDATE-0020, CANDIDATE-0021
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0021 (Bookshelf MCQ claim — America as enduring analytic lens)

```yaml
status: rejected
reason: "superseded by CANDIDATE-0025 (concrete U.S. constitutional facts + evidence)"
timestamp: 2026-04-26 02:50:01
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ round source: Library-Bookshelf -> Recursion-Gate MCQ (2026-04-25)
    Companion selections:
    - America pattern: enduring core lens
    - Promotion strictness: strict top2
    - Target default: IX-A knowledge
    
    Proposed entry (candidate text):
    America-focused shelf work is a durable analytic lens in the companion's knowledge system, used repeatedly for interpretation across institutional, founding, and strategic-history contexts.
    
    Evidence cluster:
    HNSRC-0087, HNSRC-0088, HNSRC-0089, HNSRC-0090, HNSRC-0091, HNSRC-0092, HNSRC-0093, HNSRC-0094
    
    Boundary note:
    This candidate is claim-first and bounded to explicit MCQ response + listed shelf evidence; no auto-merge requested.
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Bookshelf MCQ claim — America as enduring analytic lens"
convergence: recurring
convergence_prior: CANDIDATE-0019, CANDIDATE-0020
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0020 (Bookshelf membrane claim draft — Library of America lens)

```yaml
status: rejected
reason: "superseded — placeholder suggested_entry; LOA phrasing was too meta without concrete IX line"
timestamp: 2026-04-26 02:43:05
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    Membrane source: docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md
    Proposed statement: Sustained engagement with Library of America is part of how knowledge is organized and interpreted across sessions.
    Profile target suggestion: IX-B. CURIOSITY
    Evidence: HNSRC-0101, HNSRC-0102, HNSRC-0103, HNSRC-0104, HNSRC-0105, HNSRC-0106, HNSRC-0107, HNSRC-0108
    Rationale: Explicit companion selection from Coffee E membrane quiz (enduring).
mind_category: curiosity
signal_type: operator_paste
priority_score: 3
summary: "Bookshelf membrane claim draft — Library of America lens"
convergence: recurring
convergence_prior: CANDIDATE-0019
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0019 (Bookshelf membrane claim draft — America lens)

```yaml
status: rejected
reason: "superseded — placeholder suggested_entry; membrane framing mixed methodology/IX mapping"
timestamp: 2026-04-26 02:43:00
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    Membrane source: docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md
    Proposed statement: Sustained engagement with America is part of how knowledge is organized and interpreted across sessions.
    Profile target suggestion: IX-B. CURIOSITY
    Evidence: HNSRC-0087, HNSRC-0088, HNSRC-0089, HNSRC-0090, HNSRC-0091, HNSRC-0092, HNSRC-0093, HNSRC-0094
    Rationale: Explicit companion selection from Coffee E membrane quiz (enduring).
mind_category: curiosity
signal_type: operator_paste
priority_score: 3
summary: "Bookshelf membrane claim draft — America lens"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0030 (Competence claim — Decolonization dynamics and post-col…)

```yaml
status: approved
timestamp: 2026-04-26 05:02:49
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25)
    Performance basis:
    - Correct: decol_1 (decolonization interaction pattern)
    - Correct: decol_2 (post-colonial fragility mechanism)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge that decolonization commonly reflected interaction of imperial exhaustion, nationalist mobilization, and legitimacy shifts, and that post-colonial fragility often followed institutional thinness, contested legitimacy, and inherited border-security-fiscal constraints.
    
    Evidence anchors:
    Bookshelf topic cluster and topic-anchored MCQ verification (decolonization shelf lane).
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — Decolonization dynamics and post-colonial fragility"
convergence: recurring
convergence_prior: CANDIDATE-0026, CANDIDATE-0019, CANDIDATE-0020, CANDIDATE-0021, CANDIDATE-0022, CANDIDATE-0027, CANDIDATE-0028, CANDIDATE-0029, CANDIDATE-0024, CANDIDATE-0023
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: post-WWII decolonization commonly emerged from interaction of imperial exhaustion, nationalist mobilization, and shifting legitimacy norms; post-colonial fragility often followed institutional thinness, contested legitimacy, and inherited border/security/fiscal constraints."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0029 (Competence claim — WWI escalation and trench stalemate…)

```yaml
status: approved
timestamp: 2026-04-26 05:02:48
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25)
    Performance basis:
    - Correct: ww1_1 (July Crisis escalation mechanism)
    - Correct: ww1_2 (Western Front stalemate condition)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge that alliance commitments, mobilization timetables, and credibility fears compressed decision space in 1914, and that trench stalemate reflected defensive firepower/fortification advantages outpacing offensive adaptation.
    
    Evidence anchors:
    Bookshelf topic cluster and topic-anchored MCQ verification (WWI shelf lane).
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — WWI escalation and trench stalemate mechanisms"
convergence: recurring
convergence_prior: CANDIDATE-0026, CANDIDATE-0019, CANDIDATE-0020, CANDIDATE-0021, CANDIDATE-0022, CANDIDATE-0027, CANDIDATE-0028, CANDIDATE-0024, CANDIDATE-0023
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: July Crisis escalation into general war followed alliance commitments, mobilization timetables, and credibility fears compressing decision space; Western Front stalemate reflected defensive firepower and fortification advantages outpacing offensive adaptation."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0028 (Competence claim — Late Qing strain and Self-Strengthen…)

```yaml
status: approved
timestamp: 2026-04-26 05:02:48
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25)
    Performance basis:
    - Correct: qing_1 (late Qing structural challenge)
    - Correct: qing_2 (Self-Strengthening framing)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge that late Qing fragility emerged from rebellion plus foreign pressure plus fiscal-administrative strain, and that Self-Strengthening was selective military-industrial modernization without full political transformation.
    
    Evidence anchors:
    Bookshelf topic cluster and topic-anchored MCQ verification (Qing shelf lane).
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — Late Qing strain and Self-Strengthening limits"
convergence: recurring
convergence_prior: CANDIDATE-0026, CANDIDATE-0019, CANDIDATE-0020, CANDIDATE-0021, CANDIDATE-0022, CANDIDATE-0027, CANDIDATE-0024, CANDIDATE-0023
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: late Qing fragility was driven by the interaction of internal rebellion, foreign pressure, and fiscal-administrative strain; Self-Strengthening represented selective military-industrial modernization without full political-institutional transformation."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0027 (Competence claim — Ottoman durability and Tanzimat refo…)

```yaml
status: approved
timestamp: 2026-04-26 05:02:48
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25)
    Performance basis:
    - Correct: ottoman_1 (durability mechanism)
    - Correct: ottoman_2 (Tanzimat characterization)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge of Ottoman imperial durability mechanisms (administrative-military flexibility, provincial incorporation, and revenue capacity) and of Tanzimat as a state-centralizing modernization attempt under pressure.
    
    Evidence anchors:
    Bookshelf topic cluster and topic-anchored MCQ verification (Ottoman shelf lane).
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — Ottoman durability and Tanzimat reform constraints"
convergence: recurring
convergence_prior: CANDIDATE-0026, CANDIDATE-0019, CANDIDATE-0020, CANDIDATE-0021, CANDIDATE-0022, CANDIDATE-0024, CANDIDATE-0023
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: Ottoman imperial durability relied on administrative-military flexibility, provincial incorporation, and revenue extraction capacity; Tanzimat reforms are best understood as state-centralizing modernization under external/internal pressure rather than liberal-democratic transition."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0024 (Competence claim — Russian center-periphery and reform-…)

```yaml
status: approved
timestamp: 2026-04-26 04:46:14
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: Historical Knowledge Check (topic-anchored + advanced round, 2026-04-25)
    Performance basis:
    - Correct: adv_russia_1 (modernization vs liberalization constraint)
    - Correct: adv_russia_2 (center-periphery scale/coordination burden)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge competence in Russian long-arc state analysis, especially the recurring tension between modernization pressure and political capacity limits, and the center-periphery coordination burdens imposed by territorial scale.
    
    Topic/evidence anchors:
    - HNSRC-0122, HNSRC-0123, HNSRC-0124, HNSRC-0125 (Russian historical state development set)
    - HNSRC-0148, HNSRC-0149, HNSRC-0150, HNSRC-0151 (imperial/modern continuity set)
    
    Boundary note:
    Candidate captures domain knowledge pattern from topic-specific testing; excludes workflow/method preference language.
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — Russian center-periphery and reform-era constraints"
convergence: recurring
convergence_prior: CANDIDATE-0022, CANDIDATE-0023
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0023 (Competence claim — Roman constitutional durability and…)

```yaml
status: approved
timestamp: 2026-04-26 04:46:09
channel_key: operator:cursor:stage-paste
source: operator — scripts/stage_gate_candidate.py
source_exchange:
  operator: |
    MCQ source: Historical Knowledge Check (topic-anchored + advanced round, 2026-04-25)
    Performance basis:
    - Correct: adv_rome_1 (Augustan durability mechanism)
    - Correct: adv_rome_2 (succession crisis mechanism)
    
    Proposed knowledge claim:
    The companion demonstrates stable knowledge competence in Roman imperial transition analysis, specifically how Augustan institutional form increased regime durability while ambiguous succession norms repeatedly reopened elite and military contestation.
    
    Topic/evidence anchors:
    - HNSRC-0007 (The Landmark Julius Caesar)
    - HNSRC-0017, HNSRC-0018, HNSRC-0019, HNSRC-0020 (Roman imperial corpus)
    - HNSRC-0028, HNSRC-0029, HNSRC-0030 (late-republic/imperial continuity set)
    
    Boundary note:
    Candidate captures domain knowledge pattern from topic-specific testing; excludes workflow/method preference language.
mind_category: knowledge
signal_type: operator_paste
priority_score: 3
summary: "Competence claim — Roman constitutional durability and succession dynamics"
convergence: recurring
convergence_prior: CANDIDATE-0022
profile_target: IX-A. KNOWLEDGE
suggested_entry: "See source_exchange.operator (staged paste)."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

### CANDIDATE-0014 through CANDIDATE-0018 — rejected 2026-04-17

```yaml
profile_target: IX-A. KNOWLEDGE
status: rejected
reason: "Operator deferred all IX-A population — will seed knowledge entries in a future session"
```

### CANDIDATE-0007 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-strategy/README.md, strategy-notebook (64 expert files)
summary: "Geopolitics and international relations"
merged_as: CUR-0001
```

### CANDIDATE-0008 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: users/grace-mar/work-jiang.md, LIB-0149
summary: "Jiang philosophy and Predictive History"
merged_as: CUR-0002
```

### CANDIDATE-0009 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-dev/README.md, work-companion-self/README.md
summary: "AI systems design and companion-self architecture"
merged_as: CUR-0003
```

### CANDIDATE-0010 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-politics/README.md
summary: "Political consulting (interest only)"
merged_as: CUR-0004
```

### CANDIDATE-0011 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-civ-mem/README.md, LIB-0157
summary: "Civilizational history and structured knowledge"
merged_as: CUR-0005
```

### CANDIDATE-0012 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: library_shelf
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: users/grace-mar/self-library.md
summary: "Theology"
merged_as: CUR-0006
```

### CANDIDATE-0013 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-cici/README.md, work-alpha-school/README.md
summary: "Mentoring and teaching methodology"
merged_as: CUR-0007
```

### CANDIDATE-0001 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-decisions.md, operator-rhythm.md
summary: "Cognitive style — evaluate-then-pick with compression"
merged_as: PERS-001
```

### CANDIDATE-0002 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-rhythm.md, operator-decisions.md
summary: "Interaction mode — short prompts, menu-driven selection"
merged_as: PERS-002
```

### CANDIDATE-0003 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-thresholds.md
summary: "Quality standard — falsifiable thesis + attributed sources + named tensions"
merged_as: PERS-003
```

### CANDIDATE-0004 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-rhythm.md
summary: "Work rhythm — punctuated resets"
merged_as: PERS-004
```

### CANDIDATE-0005 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-decisions.md
summary: "Decision failure sensitivity"
merged_as: PERS-005
```

### CANDIDATE-0006 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-frictions.md
summary: "Friction signature — cold-thread context loss and premature infrastructure"
merged_as: PERS-006
```

*(Cleared at reseed 2026-04-14. Previous candidates archived in `archive/companion-freeze-abby-2026-04-14/`. Full history in git tag `companion-freeze/abby-2026-04-14`.)*
