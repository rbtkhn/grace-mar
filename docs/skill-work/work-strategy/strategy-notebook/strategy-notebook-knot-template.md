# Knot template — strategy-notebook (WORK only; not Record)

**Use:** Copy to `chapters/YYYY-MM/knots/strategy-notebook-knot-YYYY-MM-DD-<knot_label>.md`, replace placeholders, append a row to [`knot-index.yaml`](knot-index.yaml), run `python3 scripts/validate_knot_index.py` from repo root.

**Weave length target:** **300–1000 words** for the knot file body (`wc -w`). If synthesis would exceed **~1000**, move bulk to [`days.md`](chapters/YYYY-MM/days.md) **or** split into another knot—see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave choice and section weighting* (knot body length). Thin router knots **below 300** are allowed only when **deferring** narrative to `days.md` (architecture).

**Naming:** Basename must contain **`knot`**. The segment after the date is the **machine slug** (see **`knot_label`** below).

**Relation to `days.md`:** A knot is the **atomic strategy-notebook page** — the primary unit of notebook substance. The block **`## YYYY-MM-DD`** in [`chapters/YYYY-MM/days.md`](chapters/YYYY-MM/days.md) is the **chronology and continuity layer**: it tracks which knots were active, what changed, what tensions remained open, and what should be resumed tomorrow. `days.md` organizes time; knots hold the writing.

---

### What **`knot_label`** is (and what it is not)

- **Weaving** is what you **do**: fold inbox material, expert-thread pressure, historical resonance, and judgment into a page.
- A **knot** is one **atomic notebook page** — a **named, enduring unit** of strategic writing (thesis, synthesis, case, mechanism, watch, or link hub).
- **`knot_label`** is **not** the verb "weave." It is the **stable id for this knot file** — a **short kebab-case slug** used to:
  - **Disambiguate** when **several knots share the same calendar day** (e.g. `parsi-davis` vs `sanchez-xi` on `2026-04-14`);
  - **Match** the filename: `strategy-notebook-knot-2026-04-14-parsi-davis.md` ↔ `knot_label: parsi-davis`;
  - **Join** rows in [`knot-index.yaml`](knot-index.yaml) to paths on disk (sorts, tooling, validators).

So: **you are labeling the knot** (the file / indexed row), not re-labeling the abstract idea of "weaving." If there is only **one** knot that day, you still use a sensible slug (`morning`, `islamabad`, `daily-weave`, …) so the basename and index stay readable.

**Human title** vs **machine id:** The heading below can use a **long plain-language title**; **`knot_label`** stays **short** and **kebab-case** for file + YAML.

---

## Knot — YYYY-MM-DD — &lt;human-readable title&gt;

| Field | Value |
|--------|--------|
| **Date** | YYYY-MM-DD |
| **knot_label** (machine slug) | `<kebab-slug>` — must match `strategy-notebook-knot-YYYY-MM-DD-<kebab-slug>.md` and [`knot-index.yaml`](knot-index.yaml) |
| **Day block** | [`days.md` § YYYY-MM-DD](chapters/YYYY-MM/days.md) |
| **Primary expert (`thread:`) — optional** | If this knot was woven with one **primary** expert, record **`thread:<expert_id>`** (same id as [`strategy-commentator-threads.md`](strategy-commentator-threads.md)); default **Signal / Judgment / Links / Open** weighting follows [NOTEBOOK-PREFERENCES § Weave skeletons (S1–S5)](NOTEBOOK-PREFERENCES.md#weave-skeletons-s1-s5). **Omit** for link-only hubs or when no single spine applies — multi-expert synthesis still belongs in the sections below. |

### Page type (**pick per knot** — mixed types allowed)

- [ ] **Thesis page** — a strategic claim with warrant and falsifier; the core judgment unit
- [ ] **Synthesis page** — integrates multiple expert lanes or source threads into a composite picture
- [ ] **Case page** — a comparative or contrastive study (two lanes, two episodes, two hypotheses)
- [ ] **Mechanism page** — a causal or structural pattern extracted from evidence (how X works)
- [ ] **Watch page** — a live monitoring surface for an evolving situation or thread
- [ ] **Link hub** — primarily pointers (inbox, primaries, `batch-analysis`, sister knots)

*(You can combine, e.g. Thesis page + Link hub.)*

### Verify-before-depth (optional — reduces digest-driven drift)

Tick when satisfied **before** treating synthesis depth as load-bearing. **Not** a vanity score; skip on pure link hubs if N/A.

**Quality of information (QoI) — three checks**

- [ ] **Sources:** Primaries or verify-tagged wires named for load-bearing claims (not only commentary).
- [ ] **Register:** Expert / institutional / wire lanes are **not** merged without naming the seam.
- [ ] **Time:** Claims are **dated** or explicitly **timeless** mechanism language — no stale “today” without a date.

**Key assumptions (KAC) — three checks**

- [ ] **Falsifier:** At least one **observable** pin, watch, or `Open` line could weaken the Judgment.
- [ ] **Scope:** Geographic / legal / alliance scope matches the evidence (no silent scope creep).
- [ ] **Independence:** Correlated sources are **not** counted as independent confirmation.

When using [`knot-index.yaml`](knot-index.yaml) **v4+**, you may set optional **`qoi_check`** / **`kac_check`** on the index row to mirror these (manual).

### Lineage

- **Inbox:** [`daily-strategy-inbox.md`](daily-strategy-inbox.md) — paste-ready lines / `batch-analysis | … |` rows this knot reflects
- **Expert threads:** optional `thread:<expert_id>` if this knot is expert-centric; omit otherwise
- **History resonance:** optional — chapter id(s) from [history-notebook](../../history-notebook/README.md) (e.g. `hn-i-v1-04`) + mechanism line when this knot leans on durable pattern language; **none** or **deferred** if no HN wire applies
- **Civilizational bridge:** optional — [civilizational-strategy-surface.md](../../civilizational-strategy-surface.md) case family or lens id when CIV-MEM material grounded this page; omit if none

### Signal
<page-level signal>

### Judgment
<page-level thesis / synthesis>

### Links
<primaries / wires / PH / expert corpus / related knots>

### Open / verify
<pins, tests, unresolved tensions, next-session checks>

---

### Index row (YAML — paste into `knots:` in `knot-index.yaml`)

Keeping this block **in the knot file** is the default so the path and `knot_label` stay copy-paste aligned. If you prefer a **single** YAML source of truth, maintain rows **only** in [`knot-index.yaml`](knot-index.yaml) and **delete** this block from the knot.

```yaml
  - path: docs/skill-work/work-strategy/strategy-notebook/chapters/YYYY-MM/knots/strategy-notebook-knot-YYYY-MM-DD-<knot_label>.md
    date: "YYYY-MM-DD"
    knot_label: <knot_label>
```

Optional keys (omit if unused): `clusters` (list of strings), `patterns` (list of strings), `note` (string); **v4+** also `weave_count` (int), `seam_integrity` (0–1), `qoi_check` / `kac_check` (booleans). See [gamification-metrics.md](gamification-metrics.md).

**Schema note:** `knot-index.yaml` **`knot_label`** replaces the former field **`weave_label`** (same meaning, clearer name).
