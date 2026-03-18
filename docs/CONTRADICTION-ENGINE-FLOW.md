# Contradiction engine flow (pseudocode)

**Purpose:** Implementer-oriented sketch from **detect → review → merge**. Normative behavior remains [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md). Object shape: [schemas/conflict-object.schema.json](schemas/conflict-object.schema.json).

---

## 1. On staging (after candidate appended to queue)

```
function on_candidate_staged(candidate, user_id):
    active_claims = load_active_self_and_skills(user_id)  # IX-A/B/C + skills as applicable
    related = retrieve_overlapping_claims(candidate, active_claims)
    if related.empty:
        return classify_only(candidate, "reinforcement")  # or unknown
    rel = classify_relationship(candidate, related)  # reinforcement | duplicate | refinement | contradiction
    if rel == "contradiction":
        conflict = build_conflict_object(candidate, related, scores=compute_scores(...))
        write_derived_json(user_id, "derived/conflicts/" + conflict.conflict_id + ".json", conflict)
        emit_pipeline_event("conflict_detected", candidate_id, conflict.conflict_id, ...)
    annotate_review_row(candidate.id, has_conflict_markers=(rel == "contradiction"), relationship_type=rel)
```

---

## 2. Classification (sketch)

```
function classify_relationship(candidate, existing_entries):
    if near_duplicate_text(candidate, existing_entries):
        return "duplicate"
    if strengthens_same_axis(candidate, existing_entries):
        return "reinforcement"
    if qualifies_or_narrows_without_negating(candidate, existing_entries):
        return "refinement"
    if semantic_opposition_or_mutually_exclusive(candidate, existing_entries):
        return "contradiction"
    return "reinforcement"  # default safe path; tune per lane
```

Use rules (`conflict_rules.yaml`), embeddings, or LLM **advisory** labels; human resolution remains authoritative for contradictions.

---

## 3. Merge gate (before `process_approved_candidates`)

```
function can_merge_candidate(candidate_id, user_id):
    if has_unresolved_contradiction(candidate_id, user_id):
        require operator_decision in allowed_resolutions
        if prompt_impact(candidate_id) and not operator_confirmed_prompt_delta:
            return false
    return true
```

---

## 4. On resolve + approve

```
function on_conflict_resolved(conflict_id, decision, note, approve_candidate, apply_prompt_delta, operator):
    assert decision in {growth, correction, context, reject_new, exception}
    load conflict + candidate from canonical queue
    emit_pipeline_event("conflict_resolved", ...)
    if approve_candidate and decision != "reject_new":
        apply_temporal_merge(decision, conflict.existing_entry_id, candidate, user_id)
        emit_pipeline_event("identity_superseded", ...)  # when applicable
    if apply_prompt_delta:
        merge_prompt_sections(...)
        emit_pipeline_event("prompt_delta_applied", ...)
    mark_conflict_resolved(conflict_id, decision, note, operator)
```

`apply_temporal_merge` implements §9–§10 of the engine spec (supersede, valid_until, successor entry, context split, exception flags).

---

## 5. Rebuild derived index

```
function rebuild_conflict_index(user_id):
    clear_or_scan derived/conflicts/*.json
    write derived/conflict-index.json sorted by status, strength, age
```

Run after queue edits if sidecars may be stale; derived dir is gitignored.
