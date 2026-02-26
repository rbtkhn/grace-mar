# Operator Brief — Grace-Mar Pilot

For the operator or facilitator (e.g. parent, guardian, or family member) of the pilot.

---

## What is Grace-Mar?

A **cognitive emulator** is a system the user teaches. Unlike typical apps that teach the user, this one learns *from* them. Over time it becomes a **cognitive fork** — a versioned record of how they think, what they know, and who they are, growing independently from a snapshot in time.

The pilot (the companion) is the teacher. The system only grows through their activity.

---

## First Session: Seed Survey

The first session is a short survey to get to know the companion. Four questions:

1. What are your favorite movies or shows?
2. What are your favorite books or stories?
3. What are your favorite places?
4. What are your favorite games?

**Duration:** ~10–15 minutes (adjust for attention and context)

**Who should be present:** Operator + companion. The companion answers; the operator can help prompt, rephrase, or type if needed.

---

## How We Capture Responses

- **Typing:** Operator types while the companion answers (recommended when the companion is young or prefers not to type)
- **Voice:** If using voice, responses are transcribed afterward
- **Relaxed:** No wrong answers. Partial or silly answers are fine — they all inform the profile.

---

## Consent

- Guardian/operator consent is required when the companion is a minor
- The companion may stop at any time
- You may request full deletion of all data at any time
- Milestone re-consent at ages 13, 16, 18 (per GRACE-MAR-CORE) when the companion is a minor

---

## What Gets Stored

- Survey responses → SELF.preferences (favorites)
- Future sessions → Reading list, writing samples, creations
- Everything is stored in a private GitHub repository; no third-party sharing without explicit permission

---

## Your Role: Co-Learner, Not Just Supervisor

Position yourself as a **co-learner** with the companion. AI evolves quickly; you may not have more expertise than they do. Instead of only supervising, embrace open-minded, transparent conversations. Explore the bot together, ask questions together, and be willing to navigate the space alongside them through trial, error, and adjustments.

---

## The "We did X" Ritual — Recognition & Accountability

When something worth recording happens (a drawing, a story, something learned, a new interest), the operator or companion sends a message that starts with **"we"** and an activity verb. The bot treats it as an activity report, stages candidates to the review queue, and the companion approves what enters the Record.

**Why it matters:** "We did X" is the main way the Record grows. It creates recognition (the companion sees their activity reflected), celebration (Grace-Mar acknowledges it), and accountability (review queue stays current). Treat it as a first-class habit, not an extra feature.

**How:** In Telegram, send e.g. *We drew a volcano today* or *We read The Wild Robot*. Then type **/review** to see what’s waiting; approve or reject each item. If you run the pipeline yourself, process the queue after approvals (see [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md)).

**Before each session:** Consider whether something since last time deserves a "we did X." After the session, run **/review** if anything was added.

---

## Session continuity & PENDING-REVIEW

Keep the loop closed so the Record and the review queue stay in sync.

- **Before each session:** Skim SESSION-LOG and **PENDING-REVIEW** (or run `python scripts/session_brief.py -u grace-mar` for a short brief). Note how many candidates are waiting.
- **After the session:** If anyone sent "we did X" or you added activities, run **/review** in the bot (or process the queue per [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md)) so items don’t sit in PENDING-REVIEW for long.

Full checklist and weekly rhythm: [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md).

---

## Where is the Record? How does SELF-ARCHIVE get updated?

**Where to find the Record**

All pilot files live in the repo under **`users/grace-mar/`** (or `users/pilot-001/` in some setups). The Record itself is:

| File | What it is |
|------|------------|
| **self.md** | Who the companion is — identity, preferences, interests, knowledge (IX-A), curiosity (IX-B), personality (IX-C). |
| **skills.md** | What they can do — READ, WRITE, WORK capability and edges. |
| **self-evidence.md** | Activity log — ACT-*, WRITE-*, CREATE-* entries; raw evidence the Record is built on. |
| **pending-review.md** | Staging area — candidates the analyst (or you) staged; **nothing is in the Record until you approve and merge.** |
| **session-transcript.md** | Raw conversation log (every message), for operator continuity. Not part of the Record. |
| **self-archive.md** | Gated log of **approved** activity only — the conversation that made it into the Record. |

So: **Record = SELF + SKILLS + EVIDENCE** (and what’s reflected in the bot prompt). **PENDING-REVIEW** is the gate. **SELF-ARCHIVE** is the approved-activity log.

**Why SELF-ARCHIVE isn’t updating**

SELF-ARCHIVE is **not** written in real time. It is updated **only when you merge approved candidates**. The bot and analyst do this:

