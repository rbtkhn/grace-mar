# Portability — Transferring Grace-Mar Between Schools

**Purpose:** Document how the Record moves with the companion when they change schools. The Record belongs to the companion; schools consume it. No institutional handoff — the companion brings their Record.

**See also:** [OPENCLAW-INTEGRATION](openclaw-integration.md) (school integration), [ARCHITECTURE](architecture.md) (Record structure).

---

## 1. Core Principle

**The Record is companion-owned.** self.md, skills.md, self-evidence.md live under the companion's control — in a repo, on a family machine, or in a hosted instance the companion controls. Schools do not own the Record. They read it (or receive exports). When the companion switches schools, they bring their Record. There is no "transfer" between institutions — only a change in who receives access or an export.

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
| **Light handoff** | Identity + SKILLS summary | Run `export_user_identity`; optionally append SKILLS container status (edges, gaps) from skills.md |

**Recommended default:** Identity export (`export_user_identity`) is sufficient for most schools (Alpha/Incept, tutors, onboarding). Use full fork when the school needs full evidence history.

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
| `users/[id]/skills.md` | THINK, WRITE, BUILD container status |
| `users/[id]/self-evidence.md` | Activity log (full fork export only) |
| `scripts/export_user_identity.py` | Produce identity handoff |
| `scripts/export_fork.py` | Produce full fork handoff |
| `scripts/export_view.py` | School/public views with redaction (see privacy-redaction.md) |

---

*Document version: 1.0*
*Last updated: February 2026*
