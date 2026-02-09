# SKILLS–TEMPLATE v1.1

Cognitive Emulator · Skills Module Governance Template

Status: DRAFT
Version: 1.1
Last Update: February 2026

Adapted from: CIV–SCHOLAR–TEMPLATE v3.1 (CMC)

---

## I. PURPOSE

This template governs the SKILLS module of the cognitive twin.

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
cog-em observes, records, and infers capability from accumulated evidence.

---

## II. THE THREE PILLARS

All skills organize under three fundamental cognitive modes.

### WRITE (Production)

The user produces something. cog-em captures and analyzes.

**Activities:**
- Daily journal entries
- Stories, creative writing
- Messages to friends/family
- Explanations, tutorials
- Essays, reports
- Lists, notes, plans
- Code, designs, diagrams

**What cog-em captures:**
- Vocabulary (words used, range, sophistication)
- Sentence complexity (structure, length, variety)
- Narrative style (how they tell stories)
- Emotional expression (feelings, tone)
- Topics and interests (what they write about)
- Logical structure (argument, sequence)
- Growth trajectory (improvement over time)

**Example activity:**
> Student writes daily journal. cog-em ingests each entry.
> After 30 days: vocabulary profile, style fingerprint, 
> topic map, emotional range, complexity baseline.

### READ (Intake)

The user consumes content. cog-em tracks and assesses comprehension.

**Activities:**
- Books read (with summaries, reactions)
- Articles, stories consumed
- Videos watched (educational, entertainment)
- Podcasts, audiobooks
- Instructions followed
- Maps, diagrams interpreted
- Conversations (what they took in)

