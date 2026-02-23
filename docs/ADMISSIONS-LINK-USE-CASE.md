# Admissions / Job Applicant Link — Use Case & Plan

**Purpose:** Allow applicants to share a link so admissions officers or employers can interact with their cognitive fork (Grace-Mar) as part of the application process. The fork becomes a conversational window into who the applicant is.

**Status:** Plan sketch. Not yet implemented.

**See also:** [ARCHITECTURE](ARCHITECTURE.md), [PORTABILITY](PORTABILITY.md), [SIMPLE-USER-INTERFACE](SIMPLE-USER-INTERFACE.md).

---

## Use Case

### Actor
- **Applicant** — Person applying to school or job. They have a cognitive fork (Record) that has been built over time.
- **Reviewer** — Admissions officer, hiring manager, or recruiter evaluating the application.

### Goal
The reviewer wants to **get to know the applicant** beyond static materials (résumé, essay, transcript). The applicant wants to **offer a live, authentic view** of their identity, interests, knowledge, and values.

### Flow

1. **Applicant** completes their application and includes a link (e.g. `https://grace-mar.example.com/me/abigail-smith`).
2. **Reviewer** clicks the link and lands on a chat interface.
3. **Reviewer** reads a brief intro (e.g. "This is Abigail's cognitive fork — a living record of who she is. Ask anything to get to know her.").
4. **Reviewer** asks questions; the fork responds in Abigail's voice using only what is documented in her Record.
5. **Reviewer** explores: interests, values, what she's learned, how she thinks, projects, experiences.
6. Session is **read-only** for the reviewer — they cannot add or change the Record. The fork only answers; it does not learn from this conversation.

### Value

| For reviewer | For applicant |
|--------------|---------------|
| Probe beyond the essay; ask follow-ups | Show who they are, not just what they've done |
| Interactive, exploratory | Evidence-grounded; no fabrication |
| See how the applicant reasons and expresses | Control what's in the Record; share when ready |
| Differentiator vs. static applications | Portfolio + identity in one link |

---

## Technical Sketch

### Architecture

```
Applicant's Record (SELF, SKILLS, EVIDENCE)
         │
         ▼
    Q&A / Interview API
         │
         ▼
   Web UI (chat interface)
         │
         ▼
   Reviewer (browser)
```

### Components

| Component | Description |
|-----------|-------------|
| **Shareable URL** | Per-user or per-session. e.g. `/me/<user-id>` or `/interview/<token>`. Token can encode expiry, scope. |
| **Interview mode** | Chat session where (1) the fork responds in the applicant's voice, (2) exchanges are **not** archived to the Record (reviewer is observer, not pipeline input), (3) optional framing: "I'm here so you can learn about me." |
| **Web UI** | Standalone page (no Telegram required). Same interaction as Q&A miniapp: ask, get response. Clean, institutional look for admissions/HR. |
| **API** | Reuse `/api/ask` pattern. Accept optional `user_id` or `token` to scope to the applicant's fork. Stateless; no login for reviewer. |

### Session scope

| Option | Pros | Cons |
|--------|------|------|
| **Time-limited token** | Reviewer has N days to use the link; applicant controls exposure | Requires token generation, storage |
| **Per-user public link** | Simple: `/me/abigail` always works | Link could be shared indefinitely |
| **One-time use** | Maximum control | Reviewer can't return to continue conversation |

**Recommendation:** Time-limited token (e.g. 14 days) for school/job applications. Per-user public link for portfolios / "meet me" pages.

**Alternative:** Applicant can share the [Portable Record Prompt](PORTABLE-RECORD-PROMPT.md) instead of a hosted link; reviewer pastes into their own LLM (ChatGPT, Claude, etc.). No server required; applicant controls the snapshot.

### What the fork knows

Same as today: **only what is in the Record**. Knowledge boundary applies. The fork will say "I don't know" when asked about topics outside its documented scope. This is a feature — authenticity, not overclaiming.

---

## Considerations

### Authenticity
- The Record is evidence-grounded and gated. Content enters only through the pipeline with user approval.
- The fork cannot invent experiences — it references SELF, SKILLS, EVIDENCE.
- **Caveat:** The Record is a curated snapshot. It reflects what the applicant (or family) chose to include. Schools/employers should treat it as supplementary, like a portfolio, not as verified credential.

### Privacy
- Applicant controls what is in the Record and when to share the link.
- The interview session is read-only: the reviewer cannot add to or modify the Record.
- Exchanges in interview mode should **not** feed the pipeline — the reviewer's questions are not observations about the applicant. (Optional: log for applicant's own review, but not for profile growth.)

### Positioning
- **Tagline:** "Apply with your cognitive fork. Let them meet the real you."
- **Differentiator:** Interactive identity layer — not just documents, but a conversation.
- **Audience:** Schools (Alpha, Incept, selective admissions), employers (especially roles where fit and character matter), scholarships.

### Age / maturity
- Current pilot is a 6-year-old. The use case scales: high school, college, job applicants. Voice and depth of the Record grow with the person.
- Lexile / vocabulary constraints in the prompt adapt to age. Older applicants have richer SELF, SKILLS, EVIDENCE.

---

## Implementation Plan (Phased)

### Phase 1 — Foundation ✓
- [x] Extend miniapp/server to accept interview mode via URL: `/i/<token>`, `/me/<user_id>`, `?mode=interview`, or `?t=<token>`.
- [x] Interview sessions use `channel_key: interview`; exchanges are **not** archived (read-only for reviewer).
- [x] Interview landing shows different intro: "This is Grace-Mar's cognitive fork... Ask anything to get to know her. Your questions are not saved."

### Phase 2 — Shareable links
- [ ] Token generation: create time-limited tokens for a user; store mapping (token → user_id, expiry).
- [ ] Shareable URL format: `https://grace-mar.example.com/i/<token>`.
- [ ] Landing page with brief intro for reviewer (who this is, how to use, privacy note).

### Phase 3 — Polish
- [ ] Theming: optional "interview" variant (more formal, institutional) vs. casual Q&A.
- [ ] Applicant dashboard: "Generate application link" with expiry picker; copy link, view usage (optional).
- [ ] Optional: one-time links for maximum control.

### Phase 4 — Multi-user
- [ ] Today: single pilot (pilot-001). Future: multi-user backend; each applicant has their own Record and shareable link.
- [ ] Auth for applicants (to generate links, manage Record); reviewers remain unauthenticated.

---

## Out of Scope (For Now)

- Verification that the Record is "authentic" (e.g. attestations, blockchain). The fork is as trustworthy as the applicant and the pipeline.
- Reviewer authentication or analytics (who viewed, for how long). Could be added later.
- Integration with ATS/LMS — applicant pastes link into application form; no deep integration.

---

## File Map (Current)

| File | Role |
|------|------|
| `miniapp/index.html` | Q&A UI; would add interview variant or query param |
| `miniapp_server.py` | Serves UI + `/api/ask`; would add token resolution, interview channel |
| `bot/core.py` | `get_response`, `run_lookup`; channel_key drives archive behavior |
| `users/[id]/SELF.md` | Identity source for fork |

---

*Document version: 1.0*
*Last updated: February 2026*
