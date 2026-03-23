# Audit: Structural and formatting alignment (grace-mar · companion-self · companion-xavier)

**Purpose:** Single place to compare **structure** (paths, repos, forks) and **formatting** (terminology, capitalization, naming) across three surfaces: the **grace-mar** instance, the **companion-self** template, and the planned **companion-xavier** instance. **Governed by:** [glossary.md](glossary.md), [canonical-paths.md](canonical-paths.md), [id-taxonomy.md](id-taxonomy.md), [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).

**Scope:** Layout expectations, canonical filenames, hyphenated system names, **SELF-LIBRARY** merge policy, and **Record** boundaries. Not a security or UX audit.

**Status key:** ✅ aligned · ⚠️ partial / drift risk · 🔲 not yet populated · **Scaffold present** — `docs/skill-work/work-companion-xavier/companion-xavier/` (Session 0 MCQ + gate still required for real IX content; optional separate remote later)

**Date:** March 2026

---

## 1. Roles (three surfaces)

| Surface | Repo / path | Role |
|---------|-------------|------|
| **companion-self** | [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self) | **Template** — `users/_template/`, protocol docs, **upstream** for instances. **Always hyphenated** as a **system name** ([glossary.md](glossary.md)). |
| **grace-mar** | This repository; `users/grace-mar/` | **Reference instance** — live Record, operator staging for Xavier seed (`docs/skill-work/work-companion-xavier/` when present), proves the stack. |
| **companion-xavier** | **Subtree in grace-mar:** `docs/skill-work/work-companion-xavier/companion-xavier/`; optional **export** to a separate remote later | **Logical instance** — `users/xavier/` under that subtree (and/or **symlink** `users/xavier` at repo root for tooling — see populate plan **Layout decision**). **Always hyphenated** as a **system name**. |

---

## 2. Structural alignment — `users/<id>/`

Canonical paths are **lowercase** ([canonical-paths.md](canonical-paths.md)). **Required** for minimal bot startup: `self.md`, `self-evidence.md`, `recursion-gate.md`.

| Path / concern | grace-mar (`users/grace-mar/`) | companion-self (template) | companion-xavier (`users/xavier/`) — scaffold (2026-03) |
|----------------|-------------------------------|---------------------------|---------------------------------------------|
| `self.md` | ✅ Live Record | `users/_template/` scaffold | ✅ **Placeholder shell** until Session 0 MCQ → gate (populate plan §2) |
| `self-evidence.md` | ✅ | Template scaffold | ✅ Placeholder |
| `recursion-gate.md` | ✅ | Template scaffold | ✅ Placeholder |
| `self-archive.md` | ✅ | Template scaffold | ✅ Placeholder |
| `self-library.md` | ✅ Live LIB rows | **`users/_template/self-library.md`** — governance merge target (§1b) | ✅ **Governance + empty `entries:`** — **no** grace-mar LIB rows |
| `skills.md` / skill containers | ✅ | Template scaffold | ✅ Placeholder |
| `intent.md` | Optional / instance | Optional | ✅ Placeholder — not operator-prefilled from grace-mar |
| `memory.md` | Optional | Optional | 🔲 Optional placeholder |
| `self-work.md` | Planned / grace-mar | Planned template | 🔲 **Empty** placeholder + `docs/skill-work/self-work/README.md` spec (self-work coordination plan) |
| `SELF-LIBRARY/` navigator | ✅ | As template provides | 🔲 As seeded |
| **Never copy** | — | — | **`users/grace-mar/**` Record** into companion-xavier |

**Verdict (structure):** grace-mar and companion-self follow the same **canonical naming**; companion-xavier is **specified** to mirror **paths** without mirroring **grace-mar content**, except **`self-library.md`** receiving the **same instance-agnostic governance package** as **companion-self** §1b.

---

## 3. Formatting alignment — terminology and prose

