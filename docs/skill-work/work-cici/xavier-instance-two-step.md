# Xavier — companion-self instance checklist

**Audience:** Xavier + Robert (operator). **Territory:** WORK in grace-mar (you may send this whole page or only the **Day one** section first).

**Important rule:** **Use the template, not Grace-Mar’s live identity state.**  
Your project is created from [companion-self](https://github.com/rbtkhn/companion-self). Do **not** treat [grace-mar](https://github.com/rbtkhn/grace-mar) or `users/grace-mar/**` as something to copy into your repo.

The [companion-self README](https://github.com/rbtkhn/companion-self) describes **companion-self** as the **template** repo and says a new companion should be formed through **Seed Phase**, not by copying another instance’s `users/` tree or pre-filling a Record.

---

## For Robert first (before Xavier starts)

1. On [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self), open **Settings** and enable **Template repository** so **Use this template** appears.  
   Official steps: [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) (GitHub Docs).
2. Repos created from a template have **unrelated git history** from the template — that is normal and what you want for an **independent** instance (see GitHub’s template docs above and [Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)).
3. Agree with Xavier: repo name (**`companion-xavier`** below), **Private** vs **Public**.

---

## Day one — GitHub + clone + Claude Code (do these first)

1. Go to **https://github.com/rbtkhn/companion-self**
2. Click **Use this template** (not **Fork**).
3. Choose:
   - **Owner:** your GitHub account  
   - **Repository name:** `companion-xavier` (or the name you agreed with Robert)  
   - **Visibility:** **Private** (unless you chose otherwise)  
   - Leave **Include all branches** off unless you specifically want them  
4. Click **Create repository from template**
5. Clone your new project locally:

   ```bash
   git clone https://github.com/<your-username>/companion-xavier.git
   cd companion-xavier
   ```

   Replace `<your-username>` with your GitHub username. If **git clone** fails, screen-share with Robert. Optional: [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) (GitHub Docs).

6. Open **that folder** in **Claude Code** (this is your working copy).

**After step 6, you may stop for the day** unless Robert asks for a small check.

### Tooling — capture, search, RAG, MCP (Open Brain–style)

**Searchable notes** help the assistant remember the *conversation*; **official self** for the Voice only advances through **`recursion-gate.md`** → companion approval → merge script (in **your** repo). **Do not** treat embedding search, vector databases, or MCP auto-writes as a substitute for the gate. **Do not** bulk-import captures into `self.md` or IX as if searchability meant approval.

Map the layers (Open Brain vs Record vs MEMORY vs WORK): [companion-self-for-open-brain-users.md](../work-companion-self/companion-self-for-open-brain-users.md). Three-repo framing: [ALIGNMENT.md](ALIGNMENT.md).

---

## Next — fresh instance, Seed Phase, validation (with Robert)

7. **Start fresh in your own repo only**
   - Do **not** copy `grace-mar/users/...` or Robert’s live Record into your project.  
   - Use the **template** as the starting structure only.  
   - More detail: [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

8. Complete **Seed Phase** in **your** repo (follow the template’s docs — e.g. `docs/seed-phase.md` and related files **inside your clone**).

9. Run the template’s **seed-phase validation** commands from the **companion-self / template README** in your repo (paths like `users/demo/seed-phase` are examples; Robert will help you point validators at **your** user folder when it exists).

10. After Seed Phase is **valid**, use Claude Code **inside your repo** as **your** instance workspace, with **governed** change review (not silent edits to identity files). First-load orientation: [first-good-morning-runbook.md](first-good-morning-runbook.md). Paths cheat sheet: [INSTANCE-PATHS.md](INSTANCE-PATHS.md).

---

## Revision log

| Date | Note |
|------|------|
| 2026-04-04 | Initial two-step sheet: GitHub template + clone + open in Claude Code; Seed Phase deferred. |
| 2026-04-04 | Linked GitHub Docs: [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) for operator preflight. |
| 2026-04-04 | Expanded to full **instance checklist** (10 steps): operator preface, important rule, README framing link, day one vs Seed Phase / validation; `companion-xavier` default name. |
| 2026-04-06 | **Open Brain vs gate:** tooling box after day-one step 6; links to [companion-self-for-open-brain-users.md](../work-companion-self/companion-self-for-open-brain-users.md) and [ALIGNMENT.md](ALIGNMENT.md). |
