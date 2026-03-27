# Companion-self Cursor pack — personas, rules, skills (product spec)

**Purpose:** Turn the “Cursor depth vs grace-mar” gap into a **small, template-native** `.cursor` pack for [companion-self](https://github.com/rbtkhn/companion-self). **Do not** copy grace-mar’s full rules/skills wholesale (wrong triggers, instance noise).

**Implementation home:** Add files under `companion-self/.cursor/rules/` and `companion-self/.cursor/skills/<name>/SKILL.md`. Keep existing **`long-term-objective.mdc`** and **`workspace-boundary.mdc`**; this spec **extends** them.

**Status (phase 1):** Implemented in the **companion-self** repo — `template-data-layers.mdc`, `users-tree-guard.mdc`, `generalize-from-reference.mdc`; skills `companion-self-first-hour`, `promote-from-grace-mar`; README Contents bullet for `.cursor/`. Phase 2 (instance owner) remains spec-only.

**Seed integration:** New instances record Cursor preset **intent** in **`seed_intake.json`** → optional **`cursor_operator_profile`** (validated by `seed-intake.v1.json`). See companion-self [docs/cursor-pack-from-seed.md](https://github.com/rbtkhn/companion-self/blob/main/docs/cursor-pack-from-seed.md). Generator script is still TBD; intake is the survey hook.

---

## Phase 1 (ship first) — Persona: **Template contributor**

**Who:** Maintainers and contributors working **in the upstream companion-self repo** — docs, `schema-registry/`, `users/_template/`, `users/demo/`, `scripts/`, student `app/`, manifests.

**Job-to-be-done:** Change the template **safely** (no intention drift, no instance Record leakage, no accidental grace-mar writes when multi-root).

### Rules (keep 2 + add 3 = 5 total)

| # | File | Metadata | One job |
|---|------|----------|---------|
| 1 | *(existing)* `long-term-objective.mdc` | `alwaysApply: true` | Strategic alignment (unchanged). |
| 2 | *(existing)* `workspace-boundary.mdc` | `alwaysApply: true` | No writes to grace-mar folder unless user overrides (unchanged). |
| 3 | **`template-data-layers.mdc`** | `alwaysApply: true` | **Three layers:** (A) template product surface — no one’s Record; (B) **`users/_template/`** — scaffold only; (C) **`users/demo/`** — synthetic demos / validation only, **never** a real person. Forbid treating demo artifacts as canonical identity truth. Point at `README.md` “Contents” and `docs/seed-phase.md`. |
| 4 | **`users-tree-guard.mdc`** | `globs: ["users/**"]` | Under `users/` in **this** repo, only **`_template/`** and **`demo/`** are standard. Any **new** top-level user directory is **out of pattern** for the template repo unless the human explicitly wants an in-repo sample (rare); default response: **use a forked instance repo** for real `users/<id>/`. Link `how-instances-consume-upgrades.md`. |
| 5 | **`generalize-from-reference.mdc`** | `globs: ["docs/**", "scripts/**", "bridges/**", "library/**"]` | When adapting material from **grace-mar** (read-only): **generalize** (no `grace-mar` user id, no private Record paths, no operator-only workflows). Prefer linking to grace-mar over pasting instance file trees. |

**Notes**

- Rule 4 avoids duplicating grace-mar’s `users/**` pipeline rule; template repo **users/** means something different.
- If `alwaysApply: true` count feels heavy, merge rules 3+5 into one file later; **start separate** for easier tuning.

### Skills (2)

| Skill folder | `description` (for Cursor) | What it does |
|--------------|---------------------------|--------------|
| **`companion-self-first-hour`** | First time opening companion-self in Cursor: orient, validate demo, optional app. | **Steps:** (1) Read root `README.md` + `companion-self-bootstrap.md` § first-run. (2) If user wants “smoke test”: run seed-phase validation from README (`pip install -r scripts/requirements-seed-phase.txt`, `validate-seed-phase.py` on `users/demo/seed-phase`, etc.). (3) Optional: `readme-student-app.md` — `cd app && npm install && npm start`. (4) **Do not** merge anything into a real Record; demo only. Output: short “you are here” map (template vs instance vs demo). |
| **`promote-from-grace-mar`** | Safely turn grace-mar reference into a template change proposal. | **Steps:** (1) Confirm **read-only** grace-mar (respect `workspace-boundary.mdc`). (2) Checklist: strip instance ids, PII, `users/grace-mar/**`, deployment secrets; align with `template-manifest.json` / `docs/instance-patterns.md` if relevant. (3) Output **proposal** (files + rationale); implement in **companion-self** only after human approval. Never edit grace-mar from this workspace unless user explicitly overrides. |

---

## Phase 2 (next) — Persona: **New instance owner**

**Who:** Someone who **forked** companion-self (or used “Use this template”) into **their own repo** — e.g. future `companion-xavier`. They may open **only** their fork in Cursor (no grace-mar sibling).

**Job-to-be-done:** Create **`users/<id>/`**, run **seed phase**, consume template upgrades — without copying another companion’s Record.

### Rules (3) — for **instance repo** (optional pack or fork-local `.cursor`)

These belong in **instance repos** once there is a **minimal instance scaffold** (or as documented “copy into your fork”). They are **not** required in upstream companion-self if you want the template repo to stay contributor-focused.

| # | File | Metadata | One job |
|---|------|----------|---------|
| 1 | **`instance-fork-boundary.mdc`** | `alwaysApply: true` | Your durable identity lives under **`users/<your-id>/`** after seed/readiness; create that tree from **`users/_template/`** on the template (or your fork’s copy), not from another instance’s export. Link `docs/seed-phase.md`, `how-instances-consume-upgrades.md`. |
| 2 | **`no-cross-instance-record.mdc`** | `globs: ["users/**"]` | Never copy `users/<other>/` from grace-mar or another companion into your repo. Leakage checklist language. |
| 3 | **`gate-before-merge.mdc`** | `alwaysApply: true` | If this instance uses a grace-mar-style pipeline: **stage** → companion **approve** → **merge script** only; no direct `self.md` / EVIDENCE edits by the agent. (Skip or soften if instance is docs-only until bot exists.) |

### Skills (1–2)

| Skill folder | `description` | What it does |
|--------------|---------------|--------------|
| **`instance-userdir-from-template`** | Create my `users/<id>/` from `_template` in a fork. | Copy scaffold, rename placeholders, set `id`, list required seed-phase paths, remind: no secrets in git. |
| **`seed-phase-validate-local`** | Run seed validation for my artifact dir. | Parameterize path `users/<id>/seed-phase`; same commands as README; interpret PASS/FAIL tersely. |

---

## Rollout order

1. **Implement Phase 1** in **companion-self** (3 new rules + 2 skills + README pointer: “Cursor: see …”).
2. **Dogfood** with `companion-self-and-grace-mar.code-workspace` (confirm rules don’t fight `workspace-boundary`).
3. **Phase 2** as **documented snippet** or **second skill-work doc** until instance scaffold is stable; then add to template or **instance generator** output.

---

## Explicit non-goals (for this pack)

- Daily operator politics, harness warmup, territory lists for `docs/skill-work/work-politics/**` — **grace-mar only**.
- Replacing `AGENTS.md`-scale prose in Cursor rules — keep rules **short**; link to `docs/`.

---

## Related (grace-mar)

- Template alignment and sync: [work-companion-self README](README.md), [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).
- Bootstrap copy in grace-mar: [bootstrap/companion-self-bootstrap.md](../../../bootstrap/companion-self-bootstrap.md).
