# work-business

Status: uninitialized

Purpose:
Business, market, and commercial-context work territory for this companion (ventures, research appetite, commerce surfaces—not operator research docs).

Initialization rule:
This module begins blank and is populated only from:

- seed-survey evidence
- explicit user input
- later governed work-layer updates

Boundary notes:

- `self-skill-work` tracks work-related skill claims and capability surfaces.
- `work-business.md` tracks user-specific business and commercial context for this companion.
- This file is distinct from the operator-facing **`docs/skill-work/work-business/`** tree in instance repos (deep research, territory READMEs, Grace Gems, etc.). That folder is documentation and execution space; this file is **instance context** for the companion.

Canonical machine-readable seed shape:

- `users/_template/seed-phase/work_business_seed.json`
- validated by `schema-registry/work-business-seed.v1.json`

Promotion rule:
On seed activation, approved survey outputs are copied into this module and status changes from `uninitialized` to `initialized`.
