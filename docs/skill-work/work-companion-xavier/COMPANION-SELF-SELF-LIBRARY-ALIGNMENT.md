# companion-self alignment — SELF-LIBRARY template (recommendation 4)

**Purpose:** Make **`users/_template/self-library.md`** in [companion-self](https://github.com/rbtkhn/companion-self) an **instance-agnostic governance package** (boundary + schema + **empty `entries:`**), aligned with:

- Populate companion-xavier seed plan **§1b** / scope table (SELF-LIBRARY governance merged to **template** and **Xavier** seed),
- [boundary-self-knowledge-self-library.md](../../../boundary-self-knowledge-self-library.md) (grace-mar canonical ontology),
- [companion-xavier `self-library.md`](companion-xavier/users/xavier/self-library.md) (already minimal in grace-mar).

This doc lives in **grace-mar** because the **PR is opened on companion-self**; grace-mar tracks the **intent** and **proposed file body** for operators.

---

## Current upstream state (as of 2026-03)

On **`main`**, companion-self’s [`users/_template/self-library.md`](https://github.com/rbtkhn/companion-self/blob/main/users/_template/self-library.md) is a **large** file (LIB rows cloned from grace-mar’s corpus). That is **useful as a reference corpus** but it is **not** a neutral template for **every** new instance: it bakes in grace-mar-specific rows and obscures the **SELF-KNOWLEDGE vs SELF-LIBRARY** boundary for first-time operators.

**Alignment goal:** Template = **governance + empty shelf**; optional **example / mirror** docs can hold dense LIB lists **outside** `users/_template/self-library.md`.

---

## Proposed direction (companion-self PR)

1. **Replace** `users/_template/self-library.md` with a **short** file: rule-of-one-line boundary, pointer to IFP / boundary doc in-repo, **schema** pointer (companion-self may mirror or link [library-schema.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/library-schema.md) from grace-mar or add `docs/library-schema.md` in template).
2. **Move** the existing long YAML / LIB list to something like **`docs/self-library-seed-example.md`** or **`users/_template/self-library.EXAMPLE-corpora.md`** (name TBD in PR) — clearly labeled **optional**, **not** copied into new instances by default.
3. Update **`how-instances-consume-upgrades.md`** (or template README) so new instances know: start **empty**, add LIB rows only via gate.

---

## Proposed `users/_template/self-library.md` body (paste into companion-self PR)

Paths below assume companion-self repo layout (`docs/identity-fork-protocol.md` exists upstream). Adjust links if companion-self uses different filenames.

```markdown
# SELF-LIBRARY — template scaffold

**SELF-LIBRARY** is the **governed reference** layer (lookup-first sources, canon, influence) — **not** SELF-KNOWLEDGE (IX-A). Identity-facing facts stay in `self.md` + gate.

**Rule (one line):** SELF-KNOWLEDGE is identity-facing; SELF-LIBRARY is reference-facing. Do not store civilization-scale reference as IX-A merely because the companion may use it in lookup.

**Protocol:** [docs/identity-fork-protocol.md](../../docs/identity-fork-protocol.md)

**Entries schema:** follow the instance’s library schema (see grace-mar [`docs/library-schema.md`](https://github.com/rbtkhn/grace-mar/blob/main/docs/library-schema.md) if not yet mirrored in this repo).

**Template default:** no prefilled LIB rows — add rows through the normal gated pipeline when the companion approves.

---

## Entries

```yaml
entries: []
```

---

## Optional

If this template ships an **example corpus** for operators (e.g. public-domain story index), keep it in **`docs/…`** or a clearly named **EXAMPLE** file — **not** as the default `entries:` block for new forks.
```

---

## PR checklist (operator)

| Step | Action |
|------|--------|
| 1 | Clone companion-self: `git clone https://github.com/rbtkhn/companion-self.git` (or open existing `companion-self/` root from [MERGING-FROM-COMPANION-SELF](../../../merging-from-companion-self.md) §0). |
| 2 | Branch: e.g. `template-self-library-governance`. |
| 3 | Apply proposed body above; relocate legacy LIB bulk per **Proposed direction**. |
| 4 | Open PR on **rbtkhn/companion-self**; description: link this file + [boundary-self-knowledge-self-library.md](../../../boundary-self-knowledge-self-library.md) (grace-mar). |
| 5 | After merge, note **commit SHA** in [TEMPLATE-BASELINE.md](TEMPLATE-BASELINE.md) and [MERGING-FROM-COMPANION-SELF §3](../../../merging-from-companion-self.md) sync log. |
| 6 | Re-diff **grace-mar** `docs/skill-work/work-companion-xavier/companion-xavier/users/xavier/self-library.md` — should stay **wording-aligned** with template (no grace-mar LIB rows). |

---

## Relation to Xavier (grace-mar)

No change required to **Xavier’s** `self-library.md` for this alignment doc unless the **template** wording improves; then copy the **same** governance paragraph into the subtree for parity.
