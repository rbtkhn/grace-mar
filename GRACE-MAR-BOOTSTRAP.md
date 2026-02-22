# GRACE-MAR-BOOTSTRAP

GRACE-MAR · Session Bootstrap
Use this file to initiate or continue work on GRACE-MAR in any Cursor conversation.

---

## QUICK START

**Session continuity checklist (read first, before any action):**
1. Read **SESSION HANDOFF** below (last session summary)
2. Read last SESSION-LOG entry
3. Check PENDING-REVIEW status (any candidates?)
4. Skim last 1–2 EVIDENCE entries for recent context
5. Run `git status` — any unpushed changes?

Session continuity supports the feedback loop — sustained direction over time, not one-shot processing.

**If using OpenClaw (shared workspace):** See `docs/OPENCLAW-INTEGRATION.md`. Export Record for identity: `python scripts/export_user_identity.py -u pilot-001 -o USER.md`.

When this file is loaded at the start of a conversation, present the user with multiple choice options:

1. **Run session** — Load pilot-001 files, follow `.cursor/rules/grace-mar.mdc`
2. **Continue development** — Proceed with a task (user specifies)
3. **Review status** — Summarize current phase, next steps, recent changes
4. **OpenClaw / shared workspace** — Session continuity across grace-mar + OpenClaw; see `docs/OPENCLAW-INTEGRATION.md`
5. **Transfer / handoff** — School transfer, export Record for new school; see `docs/PORTABILITY.md`
6. **Other** — User describes what they need

Wait for the user to choose before proceeding.

---

## PROJECT IDENTITY

**Name:** GRACE-MAR
**Repository:** https://github.com/rbtkhn/grace-mar
**Status:** Pilot (seeding complete)
**Current Phase:** POST-SEED — ready for first interactive sessions

---

## CORE CONCEPT

A cognitive fork: a versioned, evidence-grounded record of an individual's cognitive development — initialized from a real person at a point in time, growing through curated interactions over a lifetime.

Like a software fork:
- **Seed** = initial fork (snapshot of the real person)
- **Each interaction** = a commit on the fork's branch
- **Divergence** = the fork and the real person grow independently — by design
- **Optional merge** = new information brought in when the user chooses
- **Git** = literally the version control mechanism

The fork is not a real-time mirror. It is a living, growing cognitive record — the user's lifetime academic project and archive.

**Conceptual clarity:** See `docs/CONCEPTUAL-FRAMEWORK.md` — fork vs. twin, fork as own entity vs. emulation, terminology for AI parsing.

### Single User, Lifetime System

There is no parent mode and no child mode. There is one user. A parent helps when the user is young. The user grows into full ownership. Learning to use this system is itself a lifelong skill.

---

## TWO-MODULE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     COGNITIVE FORK                          │
├─────────────────────────┬───────────────────────────────────┤
│         SELF            │            SKILLS                 │
│   (who they ARE)        │      (what they CAN DO)           │
├─────────────────────────┼───────────────────────────────────┤
│ • Personality           │ • READ (comprehension)            │
│ • Linguistic style      │ • WRITE (expression)              │
│ • Life narrative        │ • BUILD (creation)                │
│ • Preferences/values    │                                   │
│ • Reasoning patterns    │                                   │
└─────────────────────────┴───────────────────────────────────┘
```

**SELF** — Accurate record of identity. Evolves slowly. Observed from interaction.

**SKILLS** — Three modules (READ, WRITE, BUILD) that grow through activity. Each module is an objective-topic-specialized sub-agent (teacher/tutor, evaluator, record keeper) and a "container" with an edge where optimal activities are proposed. BUILD starts from zero; creation/exploration (formerly IMAGINE) is merged into BUILD.

---

## THREE MODULES OF SKILLS

| Module | What it captures | Example activities |
|--------|------------------|-------------------|
| **READ** | Comprehension, vocabulary, knowledge intake | Books read, articles, discussions |
| **WRITE** | Expression, linguistic production | Journals, stories, messages |
| **BUILD** | Making, planning, execution, exchange, creation, exploration | Lemonade stand, projects with P&L, content for audience, things built, drawings, inventions, scenarios |

---

## KEY PRINCIPLES

### Evidence Grounding Principle
The system references the user's own evidence:
- Reference their actual work and data
- Connect new activities to prior evidence
- Never invent experiences

### Container Edge Principle
Propose activities at the boundary of current capability:
- INSIDE container → use as foundation
- AT THE EDGE → propose activities here (optimal)
- OUTSIDE container → avoid (too advanced)

### Expansion Principle (Anti-Echo-Chamber)
The fork records accurately but must not create an echo chamber:
- Introduce adjacent concepts and alternative perspectives
- Do not merely validate existing beliefs
- The fork is a record with windows, not walls

### Cognitive Augmentation Warning
The fork records cognition, not replaces it:
- Users must still do the cognitive work
- Encourage retrieval practice
- The fork is a record, not an oracle

### Accurate Recording
Record the real user, not an idealized version:
- Include quirks and imperfections
- Capture them as they are
- History is preserved, not overwritten

### Optional Emulation (Future)
The fork accumulates enough data to optionally emulate the user — answering queries in their voice. This is a future feature, not the core identity. The core is the record.

### Pipeline as Cybernetic Loop (Wiener / 5000 Days)
The gated pipeline is a self-correcting feedback loop: human provides input (conversation, "we did X"), system stages candidates, human approves, fork updates. Entropy (drift, forgotten details, LLM leak) is countered by feedback. Sustained direction over time, not one-shot processing. Session continuity (review SESSION-LOG, PENDING-REVIEW before starting) closes the loop.

### Five Resurrection Directives (5000 Days Part 12 — Operator Guidance)
When designing sessions or prompts, consider:
1. **Feedback loops** — Pipeline as cybernetic circuit; log outcomes, adjust.
2. **Humane purpose** — Embed values (dignity, connection) in prompts, not just efficiency.
3. **Tactile reclamation** — Honor physical creation: handwriting, drawing, building. Friction is future luxury.
4. **Curated message ecosystems** — The fork is a living archive; sessions contribute to it deliberately.
5. **Vocations machines can't own** — Mentoring, repair, deep inquiry. Design for identity beyond productivity.

---

## GOVERNANCE HIERARCHY

```
GRACE-MAR-CORE.md (canonical, absolute authority)
    ↓
