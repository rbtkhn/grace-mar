# Economic Benchmarks — work-dev

Benchmarks to track cost, value flow, and gate health for the Grace-Mar ↔ OpenClaw integration.

---

## How to read status

Every metric is labeled with exactly one of:

| Label | Meaning |
|-------|---------|
| **instrumented** | Durable data is emitted automatically when the named integration path runs (e.g. rows appended to `users/[id]/pipeline-events.jsonl` from hooks). |
| **manual** | Repo-local data exists, but computing the metric needs an explicit step: run a script (e.g. `continuity_read_log.py`, `recursion_gate_review.py`, `run_perf_suite.py`), parse `recursion-gate.md`, or follow a checklist. |
| **planned** | Not yet implemented; intended for a future release. |
| **blocked** | Not possible with current setup (e.g. needs external logs, or dependency not in place). |

**instrumented** does *not* mean “no human ever runs a command” — it means the integration **writes** the raw audit trail without a separate capture step. Gate-derived counts (pending age, merge rates) use **manual** because they are computed from markdown + events, not streamed as finished metrics.

Do not treat **planned** or **blocked** metrics as observable until instrumentation exists.

### Third-party / narrative “market temperature”

Analyst headlines and third-party TAM figures (e.g. McKinsey-style agent-commerce sizing) are **not** Grace-Mar instrumentation. Treat them as **external narrative / discourse** — useful for framing conversations, **not** as internal benchmarks, revenue truth, or automated metrics. They belong in research notes and partner talk, not in `pipeline-events.jsonl` or gate math unless you explicitly add a separate, labeled manual capture.

| Surface | Status | Notes |
|--------|--------|-------|
| Third-party market / TAM narratives | **manual** (narrative only) | Not instrumented in-repo; never substitute for Priority Five or integration tables above. See [research-agent-readable-writable-commerce.md](research-agent-readable-writable-commerce.md) for ingested discourse with the same boundary. |

---

## Current instrumentation status

| Surface | Status | Notes |
|--------|--------|-------|
| Export audit events | instrumented | `runtime_compat_export` events and harness audit are emitted by `openclaw_hook.py`. |
| Handback advisory events | instrumented | `intent_constitutional_critique` events are emitted by `openclaw_stage.py`. |
| OpenClaw-specific candidate provenance | instrumented | Preserved end-to-end in candidate blocks when staging via `openclaw_stage` → `/stage`. |
| Merge attribution from OpenClaw handback | instrumented | Candidate-level `candidate_source` and provenance fields written into `recursion-gate.md` at stage time. |
| Compute-ledger export / handback cost | planned | Integration scripts do not currently emit compute-ledger rows. |
| Session continuity read verification | manual | Live proof-of-read: `continuity_read_log.py` appends to `continuity-log.jsonl` when invoked (not on every OpenClaw session unless wired). **CI contract:** `tests/test_continuity_read_log.py` exercises `--dry-run` and required files for `grace-mar` on every test run. |

---

## Priority Five (instrument first)

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| **Handback count per week** | Number of `openclaw_stage` invocations | pipeline-events.jsonl, event logs | instrumented |
| **Record growth from OpenClaw** | ACT-* entries or merged Record growth attributable to OpenClaw handback | self-evidence.md, self.md, event trail | blocked |
| **Merge rate from handback** | Approved / total OpenClaw-sourced candidates | recursion-gate.md + candidate_source | manual |
| **Cost per export / handback** | Token or execution cost for `openclaw_hook` / `openclaw_stage` | compute-ledger.jsonl | planned |
| **Time in gate** | Days from stage to approve/reject for OpenClaw-sourced candidates | recursion-gate.md timestamps + staged events | manual |

---

## Full Benchmark Set

### Integration cost

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Export cost per run | Token or execution cost for identity export (`openclaw_hook`) | compute-ledger.jsonl | planned |
| Handback cost per stage | Token or execution cost for `openclaw_stage` | compute-ledger.jsonl | planned |
| Export frequency | Exports per week | pipeline events, harness events | instrumented |
| Handback frequency | `openclaw_stage` invocations per week | pipeline-events.jsonl, event logs | instrumented |

### Value flows

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Record → OpenClaw delivery | Exports actually consumed in OpenClaw sessions | export events + external OpenClaw session logs | blocked |
| OpenClaw → Record capture | ACT-* entries or merge artifacts attributable to OpenClaw handback | self-evidence.md + event trail | blocked |
| IX growth from handback | New IX-A/B/C entries merged from OpenClaw-sourced candidates | self.md + event trail | blocked |
| Merge rate from OpenClaw | Approved / total OpenClaw-sourced candidates | recursion-gate.md + candidate_source | manual |

### Gate health

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Time in gate (OpenClaw-sourced) | Days from stage to approve/reject | recursion-gate.md timestamps + staged events | manual |
| Rejection rate (OpenClaw) | Rejected / total OpenClaw-sourced | recursion-gate.md + candidate_source | manual |
| Constitutional advisory flags | `advisory_flagged` events from handback | pipeline-events.jsonl | instrumented |

### Efficiency

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Export latency | Time from trigger to export completion | `scripts/run_perf_suite.py --tier 2` (export_prp, manifest, runtime_bundle, fork) | manual |
| Handback latency | Time from `openclaw_stage` to staged candidate | script timing or wrapper logs | manual |
| Session continuity reads | Proof that SESSION-LOG, RECURSION-GATE, EVIDENCE were read before OpenClaw | continuity-log.jsonl (live); CI dry-run + file presence via `tests/test_continuity_read_log.py` | manual |

### Utilization

| Metric | Description | Source | Status |
|--------|-------------|--------|--------|
| Sessions with export | OpenClaw sessions that use a fresh export | OpenClaw logs | blocked |
| Sessions with handback | OpenClaw sessions that trigger `openclaw_stage` | event logs | instrumented |
| Handback-to-merge ratio | Merged records / handback invocations | pipeline events + merge trail | manual |

---

## Instrumentation Notes

- **pipeline-events.jsonl** — Export and advisory events are emitted; candidate attribution uses recursion-gate.md `candidate_source` and provenance fields.
- **recursion-gate.md** — OpenClaw-sourced candidates carry `candidate_source: openclaw` and optional artifact/constitution metadata for gate metrics.
- **continuity-log.jsonl** — Written by `scripts/continuity_read_log.py` when invoked; one line per proof-of-read (session-log, recursion-gate, self-evidence). Gitignored. **CI:** `tests/test_continuity_read_log.py` does not append; it validates `--dry-run` output and that those paths exist under `users/grace-mar/`.
- **compute-ledger.jsonl** — `openclaw_hook` and `openclaw_stage` do not currently emit cost rows (planned).
- **Aggregation script** — Planned: `scripts/openclaw_benchmarks.py` (not in repo yet) would summarize metrics from the above sources.
