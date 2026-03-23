# Audit: Structural and formatting alignment (grace-mar · companion-self · companion-xavier)

**Purpose:** Single place to compare **structure** (paths, repos, forks) and **formatting** (terminology, capitalization, naming) across three surfaces: the **grace-mar** instance, the **companion-self** template, and the **companion-xavier** instance (subtree in grace-mar). **Governed by:** [glossary.md](glossary.md), [canonical-paths.md](canonical-paths.md), [id-taxonomy.md](id-taxonomy.md), [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).

**Scope:** Layout expectations, canonical filenames, hyphenated system names, **SELF-LIBRARY** merge policy, and **Record** boundaries. Not a security or UX audit.

**Status key:** ✅ aligned · ⚠️ partial / drift risk · 🔲 not yet done

**As of:** 2026-03-23

**companion-self baseline:** [`main` @ `288b438`](https://github.com/rbtkhn/companion-self/commit/288b4386684e076df894536624308e69305ae229) — SELF-LIBRARY template governance (see [TEMPLATE-BASELINE](skill-work/work-companion-xavier/TEMPLATE-BASELINE.md), [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT](skill-work/work-companion-xavier/COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md)).

---

## 1. Roles (three surfaces)

| Surface | Repo / path | Role |
|---------|-------------|------|
| **companion-self** | [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self) | **Template** — `users/_template/`, protocol docs, **upstream** for instances. **Always hyphenated** as a **system name** ([glossary.md](glossary.md)). |
| **grace-mar** | This repository; `users/grace-mar/` | **Reference instance** — live Record; operator staging for Xavier (`docs/skill-work/work-companion-xavier/`). |
| **companion-xavier** | **Subtree:** `docs/skill-work/work-companion-xavier/companion-xavier/`; **`users/xavier`** → subtree (symlink at repo root). Optional **export** to a separate remote later. | **Logical instance** — same IFP paths as template; **no** grace-mar Record copy. |

---

## 2. Structural alignment — `users/<id>/`

Canonical paths are **lowercase** ([canonical-paths.md](canonical-paths.md)). **Required** for minimal bot startup: `self.md`, `self-evidence.md`, `recursion-gate.md`.

| Path / concern | grace-mar (`users/grace-mar/`) | companion-self (template) | companion-xavier (`users/xavier/`) |
|----------------|-------------------------------|---------------------------|-------------------------------------|
| `self.md` | ✅ Live Record | `users/_template/` scaffold | ✅ Placeholder — Session 0 MCQ → gate |
| `self-evidence.md` | ✅ | Template scaffold | ✅ Placeholder |
| `recursion-gate.md` | ✅ | Template scaffold | ✅ Placeholder |
| `self-archive.md` | ✅ | Template scaffold | ✅ Placeholder |
| `self-library.md` | ✅ Live LIB rows | ✅ **Governance + empty `entries:`** on `main` ([template file](https://github.com/rbtkhn/companion-self/blob/main/users/_template/self-library.md)) | ✅ **Governance + empty `entries:`** — aligned in **substance** with template; grace-mar **boundary + schema** links; [leakage CI](../scripts/check_companion_xavier_leakage.py) |
| `skills.md` / skill containers | ✅ | Template scaffold | ✅ Placeholder (`skill-think` / `skill-write`) |
| `intent.md` | Optional / instance | Optional | ✅ Placeholder |
| `memory.md` | Optional | Optional | ✅ Placeholder |
| `self-work.md` | ✅ [users/grace-mar/self-work.md](../users/grace-mar/self-work.md) | Planned upstream (`users/_template/`) | ✅ Empty placeholder + [self-work README](skill-work/self-work/README.md) |
| `SELF-LIBRARY/` navigator | ✅ | As template provides | ⚠️ Optional later — not required for seed |
| **Never copy** | — | — | **`users/grace-mar/**` Record** into companion-xavier instance tree |

**Verdict (structure):** **Paths** match canonical naming. **Content:** grace-mar holds a **full** Record and LIB corpus; **companion-self** template **`self-library.md`** is **governance-only** + optional [example corpus](https://github.com/rbtkhn/companion-self/blob/main/docs/self-library-example-corpus-grace-mar-derived.md) in `docs/`; **companion-xavier** matches the **governance + empty shelf** rule and links to grace-mar **docs** for schema/boundary (instance-specific paths).

---

## 3. Formatting alignment — terminology and prose

| Rule | grace-mar | companion-self | companion-xavier |
|------|-----------|----------------|------------------|
| **companion-self** / **companion-xavier** (hyphenated) | [AGENTS.md](../AGENTS.md), [glossary.md](glossary.md) | System/repo name | Named instance (subtree) |
| **companion self** (two words) | Conceptual dyad only | Same | Same |
| **self-*** labels ([id-taxonomy.md](id-taxonomy.md#capitalization-and-format)) | **self-knowledge**, **self-library**, … | Template + docs should match | [TERMS-XAVIER](skill-work/work-companion-xavier/TERMS-XAVIER.md), seed docs |
| **SELF-KNOWLEDGE** / **SELF-LIBRARY** (formal surfaces) | Boundary docs | IFP + template | Same protocol |

**Verdict (formatting):** Rules are **centralized** in glossary + id-taxonomy. **Drift risk:** older or generated files (e.g. `manifest.json` strings) may still say `grace-mar-llm.txt` in non–grace-mar forks — acceptable as **artifact** until per-fork export labels are generalized; **prose** in Xavier territory should stay consistent.

---

## 4. `docs/skill-work` layout

| Area | grace-mar | companion-self | companion-xavier (seed) |
|------|-----------|----------------|-------------------------|
| Full `docs/skill-work/*` | Many territories | Narrower / submodule docs | **Interface + links:** [seed-context README](skill-work/work-companion-xavier/companion-xavier/docs/seed-context/README.md) → monorepo paths; not a full mirror of grace-mar |

**Verdict:** companion-xavier is **intentionally smaller** than grace-mar’s skill-work tree; alignment is **manifest + operator docs**, not file-for-file parity.

---

## 5. SELF-LIBRARY three-way check (2026-03)

| Check | Status |
|-------|--------|
| Template `users/_template/self-library.md` = governance + `entries: []` | ✅ companion-self `main` @ `288b438` |
| Xavier `self-library.md` = no grace-mar LIB rows | ✅ + [check_companion_xavier_leakage.py](../scripts/check_companion_xavier_leakage.py) |
| Wording / policy alignment (boundary, gate, schema pointers) | ✅ Xavier adds grace-mar **docs** links + **template alignment** line to companion-self `main` |
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

## 7. Gaps and follow-ups

1. **companion-self `users/_template` vs grace-mar `users/_template`** — grace-mar’s [users/_template/README.md](../users/_template/README.md) is **documentation-only** (filename table); companion-self has **full** template files. **No defect** — different roles; new instances are created from **companion-self**, not from grace-mar `_template`.
2. **Regenerate** [audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) when you want a fresh path diff (avoid stale `/tmp/companion-self` paths).
3. **Session 0 / gate** — IX content still **empty** until Xavier completes MCQ and approvals; structural alignment does **not** imply Record population.
4. **Optional export** — Subtree → separate git remote not exercised; **document** when pursued.

---

## 8. Summary verdict

| Dimension | grace-mar vs companion-self | companion-xavier |
|-----------|-----------------------------|------------------|
| **Canonical paths** | ✅ Aligned naming; sync via [MERGING-FROM](merging-from-companion-self.md) | ✅ Same path names under `users/xavier/` |
| **SELF-LIBRARY (governance)** | ✅ Template updated on `main` (`288b438`); grace-mar retains **live** LIB rows | ✅ Empty shelf + governance; **aligned** with template **policy** |
| **Terminology** | ✅ Glossary + id-taxonomy | ✅ Wired in interface docs |
| **Record isolation** | N/A | ✅ No grace-mar Record in instance tree; CI leakage check |
| **Upstream** | grace-mar pulls template per merge doc | Scaffold + [TEMPLATE-BASELINE](skill-work/work-companion-xavier/TEMPLATE-BASELINE.md) pins companion-self **commit** |

**Conclusion:** **Structural and formatting alignment** for the three surfaces is **good** as of **2026-03-23**: companion-self **template** carries the **neutral** `self-library` scaffold; **grace-mar** remains the **reference instance** with full Record; **companion-xavier** in-repo matches **path + governance** expectations with **explicit** leakage controls. **Re-audit** after major companion-self template releases or companion-xavier **export** to a standalone repo.