SELF-TEMPLATE.md / SKILLS-TEMPLATE.md / EVIDENCE-TEMPLATE.md
    ↓
users/[id]/SELF.md / SKILLS.md / EVIDENCE.md (instance files)
```

---

## EVIDENCE TIERS

| Tier | Type | Authority |
|------|------|-----------|
| 1 | CERTIFIED | External formal verification |
| 2 | VERIFIED | Live demonstration, proctored |
| 3 | ATTESTED | Parent/teacher confirmation |
| 4 | OBSERVED | System-captured authentic activity |
| 5 | REPORTED | User self-reports |

---

## FILE MAP

```
grace-mar/
├── GRACE-MAR-BOOTSTRAP.md      # THIS FILE — session bootstrap
├── README.md                 # Project overview
├── .cursor/rules/
│   └── grace-mar.mdc         # Governance + session protocol (users/**)
├── docs/
│   ├── GRACE-MAR-CORE.md     # CANONICAL governance (v2.0)
│   ├── CONCEPTUAL-FRAMEWORK.md  # Fork vs. twin, emulation, terminology (AI parsing)
│   ├── OPENCLAW-INTEGRATION.md  # OpenClaw integration (Record as identity, session continuity, staging)
│   ├── PORTABILITY.md           # School transfer, ownership, handoff workflow
│   ├── SIMPLE-USER-INTERFACE.md # Chat workflow for families (no GitHub)
│   ├── ADMISSIONS-LINK-USE-CASE.md # Share link for admissions/employers to chat with fork
│   ├── PRIVACY-REDACTION.md        # School/public views, redaction policy
│   ├── YOUTUBE-PLAYLIST-DESIGN.md  # Playlist building, watched-video detection (history polling)
│   ├── DESIGN-ROADMAP.md     # Product/feature design (email, newsletters, X account)
│   ├── BUSINESS-ROADMAP.md   # Strategy, monetization, child safety & privacy
│   ├── DESIGN-NOTES.md       # White paper & business proposal input (positioning, insights)
│   ├── MARKET-RESEARCH-ALPHA-KHAN.md  # Alpha alternatives, Khan Academy, cost comparison
│   ├── PARENT-BRIEF.md       # Parent/guardian brief (pre-survey)
│   ├── ARCHITECTURE.md       # Module design
│   ├── SELF-TEMPLATE.md      # SELF module governance
│   ├── SKILLS-TEMPLATE.md    # SKILLS module governance
│   ├── EVIDENCE-TEMPLATE.md  # Evidence storage governance
│   ├── JOURNAL-SCHEMA.md    # Journal (daily highlights) governance
│   ├── CONCEPT.md            # Full concept explanation
│   ├── PILOT-PLAN.md         # Pilot structure
│   └── ...                   # Supporting docs
├── scripts/
│   ├── export_fork.py        # Full fork export (JSON)
│   ├── export_user_identity.py  # Record → USER.md / SOUL.md for OpenClaw
│   └── export_view.py        # School/public views with redaction
└── users/
    └── pilot-001/            # First pilot user (age 6)
        ├── SELF.md           # Identity record (seeded)
        ├── SKILLS.md         # Capability record (seeded)
        ├── EVIDENCE.md       # Activity logs (seeded)
        ├── SESSION-LOG.md    # Interaction history
        ├── ARCHIVE.md        # Raw conversation log (private)
        ├── JOURNAL.md        # Daily highlights (public-suitable)
        └── artifacts/        # Raw files (writing samples, artwork)
