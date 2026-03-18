# work-build-ai known gaps

Explicit spec-to-implementation gaps for the `work-build-ai` territory.

Use this file to keep the territory honest about what is real versus what is still implied.

---

## Gaps

| Gap ID | Area | Problem | Consequence | Suggested fix | Status |
|-------|------|---------|-------------|---------------|--------|
| **BUILD-AI-GAP-001** | Handback provenance | ~~`openclaw_stage.py` emits OpenClaw-specific metadata, but `/stage` currently collapses most of it~~ | — | Preserve source metadata and artifact details end-to-end into staged candidate blocks | `closed` — handback_server detects OpenClaw payload; passes staging_meta to core; _stage_candidate writes candidate_source, artifact_path, artifact_sha256, constitution_* into gate; recursion_gate_review parses them |
| **BUILD-AI-GAP-002** | Benchmark reality | ~~Benchmark docs lacked explicit status labels~~ | — | Add "How to read status" (instrumented \| manual \| planned \| blocked) and normalize all metric rows | `closed` — economic-benchmarks.md has legend and consistent labels |
| **BUILD-AI-GAP-003** | Session continuity | ~~No repo-local proof that continuity reads occurred~~ | — | Add a continuity-read logging path | `closed` — `scripts/continuity_read_log.py` writes to `continuity-log.jsonl`; doc in openclaw-integration.md § Proof-of-read |
| **BUILD-AI-GAP-004** | Source vocabulary | ~~Docs vs implementation used source vs candidate_source inconsistently~~ | — | Use `candidate_source` in gate blocks; `source=openclaw_stage` in event payloads | `closed` — canonical: candidate_source in recursion-gate YAML; source in events; integration-status and docs aligned |
| **BUILD-AI-GAP-005** | Factorial scenario library | No productized library or CLI to generate scenario × variation matrices for client agents | Tail failures stay invisible; engagements rely on ad hoc testing | Schema + templates per [variation-types.md](variation-types.md); optional script from historical staging logs | `open` |
| **BUILD-AI-GAP-006** | Reasoning vs action (handback) | No automated diff between OpenClaw “analysis” text and staged candidate classification / summary | Mismatch like “said high risk, staged low risk” can slip through | Rules or CI check on handback payloads; human checklist until automated | `planned` |
| **BUILD-AI-GAP-007** | Progressive autonomy metrics | No instrumented shadow-mode or tier promotion (pass rate on tails) | Hard to justify expanding agent scope safely | Log agent vs human decisions on edge cases; dashboard or JSONL | `planned` |

---

## Triage rule

Fix provenance before chasing higher-level benchmark or workflow polish. Without provenance, the rest of the territory becomes harder to trust.
