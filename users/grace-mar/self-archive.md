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

END OF FILE — EVIDENCE grace-mar v0.2 (reseeded)
