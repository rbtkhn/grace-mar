# Day 1 (No Terminal) — Xavier

**Rule:** No terminal commands required in this flow.  
**Target session length:** 30-45 minutes.

---

## Step 1 — Open the right docs

Open and read in order:
1. [README.md](README.md)
2. [first-good-morning-runbook.md](first-good-morning-runbook.md)
3. [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md)

---

## Step 2 — Complete Session 0 capture

Open:
- `companion-xavier/docs/seed-survey/seed-survey-initiation.md` (read only)
- `companion-xavier/docs/seed-survey/seed-survey-capture.md` (edit here)

Fill all rows (Q1-Q28) in capture.  
Do not edit initiation file.

---

## Step 3 — Ask Cursor AI to stage candidates (copy/paste prompt)

```text
Help me stage Session 0 outputs safely.

Inputs:
- companion-xavier/docs/seed-survey/seed-survey-capture.md
- companion-xavier/users/xavier/recursion-gate.md

Tasks:
1) Read my capture answers.
2) Propose candidate entries for recursion-gate (do not edit self.md).
3) Keep claims neutral and sourceable.
4) Add candidates only under the Candidates section.
5) Show me the diff before finalizing.

Rules:
- No content copied from users/grace-mar/**
- No hand-merge into self.md
- Stop and ask me before write actions
```

---

## Step 4 — Review checklist before saving

- [ ] Candidates are in `recursion-gate.md` only
- [ ] `self.md` unchanged
- [ ] No references to `users/grace-mar/**`
- [ ] Language is factual and reviewable

---

## Step 5 — Log completion

Add one line to:
- `companion-xavier/users/xavier/session-log.md`

Template:
- `YYYY-MM-DD: Day 1 no-terminal onboarding complete; Session 0 captured; candidates staged for review.`

---

## If blocked

If any step is unclear for more than 10 minutes:
1. Pause
2. Ask companion for live walkthrough
3. Do not improvise merge or posting

