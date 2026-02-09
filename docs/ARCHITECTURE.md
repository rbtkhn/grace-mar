# cog-em Architecture

**Governed by**: [COG-EM-CORE v1.0](COG-EM-CORE.md)

---

## Core Principle

The cognitive emulator separates **who the user is** from **what the user knows**.

```
┌─────────────────────────────────────────────────────────────┐
│                     COGNITIVE TWIN                          │
├─────────────────────────┬───────────────────────────────────┤
│         SELF            │            SKILLS                 │
│   (authentic mirror)    │        (knowledge modules)        │
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

## Module 1: SELF (Personality Module)

**Analogue to CMC's MIND files.**

Contains who the user IS — their identity, story, and way of being in the world.

**Core principle: Authentic mirroring.** The goal is faithful reproduction of the user's actual self, not an idealized or curated version. The twin should think, speak, and reason the way the user actually does — including quirks, biases, and imperfections.

### Contents

| Component | Description | Example |
|-----------|-------------|---------|
| **Personality** | Observable behavioral tendencies | Curious, methodical, shy, impulsive |
| **Linguistic style** | How they communicate | Vocabulary, sentence patterns, tone, verbal habits |
| **Life narrative** | Their story, memories, experiences | Family, places lived, significant events, relationships |
| **Preferences** | Likes, dislikes, tastes | Favorite books, movies, places, foods, people |
| **Values** | What matters to them | Fairness, creativity, family, achievement |
| **Reasoning patterns** | How they think through problems | Visual, sequential, intuitive, cautious |
| **Interests** | What captures their attention | Dinosaurs, music, building things |
| **Emotional patterns** | How they respond to situations | Cautious with new things, excited by challenges |

### Characteristics

- **Authentic mirroring**: Faithful reproduction, not idealization
- **Relatively stable**: Changes slowly over years
- **Observed, not taught**: Emerges from interaction patterns
- **Seeded early**: Initial survey captures starting point
- **Inferred**: System detects patterns in how user teaches
- **Narrative-rich**: Contains their story, not just traits

### Authentic Mirroring Principle

The SELF module strives to mirror the user as they actually are:

| Include | Exclude |
|---------|---------|
| Actual vocabulary (including "um", "like") | Polished, idealized speech |
| Real preferences (even embarrassing ones) | Curated, socially-desirable answers |
| Actual reasoning patterns (including biases) | Corrected, "better" reasoning |
| Their version of events | Objective third-party account |
| Quirks and imperfections | Normalized, generic personality |

**Why this matters:**
- Employers want to know the real person, not a polished facade
- The twin should answer "how would [user] think about X?" accurately
- Authenticity builds trust in the credential

**Validation test (recognition):**
- The user should recognize themselves in the twin
- Others who know the user should recognize them through the twin

If a parent, teacher, or friend interacts with the twin and says "yes, that's exactly how [user] would say that" — the SELF module is working. If they say "that doesn't sound like them" — it's not.

### Seeding (Initial Survey)

Simple favorites survey (5-10 minutes):

```
1. What are your favorite movies or shows?
2. What are your favorite books or stories?
3. What are your favorite places?
4. What are your favorite games?
```

That's it. Everything else is inferred from activity:
- Linguistic style ← WRITE activities
- Interests ← all pillars
- Personality ← observed patterns
- Values ← READ choices, WRITE content

### Evolution

The SELF module updates as the system observes:
- How the user explains things (linguistic fingerprint)
- What topics they gravitate toward (interests)
- How they respond to challenges (reasoning style)
- What they care about (values)

---

## Module 2: SKILLS (Capability Modules)

**Analogue to CMC's MEM files.**

Contains what the user CAN DO — capabilities that grow through authentic activity.

### The Three Pillars

Skills organize under three fundamental cognitive modes:

| Pillar | Function | Activities |
|--------|----------|------------|
| **WRITE** | Production, expression | Journal, stories, explanations, messages |
| **READ** | Intake, comprehension | Books read, summaries, interpretations |
| **IMAGINE** | Creation, exploration | Creative play, hypotheticals, problem-solving |

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
└── IMAGINE/
    ├── originality/      # Novel ideas
    ├── reasoning/        # Logical chains
    ├── flexibility/      # Adapting to constraints
    └── elaboration/      # Detail, richness
```

