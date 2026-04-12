# Skill candidates backlog (pointer log)

**Purpose:** Make **skill discovery** cheap. One line per idea beats a blank page. This file is **not** the Record; it is operator / execution-layer memory. Trim or archive rows when stale.

**Ladder (see [README](README.md)):** (1) line here → (2) draft under [`_drafts/`](_drafts/) → (3) promote portable core + manifest + `sync_portable_skills.py`.

**Hygiene (doc-only loop):** On a quiet pass (e.g. monthly), **strike or mark** rows with **no draft** after **~90 days** unless you still intend to build them — or move the pointer to `_drafts/`. Promoted rows should read `*(promoted)*` like the examples below.

**How to append:** Add a row under **Log** (newest first or oldest first — pick one habit; default **newest at bottom**).

| Field | What to write |
|--------|----------------|
| **Date** | `YYYY-MM-DD` (local) |
| **Working name** | `hyphenated-skill-name` (draft) |
| **Trigger** | When the agent or you should invoke it (one short phrase) |
| **Pointer** | Transcript path, session id, commit hash, or “this thread” |

---

## Log

| Date | Working name | Trigger | Pointer |
|------|--------------|---------|---------|
| 2026-03-29 | portable-skills-sync | *(promoted)* — use skill **`portable-skills-sync`** (`.cursor/skills/portable-skills-sync/SKILL.md`); same trigger | `skills-portable/portable-skills-sync/SKILL.md` + manifest |
| 2026-03-31 | work-jiang-ingest-fallback | *(promoted)* — use skill **`work-jiang-ingest-fallback`** (`.cursor/skills/work-jiang-ingest-fallback/SKILL.md`); same trigger | `skills-portable/work-jiang-ingest-fallback/SKILL.md` + manifest |
| 2026-03-31 | skill-narrative | *(promoted)* — use skill **`skill-narrative`** (`.cursor/skills/skill-narrative/SKILL.md`); trigger `narrative loop` | `skills-portable/skill-narrative/SKILL.md` + manifest |
| 2026-03-31 | repo-hygiene-pass | *(promoted)* — use skill **`repo-hygiene-pass`** (`.cursor/skills/repo-hygiene-pass/SKILL.md`); trigger `hygiene pass` | `skills-portable/repo-hygiene-pass/SKILL.md` + manifest |
| 2026-04-05 | memory-self-audit | `self-memory audit`, `audit MEMORY four dimensions`, `memory-self-audit` — run rubric + table for `users/<id>/self-memory.md` | `docs/memory-self-audit.md` (+ template §VIII); shipped `74ac84f`; full SKILL: `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-06 | work-jiang-volume-wiring-audit | `volume wiring audit`, `gt-* corpus audit`, `game theory book track drift` — cross-check `sources.yaml` / `source-map` / `book-architecture` / analysis memos / JSONL layers vs operator docs; patch drift (e.g. `volume-iv-book-track-conventions.md`, `VOLUME-IV-GAME-THEORY.md`) | shipped doc sync `a4967f9`; promote via `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-07 | template-sync-lockfile | `steward E` + implement → `template_diff.py --lock` — SHA-pinned lockfile for companion-self sync with direction detection (⬇ upstream / ⬆ instance / ⬆⬇ both) | this thread; `scripts/template_diff.py` `_git_blob_sha` + `template-sync.lock.json`; inspired by SynapCLI lockfile pattern |
| 2026-04-07 | search-evidence | `search evidence`, `find in evidence`, `what does the Record say about X` — TF-IDF search over self-archive.md entries; stdlib-only, no dependencies | `scripts/search_evidence.py`; 186 entries indexed; inspired by MemPalace eval → one-script alternative |
| 2026-04-08 | diplomacy-framework-pack | `Islamabad Framework`, `roadmap not treaty`, `public preamble + 5 paras` vs `operator edition` (annexes + rubric); README + STRATEGY §IV pointer; distribution disclaimers | `docs/skill-work/work-strategy/islamabad-framework.md`, `islamabad-framework-operator-edition.md`, intake `research/external/work-jiang/intake/Islamabad-5-point-reconciliation-plan-with-jiang-commentary.md`, `us-framed-five-point-gulf-peace-framework-2026-04-08.md`; STRATEGY §IV `250b1d2`; promote via `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-10 | xavier-journal-ob1-digest | `xavier journal digest`, `OB1 day entry from GitHub`, `seed xavier-journal from commits` — L1 GitHub + L2 `inbox/`, optional `--full-day-synthesis` (strategy-notebook block + session-transcript), L3 artifacts → `YYYY-MM-DD.md`; default repo `Xavier-x01/Cici` | `scripts/xavier_journal_ob1_digest.py`, `tests/test_xavier_journal_ob1_digest.py`, `docs/skill-work/work-xavier/xavier-journal/README.md`, `SYNTHESIS-SOURCES.md`; promote via `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-10 | persian-regime-adaptive-strategy | `regime strategy`, `persian strategy`, `regime switch` — three-mode strategy lens (tolerance / parity / compression) from Persian civilizational patterns; WORK only | `_drafts/persian-regime-adaptive-strategy/SKILL.md`; promote to `skills-portable/` + `manifest.yaml` + `sync_portable_skills.py --verify` |
| 2026-04-10 | russian-endurance-compression-strategy | `endurance strategy`, `russian strategy`, `compression strategy` — endurance / temporal compression / rupture-regeneration lens; orthogonal to Persian draft | `_drafts/russian-endurance-compression-strategy/SKILL.md` + `notes.md`; same promotion ladder |
| 2026-04-11 | work-dev-integrity-gap-smoke | `integrity green`, `exports refresh`, `gap smoke` — after `validate-integrity.py` reports stale derived exports: `refresh_derived_exports.py -u <id>` → re-validate; then BUILD-AI-GAP smoke: `pytest tests/test_validate_handback_analysis.py` + `generate_scenarios.py --scenario handback --format markdown` (extend with CI wiring when promoting) | this thread; `scripts/refresh_derived_exports.py`, `docs/skill-work/work-dev/workspace.md` § Next actions 4–5, `known-gaps.md` GAP-005/006; fuller step: `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-11 | factorial-scenario-matrix | `GAP-005`, `handback tail stress`, `regenerate scenario matrix`, `variation-types harness` — expand `handback_tail_stress.yaml` to markdown/json via `generate_scenarios.py`; per-stressor injection map vs V-01–V-08 | `docs/skill-work/work-dev/scenarios/baseline_scenarios/README.md`, `scenarios/handback_tail_stress.matrix.md`, `scripts/work_dev/generate_scenarios.py`; shipped `5b4d2a9`; promote via `.cursor/skills/extract-skill-from-session/SKILL.md` |
| 2026-04-11 | repo-feedback-prompt | *(promoted)* — use skill **`repo-feedback-prompt`** (`.cursor/skills/repo-feedback-prompt/SKILL.md`); same trigger | `skills-portable/repo-feedback-prompt/SKILL.md` + manifest; example reuses: [missouri](https://github.com/chrisvoncsefalvay/missouri), [agent-matrix](https://github.com/l0r3zz/agent-matrix) |
| 2026-04-11 | skill-xavier | *(promoted)* — use skill **`skill-xavier`** (`.cursor/skills/skill-xavier/SKILL.md`); triggers `skill-xavier`, `xavier journal`, `Cici day`, `OB1 learning log` — journal baseline from [xavier-journal](docs/skill-work/work-xavier/xavier-journal/README.md); port Mode B to [Cici](https://github.com/Xavier-x01/Cici) | `.cursor/skills/skill-xavier/SKILL.md`; portable copy: hand off folder to Cici `.cursor/skills/`; spec [`docs/skill-work/work-xavier/xavier-journal/README.md`](../docs/skill-work/work-xavier/xavier-journal/README.md) |
| 2026-04-12 | repo-hygiene-mixed-tree-example | `hygiene pass` on a **mixed** tree (scripts + generated + strategy docs + rules + `users/` + late edits) — use **`repo-hygiene-pass`**; bucket order: feature/tests → harness scripts → generated/work-dev → prose docs → Cursor rules/skills → instance/mirrors → straggler doc commits; then `sync_portable_skills.py --verify` + `validate_skills.py` + push | worked example `4ef092d..00e04cb` on `main`; skill `.cursor/skills/repo-hygiene-pass/SKILL.md` |
