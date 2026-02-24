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

**How:** In Telegram, send e.g. *We drew a volcano today* or *We read The Wild Robot*. Then type **/review** to see what’s waiting; approve or reject each item. If you run the pipeline yourself, process the queue after approvals (see [OPERATOR-WEEKLY-REVIEW](OPERATOR-WEEKLY-REVIEW.md)).

**Before each session:** Consider whether something since last time deserves a "we did X." After the session, run **/review** if anything was added.

---

## Session continuity & PENDING-REVIEW

Keep the loop closed so the Record and the review queue stay in sync.

- **Before each session:** Skim SESSION-LOG and **PENDING-REVIEW** (or run `python scripts/session_brief.py -u pilot-001` for a short brief). Note how many candidates are waiting.
- **After the session:** If anyone sent "we did X" or you added activities, run **/review** in the bot (or process the queue per [OPERATOR-WEEKLY-REVIEW](OPERATOR-WEEKLY-REVIEW.md)) so items don’t sit in PENDING-REVIEW for long.

Full checklist and weekly rhythm: [OPERATOR-WEEKLY-REVIEW](OPERATOR-WEEKLY-REVIEW.md).

---

## Before the Session

1. Read [LETTER-TO-USER.md](LETTER-TO-USER.md) (or [LETTER-TO-STUDENT.md](LETTER-TO-STUDENT.md) for a school-aged variant) if you want to frame it for the companion
2. Ensure you can type responses in real time (or plan for transcription)
3. Confirm consent (verbal is fine; we log it in SESSION-LOG)

---

*Document version: 1.0 · Last updated: February 2026*
*See also: PARENT-BRIEF.md (legacy name for the same content when the operator is a parent/guardian).*