### Activity-Based Growth

The user doesn't "teach" skills — they **do** things. cog-em observes and infers.

```
Activity: Daily journal entry (WRITE)
├── Content captured: full text
├── Analysis: vocabulary, complexity, style, topics
├── SELF observations: linguistic markers, emotional tone
└── Capability claims updated: WRITE.vocabulary, WRITE.expression
```

### Characteristics

- **Activity-driven**: Grows from authentic production, not explicit teaching
- **Pillar-organized**: WRITE, READ, IMAGINE as primary structure
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
| emotional reactions | emotional_patterns |

**Example:**
```
READ: "Charlotte's Web" (3rd time), "Magic Tree House #12", "Dinosaur encyclopedia"

SELF inferences:
├── interests: animals, adventure, dinosaurs
├── preferences.favorites.books: ["Charlotte's Web", ...]
├── values: friendship (Charlotte's Web theme)
└── reading_patterns: re-reads favorites, explores series
```

### Both Required for Emulation

A true cognitive twin needs both:
- SELF alone = personality without capability
- SKILLS alone = capabilities without character
- SELF + SKILLS = produces output like this specific person

**Key insight:** WRITE is both a skill AND the primary data source for SELF.

---

## Response Grounding Principle

When the twin responds to queries, it should draw from the user's own evidence.

### Grounding Sources

| Source | Use |
|--------|-----|
| **Writing Log** | Vocabulary, phrases, examples from their own writing |
| **Reading List** | References to books/content they've actually consumed |
| **Creation Log** | Examples from their own creative work |
| **SELF.narrative** | Their own stories, memories, relationships |

### Why This Matters

```
Generic AI: "You might enjoy reading about dinosaurs."
Cognitive Twin: "Remember when you read that dinosaur encyclopedia 
                 and wrote about the T-Rex in your journal? Like that."
```

The twin should:
- Use the user's actual vocabulary (from Writing Log)
- Reference books they've read (from Reading List)
- Recall their own creations (from Creation Log)
- Mention their real experiences (from SELF.narrative)

### Implementation

```
Query: "What should I learn next?"

Response generation:
1. Load SELF.interests → dinosaurs, space, building
2. Load Reading List → books read, gaps
3. Load Writing Log → recent topics, vocabulary level
4. Generate response GROUNDED in their evidence

Output: "You've been writing a lot about dinosaurs lately, 
        and you finished that Magic Tree House about the moon. 
        Maybe a book about what dinosaurs would do in space?"
```

### Grounding Rules

1. **Prefer user's own words** — Use phrases from Writing Log
2. **Reference their reading** — "Like in [book they read]..."
3. **Connect to their creations** — "Remember when you drew..."
4. **Anchor to their experiences** — "Like when you went to [place]..."
5. **Never invent experiences** — Only reference documented evidence

---

## Container Edge Principle

The three SKILLS pillars (READ, WRITE, IMAGINE) are **containers** that define what the user currently knows and can do. The twin communicates at the **edge** of these containers.

### The Container Model

