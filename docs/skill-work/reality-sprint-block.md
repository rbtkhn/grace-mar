# Reality Sprint Block — doctrine

**Purpose:** Reduce drift between analysis and execution. After a substantive plan is written, append a compact **Reality Sprint Block** so the next move is one primary path, one contact with evidence or external feedback, early failure diagnosis, and a pruned step list—not a second full plan.

**Scope:** Operator / **WORK execution layer** ([skills-modularity.md](../skills-modularity.md)). This is **not** Record truth and **not** a gate merge. Staging and companion approval rules are unchanged.

**Not imported:** Startup “hustle,” cold-outreach framing, or revenue-only metaphors. The structural ideas (narrow options, reality-first, prune the plan) are translated into Grace-Mar outcomes below.

---

## Sections (fixed shape)

1. **Primary lane** — One recommended path to execute now.
2. **Fallback lane** — One backup path only if the first is blocked.
3. **First contact with reality** — One action that produces external feedback, concrete evidence, or an observable result **soon** (not after many preparatory steps).
4. **Failure check** — Three yes/no questions that expose what will probably block execution this week.
5. **Cut-in-half version** — Only the steps that most directly advance the target outcome.
6. **Minimum evidence target** — How many comparable trials or artifacts to collect before drawing big conclusions (volume as data).

Use the paste-ready template: [reality-sprint-template.md](reality-sprint-template.md).

---

## Grace-Mar outcome translation (“what counts as direct”)

When pruning or choosing the “money line” from external material, map instead to:

| Outcome type | Examples |
|----------------|----------|
| Governed implementation | Patch, script, CI, integration wired with gate discipline |
| Evidence | Staged candidate, EVIDENCE-ready capture, reproducible receipt |
| Hypothesis test | Single experiment that could falsify the assumption |
| Decision uncertainty | One probe that reduces unknowns for STRATEGY / watches |
| Operator usability | Doc, harness, or dashboard that speeds the next real action |
| PR-shaped artifact | Minimal diff, one schema, one tested path—not a deck |

If a step does not advance one of these, it is a candidate for the cut-in-half pass.

---

## Thresholds: manual vs script

Plans split into two buckets so automation does not spam low-signal briefs.

### 1) Always manual (default)

Use the block when the human asks for a **plan, memo, or recommendation** in work-strategy, work-dev, or brief context, or when the output is clearly a **decision memo** (branches, tradeoffs, commitment level).

- The **assistant fills** the five fields in the chat or doc.
- **Nothing** auto-appends from `scripts/session_brief.py` or other scripts unless the operator opts in later.

**Example — daily brief / exploratory strategy**

- The brief is still **classifying** the week (signal, weak hypotheses, links).
- **Reality Sprint Block** is **optional or shortened** (e.g. only “First contact with reality” + one failure question). No full block required on pure “weather report” briefs.

### 2) Script may append (bounded, later)

Only where there is a **single structured consumer** and clear **active implementation** semantics (e.g. top active lane with GAP, named files, or “next merge” language in [work-dev/workspace.md](work-dev/workspace.md)).

- A script **may** append a **stub** (headings + TBD) or a filled block **only if** inputs pass **narrow gates** (e.g. step count, explicit `--reality-sprint` flag).
- **v1 default:** do not wire automation until manual use proves value; see [Deferred](#deferred-post-v1) below.

---

## Not duplicate of (other rituals)

| Mechanism | Role |
|-----------|------|
| **coffee** menu **A–E**, **Steward** | Session navigation, gate/template/integrity/git tracks; **Implement now vs Later** after steward. |
| **Impact preview** (`scripts/preview_candidate_impact.py`, gate-review app) | Inspects **candidate merge surface** for staged items—tooling, not a full execution wedge. |
| **Strategy menu C — daily brief** then **Tri-Frame** (Barnes / Mearsheimer / Mercouris) | Lens choice after intel; not the same as compressing a finished plan into one action path. |
| **Reality Sprint Block** | Applied **after** there is a substantive plan: **one** primary path, **one** reality step, prune, failure check, evidence cadence. |

Use both where useful: e.g. tri-frame to choose lens, then RSB to commit the week’s executable slice.

---

## Gate first contact

When the wedge is **merge / governance / staged candidates**, “first contact with reality” may be:

- Run **candidate impact preview:** `python3 scripts/preview_candidate_impact.py` (see work-dev tooling).
- Open the **gate-review** dashboard (`apps/gate-review-app.py` pattern in-repo) for the relevant queue.

Cross-link only; no change to merge authority or gate schema.

---

## When not to use (or shorten)

- Pure **archive** or **read-only** synthesis with no execution ask.
- **One-line status** updates.
- **Weather-only** briefs (no commitment to a test this week).
- Default **companion-facing Voice** copy (bot output)—do not treat RSB as default chat prose.

In those cases, skip the block or keep a **single** “first contact” line.

---

## Audience and Voice

- **Default:** operator-facing WORK text; may appear in strategy memos, work-dev proposals, and internal briefs.
- If any fragment might be **quoted to the companion-facing Voice**, apply existing **Lexile** and **humane-purpose** constraints ([prompt-humane-purpose.md](../prompt-humane-purpose.md)); RSB must not become boilerplate the companion is assumed to “execute.”

---

## Wiring into skill-work

This file lives at **`docs/skill-work/`** root as **cross-cutting doctrine** (not a new `work-*` territory). Territories link in via READMEs and templates (e.g. [work-template.md](work-template.md), [work-dev/README.md](work-dev/README.md), [decision-point-template.md](work-strategy/decision-point-template.md)).

**Related:** [context-efficiency-layer.md](context-efficiency-layer.md) — **what to load** at what fidelity (hot/warm/cold, budgets, recovery links). Reality Sprint compresses **one plan** into one action path; CEL assembles **session** context efficiently.

---

## Deferred (post-v1)

Not required for the first merge: bridge/harvest “pending reality contact” line, strategy-notebook promote habit, optional `log_operator_choice` / cadence notes, CI guard on template headings, `skills-portable` / `.cursor/skills` extraction, and automated `session_brief.py` append. Promote after manual RSB use shows reduced “elegant delay.”
