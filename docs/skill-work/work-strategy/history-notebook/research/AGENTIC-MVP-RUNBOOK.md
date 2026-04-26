# History-notebook agentic MVP runbook

**WORK only;** not Record.

This runbook wires self-library-bookshelf (`HNSRC-*`) into chapter operations with three generated outputs:

- [QUEUE-AUTOPRIORITY.md](QUEUE-AUTOPRIORITY.md) — what to draft next
- [PROVENANCE-PACKETS.md](PROVENANCE-PACKETS.md) — claim packets with confidence and verification tasks
- [REDTEAM-FINDINGS.md](REDTEAM-FINDINGS.md) — counterfactual challenge matrix

Config: [AGENTIC-MVP-CONFIG.yaml](AGENTIC-MVP-CONFIG.yaml).
Latest web metadata candidate pass (attach-then-merge workflow): [bookshelf-web-enrichment-2026-04-25.yaml](bookshelf-web-enrichment-2026-04-25.yaml).
Second candidate pass: [bookshelf-web-enrichment-2026-04-25-batch2.yaml](bookshelf-web-enrichment-2026-04-25-batch2.yaml).
Third candidate pass: [bookshelf-web-enrichment-2026-04-25-batch3.yaml](bookshelf-web-enrichment-2026-04-25-batch3.yaml).
Fourth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch4.yaml](bookshelf-web-enrichment-2026-04-25-batch4.yaml).
Fifth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch5.yaml](bookshelf-web-enrichment-2026-04-25-batch5.yaml).
Sixth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch6.yaml](bookshelf-web-enrichment-2026-04-25-batch6.yaml).
Seventh candidate pass: [bookshelf-web-enrichment-2026-04-25-batch7.yaml](bookshelf-web-enrichment-2026-04-25-batch7.yaml).
Eighth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch8.yaml](bookshelf-web-enrichment-2026-04-25-batch8.yaml).
Ninth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch9.yaml](bookshelf-web-enrichment-2026-04-25-batch9.yaml).
Tenth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch10.yaml](bookshelf-web-enrichment-2026-04-25-batch10.yaml).
Eleventh candidate pass: [bookshelf-web-enrichment-2026-04-25-batch11.yaml](bookshelf-web-enrichment-2026-04-25-batch11.yaml).
Twelfth candidate pass: [bookshelf-web-enrichment-2026-04-25-batch12.yaml](bookshelf-web-enrichment-2026-04-25-batch12.yaml).

## Generate all outputs

Run from repo root:

```bash
python3 scripts/build_hn_autopriority_queue.py
python3 scripts/build_hn_provenance_packets.py
python3 scripts/build_hn_redteam_findings.py
```

## Freshness checks (local + CI)

```bash
python3 scripts/build_hn_autopriority_queue.py --check
python3 scripts/build_hn_provenance_packets.py --check
python3 scripts/build_hn_redteam_findings.py --check
```

CI runs these in [`.github/workflows/test.yml`](../../../../.github/workflows/test.yml).

## Recommended regen sequence

1. Update shelf rows / chapter mapping:
   - [bookshelf-catalog.yaml](bookshelf-catalog.yaml)
   - [book-architecture.yaml](../book-architecture.yaml) (if chapter roster/status changed)
2. Validate and base exports:
   - `python3 scripts/validate_bookshelf_catalog.py`
   - `python3 scripts/build_hn_bookshelf_bibliography.py`
   - `python3 scripts/hn_shelf_anchors.py`
3. Regenerate the agentic outputs (three commands above).

## Interpretation quick-guide

- **Queue score high + low anchors**: prioritize source acquisition before deep drafting.
- **Provenance low confidence**: do not harden thesis language until at least one concrete shelf anchor is added.
- **Red-team disputed**: narrow scope, add rival explanation, and update claim wording with explicit limits.
