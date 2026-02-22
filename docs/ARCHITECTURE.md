# cog-em Architecture

**Governed by**: [COG-EM-CORE v2.0](COG-EM-CORE.md)

---

## Core Principle

The cognitive fork separates **who the user is** from **what the user can do**, recording both as structured, evidence-grounded data that grows through interaction.

```
┌─────────────────────────────────────────────────────────────┐
│                     COGNITIVE FORK                          │
├─────────────────────────┬───────────────────────────────────┤
│         SELF            │            SKILLS                 │
│   (who they ARE)        │      (what they CAN DO)           │
├─────────────────────────┼───────────────────────────────────┤
│ • Personality           │ • Academic knowledge              │
│ • Linguistic style      │ • Practical abilities             │
│ • Life narrative        │ • Creative works                  │
│ • Preferences           │ • Domain expertise                │
│ • Values                │ • Problem-solving approaches      │
│ • Reasoning patterns    │ • Demonstrated competencies       │
└─────────────────────────┴───────────────────────────────────┘
```

---

## Fork Lifecycle

The fork follows a lifecycle analogous to a software fork:

```
SEED (Initial Fork)
  │  Capture snapshot: identity, personality, preferences,
  │  baselines, initial artifacts
  │
  ▼
INTERACT (Growth Through Use)
  │  Each session = a commit
  │  Writing, reading, creating, answering → recorded
  │  Containers fill, edges advance, SELF evolves
  │
  ▼
DIVERGE (Fork Develops Its Own History)
  │  Real person grows in the real world
  │  Fork grows through its interactions
  │  They may drift apart — by design
  │
  ▼
MERGE (Optional — Bring In New Data)
  │  User logs new books, skills, life events
  │  Parent reports new information (when young)
  │  System incorporates and continues
  │
  ▼
SNAPSHOT (Preserve State at a Point in Time)
     Git tags: pilot-001-age-6, pilot-001-age-7
     Immutable. Shows who the user was at that age.
```

**Single user, lifetime system.** There is no parent mode and no child mode. A parent helps when the user is young. The user grows into full ownership.

---

## Module 1: SELF (Identity Record)

Contains who the user IS — their identity, story, and way of being in the world.

**Core principle: Accurate recording.** The goal is faithful documentation of the user's actual personality, preferences, reasoning, and voice — not an idealized or curated version. The record should capture them as they are, including quirks and imperfections.

### Contents

| Component | Description | Example |
|-----------|-------------|---------|
| **Personality** | Observable behavioral tendencies | Creative, persistent, physical, strong-willed |
| **Linguistic style** | How they communicate | Vocabulary, sentence patterns, tone, verbal habits |
| **Life narrative** | Their story, memories, experiences | Family, places lived, significant events |
| **Preferences** | Likes, dislikes, tastes | Favorite books, movies, places, foods |
| **Values** | What matters to them | Bravery, kindness, creativity |
| **Reasoning patterns** | How they think through problems | Grinder, observer, pivoter |
| **Interests** | What captures their attention | Stories, science, space, animals |
| **Emotional patterns** | How they respond to situations | Cheers up sad friends, upset but keeps trying |

### Characteristics

- **Accurately recorded**: Captures the real person, not an idealized version
- **Relatively stable**: Changes slowly over years
- **Observed from interaction**: Emerges from what the user does and says
- **Seeded early**: Initial survey captures starting point
- **Inferred**: System detects patterns in user's activity
- **Narrative-rich**: Contains their story, not just traits

### Seeding (Initial Survey)

Simple favorites survey (5-10 minutes):

```
1. What are your favorite movies or shows?
2. What are your favorite books or stories?
3. What are your favorite places?
4. What are your favorite games?
```

Everything else is inferred from activity:
- Linguistic style ← WRITE activities
- Interests ← all pillars
- Personality ← observed patterns
- Values ← READ choices, WRITE content

### Evolution

