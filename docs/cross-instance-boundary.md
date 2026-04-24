# Cross-instance boundary (grace-mar and external companions)

**Purpose:** One-page contract for **collaboration without merging Records** — especially when one operator works in grace-mar and a peer companion has a **separate instance repository** created from [companion-self](https://github.com/rbtkhn/companion-self).

**Authority:** Complements [fork-isolation-and-multi-tenant.md](fork-isolation-and-multi-tenant.md), [identity-fork-protocol.md](identity-fork-protocol.md), and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md).

---

## 1. Two repositories, two roles

| Repository | Holds |
|------------|--------|
| **grace-mar** (mentor / operator) | `users/grace-mar/` Record, work territories (e.g. collaborative **work-cici** module), template sync tooling. |
| **Peer instance** (e.g. employee’s repo) | **Her** `users/<fork_id>/` tree, **her** gate, **her** merge script — not a subtree inside grace-mar. |

“Similar companion-self type agents” here means: **same protocol**, **different forks**, **different repos** unless you explicitly choose otherwise.

---

## 2. What must not cross without the peer’s gate

- **Mentor Record facts** (SELF, EVIDENCE, prompt) must not appear in the peer’s **canonical** profile files as if they were hers without **her** recursion-gate and `process_approved_candidates.py --apply` (or equivalent).
- **Undocumented LLM knowledge** — same [knowledge boundary](knowledge-boundary-framework.md) as grace-mar; nothing becomes her Record without write + approval.

**Collaborative work modules** (advisor runbooks, mirrors, client WORK docs) live in **mentor** or **shared docs** by agreement; they are **not** her `self.md`.

---

## 3. What may cross

- **Template upgrades** from companion-self into **each** repo on its own schedule.
- **Workflow patterns** (checklists, mirror contracts) as **WORK** artifacts.
- **Pointers** (“see mentor repo PR #…”) without pasting mentor identity blocks.

---

## 4. Mechanical backstop (optional)

Run this **only in the peer’s instance repository**, not in grace-mar. Under `users/` in grace-mar, the mentor fork id appears legitimately everywhere; the same scan would raise noise.

To catch accidental paste of the **mentor fork path** into **her** tree, run from **her** repo root:

```bash
python3 scripts/check_forbidden_path_strings.py --preset isolate-external-instance --under users
```

Script: [scripts/check_forbidden_path_strings.py](../scripts/check_forbidden_path_strings.py). The preset forbids the literal substring `users/grace-mar/` anywhere in scanned files — appropriate when **no** file under **her** `users/` should reference the mentor’s profile directory.

Scans **`users/`** by default when `--under` is omitted and `users/` exists. Add `--under docs` only with `--exclude` patterns for docs that must quote paths literally.

grace-mar can keep the script so operators copy it into her repo or pull from template; **do not** wire CI on grace-mar `main` with this preset across the whole `users/` tree without a different scope.

---

## 5. Two-person scale

With **one other person**, prefer **explicit habits** over heavy automation: who runs merges on her fork, where Session 0 capture lives, and one recurring leakage check (§4) if she uses CI or pre-commit.

---

**Related:** [audit-boundary-grace-mar-companion-self.md](audit-boundary-grace-mar-companion-self.md), [skill-work/work-cici/README.md](skill-work/work-cici/README.md), [inter-fork-collaboration.md](inter-fork-collaboration.md).
