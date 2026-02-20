# SELF–TEMPLATE v2.0

Cognitive Emulator · Self Module Governance Template

Status: ACTIVE
Version: 2.0
Last Update: February 2026

**Governed by**: [COG-EM-CORE v2.0](COG-EM-CORE.md)

---

## I. PURPOSE

This template governs the SELF module of the cognitive fork.

The SELF module:
- Records WHO the user IS
- Captures personality, linguistic style, values, narrative
- Enables accurate representation (not idealization)
- Evolves as the user grows
- Preserves history at every stage

The SELF module is NOT:
- A curated persona
- An idealized version
- A generic child profile
- A static personality test result

SELF strives for ACCURATE RECORDING.

---

## II. CORE PRINCIPLE: ACCURATE RECORDING

The fork should record the user as they actually are.

### Include

- Actual vocabulary (including filler words, verbal habits)
- Real preferences (even embarrassing ones)
- Actual reasoning patterns (including biases)
- Their version of events (not objective third-party)
- Quirks and imperfections
- Verbal habits and catchphrases

### Exclude

- Polished, idealized descriptions
- Curated, socially-desirable answers
- Corrected, "better" reasoning
- Normalized, generic personality

### Accuracy Test

The SELF module is working when:
- The record accurately reflects the user's documented behavior
- Data is grounded in evidence (activities, surveys, artifacts)
- Changes over time are preserved, not overwritten

---

## III. SELF COMPONENTS

### 1. Identity

Basic information about the user.

```typescript
identity: {
  name: string;
  birthdate: Date;
  age: number;
  languages: string[];
  location: string;
  created_at: Date;
}
```

### 2. Personality

Observable behavioral tendencies.

```typescript
personality: {
  self_concept: string;          // What they think is the best thing about themselves
  
  traits: {
    trait: string;
    confidence: number;          // 0-1
    evidence: string[];          // Sessions/activities that revealed this
  }[];
  
  emotional_patterns: {
    trigger: string;
    response: string;
    examples: string[];
  }[];
  
  humor: {
    style: string;               // physical, wordplay, absurd, etc.
    trigger: string;
  };
  
  empathy_mode: string;          // How they respond to others' emotions
  
  problem_solving: {
    style: string;               // grinder, pivoter, help-seeker
    approach: string;
  };
  
  updated_at: Date;
}
```

### 3. Linguistic Style

How they communicate. **Primary data source: WRITE activities.**

```typescript
linguistic_style: {
  vocabulary_level: number;
  
  sentence_patterns: {
    pattern: string;
    frequency: number;
    examples: string[];
  }[];
  
  verbal_habits: string[];
  tone: string;
  
  samples: {
    content: string;
    date: Date;
    activity_id: string;
    context: string;
  }[];
  
  derived_from: {
    activity_count: number;
    last_updated: Date;
  };
  
  updated_at: Date;
}
```

**Derivation pipeline:**
```
WRITE Activity (journal, story, message)
    │
    └── Text analyzed for:
        ├── Vocabulary (unique words, sophistication)
        ├── Sentence patterns (structure, length)
        ├── Verbal habits (repeated phrases)
        ├── Tone (emotional register)
        └── Notable samples (added to archive)
            │
            └── SELF.linguistic_style updated
```

### 4. Life Narrative

Their story, memories, relationships.

```typescript
narrative: {
  family: {
    members: {
      name: string;
      relationship: string;
      notes: string;
    }[];
  };
  
  places: {
    birthplace: string;
    places_lived: {
      place: string;
      period: DateRange;
      significance: string;
    }[];
    favorite_places: string[];
  };
  
  significant_events: {
    event: string;
    date: Date;
    impact: string;
    their_version: string;
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
}
```

### 5. Preferences

Likes, dislikes, tastes. **Primary data source: READ activities + explicit input.**

