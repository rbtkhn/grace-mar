# work-political-consulting workspace

Canonical operator entrypoint for the territory.

Use this file when you want one place to understand:

- current campaign state
- what is stale
- what is queued for X / content
- what sources feed the weekly brief
- how outreach is being framed and tracked
- what should stage to `RECURSION-GATE`

---

## Dashboard schema

| Section | Purpose | Canonical source |
|---------|---------|------------------|
| **Campaign status** | Principal, phase, days until primary, next critical dates | `principal-profile.md`, `calendar-2026.md` |
| **Active clients** | Multi-client consulting view: who is active, jurisdiction, channel_key | [clients/](clients/) + per-client sheets |
| **Compliance blockers** | Per-jurisdiction open items before new paid work | [compliance-checklist.md](compliance-checklist.md) + client templates |
| **Territory blockers** | Stale docs, placeholder-heavy research surfaces, missing WAP gate rhythm | Derived from `calendar-2026.md`, `opposition-brief.md`, `principal-profile.md`, `revenue-log.md`, `brief-source-registry.md`, `content-queue.md`, `users/grace-mar/recursion-gate.md` |
| **Pending WAP gate items** | WAP-only `RECURSION-GATE` review | `users/grace-mar/recursion-gate.md` via territory filter |
| **Brief readiness** | What sources feed the weekly brief and what still needs checking | `brief-source-registry.md` |
| **Content queue** | X / content workflow state for `@shadowcampain` | `content-queue.md` |
| **Revenue / offer state** | Revenue totals, BTC/SMM commitments, active commercial surfaces | `revenue-log.md`, `fiverr-microtask-100.md`, `account-x.md` |
| **Outreach learning** | Offer framing, proof, target segments, funnel, and objections | `outreach-workspace.md`, `offers.md`, `proof-ledger.md`, `target-registry.md`, `outreach-funnel.md`, `objection-log.md` |
| **Next actions** | Highest-leverage companion/operator actions now | Derived from the sections above |

---

## Canonical working files

| File | Role |
|------|------|
| `README.md` | Territory doctrine, scope, sync policy, and support menu |
| `consulting-charter.md` | Umbrella consulting mission + service lines (federal / state / local / intl) |
| `compliance-checklist.md` | Pre-engagement gates (FEC, state, FARA, intl) |
| `clients/` | Per-client index; [clients/massie-ky4.md](clients/massie-ky4.md) = primary client |
| `brief-source-registry.md` | Structured intake and freshness tracker for weekly brief inputs |
| `content-queue.md` | Structured X/content operations queue |
| `weekly-brief-template.md` | Output shape for the campaign brief |
| `civ-mem-draft-protocol.md` | Civ-mem → speech/policy; human-always-approves gates |
| `civ-mem-test-run-*.md` | Dated test runs (DRAFT until signed) |
| `principal-profile.md` | Principal baseline |
| `opposition-brief.md` | Living opposition tracker |
| `calendar-2026.md` | Election and compliance calendar |
| `revenue-log.md` | Revenue and allocation continuity |
| `outreach-workspace.md` | Canonical outreach entrypoint and workflow rhythm |
| `offers.md` | Current offer framing and low-risk entry offers |
| `proof-ledger.md` | Reusable proof fragments for outreach |
| `target-registry.md` | Narrow target segments and lead-source logic |
| `outreach-funnel.md` | Outreach tracking by stage |
| `objection-log.md` | Structured learning from objections and replies |

---

## Operating rhythm

1. Refresh `brief-source-registry.md` before the weekly brief.
2. Review `content-queue.md` before asking for post drafts.
3. Use the WAP dashboard/operator surface for territory blockers and next actions.
4. Use `outreach-workspace.md` when the work block is about offer testing, proof, and buyer learning rather than campaign execution.
5. Stage WAP milestones through `RECURSION-GATE` when something should become audited continuity or Record-adjacent knowledge.

---

## Guardrail

This workspace is a `WORK` surface. It does not create a second queue, and it does not change the gated merge rule.
