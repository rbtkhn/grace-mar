# We read / we studied — THINK vs SELF IX

**Purpose:** One place for the operator ritual after shared reading, history, or study. **Governed by:** [skills-modularity.md](skills-modularity.md) §5, [pipeline-map.md](pipeline-map.md) READ flow.

---

## The fork (two paths)

| Path | What updates | Gate? |
|------|----------------|-------|
| **Intake / THINK** | `self-evidence.md` (READ-*), `skill-think.md`, optionally `skills.md` THINK | No gate for those files (operator edits directly per policy) |
| **Identity / IX** | `self.md` IX-A, IX-B, IX-C | **Yes** — RECURSION-GATE → approve → merge |

Stable facts she should *know* in-character → **IX-A** (after gate). Fleeting chat about a book → often **IX-B** or nothing. **Do not** duplicate every THINK bullet as IX-A.

---

## Checklist (after "we finished [title]" or heavy study)

1. **Evidence** — Add or update **READ-*** in `self-evidence.md` (title, date, tier, short notes).
2. **THINK** — Update `skill-think.md` (and `skills.md` THINK if you track claims there) with comprehension, vocabulary, interests *as intake*.
3. **IX (optional, separate)** — Stage **one or few** gate candidates only for lines that should live in **SELF** (knowledge / curiosity / personality). On the candidate YAML you may set:
   - `intake_evidence_id: READ-XXXX` — links IX row to the read log (merge script copies this into the IX entry).
   - Same as `evidence_ref: READ-XXXX` (alias).
4. **Approve** — Companion approves; merge runs → ACT-* + IX lines + prompt.

---

## Template: gate candidate after a book (copy into recursion-gate.md)

Use when a specific **fact or interest** should enter SELF (not the whole reading log).

```yaml
# Example — adjust CANDIDATE id, mind_category, suggested_entry
mind_category: knowledge   # or curiosity | personality
signal_type: knowledge     # or new_interest, etc.
priority_score: 3
summary: After reading [TITLE], companion retained [one concrete fact or theme].
example_from_exchange: "[short quote or paraphrase]"
profile_target: IX-A. KNOWLEDGE   # or IX-B / IX-C as appropriate
suggested_entry: "[single line for IX — one claim, not a paragraph]"
prompt_section: YOUR KNOWLEDGE
prompt_addition: "[mirror line for prompt] or none"
intake_evidence_id: READ-XXXX    # optional — your new READ id from step 1
status: pending
```

---

## Analyst / operator note

Bot analyst output cannot know your READ id until you log it. Operator-led sessions: log READ first, then stage with `intake_evidence_id` filled in.
