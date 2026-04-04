# Xavier — two steps: your project on GitHub + open in Claude Code

**Audience:** Xavier — **day one only.**  
**Territory:** WORK in grace-mar (operator sends this page). Her **instance** files live **in her own GitHub project**, not here.

This page does **one** thing: help you **create** that project and **open it** on your computer. **Seed Phase**, surveys, validation commands, and Session 0 come **next**, with Robert — **not** something you finish alone tonight.

**Template (starting point):** [companion-self on GitHub](https://github.com/rbtkhn/companion-self) — the **template** Robert uses. Your copy becomes **your** project (often named something like `companion-xavier`).

---

## Before you start (Robert checks)

- The **companion-self** repository must be set as a **Template repository** on GitHub (**Settings** → enable **Template repository**), so the green **Use this template** button appears. Official steps: [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) (GitHub Docs). If Xavier does not see **Use this template**, Robert should confirm that setting first.
- Agree a **project name** (example: `companion-xavier`) and whether it should be **Private** or **Public**.

---

## Step 1 — Create **your** project on GitHub

1. Sign in to **your** GitHub account.
2. Open: **https://github.com/rbtkhn/companion-self**
3. Click **Use this template** (not “Fork”).
4. Choose **Owner:** your account. **Repository name:** what you agreed with Robert (example: `companion-xavier`). **Private** is fine.
5. Leave **Include all branches** off unless Robert tells you otherwise.
6. Click **Create repository from template**.

You now have **your** copy. It is **not** the grace-mar project and **not** a copy of someone else’s live identity files.

**Do not:**

- Fork or copy **grace-mar** to get your instance.
- Copy anything from **`users/grace-mar/`** (or any other person’s user folder) into your project.

**Why:** Your identity in this system is built through **your** Seed Phase and approvals — not by pasting another person’s files. Details: [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md) (operator language is OK; the rule is simple: **your project, your folders**).

---

## Step 2 — Download the project and open it in Claude Code

1. On **your** new repository page on GitHub, copy the **HTTPS** address. It looks like:  
   `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git`
2. On your computer, open **Terminal** (Mac) or **Command Prompt / PowerShell** (Windows).
3. Go to the folder where you keep projects, for example:  
   `cd Desktop`  
   (or another folder you prefer)
4. Run (paste **your** URL):  
   `git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git`  
   `cd YOUR-REPO-NAME`
5. Open **Claude Code** and **open this folder** as the project (the folder you just cloned — this is **your** working copy).

If **git clone** fails or you have never used Terminal before: pause and **screen-share with Robert** — that is normal.

Official help (optional): [Cloning a repository (GitHub Docs)](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

---

## What happens next

When this folder is open in Claude Code, **stop for day one** unless Robert asks for one more tiny check.

**Next working session(s):** Seed Phase and Session 0 follow the **template’s** docs **inside your project**, with Robert guiding — same idea as [first-good-morning-runbook.md](first-good-morning-runbook.md) (first load and safe setup). **Where** your files will live (paths like `users/xavier/`, surveys): [INSTANCE-PATHS.md](INSTANCE-PATHS.md).

---

## Revision log

| Date | Note |
|------|------|
| 2026-04-04 | Initial two-step sheet: GitHub template + clone + open in Claude Code; Seed Phase deferred. |
| 2026-04-04 | Linked GitHub Docs: [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) for operator preflight. |
