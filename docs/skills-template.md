# SKILLS–TEMPLATE v2.0

Cognitive Emulator · Skills Module Governance Template

Status: ACTIVE
Version: 2.0
Last Update: February 2026

**Governed by**: [GRACE-MAR-CORE v2.0](grace-mar-core.md)

---

## I. PURPOSE

This template governs the SKILLS module of the cognitive fork.

The SKILLS module:
- Captures what the user CAN DO
- Grows through authentic activity (not explicit teaching)
- Provides queryable, verifiable capability evidence
- Tracks depth, not just breadth
- Preserves development trajectory over time

The SKILLS module is NOT:
- A curriculum
- A grading system
- A test score repository
- An automated assessment
- A teaching interface

SKILLS are demonstrated through real activity. The user DOES things;
Grace-Mar observes, records, and infers capability from accumulated evidence.

---

## II. THE THREE MODULES

**Formal specification:** Module set, boundaries, and the rule that Voice and written profile are functions of the Record (with skill-write as linguistic shaper) are specified in [SKILLS-MODULARITY](skills-modularity.md).

**Standard labels:** For APIs, docs, and cross-references use **self-skill-write**, **self-skill-think**, **self-skill-work**. See [ID-TAXONOMY § Standard capability labels](id-taxonomy.md#standard-capability-labels-self-skill-).

**Naming:** The third module is named **WORK** in prose and design (making, planning, execution, exchange, creation, exploration). **Internal identifiers remain BUILD** for compatibility: in skills.md the section is "BUILD Container"; evidence IDs use CREATE-nnn and ACT-nnn. No change to existing evidence or scripts.

All skills organize under three fundamental cognitive modules: THINK, WRITE, WORK. Each module is an objective-topic-specialized sub-agent serving as teacher/tutor, evaluator, and record keeper. WORK (making, planning, execution, exchange, creation, exploration) starts from zero and grows with experience and input through the pipeline, human-gated like all others.

### II-A. Semi-Independent Executor Contract

THINK, WRITE, and WORK may be implemented as semi-independent executors with separate prompts or strategies. They are capability-specialized components, not sovereign agents.

Constitutional constraints (mandatory):
- Stage-only: no executor may merge into canonical Record files.
- Evidence-linked output: every capability claim remains traceable.
- Knowledge boundary: no undocumented facts may be asserted as Record truth.
- User gate: conflicts between executors are resolved by user approval, not by executor arbitration.

Behavior shaping from SELF (three-dimension mind):
- IX-A Knowledge influences factual confidence and abstention thresholds.
- IX-B Curiosity influences exploration priority and query selection.
- IX-C Personality influences tone, framing, and interaction style.

Suggested default emphasis profile:

| Executor | Weight profile |
|----------|----------------|
| THINK | Curiosity > Knowledge > Personality |
| WRITE | Personality > Knowledge > Curiosity |
| WORK | Knowledge > Personality > Curiosity |

This profile is advisory and may be tuned per user while preserving the constitutional constraints above.

### WRITE (Production)

The user produces something. Grace-Mar captures and analyzes.

**Activities:**
- Daily journal entries
- Stories, creative writing
- Messages to friends/family
- Explanations, tutorials
- Essays, reports
- Lists, notes, plans
- Code, designs, diagrams

**What Grace-Mar captures:**
- Vocabulary (words used, range, sophistication)
- Sentence complexity (structure, length, variety)
- Narrative style (how they tell stories)
- Emotional expression (feelings, tone)
- Topics and interests (what they write about)
- Logical structure (argument, sequence)
- Growth trajectory (improvement over time)

**Example activity:**
> Student writes daily journal. Grace-Mar ingests each entry.
> After 30 days: vocabulary profile, style fingerprint, 
> topic map, emotional range, complexity baseline.

### THINK (Intake, Learning)

**Module intent:** THINK captures capability from evidence. When WORK has horizon goals (e.g. SAT), THINK prioritizes content and assessments that move the companion toward those goals. WORK reads THINK state to measure progress.

The user consumes content. Grace-Mar tracks and assesses comprehension.
THINK is multimodal by default and must not be limited to text.

**Activities:**
- Books read (with summaries, reactions)
- Articles, stories consumed
- Videos watched (educational, entertainment)
- Podcasts, audiobooks
- Music listening (songs, classical pieces, performances)
- Images, diagrams, maps, and visual media
- Instructions followed
- Conversations (what they took in)

**What Grace-Mar captures:**
- Content consumed (what they read/watched)
- Input modality (`text`, `video`, `audio/music`, `image/diagram/map`, or `mixed`)
- Source or artifact reference (title, URL, file path, or media id)
- Comprehension (can they summarize, explain?)
- Inference (can they predict, conclude?)
- Vocabulary acquisition (new words learned)
- Interest patterns (what they choose)
- Difficulty level (what's challenging vs easy)
- Reading velocity (speed, volume)

**Example activity:**
> Student reads chapter book, tells Grace-Mar what happened.
> Grace-Mar captures: comprehension level, new vocabulary,
> character understanding, plot inference, emotional response.

**SAT readiness (when WORK has SAT goal):** Add optional `sat_readiness` block in skill-think.md — maps THINK/MATH/Lexile to SAT domains (EBRW Reading, Math), defines trajectory and next milestones. Use **general principles** (comprehension at edge, inference through "why?", vocabulary in context, evidence "what in the story shows that?", simple choices that scale) — developmentally appropriate at companion's level; no SAT-specific mechanics for young companions. WORK reads this to measure progress. See pilot skill-think.md § SAT READINESS.

### WORK (Making, Planning, Execution, Exchange)

*(Internal identifier: BUILD container in skills.md; evidence CREATE-nnn, ACT-nnn. Kept for compatibility.)*

**Module intent:** WORK serves as tutor for the companion in the making, planning, execution, and creation domain — proposing activities at the container edge, answering questions, scaffolding next steps, aligned with work goals and life mission.

**Module objectives:** Implement and maintain the Grace-Mar Telegram and WeChat bots; develop and maintain the Grace-Mar web app at grace-mar.com; curate and maintain self-library.

The user makes things, plans, executes, or engages in exchange. Grace-Mar captures capability in building, delivery, and exchange. **Starts from zero** — no prior assumption. Grows only through pipeline input (human-gated).

**Activities:**
- Lemonade stand, crafts sale, bake sale
- School project with P&L (e.g., Airbnb, food truck)
- Content creation with audience (YouTube, blog)
- Allowance management, budgeting
- Following instructions to build (Legos, models, projects)
- Physical making (photo upload of things built)
- "We did X" involving planning, delivery, or exchange
- Any artifact showing goals, timelines, customer feedback, or financial outcome

**What Grace-Mar captures:**
- Planning (goals, timelines, milestones)
- Execution (follow-through, deliverables)
- Making (following instructions, assembly, construction)
- Customer/audience (who to serve, feedback received)
- Financial (basic money concepts, profit/loss, budgeting)
- Collaboration (teamwork, delegation, roles)
- Marketing (telling your story, reach)
- Decision-making (trade-offs, prioritization, saying no)

**Example activity:**
> Student participates in class food truck project. "We did X" + artifact (business plan, P&L).
> Grace-Mar captures: planning level, execution follow-through, financial understanding, teamwork.

**Integration with zero-human business vision:** The WORK module grows from evidence; when sufficient, the Record (including WORK) can inform agent-run businesses that act on the user's behalf. The user gates what enters; the module reflects demonstrated capability, not aspiration.

**Future API surface:** WORK is the natural integration point for external APIs — marketplaces, creation tools (e.g. Canva, design apps), planning/financial systems, content platforms, or any service that involves making, planning, execution, or exchange. The Record (BUILD container + evidence) would drive or constrain what those integrations can do on the companion's behalf; the companion remains the gate for what enters the Record.

**Creation and exploration (WORK):** Making includes creative output — drawings, paintings, crafts, inventions, designs. Grace-Mar captures creative capability alongside execution.

**Activities (creation):**
- Drawing, painting, crafts (image upload)
- Creative play and scenarios
- "What if" questions and answers
- Problem-solving (novel situations)
- Inventions, designs (conceptual)
- Hypotheticals, counterfactuals
- Games, puzzles, challenges

**What Grace-Mar captures (creation):**
- Originality (novel ideas, combinations)
- Elaboration (detail, richness)
- Flexibility (adapting to constraints)
- Visual expression (from artwork)
- Subject matter (what they choose to create)

**Companion work goals and life mission:**
- **work_goals** (skill-work.md): Companion's own objectives for making, planning, execution, creation — near_term, horizon; evidence-linked when captured. Gated.
- **life_mission** (self.md § VI VALUES): What they want to become or contribute. Identity-level; WORK goals align with it. See ID-TAXONOMY and SKILLS-MODULARITY.

---

## III. MODULE INTERACTIONS

The three modules are not isolated. Most activities engage multiple modules.

| Activity | Primary | Secondary |
|----------|---------|-----------|
| Write a story | WRITE | WORK |
| Summarize a book | THINK | WRITE |
| Solve a puzzle | WORK | — |
| Explain how something works | WRITE | THINK |
| Ask "what if" about a story | WORK | THINK |
| Journal about the day | WRITE | — |
| Follow instructions to build | THINK | WORK |
| Run a lemonade stand | WORK | WRITE |
| Class food truck project | WORK | THINK |
| Create content for audience | WORK | WRITE |
| Manage allowance, budget | WORK | — |
| Drawing, artwork, invention | WORK | — |

**Tagging rule:** Tag primary module; optionally tag secondary.
Evidence accrues to tagged modules.

### Skill modules vs. self (IX-A/B/C)

**Skill modules (THINK, WRITE, WORK) update only capability** — comprehension, production, making. They do *not* extract or write knowledge, curiosity, or personality into SELF.

**The analyst** (see ARCHITECTURE, pipeline) extracts patterns for **self-knowledge (IX-A), curiosity (IX-B), and personality (IX-C)** from the same inputs and stages candidates to RECURSION-GATE → SELF after companion approval.

So **one input** (e.g. art, music, journal, conversation) can update both: (1) a skill container (THINK/WRITE/WORK) for *capability*, and (2) SELF (IX-A/B/C) via analyst-staged candidates. The analyst serves SELF; the skill modules serve SKILLS.

---

## IV. SKILLS PHASE MODEL

All SKILLS operate within one of three phases.

### PHASE I — BUILDING (Default)

The user is actively building this skill through interaction.

Characteristics:
- Knowledge is accumulating
- Depth is increasing
- No formal verification required
- Record reflects what has been demonstrated

Permitted:
- Free teaching
- Exploration
- Mistakes and corrections
- Inconsistencies (user is learning)

### PHASE II — MILESTONE

A verification checkpoint has been reached.

Triggers:
- User declares "I know this now"
- Parent/teacher attests competence
- Threshold criteria met (e.g., 5+ teaching sessions)
- External verification (proctored demonstration)

Characteristics:
- Knowledge claim is formalized
- Verification level assigned
- Snapshot of current understanding
- Gaps explicitly identified

### PHASE III — ARCHIVED

Historical record of knowledge at a point in time.

Characteristics:
- Read-only
- Preserved as part of trajectory
- May be superseded by later learning
- Cannot be modified, only annotated

---

## III. CAPABILITY CLAIMS

Capability Claims are formal statements about what the user can do,
derived from accumulated activity evidence across the three modules.

Analogous to CMC's Recursive Learning Ledger (RLL): activities feed capability claims; claims accumulate; the Record improves over time. See [PIPELINE-MAP](pipeline-map.md#recursive-learning-process) for the full recursive learning definition.

### Capability Claim Structure

```typescript
interface CapabilityClaim {
  id: string;                    // CAP-WRITE-VOC-001
  module: 'WRITE' | 'THINK' | 'BUILD';
  dimension: string;             // "vocabulary", "comprehension", "originality"
  statement: string;             // "Uses age-appropriate vocabulary with variety"
  
  // Level
  level: 1 | 2 | 3 | 4 | 5;     // Developmental level
  
  // Verification
  verification_level: VerificationLevel;
  confidence_tier: 1 | 2 | 3 | 4;
  
  // Temporal
  first_demonstrated: Date;
  last_confirmed: Date;
  activity_count: number;        // Number of activities showing this
  
  // Evidence
  evidence: ActivityReference[]; // Links to activities
  
  // Status
  status: 'emerging' | 'established' | 'archived';
}
```

### Example Claims

```
CAP-WRITE-VOC-001
Module: WRITE
Dimension: vocabulary
Statement: Uses age-appropriate vocabulary (500+ unique words observed)
Level: 2
Evidence: 42 journal entries, 8 stories
Status: established

CAP-READ-COMP-001
Module: THINK
Dimension: comprehension
Statement: Can accurately summarize chapter-length narratives
Level: 3
Evidence: 15 book summaries, 90%+ accuracy
Status: established

CAP-BUILD-ORIG-001
Module: BUILD
Dimension: originality (creation)
Statement: Generates novel combinations (e.g., "dinosaur astronaut")
Level: 2
Evidence: 23 creative play sessions
Status: emerging

CAP-BUILD-PLAN-001
Module: BUILD
Dimension: planning
Statement: Can set goals and track milestones (e.g., food truck project)
Level: 1
Evidence: 1 group project, "we did X" + artifact
Status: emerging
```

### Verification Levels

| Level | Meaning | How Achieved |
|-------|---------|--------------|
| OBSERVED | System captured authentic activity | Activity records only |
| ATTESTED | Parent/teacher confirms capability | Third-party attestation |
| VERIFIED | Demonstrated in live session | Proctored demonstration |
| CERTIFIED | External formal verification | Standardized assessment |

### Confidence Tiers

| Tier | Confidence | Meaning |
|------|------------|---------|
| 1 | CERTIFIED | Externally verified, high confidence |
| 2 | VERIFIED | Demonstrated live, attested |
| 3 | OBSERVED | Based on captured activities |
| 4 | INFERRED | Pattern detected, limited evidence |

### Developmental Levels (per dimension)

Each module dimension has 5 developmental levels.

**WRITE.vocabulary**
| Level | Description |
|-------|-------------|
| 1 | Basic (100-300 words, simple) |
| 2 | Developing (300-600 words, some variety) |
| 3 | Competent (600-1000 words, situational) |
| 4 | Proficient (1000+ words, nuanced) |
| 5 | Advanced (rich, precise, domain-specific) |

**THINK.comprehension**
| Level | Description |
|-------|-------------|
| 1 | Recalls main events |
| 2 | Summarizes with key details |
| 3 | Identifies themes and motives |
| 4 | Analyzes author intent |
| 5 | Critiques and compares |

**BUILD.originality** (creation)
| Level | Description |
|-------|-------------|
| 1 | Recombines familiar elements |
| 2 | Creates novel combinations |
| 3 | Invents new scenarios |
| 4 | Generates unexpected connections |
| 5 | Produces genuinely surprising ideas |

---

## IV. CAPABILITY GAP LOG

Explicitly track underdeveloped areas.

Adapted from CMC's Negative Capability Zone.

### Purpose

- Prevents false confidence
- Identifies development opportunities
- Shows honest self-assessment
- Differentiates from polished credentials

### Gap Categories

| Category | Meaning |
|----------|---------|
| DEVELOPING | Actively working on, not yet competent |
| LIMITED_EVIDENCE | Few activities in this area |
| STRUGGLED | Attempted, found difficult |
| AGE_BOUNDARY | At edge of developmental expectation |
| NOT_ENGAGED | No activities in this area (neutral) |

### Gap Format

```
CAPABILITY GAP LOG

GAP-WRITE-LOGIC-001
  Module: WRITE
  Dimension: logic
  Status: DEVELOPING
  Observation: Sequential narratives strong; argument structure weak
  Evidence: 12 stories (all sequential), 0 persuasive pieces
  Suggested: Activities involving "convince me why..."
```

### Gap by Pillar Examples

**WRITE gaps:**
- Limited vocabulary range (relies on same 200 words)
- Simple sentence structures (no complex clauses)
- Weak logical organization

**THINK gaps:**
- Inference limited (misses implied meaning)
- Difficulty with non-fiction
- Low retention of factual content

**BUILD gaps (creation):**
- Ideas stay close to source material
- Struggles with "what if" questions
- Gives up quickly on novel problems

---

## V. STRUGGLE LOG

Track difficulties, not just successes.

Adapted from CMC's Failure-First Standard.

### Purpose

- Authentic mirroring includes struggles
- Shows how user learns from difficulty
- Reveals learning patterns and resilience
- Differentiates from curated profiles

### What to Capture

- Activities where user struggled
- Module dimensions that are difficult
- Emotional responses to difficulty
- Breakthrough moments
- Growth trajectory

### Format

```
STRUGGLE LOG

STRUGGLE-WRITE-001: Complex Sentences
  Module: WRITE
  Dimension: complexity
  First observed: 2026-03-01
  Status: RESOLVING
  
  Pattern: 
    Attempts multi-clause sentences but loses structure.
    Gets frustrated, reverts to simple sentences.
  
  Breakthrough (2026-03-18):
    Started using "because" and "so" connectors.
    Emotional shift: frustration → confidence.
  
  Evidence: Activities 0024, 0031, 0042, 0056

STRUGGLE-READ-001: Non-Fiction Comprehension
  Module: THINK
  Dimension: comprehension
  First observed: 2026-02-15
  Status: ONGOING
  
  Pattern:
    Strong with stories; struggles with factual text.
    Misses key points, focuses on tangential details.
  
  Suggested:
    More "explain what you learned" activities after
    non-fiction content.
```

### Struggle Types by Module

**WRITE struggles:**
- Vocabulary limitations
- Sentence complexity
- Organizing ideas logically
- Expressing emotions in words

**THINK struggles:**
- Comprehending complex text
- Making inferences
- Retaining factual information
- Following multi-step instructions

**BUILD struggles (creation):**
- Breaking from familiar patterns
- Sustaining creative play
- Logical reasoning chains
- Handling open-ended problems

---

## VI. ACTIVITY CAPTURE FORMAT

Structured capture of what the user produces.

### Activity Record

```
ACTIVITY ####

Date: [YYYY-MM-DD HH:MM]
Duration: [minutes]
Modality: voice | text | drawing | video | mixed

METADATA:
- Live capture: [yes/no]
- Biometric confirmed: [yes/no]
- Parent present: [yes/no]
- Device: [iPad/phone/computer]

ACTIVITY TYPE:
[journal | story | summary | question | conversation | creative | artwork | building | problem | business | project]

MODULE TAGS:
- Primary: [WRITE | THINK | BUILD]
- Secondary: [WRITE | THINK | BUILD | none]

CONTENT:
[Full text, transcript, image file, or description of activity content]

MODULE ANALYSIS:

If WRITE:
- Vocabulary: [word count, unique words, new words]
- Complexity: [avg sentence length, structure notes]
- Style: [narrative markers, tone]
- Expression: [emotional content]
- Topics: [subject tags]
- Logic: [structure, argument]

If THINK:
- Content consumed: [book, article, video title, music piece, image/diagram/map]
- Input modality: [text | video | audio_music | image_diagram_map | mixed]
- Source reference: [url | file path | media id | library id]
- Comprehension: [summary accuracy, key points captured]
- Inference: [conclusions drawn]
- Vocabulary: [new words encountered]

If BUILD (creation/artwork):
- Image file: [reference to uploaded image, if applicable]
- Prompt/trigger: [what sparked the creation]
- Subject matter: [what they drew/made]
- Elaboration: [detail level 1-5]
- Originality: [novel elements, unexpected choices]
- Technique: [developmental observations]
- Colors/mood: [emotional expression]
- Student description: [what they say about it]

If BUILD (planning/execution):
- Planning: [goals, timelines, milestones evidenced]
- Execution: [follow-through, deliverables]
- Financial: [P&L, budgeting, money concepts]
- Collaboration: [teamwork, roles, delegation]
- Artifact: [business plan, sales record, feedback, etc.]

SELF OBSERVATIONS (always):
- Linguistic markers: [notable phrases, vocabulary]
- Emotional tone: [enthusiastic, frustrated, neutral]
- Interests signaled: [topics gravitated toward]

VERIFICATION FLAGS:
- Temporal consistency: [normal/suspicious]
- Behavioral fingerprint match: [yes/no/uncertain]
- AI detection: [human/uncertain/flagged]
```

### Example: Journal Entry

```
ACTIVITY 0042

Date: 2026-03-15 19:30
Duration: 8 minutes
Modality: voice (transcribed)

METADATA:
- Live capture: yes
- Biometric confirmed: yes (voice match)
- Parent present: no
- Device: iPad

ACTIVITY TYPE: journal

MODULE TAGS:
- Primary: WRITE
- Secondary: none

CONTENT:
"Today was really fun because we went to the park and I played 
on the big slide. Maya was there and we pretended we were 
explorers looking for treasure. I found a cool rock that looks 
like a dinosaur egg. Mom said we can keep it. I want to go 
back tomorrow."

MODULE ANALYSIS:

WRITE:
- Vocabulary: 54 words, 42 unique, 0 new
- Complexity: avg 12 words/sentence, simple structure
- Style: narrative, sequential, present-focused
- Expression: positive, excited ("really fun", "cool")
- Topics: play, friends, nature, family
- Logic: temporal sequence (today → tomorrow)

SELF OBSERVATIONS:
- Linguistic markers: "really fun", "cool", sequential narrative
- Emotional tone: enthusiastic, happy
- Interests signaled: outdoor play, imagination games, nature

VERIFICATION FLAGS:
- Temporal consistency: normal
- Behavioral fingerprint match: yes
- AI detection: human
```

### Example: Artwork Upload

```
ACTIVITY 0058

Date: 2026-03-22 16:45
Duration: n/a (upload)
Modality: image

METADATA:
- Live capture: no (uploaded after)
- Biometric confirmed: n/a
- Parent present: yes (took photo)
- Device: iPad

ACTIVITY TYPE: artwork

MODULE TAGS:
- Primary: BUILD
- Secondary: none

CONTENT:
[Image: drawing_family_superheroes.jpg]

Student description (voice): "This is my family but we're all 
superheroes. Dad can fly, Mom has super strength, I can turn 
invisible, and my brother shoots lasers from his eyes."

MODULE ANALYSIS:

BUILD (image/artwork):
- Image file: drawing_family_superheroes.jpg
- Subject matter: family, superheroes, powers
- Elaboration: 4/5 (detailed costumes, background city)
- Originality: 3/5 (familiar superhero tropes, personalized)
- Technique: age-appropriate, confident lines
- Colors/mood: bright, happy, action-oriented
- Student description: assigned specific powers to each family member

SELF OBSERVATIONS:
- Interests signaled: superheroes, family, powers/abilities
- Emotional tone: playful, imaginative
- Relationships: included all family members, self has "invisible" power

VERIFICATION FLAGS:
- Temporal consistency: normal
- Image authenticity: appears original user artwork
```

---

## VII. MODULE STRUCTURE

Skills organize under the three modules, with sub-dimensions.

### Structure

```
SKILLS/
├── WRITE/
│   ├── vocabulary/           # Words used, range, sophistication
│   ├── complexity/           # Sentence structure, variety
│   ├── style/                # Narrative voice, tone
│   ├── expression/           # Emotional content, feeling
│   ├── topics/               # What they write about
│   ├── logic/                # Argument, sequence, structure
│   └── growth/               # Trajectory over time
│
├── THINK/
│   ├── comprehension/        # Understanding what was consumed
│   ├── inference/            # Conclusions beyond explicit
│   ├── vocabulary/           # Words acquired
│   ├── interests/            # What they choose to read
│   ├── difficulty/           # Level of challenge handled
│   ├── velocity/             # Speed, volume
│   └── content_log/          # What they've read
│
└── BUILD/
    ├── planning/             # Goals, timelines, milestones
    ├── execution/            # Follow-through, deliverables
    ├── customer_audience/    # Who to serve, feedback
    ├── financial/            # Money concepts, P&L, budgeting
    ├── collaboration/        # Teamwork, delegation, roles
    ├── marketing/            # Telling your story, reach
    ├── decision_making/      # Trade-offs, prioritization
    ├── originality/          # Novel ideas, combinations (creation)
    ├── elaboration/          # Detail, richness (creation)
    ├── flexibility/          # Adapting to constraints (creation)
    └── persistence/          # Sticking with hard problems
```

### Subject Knowledge

Traditional subjects (math, science, history) are NOT separate modules.
They are CONTEXTS where READ/WRITE/WORK are applied.

**Example: Math**
- READ: Understands math concepts, can interpret problems
- WRITE: Can produce correct solutions, explain reasoning
- WORK: Can solve novel problems, find patterns

**Example: History**
- READ: Knows historical events, can summarize periods
- WRITE: Can explain historical cause/effect
- WORK: Can reason about counterfactuals ("what if...")

Subject knowledge emerges from evidence across all three modules. WORK starts from zero; no evidence = no claims.

---

## VIII. DEPENDENCY MAPPING

Track prerequisites and unlocks.

### Prerequisite Chains

```
VKC-MATH-0001 (Counting)
    └── VKC-MATH-0002 (Addition)
        └── VKC-MATH-0003 (Subtraction)
            └── VKC-MATH-0004 (Multiplication)
                └── VKC-MATH-0005 (Division)
                    └── VKC-MATH-0006 (Fractions)
```

### Why This Matters

- Validates knowledge claims (can't know division without multiplication)
- Identifies gaps (missing prerequisite = likely struggle)
- Enables intelligent querying ("what should they learn next?")
- Detects suspicious patterns (advanced without basics)

---

## IX. INCONSISTENCY HANDLING

When new teaching contradicts previous teaching.

Adapted from CMC's Anomaly Flag Protocol.

### Inconsistency Types

| Type | Meaning | Resolution |
|------|---------|------------|
| GROWTH | Student learned/changed | Update, preserve history |
| ERROR | One session was wrong | Flag, seek clarification |
| CONTEXT | Both true in different contexts | Preserve both with context |
| RETRACTION | Student explicitly retracts | Archive old, note retraction |

### Inconsistency Format

```
INCONSISTENCY FLAG

ID: INC-001
Previous: "2 + 2 = 5" (Session 042)
Current: "2 + 2 = 4" (Session 067)
Type: ERROR → GROWTH
Resolution: Student corrected error after learning
Action: Update VKC, preserve history
```

### Principle

Do NOT silently reconcile. Preserve the tension.
Let the user's learning journey be visible.

---

## X. SNAPSHOTS

Preserve skills at points in time.

### Snapshot Triggers

- Age milestones (6, 8, 10, 12, 14, 16, 18)
- Grade transitions
- Major life events (moving, changing schools)
- On-demand (operator/user request)

### Snapshot Format

```
SKILLS–SNAPSHOT–[NAME]–AGE–[X]

Created: [YYYY-MM-DD]
Status: ARCHIVED

SUMMARY:
- Total VKCs: [count]
- Domains active: [list]
- Strongest domain: [domain]
- Current focus: [what they're learning now]

DOMAIN BREAKDOWN:
[For each active domain]
- VKC count: [n]
- Depth range: [1-3] to [3-5]
- Verification levels: [breakdown]

NOTABLE SKILLS:
- [Top 5 VKCs with highest depth/verification]

ACTIVE GAPS:
- [Current knowledge gaps]

LEARNING VELOCITY:
- [How fast they're acquiring skills]
```

### Preservation Rule

Snapshots are IMMUTABLE. They preserve who the user was.
Later learning does not modify snapshots.

---

## XI. CONTAINER EDGE TEACHING

The three modules are CONTAINERS that define current capability boundaries. The system proposes activities at the EDGE. The WORK module's BUILD container starts empty until evidence enters through the pipeline.

### Container State

Each module has a current boundary:

```
THINK Container:
├── Vocabulary: ~800 words (level 3)
├── Comprehension: chapter books (level 3)
├── Inference: basic predictions (level 2)
└── EDGE: longer books, 1-2 new words per session

WRITE Container:
├── Vocabulary: ~400 active words (level 2)
├── Complexity: simple sentences (level 2)
├── Expression: strong (level 3)
└── EDGE: compound sentences, connectors

BUILD Container (creation dimensions):
├── Originality: familiar recombinations (level 2)
├── Elaboration: moderate detail (level 3)
├── Flexibility: adapting to constraints
└── EDGE: novel combinations, longer chains
```

### Teaching at the Edge

| Zone | Description | System behavior |
|------|-------------|-----------------|
| Inside | Already knows/can do | Use as foundation, reference |
| Edge | Just beyond current | Propose activities here (optimal) |
| Outside | Too advanced | Don't go here yet |

### Gap vs Edge

**Gap:** Something INSIDE the container that's missing
- Fill gaps BEFORE extending edge
- Example: Can read but can't summarize → fill gap

**Edge:** The BOUNDARY of current capability
- Extend after gaps are filled
- Example: Ready for slightly harder books

### Implementation

When the system proposes activities or interacts:

1. Check container state (levels, gaps)
2. Use vocabulary FROM container (grounding)
3. Introduce concepts AT edge (growth)
4. Fill gaps before extending (foundations)
5. Never jump outside container (frustration)

---

## XII. QUERYING SKILLS

How evaluators interact with the SKILLS module.

### Pillar Queries

**WRITE capability:**
> "How well does [user] write?"
> Returns: Levels across vocabulary, complexity, style, expression, logic

**THINK capability:**
> "How well does [user] comprehend?"
> Returns: Levels across comprehension, inference, vocabulary acquisition

**WORK capability (includes creation):**
> "What business/planning/creation capability does [user] have?"
> Returns: Levels across planning, execution, financial, collaboration, originality, elaboration (or "no evidence yet" if container empty)

### Cross-Module Queries

**Overall profile:**
> "What are [user]'s cognitive strengths?"
> Returns: Module comparison, strongest dimensions

**Demonstration:**
> "Show me how [user] would explain [topic]"
> Returns: Record data + SELF context (optional emulation if enabled)

**Trajectory:**
> "How has [user]'s writing developed?"
> Returns: WRITE module growth over time, milestones, struggles

**Gap analysis:**
> "Where should [user] focus development?"
> Returns: Lowest dimensions, limited-evidence areas, struggles

### Example Query Responses

```
Query: "How well does [user] write?"

WRITE CAPABILITY PROFILE

Vocabulary:     ████████░░  Level 4 (Proficient)
Complexity:     ██████░░░░  Level 3 (Competent)
Style:          ███████░░░  Level 3.5 (Developing)
Expression:     █████████░  Level 4.5 (Strong)
Topics:         ████████░░  Level 4 (Varied)
Logic:          █████░░░░░  Level 2.5 (Developing)

Summary: Strong emotional expression and vocabulary;
logical organization is current growth area.

Evidence: 67 journal entries, 12 stories, 8 explanations
Last activity: 2 days ago
```

---

## XII. VERSIONING

### Version Control

- All Capability Claims are versioned
- Activities are immutable once captured
- Changes are timestamped
- History is preserved
- Deletions are not permitted (only archival)

### Audit Trail

Every modification to SKILLS must record:
- What changed
- When it changed
- Why it changed (activity reference, attestation, etc.)
- Previous value (preserved)

---

## XIII. INTEGRATION WITH SELF

SKILLS and SELF interact bidirectionally. WRITE is the primary data source for SELF.

### SELF → SKILLS (Prediction)

- Interests (SELF) predict which modules develop fastest
- Reasoning patterns (SELF) shape how WORK (creation) capability grows

### SKILLS → SELF (Inference)

**WRITE activities update SELF automatically:**

| WRITE dimension | Updates SELF component |
|-----------------|------------------------|
| vocabulary | linguistic_style.vocabulary_level |
| complexity | linguistic_style.sentence_patterns |
| style | linguistic_style.tone, verbal_habits |
| expression | emotional_patterns |
| topics | interests |
| content | linguistic_style.samples (raw examples) |

**Pipeline:**
```
Journal Entry → WRITE Analysis → SELF Update
                    │                  │
                    │                  └── vocabulary_level recalculated
                    │                  └── new sentence patterns detected
                    │                  └── verbal habits updated
                    │                  └── sample added to linguistic archive
                    │
                    └── WRITE capability claims updated
```

### The THINK → SELF Pipeline

Every THINK activity triggers a SELF update:

| THINK data | Updates SELF component |
|-----------|------------------------|
| content chosen | interests (topics they seek out) |
| genres preferred | preferences.favorites |
| themes returned to | values (what matters to them) |
| emotional reactions | emotional_patterns |
| re-reads | preferences (what they return to) |

**Example:**
```
THINK Activity: Finished "Charlotte's Web" (2nd read)
    │
    └── SELF updates:
        ├── interests: animals, farm life, friendship
        ├── preferences.favorites.books: ["Charlotte's Web", ...]
        ├── values: loyalty, sacrifice (inferred from theme)
        └── reading_patterns: re-reads favorites
```

### WORK → SELF

- Planning/collaboration style → reasoning_patterns
- Financial/values signals → values (if evidenced)
- Execution approach → personality (e.g., follow-through)
- Creative content (artwork, inventions) → interests (what they explore)

### Key Insight

WRITE is both:
1. A skill module (capability to produce)
2. The primary data source for SELF (how they express themselves)

The linguistic fingerprint lives in SELF but is derived from WRITE.

### Query Requiring Both

> "Write a journal entry the way [user] would."

Uses: SELF.linguistic_style (derived from WRITE) + SELF.interests + WRITE.topics

---

## XIV. COMPLIANCE CHECKLIST

Before marking any Capability Claim as ESTABLISHED:

- [ ] At least 5 activities demonstrating this capability
- [ ] Level assigned (1-5)
- [ ] Verification level assigned
- [ ] Confidence tier assigned
- [ ] Evidence linked (activity references)
- [ ] Inconsistencies resolved
- [ ] SELF observations captured from activities

Before creating SNAPSHOT:

- [ ] All module dimensions reviewed
- [ ] Gaps explicitly documented
- [ ] Struggles logged
- [ ] Module breakdown complete
- [ ] Summary written
- [ ] Timestamp recorded
- [ ] Marked as ARCHIVED (immutable)

---

END OF FILE — SKILLS–TEMPLATE v2.0
