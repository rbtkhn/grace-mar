# work-cici Post-Rename Audit

## Status

- **Active lane name:** Cici (`work-cici`)
- **Legacy lane name:** work-xavier
- **Date audited:** 2026-04-24
- **Auditor:** Repository audit (assisted review)

## Active contract check

Active top-level hub and lane entrypoints describe **Cici** as the current lane identity, with **Xavier** reserved for legacy filenames, GitHub handle **@Xavier-x01**, template paths (`users/xavier/`), or explicit rename history.

| File | Result |
|------|--------|
| [docs/skill-work/README.md](../README.md) | **Pass** — work-cici row: “Cici, formerly Xavier”; not Cici’s Record repo. |
| [README.md](README.md) | **Pass** — Purpose, Rename note, Naming, legacy table, Cici-first body. |
| [INDEX.md](INDEX.md) | **Pass** (after audit) — README row Cici-first; two table cells updated (SYNC-DAILY, rubric); row for [POST-RENAME-AUDIT.md](POST-RENAME-AUDIT.md) added. |
| [LANES.md](LANES.md) | **Pass** (after audit) — H1 and lead now Cici; template Record path `users/xavier/` called out as instance template, not lane name. |

## Legacy reference classification

| Reference | Location | Classification | Action |
|-----------|----------|----------------|--------|
| `work-xavier` in rename blurb | [INDEX.md](INDEX.md) | historical / continuity | no action |
| `xavier-*.md`, `TERMS-XAVIER.md`, `COMPANION-XAVIER-*` | lane root + legacy table | historical filename | no action |
| [scripts/build_xavier_handbook_bundle.py](../../scripts/build_xavier_handbook_bundle.py), [scripts/generate_smm_xavier_pdf.sh](../../scripts/generate_smm_xavier_pdf.sh) | `scripts/` | script compatibility name | document in this file; no rename in this PR |
| `smm-xavier-*` bundle paths | work-politics outputs | script compatibility / stable paths | no action |
| “Advisor / **Xavier** daily sync” (was) | [INDEX.md](INDEX.md) `SYNC-DAILY` row | active prose drift | **fixed** → Cici |
| “evaluate **Xavier** vs the content plans” (was) | [INDEX.md](INDEX.md) rubric row | active prose drift | **fixed** → Cici |
| “WORK vs Record (**Xavier**)” (was) | [LANES.md](LANES.md) H1 | active title drift | **fixed** → Cici + template path note |
| `users/grace-mar/**` in boundary / leakage rules | [README.md](README.md), [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md), etc. | boundary / policy cite (not “copy in”) | no action — paths appear only as **do not copy** or cross-lane policy |
| `Xavier’s instance layer` (OB1 framing) | [ALIGNMENT.md](ALIGNMENT.md) | person + product (GitHub **Cici** = Xavier’s public instance) | keep wording; optional future edit to “Cici’s instance layer (handle @Xavier-x01)” if desired |
| “Xavier’s **intentions**” in PDF ingest summary | [evidence/cici-personalization-pdf-ingest-2026-04-13.md](evidence/cici-personalization-pdf-ingest-2026-04-13.md) | archived session paraphrase | no action |
| `first-good-morning-runbook` “Xavier paths” | [first-good-morning-runbook.md](first-good-morning-runbook.md) | active runbook | **fixed** → Cici instance + template `users/xavier/` |
| `cici_journal_ob1_digest` docstring “Xavier’s OB1” | [scripts/cici_journal_ob1_digest.py](../../scripts/cici_journal_ob1_digest.py) | ambiguous (script header) | review — document only in this PR; no script edit |

## Boundary check

| Check | Status |
|-------|--------|
| Cici `users/cici/governed-state` is not hosted in grace-mar as a live tree | **Pass** — only docs/evidence *describe* the external repo; no `users/cici/governed-state` directory under grace-mar. |
| `users/grace-mar` content is not normatively *imported* into work-cici as Record | **Pass** — references are boundary rules, leakage checks, or optional mentor links (e.g. cici-notebook discoverability); not bulk copy. |
| work-cici remains WORK-only | **Pass** — README + hub state not Record truth. |
| work-cici is not Cici’s Record repo | **Pass** — stated in hub + README. |
| Scripts do not **push** to Cici’s GitHub automatically | **Pass** — e.g. `cici_journal_ob1_digest.py` **writes** local `cici-notebook` markdown only; API read for activity; no auto-push in script. |
| [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md) exists and is linked | **Pass** — linked from [README.md](README.md), [UPLOAD-PREP.md](UPLOAD-PREP.md), [WORK-LEDGER.md](WORK-LEDGER.md), etc. |