```
┌─────────────────────────────────────────────────────┐
│                   TOO ADVANCED                       │
│              (beyond current reach)                  │
├─────────────────────────────────────────────────────┤
│ ░░░░░░░░░░░░░░░░ THE EDGE ░░░░░░░░░░░░░░░░░░░░░░░░░ │
│   (zone of proximal development — where to teach)   │
├─────────────────────────────────────────────────────┤
│                                                     │
│              INSIDE THE CONTAINER                   │
│           (what they already know/can do)           │
│                                                     │
│   READ: books read, vocabulary acquired             │
│   WRITE: words used, complexity achieved            │
│   IMAGINE: creativity demonstrated                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Communication at the Edge

| Zone | What it means | Twin behavior |
|------|---------------|---------------|
| Inside container | Already knows/can do | Reference, don't teach |
| At the edge | Just beyond current level | Teach here — optimal |
| Outside container | Too advanced | Don't go here yet |

### How the Twin Finds the Edge

**READ container edge:**
```
Current: Reading chapter books, vocabulary ~800 words
Edge: Slightly longer books, 1-2 new words per session
Too far: Young adult novels, complex vocabulary
```

**WRITE container edge:**
```
Current: Simple sentences, 50-word entries
Edge: Introduce compound sentences, "because" connectors
Too far: Paragraph structure, thesis statements
```

**IMAGINE container edge:**
```
Current: Recombines familiar elements
Edge: Prompt novel combinations, "what if X met Y?"
Too far: Abstract reasoning, philosophical hypotheticals
```

### Gap Filling

The Capability Gap Log identifies holes INSIDE the container:

```
Container: WRITE
  │
  ├── Established: vocabulary, expression, topics
  ├── GAP: logical organization (should be here, isn't)
  └── Edge: complexity (next to develop)

Twin response: Fill the gap before extending the edge.
"Let's try writing about what happened FIRST, THEN, FINALLY..."
```

### Implementation

When the twin responds:

1. **Load container state** — What's in each pillar?
2. **Identify the edge** — What's the current boundary?
3. **Check for gaps** — Any holes inside the container?
4. **Calibrate response:**
   - Use vocabulary FROM the container (grounding)
   - Introduce concepts AT the edge
   - Fill gaps BEFORE extending
   - Never jump OUTSIDE the container

### Example

```
Student: "Tell me about volcanoes."

Container check:
- READ: Has read 2 books mentioning volcanoes (basic)
- WRITE: Uses "hot", "fire", "explode" (limited vocab)
- IMAGINE: Drew a volcano once (surface interest)

Edge identification:
- Vocabulary edge: "lava", "eruption", "magma"
- Concept edge: Why volcanoes happen (plate tectonics)

Response (at edge, grounded):
"Remember when you drew that volcano with the red lava? 
 The hot melted rock inside is called 'magma.' 
 When it comes out, it's called 'lava.' 
 Do you know why it comes out? The Earth is like a puzzle..."
```

### Zone of Proximal Development

This is the educational principle: teach at the boundary of current capability, where the user can succeed with guidance.

- Too easy → boredom, no growth
- Too hard → frustration, shutdown
- At the edge → engagement, growth

---

## Query Modes

### Query SELF
> "What kind of person is [user]?"
> "How does [user] typically approach new problems?"
> "What are [user]'s core values?"

### Query SKILLS (by pillar)
> "How well does [user] write?"
> "What's [user]'s reading comprehension level?"
> "How creative/original is [user]?"

### Query BOTH (Full Emulation)
> "Write a journal entry the way [user] would."
> "Explain [concept] the way [user] would explain it."
> "What would [user] find interesting about [subject]?"

---

## Data Model (Draft)

### SELF Schema

**Design principle: Authentic mirroring, not idealization.**

```typescript
interface Self {
  id: string;
  user_id: string;
  
  // Core identity
  personality: {
    traits: { trait: string; confidence: number }[];
    updated_at: Date;
  };
  
  linguistic_style: {
    vocabulary_level: number;
    sentence_patterns: string[];
    verbal_habits: string[];      // "um", "like", catchphrases
    tone: string;
    samples: string[];            // Actual examples of their speech/writing
    updated_at: Date;
  };
  
  // Life narrative (their story)
  narrative: {
    family: {
      members: { name: string; relationship: string; notes: string }[];
      dynamics: string;
    };
    places: {
      birthplace: string;
      places_lived: { place: string; period: DateRange; significance: string }[];
      favorite_places: string[];
    };
    significant_events: {
      event: string;
      date: Date;
      impact: string;
      how_they_tell_it: string;   // Their version of the story
    }[];
    relationships: {
      name: string;
      nature: string;
      significance: string;
    }[];
    memories: {
      content: string;
      date_added: Date;
      emotional_tone: string;
    }[];
  };
  
  // Preferences
  preferences: {
    favorites: {
      movies: string[];
      books: string[];
      places: string[];
      activities: string[];
      people: string[];
      foods: string[];
      music: string[];
    };
    dislikes: string[];
    happiness_triggers: string[];
    frustration_triggers: string[];
    learning_preferences: string[];
  };
  
  // Values (what matters to them)
  values: {
    core: string[];
    inferred_from: string[];
    updated_at: Date;
  };
  
  // How they think
  reasoning_patterns: {
    style: string;  // visual, sequential, intuitive, etc.
    approach_to_new: string;
    approach_to_hard: string;
    approach_to_conflict: string;
    updated_at: Date;
  };
  
  // What captures their attention
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
  
  // The three pillars
  pillars: {
    WRITE: PillarProfile;
    READ: PillarProfile;
    IMAGINE: PillarProfile;
  };
  
  // All captured activities
  activities: Activity[];
  
  // Derived capability claims
  capabilities: CapabilityClaim[];
  
  // Gaps and struggles
  gaps: GapEntry[];
  struggles: StruggleEntry[];
  
  created_at: Date;
  updated_at: Date;
}

interface PillarProfile {
  dimensions: {
    [dimension: string]: {
      level: 1 | 2 | 3 | 4 | 5;
      confidence: number;           // 0-1
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
  
  activity_type: 'journal' | 'story' | 'summary' | 'conversation' | 'creative' | 'artwork' | 'building' | 'problem';
  pillar_primary: 'WRITE' | 'READ' | 'IMAGINE';
  pillar_secondary?: 'WRITE' | 'READ' | 'IMAGINE';
  
  // Content varies by modality
  content: {
    text?: string;               // For voice/text
    image_file?: string;         // For artwork uploads
    user_description?: string; // What they say about their creation
  };
  
  analysis: {
    pillar_metrics: Record<string, any>;  // Dimension-specific analysis
    self_observations: {
      linguistic_markers: string[];
      emotional_tone: string;
      interests_signaled: string[];
    };
    // For image activities
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
    image_authenticity?: 'original' | 'uncertain' | 'flagged';
  };
}

interface CapabilityClaim {
  id: string;
  pillar: 'WRITE' | 'READ' | 'IMAGINE';
  dimension: string;
  statement: string;
  level: 1 | 2 | 3 | 4 | 5;
  
  verification_level: 'observed' | 'attested' | 'verified' | 'certified';
  confidence_tier: 1 | 2 | 3 | 4;
  
  first_demonstrated: Date;
  last_confirmed: Date;
  activity_count: number;
  evidence: string[];  // Activity IDs
  
  status: 'emerging' | 'established' | 'archived';
}
```

---

## Privacy Considerations

### SELF (Highly Sensitive)
- Contains personality, values, emotional patterns
- Highest privacy tier
- Parent oversight required for minors
- Granular access control (can share skills without personality)

### SKILLS (Sensitive)
- Contains capability data across READ/WRITE/IMAGINE
- Can be shared for credential purposes
- Pillar-limited access possible (share WRITE, not all pillars)

### Access Control Matrix

| Accessor | SELF Access | SKILLS Access |
|----------|-------------|---------------|
| Student | Full | Full |
| Parent (child <12) | Full | Full |
| Parent (child 12-18) | Summary | Full |
| Parent (child 18+) | None (unless granted) | None (unless granted) |
| Employer | None (unless granted) | Granted pillars only |
| University | None (unless granted) | Granted pillars only |
| Mentor | Granted portions | Granted pillars |

---

## MVP Scope

### Phase 1 (Solo Pilot)

**SELF:**
- Preference survey (seeding)
- Basic linguistic style capture
- Interest tracking

**SKILLS:**
- WRITE pillar only (journal entries)
- Activity capture and analysis
- Basic dimension tracking (vocabulary, complexity, expression)

### Phase 2 (Cohort Pilot)

**SELF:**
- Personality inference from activities
- Reasoning pattern detection
- Value inference

**SKILLS:**
- All three pillars (WRITE, READ, IMAGINE)
- Full dimension tracking
- Capability claims with verification levels
- Gap and struggle logging

---

## Open Questions

1. **How granular should SELF be for a 6-year-old?**
   - Personality traits are still forming
   - Preferences change rapidly
   - Need to balance capture vs. overfit

2. **How to prompt READ and IMAGINE activities?**
   - WRITE is natural (journal)
   - READ needs "tell me about what you read" prompts
   - IMAGINE needs creative prompts or observation

3. **How to handle SELF changes over time?**
   - Person at 6 ≠ person at 16
   - Preserve history (snapshots) + update current

4. **What's the minimum for useful emulation?**
   - WRITE samples + SELF linguistic style might be enough to start
   - Full pillar coverage can wait

---

## Template Governance

Each module is governed by a template that defines structure, rules, and compliance checks.

| Module | Template | Adapted From |
|--------|----------|--------------|
| SELF | [SELF–TEMPLATE.md](SELF-TEMPLATE.md) | CMC's CIV–MIND–TEMPLATE |
| SKILLS | [SKILLS–TEMPLATE.md](SKILLS-TEMPLATE.md) | CMC's CIV–SCHOLAR–TEMPLATE |
| EVIDENCE | [EVIDENCE–TEMPLATE.md](EVIDENCE-TEMPLATE.md) | CMC's CIV–ARC–TEMPLATE |

### Key Concepts from Templates

**From SELF–TEMPLATE:**
- Authentic mirroring principle
- Component structure (personality, linguistic, narrative, preferences, values, reasoning, interests)
- Seeding via simple favorites survey (movies, books, places, games)
- Evolution with preserved history
- Forbidden behaviors (things the user would never say)
- Snapshots at age milestones

**From SKILLS–TEMPLATE:**
- Three pillars: WRITE, READ, IMAGINE
- Activity-based growth (not explicit teaching)
- Capability Claims with developmental levels
- Capability Gap Log
- Struggle Log (difficulties and breakthroughs)
- Activity Capture Format (text, voice, image)
- WRITE → SELF linguistic pipeline
- READ → SELF preferences pipeline
- Snapshots at age milestones

**From EVIDENCE–TEMPLATE:**
- Evidence tiers (Certified → Verified → Attested → Observed → Reported)
- Reading List as systematic canon (like ARC)
- Re-reads as strong preference signal
- Media log for movies, shows, games
- Attestation log for parent/teacher confirmations
- Evidence metrics and confidence calculation
- Immutability rules (activities can't be modified)

---

## Storage and Versioning

GitHub repository is the authoritative record store.

### Storage Model

```
GitHub Repository (rbtkhn/cog-em)
├── docs/                    # Templates and governance
├── users/
│   └── pilot-001/
│       ├── SELF.md          # Personality profile
│       ├── SKILLS.md        # Capability containers
│       ├── EVIDENCE.md      # Reading/Writing/Creation logs
│       └── SESSION-LOG.md   # Interaction history
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

### Commit Protocol

Every session that updates user data:
1. Update relevant files (SELF, SKILLS, EVIDENCE)
2. Commit with descriptive message
3. Push to GitHub

**Commit message format:**
```
[PILOT-001] Session XXX: [activity type]

- SELF: [what was updated]
- SKILLS: [what was updated]  
- EVIDENCE: [what was added]
```

### Snapshots

Age-based snapshots = git tags:
```
git tag pilot-001-age-6 -m "Snapshot at age 6"
git tag pilot-001-age-7 -m "Snapshot at age 7"
```

Tags preserve the exact state at that point in time.

---

*Document version: 1.2*  
*Last updated: February 2026*
