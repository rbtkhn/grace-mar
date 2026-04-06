# How Instances Consume Upgrades from This Template

**Companion-Self template**

When companion-self (this repo) is updated, an instance (e.g. [Grace-Mar](https://github.com/rbtkhn/grace-mar)) can pull those changes **without overwriting its Record**.

**Workspace boundary:** When working on the template, use a workspace where grace-mar is read-only (e.g. `companion-self-and-grace-mar.code-workspace`). Do not modify the instance from this workspace; all instance changes and template merges happen in the instance's own workspace. See [companion-self-bootstrap](companion-self-bootstrap.md) §7.

---

## Sync architecture (template view)

Instances should read template sync through four layers:

| Layer | Owned by | Purpose |
|------|----------|---------|
| **Doctrine** | Template upgrade docs + instance merge docs | What may sync, what must never sync, and how to merge safely |
| **Contract** | Instance-side machine file (for example `instance-contract.json`) | Which template version / commit the instance is trying to match |
| **Applied provenance** | Instance-side machine file (for example `template-source.json`) | Which template commit the instance actually merged most recently |
| **Audit** | Diff scripts, audit reports, sync logs | What currently differs and what merge slice should happen next |

The important distinction is simple:

- the **contract** says what the instance is **targeting**
- the **applied provenance** says what the instance has **actually merged**

They may differ temporarily during staged catch-up work. Do not force them into one field.

---

## Safe to Sync from Template

- **Concept docs** — e.g. concept.md, generalized framework
- **Protocol docs** — e.g. identity-fork-protocol (short form or full spec if maintained here)
- **Seed-phase definition** — what seed is, what it produces, that it is the only creation path
- **SELF / self-knowledge, self-identity, self-curiosity, self-personality / self-skill-think / self-skill-write / self-skill-work / self-skill-steward / self-evidence / recursion-gate / self-memory templates** — schema and structure only; instance keeps its own copies and updates them to match the template when upgrading
- **Template-level governance** — pipeline rule, knowledge boundary, operating modes (e.g. in AGENTS.md or equivalent in the instance, derived from template guidance)

The instance **compares** template docs and templates with its own, **merges** changes into its files, and runs any validation (e.g. governance checker, validate-integrity). There is **no** automated overwrite of `users/<id>/`.

---

## Never Overwrite with Template

- **`users/<id>/`** — The Record (SELF, self-skill-think, self-skill-write, self-skill-work, self-skill-steward, self-evidence, etc.) for a real companion. Template has no Record; instance must never replace it with template content.
- **Instance-specific config** — Bot tokens, instance domains, PRP output paths, etc.
- **Instance-only code** — Bot, pipeline scripts, instance tooling.

---

## Process (Recommended)

1. Pull or merge from companion-self (e.g. `git pull origin main` from template remote, or copy specific files).
2. Confirm the instance’s **target contract** (for example its `instance-contract.json`) before comparing files.
3. Compare template paths with instance paths (docs, `users/_template/` vs instance’s template or schema docs).
4. Merge changes into the instance’s docs and template files by hand (or with a small sync script that only touches allowed paths).
5. Update the instance’s **applied provenance** record (for example `template-source.json`) with the actual commit, version, and merged paths.
6. Run instance validation (e.g. governance check, validate-integrity).
7. Run the instance’s sync-contract check (for example `python scripts/validate_template_sync_contract.py`) so target contract, applied provenance, and local manifest mirror stay structurally aligned.
8. Do **not** copy template `users/_template/` *over* an existing `users/<id>/` Record — use it only when creating a **new** user directory.

---

## Canonical Template Paths (for instance merge checklist)

When an instance (e.g. Grace-Mar) merges upgrades from companion-self, it should compare and merge **only** these paths. **When companion-self adds or renames files, this list and the template manifest are updated.** Instance merge docs (e.g. grace-mar's `docs/MERGING-FROM-COMPANION-SELF.md`) should align with this list.

**Machine-readable:** The same list is in **`template-manifest.json`** at repo root (paths, descriptions, optional flag, `canonicalAsOf` date). Scripts and CI can diff instance files against it; keep the manifest and this table in sync.

**Instance-side copy rule:** If an instance keeps a local copy of `template-manifest.json`, treat that copy as a **cached audit mirror**, not as a new independent source of truth. The canonical manifest remains the one in companion-self at the commit the instance claims to target or has applied.

| Path | Description |
|------|-------------|
| `docs/concept.md` | Concept: Record, Voice, education structure, knowledge boundary, invariants, long-term objectives. |
| `docs/identity-fork-protocol.md` | Protocol: Sovereign Merge Rule, schema (SELF, self-skill-*, self-evidence), evidence linking. |
| `docs/seed-phase.md` | Definition of seed phase; what creates initial Record. |
| `docs/long-term-objective.md` | Permanent system rules (democratize Alpha-style education; sovereignty; knowledge boundary). |
| `docs/skill-work/skill-work-alpha-school/alpha-school-reference.md` | Alpha School reference (skill-work-alpha-school submodule): benchmarks, 2-hour screen-time target, equivalent metrics. |
| `docs/skill-work/skill-work-human-teacher/human-teacher-objectives.md` | Human teaching/learning objectives (skill-work-human-teacher submodule): read and modulate skill-think; operator/parent augment path. |
| `docs/instance-patterns.md` | Instance patterns and reference implementation (Grace-Mar variations, analyst contract, staging format). |
| `docs/change-review.md` | Change review v1 entrypoint: governed post-seed self-revision doctrine (separate from seed phase). |
| `docs/contradiction-policy.md` | Contradiction classification and resolution policy during change review. |
| `docs/change-types.md` | Canonical change scopes for proposals (identity, pedagogy, upgrade_collision, etc.). |
| `docs/change-review-lifecycle.md` | Proposal-to-decision lifecycle (detect → decide → merge or preserve). |
| `schema-registry/change-proposal.v1.json` | Change-review JSON Schema: governed change proposal. |
| `schema-registry/change-decision.v1.json` | Change-review JSON Schema: decision record. |
| `schema-registry/identity-diff.v1.json` | Change-review JSON Schema: before/after diff payload. |
| `schema-registry/change-review-queue.v1.json` | Change-review JSON Schema: queue summary. |
| `schema-registry/change-event-log.v1.json` | Change-review JSON Schema: audit event log. |
| `schema-registry/boundary-classification.v1.json` | Persisted boundary hint snapshot per gate candidate (optional `review-queue/boundary-classifications/`). |
| `schema-registry/harness-replay-event.v1.json` | Compact replay step derived from audit JSONL (`grace_mar.replay`). |
| `schema-registry/answer-provenance.v1.json` | Heuristic lane-mix summary for recent pipeline rows. |
| `scripts/validate-change-review.py` | Validates `users/<id>/review-queue/` trees against change-review schemas (`--allow-empty` for empty template scaffold; `--allow-missing-decisions` when proposals and diffs exist but decisions do not). |
| `scripts/generate-identity-diff.py` | Renders Markdown from one `identity-diff` JSON file. |
| `docs/change-review-validation.md` | Operator doc: validation rules and commands. |
| `users/demo/review-queue/*` | Demo review-queue tree + README for change-review validation (not a live Record). |
| `users/_template/review-queue/*` | Template review-queue scaffold (empty proposal/decision/diff dirs allowed). |
| `users/_template/self.md` | SELF schema/structure scaffold for new users only. |
| `users/_template/self-knowledge.md` | IX-A: what they've learned (self-knowledge) scaffold. |
| `users/_template/self-identity.md` | Durable identity commitments scaffold (identity, boundaries, role commitments). |
| `users/_template/self-curiosity.md` | IX-B: what they're curious about (self-curiosity) scaffold. |
| `users/_template/self-personality.md` | IX-C: voice, preferences, values (self-personality) scaffold. |
| `users/_template/self-skill-think.md` | THINK (self-skill-think) scaffold. |
| `users/_template/self-skill-write.md` | WRITE (self-skill-write) scaffold. |
| `users/_template/self-skill-work.md` | WORK (self-skill-work) scaffold. |
| `users/_template/self-skill-steward.md` | STEWARD (self-skill-steward) scaffold — governance literacy. |
| `users/_template/self-evidence.md` | Evidence schema/structure scaffold. |
| `users/_template/recursion-gate.md` | Recursive-gate staging scaffold (candidates at the gate). |
| `users/_template/self-memory.md` | Self-memory scaffold (short/medium/long; non-Record; optional). |
| `users/_template/self-library.md` | SELF-LIBRARY scaffold: governance + **empty `entries:`**; add LIB rows via gate. Optional bulk example: `docs/self-library-example-corpus-grace-mar-derived.md`. |
| `docs/self-library-example-corpus-grace-mar-derived.md` | Optional grace-mar-derived LIB list for operators who want a trimmable starting shelf (not default for new instances). |

Optional (instance may keep its own and take only selected content): `README.md`, `companion-self-bootstrap.md`, other `docs/` (roadmap, recursive-self-learning-objectives, insights, etc.). **Never overwrite** `users/<id>/` for any real user id.

A small sync script could list these paths and diff/merge them into the instance; it must exclude `users/<id>/` for any real user.

---

## Auditability (bridging the gap)

**Template side:** `template-manifest.json` is the single source of truth for canonical paths and the date they were last updated (`canonicalAsOf`). When the path list or key docs change, update the manifest and commit. An auditor can read the manifest and compare to any companion-self commit.

**Template versioning:** The template repo has **`template-version.json`** at repo root (`templateVersion`, `releasedAt`, `gitTag`) and optional **git tags** (e.g. `template-v0.2.0`). Prefer pulling from a tag when upgrading so the instance has a fixed reference. Update `canonicalAsOf` in `template-manifest.json` when cutting a release.

**Template integrity:** Run **`node scripts/validate-template.js`** from the repo root to ensure every path in `template-manifest.json` exists and that no forbidden files (e.g. `.DS_Store`) are tracked. CI runs this on push; instances can run it after pulling to confirm manifest and filesystem match.

**Instance side:** Keep two separate machine concepts:

- **target contract** — what template version / commit the instance is aiming to align to
- **applied provenance** — what template commit actually landed in the instance most recently

When you merge from companion-self, **record in your repo** the template commit (or tag) and date in an applied provenance file such as `template-source.json`:

- `companionSelfCommit`: the full git commit hash (or tag) you merged from
- `templateVersion`: from template’s `template-version.json` (e.g. 0.2.0)
- `syncedAt`: date (ISO) when that merge landed in the instance

An example schema lives in **`docs/template-source.example.json`**; copy to your instance (e.g. repo root or `docs/template-source.json`) and update it after each merge. That gives a verifiable audit trail: "this instance merged from companion-self at this point."

If the instance also keeps a target contract file (for example `instance-contract.json`), that file should hold the **intended** upstream version / commit separately rather than being overwritten by every small applied slice.

**How to audit:** (1) From companion-self: open `template-manifest.json` at the commit the instance claims it merged. (2) From the instance: read its recorded commit and `syncedAt`. (3) Optionally: instance CI or a script can diff its copy of the canonical paths against the manifest (e.g. fetch manifest from companion-self at the recorded commit, compare paths and optionally checksums). No automated link is required; both sides are independently auditable and can be compared by hand or script.

**Recommended instance check:** After sync, run a small validator that checks:

- target contract file exists and names the intended version / commit
- applied provenance file exists and points back to the same target contract
- local cached manifest mirror matches the target template version
- target vs applied drift is reported as a warning unless the operator explicitly wants strict convergence

---

*Companion-Self template · Upgrade consumption*

---

## Seed-phase upgrade compatibility

Template upgrades may change **seed JSON Schemas** (`schema-registry/seed-*.v1.json`), **readiness policy** ([docs/seed-phase-readiness.md](docs/seed-phase-readiness.md)), or artifact layout under `users/_template/seed-phase/`.

| Rule | Rationale |
|------|-----------|
| **Do not overwrite** prior seed outputs in an instance repo without operator review | Preserves provenance and guardian/companion decisions. |
| **Re-validate or version-map** | Run `python3 scripts/validate-seed-phase.py <path>` after merge; if schemas diverge, document field mapping from old → new `seed_phase_version` instead of silent replacement. |
| **Keep seed artifacts separate from merged Record** | Seed files are pre-activation; `users/<id>/` Record merges use the identity fork protocol only after activation. |

Instance merge docs should log template `templateVersion` / `seed_phase.version` when seed-related paths change.

---

## Template upgrade collisions

Template upgrades must not silently override instance-governed state.

If a template upgrade conflicts with:

- durable identity commitments
- pedagogy rules
- memory-governance policy
- safety or boundary rules
- prior seed outputs
- other reviewed instance commitments

the instance should open a governed change proposal rather than auto-merge the new template logic into active state.

### Required behavior

1. **Do not overwrite reviewed instance truth with template defaults**  
   Template doctrine is upstream guidance, not authority to erase instance history.

2. **Open a change proposal when upgrades materially affect governed state**  
   Upgrade collisions should become visible review objects.

3. **Preserve prior state refs and evidence refs**  
   The instance should remain auditable across upgrades.

4. **Record a decision before merge**  
   No collision should merge into governed state without an explicit decision.

5. **Keep review artifacts separate from the live Record**  
   Proposals, decisions, and diffs are governance objects, not replacements for durable truth surfaces.

### Examples of upgrade collisions

- a template upgrade changes default pedagogy, but the instance has already reviewed and approved a different pedagogy profile
- a template upgrade changes memory-governance expectations, but the instance has existing reviewed retention constraints
- a template upgrade introduces a stronger safety boundary that should be staged, reviewed, and then merged according to local doctrine

### Buffer rule

A template may evolve faster than an instance should merge.

Change review is the buffer that protects instance coherence.

---

## New safeguards (v2026-03)

- Before large Record-affecting changes, run **`node scripts/gate-guardian.js`** (or `CI=true` / `--yes` only when you intentionally bypass the interactive prompts in automation).
- Run **`node scripts/validate-template.js`** after merges; it chains **`python3 scripts/validate-record-boundaries.py`** (opt-in frontmatter on `users/**/*.md`) and **`python3 scripts/layer-enforcer.py`** (forbidden paths from **`docs/layer-map.json`**).
- **Protected surfaces (conceptual):** durable truth lives under **`users/<id>/`** as files such as **`self.md`**, **`self-evidence.md`**, **`self-identity.md`**, **`self-knowledge.md`**, **`self-personality.md`** — not as a generic `Record/` directory inside `users/`. Personality in scaffold terms maps to **`self-personality.md`** / IX-C in the instance protocol; do not invent parallel directory trees that duplicate those files.
- Optional: **`python3 scripts/truth-density-score.py`** (heuristic; documents **`must-persist`** convention in tension doc) and **`node scripts/generate-provenance.js`** (writes gitignored **`state/provenance/record-docs-summary.json`**).