## Script compatibility check

| Script | Role | Classification |
|--------|------|----------------|
| [build_xavier_handbook_bundle.py](../../scripts/build_xavier_handbook_bundle.py) | Assembles `smm-xavier-handbook-bundle.md` for work-politics SMM print | **safe legacy name** (downstream paths + handbooks) |
| [generate_smm_xavier_pdf.sh](../../scripts/generate_smm_xavier_pdf.sh) | HTML/PDF from bundle | **safe legacy name** |
| [xavier_journal_ob1_digest.py](../../scripts/xavier_journal_ob1_digest.py) | Deprecated; forwards to `cici_journal_ob1_digest.py` | **safe legacy name** (compat entry) |
| [cici_journal_ob1_digest.py](../../scripts/cici_journal_ob1_digest.py) | Local day files under `work-cici/cici-notebook/`; GitHub API for activity | **safe**; not a rename candidate in this PR |
| [review_orchestrator.py](../../scripts/runtime/review_orchestrator.py) | `work_lanes` includes `xavier` (legacy tag) and `cici` | **safe** (string match for lane tags) |

None of the above are **unsafe**; **needs alias wrapper** and **needs future rename** are deferred until a dedicated tooling PR with path updates. **No script renames** in this audit PR.

## Remaining drift

After the small INDEX / LANES / first-good-morning fixes above, **no** top-level table row in `README` / `INDEX` / `LANES` (audited) uses “Xavier” as the *current* lane name.

Ongoing “Xavier” uses that are **intentional** (not drift): GitHub `Xavier-x01`, instance template path `users/xavier/`, legacy filenames, handoff that says “Xavier (owner) approves” in the **Cici** repo, and historical evidence text.

**Optional** future polish (not required for this audit): [ALIGNMENT.md](ALIGNMENT.md) line that says **Xavier’s instance layer** could be rephrased to foreground **Cici** with handle in parens, without deleting technical accuracy.

## Recommended next PR

**C. add CI grep guard for active-prose drift** — **done** in a follow-up: `python3 scripts/check_work_cici_drift.py` in [scripts/](../../scripts/check_work_cici_drift.py), wired into [`.github/workflows/naming-check.yml`](../../.github/workflows/naming-check.yml) and documented in [LANE-CI](LANE-CI.md#drift-guard). Fails the build on disallowed active-prose substrings, with an allowlist for `formerly Xavier`, `Xavier-x01`, `work-xavier`, `users/xavier/`, `xavier-` filenames, `TERMS-XAVIER`, `COMPANION-XAVIER`, and legacy SMM / digest script names. No new automation that writes to Cici.

(Alternatives not chosen for that hardening: **A** wrapper scripts, **B** full INDEX/LANES nav only — reflows shipped alongside C.)

---

## Validation (recorded 2026-04-24)

```bash
grep -R "Advisor/project module for Xavier" -n docs/skill-work/README.md docs/skill-work/work-cici/README.md docs/skill-work/work-cici/INDEX.md docs/skill-work/work-cici/LANES.md 2>/dev/null || true
grep -R "Not Xavier" -n docs/skill-work/README.md docs/skill-work/work-cici/README.md docs/skill-work/work-cici/INDEX.md docs/skill-work/work-cici/LANES.md 2>/dev/null || true
# (no matches expected for those four files)
grep -R "users/grace-mar" -n docs/skill-work/work-cici 2>/dev/null | head -20
find docs/skill-work/work-cici -maxdepth 1 -type f | sort
test -d docs/skill-work/work-cici
```

`users/grace-mar` matches are **expected** on leakage / boundary lines (forbid copying into instance trees).

---

## Report summary

- **Audit file created:** this document.
- **Tiny fixes made:** [INDEX.md](INDEX.md) (SYNC-DAILY + rubric rows; **new row** pointing to this audit), [LANES.md](LANES.md) (title + lead), [first-good-morning-runbook.md](first-good-morning-runbook.md) (Cici instance wording). **No** change to the two strict grep targets (“Advisor/project module for Xavier”, “Not Xavier’s Record…”) in hub/README/INDEX/LANES — they were **already** absent; optional drift fixes only.
- **Xavier references:** Classified in the table above; scripts classified **safe legacy** or **safe** with no renames in this pass.
- **Record surfaces / SELF / SKILLS / users/grace-mar:** **No** edits to companion Record trees or `.cursor/skills/`; **no** new governed-state import into grace-mar.
