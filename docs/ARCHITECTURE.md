# cog-em Architecture

## Core Principle

The cognitive emulator separates **who the student is** from **what the student knows**.

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

Contains who the student IS — their identity, story, and way of being in the world.

**Core principle: Authentic mirroring.** The goal is faithful reproduction of the student's actual self, not an idealized or curated version. The twin should think, speak, and reason the way the student actually does — including quirks, biases, and imperfections.

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
- **Inferred**: System detects patterns in how student teaches
- **Narrative-rich**: Contains their story, not just traits

### Authentic Mirroring Principle

The SELF module strives to mirror the student as they actually are:

| Include | Exclude |
|---------|---------|
| Actual vocabulary (including "um", "like") | Polished, idealized speech |
| Real preferences (even embarrassing ones) | Curated, socially-desirable answers |
| Actual reasoning patterns (including biases) | Corrected, "better" reasoning |
| Their version of events | Objective third-party account |
| Quirks and imperfections | Normalized, generic personality |

**Why this matters:**
- Employers want to know the real person, not a polished facade
- The twin should answer "how would [student] think about X?" accurately
- Authenticity builds trust in the credential
- The student should recognize themselves in the twin

### Seeding (Initial Survey)

For a 6-year-old:
1. Ten favorite movies/shows
2. Ten favorite books/stories
3. Ten favorite places
4. Ten favorite things to do
5. Ten favorite people (family, friends, characters)
6. What makes you happy?
7. What makes you frustrated?
8. How do you like to learn new things?

### Evolution

The SELF module updates as the system observes:
- How the student explains things (linguistic fingerprint)
- What topics they gravitate toward (interests)
- How they respond to challenges (reasoning style)
- What they care about (values)

---

## Module 2: SKILLS (Knowledge Modules)

**Analogue to CMC's MEM files.**

Contains what the student KNOWS and CAN DO — competencies that grow through teaching.

### Structure

```
SKILLS/
├── ACADEMIC/
│   ├── mathematics/
│   ├── language/
│   ├── science/
│   ├── history/
│   └── ...
├── PRACTICAL/
│   ├── cooking/
│   ├── coding/
│   ├── music/
│   └── ...
├── CREATIVE/
│   ├── art/
│   ├── writing/
│   ├── design/
│   └── ...
└── DOMAIN/
    ├── [specialized areas]/
    └── ...
```

### Knowledge Node Structure

Each piece of knowledge includes:

```
{
  "concept": "Multiplication",
  "depth": 3,              // 1-5 scale
  "first_taught": "2026-03-15",
  "last_demonstrated": "2026-04-20",
  "teaching_sessions": 7,
  "verification_level": "attested",
  "connections": ["addition", "division", "area"],
  "evidence": [
    { "type": "teaching", "date": "...", "content": "..." },
    { "type": "demonstration", "date": "...", "content": "..." }
  ]
}
```

### Characteristics

- **Grows continuously**: New knowledge added through teaching
- **Explicitly taught**: Student actively teaches the system
- **Verified**: Different trust tiers (self-reported → certified)
- **Connected**: Knowledge nodes link to related concepts
- **Depth-tracked**: Not just "knows" but "how deeply"

---

## Interaction Between Modules

### SELF Influences SKILLS

- **Learning style** (SELF) affects how knowledge is structured (SKILLS)
- **Interests** (SELF) predict which skills develop fastest
- **Reasoning patterns** (SELF) shape how concepts connect

### SKILLS Reveal SELF

- What a student chooses to teach reveals interests
- How they explain reveals linguistic style
- What they struggle with reveals learning patterns

### Both Required for Emulation

A true cognitive twin needs both:
- SELF alone = personality without capability
- SKILLS alone = knowledge without character
- SELF + SKILLS = thinking like this specific person

---

## Query Modes

### Query SELF
> "What kind of learner is [student]?"
> "How does [student] typically approach new problems?"
> "What are [student]'s core values?"

### Query SKILLS
> "What does [student] know about calculus?"
> "Solve this problem the way [student] would."
> "What's the depth of [student]'s programming knowledge?"

### Query BOTH (Full Emulation)
> "How would [student] approach learning [new topic]?"
> "Explain [concept] the way [student] would explain it."
> "What would [student] find interesting about [subject]?"

---

## Data Model (Draft)

### SELF Schema

**Design principle: Authentic mirroring, not idealization.**

```typescript
interface Self {
  id: string;
  student_id: string;
  
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
  student_id: string;
  
  domains: {
    [domain: string]: {
      [subdomain: string]: KnowledgeNode[];
    };
  };
  
  created_at: Date;
  updated_at: Date;
}

interface KnowledgeNode {
  id: string;
  concept: string;
  depth: 1 | 2 | 3 | 4 | 5;
  
  first_taught: Date;
  last_demonstrated: Date;
  teaching_sessions: number;
  
  verification: {
    level: 'self_reported' | 'attested' | 'verified' | 'certified';
    attestations: Attestation[];
  };
  
  connections: string[];  // IDs of related nodes
  
  evidence: Evidence[];
  
  gaps: string[];  // Known gaps or weaknesses
}

interface Evidence {
  type: 'teaching' | 'demonstration' | 'creation' | 'attestation';
  date: Date;
  content: string;
  modality: 'voice' | 'text' | 'drawing' | 'video';
  verification_level: string;
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
- Contains knowledge and competency data
- Can be shared for credential purposes
- Domain-limited access possible (share math, not personal life)

### Access Control Matrix

| Accessor | SELF Access | SKILLS Access |
|----------|-------------|---------------|
| Student | Full | Full |
| Parent (child <12) | Full | Full |
| Parent (child 12-18) | Summary | Full |
| Parent (child 18+) | None (unless granted) | None (unless granted) |
| Employer | None (unless granted) | Granted domains only |
| University | None (unless granted) | Granted domains only |
| Mentor | Granted portions | Granted domains |

---

## MVP Scope

### Phase 1 (Solo Pilot)

**SELF:**
- Preference survey (seeding)
- Basic linguistic style capture
- Interest tracking

**SKILLS:**
- Free-form teaching (no structured domains yet)
- Simple knowledge nodes
- Basic depth tracking

### Phase 2 (Cohort Pilot)

**SELF:**
- Personality inference from interactions
- Reasoning pattern detection
- Value inference

**SKILLS:**
- Structured domains (academic, practical, creative)
- Connection mapping
- Verification levels

---

## Open Questions

1. **How granular should SELF be for a 6-year-old?**
   - Personality traits are still forming
   - Preferences change rapidly
   - Need to balance capture vs. overfit

2. **Should SKILLS have curriculum structure or emerge organically?**
   - Structured: easier to compare, evaluate
   - Organic: respects how children actually learn

3. **How to handle SELF changes over time?**
   - Person at 6 ≠ person at 16
   - Preserve history or update in place?

4. **What's the minimum SELF needed for useful emulation?**
   - Linguistic style + interests might be enough to start
   - Full personality model can wait

---

*Document version: 1.0*  
*Last updated: February 2026*
