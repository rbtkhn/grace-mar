# COMPANION-SELF BOOTSTRAP

**Use this file in the companion-self repo workspace.** Copy this file into the root of your new companion-self repository, open that repo in a new Cursor workspace, then open this file and say: *"Read companion-self-bootstrap.md and set up this repo as the companion-self template per the plan."* The agent will have full context to continue.

**In grace-mar:** This file is a copy of the bootstrap used in the companion-self repo. The template repo exists at [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self). For the latest audit of grace-mar (instance) vs this template, see [docs/audit-grace-mar-vs-companion-self-template.md](docs/audit-grace-mar-vs-companion-self-template.md).

---

## 1) What This Repo Is

**Companion-self** = the **template** repo. **Grace-Mar** = the **instance** repo (first and currently only instance).

- **Template:** Concept, protocol, seed-phase definition, and structure for creating a new companion self. No one's Record; no pilot data.
- **Instance:** One live companion self (Record, bot, pipeline). Created from the template when a **new user completes seed phase**.
- **Creation rule:** A new companion self is **initiated only by a new user via seed phase**. No copying another repo's `users/`; no pre-filled Record.

**Domains:** companion-self.com = concept/product (this template). grace-mar.com = the first instance (profile, bot, PRP).

---

## 2) Why Two Repos

- **Different sovereigns:** Template = product/concept steward. Instance = companion and operator.
- **Different lifecycles:** Template changes slowly (protocol, seed design). Instance changes with every pipeline merge and session.
- **Fork semantics:** People fork **companion-self** to create new instances (new user + seed phase). They do **not** fork grace-mar to get a second companion.
- **System development:** Ongoing system development (protocol, schema, seed phases) happens in **companion-self**. Grace-Mar **consumes** upgrades by merging from the template (docs, templates, governance) without overwriting its Record.

---

## 3) What to Create in This Repo (Companion-Self)

### Minimum viable

1. **readme.md**
   - One-line: companion-self = template; grace-mar = first instance.
   - "A new companion self is created when a new user completes seed phase."
   - Link to grace-mar.com and to the grace-mar repo as reference implementation.
   - Optional: link to companion-self.com when the site exists.

