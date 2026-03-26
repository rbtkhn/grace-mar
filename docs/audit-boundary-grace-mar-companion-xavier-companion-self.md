# Audit: Boundaries — grace-mar · companion-self · companion-xavier

**Purpose:** State the **proper** boundaries between three surfaces — what **must** stay separate, what **may** cross under contract, and **how** enforcement works. Complements [audit-structural-alignment-grace-mar-companion-self-companion-xavier.md](audit-structural-alignment-grace-mar-companion-self-companion-xavier.md) (paths and formatting). **Governed by:** [AGENTS.md](../AGENTS.md), [identity-fork-protocol.md](identity-fork-protocol.md), [fork-isolation-and-multi-tenant.md](fork-isolation-and-multi-tenant.md), [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).

**As of:** 2026-03-23

---

## 1. The three surfaces (what they *are*)

| Surface | What it is | Holds a live companion Record? |
|---------|------------|--------------------------------|
| **grace-mar** | This **repository** — reference **instance** `users/grace-mar/`, full stack, operator tooling | **Yes** — Grace-Mar’s fork |
| **companion-self** | **Upstream template** repo — `users/_template/`, protocol docs, reusable scaffolds | **No** — no `users/<real-id>/` Record; template only |
| **companion-xavier** | **Logical instance** — `users/xavier/` (subtree + symlink), same IFP as any instance | **Yes** — Xavier’s fork (empty until Session 0 + gate) |

**Boundary mistake to avoid:** Treating **companion-self** as “another fork” like grace-mar or Xavier. It is **blueprint**, not identity.

---

## 2. Boundary matrix (normative)

| Boundary | grace-mar | companion-self | companion-xavier |
|----------|-----------|----------------|------------------|
| **Fork namespace** | `users/grace-mar/` only | `users/_template/` only (scaffold, not a person) | `users/xavier/` only |
| **Cross-fork Record copy** | — | — | **Forbidden:** no `users/grace-mar/**` content in Xavier tree ([LEAKAGE-CHECKLIST](skill-work/work-xavier/LEAKAGE-CHECKLIST.md), [check script](../scripts/check_companion_xavier_leakage.py)) |
| **Template → instance** | Merges via [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md); **never** overwrite live Record wholesale | Source of **structure** and **protocol** | Scaffold from **template baseline**, not from grace-mar Record ([ALIGNMENT](skill-work/work-xavier/ALIGNMENT.md)) |
| **Instance → template** | Structural / instance-agnostic improvements may **propose** upstream PRs | Accepts PRs; remains **generic** | Does **not** push Xavier Record into template |
| **SELF-KNOWLEDGE vs SELF-LIBRARY** | IX vs `self-library.md` rows — [boundary doc](boundary-self-knowledge-self-library.md) | Template teaches the same rule | Seed: **governance + empty `entries:`**; no grace-mar LIB ids |
| **WORK vs Record** | `docs/skill-work/work-*`, `users/*/self-work.md` coordination — not IX | N/A (docs) | Client/job docs **linked**, not merged into `self.md` without gate |
| **Gated merge** | `process_approved_candidates.py` — companion approves | N/A | Same **five-file** protocol for Xavier |
| **Workspace (multi-root)** | Instance edits live **here**; template read-only when diffing ([MERGING-FROM §0](merging-from-companion-self.md)) | Template edits in **companion-self** repo; do not edit grace-mar from template workspace as if it were writable | Xavier subtree edited **in grace-mar** monorepo |

---

## 3. What **may** cross (allowed flows)

| Flow | Rule |
|------|------|
| **Protocol & docs** | IFP, glossary, architecture concepts — sync **companion-self → grace-mar** per merge doc; **companion-xavier** mirrors **approved** manifest paths only. |
| **SELF-LIBRARY governance** | Same **instance-agnostic** `self-library.md` **shape** (governance + empty `entries:`) on template **and** Xavier seed — **not** grace-mar’s LIB row corpus. |
| **Scripts / exports** | `GRACE_MAR_USER_ID=xavier` resolves `users/xavier/`; exports are **per-fork** ([fork isolation](fork-isolation-and-multi-tenant.md)). |
| **Operator staging** | `docs/skill-work/work-xavier/` holds **contracts** (manifest, leakage) — **not** Xavier’s Record body. |

---

## 4. What **must not** cross (hard lines)

| Prohibited | Why |
|------------|-----|
| **Grace-Mar Record facts** into `users/xavier/` without pipeline | Sovereign merge rule; breaks fork isolation and auditability. |
| **Template treated as Record** | No approvals or IX in companion-self `users/_template/` as if it were a companion. |
| **Xavier client WORK** pasted into **her** `self.md` as identity without gate | WORK ≠ SELF-KNOWLEDGE until staged and approved. |
| **LLM / training knowledge** into profile without pipeline | [AGENTS.md](../AGENTS.md) knowledge boundary. |

---

## 5. companion-xavier **inside** grace-mar (monorepo boundary)

The **work-xavier** folder is a **membrane**:

- **Toward grace-mar:** Does not hold `users/grace-mar/` data.
- **Toward companion-xavier subtree:** Only **manifest-approved** material; [SEED-MANIFEST](skill-work/work-xavier/SEED-MANIFEST.md).

So: **one repo**, **two fork namespaces** (`grace-mar`, `xavier`) — **no** shared writable Record between them ([fork isolation §1](fork-isolation-and-multi-tenant.md)).

---

## 6. Audit checklist (operator)

- [ ] **Namespaces:** `users/grace-mar/` and `users/xavier/` are disjoint; symlink `users/xavier` resolves only to Xavier subtree.
- [ ] **Leakage:** [check_companion_xavier_leakage.py](../scripts/check_companion_xavier_leakage.py) passes; spot-check no `grace-mar` identity in Xavier files.
- [ ] **Template pin:** [TEMPLATE-BASELINE](skill-work/work-xavier/TEMPLATE-BASELINE.md) reflects **companion-self `main`** commit used for scaffold alignment.
- [ ] **Gate:** No hand-merge into Xavier `self.md`; Session 0 → candidates → approve → script.
- [ ] **WORK vs Record:** [LANES](skill-work/work-xavier/LANES.md) understood for client vs identity.

---

## 7. Verdict

**Proper boundaries are well-defined** in repo policy: **fork isolation** (namespace per companion), **template upstream** (companion-self without live Record), **monorepo membrane** (work-xavier + leakage checks), and **IFP** (stage → approve → merge). **Drift risk** is operational: copying prose, rushing Session 0 merges, or conflating **work-politics** client copy with **Xavier** — countered by **LEAKAGE-CHECKLIST**, **LANES**, and **gated pipeline**.

**Related:** [audit-structural-alignment-grace-mar-companion-self-companion-xavier.md](audit-structural-alignment-grace-mar-companion-self-companion-xavier.md) · [audit-companion-self.md](audit-companion-self.md) · [conceptual-framework.md](conceptual-framework.md) (Record vs fork, tricameral mind).
