# EVIDENCE — grace-mar

Version: 0.2
Created: February 2026
Reseeded: April 2026
Status: ACTIVE

Canonical evidence surface — not identity (SELF), not reference routing (SELF-LIBRARY), not runtime transcript storage. Normalized, provenance-linked entries with artifact references. Long raw transcripts belong under `artifacts/` and are referenced here, not inlined. Evidence may inform SELF or SKILLS only through explicit reviewed synthesis via the gated pipeline.

---

## Transcript handling rule

Do not inline long raw transcripts in the canonical archive. § VIII (Gated Approved Log) is the primary area where this applies.

- Store the raw transcript or long conversation extract under `artifacts/` (e.g. `artifacts/act-XXXX-telegram-thread.md`)
- Create a normalized archive entry here with: date, modality, activity type, topic, `artifact_ref`, normalized summary, evidence tier
- Inline transcript excerpts only when the exact wording is itself the evidence (e.g. a specific phrasing that reveals a knowledge boundary or personality signal)

---

## Entry shape (working convention)

Forward-facing standard for new entries. Existing entries are not retroactively rewritten.

Every durable archive entry should aim to separate four layers:

1. **artifact_ref** — where the raw thing lives (path under `artifacts/`)
2. **normalized** — structured facts about the thing
3. **analysis_ref** — optional interpretation stored separately (e.g. `artifacts/analyses/`)
4. **candidate_for** — optional downstream synthesis targets (THINK, WRITE, SELF)

### Evidence subtypes

Preferred values for `evidence_subtype`:

- `reading_item`
- `writing_sample`
- `lookup_event`
- `conversation_excerpt`
- `artifact_observation`
- `development_marker`

Subtype describes the evidence class, not the topic.

### Review fields

- `review_status`: `active` | `compressed` | `superseded`
- `reviewed_at`: ISO date of last review

### Example (new-style entry)

```yaml
  - id: ACT-XXXX
    date: 2026-XX-XX
    evidence_subtype: conversation_excerpt
    modality: text (Telegram)
    activity_type: correction / boundary stress
    topic: example topic
    artifact_ref: artifacts/act-XXXX-telegram-thread.md
    normalized:
      summary: >
        Short factual summary of what happened.
      evidence_tier: 3
    review_status: active
    reviewed_at: 2026-XX-XX
    candidate_for:
      - self-skill-think
```

---

## I. READING LIST

Books, articles, content consumed.

```yaml
entries: []
```

---

## II. WRITING SAMPLES

```yaml
entries: []
```

---

## III. CREATIVE WORKS

```yaml
entries: []
```

---

## IV. ACTIVITIES & OBSERVATIONS

```yaml
entries: []
```

---

## V. LOOKUP EVENTS

```yaml
entries: []
```

---

## VI. DEVELOPMENT MARKERS

```yaml
entries: []
```

---

## VII. MEDIA

```yaml
entries: []
```

---

## VIII. GATED APPROVED LOG

*(Entries merged via the gated pipeline.)*

---

## VIII. GATED APPROVED LOG (SELF-ARCHIVE)

> Append-only log of approved activity for the self (voice and non-voice). Written only when candidates are merged via process_approved_candidates. Lives in this file as § VIII (see docs/canonical-paths.md).

---


**[2026-04-25 21:50:17]** `APPROVED` (Operator)
> CANDIDATE-0023 → ACT-0001
> Competence claim — Roman constitutional durability and succession dynamics
> operator: | MCQ source: Historical Knowledge Check (topic-anchored + advanced round, 2026-04-25) Performance basis: - Correct: adv_rome_1 (Augustan durability mechanism) - Correct: adv_rome_2 (succession crisis mechanism) Proposed knowledge claim: The companion demonstrates stable knowledge competence in Roman imperial transition analysis, specifically how Augustan institutional form increased reg