The SELF record updates as the system observes:
- How the user explains things (linguistic fingerprint)
- What topics they gravitate toward (interests)
- How they respond to challenges (reasoning style)
- What they care about (values)

History is always preserved. Changes do not overwrite.

---

## Module 2: SKILLS (Capability Record)

Contains what the user CAN DO — capabilities that grow through authentic activity.

### The Four Pillars

Skills organize under four fundamental cognitive modes. The fourth (BUSINESS) starts from zero and grows with experience through the pipeline (human-gated).

| Pillar | Function | Activities |
|--------|----------|------------|
| **WRITE** | Production, expression | Journal, stories, explanations, messages |
| **READ** | Intake, comprehension | Books read, summaries, interpretations |
| **IMAGINE** | Creation, exploration | Creative play, hypotheticals, artwork, problem-solving |
| **BUSINESS** | Planning, execution, exchange | Lemonade stand, projects with P&L, content with audience, budgeting |

### Structure

```
SKILLS/
├── WRITE/
│   ├── vocabulary/       # Words used, range, sophistication
│   ├── complexity/       # Sentence structure, variety
│   ├── style/            # Narrative voice, tone
│   ├── expression/       # Emotional content
│   └── logic/            # Argument, sequence
│
├── READ/
│   ├── comprehension/    # Understanding content
│   ├── inference/        # Conclusions beyond explicit
│   ├── vocabulary/       # Words acquired
│   └── interests/        # What they choose
│
├── IMAGINE/
│   ├── originality/      # Novel ideas
│   ├── reasoning/        # Logical chains
│   ├── flexibility/      # Adapting to constraints
│   └── elaboration/      # Detail, richness
│
└── BUSINESS/
    ├── planning/         # Goals, timelines, milestones
    ├── execution/        # Follow-through, deliverables
    ├── financial/        # Money concepts, P&L, budgeting
    └── collaboration/    # Teamwork, delegation
```

### Activity-Based Growth

The user doesn't explicitly "teach" skills — they **do** things. cog-em observes and records.

```
Activity: Daily journal entry (WRITE)
├── Content captured: full text
├── Analysis: vocabulary, complexity, style, topics
├── SELF observations: linguistic markers, emotional tone
└── Capability claims updated: WRITE.vocabulary, WRITE.expression
```

### Characteristics

- **Activity-driven**: Grows from authentic production, not explicit teaching
- **Pillar-organized**: WRITE, READ, IMAGINE, BUSINESS as primary structure
- **Dimension-tracked**: Each pillar has measurable sub-dimensions
- **Level-based**: 5 developmental levels per dimension
- **Evidence-linked**: Every claim traces to captured activities

---

## Interaction Between Modules

### SELF → SKILLS (Prediction)

- **Interests** (SELF) predict which pillars develop fastest
- **Reasoning patterns** (SELF) shape IMAGINE capability growth

### SKILLS → SELF (Inference)

Each pillar feeds different SELF components:

```
WRITE Activity ──→ SELF.linguistic_style (primary source)
                   SELF.interests (topics written about)
                   SELF.emotional_patterns (expression)

READ Activity ───→ SELF.interests (what they choose)
                   SELF.preferences (content patterns)
                   SELF.values (themes they return to)

IMAGINE Activity → SELF.reasoning_patterns (how they think)
                   SELF.interests (what they explore)
```

### The WRITE → SELF Pipeline

Every WRITE activity triggers a SELF update:

| WRITE dimension | Updates SELF component |
|-----------------|------------------------|
| vocabulary | linguistic_style.vocabulary_level |
| complexity | linguistic_style.sentence_patterns |
| style | linguistic_style.tone, verbal_habits |
| expression | emotional_patterns |
| topics | interests |

### The READ → SELF Pipeline

Every READ activity triggers a SELF update:

| READ data | Updates SELF component |
|-----------|------------------------|
| content chosen | interests (topics they seek out) |
| genres preferred | preferences.favorites |
| themes returned to | values (what matters to them) |
| difficulty level | (informs developmental stage) |

