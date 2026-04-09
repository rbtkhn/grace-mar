# OB1 Bridge — Operator Runbook

**Prerequisite:** An OB1 Supabase instance must be deployed before any of these workflows are usable. See [README.md](README.md) § Implementation triggers.

All workflows are **manual and operator-initiated**. No background process, no webhook, no scheduled job.

---

## Phase 1: Export (companion-self → OB1)

### When to export

- After a batch of gate merges (Record has grown meaningfully)
- When setting up a new OB1 instance for the first time
- When refreshing an OB1 deployment after extended companion-self work

### Workflow

1. **Review what will export.** Run the export script with `--dry-run` first:
   ```bash
   python3 scripts/export_open_brain_bundle.py -u <user-id> --dry-run
   ```
   Verify: governed surfaces (pending gate, session-log) are excluded. Only approved Record content appears.

2. **Run the export.** Remove `--dry-run`:
   ```bash
   python3 scripts/export_open_brain_bundle.py -u <user-id> -o ob1-export/
   ```
   Output: `ob1-export/` directory with `manifest.json`, content files, and `.meta.json` sidecars.

3. **Verify determinism.** Run the export again. The manifest and content fingerprints should match (content-addressed, not timestamp-dependent).

4. **Ingest into OB1.** Use OB1's recipe system or manual import path. The export bundle is self-describing (manifest lists files, schemas, and provenance).

5. **Do not commit the export bundle.** It is a transient artifact. The source of truth remains the companion-self repo files.

### What is excluded by default

| Surface | Reason |
|---------|--------|
| `recursion-gate.md` (pending candidates) | Unapproved content is not Record |
| `session-log.md` | Operational log, not identity |
| `self-memory.md` | Ephemeral continuity, not durable knowledge |
| `bot/prompt.py` | Derivative of SELF; not a primary source |
| `.git/`, `scripts/`, `tests/` | Infrastructure, not Record |

Override with `--include <surface>` if specific surfaces are needed for a use case.

---

## Phase 2: Import-staging (OB1 → companion-self)

### When to import

- When OB1 has accumulated thoughts from AI interactions that may contain identity-relevant material
- When a companion session happened through an OB1-connected client and produced signals not captured in companion-self
- **Not** as a routine sync — only when there is a reason to believe OB1 holds uncaptured material

### Workflow

1. **Export from OB1.** Use OB1's backup or export tooling to produce a local JSON file of thoughts. This step is OB1-side; no companion-self script is involved.

2. **Review the raw export.** Inspect the JSON to understand volume and content quality before running the import script.

3. **Run the import-staging script with `--dry-run`:**
   ```bash
   python3 scripts/import_ob1_to_proposals.py --input ob1-thoughts.json --dry-run
   ```
   Verify: low-grounded thoughts are filtered. Duplicates (by OB1 id + fingerprint) are skipped. Trust tiers are assigned. Target surfaces are reasonable.

4. **Run the import-staging script:**
   ```bash
   python3 scripts/import_ob1_to_proposals.py --input ob1-thoughts.json
   ```
   Output: proposal objects staged for review.

5. **Review proposals through the existing pipeline.** The companion reviews and approves/rejects each proposal through RECURSION-GATE, the same as any other candidate.

6. **Merge approved proposals:**
   ```bash
   python3 scripts/process_approved_candidates.py --apply
   ```

### What the import script never does

- Write to `self.md`, `self-archive.md`, or `bot/prompt.py`
- Auto-approve proposals
- Create a sync loop or schedule
- Skip grounding filters or trust-tier assignment
- Import without deduplication

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| Export produces different fingerprints on repeated runs | Non-deterministic content (timestamps in output?) | Check export script for time-dependent fields |
| Import stages duplicates | Dedup key mismatch (OB1 id changed?) | Verify OB1 thought IDs are stable across exports |
| Proposals reference unknown IX-A/B/C targets | Mapping rules need updating for new Record structure | Review [mapping.md](mapping.md) target surface rules |
| OB1 ingest rejects export bundle | OB1 schema version mismatch | Pin OB1 version; check recipe compatibility |

---

## Guardrails

- **Always dry-run first.** Both export and import scripts support `--dry-run`.
- **Never bypass the gate.** OB1 content enters through RECURSION-GATE like everything else.
- **No secrets in the repo.** Supabase credentials, API keys, and connection strings stay in the operator's local environment, never committed.
- **No unattended execution.** Do not cron, schedule, or automate these scripts.