| Rule | grace-mar | companion-self | companion-xavier |
|------|-----------|----------------|------------------|
| **companion-self** / **companion-xavier** (hyphenated) | Documented in [AGENTS.md](../AGENTS.md), [glossary.md](glossary.md) | **System/repo name** | **companion-xavier** = named instance (subtree or exported repo) |
| **companion self** (two words) | **Conceptual** dyad only | Same distinction | Same |
| **self-*** standard labels ([id-taxonomy.md](id-taxonomy.md#capitalization-and-format)) | **self-knowledge**, **self-library**, … | Template should match | Same |
| **SELF-KNOWLEDGE** / **SELF-LIBRARY** (formal surfaces) | Glossary + boundary docs | Same protocol | Same |

**Verdict (formatting):** Rules are **centralized** in glossary + id-taxonomy; all three surfaces should **cite** the same conventions. **Drift risk:** older docs may still mix spelling; refresh when touching files.

---

## 4. docs / skill-work layout

| Area | grace-mar | companion-self | companion-xavier (seed) |
|------|-----------|----------------|-------------------------|
| Full `docs/skill-work/*` | Many territories (instance + operator) | Narrower template doc set | **Subset only** per populate plan scope — work-politics (curated), work-companion-xavier, work-dev subset, work-business, self-work README, SELF-LIBRARY governance |
| Protocol mirrors (IFP, architecture) | ✅ Elaborated | ✅ or path equivalents | 🔲 Mirror approved manifest |

**Verdict:** companion-xavier is **intentionally smaller** than grace-mar’s skill-work tree; alignment is **manifest-driven**, not file-for-file parity with grace-mar.

---

## 5. Prior audits (do not duplicate)

| Document | What it covers |
|----------|----------------|
| [audit-grace-mar-vs-companion-self-template.md](audit-grace-mar-vs-companion-self-template.md) | Instance vs **template** — structure, protocol, **partial** path/manifest drift |
| [skill-work/work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) | Path-level diff snapshot (may be stale; regenerate from live template) |
| [AUDIT-COMPANION-SELF.md](AUDIT-COMPANION-SELF.md) | Companion-self **concept** vs grace-mar docs |
| [merging-from-companion-self.md](merging-from-companion-self.md) | Safe sync surfaces; **never** overwrite `users/grace-mar/` |

This three-way audit **adds** explicit **companion-xavier** expectations and ties **SELF-LIBRARY** to **both** template and instance seeds.

---

## 6. Gaps and recommended actions

1. **companion-xavier subtree not populated yet** — All 🔲 rows become checklists when `companion-xavier/` exists under **work-companion-xavier**; re-run after scaffold + optional symlink for `users/xavier`.
2. **Template manifest baseline** — grace-mar still benefits from a **recorded** companion-self commit/tag in sync docs ([audit-grace-mar-vs-companion-self-template.md](audit-grace-mar-vs-companion-self-template.md) §7).
3. **Regenerate** [audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) against a **current** `companion-self` clone (paths in that file may point at `/tmp/companion-self`).
4. **SELF-LIBRARY** — When §1b executes, confirm **`users/_template/self-library.md`** (companion-self) and **`.../companion-xavier/users/xavier/self-library.md`** (grace-mar subtree) **match** the governance slice (or document deltas).

---

## 7. Summary

| Dimension | grace-mar vs companion-self | companion-xavier (planned) |
|-----------|-----------------------------|----------------------------|
| **Canonical paths** | ✅ Aligned; template path list partially divergent | 🔲 Same paths; **only self-library.md** merged with governance |
| **Terminology** | ✅ Glossary + id-taxonomy locked | Same rules |
| **Record isolation** | N/A | ✅ No `users/grace-mar/` in seed |
| **Upstream** | Pulls template per merge doc | Subtree scaffold from template + manifest; optional export |

**Conclusion:** **Structural** alignment is **defined** by canonical paths and the populate plan; **formatting** alignment is **defined** by glossary and id-taxonomy. **companion-self** remains **upstream**; **grace-mar** holds **both** the operator Record and the **companion-xavier** subtree; **companion-xavier** stays **lean** until MCQ and gate populate the Record. Refresh after the **`companion-xavier/`** subtree is scaffolded and after **major** template upgrades.
