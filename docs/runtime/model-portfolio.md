# Model Portfolio

**Status:** Human guide for runtime routing. Does not change `config/model_routing/*.yaml`.

Grace-Mar should use a portfolio of model capabilities rather than treating one model as the whole stack. The existing routing YAML remains the machine-readable policy surface; this document explains the operating shape in human terms.

## Portfolio Roles

| Role | Use for | Avoid for |
|------|---------|-----------|
| Deterministic / no model | Validation, manifests, regeneration, receipts, scripted transforms | Judgment, synthesis, uncertain interpretation |
| Fast local | Private routine drafting, repeated lane summaries, local recall, cheap iteration | High-stakes judgment, difficult code, external facts without lookup |
| Stronger local | Longer local synthesis, eval-style comparisons, private context-heavy work | Tasks needing frontier reasoning or current web facts |
| Specialized | Embeddings, speech, OCR, code indexing, transcript processing | General policy or identity judgment |
| Frontier / cloud | Hard reasoning, coding assistance, complex synthesis, current research with citations | Silent memory ownership, ungated Record edits, routine private loops |

## Existing Machine Policy

Use these as the current source for executable routing policy:

- `config/model_routing/model_tiers.yaml`
- `config/model_routing/task_policy.yaml`
- `docs/runtime/model-tier-routing.md`
- `scripts/runtime/model_policy.py`

This guide should not drift into a second routing table. If the portfolio semantics become executable, update the YAML and resolver directly.

## Local-First Defaults

- Prefer deterministic scripts for rebuildable artifacts.
- Prefer local or cheap models for repetitive, private, or context-heavy drafts.
- Use frontier/cloud models for rare, hard, or high-ambiguity work where reasoning quality matters.
- Keep receipts and source links when cloud output affects decisions.
- Never let a model tier override the Record gate.

## Follow-Up Hooks

Deferred until after v1:

- add explicit local/cloud provider categories to `model_tiers.yaml`
- add conductor or bridge routing-decision receipts
- add token/cost/eval accounting
- add automated fallback between providers
