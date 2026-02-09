# COG-EM-BOOTSTRAP

Cognitive Emulator · Session Bootstrap
Use this file to initiate or continue work on cog-em in any Cursor conversation.

---

## QUICK START

**To continue development:** Read this file, then proceed with the task.

**To run a pilot session:** Load `users/pilot-001/SELF.md`, `SKILLS.md`, `EVIDENCE.md`, then interact with the user following the Cursor rule at `.cursor/rules/cog-em-pilot.mdc`.

---

## PROJECT IDENTITY

**Name:** cog-em (Cognitive Emulator)
**Repository:** https://github.com/rbtkhn/cog-em
**Status:** Pre-pilot
**Current Phase:** SEEDING (initial profile building)

---

## CORE CONCEPT

A cognitive emulator is an AI system that:
- Learns FROM the user (not teaches TO the user)
- Grows only through authentic user activity
- Mirrors the user's personality, reasoning, and knowledge
- Functions as a living credential (queryable diploma/CV)
- Persists across years (childhood → career)

The user teaches the system. The system becomes their cognitive twin.

---

## TWO-MODULE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     COGNITIVE TWIN                          │
├─────────────────────────┬───────────────────────────────────┤
│         SELF            │            SKILLS                 │
│   (who they ARE)        │      (what they CAN DO)           │
├─────────────────────────┼───────────────────────────────────┤
│ • Personality           │ • READ (comprehension)            │
│ • Linguistic style      │ • WRITE (expression)              │
│ • Life narrative        │ • IMAGINE (creation)              │
│ • Preferences/values    │                                   │
│ • Reasoning patterns    │                                   │
└─────────────────────────┴───────────────────────────────────┘
```

**SELF** — Authentic mirror of identity. Evolves slowly. Observed, not taught.

**SKILLS** — Three pillars (READ, WRITE, IMAGINE) that grow through activity. Each pillar is a "container" with an edge where teaching happens.

---

## THREE PILLARS OF SKILLS

| Pillar | What it captures | Example activities |
|--------|------------------|-------------------|
| **READ** | Comprehension, vocabulary, knowledge intake | Books read, articles, discussions |
| **WRITE** | Expression, linguistic production | Journals, stories, messages |
| **IMAGINE** | Creation, synthesis, exploration | Drawings, inventions, scenarios |

---

## KEY PRINCIPLES

### Response Grounding Principle
The twin speaks THROUGH the user's evidence:
- Use their vocabulary and phrases
- Reference books they've actually read
- Recall their own creations
- Never invent experiences

### Container Edge Principle
Teach at the boundary of current capability:
- INSIDE container → use as foundation
- AT THE EDGE → teach here (optimal)
- OUTSIDE container → avoid (too advanced)

### Expansion Principle (Anti-Echo-Chamber)
The twin mirrors but must not create an echo chamber:
- Introduce adjacent concepts and alternative perspectives
- Do not merely validate existing beliefs
- The twin is a mirror with windows, not walls

### Cognitive Augmentation Warning
The twin augments cognition, not replaces it:
- Users must still do the cognitive work
- Encourage retrieval practice (ask user to recall before confirming)
- The twin is a mirror, not an oracle

### Authentic Mirroring
Mirror the real user, not an idealized version:
- Include quirks and imperfections
- Others should recognize the user through the twin

---

## GOVERNANCE HIERARCHY

```
COG-EM-CORE.md (canonical, absolute authority)
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
cog-em/
├── COG-EM-BOOTSTRAP.md      # THIS FILE — session bootstrap
├── README.md                 # Project overview
├── .cursor/rules/
│   └── cog-em-pilot.mdc     # Cursor rule for pilot sessions
├── docs/
│   ├── COG-EM-CORE.md       # CANONICAL governance
│   ├── ARCHITECTURE.md      # Module design
│   ├── SELF-TEMPLATE.md     # SELF module governance
│   ├── SKILLS-TEMPLATE.md   # SKILLS module governance
│   ├── EVIDENCE-TEMPLATE.md # Evidence storage governance
│   ├── CONCEPT.md           # Full concept explanation
│   ├── PILOT-PLAN.md        # 2-month pilot structure
│   ├── COMPETITIVE-ANALYSIS.md
│   ├── ANTI-CHEATING.md
│   ├── DIFFERENTIATION.md
│   ├── TEAM.md
│   └── LETTER-TO-STUDENT.md
└── users/
    ├── README.md            # User directory structure
    └── pilot-001/           # First pilot user (age 6)
        ├── SELF.md          # Personality profile (to be seeded)
        ├── SKILLS.md        # Capability containers (empty)
        ├── EVIDENCE.md      # Activity logs (empty)
        └── SESSION-LOG.md   # Interaction history
```

---

## CURRENT STATUS

**Completed:**
- [x] Core concept defined
- [x] Two-module architecture (SELF + SKILLS)
- [x] Three pillars (READ, WRITE, IMAGINE)
- [x] COG-EM-CORE governance document
- [x] All templates created
- [x] Pilot user directory structure
- [x] Cursor rule for pilot sessions
- [x] GitHub repository live

**Next:**
- [ ] Run first pilot session with pilot-001
- [ ] Complete initial survey (favorite books, movies, places, games)
- [ ] Begin WRITE activities (daily journal)
- [ ] Begin READ evidence (reading list)

---

## PILOT USER

**ID:** pilot-001
**Age:** 6 years old
**Phase:** SEEDING
**Goal:** Build initial SELF profile through survey + early activities

**Initial survey questions:**
1. What are your favorite books?
2. What are your favorite movies/shows?
3. What are your favorite places?
4. What are your favorite games?

---

## SESSION WORKFLOW

1. **Load user files** — SELF.md, SKILLS.md, EVIDENCE.md
2. **Check SESSION-LOG.md** — What happened last time?
3. **Greet** — Use their name, reference prior session
4. **Explore** — Follow their interests, teach at the edge
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

## RELATED PROJECTS

This project adapts patterns from the **Civilizational Memory Codex (CMC)**:
- CIV-MEM-CORE → COG-EM-CORE
- CIV-MIND-TEMPLATE → SELF-TEMPLATE
- CIV-SCHOLAR-TEMPLATE → SKILLS-TEMPLATE
- CIV-ARC-TEMPLATE → EVIDENCE-TEMPLATE

CMC repository: `/Users/robertkuhne/Documents/CIV–MEM/`

---

## CONTACT

Repository owner: rbtkhn

---

END OF BOOTSTRAP — COG-EM v1.0
