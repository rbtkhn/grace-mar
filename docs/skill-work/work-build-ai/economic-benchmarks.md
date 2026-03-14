# Economic Benchmarks — work-build-ai

Benchmarks to track cost, value flow, and gate health for the Grace-Mar ↔ OpenClaw integration.

---

## Current instrumentation status

| Surface | Status | Notes |
|--------|--------|-------|
| Export audit events | Instrumented | `runtime_compat_export` events and harness audit are emitted by `openclaw_hook.py`. |
| Handback advisory events | Instrumented | `intent_constitutional_critique` events are emitted by `openclaw_stage.py`. |
| OpenClaw-specific candidate provenance | Partial | Sender emits metadata, but staged candidates do not preserve the full provenance cleanly. |
| Merge attribution from OpenClaw handback | Partial | Event-level hints exist, but candidate-level attribution is not fully reliable. |
| Compute-ledger export / handback cost | Planned | Benchmarks mention this, but integration scripts do not currently emit those ledger rows. |
| Session continuity read verification | Documented only | Startup checklist exists in docs, but there is no repo-local proof that reads occurred. |

---

## Priority Five (instrument first)

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| **Handback count per week** | Number of `openclaw_stage` invocations | pipeline-events.jsonl, event logs | **instrumented** |
| **Record growth from OpenClaw** | ACT-* entries or merged Record growth attributable to OpenClaw handback | self-evidence.md, self.md, event trail | **partial** |
| **Merge rate from handback** | Approved / total OpenClaw-sourced candidates | recursion-gate.md metadata + events | **partial** |
| **Cost per export / handback** | Token or execution cost for `openclaw_hook` / `openclaw_stage` | compute-ledger.jsonl | **planned** |
| **Time in gate** | Days from stage to approve/reject for OpenClaw-sourced candidates | recursion-gate.md timestamps + staged events | **partial** |

---

## Full Benchmark Set

### Integration cost

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Export cost per run | Token or execution cost for identity export (`openclaw_hook`) | compute-ledger.jsonl | **planned** |
| Handback cost per stage | Token or execution cost for `openclaw_stage` | compute-ledger.jsonl | **planned** |
| Export frequency | Exports per week | pipeline events, harness events | **instrumented** |
| Handback frequency | `openclaw_stage` invocations per week | pipeline-events.jsonl, event logs | **instrumented** |

### Value flows

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Record → OpenClaw delivery | Exports actually consumed in OpenClaw sessions | export events + external OpenClaw session logs | **needs_external_logs** |
| OpenClaw → Record capture | ACT-* entries or merge artifacts attributable to OpenClaw handback | self-evidence.md + event trail | **partial** |
| IX growth from handback | New IX-A/B/C entries merged from OpenClaw-sourced candidates | self.md + event trail | **partial** |
| Merge rate from OpenClaw | Approved / total OpenClaw-sourced candidates | recursion-gate.md + events | **partial** |

### Gate health

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Time in gate (OpenClaw-sourced) | Days from stage to approve/reject | recursion-gate.md timestamps + staged events | **partial** |
| Rejection rate (OpenClaw) | Rejected / total OpenClaw-sourced | recursion-gate.md + events | **partial** |
| Constitutional advisory flags | `advisory_flagged` events from handback | pipeline-events.jsonl | **instrumented** |

### Efficiency

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Export latency | Time from trigger to export completion | script timing or wrapper logs | **manual** |
| Handback latency | Time from `openclaw_stage` to staged candidate | script timing or wrapper logs | **manual** |
| Session continuity reads | Frequency SESSION-LOG, RECURSION-GATE, EVIDENCE read before OpenClaw sessions | OpenClaw startup logs / checklists | **documented_only** |

### Utilization

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Sessions with export | OpenClaw sessions that use a fresh export | OpenClaw logs | **needs_external_logs** |
| Sessions with handback | OpenClaw sessions that trigger `openclaw_stage` | event logs | **instrumented** |
| Handback-to-merge ratio | Merged records / handback invocations | pipeline events + merge trail | **partial** |

---

## Instrumentation Notes

- **pipeline-events.jsonl** — Export and advisory events exist today; candidate attribution is still easier to recover from events than from staged candidate metadata.
- **recursion-gate.md** — Candidate-level `source: openclaw` is not reliable today; treat OpenClaw-specific gate metrics as partial until provenance is preserved end-to-end.
- **compute-ledger.jsonl** — `openclaw_hook` and `openclaw_stage` do not currently emit cost rows directly.
- **Aggregation script** — Optional: `scripts/openclaw_benchmarks.py` to summarize metrics from the above sources.