```typescript
preferences: {
  favorites: {
    movies: string[];
    books: string[];
    music: string[];
    places: string[];
    activities: string[];
    foods: string[];
    people: string[];
    [custom]: string[];
  };
  
  dislikes: string[];
  
  happiness_triggers: string[];
  frustration_triggers: string[];
  
  learning_preferences: {
    modality: string;
    environment: string;
    time_of_day: string;
  };
  
  derived_from: {
    read_activity_count: number;
    explicit_input_count: number;
    last_updated: Date;
  };
  
  updated_at: Date;
}
```

### 6. Values

What matters to them.

```typescript
values: {
  core: string[];
  
  inferred_from: {
    value: string;
    evidence: string[];
  }[];
  
  conflicts: {
    value_a: string;
    value_b: string;
    context: string;
  }[];
  
  updated_at: Date;
}
```

### 7. Reasoning Patterns

How they think.

```typescript
reasoning_patterns: {
  style: string;
  
  approach_to_new: string;
  approach_to_hard: string;
  approach_to_conflict: string;
  
  characteristic_moves: {
    situation: string;
    typical_response: string;
    examples: string[];
  }[];
  
  updated_at: Date;
}
```

### 8. Interests

What captures their attention. **Derived from all three pillars.**

```typescript
interests: {
  current: {
    topic: string;
    intensity: number;
    since: Date;
    sources: string[];
  }[];
  
  historical: {
    topic: string;
    period: DateRange;
    peak_intensity: number;
  }[];
  
  emerging: string[];
  declining: string[];
  
  derived_from: {
    write_topics: number;
    read_content: number;
    imagine_themes: number;
    last_updated: Date;
  };
}
```

---

## IV. SELF SEEDING (INITIAL SURVEY)

Simple favorites survey to initialize SELF. Everything else is inferred from activity.

### Core Survey (4 questions)

```
1. What are your favorite movies or shows?
2. What are your favorite books or stories?
3. What are your favorite places?
4. What are your favorite games?
```

### Optional Extensions (if user is engaged)

```
5. Who are your favorite people?
6. What do you like to do for fun?
7. What do you want to be when you grow up?
```

### Why This Works

| Survey Question | Seeds SELF Component |
|-----------------|---------------------|
| Favorite movies | preferences.favorites.movies, interests |
| Favorite books | preferences.favorites.books, interests |
| Favorite places | preferences.favorites.places, narrative |
| Favorite games | preferences.favorites.games, interests |

Everything else — linguistic style, personality, values, reasoning patterns — is **inferred from activity**, not surveyed.

### After Seeding

```
SELF initialized with:
├── preferences.favorites (from survey)
├── interests (inferred from favorites)
└── everything else: EMPTY (to be derived from activity)

First writing sample:
└── SELF.linguistic_style begins populating
```

The survey gives the system something to reference.
Activity gives the record depth.

---

## V. SELF EVOLUTION

SELF evolves over a lifetime.

### What Evolves

- Preferences change (6-year-old → 16-year-old)
- Linguistic style matures
- Reasoning patterns develop
- Interests shift
- Values deepen

### How It Evolves

1. **Continuous Inference**
   - System observes patterns in activity
   - Patterns detected and recorded
   - Confidence scores updated

2. **Periodic Anchoring**
   - Annual or milestone surveys
   - Parent/teacher attestation (when young)
   - User self-reflection (as they grow)

3. **Explicit Updates**
   - User says "I don't like that anymore"
   - Major life event
   - User logs new information

### Preserving History

Changes do NOT overwrite. History is preserved.

```
PREFERENCE HISTORY: Favorite Movie

2026-03 (age 6): Frozen
2027-09 (age 7): Moana
2029-01 (age 9): Harry Potter
2031-06 (age 11): Star Wars
```

The fork knows current preference AND can recall past preferences.

---

## VI. SNAPSHOTS

Preserve SELF at points in time.

### Snapshot Triggers

- Age milestones (6, 8, 10, 12, 14, 16, 18)
- Major life transitions
- Annual archival
- On-demand

### Snapshot Format

