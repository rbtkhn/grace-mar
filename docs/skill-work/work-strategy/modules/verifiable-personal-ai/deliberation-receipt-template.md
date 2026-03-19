# Deliberation receipt — template (WORK only)

Copy this file or the YAML block below per run. Store next to the draft (e.g. `work-business/…-receipt-2026-03-19.md`) or link from RECURSION-GATE candidate text.

---

## Receipt metadata (fill in)

```yaml
receipt_id: VPA-YYYY-MM-DD-001
created_at: YYYY-MM-DD HH:MM (timezone)
operator: <name or operator:cursor>
territory: work-strategy | work-politics | work-business | work-dev | other
topic_one_line: <e.g. WorldLand / weekly brief / client memo>
neutral_summary_ref: <path or “inline below”>
neutral_summary_hash_optional: <optional short hash or word count for drift check by eye>
sources_primary:
  - <url or doc path>
  - <url or doc path>
pipeline_steps_completed:
  perceiver: true | false
  energy_chokepoint_hook: true | false | n/a
  analyst_four_lens: true | false | n/a
  council_deliberation: true | false | n/a
  triangulation_three_lenses: true | false
  synthesis_after_minds: true | false
lens_manifest_version: <e.g. work-politics/analytical-lenses as of git SHA or date>
synthesis_artifact: <path to synthesis output or “inline in draft §X”>
draft_artifact: <path to markdown draft>
gate_status: not_staged | staged CANDIDATE-XXXX | approved_pending_merge
companion_approval_required_before_ship: true
self_evidence_note: none | optional ACT- only if companion approved candidate for audit line
```

## Checklist (human)

- [ ] Same neutral fact summary used for all three lenses (no lens-specific cherry-picking).
- [ ] Contradictions surfaced, not flattened.
- [ ] Final synthesis explicitly human (operator), not auto-shipped.
- [ ] No SELF/prompt merge implied by this receipt.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Draft owner | | |
| Reviewer (if any) | | |

---

## Optional: inline neutral summary anchor

*(Paste ≤200 words here only if `neutral_summary_ref` is “inline below”.)*

```

```
