# Knot template — strategy-notebook (WORK only; not Record)

**Use:** Copy to `chapters/YYYY-MM/knots/knot-YYYY-MM-DD-<knot_label>.md`, replace placeholders, append a row to [`knot-index.yaml`](knot-index.yaml), run `python3 scripts/validate_knot_index.py` from repo root.

**Naming:** Basename must contain **`knot`**. The segment after the date is the **machine slug** (see **`knot_label`** below).

**Relation to `days.md`:** The block **`## YYYY-MM-DD`** in [`chapters/YYYY-MM/days.md`](chapters/YYYY-MM/days.md) is usually the **rolling synthesis**. A knot is an optional **sidecar**; it does **not** replace the day block unless you adopt that policy.

---

### What **`knot_label`** is (and what it is not)

- **Weaving** is what you **do** (fold inbox → Signal/Judgment, tighten Judgment, promote links — the **action**).
- A **knot** is one **saved artifact** from that work — a **named wave** or **bundle** you chose to **freeze**, **abstract**, or **use as a link hub**.
- **`knot_label`** is **not** the verb “weave.” It is the **stable id for this knot file** — a **short kebab-case slug** used to:
  - **Disambiguate** when **several knots share the same calendar day** (e.g. `parsi-davis` vs `sanchez-xi` on `2026-04-14`);
  - **Match** the filename: `knot-2026-04-14-parsi-davis.md` ↔ `knot_label: parsi-davis`;
  - **Join** rows in [`knot-index.yaml`](knot-index.yaml) to paths on disk (sorts, tooling, validators).

So: **you are labeling the knot** (the file / indexed row), not re-labeling the abstract idea of “weaving.” If there is only **one** knot that day, you still use a sensible slug (`morning`, `islamabad`, `daily-fold`, …) so the basename and index stay readable.

**Human title** vs **machine id:** The heading below can use a **long plain-language title**; **`knot_label`** stays **short** and **kebab-case** for file + YAML.

---

## Knot — YYYY-MM-DD — &lt;human-readable title&gt;

| Field | Value |
|--------|--------|
| **Date** | YYYY-MM-DD |
| **knot_label** (machine slug) | `<kebab-slug>` — must match `knot-YYYY-MM-DD-<kebab-slug>.md` and [`knot-index.yaml`](knot-index.yaml) |
| **Day block** | [`days.md` § YYYY-MM-DD](chapters/YYYY-MM/days.md) |

### Role (**pick per knot** — mixed modes allowed)

- [ ] **Snapshot** — freeze emphasis / wording from a weave pass  
- [ ] **Abstract** — short thesis; long prose stays in `days.md`  
- [ ] **Link hub** — almost only pointers (inbox, primaries, `batch-analysis`)  

*(You can combine, e.g. Abstract Judgment + Link hub for Links.)*

### Lineage

- **Inbox:** [`daily-strategy-inbox.md`](daily-strategy-inbox.md) — paste-ready lines / `batch-analysis | … |` rows this knot reflects  
- **Expert threads:** optional `thread:<expert_id>` if this knot is expert-centric; omit otherwise  

### Signal

*(**Optional prose** — or one line: “See [`days.md`](chapters/YYYY-MM/days.md) § Signal for YYYY-MM-DD.” Leave blank only if the pointer is enough.)*

### Judgment

*(**Optional prose** — or: “See `days.md` § Judgment.”)*

### Links

*(**Optional** — primaries / wires / PH / expert corpus paths.)*

### Open / verify

*(**Optional** — pins, `verify:` tails, next-session tests.)*

---

### Index row (YAML — paste into `knots:` in `knot-index.yaml`)

Keeping this block **in the knot file** is the default so the path and `knot_label` stay copy-paste aligned. If you prefer a **single** YAML source of truth, maintain rows **only** in [`knot-index.yaml`](knot-index.yaml) and **delete** this block from the knot.

```yaml
  - path: docs/skill-work/work-strategy/strategy-notebook/chapters/YYYY-MM/knots/knot-YYYY-MM-DD-<knot_label>.md
    date: "YYYY-MM-DD"
    knot_label: <knot_label>
```

Optional keys (omit if unused): `clusters` (list of strings), `patterns` (list of strings), `note` (string).

**Schema note:** `knot-index.yaml` **`knot_label`** replaces the former field **`weave_label`** (same meaning, clearer name).
