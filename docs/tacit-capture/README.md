# Tacit capture (Grace-Mar)

**Runtime / WORK only.** Markdown-first intake for lived observations, normalized to JSON, then optional **review-only** candidate objects. **Not** SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or Voice prompt truth.

**Related:** [runtime vs Record](../runtime-vs-record.md), [prepared-context layer](../prepared-context-layer.md), [moonshot operating model](../moonshot-operating-model.md).

---

## Intake format (raw `.md`)

Place files under `runtime/tacit/inbox/` (gitignored except `.gitkeep`) or pass any path to the normalizer.

```markdown
# Tacit Capture
source: voice_note
timestamp: 2026-04-19T09:12:00-07:00
lane: work-strategy
intended_destination: moonshot|work
confidence: high
privacy: shareable
tags: [negotiation, pattern]

## Raw note

Freeform text…
```

- **`intended_destination`:** pipe-separated tokens (`moonshot`, `skill`, `library`, `work`, `unknown`, …). Drives deterministic candidate types.
- **`confidence` / `privacy`:** `low|medium|high` and `private|shareable`.

---

## Commands

```bash
# 1) Normalize to JSON (+ optional index line)
python3 scripts/tacit/normalize_tacit_capture.py \
  --input path/to/note.md --repo-root . --append-index

# 2) Generate candidate JSON files
python3 scripts/tacit/generate_tacit_candidates.py \
  --normalized runtime/tacit/normalized/<id>.json

# 3) Optional human-readable render
python3 scripts/tacit/render_tacit_candidates_md.py runtime/tacit/candidates/*.json -o /tmp/candidates.md
```

**Fixtures (CI):** `tests/tacit/fixtures/inbox/demo-note.md` → golden JSON under `tests/tacit/fixtures/expected/`.

---

## Recursion-gate boundary

- Outputs stay under **`runtime/tacit/`** or **WORK** mission folders until you **manually** promote content.
- **Do not** append to `users/<id>/recursion-gate.md` from these scripts (e.g. [`recursion-gate.md`](../users/grace-mar/recursion-gate.md) for grace-mar).
- Optional [`render_tacit_candidates_md.py`](../../scripts/tacit/render_tacit_candidates_md.py) is for **copy-paste** only.
- Durable Record changes still require companion approval and `process_approved_candidates.py` per [AGENTS.md](../AGENTS.md).

---

## SELF vs MEMORY

- **SELF (`self.md`):** IX / self-knowledge updates **only** via gate + merge. This pipeline **does not** write `self.md`.
- **MEMORY (`self-memory.md`):** Optional continuity; **not** authoritative vs SELF. You may **manually** log follow-ups; no automatic tacit → MEMORY link in v1.

---

## End-to-end demo (mission-aware prepared context)

1. Normalize the fixture (or your own inbox file).
2. Generate candidates from the resulting normalized JSON.
3. Copy a summary into a mission intake folder (see [demo mission intake](../skill-work/work-moonshots/missions/demo-christianity-islam-bridge/intake/README.md)).
4. Include the mission spec in a **budgeted** prepared-context build (WORK / runtime; not canonical):

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy --mode medium \
  -q "mission" \
  -o prepared-context/tacit-mission-demo.md \
  --include-mission docs/skill-work/work-moonshots/missions/demo-christianity-islam-bridge/mission-spec.md
```

Same budget, inclusion/exclusion reporting, and boundary footer as other prepared-context builds. **`--include-checkpoint`** is equivalent priority; **`--include-mission`** labels pieces as `mission_workspace` in the Included list.

---

## Schemas

- [`schema-registry/tacit-capture-normalized.v1.json`](../../schema-registry/tacit-capture-normalized.v1.json)
- [`schema-registry/tacit-candidate.v1.json`](../../schema-registry/tacit-candidate.v1.json)

## Candidate types (v1)

See [candidate-types.md](candidate-types.md).

---

## Implementation status (v1)

**Implemented:** normalize → index append → deterministic candidates → optional markdown render; mission WORK tree under `work-moonshots/missions/`; `--include-mission` on `build_budgeted_context.py`; tests under `tests/tacit/`.

**Intentionally deferred:** LLM enrichment; automatic `recursion-gate.md` staging; optional exporter from tacit into `runtime/observations` for unified ranking.

**Governance:** No writes to SELF, EVIDENCE, SKILLS, or `bot/prompt.py`; gate merge path unchanged.
