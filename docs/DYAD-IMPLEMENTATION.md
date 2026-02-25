# Dyad Implementation — Tricameral Mind (MIND, RECORD, VOICE)

Specific implementations to track and encourage tricameral-mind activity (MIND consulting and feeding RECORD/VOICE). Builds on existing infrastructure.

---

## 1. Event Instrumentation

### 1.1 Emit dyad events from `bot/core.py`

**Lookup (consultation)** — When user affirms a lookup, emit an event. Add to `get_response` after the lookup path:

```python
# After: assistant_message = _lookup_with_library_first(...)
emit_pipeline_event("dyad:lookup", None, channel_key=channel_key, question=question[:100])
```

**Activity report (feeding the other chamber)** — Already archives `ACTIVITY REPORT`. Add:

```python
# After: staged = analyze_activity_report(...)
emit_pipeline_event("dyad:activity_report", None, channel_key=channel_key)
```

**Mini App lookup** — `run_lookup` and `run_grounded_response` are direct consultations. Add emission in both:

```python
# In run_lookup, after _lookup_with_library_first returns
emit_pipeline_event("dyad:lookup", None, channel_key=channel_key, source="miniapp", question=question[:100])

# In run_grounded_response, after response
emit_pipeline_event("dyad:grounded_query", None, channel_key=channel_key, source="miniapp")
```

**Schema** — Use `PIPELINE-EVENTS.jsonl` with new event types: `dyad:lookup`, `dyad:activity_report`, `dyad:grounded_query`. Optional `source` and `question` fields.

---

## 2. Parse existing data for dyad metrics

### 2.1 COMPUTE-LEDGER buckets

`COMPUTE-LEDGER.jsonl` already has `bucket`:
- `library_lookup` — Record-first lookup
- `lookup_factual` — External lookup
- `lookup_rephrase` — Rephrasing lookup result

**Count consultations** — Sum rows where `bucket in ("library_lookup", "lookup_factual", "lookup_rephrase")`. Each row = one consultation.

### 2.2 ARCHIVE event types

Parse `SELF-ARCHIVE.md` for:
- `LOOKUP REQUEST` — User triggered lookup (question stored)
- `GRACE-MAR (lookup)` — Lookup response delivered
- `ACTIVITY REPORT` — "We did X" feeding

Fallback if we don’t emit dyad events yet: regex on archive blocks.

---

## 3. `scripts/dyad_metrics.py` — New script

Compute dyad health from PIPELINE-EVENTS, COMPUTE-LEDGER, and optionally SELF-ARCHIVE.

**Output (JSON / human-readable):**
- `consultations_7d` — Lookup + grounded_query count (from ledger buckets or dyad events)
- `activity_reports_7d` — `dyad:activity_report` or SELF-ARCHIVE `ACTIVITY REPORT` count
- `integrations_7d` — `applied` events from PIPELINE-EVENTS
- `consultation_ratio` — consultations / (consultations + chat turns) if estimable
- `dyad_score` — Simple composite (e.g. consultations + 2*integrations + activity_reports) for trend

**Usage:** `python scripts/dyad_metrics.py [--user grace-mar] [--days 7] [--json]`

---

## 4. Session brief — "From the Record"

Extend `scripts/session_brief.py`:

**New section: "From the Record"**
- Parse SELF.md for 1–3 recent or salient IX-A/IX-B/IX-C topics (e.g. last merged, or sample from each dimension).
- Output: "The Record currently holds: [topic 1], [topic 2], [topic 3]. Ask Grace-Mar to recall any of these."
- Encourages the user to *consult* the other chamber.

**Integration nudge**
- If `pending_count > 0` and oldest pending is >3 days: add line "You have N candidates waiting — consider bringing them into the Record (type /review)."
- Already has pending count; add staleness check via PENDING-REVIEW.md mtime or candidate timestamps.

---

## 5. Dashboard — Dyad health panel

Extend `scripts/generate_profile.py`:

**New data:**
- `dyad_consultations_7d` — from dyad_metrics or ledger
- `dyad_integrations_7d` — applied count (already have `pipeline_applied`)
- `dyad_activity_reports_7d` — activity report count

**New section in Benchmarks grid:**
- "Consultations (7d)" — lookup + grounded
- "Integrations (7d)" — applied
- "Activity reports (7d)" — "we did X" count

Or a small "Dyad" subsection: "Consultations / Integrations / Reports" with 7-day counts.

---

## 6. "Ask the Record" affordances

### 6.1 Mini App suggested prompts

Add to `miniapp/index.html` (or equivalent) a row of suggested prompts:
- "What do I know about [X]?" (with X from IX-B sample, e.g. "dinosaurs", "space")
- "What would I say about [Y]?"
- "What's in my Record?"

These route to `run_grounded_response` or `run_lookup` — direct consultation.

### 6.2 System prompt hint

In `bot/prompt.py` SYSTEM_PROMPT, add one line: "When the user asks 'what do I know about X?' or 'what's in my record?' — answer from your documented knowledge; that's the user consulting their Record."

(May already be implicit; retrieval handles it in grounded mode.)

---

## 7. Implementation order

| Priority | Item | Effort | Dependency |
|----------|------|--------|------------|
| 1 | dyad_metrics.py — parse ledger + PIPELINE-EVENTS | Low | None |
| 2 | session_brief: "From the Record" section | Low | SELF.md parsing |
| 3 | session_brief: integration nudge (stale pending) | Low | _pending_count, mtime |
| 4 | core.py: emit dyad:lookup, dyad:activity_report, dyad:grounded_query | Low | None |
| 5 | Dashboard: dyad subsection (consultations, integrations, reports) | Low | dyad_metrics or inline |
| 6 | Mini App: suggested "Ask the Record" prompts | Medium | miniapp UI |
| 7 | dyad_metrics: parse SELF-ARCHIVE as fallback | Medium | Archive format |

---

## 8. File touch points

| File | Changes |
|------|---------|
| `bot/core.py` | emit_pipeline_event for dyad:lookup, dyad:activity_report; run_lookup, run_grounded_response |
| `scripts/session_brief.py` | "From the Record" section; integration nudge |
| `scripts/generate_profile.py` | Dyad panel / metrics in Benchmarks |
| `scripts/dyad_metrics.py` | **New** — compute consultations, integrations, activity reports |
| `miniapp/index.html` | Suggested "Ask the Record" prompts (optional) |
| `docs/DYAD-IMPLEMENTATION.md` | This spec |