2. **docs/** (or single doc)
   - **Concept:** What is a companion self? (Mind + Record + Voice; cognitive fork; sovereign merge; knowledge boundary.) One to three pages. Can be extracted/simplified from grace-mar's `docs/conceptual-framework.md` and `docs/architecture.md`, generalized (no "Abby", no "6-year-old").
   - **Protocol:** Identity Fork Protocol in short form (stage → approve → merge; agent may stage, may not merge; evidence linkage). Can be summarized from grace-mar's `docs/identity-fork-protocol.md`.
   - **Seed phase:** Definition of seed phases (what surveys, what artifacts, what creates initial SELF/SKILLS/EVIDENCE). "New instance = new user + seed phase" as the only creation path. Can be derived from grace-mar's ARCHITECTURE (Fork Lifecycle, Seeding) and OPERATOR-BRIEF.

3. **Optional: users/_template/**
   - Empty or minimal structure: self.md (template only), skills.md (template), self-evidence.md (template), recursion-gate.md (template), memory.md (template). No real data. Used as the scaffold when creating a new user directory in an instance repo. Use companion-self's `users/_template/` or derive from companion-self's schema docs (`docs/self-template.md`, `docs/evidence-template.md`, etc.).

4. **Optional: HOW-INSTANCES-CONSUME-UPGRADES.md** (or section in README)
   - Describe how an instance (e.g. grace-mar) merges upgrades from this template: compare and update docs (CONCEPTUAL-FRAMEWORK, IDENTITY-FORK-PROTOCOL, SELF-TEMPLATE, seed description, AGENTS governance); never overwrite the instance's `users/<id>/` Record. Optionally: list of template paths safe to copy into instances; or a small sync script idea. **Instances:** Use the merge checklist in grace-mar's [merging-from-companion-self.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/merging-from-companion-self.md) when pulling upgrades.

### Optional later

- One-page static site for companion-self.com (concept + link to grace-mar.com).
- Script or checklist: "Initialize new user from seed" (create `users/<new_id>/` from _template, run seed phase steps).
- LICENSE, CONTRIBUTING for the template repo.

---

## 4) What Not to Put Here

- No bot code (lives in instance; grace-mar has the reference implementation).
- No Record data (no SELF/EVIDENCE with real people).
- No instance-specific config (no Telegram token, no grace-mar.com paths). Template is generic.

---

## 5) Merging Upgrades: Template → Instance (Grace-Mar)

When companion-self (template) is updated, grace-mar (instance) can pull those changes without overwriting its Record:

- **Safe to sync from template:** Concept docs, protocol docs, SELF/SKILLS/EVIDENCE *templates* (schema/structure), seed-phase definition, template-level governance (pipeline rule, knowledge boundary). Grace-mar keeps its own copies and updates them to match the template.
- **Never overwrite with template:** `users/grace-mar/` (the Record), instance-specific bot/config, PRP output paths.
- **Process:** Compare template docs/templates with grace-mar's; merge changes into grace-mar's files; run validation (e.g. governance checker, validate-integrity). No automated overwrite of `users/grace-mar/`. Grace-mar's merge checklist: [docs/merging-from-companion-self.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/merging-from-companion-self.md).
- **Optional:** Maintain a list of "template paths" in companion-self (e.g. `docs/conceptual-framework.md`, `docs/self-template.md`) and document in this repo that instances may copy those paths when upgrading.

---

## 6) Key Decisions (Already Made)

- **Template vs instance:** companion-self = template; grace-mar = instance. No "pilot" label; grace-mar is the only instance, identified as `grace-mar` (user id `grace-mar` in grace-mar repo).
- **Creation path:** New companion self = new user + seed phase only. No copy-from-another-instance.
- **System development:** Happens in companion-self; grace-mar consumes via the merge process above.
- **Bootstrap location:** This file can live in grace-mar until the companion-self repo exists; then copy it to the root of companion-self so that opening the companion-self workspace and reading this file gives the agent full context.

---

## 7) First-Run in New Workspace (Agent Instructions)

When the user opens the **companion-self** repo in a new Cursor workspace and invokes you with this bootstrap:

1. **Confirm context:** This repo is the companion-self **template**. The user may have copied this bootstrap from the grace-mar repo. There is no Record here; no `users/grace-mar/`.
2. **Use the developer plan:** Follow the checklist and plan in grace-mar's [companion-self-developer-plan.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/companion-self-developer-plan.md): minimal docs list, source mapping, and phased implementation (README → concept → protocol → seed → optional scaffold and upgrade guide).
3. **Create the minimum:** README (template vs instance; new user + seed phase; link to grace-mar). One or more concept/protocol/seed docs under `docs/` (or a single concept.md). Generalize from grace-mar's concepts; remove instance-specific references.
4. **Optional:** Add `users/_template/` with minimal SELF/SKILLS/EVIDENCE/RECURSION-GATE/MEMORY templates (structure only). Add a short HOW-INSTANCES-CONSUME-UPGRADES or merge section.
5. **Do not** copy the full grace-mar codebase or Record. Only what defines the template: concept, protocol, seed, and optional scaffold.
6. **Propose before implementing:** Per user preference, show a short proposal (scope, files to create) before writing; implement after approval.

---

## 8) Reference: Where to Find Source Material (Grace-Mar)

If you need to extract or generalize content for companion-self, the canonical sources are in the **grace-mar** repo:

- Concept: `docs/conceptual-framework.md`, `docs/architecture.md`
- Protocol: `docs/identity-fork-protocol.md`
- Governance: `agents.md` (template-level rules: pipeline, knowledge boundary, operating modes)
- Seed / lifecycle: `docs/architecture.md` (Fork Lifecycle, Seeding), `docs/operator-brief.md`
- Schema templates: `docs/self-template.md`, `docs/skills-template.md`, `docs/evidence-template.md`, `docs/memory-template.md`
- Modularity (module set, skill-write as voice shaper): `docs/skills-modularity.md`
- Merge process (instance side): `docs/merging-from-companion-self.md` (template paths, merge checklist)
- Instance vs template audit: `docs/audit-grace-mar-vs-companion-self-template.md` (compliance check; use to confirm grace-mar is a valid source before extracting template)

**Naming:** Third skill module is **WORK** in prose; internal identifier remains **BUILD** (container, CREATE-nnn, ACT-nnn). Standard label: **self-skill-work**. When generalizing for the template, use WORK in concept docs.

---

## 9) Continue template analysis (new session)

When resuming in a **new session** and the user says "continue template analysis" (or similar):

- **If you are in the grace-mar workspace:** Re-read [docs/audit-grace-mar-vs-companion-self-template.md](docs/audit-grace-mar-vs-companion-self-template.md). Optionally re-run the audit (structure, protocol, schema paths, governance), update the audit doc for any changes, or extend analysis (e.g. gap deep-dives, template-path diff readiness). Use [docs/companion-self-developer-plan.md](docs/companion-self-developer-plan.md) and [docs/merging-from-companion-self.md](docs/merging-from-companion-self.md) for context.
- **If you are in the companion-self workspace:** Continue from [COMPANION-SELF-DEVELOPER-PLAN](https://github.com/rbtkhn/grace-mar/blob/main/docs/companion-self-developer-plan.md) (grace-mar): next unchecked phase (A1 README → B1 concept → C1 protocol → D1 seed → E1/E2 optional). Use grace-mar as read-only reference; extract and generalize only. Propose scope before implementing.

**Recent context (grace-mar, Feb 2026):** Audit completed (grace-mar compliant). WORK rename applied in docs; SKILLS-MODULARITY formalized (full module set, outputs as f(skill-write)). Landing page desert theme + card. Bootstrap updated for handoff.

---

**End of bootstrap.** Use this file in the companion-self workspace to continue seamlessly.
