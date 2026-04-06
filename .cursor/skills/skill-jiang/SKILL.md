---
name: skill-jiang
preferred_activation: skill-jiang
description: >-
  Blind forward prediction on Jiang Predictive History lecture series: read only
  prefix lectures (NN ≤ k), predict episode k+1, then open and score. Volume IV
  default (game-theory-NN). Anti-leak checklist, templates, log path, recursive
  merges into CURSOR_APPENDIX.md. WORK only; not Record.
version: 0.3.0
tags:
  - operator
  - work-jiang
  - predictive-history
---

# skill-jiang (forward chain)

**Preferred activation:** **`skill-jiang`**, **`jiang next lecture`**, **`gt forward chain`**.

**Purpose:** Develop **calibrated priors** for the **next** lecture in a series using **only** material already in-repo for episodes **≤ k**, then **score** against the actual **k+1** and **merge** lessons into [CURSOR_APPENDIX.md](CURSOR_APPENDIX.md).

**Companion skills:** [work-jiang-feature-checklist](../work-jiang-feature-checklist/SKILL.md), [work-jiang-ingest-fallback](../work-jiang-ingest-fallback/SKILL.md).

---

## Mechanical blind runs (original intent)

**Problem:** Ad-hoc `read_file` / `glob` easily leaks **k+1** (filenames, full lecture list, YAML, index).

**Fix:** Use the repo script so **only** episodes **1…K** are read for prediction; open **K+1** only after the prediction artifact exists.

```bash
# 1) Emit prefix only (write path = audit trail)
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \
  --prefix-end K -o prediction-tracking/scratch/gt-prefix-K.md

# Optional: omit ## Full transcript and below (smaller bundle, still blind)
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \
  --prefix-end K --trim-at-full-transcript -o prediction-tracking/scratch/gt-prefix-K.md

# 2) Draft prediction packet from that bundle only (no other lecture paths).

# 3) Reveal episode K+1 for scoring (after prediction file saved)
python3 scripts/work_jiang/forward_chain_blind_bundle.py reveal --episode $((K+1)) \
  --require-prediction-path prediction-tracking/scratch/gt-predict-$(($K+1)).md
```

**Audit:** `python3 scripts/work_jiang/forward_chain_blind_bundle.py paths --prefix-end K` lists **only** paths **1…K**.

The Volume IV log in `lecture-forward-chain-gt-01-18.md` was a **single-pass retrospective** simulation; **new** calibration runs should use **bundle + reveal** above (or equivalent strict I/O).

---

## Anti-leak checklist (before predicting episode k+1)

- [ ] Open **only** curated lectures: `research/external/work-jiang/lectures/<series>-NN-*.md` for **NN ≤ k** (Volume IV: `game-theory-01` … `game-theory-0k` with zero padding).
- [ ] Do **not** open lecture **NN > k**; do **not** read `analysis/*` for episode **> k**.
- [ ] Do **not** use `metadata/sources.yaml` rows (or `CHANNEL-VIDEO-INDEX.md`) for titles of **unreleased** or **not-yet-opened** episodes—YAML/index can **spoil** titles. Prefer **H1 + At a glance** from **opened** lecture files only.
- [ ] Do **not** use Web / YouTube for **next title** during **backtest** chain.
- [ ] **Default corpus:** **lectures only** (strict calibration). Optional **sensitivity run:** allow `analysis/*` for **NN ≤ k** only; label the log entry `mode: lectures+analysis_prefix`.

**Full-prefix rule (grace-mar operator choice):** Before each prediction, re-consult **all** of episode **01 … k** (entire markdown files when token budget allows; if constrained, minimum per episode: **H1, metadata block, At a glance, Concepts tags**—note `read_depth: summary` in the log).

---

## Prediction packet template (output before opening k+1)

```markdown
### Round k → predict gt-(k+1)
- **Prefix:** gt-01 … gt-k | **read_depth:** full | summary
- **H1 (ranked hypotheses)** — 2–4 bullets: topic + *why prefix supports it*
- **Falsifiers** — per hypothesis: what title/opening would kill it
- **Confidence:** low / med per hypothesis
- **skill_merge_id:** (optional) if promoting a candidate heuristic this round
```

---

## Resolution template (after opening lecture k+1)

```markdown
### Resolution (gt-(k+1) opened)
- **Actual (one line):** title + thesis from At a glance / opening
- **Scores:** H1a: hit|partial|miss; H1b: …
- **miss_taxonomy:** (optional) e.g. last_episode_overweight | new_case_study | title_literal_surprise | arc_correct_case_wrong
- **Adjustment:** one short paragraph — *mergeable* rule for next round
- **Heuristic candidates:** bullets only if rule survived ≥2 rounds or operator approves merge
```

---

## Scoring rubric (default)

| Label | Meaning |
|-------|---------|
| **hit** | Top hypothesis matches **dominant** topic + mechanism (not just a shared keyword). |
| **partial** | Right **arc** (e.g. “another law-of-* installment”) but wrong **case** or emphasis; or #2 hypothesis was closer. |
| **miss** | Wrong frame; next episode was a **pivot** not suggested by falsifiers, or misread prefix. |

---

## Log path

Append-only chain log (operator lane, not Record):

`research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-01-18.md`

Optional machine lines: `research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain.jsonl` (one JSON object per round).

Do **not** conflate with claim adjudication: `prediction-tracking/registry/predictions.jsonl` is **orthogonal** unless operator unifies later.

---

## Skill merge cadence (recursive accuracy)

After chain rounds **3, 6, 9, 12, 15**, and **after gt-18** (optional patch after **live gt-19**):

1. Read accumulated **adjustments** + **miss_taxonomy** tags in the chain log.
2. **Distill** into [CURSOR_APPENDIX.md](CURSOR_APPENDIX.md): rubric tweaks, checklist bullets, heuristics (max ~15 active), deprecated lines.
3. Bump **version** in this file frontmatter (`version:`) and add a row to appendix **Changelog**.

---

## Live next episode (e.g. gt-19)

After **gt-18** is in the prefix, run **one** prediction packet **before** any new ingest. Resolve when YouTube ships; append **live_gt_19** section to the chain log; if live breaks a heuristic, add **live vs backtest** caveat to appendix.

---

## Reference paths (grace-mar)

- Lectures: `research/external/work-jiang/lectures/game-theory-NN-*.md`
- Volume spec: `research/external/work-jiang/book/VOLUME-IV-GAME-THEORY.md`
- Transcript workflow: `research/external/work-jiang/WORKFLOW-transcripts.md`
- Forward-chain log: `research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-01-18.md`
- Machine tail: `research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain.jsonl`
- Blind bundle script: `scripts/work_jiang/forward_chain_blind_bundle.py`

## Changelog (skill)

| Version | Notes |
|---------|--------|
| 0.3.0 | Mechanical blind: `forward_chain_blind_bundle.py` (bundle / reveal / paths); retrospective log caveated. |
| 0.2.0 | Volume IV backtest logged; appendix populated from merges M3–M18. |
| 0.1.0 | Initial scaffold + templates. |
