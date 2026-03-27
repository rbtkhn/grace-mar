# Gate vs change-review

Portable doctrine (template + instance). **Same file** in [companion-self](https://github.com/rbtkhn/companion-self) and [grace-mar](https://github.com/rbtkhn/grace-mar) so audits and onboarding do not fork the concept.

---

## Recursion gate (default path)

**`recursion-gate.md`** (or the instance’s canonical gate file) is where **routine** candidates land:

- analyst or operator stages YAML/structured blocks
- each item is a **proposed** line or change to SELF / EVIDENCE / prompt (per instance pipeline)
- the companion **approves, rejects, or edits** at the gate
- merge runs only after approval (**Sovereign Merge Rule**)

The gate answers: *“Should this observation become part of the governed Record next?”*

---

## Change-review queue (material escalation)

**`users/<id>/review-queue/`** holds **material** post-seed changes that need more than a single approve line:

- contradictions or revisions to durable commitments, safety, or memory governance
- cross-surface moves (identity vs SELF-LIBRARY vs CIV-MEM) that deserve an audit trail
- policy or prompt shifts that change how the Voice behaves
- explicit operator decision to escalate a gate item

Artifacts include **`change_review_queue.json`**, **`change_event_log.json`**, **`proposals/`**, **`decisions/`**, **`diffs/`** (see change-review validation docs).

This answers: *“Is this change **safe, scoped, and evidenced** enough to apply — and what did we believe before?”*

---

## Relationship

| | Recursion gate | Change-review |
|---|----------------|---------------|
| **Typical size** | One candidate, one merge batch | Proposal + decision + optional identity diff |
| **Authority** | Still no merge without approval | Still no merge without approval |
| **Provenance** | Gate YAML + pipeline | Queue + events + structured proposal |

The change-review queue **does not replace** the gate. Escalation **adds process**; it does not bypass the companion.

---

## When to escalate

Escalate from gate → change-review when:

- the edit is **high stakes** (identity/safety/memory policy), or
- reviewers need a **before/after** diff and a **decision record**, or
- the companion asks for **slow review** instead of same-session gate approval.

Keep routine IX-A/B/C lines and evidence-linked updates **on the gate** unless one of the above applies.

---

## Bridge tooling (grace-mar reference implementation)

In **grace-mar**, operators may run:

```bash
python3 scripts/export_gate_to_review_queue.py --user <fork_id> --candidate-id CANDIDATE-XXXX
```

That writes a proposal JSON, a **`derived/`** snapshot, and updates the queue and event log. Validate with:

```bash
python3 scripts/validate-change-review.py users/<fork_id>/review-queue --allow-empty
```

(`--allow-empty` is often needed until **decisions/** and **diffs/** contain matching artifacts; see [change-review-validation.md](change-review-validation.md).)

---

## See also

- [template-instance-contract.md](https://github.com/rbtkhn/companion-self/blob/main/docs/template-instance-contract.md) (companion-self) — compatibility roles
- [identity-fork-protocol.md](identity-fork-protocol.md) — IFP §4.1 workflow and §4.3 material escalation
- [boundary-review-queue.md](boundary-review-queue.md) — boundary classification vs gate
- [change-review.md](https://github.com/rbtkhn/companion-self/blob/main/docs/change-review.md) (companion-self) — governed self-revision doctrine
