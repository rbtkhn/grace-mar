# Observability

Companion-Self template · Inspectability without trusting agent self-report

---

## Why this exists

A governed companion system should not rely on **agent self-reporting alone**. Operators and reviewers should be able to see, from **data**:

- what proposals exist and their **status**
- which validations **passed or failed** (from real validator runs)
- which **Record surfaces** and **change scopes** proposals touch
- what **evidence types** support proposals
- how many proposals look **stale** (still open in early lifecycle states)

---

## Core principle

**Observability is not the Record.** It is an **inspection layer** over evidence, prepared context, change-review artifacts, validators, and (where instances expose them) audit logs. It does not approve merges and must not silently mutate governed state.

---

## Minimum observability surfaces

| Surface | Typical source |
|---------|----------------|
| Proposal queue summary | `users/<id>/review-queue/proposals/*.json` (Change Proposal v1) |
| Validation status | Subprocess runs of `validate-change-review.py` (and optionally `validate-seed-phase.py`) |
| Change-type summary | `changeType` field on proposals |
| Touched surfaces | `targetSurface`, `primaryScope`, `secondaryScopes` |
| Evidence-type summary | `supportingEvidence[].type` |
| Stale open proposals | Proposals in `proposed` or `under_review` older than a threshold (see report script) |

---

## Observability contract

The observability layer should help answer:

1. **What changed recently?** — Inspect proposal `createdAt`, event logs, and instance merge history (outside this doc).
2. **What is waiting for review?** — Count proposals by `status`; list open items under `review-queue/`.
3. **What failed validation?** — `validationSummary` in the generated report reflects **exit codes** from `scripts/validate-change-review.py` (and optional seed-phase validator), not guessed values.
4. **What contradictions are still open?** — Use proposal `changeType` (e.g. `contradiction`) and [contradiction-policy.md](contradiction-policy.md); fine-grained contradiction taxonomies may land in future proposal fields.
5. **What surfaces see the most proposal activity?** — `targetSurfaceCounts` and `scopeCounts` in the report.
6. **What evidence types are entering?** — `evidenceTypeCounts` from `supportingEvidence`.

### Non-goals

- Observability is **not** approval.
- Observability is **not** a hidden merge path.
- Observability outputs must **not** silently change governed state.

---

## Generated report

```bash
python3 scripts/build-observability-report.py
python3 scripts/build-observability-report.py --review-root users/_template/review-queue --skip-seed-validation
```

Default **`--review-root`** is **`users/demo/review-queue`**. Output: **`users/demo/observability/observability-report.json`** (directory created if missing).

**Policy (template):** The demo report is **intended to be committed** when regenerated after meaningful demo or script changes so operators and CI can diff it. Regenerate with the script; do not hand-edit as source of truth. If an instance prefers not to commit reports, gitignore `**/observability-report.json` locally and document that choice.

After the report shape is stable, it is validated against **`schema-registry/observability-report.v1.json`** by the same script (requires `jsonschema`).

---

## Related

- [change-review.md](change-review.md) — doctrine entrypoint
- [change-review-validation.md](change-review-validation.md) — validator commands
- [state-proposals.md](state-proposals.md) — Change Proposal v1
- [authority-map.md](authority-map.md) — write authority

---

Companion-Self template · Observability v1
