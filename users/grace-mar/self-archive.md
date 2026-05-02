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

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0042 → ACT-0013
> IX-A: maritime power as naval-commercial system
> warrant: Revisit if a direct Mahan source is added to self-library-bookshelf or if this should be reframed as Venetian maritime-power context rather than Mahan-style theory.
> source_binding_strength: weak
> shelf_refs: [HNSRC-0247, HNSRC-0248]
> quiz_receipt:
> source_kind: secondary
>   citation_label: "Roger Crowley, City of Fortune; Roger Crowley, Spice"
>   visible_prompt: "Drawing on Roger Crowley's accounts of Venetian sea power and the spice contest, which answer best captures the strategic mechanism of maritime power?"
>   stem_topic: "Maritime power as naval-commercial system"
>   selected_answer: "B - naval commerce, bases, chokepoints, and fleet concentration make maritime power geopolitically decisive."
>   correct_answer: "B - naval commerce, bases, chokepoints, and fleet concentration make maritime power geopolitically decisive."
>   validation_note: "Companion selected the concept-level answer matching the maritime-power mechanism. Binding is weak because the catalog has Crowley secondary context, not a direct Mahan primary/source row."
>   staged_claim: "Knows: Mahan-style sea-power analysis treats naval commerce, bases, chokepoints, and fleet concentration as mechanisms that make maritime power geopolitically decisive."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0043 → ACT-0014
> IX-A: offensive realism and regional hegemony
> warrant: Revisit if a direct Mearsheimer source is added to self-library-bookshelf or if the operator wants only catalog-bound claims approved.
> source_binding_strength: weak
> shelf_refs: []
> quiz_receipt:
> source_kind: secondary
>   citation_label: "Mearsheimer, offensive realism"
>   visible_prompt: "In Mearsheimer's offensive realism, why do great powers seek regional hegemony?"
>   stem_topic: "Offensive realism and regional hegemony"
>   selected_answer: "B - anarchy leaves states unable to be fully certain of other states' intentions."
>   correct_answer: "B - anarchy leaves states unable to be fully certain of other states' intentions."
>   validation_note: "Companion selected the concept-level answer matching the offensive-realist mechanism. Binding is weak because no direct Mearsheimer shelf row was found in self-library-bookshelf at repair time."
>   staged_claim: "Knows: in Mearsheimer's offensive realism, great powers seek regional hegemony because anarchy leaves states unable to be fully certain of other states' intentions."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0044 → ACT-0015
> IX-A: Melian Dialogue as realist lesson on power asymmetry
> warrant: Revisit if I stop treating the Melian Dialogue as a realist power-asymmetry anchor.
> source_binding_strength: strong
> shelf_refs: [HNSRC-0003]
> quiz_receipt:
> source_kind: primary
>   citation_label: "Thucydides, History of the Peloponnesian War"
>   visible_prompt: "In Thucydides' account of the Melian Dialogue, what realist lesson is usually drawn from Athens' argument to Melos?"
>   stem_topic: "Melian Dialogue and power asymmetry"
>   selected_answer: "C - power asymmetry can override moral argument when no higher enforcing authority exists."
>   correct_answer: "C - power asymmetry can override moral argument when no higher enforcing authority exists."
>   validation_note: "Companion selected the concept-level answer matching the standard realist reading of the Melian Dialogue."
>   staged_claim: "Knows: the Melian Dialogue is commonly read as a realist lesson that power asymmetry can override moral argument when no higher enforcing authority exists."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0045 → ACT-0016
> IX-A: second-strike capability and deterrence
> warrant: Revisit if a dedicated nuclear-strategy primary source is added to self-library-bookshelf or if this should remain report-only until better anchored.
> source_binding_strength: weak
> shelf_refs: [HNSRC-0256]
> quiz_receipt:
> source_kind: secondary
>   citation_label: "H. W. Brands, The General vs. the President"
>   visible_prompt: "Against the background of Cold War nuclear escalation debates, what does second-strike capability mean?"
>   stem_topic: "Second-strike capability and deterrence"
>   selected_answer: "B - a state can absorb a nuclear attack and still retaliate, making a first strike less attractive."
>   correct_answer: "B - a state can absorb a nuclear attack and still retaliate, making a first strike less attractive."
>   validation_note: "Companion selected the concept-level answer matching deterrence theory. Binding is weak because the available shelf row is secondary Cold War context rather than a dedicated primary nuclear-strategy source."
>   staged_claim: "Knows: second-strike capability means a state can absorb a nuclear attack and still retaliate, making a first strike less attractive and stabilizing deterrence."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0046 → ACT-0017
> IX-A: Herodotus as history-as-inquiry
> warrant: Revisit if this should be narrowed from general Herodotean inquiry to the Greek-Persian conflict specifically.
> source_binding_strength: strong
> shelf_refs: [HNSRC-0001, HNSRC-0002]
> quiz_receipt:
> source_kind: primary
>   citation_label: "Herodotus, The Histories"
>   visible_prompt: "Drawing on Herodotus' account of the Greek-Persian world, what best captures why his history is more than a simple war chronicle?"
>   stem_topic: "Herodotus history as inquiry into empire, customs, and causes"
>   selected_answer: "B - it combines inquiry into causes with comparisons of peoples, customs, empires, and political choices."
>   correct_answer: "B - it combines inquiry into causes with comparisons of peoples, customs, empires, and political choices."
>   validation_note: "Companion selected the concept-level answer matching the Herodotean history-as-inquiry anchor."
>   staged_claim: "Knows: Herodotus' Histories treats history as inquiry into causes, empire, customs, peoples, and political choices, not only as a war chronicle."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0047 → ACT-0018
> IX-A: Thucydides and alliance coercion
> warrant: Revisit if this should be merged with the Melian Dialogue power-asymmetry candidate rather than kept as a distinct alliance-coercion claim.
> source_binding_strength: strong
> shelf_refs: [HNSRC-0003]
> quiz_receipt:
> source_kind: primary
>   citation_label: "Thucydides, History of the Peloponnesian War"
>   visible_prompt: "In Thucydides' account of the Peloponnesian War, what is the strategic significance of alliance coercion?"
>   stem_topic: "Thucydides and alliance coercion"
>   selected_answer: "B - it shows that great-power rivalry often pressures smaller poleis into dependence, tribute, or obedience."
>   correct_answer: "B - it shows that great-power rivalry often pressures smaller poleis into dependence, tribute, or obedience."
>   validation_note: "Companion selected the concept-level answer matching the Thucydidean alliance-coercion anchor."
>   staged_claim: "Knows: in Thucydides' account of the Peloponnesian War, great-power rivalry can pressure smaller poleis into dependence, tribute, or obedience."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0048 → ACT-0019
> IX-A: Clausewitz friction
> warrant: Revisit if the operator wants this framed under strategy vocabulary rather than general IX-A knowledge.
> source_binding_strength: strong
> shelf_refs: [HNSRC-0146]
> quiz_receipt:
> source_kind: primary
>   citation_label: "Clausewitz, On War"
>   visible_prompt: "Drawing on Clausewitz's On War, what does friction most directly mean?"
>   stem_topic: "Clausewitz and friction"
>   selected_answer: "B - the unpredictable accumulation of practical difficulties that makes real war harder than planned war."
>   correct_answer: "B - the unpredictable accumulation of practical difficulties that makes real war harder than planned war."
>   validation_note: "Companion selected the concept-level answer matching the Clausewitz friction anchor."
>   staged_claim: "Knows: in Clausewitz's On War, friction means the unpredictable accumulation of practical difficulties that makes real war harder than planned war."

