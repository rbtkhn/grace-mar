# work-dev

Status: uninitialized

Purpose:
Development and technical-research work territory for this companion.

Optional pacing (WORK doctrine, not Record): for Pomodoro-style focus intervals inside the ~2-hour design ceiling, see [pomodoro-and-timeboxing.md](../../docs/skill-work/work-dev/pomodoro-and-timeboxing.md).

Initialization rule:
This module begins blank and is populated only from:

- seed-survey evidence
- explicit user input
- later governed work-layer updates

Boundary notes:

- `self-skill-work` tracks work-related skill claims and capability surfaces.
- `work-dev.md` tracks user-specific development and technical-systems context.
- This file is distinct from any operator-facing `work-dev` folder used for repo development or integration work (for example `docs/skill-work/work-dev/` in instance repos).

Canonical machine-readable seed shape:

- `users/_template/seed-phase/work_dev_seed.json`
- validated by `schema-registry/work-dev-seed.v1.json`

Promotion rule:
On seed activation, approved survey outputs are copied into this module and status changes from `uninitialized` to `initialized`.
