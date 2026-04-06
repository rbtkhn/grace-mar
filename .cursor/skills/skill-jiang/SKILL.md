---
name: skill-jiang
preferred_activation: skill-jiang
description: >-
  Blind forward prediction on Jiang Predictive History: prefix-only lectures (NN ≤ k),
  predict k+1, reveal, score. Canonical audit: lecture-forward-chain-gt-BLIND-prefix-only.md.
  Volume IV game-theory-NN. WORK only; not Record.
version: 0.5.1
tags:
  - operator
  - work-jiang
  - predictive-history
---

# skill-jiang (forward chain)

**Preferred activation:** **`skill-jiang`**, **`jiang next lecture`**, **`gt forward chain`**.

**Purpose:** Build **calibrated priors** for the **next** lecture using **only** in-repo material for episodes **≤ k**, then **score** against **k+1** and merge durable rules into [CURSOR_APPENDIX.md](CURSOR_APPENDIX.md).

**Companion skills:** [work-jiang-feature-checklist](../work-jiang-feature-checklist/SKILL.md), [work-jiang-ingest-fallback](../work-jiang-ingest-fallback/SKILL.md).

---

## Canonical workflow (prefix-only calibration)

Use this loop for **honest** recursive calibration. Committed audit: **[`lecture-forward-chain-gt-BLIND-prefix-only.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND-prefix-only.md)** (`run_mode: prefix_only`). Machine tail: **[`registry/lecture-forward-chain-blind-prefix-only.jsonl`](../../../research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain-blind-prefix-only.jsonl)**.

For blind round **R** (prefix **1…R**, predict episode **R+1**):

1. **Ingest** — **Prior round** in the **prefix-only** BLIND only: **Scores**, **Adjustment**, **miss_taxonomy**. Plus **`scratch/gt-series-model.md`**. Do **not** use [`lecture-forward-chain-gt-BLIND.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND.md) (historical batch / oracle replay) as a hypothesis source.
2. **Bundle** — Emit `scratch/gt-prefix-R.md`:
   - **R = 1:** `bundle --prefix-end 1` (optional `--closed-loop` is a no-op for gate).
   - **R ≥ 2:** `bundle --closed-loop --prefix-end R …` after prior **`advance`** and non-empty series model.
   - **R ≥ 10:** add `--trim-at-full-transcript`; log `read_depth: summary` in the round section.
3. **Predict** — Write **`scratch/gt-predict-(R+1).md`** from **only** `gt-prefix-R.md` (+ step 1). See **Agent invariants** below.
4. **Reveal** — `reveal --episode $((R+1)) --require-prediction-path …/gt-predict-$(($R+1)).md`
5. **Log** — Append round section to **prefix-only** BLIND + one JSON line to **`lecture-forward-chain-blind-prefix-only.jsonl`** (`run_kind: prefix_only`).
6. **Advance** — `advance --completed-round R` → `scratch/gt-closed-loop-state.yaml`.
7. **Model** — Update **`gt-series-model.md`** (non-empty; encode mergeable **Adjustment**).

**Fresh calibration start:** `python3 scripts/work_jiang/forward_chain_blind_bundle.py advance --reset` (clears closed-loop state). Then seed **`gt-series-model.md`**, run **R = 1** without needing prior advance.

**Anti-leak (why bundle):** Ad-hoc `read_file` / `glob` leaks **k+1** (filenames, full lecture list, YAML). The script reads **only** episodes **1…R** for the bundle. Audit: `paths --prefix-end R` lists those paths only.

```bash
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \
  --prefix-end R -o research/external/work-jiang/prediction-tracking/scratch/gt-prefix-R.md
# R ≥ 10: add --trim-at-full-transcript
# R ≥ 2: add --closed-loop after prior advance + model

python3 scripts/work_jiang/forward_chain_blind_bundle.py reveal --episode $((R+1)) \
  --require-prediction-path research/external/work-jiang/prediction-tracking/scratch/gt-predict-$(($R+1)).md
```