**[2026-05-01 22:55:30]** `APPROVED` (Operator)
> CANDIDATE-0049 → ACT-0020
> IX-A: Tocqueville associations and democratic self-government
> warrant: Revisit if this should be narrowed to civil society as a curiosity lens rather than promoted as IX-A knowledge.
> source_binding_strength: strong
> shelf_refs: [HNSRC-0262]
> quiz_receipt:
> source_kind: primary
>   citation_label: "Tocqueville, Democracy in America"
>   visible_prompt: "In Tocqueville's Democracy in America, why are associations and civil society politically important?"
>   stem_topic: "Tocqueville associations and democratic self-government"
>   selected_answer: "B - they help democratic citizens practice self-government outside the state and resist isolated individualism."
>   correct_answer: "B - they help democratic citizens practice self-government outside the state and resist isolated individualism."
>   validation_note: "Companion selected the concept-level answer matching the Tocqueville civil-society anchor."
>   staged_claim: "Knows: in Tocqueville's Democracy in America, associations and civil society help democratic citizens practice self-government outside the state and resist isolated individualism."
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

  - id: ACT-0013
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: maritime power as naval-commercial system"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0014
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: offensive realism and regional hegemony"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0015
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Melian Dialogue as realist lesson on power asymmetry"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0016
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: second-strike capability and deterrence"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0017
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Herodotus as history-as-inquiry"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0018
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Thucydides and alliance coercion"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0019
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Clausewitz friction"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0020
    date: 2026-05-01
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: pipeline merge
    summary: "IX-A: Tocqueville associations and democratic self-government"
    curated_by: user
    evidence_tier: 3
