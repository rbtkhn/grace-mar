# Enable sync pack for an instance

Use this runbook to enable manual sync for a new instance.

---

## 1) Choose source territory

Pick one or more source territories to mirror.

---

## 2) Create mirror folder in instance interface

Example target:

- `docs/skill-work/work-<instance>/work-<territory>-mirror/`

Add:

- `README.md` (instance explanation)
- `SYNC-CONTRACT.md` (from template)
- `SYNC-LOG.md` (from template)

---

## 3) Fill contract placeholders

Set:

- `{{territory}}`
- `{{source_path}}`
- `{{mirror_path}}`
- relevance criteria for that instance

Optional:

- keep or remove scoring rubric section

---

## 4) Wire navigation

Update local interface docs (typically):

- instance `README.md`
- instance `INDEX.md`
- any seed-context link page
- optional `GOOD-MORNING.md` routine
- if needed, copy/adapt `INITIAL-GOOD-MORNING.md` sequence

---

## 5) Decide mode

- **starter mode (default):** contract + log only
- **training mode (optional):** add `SYNC-DAILY.md` + staleness guardrail

---

## 6) Safety verification

Before first run, confirm:

- sync writes stay in mirror docs
- no direct Record writes
- identity implications route through gate
- human approval remains required for consequential/public changes