### Both Required for Full Record

A complete cognitive fork needs both:
- SELF alone = personality without capability
- SKILLS alone = capabilities without character
- SELF + SKILLS = the full picture of this specific person

**Key insight:** WRITE is both a skill AND the primary data source for SELF.

---

## Evidence Grounding Principle

When the system interacts with the user, it should reference their own evidence.

### Grounding Sources

| Source | Use |
|--------|-----|
| **Writing Log** | Vocabulary, phrases, examples from their own writing |
| **Reading List** | References to books/content they've actually consumed |
| **Creation Log** | Examples from their own creative work |
| **SELF.narrative** | Their own stories, memories, relationships |

### Why This Matters

```
Generic system: "You might enjoy reading about dinosaurs."
Grounded system: "You wrote about Earth's layers last week and 
                  said you like learning about space. Maybe a 
                  book about what's inside other planets?"
```

The system should:
- Reference the user's actual work and data
- Connect new activities to prior evidence
- Anchor suggestions to their documented interests
- Never invent experiences or reference undocumented content

### Grounding Rules

1. **Reference their work** — Connect to Writing Log, Creation Log
2. **Reference their reading** — "Like in [book they read]..."
3. **Connect to their creations** — "Your drawing of [X] showed..."
4. **Anchor to their experiences** — "Like when you went to [place]..."
5. **Never invent experiences** — Only reference documented evidence

---

## Container Edge Principle

The four SKILLS pillars (READ, WRITE, IMAGINE, BUSINESS) are **containers** that define what the user currently knows and can do. The system proposes activities at the **edge** of these containers.

### The Container Model

```
┌─────────────────────────────────────────────────────────────┐
│                   TOO ADVANCED                               │
│              (beyond current reach)                          │
├─────────────────────────────────────────────────────────────┤
│ ░░░░░░░░░░░░░░░░ THE EDGE ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│   (zone of proximal development — optimal activity zone)    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              INSIDE THE CONTAINER                           │
│           (what they already know/can do)                   │
│                                                             │
│   READ: books read, vocabulary acquired                     │
│   WRITE: words used, complexity achieved                    │
│   IMAGINE: creativity demonstrated                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Activity Calibration

| Zone | What it means | System behavior |
|------|---------------|-----------------|
| Inside container | Already knows/can do | Reference, build on |
| At the edge | Just beyond current level | Propose activities here — optimal |
| Outside container | Too advanced | Don't go here yet |

### Gap Filling

The Capability Gap Log identifies holes INSIDE the container:

```
Container: WRITE
  │
  ├── Established: vocabulary, expression, topics
  ├── GAP: sentence boundaries (should be here, developing)
  └── Edge: paragraph structure (next to develop)

System: Fill the gap before extending the edge.
```

### Zone of Proximal Development

Activities proposed at the boundary of current capability, where the user can succeed with guidance.

- Too easy → boredom, no growth
- Too hard → frustration, shutdown
- At the edge → engagement, growth

---

## Query Modes

### Browse the Record (Primary)

> "What are [user]'s interests?" → SELF.interests
> "Show me [user]'s writing growth" → SKILLS.WRITE trajectory
> "What books has [user] read?" → EVIDENCE.reading_list
> "Show me [user]'s artwork" → EVIDENCE.creation_log

### Query Capabilities

> "How well does [user] write?" → SKILLS.WRITE levels
> "What's [user]'s reading comprehension level?" → SKILLS.READ
> "How creative/original is [user]?" → SKILLS.IMAGINE

### Query Both (Full Profile)

> "What are [user]'s cognitive strengths?" → SELF + SKILLS
> "Where should [user] focus development?" → Gaps + edges
> "Show me [user]'s growth trajectory" → Evidence over time

### Emulation Queries (Optional Future Feature)

If the user enables emulation:
> "Write a journal entry the way [user] would."
> "Explain [concept] the way [user] would explain it."

Emulation requires rich SELF + SKILLS data and explicit user opt-in.

---

## Data Model (Draft)

### SELF Schema

```typescript
interface Self {
  id: string;
  user_id: string;
  
