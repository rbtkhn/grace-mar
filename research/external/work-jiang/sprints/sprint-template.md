# Sprint template — work-jiang (Grace-Mar)

**Use:** Copy to a dated file (e.g. `SPRINT-YYYY-MM-topic.md`) for a **multi-step** work-jiang tranche. Single artifacts can go straight through [scripts/jiang-compress.py](../../../scripts/jiang-compress.py) into [`../compressions/`](../compressions/).

**Lane:** `research/external/work-jiang/` — **not** Record until merged through **RECURSION-GATE** ([identity-fork-protocol.md](../../../docs/identity-fork-protocol.md)).

---

## Sprint meta

| Field | Value |
|--------|--------|
| **Name** | |
| **Start / end** | |
| **Owner** | operator / instance id |
| **Compression outputs** | (paths under `compressions/*.json` as you create them) |

---

## Clear objectives (Bloom: “what done looks like”)

- Tie to **founding intent** when present: `users/<id>/reflection-proposals/SEED-founding-intent.md`
- Tie to **seed** when present: `users/<id>/seed/minimal-core.json` ([seed-phase-wizard.md](../../../docs/seed-phase-wizard.md))

**This sprint’s objectives (3 bullets max):**

1.
2.
3.

---

## Orientation

- **Daily intention** (optional): append via `jiang-compress.py` or hand-edit `reflection-proposals/DAILY-INTENTION-YYYY-MM-DD.md`
- **Good morning context:** [good-morning-brief.py](../../../scripts/good-morning-brief.py)

---

## Flow check (~80–85% “in the zone”)

Self-assessment only — **not** a scored metric in-repo.

| Session | Felt difficulty (too easy / in zone / overwhelmed) | Adjust next session |
|---------|------------------------------------------------------|---------------------|
| | | |

If work is **ready to build on**, run compression:

```bash
python3 scripts/jiang-compress.py -u <id> --input <path-to-artifact.md>
# Optional: --print-gate-stub  then paste into users/<id>/recursion-gate.md if SELF/EVIDENCE should change
```

---

## Evidence and traceability

- **Activity / ACT / READ ids:** cite `users/<id>/self-evidence.md`, `self-archive.md`, or artifact paths under `users/<id>/artifacts/`
- **Do not** reference fictional paths (`self-evidence/` as a folder, `gate-guardian`, template-only scripts)

---

## Gate and merge

- **WORK-only** updates in `research/external/work-jiang/` may need **no** gate
- **Record changes** → stage in `users/<id>/recursion-gate.md`, companion approval, then [process_approved_candidates.py](../../../scripts/process_approved_candidates.py) (do not hand-edit SELF/EVIDENCE per AGENTS.md)

---

## Retro (end of sprint)

- What was **actually** learned vs planned?
- What belongs in **skill-think** vs **skill-write** vs **WORK** next?
- Link final compression JSON path(s):
