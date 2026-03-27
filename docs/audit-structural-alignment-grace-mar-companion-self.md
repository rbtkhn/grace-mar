# Audit: Structural and formatting alignment (grace-mar · companion-self)

**Purpose:** Compare **structure** (paths, repos) and **formatting** (terminology, capitalization, naming) across the **grace-mar** instance and the **companion-self** template. **Normative boundaries:** [audit-boundary-grace-mar-companion-self.md](audit-boundary-grace-mar-companion-self.md). **Governed by:** [glossary.md](glossary.md), [canonical-paths.md](canonical-paths.md), [id-taxonomy.md](id-taxonomy.md), [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).

**Scope:** Layout expectations, canonical filenames, hyphenated system names, **SELF-LIBRARY** merge policy, and **Record** boundaries. Not a security or UX audit.

**Status key:** ✅ aligned · ⚠️ partial / drift risk · 🔲 not yet done

**As of:** 2026-03-27 (updated: additional instances are **not** hosted in this repo).

**companion-self baseline:** [`main` @ `288b438`](https://github.com/rbtkhn/companion-self/commit/288b4386684e076df894536624308e69305ae229) — SELF-LIBRARY template governance (see [TEMPLATE-BASELINE](skill-work/work-companion-self/TEMPLATE-BASELINE.md), [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT](skill-work/work-companion-self/COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md)).

---

## 1. Roles (two surfaces in this repo)

| Surface | Repo / path | Role |
|---------|-------------|------|
| **companion-self** | [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self) | **Template** — `users/_template/`, protocol docs, **upstream** for instances. **Always hyphenated** as a **system name** ([glossary.md](glossary.md)). |
| **grace-mar** | This repository; `users/grace-mar/` | **Reference instance** — live Record; operator tooling under `docs/skill-work/`. |

**Other instances** (e.g. a companion who bootstraps from the template in **their own** repository) are **not** mirrored here; alignment is **concept + protocol**, not co-location in the grace-mar repo.

---

## 2. Structural alignment — `users/<id>/`

Canonical paths are **lowercase** ([canonical-paths.md](canonical-paths.md)). **Required** for minimal bot startup: `self.md`, `self-evidence.md`, `recursion-gate.md`.

| Path / concern | grace-mar (`users/grace-mar/`) | companion-self (template) |
|----------------|-------------------------------|---------------------------|
| `self.md` | ✅ Live Record | `users/_template/` scaffold |
| `self-evidence.md` | ✅ | Template scaffold |
| `recursion-gate.md` | ✅ | Template scaffold |
| `self-archive.md` | ✅ | Template scaffold |
| `self-library.md` | ✅ Live LIB rows | ✅ **Governance + empty `entries:`** on `main` ([template file](https://github.com/rbtkhn/companion-self/blob/main/users/_template/self-library.md)) |
| `skills.md` / skill containers | ✅ | Template scaffold |
| `self-work.md` | ✅ [users/grace-mar/self-work.md](../users/grace-mar/self-work.md) | Planned upstream (`users/_template/`) |

**Verdict (structure):** **Paths** match canonical naming. **Content:** grace-mar holds a **full** Record and LIB corpus; **companion-self** template **`self-library.md`** is **governance-only** + optional [example corpus](https://github.com/rbtkhn/companion-self/blob/main/docs/self-library-example-corpus-grace-mar-derived.md) in `docs/`.

---

## 3. Formatting alignment — terminology and prose

| Rule | grace-mar | companion-self |
|------|-----------|----------------|
| **companion-self** (hyphenated) | [AGENTS.md](../AGENTS.md), [glossary.md](glossary.md) | System/repo name |
| **companion self** (two words) | Conceptual dyad only | Same |
| **self-*** labels ([id-taxonomy.md](id-taxonomy.md#capitalization-and-format)) | **self-knowledge**, **self-library**, … | Template + docs should match |
| **SELF-KNOWLEDGE** / **SELF-LIBRARY** (formal surfaces) | Boundary docs | IFP + template |

**Verdict (formatting):** Rules are **centralized** in glossary + id-taxonomy.

---

## 4. `docs/skill-work` layout

| Area | grace-mar | companion-self |
|------|-----------|----------------|
| Full `docs/skill-work/*` | Many territories | Narrower / submodule docs |

**Verdict:** Alignment is **manifest + operator docs**, not file-for-file parity with the template.

---

## 5. SELF-LIBRARY check

| Check | Status |
|-------|--------|
| Template `users/_template/self-library.md` = governance + `entries: []` | ✅ companion-self `main` @ `288b438` |
| grace-mar `self-library.md` = live LIB rows + boundary docs | ✅ |
| Optional example corpus only in template `docs/` | ✅ [self-library-example-corpus-grace-mar-derived.md](https://github.com/rbtkhn/companion-self/blob/main/docs/self-library-example-corpus-grace-mar-derived.md) on companion-self |

---

## 6. Prior audits (do not duplicate)

| Document | What it covers |
|----------|----------------|
| [audit-grace-mar-vs-companion-self-template.md](audit-grace-mar-vs-companion-self-template.md) | Instance vs **template** — structure, protocol, drift |
| [skill-work/work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) | Path-level diff snapshot — **regenerate** from a current clone when doing a full template sync |
| [AUDIT-COMPANION-SELF.md](AUDIT-COMPANION-SELF.md) | Companion-self **concept** vs grace-mar docs |
| [merging-from-companion-self.md](merging-from-companion-self.md) | Safe sync surfaces; **never** overwrite `users/grace-mar/` |

---

## 7. Summary verdict

| Dimension | Result |
|-----------|--------|
| **Canonical paths** | ✅ Aligned naming; sync via [MERGING-FROM](merging-from-companion-self.md) |
| **SELF-LIBRARY (governance)** | ✅ Template updated on `main` (`288b438`); grace-mar retains **live** LIB rows |
| **Terminology** | ✅ Glossary + id-taxonomy |
| **Upstream** | grace-mar pulls template per merge doc; [TEMPLATE-BASELINE](skill-work/work-companion-self/TEMPLATE-BASELINE.md) pins companion-self **commit** for governance merges |

**Re-audit** after major companion-self template releases.
