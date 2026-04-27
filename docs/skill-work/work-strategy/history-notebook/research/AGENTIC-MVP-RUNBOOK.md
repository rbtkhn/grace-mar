# History-notebook agentic MVP runbook

**WORK only;** not Record.

This runbook wires self-library-bookshelf (`HNSRC-*`) into chapter operations with three generated outputs:

- [QUEUE-AUTOPRIORITY.md](QUEUE-AUTOPRIORITY.md) — what to draft next
- [PROVENANCE-PACKETS.md](PROVENANCE-PACKETS.md) — claim packets with confidence and verification tasks
- [REDTEAM-FINDINGS.md](REDTEAM-FINDINGS.md) — counterfactual challenge matrix

Coffee E membrane outputs:

- [BOOKSHELF-MEMBRANE-REPORT.md](BOOKSHELF-MEMBRANE-REPORT.md) — scored round/session rationale
- [BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md](BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md) — pending candidate drafts (work layer only)

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
python3 scripts/build_bookshelf_membrane_candidates.py --emit-round --round-index 1 --round-size 7
python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json
```

## Freshness checks (local + CI)

```bash
python3 scripts/build_hn_autopriority_queue.py --check
python3 scripts/build_hn_provenance_packets.py --check
python3 scripts/build_hn_redteam_findings.py --check
python3 scripts/build_bookshelf_membrane_candidates.py --emit-round --round-index 1 --round-size 7 --check
python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json --check
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
4. Coffee E self-knowledge quiz membrane:
   - Generate round prompt payload:
     - `python3 scripts/build_bookshelf_membrane_candidates.py --emit-round --round-index <N> --round-size 7`
   - Ask 5-10 MCQs in chat (`AskQuestion`) and append selected options to:
     - [bookshelf-membrane-responses.json](bookshelf-membrane-responses.json)
   - Build report + drafts:
     - `python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json`
   - Optional determinism gate:
     - `python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json --check`

## Interpretation quick-guide

- **Queue score high + low anchors**: prioritize source acquisition before deep drafting.
- **Provenance low confidence**: do not harden thesis language until at least one concrete shelf anchor is added.
- **Red-team disputed**: narrow scope, add rival explanation, and update claim wording with explicit limits.