Retrospective narrative (not a substitute for blind evidence): [`lecture-forward-chain-gt-01-18.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-01-18.md).

---

## Recursive accuracy (closed loop)

**Recursive accuracy** means the **predictor changes** round over round—not only that the log has an “Adjustment” field. Each **Adjustment** should **constrain** the next packet (down-weight falsified moves, add falsifiers from partials).

**Smoke / I/O only:** [`run_blind_chain_rounds.py`](../../../scripts/work_jiang/run_blind_chain_rounds.py) pre-seeds packets for **bundle/reveal ordering** checks—not calibration.

**Maintenance (not calibration):** [`closed_loop_gt18_runner.py`](../../../scripts/work_jiang/closed_loop_gt18_runner.py) (reveal→advance→bundle) and [`inject_blind_closed_loop_replays.py`](../../../scripts/work_jiang/inject_blind_closed_loop_replays.py) (BLIND markdown injection) do **not** make predictions honest.

---

### Agent invariants (non-negotiable)

When the operator invokes **skill-jiang**, **closed-loop**, **blind forward chain**, or edits **prediction-tracking** blind artifacts, the assistant **must**:

1. **Prefix-only predictions:** Draft **`gt-predict-(k+1).md` only from** the current **`gt-prefix-k.md`** bundle (plus **prior round** in **prefix-only** BLIND and **`gt-series-model.md`**). **Do not** use: memory of Volume IV order, **any** prediction/resolution text from [`lecture-forward-chain-gt-BLIND.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND.md), **glob/list** of `lectures/game-theory-*.md` for unopened episodes, **YouTube/metadata** for the next title, or training priors about “what usually comes next.”

2. **No arc-oracle closure:** Finishing **N rounds** or running **bulk scripts** is **not** permission to **shape hypotheses to match known lecture titles**. **Oracle / smoke** runs must be **explicit** and labeled **`run_mode: oracle_replay`** in BLIND; do **not** claim **prefix-only calibration**.

3. **Stop vs cheat:** If token pressure is high, **narrow read_depth** (H1 + metadata + At a glance + tags per episode) and **say so in the packet**—do **not** substitute **known outcomes**.

4. **Default on conflict:** If **“complete the chain fast”** conflicts with **closed-loop learning**, **default to prefix-only** and **ask** unless the operator explicitly chooses **smoke / oracle**.

See [`.cursor/rules/skill-jiang-closed-loop.mdc`](../../.cursor/rules/skill-jiang-closed-loop.mdc).

---

### Mechanical gate (script-enforced)

For **K ≥ 2**, **`bundle --closed-loop`** requires:

1. **`advance --completed-round (K−1)`** after the prior round was scored.
2. **Non-empty** `scratch/gt-series-model.md`.

**`--force`** bypasses checks (stderr warning)—maintenance only.

```bash
python3 scripts/work_jiang/forward_chain_blind_bundle.py advance --completed-round 1
python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle --closed-loop \
  --prefix-end 2 -o research/external/work-jiang/prediction-tracking/scratch/gt-prefix-2.md
```

Optional: `--closed-loop-state PATH`, `--series-model PATH` (also on `advance`).

---

## Anti-leak checklist (before predicting episode k+1)

- [ ] Open **only** `research/external/work-jiang/lectures/<series>-NN-*.md` for **NN ≤ k**.
- [ ] Do **not** open lecture **NN > k**; do **not** read `analysis/*` for episode **> k**.
- [ ] Do **not** use `metadata/sources.yaml` or `CHANNEL-VIDEO-INDEX.md` to learn **unopened** titles.
- [ ] Do **not** use Web / YouTube for **next title** during **backtest** chain.
- [ ] **Default corpus:** lectures only. Optional **sensitivity:** `analysis/*` for **NN ≤ k** only—label `mode: lectures+analysis_prefix`.

**Full-prefix rule:** Re-consult **all** of **01…k** in the bundle (full file when possible; minimum **H1, metadata, At a glance, Concepts tags**—note `read_depth` in log).

---

## Prediction packet template

```markdown
### Round k → predict gt-(k+1)
- **Prefix:** gt-01 … gt-k | **read_depth:** full | summary
- **run_mode:** prefix_only
- **H1 (ranked hypotheses)** — 2–4 bullets: topic + *why prefix supports it*
- **Falsifiers** — per hypothesis
- **Confidence:** low / med per hypothesis
- **skill_merge_id:** (optional)
```

---

## Resolution template

