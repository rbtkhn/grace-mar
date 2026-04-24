# Portability — Record Transfer And Runtime Portability

**Purpose:** Document how the Record moves with the companion when they change schools, and how Grace-Mar can be moved between runtimes without giving up canonical ownership. The Record belongs to the companion; schools and runtimes consume exports.

**See also:** [OPENCLAW-INTEGRATION](openclaw-integration.md) (runtime adapter example), [ARCHITECTURE](architecture.md) (Record structure).

---

## 1. Core Principle

**The Record is companion-owned.** self.md, skills.md, self-evidence.md live under the companion's control — in a repo, on a family machine, or in a hosted instance the companion controls. Schools do not own the Record. They read it (or receive exports). When the companion switches schools, they bring their Record. There is no "transfer" between institutions — only a change in who receives access or an export.

**Runtime portability is separate from school transfer.** A runtime such as OpenClaw, Cursor, Codex, Claude Code, or a future local harness may consume exported Grace-Mar surfaces, but it does not become the system of record. Grace-Mar remains canonical; the runtime is an adapter.

### Portable lanes

Grace-Mar exports can package four distinct lanes:

| Lane | Meaning | Canonical? |
|------|---------|------------|
| **record** | identity, skills, evidence, library, PRP | Yes |
| **runtime** | warmup, `self-memory.md`, session continuity aids | No |
| **audit** | event logs, merge receipts, checksum/freshness surfaces | Append-only operational history |
| **policy** | intent rules and machine-readable alignment surfaces | Canonical policy, not identity |

Do not confuse these lanes. The `runtime` lane may travel with a harness for continuity, but it must remain labeled non-canonical.

Runtime memory plugins belong here too: if a downstream runtime uses Hindsight-style retain/recall, that memory is portable only as part of the `runtime` lane and must not be mistaken for Record truth.

---

## 2. Transfer Workflow (Checklist)

When switching from School A to School B:

| Step | Action |
|------|--------|
| 1 | **Export the Record** (see §3). Run `export_user_identity` and/or `export_fork` depending on what the new school needs. |
| 2 | **Provide to School B.** Send the export file(s) or grant access (e.g., repo URL, shared folder) per School B's process. |
| 3 | **Revoke access at School A** (see §4). Remove shares, tokens, or integrations. The Record stays with you; School A no longer has access. |
| 4 | **Confirm School B has it.** Verify they received the export or can read the Record. |
| 5 | **Continue the pipeline.** Keep staging and merging through RECURSION-GATE as before. School B's events can feed the pipeline via "we did X" if applicable. |

---

## 3. Handoff Format

What the companion gives to the new school depends on integration depth.

| Use case | Contents | How to produce |
|----------|----------|----------------|
| **Identity only** | Interests, personality, values, IX-A/B/C, linguistic style | `python scripts/export_user_identity.py -u grace-mar -o handoff-identity.md` |
| **Full fork** | SELF, EVIDENCE, SKILLS, LIBRARY | `python scripts/export_fork.py -u grace-mar -o handoff-fork.json` |
| **Runtime bundle** | Record + policy + optional runtime/audit lanes for a downstream harness | `python scripts/export_runtime_bundle.py -u grace-mar -o handoff-runtime-bundle` |
| **Emulation-ready bundle** | Runtime bundle + PRP + fork export + authority map + change-proposal return contract | `python scripts/export.py emulation -- --mode portable_bundle_only -o handoff-emulation-bundle` |
| **Light handoff** | Identity + SKILLS summary | Run `export_user_identity`; optionally append SKILLS container status (edges, gaps) from skills.md |

**Recommended default:** Identity export (`export_user_identity`) is sufficient for most schools (Alpha/Incept, tutors, onboarding). Use full fork when the school needs full evidence history.

### Runtime modes

Runtime portability may be exported in one of three declared modes:

| Mode | Meaning |
|------|---------|
| **`adjunct_runtime`** | Another runtime assists the canonical repo; light continuity only |
| **`primary_runtime`** | Another runtime is the main live surface; richer continuity/audit export |
| **`portable_bundle_only`** | Produce a transport package without assuming a live runtime |

These modes change packaging and review rhythm only. They do **not** alter the Sovereign Merge Rule.

### Emulation bundle vs membrane bundle

Use the **emulation-ready bundle** when a foreign runtime needs a broad governed package to load Grace-Mar behavior under the existing export contract:

- PRP for prompt/bootstrap loading
- fork export for machine-readable inspection
- runtime bundle lanes for policy/runtime continuity
- explicit return references for `change-proposal.v1.json` and membrane imports

Use the **runtime-complements membrane bundle** when you want a narrow, allow-listed runtime context exchange:

- `scripts/runtime/export_runtime_context.py`
- `scripts/runtime/import_runtime_observation.py`

That membrane path is smaller on purpose. It is for bounded runtime exchange, not full emulation-oriented loading.

For the concentrated contract and behavior-spec layer around this bundle, see [portability/emulation/README.md](portability/emulation/README.md).

---

## 4. Revocation Guidance

**If the school had file access (repo, shared drive):**
- Remove the school's access to the repo or folder.
- Rotate any shared credentials if applicable.

**If the school had an export file:**
- There is no technical revocation; the file is a snapshot. Inform School A that they should delete their copy and no longer use it. The canonical Record remains with the companion.

**If using a future API/token model:**
- Revoke the token or disconnect the integration for School A.

---

## 5. Version and Compatibility

Exports include a generation timestamp. The Record schema (SELF, SKILLS, EVIDENCE structure) is documented in [ARCHITECTURE](architecture.md). Schools consuming exports should tolerate extra fields and ignore unknown ones.

---

## 6. File Map

| File | Role in transfer |
|------|------------------|
| `users/[id]/self.md` | Identity, interests, personality, IX-A/B/C |
| `users/[id]/skills.md` | THINK and WRITE Record skill status |
| `users/[id]/self-evidence.md` | Activity log (full fork export only) |
| `users/[id]/self-memory.md` | Runtime continuity only; not canonical identity |
| `users/[id]/runtime-bundle/` | Portable package for downstream runtimes; includes record/runtime/audit/policy lanes |
| `users/[id]/emulation-bundle/` | Emulation-oriented wrapper over the existing runtime bundle plus proposal/membrane return references |
| `users/[id]/pipeline-events.jsonl` | Audit trail for staging, merge, validation, export |
| `users/[id]/merge-receipts.jsonl` | Merge provenance and approval replay |
| `scripts/export_user_identity.py` | Produce identity handoff |
| `scripts/export_fork.py` | Produce full fork handoff |
| `scripts/export_runtime_bundle.py` | Produce runtime-neutral portability bundle |
| `scripts/export_view.py` | School/public views with redaction (see privacy-redaction.md) |

---

*Document version: 1.0*
*Last updated: February 2026*
