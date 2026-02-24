# Friction Audit

**Purpose:** Identify the top friction points in the current workflow, rank them by impact and effort, and prioritize interventions.

**Last updated:** February 2026

---

## Scoring

- **Impact:** 1–5 (1 = minor annoyance, 5 = blocks or heavily discourages use)
- **Effort:** 1–5 (1 = quick fix, 5 = major build)
- **Priority:** Impact ÷ Effort (higher = tackle first)

---

## Top 5 Friction Points

### 1. Process the review queue

**What it is:** User must open PENDING-REVIEW.md, change `status: pending` to `approved` or `rejected` for each candidate, then tell the assistant "process the review queue." The assistant updates SELF, EVIDENCE, SESSION-LOG, prompt.py, and moves candidates to Processed.

**Impact:** 4 — If queue grows (e.g., after a long bot session), review becomes tedious. Skipping leaves orphaned candidates. No batch actions.

**Effort:** 2 — Could add: (a) CLI/dashboard for approve-all / reject-all with filters, (b) priority-sorted view (already have priority_score), (c) "quick approve" for high-confidence candidates.

**Priority:** 4 ÷ 2 = **2.0**

**Planned intervention:** Web dashboard (approved improvement #4) with approve/reject UI. Shorter term: document that candidates can be sorted by priority_score when reviewing in Cursor.

---

### 2. Upload artifact (WRITE / BUILD creation)

**What it is:** To log a writing sample or artwork, the user must: (1) photograph or scan, (2) save to `artifacts/`, (3) create or extend the EVIDENCE.md entry (YAML structure, analysis). No upload flow, no templates.

**Impact:** 5 — This is the main blocker for WRITE and BUILD (creation) evidence. High cognitive load: user must know the schema and write YAML.

**Effort:** 3 — Options: (a) Telegram bot photo upload → staging area with minimal metadata, (b) template script that scaffolds a new WRITE-* or CREATE-* entry from filename + prompts for key fields, (c) web form for artifact + metadata.

**Priority:** 5 ÷ 3 = **1.67**

**Planned intervention:** Template script (low effort) for new WRITE/CREATE entries. Longer term: optional bot or web upload flow.

---

### 3. Integration (five-file sync on approval)

**What it is:** When processing approved candidates, the assistant must update SELF.md, EVIDENCE.md (ACT-*), PENDING-REVIEW.md, SESSION-LOG.md, and bot/prompt.py in one atomic pass. Any omission causes inconsistency.

**Impact:** 3 — Error-prone. One missed file = drift. Human must verify.

**Effort:** 3 — Could add: (a) integration script that takes approved candidate IDs and performs all updates, (b) validator that checks consistency post-integration, (c) single "process" command that reads PENDING-REVIEW and applies changes.

**Priority:** 3 ÷ 3 = **1.0**

**Planned intervention:** Integration script (see approved improvement #5 Integrity-by-default). Reduces manual edit surface.

---

### 4. Bot session review

**What it is:** After a bot conversation, the user may want to review what happened. SELF-ARCHIVE.md holds the gated approved log; SESSION-TRANSCRIPT.md has the raw log. There's no summary, no "what's new in PENDING," no diff of profile changes. User must read archive + PENDING-REVIEW manually.

**Impact:** 3 — Slows "what did we learn?" reflection. Hard to spot missed signals or duplicates.

**Effort:** 2 — Could add: (a) session summary script (last N messages, new candidates staged), (b) "since last commit" diff for SELF/SKILLS.

**Priority:** 3 ÷ 2 = **1.5**

**Planned intervention:** Session summary script or dashboard view. Low effort, high clarity.

---

### 5. READ evidence logging

**What it is:** Reading List in EVIDENCE is empty. No flow exists for "we finished a book" or "we read X." User would need to add READ-* entry manually with full schema (title, author, evidence_tier, comprehension, etc.).

**Impact:** 4 — READ module is underfed. Architecture expects READ → SELF.interests, SKILLS.READ, but there's no habit or tool.

**Effort:** 2 — Options: (a) minimal READ template (title, date, tier, 1–2 comprehension notes), (b) "we finished [book]" operator flow that stages a READ candidate for PENDING-REVIEW, (c) analyst could flag book mentions in bot → stage as curiosity/knowledge (already happens for interest) but not as structured READ evidence.

**Priority:** 4 ÷ 2 = **2.0**

**Planned intervention:** Minimal READ entry template + operator "we [read/finished X]" convention. Document in Pipeline Map and grace-mar rule.

---

## Summary Table

| Rank | Friction point        | Impact | Effort | Priority |
|------|------------------------|--------|--------|----------|
| 1    | Process review queue   | 4      | 2      | 2.0      |
| 2    | READ evidence logging  | 4      | 2      | 2.0      |
| 3    | Bot session review     | 3      | 2      | 1.5      |
| 4    | Upload artifact        | 5      | 3      | 1.67     |
| 5    | Integration (five-file) | 3     | 3      | 1.0      |

---

## Lower-Priority Friction (not top 5)

| Friction                     | Impact | Effort | Note                                      |
|-----------------------------|--------|--------|-------------------------------------------|
| Git commit after session    | 2      | 1      | Already documented; low friction          |
| Analyst dedup maintenance   | 2      | 2      | prompt.py analyst section grows; periodic |
| Lexile ceiling updates      | 2      | 2      | Rare; requires writing sample evidence    |
| Multi-fork setup            | 2      | 2      | No second user yet; init script planned   |

---

## Recommended Order of Intervention

1. **Quick wins (effort 1–2):** READ template + "we finished [book]" convention; session summary script.
2. **Medium (effort 2–3):** Review queue UI (dashboard); artifact template script.
3. **Structural (effort 3+):** Integration script; upload flow.

---

*Document version: 1.0*
