# Moonshot Operating Model (PMOS v0.1)

**Status:** Active (WORK doctrine)  
**Scope:** Grace-Mar **Personal Moonshot OS** — governance-first scaffold. **Not** Record; **not** medical-by-default (domain-neutral moonshots).

## North star

- **civilization_memory / external research** and **operator intent** inform moonshots.
- **Long-horizon programs** are drafted in **[users/[id]/self-moonshots.md](../users/grace-mar/self-moonshots.md)** as **staging only** — not authoritative SELF until merged via the **gated pipeline**.
- **AI / assistants** **propose** and **stage** candidates; **companions** approve merges — same invariant as [AGENTS.md](AGENTS.md).

## v0.1 deliverables

| Deliverable | Path |
|-------------|------|
| Staging surface | `users/[id]/self-moonshots.md` |
| Template | [docs/skill-work/work-moonshots/moonshot-template.md](skill-work/work-moonshots/moonshot-template.md) |
| Lane README | [docs/skill-work/work-moonshots/README.md](skill-work/work-moonshots/README.md) |

**Out of v0.1:** Bot/CLI commands, data-ingestion connectors, HTML dashboards, “agent swarm” automation.

## Edit authority

| Actor | `self-moonshots.md` | Merge to `self.md` / EVIDENCE |
|-------|---------------------|--------------------------------|
| Companion / operator | Yes | Only via `process_approved_candidates.py` after approval |
| Assistant | **Do not** treat staging as merge authority — **stage** `CANDIDATE-*` in `recursion-gate.md` | Same as today |

## Promotion mapping (after approval)

| Content | Destination |
|---------|-------------|
| Durable **why** / values / identity-relevant commitments | `self.md` IX-B / IX-C (or IX-A if factual), with provenance |
| **Dated outcomes** (milestones, launches) | `self-archive.md` (ACT / CREATE / structured evidence per instance conventions) |
| Running experiments / next steps | Stay in `self-moonshots.md` or **self-memory** until promoted |

**EVIDENCE in v0.1:** Optional habit when a milestone is merged — **not** required to ship the scaffold.

## Voice / prompt / benchmarks (deferred)

- **v0.1** does **not** change [bot/prompt.py](../bot/prompt.py).
- After a gate merge touches profile text, use existing **identity delta** / voice checks per [instance-doctrine.md](../users/grace-mar/instance-doctrine.md) if applicable.

## Life portfolio / cross-moonshot synthesis (deferred)

- Overlaps between moonshots may be noted in **self-memory** (continuity) or a future **WORK** index — **not** a parallel Record.

## Example: recursion-gate block (moonshot promotion)

Use the same **`### CANDIDATE-XXXX`** + **```yaml** shape as [recursion-gate.md](../users/grace-mar/recursion-gate.md). Fields consumed by `process_approved_candidates.py` include **`summary`**, **`mind_category`**, **`profile_target`**, **`status`**, **`channel_key`**, **`source`**, and optional **`suggested_entry`**.

**Illustrative only** — use a new `### CANDIDATE-XXXX` heading in `recursion-gate.md`, then a fenced **`yaml`** block **below** it (same pattern as existing candidates). Assign a fresh id; keep the block **above** `## Processed` while **pending**. YAML body example:

```yaml
mind_category: curiosity
signal_type: moonshot_promotion
profile_target: IX-B. CURIOSITY
status: pending
channel_key: operator:cursor
source: users/grace-mar/self-moonshots.md
summary: "Promote active moonshot <moonshot-id> — durable curiosity line from staging"
suggested_entry: "(paste proposed IX line; companion edits before approve)"
```

**Align to live schema:** When staging real candidates, copy field names from the most recent approved block in `recursion-gate.md` and from [process_approved_candidates.py](../scripts/process_approved_candidates.py) YAML parsing.

## Security

- No secrets in `self-moonshots.md` or templates.
- No unfounded legal / medical / financial claims as Record facts; professional context belongs outside LLM inference.

## Related

- [Canonical paths — self-moonshots](canonical-paths.md) (staging row)
- [Id taxonomy — self-moonshots](id-taxonomy.md#standard-location-labels)
- [Identity fork protocol](identity-fork-protocol.md)
- [Promotion ladder](skill-work/work-strategy/promotion-ladder.md) (optional cross-link for long arcs)
