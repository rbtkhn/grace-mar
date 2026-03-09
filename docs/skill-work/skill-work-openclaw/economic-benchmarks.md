# Economic Benchmarks — skill-work-openclaw

Benchmarks to track cost, value flow, and gate health for the Grace-Mar ↔ OpenClaw integration.

---

## Priority Five (instrument first)

| Metric | Description | Source |
|--------|-------------|--------|
| **Handback count per week** | Number of `openclaw_stage` invocations | pipeline-events.jsonl, event logs |
| **Record growth from OpenClaw** | ACT-* entries with `source: openclaw`; IX-A/B/C entries merged from handback | self-evidence.md, self.md |
| **Merge rate from handback** | Approved / total OpenClaw-sourced candidates | recursion-gate.md metadata |
| **Cost per export / handback** | Token usage (openclaw_hook, openclaw_stage) | compute-ledger.jsonl |
| **Time in gate** | Days from stage to approve/reject for OpenClaw-sourced candidates | recursion-gate.md timestamps |

---

## Full Benchmark Set

### Integration cost

| Metric | Description | Source |
|--------|-------------|--------|
| Export cost per run | Token usage for identity export (openclaw_hook) | compute-ledger.jsonl |
| Handback cost per stage | Token usage for openclaw_stage (constitutional check, staging) | compute-ledger.jsonl |
| Export frequency | Exports per week | Pipeline/event logs |
| Handback frequency | openclaw_stage invocations per week | pipeline-events.jsonl, event logs |

### Value flows

| Metric | Description | Source |
|--------|-------------|--------|
| Record → OpenClaw delivery | Exports actually consumed in OpenClaw sessions | Export events + OpenClaw session logs |
| OpenClaw → Record capture | ACT-* entries with `source: openclaw` | self-evidence.md |
| IX growth from handback | New IX-A/B/C entries merged from OpenClaw-sourced candidates | self.md |
| Merge rate from OpenClaw | Approved / total OpenClaw-sourced candidates | recursion-gate.md |

### Gate health

| Metric | Description | Source |
|--------|-------------|--------|
| Time in gate (OpenClaw-sourced) | Days from stage to approve/reject | recursion-gate.md timestamps |
| Rejection rate (OpenClaw) | Rejected / total OpenClaw-sourced | recursion-gate.md |
| Constitutional advisory flags | `advisory_flagged` events from handback | pipeline-events.jsonl |

### Efficiency

| Metric | Description | Source |
|--------|-------------|--------|
| Export latency | Time from trigger to export completion | Script timing |
| Handback latency | Time from openclaw_stage to staged candidate | Script timing |
| Session continuity reads | Frequency SESSION-LOG, RECURSION-GATE, EVIDENCE read before OpenClaw sessions | OpenClaw startup logs / checklists |

### Utilization

| Metric | Description | Source |
|--------|-------------|--------|
| Sessions with export | OpenClaw sessions that use a fresh export | OpenClaw logs |
| Sessions with handback | OpenClaw sessions that trigger openclaw_stage | event logs |
| Handback-to-merge ratio | Merged records / handback invocations | Pipeline events |

---

## Instrumentation Notes

- **pipeline-events.jsonl** — Add `source: openclaw` to events from openclaw_stage and openclaw_hook.
- **recursion-gate.md** — Add `source: openclaw` to candidate metadata when staged via openclaw_stage.
- **compute-ledger.jsonl** — Ensure openclaw_hook and openclaw_stage emit token usage.
- **Aggregation script** — Optional: `scripts/openclaw_benchmarks.py` to summarize metrics from the above sources.
