# Grace-Mar Web App Plan — grace-mar.com

**Purpose:** Plan for developing and maintaining the Grace-Mar web app at grace-mar.com. Aligns with skill-work objectives and long-term identity infrastructure goals.

**Status:** Plan. Not yet implemented.

**Governed by:** [GRACE-MAR-CORE](grace-mar-core.md), [CHAT-FIRST-DESIGN](chat-first-design.md)

**See also:** [ADMISSIONS-LINK-USE-CASE](admissions-link-use-case.md), [DESIGN-ROADMAP](design-roadmap.md)

---

## 1. Current State

| Asset | Location | Role |
|-------|----------|------|
| Profile pages | `profile/` → static HTML | Identity, interests, curiosity, skills summary |
| LLM flow | `profile/llm/` | Paste PRP; chat with fork in external LLM |
| Telegram redirect | `profile/telegram/` | Link to bot |
| WeChat redirect | `profile/wechat/` | Link to bot |
| Playlist placeholder | `profile/playlist/` | Reserved |

**Gap:** No hosted chat at grace-mar.com. Chat lives in Telegram/WeChat only. Admissions use case and families without messaging apps have no web chat.

---

## 2. Long-Term Vision

Grace-mar.com becomes the **primary front door** for Grace-Mar:
- Stable, memorable URL for identity infrastructure
- Web chat for companions, reviewers, families
- Profile, review flow, export, bots — unified presence
- Institutional access (admissions, schools, employers) via browser

**Principle:** Web app is another channel; chat-first design applies. Record felt, not seen.

---

## 3. Phased Plan

### Phase 1: Extend Existing Site (0–3 months)

**Goal:** Web chat at grace-mar.com for reviewers and families. Minimal scope.

| Deliverable | Description |
|-------------|-------------|
| **Chat page** | `/chat` or `/me/<user-id>` — ask, get response. Reuse bot core (`run_grounded_response`, retriever, prompt). |
| **Admissions mode** | Time-limited token; reviewer sees applicant's fork; read-only. See [ADMISSIONS-LINK-USE-CASE](admissions-link-use-case.md). |
| **API** | `/api/ask` (or equivalent) — accepts question + user_id/token; returns Voice response. Stateless. |
| **Landing** | Improve profile/index.html — clear entry points: Chat, Profile, LLM, Telegram, WeChat. |

**Tech:** Static HTML/CSS/JS for front-end; backend API (Python, FastAPI or Flask) wrapping bot core. Host on existing infra.

**Dependencies:** bot/core.py, bot/retriever.py, bot/prompt.py; PRP export.

---

### Phase 2: Companion-Facing Features (3–6 months)

**Goal:** Web app for companions (and operators) to manage Record, review pipeline, export.

| Deliverable | Description |
|-------------|-------------|
| **Review flow** | View PENDING-REVIEW; approve/reject from web. Same gate as today; web UI instead of editing files. |
| **Session continuity** | Before chat, load SESSION-LOG, MEMORY. Close the loop. |
| **Export** | Trigger export (PRP, curriculum_profile, etc.) from web; download. |
| **Auth** | Companion/operator login. Scope: one user per instance for pilot. |

**Tech:** Add auth layer; integrate with pipeline (read PENDING-REVIEW; call process_approved_candidates on approve).

**Dependencies:** Pipeline scripts; user dir structure.

---

### Phase 3: Hub and Polish (6–12 months)

**Goal:** Full web app as central hub.

| Deliverable | Description |
|-------------|-------------|
| **Dashboard** | Overview: recent activity, pending count, evidence summary, work goals progress. |
| **Journal view** | Read JOURNAL entries (approved only). Optional: add entry via web. |
| **Library view** | LIBRARY status; add/update via web (staged, gated). |
| **Profile editing** | No direct SELF/SKILLS editing; all changes via pipeline. Web surfaces staging and approval. |
| **Mobile-responsive** | Grace-mar.com usable on phone. |

**Tech:** Expand front-end; ensure API coverage for all read/write paths that need web access.

---

## 4. Technical Approach

### Architecture

```
grace-mar.com
├── /              Landing, links
├── /profile       Static profile pages (existing)
├── /llm           PRP paste flow (existing)
├── /chat          Web chat (Phase 1)
├── /me/<id>       Shareable chat (admissions) (Phase 1)
├── /review        Pipeline review (Phase 2)
├── /export        Export triggers (Phase 2)
└── /api
    ├── /ask       Chat API (Phase 1)
    ├── /pending   PENDING-REVIEW read (Phase 2)
    └── /approve   Process approved (Phase 2)
```

### Reuse

| Component | Reuse |
|-----------|-------|
| Voice logic | bot/core.py — `run_grounded_response`, prompt assembly |
| Retrieval | bot/retriever.py — load_record_chunks |
| Prompt | bot/prompt.py — SYSTEM_PROMPT, etc. |
| Export | scripts/export_prp.py, export_curriculum.py |
| Pipeline | scripts/process_approved_candidates.py |

### Chat-First Alignment

- Chat page: one input, one response. No nested menus.
- Record felt not seen: responses reflect Record; user doesn't browse SELF/SKILLS directly.
- Bounded sessions: "all done!" closure where appropriate.

---

## 5. Dependencies

| Phase | Depends on |
|-------|------------|
| Phase 1 | bot core, retriever, prompt; hosting for API |
| Phase 2 | Auth; pipeline scripts; file read/write from web process |
| Phase 3 | Phase 1–2 complete; dashboard/UI design |

---

## 6. Success Criteria

| Phase | Success |
|-------|---------|
| 1 | Reviewer can open `/me/<token>`, ask questions, get fork responses. No Telegram. |
| 2 | Operator can approve PENDING-REVIEW from web. Export downloadable. |
| 3 | Companion/operator uses grace-mar.com as primary interface. |

---

## 7. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Scope creep | Phase 1 only: chat + admissions. Defer dashboard, editing. |
| Auth complexity | Start with single-user pilot; token-based for admissions. |
| Duplication with bots | Reuse bot core; web is another client. |

---

*Plan version: 1.0*
*Last updated: February 2026*
