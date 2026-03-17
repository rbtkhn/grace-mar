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
| **BUILD-AI-GAP-004** | Source vocabulary | Docs often describe `source: openclaw` as candidate metadata, while implementation more often emits `candidate_source=openclaw` or `source=openclaw_stage` only in events | Terminology drift makes audit review and metrics design harder | Normalize the vocabulary in docs and code around candidate source vs event source | `open` |

---

## Triage rule

Fix provenance before chasing higher-level benchmark or workflow polish. Without provenance, the rest of the territory becomes harder to trust.
