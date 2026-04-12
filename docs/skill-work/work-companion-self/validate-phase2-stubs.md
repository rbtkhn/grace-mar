# Validate CLI — Phase 2 documentation stubs

Orchestrator v1 is **read-only**. The following are **placeholders** for post-v1 work—expand before any `--fix` or gate-staging automation.

## Fix-level policy (`fix-level-policy-doc` todo)

Define **safe | moderate | aggressive** with explicit allowed effects on Record surfaces. No implementation until companion-approved design.

## Fix-helper matrix (`fix-helper-matrix` todo)

| Script | Eligible fix-level | Allowed staging | Forbidden |
|--------|-------------------|-----------------|-----------|
| TBD | TBD | CANDIDATE-shaped only | Direct writes to `self.md` / `self-archive.md` without gate |

## Gate staging design (`phase2-gate-staging` todo)

Auto-fix must emit **`### CANDIDATE-XXXX`** blocks with YAML keys consumed by `process_approved_candidates.py`—verify parser against live gate examples before implementation. No unstructured append to `recursion-gate.md`.
