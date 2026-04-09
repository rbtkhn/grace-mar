# Git branch hygiene (operator)

**Purpose:** A **small, repeatable** check so you do not lose track of branches or confuse **“merge into main”** with **Record gate merge**. This doc supports the [coffee](../../../.cursor/skills/coffee/SKILL.md) **branch snapshot** (work-start and signing-off **coffee** Step 1; legacy **hey** still works) and **coffee menu E — git/ship** (repository hygiene — full pass when that steward sub-track is chosen).

**Not the same as coffee menu E — Steward (template/boundary).** **E** = template + boundary audit (grace-mar vs companion-self, fork isolation, reconciliation code). **Branch hygiene** = **local git** pointers (`main` vs feature branches) — different job.

---

## When you merge branches (git)

Merge a **git branch** when that line of work should **become part of `main`** (or your chosen target branch) and is **ready** (reviewed, tested if you care, not half-finished).

You do **not** merge every day by habit — you **triage** often; you **merge** when a unit of work is done.

**Different from Record:** Merging **candidates** into **SELF/EVIDENCE** uses **RECURSION-GATE** + `process_approved_candidates.py` — companion approval. **Git merge** is **repo history** only.

---

## Branch snapshot (what the agent runs for you)

**Commands (read-only):**

```bash
git status -sb
git branch -vv
```

**Plain-language rules:**

| What you see | Meaning | Typical action |
|--------------|---------|----------------|
| Only `* main` and `main` tracks `origin/main` | No extra branches | **None** — say “branch hygiene: clean.” |
| Branch listed, `[gone]` or already contained in `main` | **Stale** — work is on `main` already | **Delete** local (and remote if it still exists): `git branch -d name` then `git push origin --delete name` if needed. |
| Branch with commits **not** on `main` | **Active or parked** work | If **done** → merge via PR or `git merge` then push. If **not done** → leave; optionally `git merge main` into it so it stays current. |
| Dirty `main` (modified files) | Uncommitted work | **Not** a branch problem first — commit, stash, or discard per your lane; handoff script already flags this. |

If you are unsure, the **prescription** is: **one sentence** — “No action,” “Delete branch X (merged),” or “Finish or merge branch Y when ready.”

---

## Fit in coffee (work-start and signing-off)

- **Work-start coffee:** After warmup scripts (and lighter cadence when applicable), agent runs the snapshot and gives **one short paragraph** unless only `main` exists and clean.
- **Closeout coffee:** Same snapshot after `operator_handoff_check.py` when useful; pairs with **menu D** or **B** if you want to **execute** deletes/merges that session.

**Guardrail:** Snapshot is **read-only** in Step 1. Actually **merging or deleting** branches is **ship** work — do it when you choose **D** or leave the session and run git yourself.

---

## See also

- [session-continuity-contract.md](session-continuity-contract.md) — continuity is not agent memory.
- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) — Record export / gate merge loop (not git branch merge).