  personality: {
    self_concept: string;
    traits: { trait: string; confidence: number }[];
    emotional_patterns: { trigger: string; response: string }[];
    humor: { style: string; trigger: string };
    empathy_mode: string;
    problem_solving: { style: string; approach: string };
    updated_at: Date;
  };
  
  linguistic_style: {
    vocabulary_level: number;
    sentence_patterns: string[];
    verbal_habits: string[];
    tone: string;
    samples: string[];
    updated_at: Date;
  };
  
  narrative: {
    family: { members: { name: string; relationship: string; notes: string }[] };
    places: { favorite_places: string[] };
    significant_events: { event: string; date: Date; impact: string }[];
    memories: { content: string; date_added: Date; emotional_tone: string }[];
  };
  
  preferences: {
    favorites: {
      movies: string[];
      books: string[];
      places: string[];
      activities: string[];
      foods: string[];
    };
    dislikes: string[];
    learning_preferences: string[];
  };
  
  values: {
    core: string[];
    inferred_from: string[];
    updated_at: Date;
  };
  
  reasoning_patterns: {
    style: string;
    approach_to_new: string;
    approach_to_hard: string;
    updated_at: Date;
  };
  
  interests: {
    current: { topic: string; intensity: number }[];
    historical: { topic: string; period: DateRange }[];
  };
  
  created_at: Date;
  updated_at: Date;
}
```

### SKILLS Schema

```typescript
interface Skills {
  id: string;
  user_id: string;
  
  pillars: {
    WRITE: PillarProfile;
    READ: PillarProfile;
    IMAGINE: PillarProfile;
  };
  
  activities: Activity[];
  capabilities: CapabilityClaim[];
  gaps: GapEntry[];
  struggles: StruggleEntry[];
  
  created_at: Date;
  updated_at: Date;
}

interface PillarProfile {
  dimensions: {
    [dimension: string]: {
      level: 1 | 2 | 3 | 4 | 5;
      confidence: number;
      activity_count: number;
      last_activity: Date;
    };
  };
}

interface Activity {
  id: string;
  date: Date;
  duration_minutes: number;
  modality: 'voice' | 'text' | 'image' | 'video' | 'mixed';
  activity_type: string;
  pillar_primary: 'WRITE' | 'READ' | 'IMAGINE' | 'BUSINESS';
  pillar_secondary?: 'WRITE' | 'READ' | 'IMAGINE' | 'BUSINESS';
  
  content: {
    text?: string;
    image_file?: string;
    user_description?: string;
  };
  
  analysis: {
    pillar_metrics: Record<string, any>;
    self_observations: {
      linguistic_markers: string[];
      emotional_tone: string;
      interests_signaled: string[];
    };
    image_analysis?: {
      subject_matter: string[];
      elaboration: 1 | 2 | 3 | 4 | 5;
      originality: 1 | 2 | 3 | 4 | 5;
      colors_mood: string;
    };
  };
  
  verification: {
    live_capture: boolean;
    biometric_confirmed: boolean;
    ai_detection: 'human' | 'uncertain' | 'flagged';
  };
}

interface CapabilityClaim {
  id: string;
  pillar: 'WRITE' | 'READ' | 'IMAGINE' | 'BUSINESS';
  dimension: string;
  statement: string;
  level: 1 | 2 | 3 | 4 | 5;
  
  verification_level: 'observed' | 'attested' | 'verified' | 'certified';
  confidence_tier: 1 | 2 | 3 | 4;
  
  first_demonstrated: Date;
  last_confirmed: Date;
  activity_count: number;
  evidence: string[];
  