**[2026-04-25 21:50:26]** `APPROVED` (Operator)
> CANDIDATE-0024 → ACT-0002
> Competence claim — Russian center-periphery and reform-era constraints
> operator: | MCQ source: Historical Knowledge Check (topic-anchored + advanced round, 2026-04-25) Performance basis: - Correct: adv_russia_1 (modernization vs liberalization constraint) - Correct: adv_russia_2 (center-periphery scale/coordination burden) Proposed knowledge claim: The companion demonstrates stable knowledge competence in Russian long-arc state analysis, especially the recurring tens

**[2026-04-25 22:04:07]** `APPROVED` (Operator)
> CANDIDATE-0027 → ACT-0003
> Competence claim — Ottoman durability and Tanzimat reform constraints
> operator: | MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25) Performance basis: - Correct: ottoman_1 (durability mechanism) - Correct: ottoman_2 (Tanzimat characterization) Proposed knowledge claim: The companion demonstrates stable knowledge of Ottoman imperial durability mechanisms (administrative-military flexibility, provincial incorporation, and revenue capacity) a

**[2026-04-25 22:04:13]** `APPROVED` (Operator)
> CANDIDATE-0028 → ACT-0004
> Competence claim — Late Qing strain and Self-Strengthening limits
> operator: | MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25) Performance basis: - Correct: qing_1 (late Qing structural challenge) - Correct: qing_2 (Self-Strengthening framing) Proposed knowledge claim: The companion demonstrates stable knowledge that late Qing fragility emerged from rebellion plus foreign pressure plus fiscal-administrative strain, and that Self-Stren

**[2026-04-25 22:04:15]** `APPROVED` (Operator)
> CANDIDATE-0029 → ACT-0005
> Competence claim — WWI escalation and trench stalemate mechanisms
> operator: | MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25) Performance basis: - Correct: ww1_1 (July Crisis escalation mechanism) - Correct: ww1_2 (Western Front stalemate condition) Proposed knowledge claim: The companion demonstrates stable knowledge that alliance commitments, mobilization timetables, and credibility fears compressed decision space in 1914, and that

**[2026-04-25 22:04:17]** `APPROVED` (Operator)
> CANDIDATE-0030 → ACT-0006
> Competence claim — Decolonization dynamics and post-colonial fragility
> operator: | MCQ source: New Region Set — Ottoman, Qing, WWI, Decolonization (2026-04-25) Performance basis: - Correct: decol_1 (decolonization interaction pattern) - Correct: decol_2 (post-colonial fragility mechanism) Proposed knowledge claim: The companion demonstrates stable knowledge that decolonization commonly reflected interaction of imperial exhaustion, nationalist mobilization, and legiti

**[2026-04-26 06:52:22]** `APPROVED` (Operator)
> CANDIDATE-0025 → ACT-0007
> IX-A: U.S. separation of powers, federalism, and Great Compromise (founding shelf)
> warrant: Revisit if I materially stop treating this founding canon as my reference set for U.S. constitutional questions.
> operator: | Knowledge claim (not methodology): the companion affirms a stable, testable set of U.S. constitutional facts/patterns from founding-era canonical shelf material, grounded in the America-focused HNSRC cluster. Evidence: HNSRC-0087, HNSRC-0088, HNSRC-0089, HNSRC-0090, HNSRC-0091, HNSRC-0092, HNSRC-0093, HNSRC-0094

**[2026-04-26 06:52:22]** `APPROVED` (Operator)
> CANDIDATE-0026 → ACT-0008
> IX-A: American narrative-historical LOA set as reference canon (not a method claim)
> warrant: Revisit if the LOA-anchored shelf is materially re-sorted or deprioritized as my American narrative spine.
> operator: | Knowledge claim: the LOA-anchored shelf set supports an internal map of the American story through primary narrative-historical texts, not a statement about curation as a "method" — it is the substantive canon the companion is reading. Evidence: HNSRC-0101, HNSRC-0102, HNSRC-0103, HNSRC-0104, HNSRC-0105, HNSRC-0106, HNSRC-0107, HNSRC-0108

