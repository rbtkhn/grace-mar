# K-12 schools — technical MVP (companion-self type)

**Purpose:** Minimum school-specific glue on top of existing grace-mar / companion-self instance model. See [k12-schools-pilot-playbook.md](k12-schools-pilot-playbook.md). **Colorado targeting:** [k12-schools-colorado.md](k12-schools-colorado.md).

---

## MVP scope

| In scope | Out of scope (MVP) |
|----------|-------------------|
| Per-student `users/<student_id>/` tree | Deep SIS grade passback |
| Roster-driven provisioning | Full SSO (optional phase 1.5) |
| Org id + admin roster list | District-wide RFP automation |
| Merge authority policy (documented) | Custom LMS plugins |
| Bulk export per cohort | Real-time analytics dashboard |

---

## 1. Roster provisioning

| Approach | MVP |
|----------|-----|
| **Input** | CSV: `student_id, display_name, grade, parent_email, merge_authority_role` (or minimal: id + name) |
| **Process** | Script or operator run: copy `users/_template/` → `users/<org_slug>_<student_id>/` (or `users/<student_id>/` with org in metadata) |
| **Bind Voice** | Telegram: parent links child bot session per onboarding doc; or school-issued invite |
| **Idempotency** | Re-run safe: skip if user dir exists |

**Existing anchors:** [companion-self-developer-plan.md](companion-self-developer-plan.md), `users/_template/`.

---

## 2. Admin (minimal)

| Function | MVP |
|----------|-----|
| **Roster view** | Markdown or simple HTML: list instances + pending gate count per student |
| **Health** | `harness_warmup.py` per user or batch script |
| **Support** | Operator SSH / git access to instance repo (hosted pilot) |

No multi-tenant SaaS dashboard required for first pilot if operator-managed.

---

## 3. Merge authority policy

| Policy | When to use |
|--------|-------------|
| **Parent-only** | Homeschool-heavy microschool; COPPA clarity |
| **Educator-only** | School asserts official Record; parent read-only export |
| **Dual** | Either may approve; dedupe in gate review |

**Implementation:** Document in DPA + pilot SOW. Technically same RECURSION-GATE; **who** changes `status: approved` is procedural (parent Telegram vs educator Cursor).

---

## 4. Bulk export

| Export | Command / artifact |
|--------|-------------------|
| **PRP per student** | `scripts/export_prp.py -u <id> -o <out>/<id>-llm.txt` |
| **Identity markdown** | `scripts/export_user_identity.py --user <id>` |
| **Full fork** | `scripts/export_fork.py` per user (heavy) |
| **Batch** | Shell loop over roster list; zip for school DPA-governed download |

**Existing:** [portability.md](portability.md), [using-grace-mar-without-a-school.md](using-grace-mar-without-a-school.md).

---

## 5. Post-MVP (pilot 2+)

- OAuth / Google Classroom roster read
- Web Voice surface + school SSO
- Automated pipeline apply after educator approval in Mini App