```markdown
### Resolution (gt-(k+1) opened)
- **Actual (one line):** title + thesis from At a glance / opening
- **Scores:** hit | partial | miss per hypothesis
- **miss_taxonomy:** (optional)
- **Adjustment:** one short mergeable paragraph for next round
```

---

## Scoring rubric

| Label | Meaning |
|-------|---------|
| **hit** | Top hypothesis matches **dominant** topic + mechanism. |
| **partial** | Right arc, wrong emphasis; or #2 was closer. |
| **miss** | Wrong frame or unpredicted pivot. |

---

## Logs (operator lane, not Record)

| Artifact | Role |
|----------|------|
| **`lecture-forward-chain-gt-BLIND-prefix-only.md`** | **Canonical** prefix-only calibration (append each round). |
| **`registry/lecture-forward-chain-blind-prefix-only.jsonl`** | Machine tail; `run_kind: prefix_only`. |
| **`lecture-forward-chain-gt-BLIND.md`** | **Historical** — templated batch + prior oracle replay; **not** for next-round hypotheses. |
| **`registry/lecture-forward-chain-blind.jsonl`** | Historical blind tail (includes batch + replay rows). |

Narrative / retrospective: `lecture-forward-chain-gt-01-18.md`. Do **not** conflate with `prediction-tracking/registry/predictions.jsonl` unless operator unifies.

---

## Skill merge cadence

After prefix-only rounds **3, 6, 9, 12, 15**, and **after gt-18** (optional: live **gt-19**):

1. Read **adjustments** + **miss_taxonomy** in **`lecture-forward-chain-gt-BLIND-prefix-only.md`** only.
2. Distill into [CURSOR_APPENDIX.md](CURSOR_APPENDIX.md) (cap ~15 active heuristics).
3. Bump **version** here + appendix **Changelog**.

---

## Live next episode (e.g. gt-19)

With **gt-18** in prefix: one prediction **before** new ingest; resolve when shipped; append **live_gt_19** to the **prefix-only** log; caveat appendix if heuristics break.

---

## Reference paths (grace-mar)

- Lectures: `research/external/work-jiang/lectures/game-theory-NN-*.md`
- Volume spec: `research/external/work-jiang/book/VOLUME-IV-GAME-THEORY.md`
- Transcript workflow: `research/external/work-jiang/WORKFLOW-transcripts.md`
- **Canonical blind log:** `prediction-tracking/lecture-forward-chain-gt-BLIND-prefix-only.md`
- **Canonical blind JSONL:** `prediction-tracking/registry/lecture-forward-chain-blind-prefix-only.jsonl`
- Historical blind log: `prediction-tracking/lecture-forward-chain-gt-BLIND.md`
- Bundle / reveal / paths / **advance** / **advance --reset:** `scripts/work_jiang/forward_chain_blind_bundle.py`
- Batch smoke helper: `scripts/work_jiang/run_blind_chain_rounds.py`
- Maintenance only: `scripts/work_jiang/closed_loop_gt18_runner.py`, `inject_blind_closed_loop_replays.py`

## Changelog (skill)

| Version | Notes |
|---------|--------|
| 0.5.1 | **Prefix-only loop complete:** rounds **1–17** through **gt-18** logged in canonical BLIND + JSONL; **`CURSOR_APPENDIX.md` v0.5.1** post–gt-18 distill (cadence merges folded). |
| 0.5.0 | **Reset contract:** canonical **prefix-only** BLIND + JSONL; **SKILL** rebuilt around one workflow; **historical** `lecture-forward-chain-gt-BLIND.md` quarantined for hypotheses; **`advance --reset`**; bulk runners = maintenance only. |
| 0.4.4 | Agent invariants + `skill-jiang-closed-loop.mdc`. |
| 0.4.3 | Closed-loop replay through gt-18 (mixed honesty); runner/inject scripts. |
| 0.4.2 | `bundle --closed-loop` + `advance`. |
| 0.4.1 | Closed loop documented; batch = smoke. |
| 0.4.0 | BLIND.md + blind JSONL (batch). |
| 0.3.0 | `forward_chain_blind_bundle.py`. |
| 0.2.0 | Volume IV backtest; appendix M3–M18. |
| 0.1.0 | Scaffold. |
