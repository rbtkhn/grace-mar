# Cici — Phase 1 implementation prompt (Git-first governed state)

**Purpose:** Instruction prompt for implementing **Phase 1** in the **[Xavier-x01/Cici](https://github.com/Xavier-x01/Cici)** repository — migration toward **GitHub-native, file-centric, local-first** operation, inspired by **companion-self**, without reckless rewrite.

**Source:** Operator PDF export `Implement Phase 1 Git-first governed state foundation.pdfs=1.pdf` (saved here as markdown for version control). **Instruction text only** — agent execution transcript after the prompt is omitted.

**Outcome (reference):** Implemented on Cici `main` ([`6379661`](https://github.com/Xavier-x01/Cici/commit/6379661)); see repo [README](https://github.com/Xavier-x01/Cici#governed-state-model-phase-1) and [`docs/governed-state-doctrine.md`](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md).

---

You are working inside the GitHub repository for **Cici**. Your job is to implement **Phase 1** of a migration that makes this project significantly more **GitHub-native**, **file-centric**, and **local-first**, inspired by the structure and philosophy of **companion-self**, while preserving Cici’s strongest existing capabilities.

This is a **careful transition**, not a reckless rewrite.

## Core goal

Transition Cici from a system whose durable memory depends primarily on hosted **Supabase/Postgres** state into a system where:

- **Git-managed files** are the canonical source of truth for **durable governed state**
- **Local-first** operation is the default direction
- **Supabase** remains supported, but becomes an **optional operational bridge**
- Important durable changes happen through **proposals and review**, not silent direct writes
- The repo becomes more **forkable**, **inspectable**, and **template-like**

Do not try to complete the full migration in one pass. Implement only the **smallest credible Phase 1 foundation**.

## Non-negotiable constraints

- Implement **only Phase 1** in this pass.
- Preserve **all** currently working functionality unless absolutely necessary to change.
- **Do not** remove Supabase support.
- **Do not** break current setup for existing users.
- **Do not** do large file moves unless clearly necessary for Phase 1.
- Prefer **additive** changes over destructive changes.
- Prefer **repo-native** naming and conventions where they already exist.
- Keep the migration legible to a **non-technical owner**.
- Use **GitHub-native** mechanisms wherever practical: files, schemas, validation, Actions, review artifacts, explicit manifests.
- **Do not** over-engineer. Build the minimal foundation that proves the architectural direction.

## What must be preserved

Cici may already have valuable strengths. Do not undermine them. Preserve and respect:

- Memory capture / ingestion flows
- MCP-related capabilities, if present
- Fingerprint deduplication, if present
- Multi-AI / gateway architecture, if present
- Recipes / skills / primitives / schemas where they are already useful
- Vector capabilities, if present
- Dashboards and backend compatibility, even if they remain partially Supabase-oriented for now

The point is **not** to discard working memory infrastructure. The point is to make it **subordinate** to a Git-governed durable state model.

If any of the above are absent in Cici, adapt to the **actual** repository structure rather than forcing Open Brain / Xavier assumptions onto this codebase.

## Architectural direction

You are aiming toward this model.

### Canonical layers

| Layer | Meaning |
|-------|---------|
| **Evidence** | Raw or source-adjacent imports |
| **Prepared context** | Normalized, transformed, deduplicated, staged context |
| **Governed state** | Durable approved state that becomes part of the instance’s long-term truth |

### Source-of-truth rule

- **Git-managed governed state** is canonical.
- Operational databases/services are **derivative** and optional.
- Supabase may continue to support search, indexing, auth, sync, dashboards, and acceleration — but Supabase **must not** be treated as the **sole** durable truth going forward.

### Change rule

- Important durable updates should become **proposal artifacts**.
- Proposals should move through a **review queue**.
- Approved changes can then update **governed state**.

### Template rule

- The repo should begin moving toward a **template vs instance** model — but **do not** fully redesign the whole project in this pass.

## Phase 1 deliverables

You must implement a **minimal but real** Phase 1 that includes the following.

### A. Repository audit

Inspect the current repository first and summarize:

- Current top-level structure
- Where Supabase is central today, if anywhere
- Where file-based state already exists
- Where memory, schemas, dashboards, and operational layers currently live
- The least disruptive insertion points for a Git-first governed-state layer

Do this audit **before** making major changes.

### B. A new governed-state scaffold

Add a minimal **file-based** governed-state structure. Use existing naming conventions where sensible, but aim for a conceptually clear scaffold **like**:

- `evidence/`
- `prepared-context/`
- `users/_template/`
- `users/demo/` or another minimal example instance if appropriate
- `users/<instance>/...` for governed state surfaces
- `config/` or another suitable place for authority / runtime doctrine
- `bridges/supabase/` if that fits naturally
- `.github/workflows/` additions if validation is added

Do **not** force these exact names if the repo already has a better convention. But you must create a clear file-based home for the **three-layer** state model.

At minimum, the structure should make it possible to distinguish:

- Raw **evidence**
- **Prepared context**
- **Approved durable state**

Add short README files in new directories where that helps explain purpose.

### C. A short doctrine file

Create a concise doctrine / architecture document explaining:

- Git-managed governed state is **canonical**
- Operational services/databases are **derivative**
- Evidence and prepared context may be **staged** or **cached**
- Durable state should change through **governed review**
- Supabase remains supported as an **optional operational bridge** during migration

Short, crisp, **constitutional** tone — not a bloated manifesto.

Possible filenames: `docs/governed-state-doctrine.md`, `docs/architecture/governed-state.md`, or the nearest repo-native equivalent.

### D. Proposal artifacts for material durable changes

Create a structured artifact format for **material** changes to governed state. Prefer **JSON** if the repo already uses structured schemas heavily.

Include fields **like**: `id`, `created_at`, `status`, `change_type`, `target_surface`, `summary`, `rationale`, `evidence_refs`, `proposed_diff_summary`, `confidence`, `proposer`, `reviewer`, `decision_notes`.

Support a lifecycle **like**: `proposed`, `under_review`, `approved`, `rejected`, `deferred`, `superseded`.

Create:

- One **schema** for proposals
- One or two **example** proposal files
- Brief **documentation** for how proposals work

### E. A lightweight review queue

Create the lightest viable review queue that makes proposals **inspectable in Git**. This can be folder-based, index-based, or a combination.

The owner should be able to tell:

- What is awaiting review
- What was approved
- What was rejected
- What changed and why

Do **not** build a giant workflow engine. Keep it simple and inspectable.

### F. A seed-phase foundation

Implement the foundation of a formal **Seed Phase**. Do not fully rebuild the entire onboarding experience unless easy — but establish the pattern clearly.

At minimum:

- Add a `docs/seed-phase.md`
- Define what Seed Phase means **in this repo**
- Create one or more seed artifacts, such as: `seed_intent.json`, readiness check placeholder(s), validation script(s)
- Make clear that new instances should be initialized through **Seed Phase**, not by copying real user data

If it fits the repo naturally, create: `users/_template/`, a minimal demo or sample instance scaffold, a simple validation or readiness script.

### G. A minimal authority-map stub

Create a lightweight authority model that distinguishes:

- **Canonical** human-controlled governed state writes
- **Proposal-only** writes by agents or automations
- **Operational** / cache / index writes
- **Ephemeral** runtime state

JSON, YAML, or Markdown depending on repo style. Does not need to be elaborate — must establish the **boundary**.

### H. Validation / CI

Add **lightweight** validation for the new governed-state artifacts. Prefer existing tooling if present. Examples:

- JSON schema validation
- Folder structure checks
- Proposal status validation
- Seed artifact validation

Add or extend **GitHub Actions** if appropriate so malformed governed-state artifacts **fail validation**. Keep this minimal and maintainable.

### I. Documentation updates

Update the docs so the repo begins to communicate this new direction clearly. At minimum:

- README or architecture docs should explain that the project is moving toward **Git-first governed state**
- Supabase should be described as **supported but non-canonical**
- Imports / capture / memory flows should be conceptually reframed where appropriate as: evidence → import → normalization → prepared context → proposal generation → optional approval into governed state

Do **not** rewrite every doc in the repo. Touch only the docs necessary to establish the model.

### J. Migration and compatibility notes

If appropriate, add a short migration-oriented note or file that explains:

- Existing Supabase-backed users are still supported
- The new file-based governed-state layer is **additive** in Phase 1
- Later phases may expand local-first defaults

Do not overcommit to Phase 2 implementation details. Clarify compatibility and direction.

## Specific guidance on Supabase

- **Do not** remove Supabase.
- **Do not** disable working Supabase flows.
- **Do not** rewrite dashboards to eliminate Supabase in this pass unless a small compatibility improvement is trivial.

Instead, reposition Supabase conceptually and structurally as:

- An **optional bridge**
- A useful operational layer for search / index / auth / sync / UI
- **Not** the canonical source of governed truth

If suitable, create a surface like `bridges/supabase/` or document the bridge concept cleanly without excessive code movement.

If Cici does not use Supabase centrally, adapt this guidance to whatever hosted or database layer it actually uses.

## Specific guidance on repository restructuring

You may propose a more companion-self-like top-level layout, but **do not** perform a massive reorganization during Phase 1.

If restructuring is needed:

- Keep it **minimal**
- Explain old → new mapping clearly
- Avoid churn
- **Do not** move major working subsystems just for aesthetic symmetry

You may add new top-level folders where needed for the governed-state foundation, but avoid **broad repo surgery**.

## Preferred execution order

1. **Audit** — Inspect the current repo; summarize architecture and insertion points.
2. **Propose minimal Phase 1 layout** — Show exact new directories/files to add or minimally modify.
3. **Implement governed-state scaffold** — Evidence / prepared-context / governed-state file surfaces in the most natural repo-native way.
4. **Implement doctrine + authority model** — Short doctrine file and authority-map stub.
5. **Implement proposal schema + examples + review queue** — Proposal artifact model and lightweight review queue.
6. **Implement seed-phase foundation** — Docs, template/seed artifacts, minimal readiness validation.
7. **Add validation / CI** — Lightweight checks.
8. **Update key docs** — New direction and compatibility model.
9. **Summarize changes** — What changed, why it matters, what remains for later phases, risks.

## Anti-goals

Do **not**:

- Rip out Supabase
- Convert the whole system into unstructured markdown notes
- Force every tiny memory write through heavy ceremony
- Replace working fast retrieval with naive file scanning everywhere
- Redesign every dashboard/backend surface in one pass
- Produce only an abstract plan without actual file/code changes
- Invent unrelated features
- Do a full repo reorganization just to mimic companion-self cosmetically

## Output / reporting requirements

Work **directly** in the repository.

**Before** major implementation:

- Inspect the repo
- Summarize the current structure
- Identify the best insertion points
- Show the minimal Phase 1 file/folder plan

Then proceed with implementation.

**After** each major phase, show: files added, files modified, short explanation of why.

**At the end**, provide:

- Repository audit summary
- Architectural choices made
- Files added / modified
- Validation / CI changes
- Compatibility notes
- Phase 2 recommendations
- Any breaking changes or risks

Where practical, include full content for small new files and focused code snippets for modified files.

Be **disciplined**, **incremental**, and **concrete**. Build the **smallest credible Phase 1 foundation** for a Git-first, governed, local-first Cici.