  status: 'emerging' | 'established' | 'archived';
}
```

---

## Privacy Considerations

### SELF (Highly Sensitive)
- Contains personality, values, emotional patterns
- Highest privacy tier
- User-controlled access at all ages

### SKILLS (Sensitive)
- Contains capability data across READ/WRITE/IMAGINE/BUSINESS
- Can be shared for credential purposes
- Pillar-limited access possible

### Access Control

| Accessor | SELF Access | SKILLS Access |
|----------|-------------|---------------|
| User | Full | Full |
| Parent (user <12) | Full (custodial) | Full |
| Parent (user 12-18) | Summary | Full |
| Parent (user 18+) | None (unless granted) | None (unless granted) |
| Employer | None (unless granted) | Granted pillars only |
| University | None (unless granted) | Granted pillars only |

There is no parent mode — parents have age-appropriate access to the user's single system.

---

## Storage and Versioning

GitHub repository is the authoritative record store. Git IS the fork.

### Storage Model

```
GitHub Repository (rbtkhn/cog-em)
├── docs/                    # Templates and governance
├── users/
│   └── pilot-001/
│       ├── SELF.md          # Identity record
│       ├── SKILLS.md        # Capability record
│       ├── EVIDENCE.md      # Activity logs
│       ├── SESSION-LOG.md   # Interaction history
│       └── artifacts/       # Raw files (writing, artwork)
└── (future users...)
```

### Version Control

| Concept | Implementation |
|---------|----------------|
| Audit trail | Git commit history |
| Change tracking | Git diffs |
| Rollback | Git revert |
| Snapshots | Git tags (e.g., `pilot-001-age-6`) |
| Backup | GitHub remote |
| The fork itself | The git repository |

### Commit Protocol

Every session that updates user data:
1. Update relevant files (SELF, SKILLS, EVIDENCE)
2. Commit with descriptive message
3. Push to GitHub

### Snapshots

Age-based snapshots = git tags:
```
git tag pilot-001-age-6 -m "Snapshot at age 6"
```

Tags preserve the exact state at that point in time.

---

## Emulation Layer

The cognitive fork can optionally power an **emulation** — a live conversational interface that behaves as the self would. The pilot supports Telegram (`bot/bot.py`) and WeChat (`bot/wechat_bot.py`). Both share the same emulation core (`bot/core.py`) and use the SELF profile to generate responses constrained to the self's knowledge, vocabulary, and personality.

### The Observation Window Model

The fork exists inside the user's mind. It is the user's mental model of the self, made explicit and structured.

The emulation layer (Telegram, WeChat, or other bot adapters) is not where the fork lives — it is an **observation window**. The user selectively exposes thoughts and information to the fork's awareness through this window. The fork processes what it observes, and the user decides what takes permanent root.

```
┌──────────────────────────────────────────────────┐
│                  USER'S MIND                      │
│                                                    │
│   ┌──────────────────────────────┐                │
│   │      COGNITIVE FORK          │                │
│   │   (structured in SELF.md)    │                │
│   └──────────────┬───────────────┘                │
│                  │                                 │
│          ┌───────┴───────┐                        │
│          │  OBSERVATION   │                        │
│          │    WINDOW      │                        │
│          └───────┬───────┘                        │
│                  │                                 │
└──────────────────┼─────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │  Emulation Layer │
          │ (Telegram/WeChat)│
          └─────────────────┘
```

The emulation layer enforces a **knowledge boundary**: the fork can only reference what has been explicitly merged into its profile. LLM world knowledge must not leak through.

---

## Input Channels

The fork's profile grows through two independent input channels. Both feed the same gated pipeline and the same profile files.

### Channel 1: Bot (Automated)

Conversations in the Telegram or WeChat bot are analyzed by an LLM analyst (`ANALYST_PROMPT` in `bot/prompt.py`). The analyst detects profile-relevant signals and stages candidates in `PENDING-REVIEW.md`. This runs automatically after bot exchanges.

```
User ↔ Bot conversation
       │
       ▼
  Analyst (LLM)
       │
       ▼
  PENDING-REVIEW.md (staged candidates)
       │
       ▼
  User approves/rejects
       │
       ▼
  SELF.md, EVIDENCE.md, prompt.py updated
