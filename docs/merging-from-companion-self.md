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
3. **Template diff default path:** `python scripts/template_diff.py` uses **`./companion-self`** (under the grace-mar repo root). Override with `--companion-self /path` or **`GRACE_MAR_COMPANION_SELF`**. If `companion-self/` is missing and clone is enabled, the script still clones into that path (same as before).

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
| `docs/identity-fork-protocol.md` | Protocol: stage → approve → merge; evidence linkage |
| `docs/seed-phase.md` | Template seed-phase definition; grace-mar currently expresses this through ARCHITECTURE and operator docs |
| `docs/long-term-objective.md` | Template-level long-term objective / system rule |
| `docs/two-hour-screentime-target.md` | Template-level screen time constraint / philosophy |
| `docs/instance-patterns.md` | Template guidance for instance variants and advanced patterns |
| `users/_template/` | Template scaffold for new instances; reference-only in grace-mar (do not copy into `users/grace-mar/`) |
| `docs/CONTRADICTION-ENGINE-SPEC.md`, `docs/contradiction-resolution.md`, `docs/approval-inbox-spec.md` | Contradiction engine + gate review surface; grace-mar has instance-specific copies—compare on sync |
| Grace-mar equivalents | `docs/conceptual-framework.md`, `docs/architecture.md`, `docs/self-template.md`, `docs/skills-template.md`, `docs/evidence-template.md`, `docs/memory-template.md`, `AGENTS.md` remain valid instance-side mirrors or elaborations when aligned conceptually |

**Never overwrite with template:** `users/grace-mar/` (the Record), instance-specific bot/config (e.g. Telegram token, render.yaml), PRP output paths (e.g. grace-mar-llm.txt). Instance-only docs (e.g. PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW) stay in grace-mar unless you explicitly promote them to the template.

**Useful rule:** Treat `grace-mar` as the proving ground and `companion-self` as the reusable base. If a change is structural and instance-agnostic, it may be a candidate to merge back upstream later. If it depends on live Record state, private operator routines, or local deployment quirks, keep it instance-only.

**Current alignment note:** The live companion-self repo contains template-only paths that do not need one-to-one copies in grace-mar, but they do need explicit acknowledgment in audits and sync notes. Use `docs/skill-work/work-companion-self/audit-report-manifest.md` as the current path-level reference until a newer diff is generated.

---

## 2. Merge checklist

Use this when you have updates in companion-self that should flow into grace-mar.

| Step | Action |
|------|--------|
| 1 | **Get template state** — Clone or pull companion-self (e.g. `git clone https://github.com/rbtkhn/companion-self.git /tmp/companion-self` or open in a sibling directory). Note the commit or tag you're syncing from. |
| 2 | **Read template inventory** — Check `template-manifest.json`, `template-version.json`, and `how-instances-consume-upgrades.md` in companion-self so you know the current upstream surface before comparing individual files. |
| 3 | **Diff mapped paths** — Compare template files with grace-mar's same-name copies or instance-side equivalents. `docs/skill-work/work-companion-self/audit-report-manifest.md` and `scripts/template_diff.py` can help. |
| 4 | **Merge into grace-mar** — For each area where the template is ahead, update grace-mar's mirrored file or instance-side equivalent. Resolve any instance-specific additions in grace-mar (keep them). Do **not** overwrite `users/grace-mar/` or instance config. |
| 5 | **Validate** — Run `python scripts/validate-integrity.py --user grace-mar --json` and `python scripts/governance_checker.py`. Fix any breakage. |
| 6 | **Log the sync** — Record in §3 (Template sync log) the date, companion-self commit/tag or template version, and paths updated. |

---

## 3. Template sync log

Record each merge from template so you can see when grace-mar was last updated and what changed.

| Date | Companion-self (commit or tag) | Paths updated |
|------|---------------------------------|---------------|
| 2026-03-23 | companion-self **`main` @ `288b438`** | **Merged:** SELF-LIBRARY template governance (`users/_template/self-library.md` + example corpus doc). [Commit](https://github.com/rbtkhn/companion-self/commit/288b4386684e076df894536624308e69305ae229). Grace-mar: [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md](skill-work/work-companion-xavier/COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md), [TEMPLATE-BASELINE](skill-work/work-companion-xavier/TEMPLATE-BASELINE.md). |
| *(no recorded baseline yet)* | — | Before claiming full alignment, record the companion-self commit/tag or `template-version.json` value used for the sync |

---

## 4. Future: optional diff script

When companion-self has stable content, a small script could:

- Accept two roots (companion-self and grace-mar) and a list of template paths.
- Report which paths differ (and optionally show a short diff).
- **Not** overwrite anything; operator still performs the merge.

Placeholder: `scripts/template_diff.py` or similar, to be added when useful.

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
