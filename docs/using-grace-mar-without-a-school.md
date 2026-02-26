# Using Grace-Mar Without a School

**Purpose:** Run Grace-Mar as a standalone identity and learning Record when you're not attached to a school — homeschool, unschool, family learning, or adult self-directed use. The Record belongs to the companion; you don't need a school to benefit from it.

**See also:** [OPERATOR-BRIEF](operator-brief.md), [SIMPLE-USER-INTERFACE](simple-user-interface.md), [PORTABILITY](portability.md) (if you later hand the Record to a school), [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md).

---

## Who This Is For

- **Homeschool / microschool families** — You want a portable, evidence-grounded Record of who the companion is (interests, curiosity, personality) that can feed tutors, curricula, or future schools. No $40K+ tuition; you run the stack yourself or use a hosted option.
- **Families using Khan, IXL, or other tools** — Grace-Mar is the identity layer; Khan/IXL (or similar) are the teaching tools. The Record holds what they care about and what they've done; you use "we did X" to keep it current.
- **Adult or self-directed learners** — The system is age-neutral. The companion can be any age; the operator may be the same person or a facilitator.

---

## What You Need

1. **Telegram** (or WeChat) and access to the Grace-Mar bot — get the link from whoever runs the instance or follow [MINIAPP-SETUP](miniapp-setup.md) / repo setup.
2. **The "we did X" habit** — When something worth recording happens, send a message like *We read X* or *We drew Y*. The bot stages candidates; you approve via **/review**.
3. **A weekly rhythm** — Process the review queue (approve/reject), optionally rotate MEMORY/SELF-ARCHIVE, skim recent exchanges. See [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md).

No GitHub or command line required if someone else hosts the bot; if you self-host, you'll run the pipeline (merge script) after approvals.

---

## Core Loop

| Step | What to do |
|------|------------|
| **Capture** | Companion uses the bot: chat, ask questions, look things up. When something worth recording happens, the operator or companion sends "we did X." |
| **Review** | Type **/review** in the bot. See pending candidates; tap Approve or Reject. |
| **Process** | If you self-host: run the merge script so approved candidates are written to SELF, EVIDENCE, prompt. If hosted: the host does this. |
| **Repeat** | Next session: optionally run `session_brief.py` for a short brief (pending count, recent activity, wisdom questions). Keep the "we did X" + /review habit. |

---

## Export and Sharing

- **PRP (Portable Record Prompt)** — Type **/prp** in the bot to download a .txt file you can paste into ChatGPT, Claude, or any LLM. The model adopts the Record's voice and knowledge. Good for one-off chats or handing to a tutor.
- **Identity export** — For schools or platforms: `python scripts/export_user_identity.py --user grace-mar` (or your user id). Produces a markdown summary of identity, interests, curiosity, personality. See [PORTABILITY](portability.md) for handoff formats.
- **Full fork export** — For full evidence history: `scripts/export_fork.py`. Use when a school or partner needs the complete Record.

---

## Optional Stack (Low-Cost Homeschool)

- **Grace-Mar** — Identity Record + Voice (this repo; open-source).
- **Khan Academy** — Free curriculum, practice, videos.
- **Khanmigo or similar** — Optional paid tutoring layer.
- **Session continuity** — Run `session_brief.py` before sessions; use PENDING-REVIEW as lightweight accountability (nothing merges until you approve).

This gives you a portable Record and a queryable Voice without a school contract. When the companion later applies to a school or joins a program, you hand them the export (see [PORTABILITY](portability.md)).

---

## Where to Read More

| Need | Document |
|------|----------|
| How to use the bot day-to-day | [SIMPLE-USER-INTERFACE](simple-user-interface.md) |
| Operator/facilitator onboarding | [OPERATOR-BRIEF](operator-brief.md) |
| Weekly pipeline rhythm | [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md) |
| Handing the Record to a school | [PORTABILITY](portability.md) |
| Technical setup (self-host) | [ARCHITECTURE](architecture.md), [agents.md](../agents.md), [PIPELINE-MAP](pipeline-map.md) |

---

*Document version: 1.0 · Last updated: February 2026*