**[2026-04-26 20:56:46]** `APPROVED` (Operator)
> CANDIDATE-0031 → RUNTIME-OBSERVATION
> IX-C: delete PERS-004 — work rhythm / cadence belongs in skill-work + work-dev, not Record
> operator: | Cadence events and operator ritual habits are WORK (skill-work doctrine + work-dev tooling), not IX-C personality. Operator: keep cadence only in work; remove PERS-004 from Record on approve.

**[2026-04-27 20:09:09]** `APPROVED` (Operator)
> CANDIDATE-0038 → ACT-0009
> IX-A: Washington as Commander in Chief of the Continental Army (June 1775)
> warrant: Revisit if I relocate commissioning facts away from June 1775 or drop the LOA Washington row as evidence for this claim.
> operator: | Anchor: Second Continental Congress, June 1775 — Commander in Chief appointment. Companion matched standard account (Washington commissioned commander of Continental Army). Evidence: HNSRC-0109 (Washington: Writings, Library of America).

**[2026-04-27 20:09:09]** `APPROVED` (Operator)
> CANDIDATE-0039 → ACT-0010
> IX-A: Delaware crossing tied to Trenton (Dec. 1776) in textbook Revolutionary narrative
> warrant: Revisit if I decouple the crossing from Trenton in my mental map or stop anchoring this arc to HNSRC-0109.
> operator: | Anchor: Delaware crossing, December 1776 — Trenton assault. Companion matched standard linkage (crossing → surprise attack on Trenton, Dec. 26, 1776). Evidence: HNSRC-0109.

**[2026-04-27 20:09:09]** `APPROVED` (Operator)
> CANDIDATE-0040 → ACT-0011
> IX-A: Washington as President of the Constitutional Convention (1787)
> warrant: Revisit if I attribute primary drafting authorship to Washington or fold this into generic ‘founding’ without his chair role.
> operator: | Anchor: Philadelphia Constitutional Convention, 1787 — presiding officer. Companion matched standard account (Washington president of the Convention). Evidence: HNSRC-0109.

**[2026-04-27 20:09:09]** `APPROVED` (Operator)
> CANDIDATE-0041 → ACT-0012
> IX-A: Farewell Address warnings on faction and permanent foreign ties
> warrant: Revisit if I flatten the Address into generic patriotism without faction/alliance tension or stop citing HNSRC-0109 for this speech cluster.
> operator: | Anchor: Farewell Address, 1796 — faction and foreign-alliance warnings. Companion matched standard pairing (faction spirit / permanent entanglements). Evidence: HNSRC-0109.
END OF FILE — EVIDENCE grace-mar v0.2 (reseeded)

  - id: ACT-0001
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — Roman constitutional durability and succession dynamics"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0002
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — Russian center-periphery and reform-era constraints"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0003
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — Ottoman durability and Tanzimat reform constraints"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0004
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — Late Qing strain and Self-Strengthening limits"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0005
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — WWI escalation and trench stalemate mechanisms"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0006
    date: 2026-04-25
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "Competence claim — Decolonization dynamics and post-colonial fragility"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0007
    date: 2026-04-26
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: U.S. separation of powers, federalism, and Great Compromise (founding shelf)"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0008
    date: 2026-04-26
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: American narrative-historical LOA set as reference canon (not a method claim)"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0009
    date: 2026-04-27
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Washington as Commander in Chief of the Continental Army (June 1775)"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0010
    date: 2026-04-27
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Delaware crossing tied to Trenton (Dec. 1776) in textbook Revolutionary narrative"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0011
    date: 2026-04-27
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Washington as President of the Constitutional Convention (1787)"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0012
    date: 2026-04-27
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Farewell Address warnings on faction and permanent foreign ties"
    curated_by: user
    evidence_tier: 3
