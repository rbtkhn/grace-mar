# WORK-JIANG BOOTSTRAP

Session bootstrap for continuing **work-jiang** (operator research lane: Jiang book/site) in a **new agent conversation**.

**Canonical membrane:** [research/external/work-jiang/README.md § Boundaries (membrane)](../research/external/work-jiang/README.md#boundaries-membrane) — research vs Record, candidates vs quotes, validators as gate.

**Skill:** [.cursor/skills/work-jiang-feature-checklist/SKILL.md](../.cursor/skills/work-jiang-feature-checklist/SKILL.md) — branch hygiene, verify block, CI, data model.

---

## Paste into message 1 (clean context)

State **Ship** vs **Think** and the concrete goal (e.g. “extend chronology for geo-08”, “fix validate_comparative_layer failure”).

If the thread may touch **`users/grace-mar/`** (SELF, RECURSION-GATE, pipeline, `work-jiang.md` beyond navigation), also run and paste:

```bash
python3 scripts/harness_warmup.py -u grace-mar --compact
```

Pure edits under `research/external/work-jiang/` and `scripts/work_jiang/` alone usually do not require warmup; use it when gate or Record state matters.

---

## Read before edits (order)

| # | File | Why |
|---|------|-----|
| 1 | [research/external/work-jiang/README.md](../research/external/work-jiang/README.md) | Production pipeline, § Boundaries, comparative vs argument layer |
| 2 | [.cursor/skills/work-jiang-feature-checklist/SKILL.md](../.cursor/skills/work-jiang-feature-checklist/SKILL.md) | Verify block, phased commits, guardrails |
| 3 | [users/grace-mar/work-jiang.md](../users/grace-mar/work-jiang.md) | Operator purpose; WORK container; links into research tree |
| 4 | [AGENTS.md](../AGENTS.md) | If merging Record: sovereign merge, no direct SELF/EVIDENCE without approval + script |

Skim as needed: `.github/workflows/work-jiang.yml` (generator order), `research/external/work-jiang/WORKFLOW-transcripts.md` (intake).

---

## Scope reminder

- **Lane:** **Geo-Strategy** — `lectures/geo-strategy-*.md` (#1–#12); **Civilization** — `lectures/civilization-*.md` + `civ-*` in `metadata/sources.yaml` when the task is that series. Default book tranche is Volume 1 (Geo-Strategy) unless the task says otherwise.
- **work-jiang is operator research** until content is merged through the gated pipeline into the Record; do not treat corpus as Voice knowledge.

---

## Canonical verify block (repo root)

After metadata, generator, or validator script changes, run the full block from the **work-jiang feature checklist** skill (same as [README production pipeline](../research/external/work-jiang/README.md#production-pipeline-book--site) through `validate_comparative_layer.py`). Trim only if the task truly skips comparative layer; otherwise run end-to-end to avoid drift.

Minimum when you touched **claims/concepts/packs only:**

```bash
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/validate_argument_layer.py
```

Add comparative validators when quotes, counter-readings, or chronology YAML changed.

---

## Non-negotiables

- Do **not** treat `metadata/quote-candidates.yaml` as polished quotations.
- Do **not** merge into `users/*/self.md`, `self-evidence.md`, or `bot/prompt.py` without companion approval and `process_approved_candidates.py` (see AGENTS.md).
- Prefer a **dedicated branch**; keep unrelated files out of the same commit when possible.

---

## End of session

- Short note: **what landed**, **what is uncommitted**, **one re-entry command** (often the verify block).
- If production paths or membrane rules changed, update `research/external/work-jiang/README.md` § Boundaries or pipeline; optional touch `docs/development-handoff.md` only if engineering-wide state shifted.

---

## Related

- [docs/audit-boundary-grace-mar-companion-self.md](../docs/audit-boundary-grace-mar-companion-self.md) — instance-wide grace-mar · template boundaries (not Jiang data rules)
- [bootstrap/grace-mar-bootstrap.md](grace-mar-bootstrap.md) — full-repo / work-dev default session
