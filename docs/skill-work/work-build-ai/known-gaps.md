# work-build-ai known gaps

Explicit spec-to-implementation gaps for the `work-build-ai` territory.

Use this file to keep the territory honest about what is real versus what is still implied.

---

## Gaps

| Gap ID | Area | Problem | Consequence | Suggested fix | Status |
|-------|------|---------|-------------|---------------|--------|
| **BUILD-AI-GAP-001** | Handback provenance | `openclaw_stage.py` emits OpenClaw-specific metadata, but `/stage` currently collapses most of it into a generic browser-style staging path | OpenClaw-sourced candidates are hard to distinguish reliably in `recursion-gate.md`; benchmark and review claims are weakened | Preserve source metadata and artifact details end-to-end into staged candidate blocks or structured event-linked metadata | `open` |
| **BUILD-AI-GAP-002** | Benchmark reality | `economic-benchmarks.md` lists cost and provenance metrics that are not fully emitted today | Operators can overestimate observability and benchmark coverage | Add explicit instrumentation-status labels and mark blocked metrics plainly | `open` |
| **BUILD-AI-GAP-003** | Session continuity | Continuity reads are documented as a startup checklist, but there is no repo-local runtime hook or log confirming they happened | One of the territory's stated core roles remains advisory rather than verifiable | Either add a continuity-read logging path or reduce the claim to checklist guidance only | `open` |
| **BUILD-AI-GAP-004** | Source vocabulary | Docs often describe `source: openclaw` as candidate metadata, while implementation more often emits `candidate_source=openclaw` or `source=openclaw_stage` only in events | Terminology drift makes audit review and metrics design harder | Normalize the vocabulary in docs and code around candidate source vs event source | `open` |

---

## Triage rule

Fix provenance before chasing higher-level benchmark or workflow polish. Without provenance, the rest of the territory becomes harder to trust.
