# Importing external working-identity candidates

Convert structured JSON from the [extraction prompt pack](extraction-prompt-pack.md) into governed candidate objects staged in `recursion-gate.md`.

---

## Expected input

A JSON file matching the extraction prompt pack contract — seven top-level keys as described in [extraction-prompt-pack.md](extraction-prompt-pack.md) and templated in [docs/templates/working-identity-extract-template.json](../templates/working-identity-extract-template.json).

The four layer sections (`domain_encoding`, `workflow_calibration`, `behavioral_calibration`, `artifact_rationale`) are processed. Each item may be a string (treated as a claim) or an object with `claim`, `confidence`, `durability`, and `examples` fields.

Items in `sensitivity_flags` are imported with `sensitivity_class: review_required` forced. `candidate_examples` and `merge_targets` are advisory and not directly staged.

---

## Usage

```bash
python3 scripts/import_working_identity_candidates.py \
  -u grace-mar \
  -f extract.json \
  --source-tool "ChatGPT"

python3 scripts/import_working_identity_candidates.py \
  -u grace-mar \
  -f extract.json \
  --dry-run
```

| Flag | Purpose |
|---|---|
| `-u` / `--user` | User ID (default: `grace-mar`) |
| `-f` / `--file` | Path to extraction JSON file (required) |
| `--source-tool` | Name of the AI system that produced the extract |
| `--dry-run` | Print candidate blocks without staging |

---

## What the script produces

1. **CANDIDATE blocks** in `users/<id>/recursion-gate.md` — one block per normalized item, inserted before `## Processed` using the existing staging infrastructure
2. **Import digest** at `artifacts/portable-record/import-digest-YYYY-MM-DD.md` — a read-only summary listing all staged candidates with their id, claim, target surface, and sensitivity class

### Default field values

| Field | Default | Rationale |
|---|---|---|
| `review_status` | `pending` | All imports require review |
| `sensitivity_class` | `review_required` | External content is untrusted until reviewed |
| `portability_class` | `cross_tool` | External extracts are inherently cross-tool |
| `durability_class` | `recurring` | Conservative default; reviewer adjusts |

### Layer-to-surface mapping

| Layer | Target surface |
|---|---|
| `domain_encoding` | SELF-LIBRARY |
| `workflow_calibration` | SKILLS |
| `behavioral_calibration` | SELF |
| `artifact_rationale` | EVIDENCE |

---

## Governance

All staged candidates are **non-canonical** until reviewed and approved through the gated pipeline. The import script writes to `recursion-gate.md` only — it does not touch SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or `bot/prompt.py`.

After staging, use the standard review workflow: review each candidate, set `status: approved` or `status: rejected`, then tell the assistant to process. For portability-specific review criteria, see the [portability review checklist](portability-review-checklist.md).

---

## Related

- [extraction-prompt-pack.md](extraction-prompt-pack.md) — how to produce the input JSON
- [working-identity-candidates.md](working-identity-candidates.md) — candidate schema and concept
- [portability-review-checklist.md](portability-review-checklist.md) — review supplement for WI candidates
- [promotion-rules.md](promotion-rules.md) — where approved candidates land in the Record
