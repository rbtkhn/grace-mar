---
name: skill-jiang
preferred_activation: skill-jiang
description: >-
  Blind forward prediction on Jiang Predictive History lecture series: read only
  prefix lectures (NN ≤ k), predict episode k+1, then open and score. Volume IV
  default (game-theory-NN). Anti-leak checklist, templates, log path, recursive
  merges into CURSOR_APPENDIX.md. WORK only; not Record.
version: 0.4.4
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

## Closed loop (skill core — stepwise adjustment)

**Recursive accuracy** means the **predictor changes** round over round, not only that the log has an “Adjustment” field.

Before drafting **round K+1**’s prediction packet, the operator (or agent) **must** ingest:

1. **Prior BLIND log section** for round **K** (or the last completed round): **Scores** + **Adjustment** + **miss_taxonomy**.
2. Optional **rolling series model** (3–5 bullets) in `scratch/gt-series-model.md` (gitignored), updated **after each resolution** with one line added or revised from the **Adjustment**.

**Then** write hypotheses for **gt-(K+1)** so they **explicitly** reflect what failed or was refined last time (e.g. down-weight a falsified move, add a falsifier suggested by a partial). **Do not** use a fixed template bank for all K unless labeled **smoke / I/O test only** — that does **not** count as calibration.

**Batch helper caveat:** `scripts/work_jiang/run_blind_chain_rounds.py` pre-seeds packets for **engineering** checks of bundle/reveal ordering; it **does not** implement closed-loop learning. For **skill-jiang** as you intend it, run rounds **sequentially** with this section.

### Agent invariants (non-negotiable)

When the operator invokes **skill-jiang**, **closed-loop**, **blind forward chain**, or edits **prediction-tracking** blind artifacts, the assistant **must**:

1. **Prefix-only predictions:** Draft **`gt-predict-(k+1).md` only from** the current **`gt-prefix-k.md`** bundle (plus **prior round** scores/adjustment in BLIND and **`gt-series-model.md`**). **Do not** use: memory of Volume IV order, **H1 text from future rounds** in `lecture-forward-chain-gt-BLIND.md`, **glob/list** of `lectures/game-theory-*.md` for unopened episodes, **YouTube/metadata** for the next title, or **“what usually comes next”** from training data.

2. **No arc-oracle closure:** Finishing **N rounds** or running **bulk scripts** is **not** permission to **shape hypotheses to match known lecture titles**. If the operator wants **I/O smoke** or **oracle replay** (arc-shaped packets for audit only), they must **say so in prose**; the assistant labels the BLIND subsection **`run_mode: oracle_replay`** (or equivalent explicit tag) and does **not** claim **prefix-only calibration**.

3. **Stop vs cheat:** If token pressure makes full-prefix read hard, **narrow read_depth** (H1 + metadata + At a glance + tags per episode) and **say so in the packet** — do **not** substitute **known outcomes** to save tokens.

4. **Runner honesty:** `closed_loop_gt18_runner.py` is **mechanical glue** (reveal → advance → bundle). It does **not** write predictions and **does not** make a run honest; **honesty is entirely** in how **`gt-predict-*.md`** was authored.

5. **Default on conflict:** If instructions conflict (**“complete the chain fast”** vs **closed-loop learning**), **default to prefix-only** and **ask one clarifying question** unless the operator explicitly chooses **smoke / oracle**.

See also: [`.cursor/rules/skill-jiang-closed-loop.mdc`](../../.cursor/rules/skill-jiang-closed-loop.mdc).

### Mechanical gate (script-enforced)

For **K ≥ 2**, use **`bundle --closed-loop`** so the tool **refuses** the next prefix until:

1. **`advance --completed-round (K−1)`** has been run after you finished scoring the prior round (writes `scratch/gt-closed-loop-state.yaml`).
2. **`scratch/gt-series-model.md`** exists and is **non-empty** (rolling bullets from the last **Adjustment**).

**K = 1** is exempt (no prior round). **`--force`** bypasses checks (stderr warning) for maintenance only.

```bash
# After scoring the round that used --prefix-end 1 (predict gt-02, reveal, log):
python3 scripts/work_jiang/forward_chain_blind_bundle.py advance --completed-round 1
# Edit scratch/gt-series-model.md (non-empty), then:
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle --closed-loop \
  --prefix-end 2 -o research/external/work-jiang/prediction-tracking/scratch/gt-prefix-2.md
```

Optional: `--closed-loop-state PATH` and `--series-model PATH` override defaults (same flags on `advance` for state path).

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
- **Blind** machine tail: `research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain-blind.jsonl`
- Blind bundle script: `scripts/work_jiang/forward_chain_blind_bundle.py`
- Blind batch helper (optional): `scripts/work_jiang/run_blind_chain_rounds.py`
- Closed-loop bulk resume (reveal→advance→bundle): `scripts/work_jiang/closed_loop_gt18_runner.py`
- BLIND replay injection (maintenance): `scripts/work_jiang/inject_blind_closed_loop_replays.py`

## Changelog (skill)

| Version | Notes |
|---------|--------|
| 0.4.4 | **Agent tighten:** non-negotiable **prefix-only** prediction invariants; **oracle / smoke** must be explicit + labeled; Cursor rule `skill-jiang-closed-loop.mdc`. |
| 0.4.3 | **Closed-loop replay through gt-18:** full `advance` + rolling model + `bundle --closed-loop` run; BLIND **Replay** subsections (3–17) + JSONL `run_kind: replay`; `closed_loop_gt18_runner.py` + `inject_blind_closed_loop_replays.py`. |
| 0.4.2 | **Mechanical closed-loop gate:** `bundle --closed-loop` + `advance --completed-round N`; `gt-closed-loop-state.yaml` + non-empty `gt-series-model.md`; `--force` escape. |
| 0.4.1 | Document **closed loop**: each round must use prior **Adjustment** (+ optional rolling model); batch template script = I/O smoke only. |
| 0.4.0 | Full Volume IV blind chain logged (`lecture-forward-chain-gt-BLIND.md`); appendix v0.4 merge; blind JSONL. |
| 0.3.0 | Mechanical blind: `forward_chain_blind_bundle.py` (bundle / reveal / paths); retrospective log caveated. |
| 0.2.0 | Volume IV backtest logged; appendix populated from merges M3–M18. |
| 0.1.0 | Initial scaffold + templates. |
