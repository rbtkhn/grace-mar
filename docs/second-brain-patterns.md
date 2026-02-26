# Second Brain Patterns — Borrowed for Grace-Mar

**Sources:** Notion Second Brain / PARA (Forté, Saxena); Claude Code + Obsidian + Skills (Dynamist).  
**Purpose:** Design patterns worth adopting or adapting for Grace-Mar's capture, organization, and maintenance flows.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md)

---

## 1. Quick Capture (Low Friction)

**Pattern:** Capture in under 30 seconds. If it takes longer, people won't do it—things fall through the cracks.

**Grace-Mar application:**
- **Telegram as capture surface** — User types or speaks; bot responds. One-tap actions (menu, lookup, checkpoint). See [CHAT-FIRST-DESIGN](chat-first-design.md).
- **"We [did X]"** — Operator reports in natural language; analyst stages. No forms, no multi-step wizards.
- **Design rule:** Any capture path should complete in one or two steps. Avoid nested menus for capture.

---

## 2. Inbox → Process (Don't Merge at Capture)

**Pattern:** Capture first; process later. Inbox holds raw items; processing assigns them to structure (projects, areas). Merge happens during review, not at capture.

**Grace-Mar application:**
- **PENDING-REVIEW** is the inbox. Analyst stages candidates; user processes during review.
- **Sovereign Merge Rule** — The agent may stage; it may not merge. See [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md).
- **Design rule:** Never require the user to decide IX-A vs IX-B vs IX-C at capture time. Staging proposes; review assigns.

---

## 3. Connection Over Isolation

**Pattern:** Notes and tasks link to structure (projects, areas, resources). Items aren't floating—they're connected to what matters now.

**Grace-Mar application:**
- **Evidence linking** — Every IX-A, IX-B, IX-C entry references `evidence_id: ACT-XXXX`. Claims trace to artifacts.
- **LIBRARY → lookup** — Books and sources connect to knowledge; lookups route through them.
- **Design rule:** Stage candidates with proposed `profile_target` and `evidence_id`. Reviewer sees the link before approving.

---

## 4. Weekly Review (Maintenance Ritual)

**Pattern:** 30 minutes or less per week to clear inboxes, process pending items, and start the next week with clarity. Block it on the calendar.

**Grace-Mar application:**
- **Operator ritual:** Process PENDING-REVIEW queue; clear staged candidates; optionally run checkpoint/summary for the week. See [OPERATOR-WEEKLY-REVIEW](operator-weekly-review.md).
- **MEMORY rotation** — Prune or rotate MEMORY per policy (weekly recommended). See [MEMORY-TEMPLATE](memory-template.md).
- **Design rule:** Document a recommended operator rhythm (e.g., "Sunday evening: process queue, rotate MEMORY"). Make it optional but explicit.

---

## 5. Two-Minute Rule (At Review Time)

**Pattern:** During processing, if an item takes 2 minutes or less to handle, do it immediately. If longer, add to a task list.

**Grace-Mar application:**
- **Quick approves/rejects** — One candidate = one decision. Approve or reject; don't defer unless necessary.
- **Batch processing** — When reviewing multiple candidates, handle trivial ones first (clear rejects, obvious approves) to reduce cognitive load.
- **Design rule:** Keep candidate cards scannable. Summary + one sentence; full detail on expand.

---

## 6. Mobile-Optimized Capture

**Pattern:** Capture surface optimized for mobile—single column, large tap targets, minimal scrolling. Add to favorites for one-tap access.

**Grace-Mar application:**
- **Chat-first** — Telegram/WeChat are mobile-native. No custom UI to optimize; the chat *is* the capture surface.
- **PRP / Mini App** — If used on mobile, keep menus flat and actions one-tap. See [PORTABLE-RECORD-PROMPT](portable-record-prompt.md), [CHAT-FIRST-DESIGN](chat-first-design.md).
- **Design rule:** Every capture path must work on a phone keyboard. No multi-column layouts, no hover states.

---

## 7. Startup Checklist (Daily Grounding)

**Pattern:** A short checklist at the start of the day—5–10 minutes—to ground oneself and avoid reactive mode. Check inbox, priorities, today's focus.

**Grace-Mar application:**
- **Operator startup:** Open PENDING-REVIEW; skim SESSION-TRANSCRIPT or SELF-ARCHIVE for recent context; process any urgent candidates.
- **Session start (Voice):** Menu (A=recent doings, B=learnings, C=curiosity, D=free chat) lets the user choose how to begin. Bounded, not infinite.
- **Design rule:** Offer a lightweight "how do you want to start?" rather than dumping everything. Match Second Brain's proactive vs. reactive framing.

---

## What We Don't Borrow

| Second Brain Concept | Why Grace-Mar Skips It |
|----------------------|------------------------|
| **PARA (Projects, Areas, Resources, Archives)** | Grace-Mar organizes by IX-A/B/C (knowledge, curiosity, personality). Identity, not productivity. |
| **Task management** | No tasks, deadlines, or project tracking. Invariant 5: identity beyond productivity. |
| **Read later** | LIBRARY serves a different role—curated sources for lookup, not a consumption queue. |
| **Recurring tasks** | No recurring to-dos. Optional: recurring wisdom questions or checkpoints as session prompts. |

---

## Summary

| Pattern | Grace-Mar Implementation |
|---------|--------------------------|
| Quick capture | Telegram chat, "we [did X]", one-tap actions |
| Inbox → process | PENDING-REVIEW; stage vs. merge |
| Connection over isolation | Evidence linking; LIBRARY → lookup |
| Weekly review | Operator processes queue; MEMORY rotation |
| Two-minute rule | Quick approve/reject; scannable candidates |
| Mobile-optimized | Chat-first; flat menus |
| Startup checklist | Operator startup; session menu (A/B/C/D) |
| Progressive disclosure | AGENTS + linked docs; load-on-demand rules |
| Markdown as canvas | SELF, EVIDENCE, SELF-ARCHIVE as files; git audit |
| Human in the loop | Sovereign Merge; conductor workflow |

---

## Actionable Inspiration

Ideas extracted from these patterns that could be implemented:

| Idea | Source | Effort | Notes |
|------|--------|--------|-------|
| **Rule file "when to load" cues** | Progressive disclosure | Low | Add one-line description to AGENTS sections so Cursor knows when to read full doc. |
| **Session priming from MEMORY** | Connection, startup | Medium | When starting a Voice session, inject MEMORY (tone, resistance notes) into context so responses honor it. **Done:** `_load_memory_appendix` adds explicit Resistance Notes instruction when that section exists. |
| **Index/graph of Record links** | Markdown as canvas | Low | Script to output SELF↔EVIDENCE↔SELF-ARCHIVE link map; helps operator navigate. |
| **Scannable candidate cards** | Two-minute rule | Low | Improve PENDING-REVIEW formatting: bold summary, collapsible detail. |
| **MCP-as-skill for Cursor** | Progressive disclosure | Medium | If Grace-Mar adds MCPs (e.g. Telegram, Notion), wrap as skills that load only when task requires. Reduces context bloat. |
| **Brand/voice for PRP** | Human in the loop | Low | PRP already encodes voice; consider explicit "voice calibration" pass (Lexile, tone) when regenerating. |
| **Weekly review reminder** | Weekly ritual | Low | Optional: cron or script that emits "PENDING-REVIEW has N candidates" to operator channel. |

**Prioritization:** Session priming (MEMORY → Voice) and scannable candidates directly improve daily use. Rule cues and index are refinements. MCP-as-skill is forward-looking if the ecosystem grows.
