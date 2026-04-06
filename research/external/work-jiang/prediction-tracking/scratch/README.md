# scratch (gitignored)

Local-only **blind bundle**, **prediction** drafts, **`gt-series-model.md`** (rolling 3–5 bullets after each adjustment), and **`gt-closed-loop-state.yaml`** (written by `advance`) for **skill-jiang** (`.cursor/skills/skill-jiang/SKILL.md`). Other files in this directory are gitignored.

```bash
# After scoring round with prefix-end N:
python3 scripts/work_jiang/forward_chain_blind_bundle.py advance --completed-round N

# Next prefix (K≥2): use --closed-loop (requires state + non-empty gt-series-model.md)
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle --closed-loop --prefix-end K \
  -o research/external/work-jiang/prediction-tracking/scratch/gt-prefix-K.md
```