```

### Channel 2: Operator (Manual)

The user brings real-world observations directly — school worksheets, art projects, overheard conversations, anything observed outside the bot. The operator (this conversation, or any session with the system maintainer) runs signal detection manually and stages candidates the same way.

```
User: "we learned about volcanoes today" [+ optional artifact]
       │
       ▼
  Operator runs signal detection
       │
       ▼
  PENDING-REVIEW.md (staged candidates)
       │
       ▼
  User approves/rejects
       │
       ▼
  SELF.md, EVIDENCE.md, prompt.py updated
```

### The "we" Convention

When the user says **"we [did X]"** in the operator channel, it is a **pipeline invocation**. The operator should immediately run signal detection and present staged candidates — no acknowledgment step, no waiting for a separate "process" command. The word "we" means: "I observed the self doing this; process it."

Examples:
- "we learned about volcanoes today" → run pipeline
- "we painted a pharaoh at school" → run pipeline
- "we read a book about robots" → run pipeline

The user's statement (and any attached artifact) serves as the evidence.

---

## Gated Pipeline

All profile changes — from either input channel — pass through a user-controlled gate. Nothing is committed to the fork without explicit approval.

### Signal Types

The analyst (automated or manual) detects three categories of signal:

| Category | What it captures | Profile target |
|----------|-----------------|----------------|
| **Knowledge** | Facts entering the self's awareness | IX-A in SELF.md |
| **Curiosity** | Topics that catch attention, engagement signals | IX-B in SELF.md |
| **Personality** | Behavioral patterns, speech traits, values, art style | IX-C in SELF.md |

### Pipeline Stages

1. **Signal detection** — Identify profile-relevant information in the input
2. **Candidate staging** — Write structured candidates to `PENDING-REVIEW.md` with analysis and recommendations
3. **User review** — User approves, rejects, or modifies each candidate
4. **Integration** — Approved candidates are merged into `SELF.md` (profile), `EVIDENCE.md` (evidence log), `bot/prompt.py` (emulation prompt), and `SESSION-LOG.md` (history)

### Candidate Structure

Each candidate specifies:
- `mind_category`: knowledge, curiosity, or personality
- `signal_type`: the specific type of signal detected
- `summary`: what was observed
- `profile_target`: which section of SELF.md it updates
- `suggested_entry`: the proposed profile text
- `prompt_section`: which part of the emulation prompt to update

### The Gate

The gate is the user's discernment. The system proposes; the user disposes. This is not a technical filter — it reflects the user's judgment about what matters and what should become part of the fork's permanent record.

---

## Three-Channel Mind Model

Post-seed growth is organized into three channels within Section IX of SELF.md. The seed baseline (Sections I–VIII) remains intact; these channels capture everything learned after seeding.

### IX-A. Knowledge

Facts that entered the self's awareness through observation. Each entry records what was learned, the source, and how the self would express it in their own words.

### IX-B. Curiosity

Topics that caught the self's attention — what they're drawn to, what resonates. Tracked with an intensity score and the triggering signal. Distinct from seed interests (Section VI) because these emerge from post-seed observation.

### IX-C. Personality (Observed)

Emergent behavioral patterns detected through the observation window. Art media choices, speech patterns, emotional responses, value expressions. These are not declared traits — they are observed and documented.

### Multi-Channel Signals

A single artifact can generate entries in all three channels simultaneously. For example, a painted pharaoh portrait produces:
- **Knowledge**: Egyptian pharaohs / King Tut's death mask
- **Curiosity**: Deepening engagement with ancient Egypt
- **Personality**: First use of paint as art medium, bold color choices

This mirrors how real cognition works — a single experience produces knowledge, interest, and identity signals at the same time.

---

*Document version: 3.0*
*Last updated: February 2026*