1. **Conversation** → Bot replies; analyst may detect a “signal” (new knowledge, curiosity, personality).
2. **Staging** → That becomes a **candidate** in PENDING-REVIEW (you saw “ANALYST: signal detected - staged candidate” in the log).
3. **Your step** → You open PENDING-REVIEW, approve (or reject) each candidate, then **process the queue** (merge). Only then does the script write to SELF, EVIDENCE, SESSION-LOG, the bot prompt, **and append to SELF-ARCHIVE**.

**How to get SELF-ARCHIVE to update (short version)**

1. Open **`users/grace-mar/pending-review.md`** (or your user id).
2. In the **Candidates** section, for each block you want to keep: change `status: pending` to **`status: approved`** (or `rejected` to skip).
3. Process the queue: either tell your assistant **“process the review queue”** or run:
   ```bash
   python3 scripts/process_approved_candidates.py --user grace-mar --generate-receipt /tmp/receipt.json --approved-by "Your Name"
   python3 scripts/process_approved_candidates.py --user grace-mar --apply --approved-by "Your Name" --receipt /tmp/receipt.json
   ```
4. After the merge, **SELF-ARCHIVE** is appended with the approved exchange(s); SELF, EVIDENCE, and the bot prompt are updated too.

Recommended rhythm: do this at least weekly (e.g. [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md) step 2) so the Record and SELF-ARCHIVE stay in sync with conversations.

---

## Getting Telegram chat content into Cursor

The bot writes live chat to **`users/grace-mar/session-transcript.md`** and stages candidates to **`users/grace-mar/pending-review.md`**. Those paths are relative to the **repo root of the process running the bot**. So whether that content appears in Cursor depends on where the bot runs.

**Option A — Bot runs on the same machine as Cursor, from this repo**

- Run the Telegram bot from this repo (e.g. `python -m bot.bot` or your start command from `/Users/.../grace-mar`).
- Set `GRACE_MAR_USER_ID=grace-mar` (or leave default).
- Then **`users/grace-mar/session-transcript.md`** and **pending-review.md** are inside this workspace; just open them in Cursor. New exchanges appear as the bot runs.

**Option B — Bot runs elsewhere (e.g. Render, another server)**

- The bot writes to that environment’s clone of the repo. To get that content into Cursor:
  1. **Pull from GitHub** — If the server (or a job on it) commits and pushes `users/grace-mar/session-transcript.md` and `pending-review.md` to the same repo you use in Cursor, run `git pull` in Cursor to get the latest.
  2. **Sync script** — If you have SSH or an API to the server, add a small script that copies those two files from the server into this repo (e.g. `scp server:grace-mar/users/grace-mar/session-transcript.md users/grace-mar/`), then run it when you want to refresh.
  3. **Manual paste** — Copy the chat from your log viewer or Telegram export and paste into a file in this repo (e.g. create `users/grace-mar/LOG-2026-02-25.md` or append to a notes file). Use that for operator context; it won’t update SESSION-TRANSCRIPT on the server.

**Bot on Render (24/7)** — Use the operator fetch so Cursor gets the live chat and pipeline:

1. In **Render** → your service → Environment: add **`OPERATOR_FETCH_SECRET`** (e.g. a long random string). Redeploy.
2. In **Cursor** (repo root), run:
   ```bash
   export OPERATOR_FETCH_SECRET=the-same-secret
   export GRACE_MAR_RENDER_URL=https://your-app.onrender.com
   python3 scripts/fetch_operator_files.py
   ```
   This writes `users/grace-mar/session-transcript.md` and `pending-review.md`. Run whenever you want to refresh.

**Option C — One-off: save a log snippet in the repo**

- To keep a specific conversation (e.g. the Feb 25 history Q&A) in the repo for reference: create a file like **`users/grace-mar/notes/2026-02-25-telegram-log.md`** and paste the conversation and any analyst line (e.g. “ANALYST: signal detected - staged candidate”) into it. That way it’s in Cursor and in version control without touching the bot’s live files.

**Summary**

| Bot runs in | What to do so Cursor has the chat |
|-------------|------------------------------------|
| This repo (same machine) | Run bot from this repo; open `users/grace-mar/session-transcript.md`. |
| **Render (24/7)** | Set `OPERATOR_FETCH_SECRET` on Render; run `python3 scripts/fetch_operator_files.py` from Cursor with `GRACE_MAR_RENDER_URL` and the same secret. Opens `users/grace-mar/session-transcript.md` and `pending-review.md` after fetch. |
| Other remote | Use fetch script if the host exposes the same operator endpoints; or sync the two files by another means; or paste into a notes file. |

---

## Before the Session

1. Read [letter-to-user.md](letter-to-user.md) (or [letter-to-student.md](letter-to-student.md) for a school-aged variant) if you want to frame it for the companion
2. Ensure you can type responses in real time (or plan for transcription)
3. Confirm consent (verbal is fine; we log it in SESSION-LOG)

---

*Document version: 1.0 · Last updated: February 2026*
*See also: parent-brief.md (legacy name for the same content when the operator is a parent/guardian).*
