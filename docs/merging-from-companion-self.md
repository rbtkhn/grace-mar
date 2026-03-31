# Merging Upgrades from Companion-Self (Template → Instance)

**Purpose:** Grace-Mar is a private **instance** and working tool; companion-self is the upstream **template** repo and live public/open-source product surface. When the template is updated (concept, protocol, seed, schema), this doc describes how to pull those changes into grace-mar without overwriting the Record. Structural improvements proven inside grace-mar may later be generalized back into companion-self, but instance data and private workflows remain in grace-mar. See [COMPANION-SELF-BOOTSTRAP](../bootstrap/companion-self-bootstrap.md) §5 for the contract. For a side-by-side overview of instance vs template, see [grace-mar vs companion-self](grace-mar-vs-companion-self.md).

**Workspace boundary:** All grace-mar modifications—including merges from companion-self—are done in **this (grace-mar) workspace**. Do not edit grace-mar from a companion-self workspace; there, grace-mar is read-only reference. When you perform the merge checklist below, you are in the grace-mar workspace; companion-self is pulled or opened for reference only. See companion-self [COMPANION-SELF-BOOTSTRAP](https://github.com/rbtkhn/companion-self/blob/main/companion-self-bootstrap.md) §7.

---

## 0. Editable companion-self from this repo (multi-root + `template_diff`)

1. **Clone or submodule** the template into **`companion-self/`** at the root of this repository (sibling to `bot/`, `docs/`, etc.):
   - **Clone (simplest):** `git clone https://github.com/rbtkhn/companion-self.git companion-self`
   - **Submodule (tracked pin):** remove `/companion-self/` from `.gitignore` if present, then  
     `git submodule add https://github.com/rbtkhn/companion-self.git companion-self`  
     and commit the submodule metadata.
2. **Open the multi-root workspace** in Cursor / VS Code: **File → Open Workspace from File…** → choose **`grace-mar.code-workspace`**. You get two roots: **grace-mar** (`.`) and **companion-self** (`./companion-self`).
3. **Template workspace filename (companion-self repo only):** If the upstream template still uses a long name such as `companion-self-and-grace-mar.code-workspace`, rename it in **companion-self** to `companion-self.code-workspace` or `template.code-workspace` and update template README links there. Grace-mar’s own workspace file stays **`grace-mar.code-workspace`**. See [naming-convention.md](naming-convention.md).
4. **Template diff default path:** `python scripts/template_diff.py` uses **`./companion-self`** (under the grace-mar repo root). Override with `--companion-self /path` or **`GRACE_MAR_COMPANION_SELF`**. If `companion-self/` is missing and clone is enabled, the script still clones into that path (same as before).

The default clone-on-miss behavior targets **`./companion-self`** instead of `/tmp/companion-self`, so edits and diffs stay inside your tree when you use the workspace file.

---

## 1. Template sync surfaces (safe to sync)

Use the live template repo's manifest and upgrade docs as the source of truth. Grace-mar keeps local copies or instance-specific equivalents where useful, but not every template path must exist verbatim in the instance. **When companion-self adds or renames files, update this section and the audit.**

| Path | Description |
|------|-------------|
| `template-manifest.json` | Authoritative template inventory; use this first when checking what the template now contains |
| `template-version.json` | Template version / release marker for recording sync baseline |
| `how-instances-consume-upgrades.md` | Companion-self's instance upgrade contract; compare with this doc when drift appears |
| `docs/concept.md` | Template concept doc; grace-mar may mirror this into its broader concept docs rather than a same-named file |
| `docs/identity-fork-protocol.md` | Protocol: stage → approve → merge; evidence linkage (template **short form**; see IFP note below) |
| `docs/seed-phase.md` | Template seed-phase definition; grace-mar currently expresses this through ARCHITECTURE and operator docs |
| `docs/long-term-objective.md` | Template-level long-term objective / system rule |
| `docs/two-hour-screentime-target.md` | Template-level screen time constraint / philosophy |
| `docs/instance-patterns.md` | Template guidance for instance variants and advanced patterns |
| `users/_template/` | Template scaffold for new instances; reference-only in grace-mar (do not copy into `users/grace-mar/`) |
| `docs/CONTRADICTION-ENGINE-SPEC.md`, `docs/contradiction-resolution.md`, `docs/approval-inbox-spec.md` | Contradiction engine + gate review surface; grace-mar has instance-specific copies—compare on sync |
| `docs/change-review.md`, `docs/contradiction-policy.md`, `docs/change-types.md`, `docs/change-review-lifecycle.md` | Change-review doctrine (post-seed); `template-manifest.json` → `change_review` |
| `docs/change-review-validation.md` | Operator doc: validation rules and commands for `validate-change-review.py` (grace-mar may mirror under `docs/` for instance operators) |
| `schema-registry/change-*.v1.json`, `schema-registry/identity-diff.v1.json` | Change-review JSON Schemas; listed under `change_review.schemas` in the manifest |
| Grace-mar mirrors | Same four doctrine files under `docs/` (banner points to template); schemas under `docs/schemas/` (`change-proposal.v1.json`, …, `identity-diff.v1.json`) for local tooling and diffs |
| Grace-mar equivalents | `docs/conceptual-framework.md`, `docs/architecture.md`, `docs/self-template.md`, `docs/skills-template.md`, `docs/evidence-template.md`, `docs/memory-template.md`, `AGENTS.md` remain valid instance-side mirrors or elaborations when aligned conceptually |
| Instance naming | [naming-convention.md](naming-convention.md) — lowercase docs, reserved `AGENTS.md`, OpenClaw export path, template workspace note |

**Never overwrite with template:** `users/grace-mar/` (the Record), instance-specific bot/config (e.g. Telegram token, render.yaml), PRP output paths (e.g. grace-mar-llm.txt). Instance-only docs (e.g. PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW) stay in grace-mar unless you explicitly promote them to the template.

**Useful rule:** Treat `grace-mar` as the proving ground and `companion-self` as the reusable base. If a change is structural and instance-agnostic, it may be a candidate to merge back upstream later. If it depends on live Record state, private operator routines, or local deployment quirks, keep it instance-only.

**Current alignment note:** The live companion-self repo contains template-only paths that do not need one-to-one copies in grace-mar, but they do need explicit acknowledgment in audits and sync notes. Use `docs/skill-work/work-companion-self/audit-report-manifest.md` as the current path-level reference until a newer diff is generated.

### Identity Fork Protocol (IFP) — short form vs full spec

Companion-self ships **`docs/identity-fork-protocol.md` as a short-form summary** with a pointer to the reference implementation. Grace-mar holds the **canonical full IFP v1.0** at the same path (`docs/identity-fork-protocol.md`) — much longer, normative for this instance. **Do not overwrite** grace-mar’s file with the template short form during template→instance sync. If the template summary changes, merge **selective** clarifications by hand, or promote an updated full spec to companion-self only as a deliberate release. Upstream link in the template must target `docs/identity-fork-protocol.md` (not a legacy `IDENTITY-FORK-PROTOCOL.md` filename).

---

## 2. Merge checklist

Use this when you have updates in companion-self that should flow into grace-mar.

| Step | Action |
|------|--------|
| 1 | **Get template state** — Clone or pull companion-self (e.g. `git clone https://github.com/rbtkhn/companion-self.git companion-self` at repo root per §0, or another path with `GRACE_MAR_COMPANION_SELF`). Note the commit or tag you're syncing from. |
| 2 | **Read template inventory** — Check `template-manifest.json`, `template-version.json`, and `how-instances-consume-upgrades.md` in companion-self so you know the current upstream surface before comparing individual files. |
| 3 | **Diff mapped paths** — Compare template files with grace-mar's same-name copies or instance-side equivalents. `docs/skill-work/work-companion-self/audit-report-manifest.md` and `scripts/template_diff.py` can help. |
| 4 | **Merge into grace-mar** — For each area where the template is ahead, update grace-mar's mirrored file or instance-side equivalent. Resolve any instance-specific additions in grace-mar (keep them). Do **not** overwrite `users/grace-mar/` or instance config. |
| 5 | **Validate** — Run `python scripts/validate-integrity.py --user grace-mar --json` and `python scripts/governance_checker.py`. Fix any breakage. |
| 6 | **Log the sync** — Record in §3 (Template sync log) the date, companion-self commit/tag or template version, and paths updated. |

---

## 2a. Merge slice — routine template hygiene

When companion-self moves quickly, prefer **small, scoped merges** over rare “catch-up” merges. Each slice should be one reviewable purpose (e.g. one doc, one schema file, one script), then log §3 and commit with the **template SHA** in the commit body.

| Step | Action |
|------|--------|
| 1 | **Pin** — `git -C companion-self pull` (or fetch); note `HEAD` and `template-version.json` (`templateVersion`, `gitTag`). |
| 2 | **Diff** — `python3 scripts/template_diff.py --use-manifest -o docs/skill-work/work-companion-self/audit-report-manifest.md` |
| 3 | **Choose one slice** — e.g. one `docs/` file, `schema-registry/` file, or validator; skip `app/` unless you run the template student app. |
| 4 | **Merge by hand** — copy or edit per §2; never bulk-overwrite `users/grace-mar/`. |
| 5 | **Validate** — `python3 scripts/validate-integrity.py --user grace-mar --json`; run merged validators if you pulled them (e.g. `validate-change-review.py` on demo paths). |
| 6 | **Log + commit** — §3 row; optional update [`template-source.json`](../template-source.json) (`companionSelfCommit`, `templateVersion`, `mergedAt` / `syncedAt`). |

**Alignment triage:** For governance-first review (behavior vs wording-only diffs, manifest rhythm, optional DESIGN/validator upstream), see [work-companion-self/README.md § Three-track alignment](skill-work/work-companion-self/README.md#three-track-alignment-operator-policy).

**Operator verification (ongoing):** There is **no** `validate-template-sync.py` in companion-self as of template **0.4.0**; template **manifest integrity** is `node scripts/validate-template.js` (see companion-self `how-instances-consume-upgrades.md` § Auditability). Instances record merges in §3 and/or `template-source.json`; do not assume tools from informal narratives until they exist on `main`.

---

## 3. Template sync log

Record each merge from template so you can see when grace-mar was last updated and what changed.

| Date | Companion-self (commit or tag) | Paths updated |
|------|---------------------------------|---------------|
| 2026-03-28 | companion-self **`main` @ `a08650a98c30277aa219c3bfc3ef02d78504a2c4`** | **Work-business seed parity (template):** [`schema-registry/work-business-seed.v1.json`](../schema-registry/work-business-seed.v1.json), [`users/_template/work-business.md`](../users/_template/work-business.md), [`users/_template/seed-phase/work_business_seed.json`](../users/_template/seed-phase/work_business_seed.json), [`users/demo/seed-phase/work_business_seed.json`](../users/demo/seed-phase/work_business_seed.json); `seed-phase-manifest.json` (both template + demo) artifact keys **`work_business_seed`** then **`work_dev_seed`**; [`scripts/validate-seed-phase.py`](../scripts/validate-seed-phase.py), [`scripts/generate-seed-dossier.py`](../scripts/generate-seed-dossier.py); [`template-manifest.json`](../template-manifest.json) `seed_phase.schemas` + paths; docs [`seed-phase-artifacts.md`](seed-phase-artifacts.md), [`seed-phase-survey.md`](seed-phase-survey.md), [`seed-phase-validation.md`](seed-phase-validation.md); [`users/_template/README.md`](../users/_template/README.md); root [`README.md`](../README.md) scaffold line. **Refreshed** [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) via `template_diff.py --use-manifest`. Validated: `validate-seed-phase` (demo strict + `_template` placeholders); `generate-seed-dossier` (demo). |
| 2026-03-27 | companion-self **`template-v0.4.0`** / **`main` @ `3eaf7b17090ae1e8d497856544febf397cb4e98a`** | **Schema + validator parity:** root [`schema-registry/`](../../schema-registry/) (full), [`template-manifest.json`](../../template-manifest.json), [`how-instances-consume-upgrades.md`](../../how-instances-consume-upgrades.md), companion-self validators and JS (`scripts/validate-change-review.py`, `validate-seed-phase.py`, `generate-identity-diff.py`, `validate-template.js`, `validate-record-boundaries.py`, `layer-enforcer.py`, `gate-guardian.js`, `generate-provenance.js`, `truth-density-score.py`, `generate-seed-dossier.py`, `requirements-seed-phase.txt`), `users/_template/**` (full scaffold), `users/demo/seed-phase`, `users/demo/review-queue`, `bridges/bridge-schema.json`, manifest-listed docs (seed-phase series, `layer-map.json`, `docs/skill-work/skill-work-alpha-school/*`, `docs/skill-work/skill-work-human-teacher/*`, `docs/self-identity/intent-coherence-checklist.md`, etc.). **Mirrored** template schemas into [`docs/schemas/`](../schemas/) (kept [`conflict-object.schema.json`](../schemas/conflict-object.schema.json)). **Instance tweak:** `docs/layer-map.json` — removed recursive `users/**/Record/**` from `forbiddenCrossings` so `users/grace-mar/runtime-bundle/Record` passes `layer-enforcer` while `users/*/Record` stays forbidden. Validated: `validate-change-review` (demo + `_template`), `validate-seed-phase` (demo), `node scripts/validate-template.js`, `validate-integrity.py`. |
| 2026-03-27 | companion-self **`template-v0.4.0`** / **`main` @ `3eaf7b17090ae1e8d497856544febf397cb4e98a`** | **Merge slice (docs):** [docs/change-review-validation.md](change-review-validation.md) from template (validator commands + scope). **Refreshed** [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) via `template_diff.py --use-manifest`. **Note:** Template has no `validate-template-sync.py`; use `node scripts/validate-template.js` in template repo for manifest path checks per upstream § Auditability. |
| 2026-03-26 | companion-self **`template-v0.3.4`** / **`main` @ `4df99a4`** | **Student app:** `GET /api/change-review?profile=demo`, **`/change-review`** page, nav links; README + `readme-student-app.md`. Template **0.3.4**. Instance merge: optional pull for operators who run the template app. |
| 2026-03-26 | companion-self **`template-v0.3.3`** / **`main` @ `9a042b0`** | **Change-review demo + validator:** `scripts/validate-change-review.py`, `users/demo/change-review/*`, manifest `change_review.validator`, template **0.3.3**. Grace-mar: on-disk mirrors of doctrine docs + `docs/schemas/` change-review v1 schemas; contradiction docs link to local mirrors. |
| 2026-03-26 | companion-self **`template-v0.3.2`** / **`main` @ `0475ed1`** | **Change review PR1+PR2:** doctrine docs (`docs/change-review.md`, `contradiction-policy.md`, `change-types.md`, `change-review-lifecycle.md`), five `schema-registry/*change*` + `identity-diff.v1.json`, README + `how-instances-consume-upgrades.md`, `template-manifest.json` `change_review` + `schemas`, `docs/schema-record-api.md`, template version **0.3.2**. Grace-mar: sync surfaces logged in §1; instance contradiction docs remain authoritative for the live fork—compare on next merge. |
| 2026-03-26 | companion-self **`main` @ `a679f95`** (local clone; push upstream separately) | **Seed Phase v2** in template: `docs/seed-phase*.md`, `schema-registry/seed-*.v1.json`, `users/_template/seed-phase/`, `users/demo/seed-phase/`, `scripts/validate-seed-phase.py`, CI workflow. Grace-Mar mapping: [companion-self-seed-phase-v2-mapping.md](companion-self-seed-phase-v2-mapping.md). |
| 2026-03-26 | — (grace-mar-only) | **Added:** [docs/seed-phase-wizard.md](seed-phase-wizard.md), `scripts/seed-phase-wizard.py`, `scripts/good-morning-brief.py` — operator seed + morning brief under `users/<id>/`; does not replace template `docs/seed-phase.md`; companion-self may port an adapted version later. |
| 2026-03-26 | companion-self **`main` @ `87628a5`** (manifest diff only) | **Refreshed:** [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) via `python3 scripts/template_diff.py --use-manifest -o …`. Not a content merge from template. |
| 2026-03-23 | companion-self **`main` @ `288b438`** | **Merged:** SELF-LIBRARY template governance (`users/_template/self-library.md` + example corpus doc). [Commit](https://github.com/rbtkhn/companion-self/commit/288b4386684e076df894536624308e69305ae229). Grace-mar: [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md](skill-work/work-companion-self/COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md), [TEMPLATE-BASELINE](skill-work/work-companion-self/TEMPLATE-BASELINE.md). |
| *(baseline for governance merges)* | **`288b438`** | Recorded in [TEMPLATE-BASELINE.md](skill-work/work-companion-self/TEMPLATE-BASELINE.md). Re-run manifest diff after each material template pull; `main` tip may advance beyond this pin. |

---

## 4. Diff script (implemented)

[`scripts/template_diff.py`](../scripts/template_diff.py) compares companion-self and grace-mar:

- Default template root: `$GRACE_MAR_COMPANION_SELF` or `./companion-self` (see §0); clones shallow `main` if missing unless `--no-clone`.
- **`--use-manifest`** — paths from companion-self `template-manifest.json`, plus a recursive pass over `docs/skill-work/` in both repos.
- **`--output <file>`** — write the report; commit [work-companion-self/audit-report-manifest.md](skill-work/work-companion-self/audit-report-manifest.md) when refreshing the audit.

It **does not** overwrite instance files; operator merges by hand per §2.

When an operator or agent runs a **template + boundary audit** (e.g. `coffee` **A**; legacy hey **A** still works), the narrative should close with **specific upstream / downstream recommendations for reconciliation code** — `scripts/`, validators, CI, hooks — not only doc drift. Spec: [work-companion-self/README — Reconciliation code audit](skill-work/work-companion-self/README.md#reconciliation-code-audit-upstream-and-downstream).

---

## 5. Deciding whether a Grace-Mar change should go upstream

Use this checklist before proposing an instance-side improvement back to `companion-self`.

| Question | If yes | If no |
|------|--------|-------|
| Is the change reusable across many future instances? | Candidate for upstreaming | Keep in `grace-mar` |
| Does it avoid `users/grace-mar/`, private artifacts, and instance-only config? | Candidate for upstreaming | Keep in `grace-mar` |
| Can it be described without Abby/Grace-Mar-specific context? | Candidate for upstreaming | Generalize first or keep local |
| Is it governance, schema, docs, tooling, bootstrap, or sync logic? | Strong upstream candidate | Review carefully |
| Is it a private operating habit or one-off workflow for this instance? | Probably instance-only | Keep in `grace-mar` |

If mixed, split the change: upstream the reusable layer to `companion-self`; keep the instance-specific layer in `grace-mar`.

---

## 6. Related

- **companion-self-bootstrap.md** §5 — Contract: safe to sync, never overwrite, process.
- **operator-weekly-review.md** — Optional step: periodic template sync when template or instance change.
- **AGENTS.md** — Template-level rules; when updated in companion-self, sync into grace-mar per this doc.
