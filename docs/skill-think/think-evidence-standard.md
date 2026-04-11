# THINK — evidence standard and SSOT

## Pipeline order (unchanged)

1. **EVIDENCE** — READ/ACT rows in `self-archive.md` (or instance EVIDENCE path).
2. **THINK** — Capability intake in `skill-think.md` (prose) **and/or** structured [think-claims.json](../../artifacts/skill-think/think-claims.json).
3. **IX (optional)** — Gate-approved promotion to `self.md` when identity-facing.

## SSOT: prose vs JSON (Phase A)

| Surface | Role |
|---------|------|
| **`skill-think.md`** | Narrative, edge, rich context — **authoritative for tone and detail** |
| **`think-claims.json`** | Machine index for validation, observability, promotion flags — **must cite ≥1 `READ-*` or `ACT-*` id** |

**Rule:** When you add or change a structured claim, update **both** or delete the JSON row. The validator warns on schema issues; it does not auto-sync prose.

**Phase B (optional):** Single canonical source + generation — only if tooling is committed.

## Validator

`python3 scripts/validate_think_claims.py` — schema validation + advisory warnings (stale dates, high confidence with single evidence). Optional `--skill-think-md` to warn if `THINK-XXX` id is absent from prose.

## Anchors in prose (optional)

If you use claim ids in markdown (e.g. a line starting with **`THINK-001`**), the optional anchor check can detect drift.
