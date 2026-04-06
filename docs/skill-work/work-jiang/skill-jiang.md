# skill-jiang (Cursor)

**Operator lane — not Record.**

Cursor skill for **blind forward prediction** on Predictive History lecture series (default Volume IV `game-theory-NN`): read only prefix episodes, predict the next, score, and **merge** lessons into the skill appendix on a fixed cadence.

- **Skill entrypoint:** [`.cursor/skills/skill-jiang/SKILL.md`](../../../.cursor/skills/skill-jiang/SKILL.md)
- **Learned heuristics (recursive layer):** [`.cursor/skills/skill-jiang/CURSOR_APPENDIX.md`](../../../.cursor/skills/skill-jiang/CURSOR_APPENDIX.md)
- **Volume IV chain log:** [`research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-01-18.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-01-18.md)

**Triggers (examples):** `skill-jiang`, `jiang next lecture`, `gt forward chain`.

**Mechanical blind:** `python3 scripts/work_jiang/forward_chain_blind_bundle.py` — `bundle` (prefix 1..K only), `reveal` (episode M for scoring), `paths` (audit). See skill body for the full sequence.

**Related:** [work-jiang-feature-checklist](../../../.cursor/skills/work-jiang-feature-checklist/SKILL.md), [work-jiang-ingest-fallback](../../../.cursor/skills/work-jiang-ingest-fallback/SKILL.md), [prediction-tracking README](../../../research/external/work-jiang/prediction-tracking/README.md).
