# Merging Upgrades from Companion-Self (Template → Instance)

**Purpose:** Grace-Mar is an **instance**; companion-self is the **template** repo. When the template is updated (concept, protocol, seed, schema), this doc describes how to pull those changes into grace-mar without overwriting the Record. See [COMPANION-SELF-BOOTSTRAP](../COMPANION-SELF-BOOTSTRAP.md) §5 for the contract.

**Workspace boundary:** All grace-mar modifications—including merges from companion-self—are done in **this (grace-mar) workspace**. Do not edit grace-mar from a companion-self workspace; there, grace-mar is read-only reference. When you perform the merge checklist below, you are in the grace-mar workspace; companion-self is pulled or opened for reference only. See companion-self [COMPANION-SELF-BOOTSTRAP](https://github.com/rbtkhn/companion-self/blob/main/COMPANION-SELF-BOOTSTRAP.md) §7.

---

## 1. Template paths (safe to sync)

These paths in companion-self are the canonical source for shared concept, protocol, and schema. Grace-mar keeps its own copies and updates them to match the template when upgrading. **When companion-self adds or renames files, update this list.**

| Path | Description |
|------|-------------|
| `docs/CONCEPTUAL-FRAMEWORK.md` | Concept: Record, Voice, cognitive fork, knowledge boundary |
| `docs/ARCHITECTURE.md` | System design, fork lifecycle, seeding |
| `docs/IDENTITY-FORK-PROTOCOL.md` | Protocol: stage → approve → merge; evidence linkage |
| `docs/SELF-TEMPLATE.md` | SELF module schema and governance |
| `docs/SKILLS-TEMPLATE.md` | SKILLS module schema |
| `docs/EVIDENCE-TEMPLATE.md` | EVIDENCE module schema |
| `docs/MEMORY-TEMPLATE.md` | MEMORY schema and scope |
| `AGENTS.md` | Template-level governance (pipeline rule, knowledge boundary, operating modes) |
| Seed-phase definition | In companion-self: docs or README section describing seed phases; in grace-mar: reflected in ARCHITECTURE and OPERATOR-BRIEF |

**Never overwrite with template:** `users/grace-mar/` (the Record), instance-specific bot/config (e.g. Telegram token, render.yaml), PRP output paths (e.g. grace-mar-llm.txt). Instance-only docs (e.g. PROFILE-DEPLOY, NAMECHEAP-GUIDE, OPERATOR-WEEKLY-REVIEW) stay in grace-mar unless you explicitly promote them to the template.

---

## 2. Merge checklist

Use this when you have updates in companion-self that should flow into grace-mar.

| Step | Action |
|------|--------|
| 1 | **Get template state** — Clone or pull companion-self (e.g. `git clone https://github.com/rbtkhn/companion-self.git /tmp/companion-self` or open in a sibling directory). Note the commit or tag you're syncing from. |
| 2 | **Diff template paths** — For each path in §1 that exists in companion-self, compare with grace-mar's copy. `diff -r` or a script (see §4) can help. |
| 3 | **Merge into grace-mar** — For each path where the template is ahead, copy or merge changes into grace-mar's file. Resolve any instance-specific additions in grace-mar (keep them). Do **not** overwrite `users/grace-mar/` or instance config. |
| 4 | **Validate** — Run `python scripts/validate-integrity.py` (or equivalent). Run governance check if applicable (e.g. `scripts/governance_checker.py`). Fix any breakage. |
| 5 | **Log the sync** — Record in §3 (Template sync log) the date, companion-self commit/tag, and paths updated. |

---

## 3. Template sync log

Record each merge from template so you can see when grace-mar was last updated and what changed.

| Date | Companion-self (commit or tag) | Paths updated |
|------|---------------------------------|---------------|
| *(none yet)* | — | — |

---

## 4. Future: optional diff script

When companion-self has stable content, a small script could:

- Accept two roots (companion-self and grace-mar) and a list of template paths.
- Report which paths differ (and optionally show a short diff).
- **Not** overwrite anything; operator still performs the merge.

Placeholder: `scripts/template_diff.py` or similar, to be added when useful.

---

## 5. Related

- **COMPANION-SELF-BOOTSTRAP.md** §5 — Contract: safe to sync, never overwrite, process.
- **OPERATOR-WEEKLY-REVIEW.md** — Optional step: periodic template sync when template or instance change.
- **AGENTS.md** — Template-level rules; when updated in companion-self, sync into grace-mar per this doc.