```

---

## SESSION HANDOFF (latest)

*Update this section at end of each session for clean transfer.*

**Last updated:** 2026-02-22

**This session:**
- Pillar → module; IMAGINE merged into BUILD. Three modules: READ, WRITE, BUILD.
- Design philosophy embedded: transcript insights (AI Awakened, Mind Warp/Architect, Kurzweil), nature analogies (membrane, absorption, crystallization), CONCEPTUAL-FRAMEWORK invariants 26–33.
- Counterfactual harness run — 16/16 passed (knowledge boundary intact).
- Pipeline health checked — queue empty, 52 candidates processed, healthy.
- **Unpushed changes:** Kurzweil + Architect + nature analogies edits (CONCEPTUAL-FRAMEWORK, AGENTS, README, bot/prompt.py, bot/core.py, EVIDENCE-TEMPLATE). Run `git status`; consider push.

**Next session options:**
- Push remaining changes to GitHub
- Continue development or run session per pilot workflow
- Check PENDING-REVIEW if bot activity since last session

---

## LAST SESSION SUMMARY (Feb 2026)

**Design / business roadmap:**
- Split into `docs/DESIGN-ROADMAP.md` (product/feature design) and `docs/BUSINESS-ROADMAP.md` (strategy, monetization, go-to-market)
- DESIGN-ROADMAP: Grace-Mar email, outbound curated newsletter, inbound newsletter processing, X (Twitter) follow-only account
- BUSINESS-ROADMAP: positioning, monetization angles, priority items, metrics, risks; **child safety & privacy (COPPA, PII)** moved here (not essential to system operation)
- `docs/YOUTUBE-PLAYLIST-DESIGN.md`: added Section 7 — Watched Video Detection via history polling (OAuth → poll → filter by recommended → stage → approve → LIBRARY)

**OpenClaw research (pending write-up):**
- OpenClaw: personal AI assistant, runs on your machine, WhatsApp/Telegram/Discord/Signal/iMessage, persistent memory, skills/plugins, open source. See https://openclaw.ai/
- Chinese integrations: WeChat Official Account, WeCom (openclaw-plugin-wecom), personal WeChat (openclaw-wechat), DingTalk (dingtalk-openclaw-connector)
- Grace-Mar already has `docs/OPENCLAW-INTEGRATION.md` — Record as identity, session continuity, staging automation
- **Next step:** Consider adding DESIGN-ROADMAP entry for OpenClaw + Chinese app integration ideas (WeChat, DingTalk, Xiaohongshu, etc.)

---

## CURRENT STATUS

**Completed:**
- [x] Core concept defined (fork model, v2.0)
- [x] Two-module architecture (SELF + SKILLS)
- [x] Three modules (READ, WRITE, BUILD)
- [x] GRACE-MAR-CORE governance document (v2.0)
- [x] All templates created (v2.0)
- [x] Pilot user directory structure
- [x] Cursor rule for sessions
- [x] GitHub repository live
- [x] **Seed Phase 1** — Identity + preferences (parent-reported)
- [x] **Seed Phase 2** — Personality + behavior (10 MC questions, child-reported)
- [x] **Seed Phase 3** — Academic/intellectual baselines (20 yes/no, parent-reported)
- [x] **Seed Phase 4** — Creativity (8 artworks analyzed + child Q&A)
- [x] **Seed Phase 5** — Writing voice (3 writing samples + child Q&A)
- [x] **Seed Phase 6** — Personality core (5 targeted questions, child-reported)
- [x] DESIGN-ROADMAP + BUSINESS-ROADMAP split (email, newsletters, X, child safety)
- [x] YOUTUBE-PLAYLIST-DESIGN: watched video detection via history polling

**All containers have data. Seeding is complete.**

**Next:**
- [ ] First interactive session (post-seed)
- [ ] Begin regular WRITE activities
- [ ] Begin READ evidence logging
- [ ] Create age-6 snapshot (git tag)
- [ ] Optional: OpenClaw + Chinese apps integration design (add to DESIGN-ROADMAP)

---

## PILOT USER

**ID:** pilot-001
**Name:** Grace-Mar (fork name) / Abby (the real child)
**Age:** 6 years old
**Phase:** POST-SEED — all 6 seed phases complete
**Status:** SELF populated (identity, personality, linguistic style, interests, values), SKILLS populated (READ, WRITE, BUILD), EVIDENCE populated (8 artworks, 3 writing samples, media log)

---

## SESSION WORKFLOW

1. **Load user files** — SELF.md, SKILLS.md, EVIDENCE.md
2. **Check SESSION-LOG.md** — What happened last time?
3. **Greet** — Use their name, reference prior session
4. **Interact** — Follow their interests, propose activities at the edge
5. **Capture** — Log new activities, skills, preferences
6. **Commit** — `git add && git commit && git push`

---

## IMMUTABILITY RULES

- Activities (EVIDENCE) are immutable once captured
- Claims (SKILLS) may upgrade, never downgrade or delete
- SELF components may update but history is preserved
- Git commits = audit trail
- Snapshots via git tags (age-based)

---

## COMMANDS

**Check status:**
```bash
git status
```

**After session updates:**
```bash
git add users/pilot-001/*
git commit -m "Session [DATE]: [summary]"
git push origin main
```

**Create age snapshot:**
```bash
git tag pilot-001-age-6
git push origin --tags
```

---

END OF BOOTSTRAP — GRACE-MAR v2.0