```
SELF–SNAPSHOT–[NAME]–AGE–[X]

Created: [YYYY-MM-DD]
Status: ARCHIVED

PERSONALITY SUMMARY:
[Key traits at this age]

LINGUISTIC MARKERS:
[How they communicated at this age]

FAVORITES AT THIS AGE:
[Top preferences]

VALUES:
[What mattered to them]

INTERESTS:
[What captured their attention]

NARRATIVE:
[Their story up to this point]
```

### Preservation Rule

Snapshots are IMMUTABLE.
The user can revisit who they were at any age.

---

## VII. QUERYING SELF

How the SELF record is accessed.

### Record Queries (Primary)

When browsing or querying the fork:

| Query | Source |
|-------|--------|
| "What kind of person is [user]?" | Personality summary |
| "How does [user] communicate?" | Linguistic markers + samples from Writing Log |
| "What does [user] care about?" | Values and interests + evidence |
| "Tell me about [user]'s background" | Life narrative |
| "What are [user]'s interests?" | Interest profile with sources |

### Evidence-Grounded Interaction

When the system interacts with the user:
1. Load relevant SELF components
2. Load relevant evidence (Writing Log, Reading List)
3. Reference their actual data
4. Connect new activities to prior evidence

### Emulation Queries (Optional Future Feature)

When the user enables emulation:
- "Write a journal entry the way [user] would"
- "Explain [concept] the way [user] would"
- Apply linguistic style from WRITE samples
- Reference their actual experiences
- Deliver in their voice, grounded in evidence

Emulation requires explicit opt-in and sufficient data.

---

## VIII. EMULATION FEATURES (Optional, Future)

These features depend on sufficient SELF data and explicit user opt-in.

### Linguistic Fingerprint

When emulation is enabled, the system can produce output
in the user's voice using their documented linguistic style.

### Forbidden Behaviors (Emulation Mode)

When emulating, the system should NOT produce output that
contradicts the user's documented patterns:

```typescript
forbidden: {
  phrases_never_used: string[];
  tones_never_adopted: string[];
  reasoning_never_used: string[];
}
```

### Recognition Test (Emulation Mode)

If a parent, teacher, or friend interacts with the emulation
and says "that sounds exactly like them" — success.
If they say "that doesn't sound like them" — failure.

---

## IX. PRIVACY TIERS

SELF is highly sensitive.

### Access Levels

| Accessor | Access Level |
|----------|--------------|
| User | Full |
| Parent (user <12) | Full (custodial) |
| Parent (user 12-16) | Summary + explicit grants |
| Parent (user 16+) | Summary only |
| Parent (user 18+) | None unless granted |
| Employer | None unless granted (rare) |
| University | None unless granted (rare) |
| Mentor | Granted portions only |

### What Can Be Shared

- SKILLS can be shared without SELF
- SELF sharing is always opt-in
- Granular control (share interests, not values)
- Time-limited access

---

## X. COMPLIANCE CHECKLIST

Before marking SELF as initialized:

- [ ] Identity complete
- [ ] Initial survey completed
- [ ] At least 5 preferences captured
- [ ] Language samples collected (5+)
- [ ] Basic personality traits inferred
- [ ] Family/narrative basics captured

Before creating SELF SNAPSHOT:

- [ ] All components reviewed
- [ ] Historical changes preserved
- [ ] Linguistic samples current
- [ ] Personality confidence scores assigned
- [ ] Interests updated
- [ ] Timestamp recorded
- [ ] Marked as ARCHIVED (immutable)

---

## XI. INTEGRATION WITH SKILLS

### SELF → SKILLS

- Learning preferences (SELF) shape how knowledge is organized
- Interests (SELF) predict which domains develop
- Reasoning patterns (SELF) affect concept connections

### SKILLS → SELF

- What user produces reveals interests
- How they express reveals linguistic style
- Struggles reveal emotional patterns

### Full Record Requires Both

> "What are [user]'s cognitive strengths?"

= SKILLS (what they can do) + SELF (how they approach it)

---

END OF FILE — SELF–TEMPLATE v2.0
