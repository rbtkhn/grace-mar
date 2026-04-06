# Jiang lectures — prediction accuracy tracking

**Purpose:** Log **forecast-like claims** from Jiang’s talks (especially Geo-Strategy / Predictive History), then **periodically resolve** them against **dated, citable** world events — for **operator research** and book/site honesty. **Not** Record truth until merged through the gate.

**Scope:** **Geo-Strategy (Volume I)** is the primary target for Part II prediction adjudication. The **Civilization** strand (Volume II) uses **Part II — Divergence** instead — see [`book/PART-II-CIVILIZATION-DIVERGENCE.md`](../book/PART-II-CIVILIZATION-DIVERGENCE.md) and [`divergence-tracking/README.md`](../divergence-tracking/README.md).

**What this is not:** A scoreboard to “debunk” or “prove” a person. It is a **discipline**: separate **strong predictions** (falsifiable, time-bounded) from **models / heuristics** (still useful if a specific forecast misses).

---

## Structural next-lecture chain (orthogonal)

**Purpose:** Blind **forward** exercise — predict lecture **k+1** from curated markdown for episodes **1…k** only, then score. Trains **skill-jiang** (Cursor) and produces **mergeable** heuristics; **not** the same as claim adjudication in `registry/predictions.jsonl`.

| Artifact | Path |
|----------|------|
| Human log + rubric | [lecture-forward-chain-gt-01-18.md](lecture-forward-chain-gt-01-18.md) (retrospective bake-off narrative) |
| **Blind** log (mechanical bundle + reveal) | [lecture-forward-chain-gt-BLIND.md](lecture-forward-chain-gt-BLIND.md) |
| Optional JSONL tail | [registry/lecture-forward-chain.jsonl](registry/lecture-forward-chain.jsonl) |
| Cursor skill | [`.cursor/skills/skill-jiang/SKILL.md`](../../../../.cursor/skills/skill-jiang/SKILL.md) |
| Blind bundle (prefix only / reveal k+1) | Run from repo root: `python3 scripts/work_jiang/forward_chain_blind_bundle.py` (`bundle`, `reveal`, `paths`) |

---

## Claim types

| Type | Example | Accuracy expectation |
|------|---------|----------------------|
| **Event** | “US will invade Iran” (yes/no by date T) | Binary / partial with evidence |
| **Time-bounded** | “Ground invasion possible in ~two years” | Check window; may be **partial** if “possible” not “certain” |
| **Conditional** | “If Trump wins, he likely initiates war vs Iran” | Resolve **antecedent** first, then **consequent** |
| **Trend** | “Dispensationalism becomes more popular” | Needs **operational metric** (polls, sales, membership) or mark **not_evaluable** |
| **Interpretive / model** | Asymmetry beats dominance in Millennium Challenge | Not a dated world event — track as **pedagogical claim**, not prediction |

---

## Resolution statuses

| Status | Meaning |
|--------|---------|
| `pending` | Before evaluation window or evidence not yet reviewed |
| `supported` | Outcome matches claim within stated vagueness |
| `contradicted` | Clear mismatch with good evidence |
| `partial` | Mixed fit (e.g. escalation short of “invasion”) |
| `ambiguous` | Sources conflict or terms unclear |
| `not_evaluable` | Trend/interpretive without agreed metric |
| `superseded` | Lecture explicitly updates claim in a later video (link `superseded_by`) |

---

## Evidence standard

- Prefer **primary** (official statements, treaties, orders) and **reputable news** with **URLs + access date** in `evidence_urls`.
- Paste **short quotes** in `outcome_notes`; avoid pasting paywalled full text.
- When the lecture uses **hedges** (“possible,” “I think,” “maybe two or six years”), score **generously** on intent: a “possible” window is **not** falsified by quiet alone.

---

## Registry format

**Append-only JSONL:** [registry/predictions.jsonl](registry/predictions.jsonl)

Each line is one object. Required fields:

- `prediction_id` — stable slug (e.g. `jiang-GS01-001`)
- `video_id`, `lecture_ref`, `upload_date` (YYYYMMDD)
- `excerpt` — short verbatim or near-verbatim from transcript
- `claim_summary` — one line for scanning
- `claim_type` — see table above
- `evaluation_window` — optional `{ "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }` or `null`
- `resolution_status`
- `resolved_at_utc` — null until reviewed
- `outcome_notes` — operator narrative + what would change status
- `evidence_urls` — list of strings

Optional: `superseded_by`, `related_prediction_ids`, `accuracy_note` (why partial/ambiguous).

**SQLite query index (generated, not canonical):** from repo root, `python3 scripts/work_jiang/rebuild_registry_db.py` builds [../registry/work_jiang_metrics.sqlite](../registry/README.md) from both JSONL files. Query examples: `python3 scripts/work_jiang/query_predictions.py --status contradicted`. JSONL remains source of truth; edit rows there, then rebuild.

---

## Rhythm

- **Quarterly:** Resolve all `pending` whose `evaluation_window` has ended.
- **After major news** (Middle East, US elections): spot-check **conditional** rows.

---

## Relation to engagement metrics

[Influence tracking](../influence-tracking/README.md) measures **attention** (views/likes). Prediction tracking measures **forecast fit** — orthogonal; spikes in views do not validate claims.

## Relation to pattern tracking

Cross-lecture **mechanisms / scripts** (not single-shot forecasts) live in [`../pattern-tracking/README.md`](../pattern-tracking/README.md). Prediction rows may list `linked_pattern_ids` in a future schema extension; today, patterns carry **`linked_prediction_ids`** back into this registry.

## Relation to divergence tracking

[Divergence tracking](../divergence-tracking/README.md) asks whether a claim **matches how a field usually frames** the same topic. A prediction can be **wrong** and still **mainstream**, or **right** but **heterodox** — use both registries.

## CIV-MEM lens

Classify predictions by **what kind of civilizational object** is at stake (invasion, institution, seam-opening). See [CIV-MEM-LENS.md](../CIV-MEM-LENS.md) §3–4. Optional `civ_mem` object on rows documents **time structure** and **institutions** under review.

---

## Optional prediction-market crosswalk

Some analyses may link structured predictions to **real** markets (e.g. Polymarket) for implied-probability comparison. That step is **optional**, runs **after** extraction, and uses **safeguards** (no forced fit, liquidity + resolution caveats). See **[PREDICTION-MARKETS-INTEGRATION.md](PREDICTION-MARKETS-INTEGRATION.md)**.

---

## Related

- [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md) — transcript + analysis layers  
- [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md) — project purpose  