**What cog-em captures:**
- Content consumed (what they read/watched)
- Comprehension (can they summarize, explain?)
- Inference (can they predict, conclude?)
- Vocabulary acquisition (new words learned)
- Interest patterns (what they choose)
- Difficulty level (what's challenging vs easy)
- Reading velocity (speed, volume)

**Example activity:**
> Student reads chapter book, tells cog-em what happened.
> cog-em captures: comprehension level, new vocabulary,
> character understanding, plot inference, emotional response.

### IMAGINE (Creation/Exploration)

The user thinks beyond what's given. cog-em captures creative and reasoning capability.

**Activities:**
- Creative play and scenarios
- "What if" questions and answers
- Problem-solving (novel situations)
- Inventions, designs
- Hypotheticals, counterfactuals
- Drawing, painting, crafts (image upload)
- Building, making (photo upload)
- Games, puzzles, challenges
- Planning future events

**Input modalities:**
- Voice/text (describing creative play)
- Image upload (artwork, drawings, crafts)
- Photo upload (things they built/made)
- Video (creative performances)

**What cog-em captures:**
- Originality (novel ideas, combinations)
- Reasoning (logical steps, if-then)
- Pattern-finding (connections, analogies)
- Flexibility (adapting to constraints)
- Elaboration (detail, richness)
- Risk tolerance (safe vs wild ideas)
- Persistence (sticking with hard problems)
- Visual expression (from artwork)
- Subject matter (what they choose to create)

**Example activity (verbal):**
> Student plays "what would happen if dinosaurs came back?"
> cog-em captures: reasoning chains, creative elements,
> knowledge applied, narrative construction.

**Example activity (image upload):**
> Student uploads drawing of "my family as superheroes"
> cog-em captures: subject matter (family, superheroes),
> elaboration (detail level), originality (power choices),
> interests (superheroes), relationships (who's included).

---

## III. PILLAR INTERACTIONS

The three pillars are not isolated. Most activities engage multiple pillars.

| Activity | Primary | Secondary |
|----------|---------|-----------|
| Write a story | WRITE | IMAGINE |
| Summarize a book | READ | WRITE |
| Solve a puzzle | IMAGINE | — |
| Explain how something works | WRITE | READ |
| Ask "what if" about a story | IMAGINE | READ |
| Journal about the day | WRITE | — |
| Follow instructions to build | READ | IMAGINE |

**Tagging rule:** Tag primary pillar; optionally tag secondary.
Evidence accrues to tagged pillars.

---

## IV. SKILLS PHASE MODEL

All SKILLS operate within one of three phases.

### PHASE I — BUILDING (Default)

The user is actively teaching this skill to the twin.

Characteristics:
- Knowledge is accumulating
- Depth is increasing
- No formal verification required
- Twin reflects what has been taught

Permitted:
- Free teaching
- Exploration
- Mistakes and corrections
- Inconsistencies (user is learning)

### PHASE II — MILESTONE

A verification checkpoint has been reached.

Triggers:
- Student declares "I know this now"
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
derived from accumulated activity evidence across the three pillars.

Analogous to CMC's Recursive Learning Ledger (RLL).

### Capability Claim Structure

```typescript
interface CapabilityClaim {
  id: string;                    // CAP-WRITE-VOC-001
  pillar: 'WRITE' | 'READ' | 'IMAGINE';
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
Pillar: WRITE
Dimension: vocabulary
Statement: Uses age-appropriate vocabulary (500+ unique words observed)
Level: 2
Evidence: 42 journal entries, 8 stories
Status: established

CAP-READ-COMP-001
Pillar: READ
Dimension: comprehension
Statement: Can accurately summarize chapter-length narratives
Level: 3
Evidence: 15 book summaries, 90%+ accuracy
Status: established

CAP-IMAGINE-ORIG-001
Pillar: IMAGINE
Dimension: originality
Statement: Generates novel combinations (e.g., "dinosaur astronaut")
Level: 2
Evidence: 23 creative play sessions
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

Each pillar dimension has 5 developmental levels.

**WRITE.vocabulary**
| Level | Description |
|-------|-------------|
| 1 | Basic (100-300 words, simple) |
| 2 | Developing (300-600 words, some variety) |
| 3 | Competent (600-1000 words, situational) |
| 4 | Proficient (1000+ words, nuanced) |
| 5 | Advanced (rich, precise, domain-specific) |

**READ.comprehension**
| Level | Description |
|-------|-------------|
| 1 | Recalls main events |
| 2 | Summarizes with key details |
| 3 | Identifies themes and motives |
| 4 | Analyzes author intent |
| 5 | Critiques and compares |

**IMAGINE.originality**
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
  Pillar: WRITE
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

**READ gaps:**
- Inference limited (misses implied meaning)
- Difficulty with non-fiction
- Low retention of factual content

**IMAGINE gaps:**
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
- Pillar dimensions that are difficult
- Emotional responses to difficulty
- Breakthrough moments
- Growth trajectory

### Format

```
STRUGGLE LOG

STRUGGLE-WRITE-001: Complex Sentences
  Pillar: WRITE
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
  Pillar: READ
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

### Struggle Types by Pillar

**WRITE struggles:**
- Vocabulary limitations
- Sentence complexity
- Organizing ideas logically
- Expressing emotions in words

**READ struggles:**
- Comprehending complex text
- Making inferences
- Retaining factual information
- Following multi-step instructions

**IMAGINE struggles:**
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
[journal | story | summary | question | conversation | creative | artwork | building | problem]

PILLAR TAGS:
- Primary: [WRITE | READ | IMAGINE]
- Secondary: [WRITE | READ | IMAGINE | none]

CONTENT:
[Full text, transcript, image file, or description of activity content]

PILLAR ANALYSIS:

If WRITE:
- Vocabulary: [word count, unique words, new words]
- Complexity: [avg sentence length, structure notes]
- Style: [narrative markers, tone]
- Expression: [emotional content]
- Topics: [subject tags]
- Logic: [structure, argument]

If READ:
- Content consumed: [book, article, video title]
- Comprehension: [summary accuracy, key points captured]
- Inference: [conclusions drawn]
- Vocabulary: [new words encountered]

If IMAGINE (verbal):
- Prompt/trigger: [what sparked the imagination]
- Originality: [novel elements]
- Reasoning: [logical chains]
- Elaboration: [detail level 1-5]

If IMAGINE (image/artwork):
- Image file: [reference to uploaded image]
- Subject matter: [what they drew/made]
- Elaboration: [detail level 1-5]
- Originality: [novel elements, unexpected choices]
- Technique: [developmental observations]
- Colors/mood: [emotional expression]
- Student description: [what they say about it]

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

PILLAR TAGS:
- Primary: WRITE
- Secondary: none

CONTENT:
"Today was really fun because we went to the park and I played 
on the big slide. Maya was there and we pretended we were 
explorers looking for treasure. I found a cool rock that looks 
like a dinosaur egg. Mom said we can keep it. I want to go 
back tomorrow."

PILLAR ANALYSIS:

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

PILLAR TAGS:
- Primary: IMAGINE
- Secondary: none

CONTENT:
[Image: drawing_family_superheroes.jpg]

Student description (voice): "This is my family but we're all 
superheroes. Dad can fly, Mom has super strength, I can turn 
invisible, and my brother shoots lasers from his eyes."

PILLAR ANALYSIS:

IMAGINE (image/artwork):
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
- Image authenticity: appears original child artwork
```

---

## VII. PILLAR STRUCTURE

Skills organize under the three pillars, with sub-dimensions.

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
├── READ/
│   ├── comprehension/        # Understanding what was consumed
│   ├── inference/            # Conclusions beyond explicit
│   ├── vocabulary/           # Words acquired
│   ├── interests/            # What they choose to read
│   ├── difficulty/           # Level of challenge handled
│   ├── velocity/             # Speed, volume
│   └── content_log/          # What they've read
│
└── IMAGINE/
    ├── originality/          # Novel ideas, combinations
    ├── reasoning/            # Logical steps, if-then
    ├── patterns/             # Connections, analogies
    ├── flexibility/          # Adapting to constraints
    ├── elaboration/          # Detail, richness
    ├── risk/                 # Safe vs wild ideas
    └── persistence/          # Sticking with hard problems
```

### Subject Knowledge

Traditional subjects (math, science, history) are NOT separate pillars.
They are CONTEXTS where READ/WRITE/IMAGINE are applied.

**Example: Math**
- READ: Understands math concepts, can interpret problems
- WRITE: Can produce correct solutions, explain reasoning
- IMAGINE: Can solve novel problems, find patterns

**Example: History**
- READ: Knows historical events, can summarize periods
- WRITE: Can explain historical cause/effect
- IMAGINE: Can reason about counterfactuals ("what if...")

Subject knowledge emerges from evidence across all three pillars.

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
- On-demand (parent/user request)

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

The three pillars are CONTAINERS that define current capability boundaries. The twin teaches at the EDGE.

### Container State

Each pillar has a current boundary:

```
READ Container:
├── Vocabulary: ~800 words (level 3)
├── Comprehension: chapter books (level 3)
├── Inference: basic predictions (level 2)
└── EDGE: longer books, 1-2 new words per session

WRITE Container:
├── Vocabulary: ~400 active words (level 2)
├── Complexity: simple sentences (level 2)
├── Expression: strong (level 3)
└── EDGE: compound sentences, connectors

IMAGINE Container:
├── Originality: familiar recombinations (level 2)
├── Reasoning: basic if-then (level 2)
├── Elaboration: moderate detail (level 3)
└── EDGE: novel combinations, longer chains
```

### Teaching at the Edge

| Zone | Description | Twin behavior |
|------|-------------|---------------|
| Inside | Already knows/can do | Use as foundation, reference |
| Edge | Just beyond current | Teach here (optimal) |
| Outside | Too advanced | Don't go here yet |

### Gap vs Edge

**Gap:** Something INSIDE the container that's missing
- Fill gaps BEFORE extending edge
- Example: Can read but can't summarize → fill gap

**Edge:** The BOUNDARY of current capability
- Extend after gaps are filled
- Example: Ready for slightly harder books

### Implementation

When the twin communicates:

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

**READ capability:**
> "How well does [user] comprehend?"
> Returns: Levels across comprehension, inference, vocabulary acquisition

**IMAGINE capability:**
> "How creative/original is [user]?"
> Returns: Levels across originality, reasoning, flexibility, elaboration

### Cross-Pillar Queries

**Overall profile:**
> "What are [user]'s cognitive strengths?"
> Returns: Pillar comparison, strongest dimensions

**Demonstration:**
> "Show me how [user] would explain [topic]"
> Returns: Twin demonstrates in user's style (WRITE + SELF)

**Trajectory:**
> "How has [user]'s writing developed?"
> Returns: WRITE pillar growth over time, milestones, struggles

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

- Interests (SELF) predict which pillars develop fastest
- Reasoning patterns (SELF) shape how IMAGINE capability grows

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

### The READ → SELF Pipeline

Every READ activity triggers a SELF update:

| READ data | Updates SELF component |
|-----------|------------------------|
| content chosen | interests (topics they seek out) |
| genres preferred | preferences.favorites |
| themes returned to | values (what matters to them) |
| emotional reactions | emotional_patterns |
| re-reads | preferences (what they return to) |

**Example:**
```
READ Activity: Finished "Charlotte's Web" (2nd read)
    │
    └── SELF updates:
        ├── interests: animals, farm life, friendship
        ├── preferences.favorites.books: ["Charlotte's Web", ...]
        ├── values: loyalty, sacrifice (inferred from theme)
        └── reading_patterns: re-reads favorites
```

### IMAGINE → SELF

- Creative content → interests (what they explore)
- Problem-solving approach → reasoning_patterns
- Risk-taking in ideas → personality.traits

### Key Insight

WRITE is both:
1. A skill pillar (capability to produce)
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

- [ ] All pillar dimensions reviewed
- [ ] Gaps explicitly documented
- [ ] Struggles logged
- [ ] Pillar breakdown complete
- [ ] Summary written
- [ ] Timestamp recorded
- [ ] Marked as ARCHIVED (immutable)

---

END OF FILE — SKILLS–TEMPLATE v1.1
