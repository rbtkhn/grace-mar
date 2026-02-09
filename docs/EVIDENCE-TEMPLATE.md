# EVIDENCE–TEMPLATE v1.0

Cognitive Emulator · Evidence Governance Template

Status: DRAFT
Version: 1.0
Last Update: February 2026

**Governed by**: [COG-EM-CORE v1.0](COG-EM-CORE.md)
Adapted from: CIV–ARC–TEMPLATE v3.1 (CMC)

---

## I. PURPOSE

This template governs how evidence is stored, organized, and weighted.

Evidence includes:
- Activities (WRITE, READ, IMAGINE)
- Content consumed (reading list, media)
- External attestations (parent, teacher)
- Assessments and verifications

Evidence does NOT include:
- The capability claims themselves (see SKILLS-TEMPLATE)
- The SELF profile (see SELF-TEMPLATE)

Evidence is RAW INPUT. Claims are DERIVED OUTPUT.

---

## II. EVIDENCE TIERS

All evidence has a trust tier.

| Tier | Name | Description | Weight |
|------|------|-------------|--------|
| 1 | CERTIFIED | External formal verification | Highest |
| 2 | VERIFIED | Live demonstration, proctored | High |
| 3 | ATTESTED | Parent/teacher confirms | Medium |
| 4 | OBSERVED | System captured authentic activity | Standard |
| 5 | REPORTED | Student self-reports (unobserved) | Lowest |

### Tier Progression

Evidence can move UP in tier:
```
REPORTED → OBSERVED: Student produces activity in-system
OBSERVED → ATTESTED: Parent confirms ("yes, she read that book")
ATTESTED → VERIFIED: Live demonstration
VERIFIED → CERTIFIED: External assessment
```

Evidence does NOT move down.

---

## III. READING LIST (READ EVIDENCE CANON)

The reading list is the systematic record of content consumed.

### Structure

```typescript
interface ReadingList {
  id: string;
  user_id: string;
  
  entries: ReadingEntry[];
  
  // Derived
  genres: GenreProfile;
  themes: ThemeProfile;
  reading_velocity: VelocityMetrics;
  
  created_at: Date;
  updated_at: Date;
}

interface ReadingEntry {
  id: string;
  
  // Content metadata
  title: string;
  author?: string;
  type: 'book' | 'article' | 'video' | 'audiobook' | 'comic' | 'other';
  genre?: string[];
  themes?: string[];
  difficulty_level?: 1 | 2 | 3 | 4 | 5;
  
  // Engagement
  status: 'in_progress' | 'completed' | 'abandoned' | 'reread';
  times_consumed: number;        // Re-reads signal strong preference
  
  // Temporal
  first_started: Date;
  last_engaged: Date;
  completed_dates: Date[];       // Track each completion
  
  // Evidence
  evidence_tier: 1 | 2 | 3 | 4 | 5;
  evidence: {
    how_added: 'user_report' | 'parent_report' | 'observed' | 'verified';
    attestations: Attestation[];
    activities: string[];        // Activity IDs where this was discussed
  };
  
  // Comprehension (from READ activities)
  comprehension?: {
    summary_given: boolean;
    accuracy: number;            // 0-1
    inference_demonstrated: boolean;
    emotional_response: string;
  };
  
  // SELF implications
  self_signals: {
    interests: string[];         // Topics signaled
    values?: string[];           // Themes returned to
    favorites_candidate: boolean; // Strong preference signal
  };
}
```

### Reading Entry Categories

Analogous to ARC's temporal categories:

| Category | Description |
|----------|-------------|
| FOUNDATION | Early/formative reading (first favorites) |
| CURRENT | Active reading in progress |
| COMPLETED | Finished and discussed |
| REVISITED | Re-read (strong preference signal) |
| ABANDONED | Started but not finished (informative) |

### Preference Signals

Re-reads are the strongest preference signal:

```
times_consumed: 1 → Normal reading
times_consumed: 2 → Strong interest
times_consumed: 3+ → Core favorite (→ SELF.preferences.favorites)
```

### Genre and Theme Tracking

```typescript
interface GenreProfile {
  genres: {
    genre: string;
    count: number;
    percentage: number;
    trend: 'increasing' | 'stable' | 'decreasing';
  }[];
}

interface ThemeProfile {
  themes: {
    theme: string;
    count: number;
    first_seen: Date;
    recurring: boolean;          // Seen in 3+ entries
  }[];
}
```

Recurring themes signal values (→ SELF.values).

---

## IV. WRITING LOG (WRITE EVIDENCE CANON)

The writing log is the systematic record of content produced.

### Structure

```typescript
interface WritingLog {
  id: string;
  user_id: string;
  
  entries: WritingEntry[];
  
  // Derived profiles
  vocabulary_profile: VocabularyProfile;
  style_profile: StyleProfile;
  topic_profile: TopicProfile;
  growth_trajectory: GrowthMetrics;
  
  created_at: Date;
  updated_at: Date;
}

interface WritingEntry {
  id: string;
  activity_id: string;           // Link to source activity
  
  // Content metadata
  type: 'journal' | 'story' | 'message' | 'explanation' | 'essay' | 'list' | 'poem' | 'other';
  title?: string;                // If applicable
  
  // Content
  full_text: string;
  word_count: number;
  
  // Temporal
  created_at: Date;
  
  // Analysis (computed)
  analysis: {
    // Vocabulary
    unique_words: number;
    new_words: string[];         // First-time uses
    vocabulary_level: number;    // Age-adjusted
    
    // Complexity
    avg_sentence_length: number;
    sentence_variety: number;    // 0-1
    complexity_score: 1 | 2 | 3 | 4 | 5;
    
    // Style
    tone: string;                // enthusiastic, reflective, etc.
    narrative_markers: string[]; // "and then", "because", etc.
    verbal_habits: string[];     // Repeated phrases
    
    // Content
    topics: string[];
    emotional_content: string;
    
    // Structure
    has_intro: boolean;
    has_conclusion: boolean;
    logical_flow: 1 | 2 | 3 | 4 | 5;
  };
  
  // SELF implications
  self_signals: {
    linguistic_markers: string[];
    interests: string[];
    emotional_tone: string;
  };
}
```

### Derived Profiles

**Vocabulary Profile:**
```typescript
interface VocabularyProfile {
  total_unique_words: number;
  vocabulary_level: number;      // Current level
  
  // Growth
  words_by_month: { month: string; count: number }[];
  new_words_rate: number;        // New words per entry
  
  // Sophistication
  simple_words_pct: number;
  complex_words_pct: number;
  domain_vocabulary: { domain: string; words: string[] }[];
}
```

**Style Profile:**
```typescript
interface StyleProfile {
  // Sentence patterns
  avg_sentence_length: number;
  sentence_variety: number;
  common_openers: string[];      // "So", "And then", "Today"
  
  // Voice
  tone_distribution: { tone: string; frequency: number }[];
  verbal_habits: { phrase: string; count: number }[];
  
  // Evolution
  style_changes: {
    date: Date;
    observation: string;         // "Started using 'however'"
  }[];
}
```

**Topic Profile:**
```typescript
interface TopicProfile {
  topics: {
    topic: string;
    count: number;
    first_mentioned: Date;
    last_mentioned: Date;
    trend: 'increasing' | 'stable' | 'decreasing';
  }[];
  
  // Themes
  recurring_themes: string[];    // Topics in 5+ entries
}
```

**Growth Trajectory:**
```typescript
interface GrowthMetrics {
  // Quantitative
  entries_count: number;
  total_words: number;
  avg_entry_length: number;
  
  // Qualitative
  vocabulary_growth: { date: Date; level: number }[];
  complexity_growth: { date: Date; score: number }[];
  
  // Milestones
  milestones: {
    date: Date;
    type: 'vocabulary' | 'complexity' | 'style' | 'length';
    description: string;         // "First 100-word entry"
  }[];
}
```

### Writing Entry Categories

| Category | Description |
|----------|-------------|
| JOURNAL | Daily/regular personal entries |
| NARRATIVE | Stories, creative fiction |
| EXPOSITORY | Explanations, how-to, informational |
| REFLECTIVE | Thoughts, feelings, opinions |
| FUNCTIONAL | Lists, messages, practical writing |

### Growth Signals

Track evolution over time:
```
Month 1: avg 30 words, simple sentences, limited vocabulary
Month 3: avg 50 words, compound sentences emerging
Month 6: avg 80 words, variety in structure, richer vocabulary
```

### Writing Log → SELF Pipeline

```
WritingEntry.analysis
    │
    ├── linguistic_markers → SELF.linguistic_style.verbal_habits
    ├── tone → SELF.linguistic_style.tone
    ├── topics → SELF.interests
    ├── emotional_content → SELF.emotional_patterns
    └── vocabulary_level → SELF.linguistic_style.vocabulary_level
```

---

## V. MEDIA LOG (IMAGINE/READ EVIDENCE)

Movies, shows, videos, games.

### Structure

```typescript
interface MediaEntry {
  id: string;
  
  // Content metadata
  title: string;
  type: 'movie' | 'show' | 'video' | 'game' | 'music' | 'podcast';
  genre?: string[];
  
  // Engagement
  status: 'watched' | 'playing' | 'finished' | 'rewatched';
  times_consumed: number;
  
  // Temporal
  first_consumed: Date;
  last_consumed: Date;
  
  // Evidence
  evidence_tier: 1 | 2 | 3 | 4 | 5;
  how_added: 'survey' | 'user_report' | 'parent_report' | 'activity_mention';
  
  // SELF implications
  self_signals: {
    interests: string[];
    favorites_candidate: boolean;
  };
}
```

### Survey-Seeded vs Activity-Derived

```
Survey: "What are your favorite movies?"
  → MediaEntry { how_added: 'survey', evidence_tier: 5 }

Activity: Student mentions movie in journal
  → MediaEntry { how_added: 'activity_mention', evidence_tier: 4 }

Parent: "She's watched Frozen 12 times"
  → MediaEntry { how_added: 'parent_report', evidence_tier: 3, times_consumed: 12 }
```

---

## V. CREATION LOG (IMAGINE EVIDENCE CANON)

The creation log is the systematic record of creative output.

### Structure

```typescript
interface CreationLog {
  id: string;
  user_id: string;
  
  entries: CreationEntry[];
  
  // Derived profiles
  creativity_profile: CreativityProfile;
  theme_profile: ThemeProfile;
  
  created_at: Date;
  updated_at: Date;
}

interface CreationEntry {
  id: string;
  activity_id: string;           // Link to source activity
  
  // Content metadata
  type: 'drawing' | 'painting' | 'craft' | 'building' | 'story_play' | 'invention' | 'design' | 'other';
  title?: string;                // Student's name for it
  description: string;           // Student's description
  
  // Media
  image_file?: string;           // Photo of creation
  video_file?: string;           // Video of creation/play
  
  // Temporal
  created_at: Date;
  
  // Analysis (computed)
  analysis: {
    // Subject matter
    subjects: string[];          // What they created/drew
    themes: string[];            // Underlying themes
    
    // Creativity dimensions
    originality: 1 | 2 | 3 | 4 | 5;
    elaboration: 1 | 2 | 3 | 4 | 5;
    flexibility: 1 | 2 | 3 | 4 | 5;
    
    // For story play / hypotheticals
    reasoning_chains?: string[]; // If-then logic observed
    
    // Emotional
    mood: string;
  };
  
  // SELF implications
  self_signals: {
    interests: string[];
    relationships_depicted?: string[];  // Who appears in art
    values?: string[];           // Themes of creation
  };
}
```

### Creativity Profile

```typescript
interface CreativityProfile {
  // Dimensions (averaged over entries)
  avg_originality: number;
  avg_elaboration: number;
  avg_flexibility: number;
  
  // Patterns
  preferred_subjects: string[];
  recurring_themes: string[];
  preferred_media: string[];     // Drawing, building, etc.
  
  // Growth
  creativity_growth: { date: Date; scores: { o: number; e: number; f: number } }[];
  
  // Milestones
  milestones: {
    date: Date;
    description: string;         // "First detailed background"
  }[];
}
```

### Creation Log → SELF Pipeline

```
CreationEntry
    │
    ├── subjects → SELF.interests
    ├── themes (recurring) → SELF.values
    ├── relationships_depicted → SELF.narrative.relationships
    ├── mood → SELF.emotional_patterns
    └── reasoning_chains → SELF.reasoning_patterns
```

---

## VI. ACTIVITY LOG (RAW EVIDENCE)

All activities are stored with full metadata.

### Activity Evidence Structure

```typescript
interface ActivityEvidence {
  id: string;
  date: Date;
  
  // Classification
  pillar: 'WRITE' | 'READ' | 'IMAGINE';
  activity_type: string;
  modality: 'voice' | 'text' | 'image' | 'video' | 'mixed';
  
  // Evidence tier
  evidence_tier: 4;              // Activities are OBSERVED by default
  
  // Verification
  verification: {
    live_capture: boolean;
    biometric_confirmed: boolean;
    parent_present: boolean;
    ai_detection: 'human' | 'uncertain' | 'flagged';
  };
  
  // Content
  content: {
    text?: string;
    image_file?: string;
    transcript?: string;
  };
  
  // Derived claims
  contributes_to: {
    skills_claims: string[];     // Capability claim IDs
    self_updates: string[];      // SELF component paths
  };
}
```

---

## VI. ATTESTATION LOG

Third-party confirmations.

### Attestation Structure

```typescript
interface Attestation {
  id: string;
  date: Date;
  
  // Who attested
  attestor: {
    role: 'parent' | 'teacher' | 'mentor' | 'examiner';
    name: string;
    verified: boolean;           // Identity confirmed
  };
  
  // What was attested
  claim_type: 'skill' | 'reading' | 'behavior' | 'knowledge';
  claim: string;                 // What they're confirming
  
  // Linked evidence
  evidence_ids: string[];        // Activities/entries this confirms
  
  // Weight
  evidence_tier: 3;              // Attestations are tier 3
}
```

### Attestation Examples

```
Parent attestation:
{
  attestor: { role: 'parent', name: 'Mom' },
  claim_type: 'reading',
  claim: 'Finished Charlotte\'s Web, can discuss characters',
  evidence_ids: ['READ-0042']
}

Teacher attestation:
{
  attestor: { role: 'teacher', name: 'Ms. Johnson' },
  claim_type: 'skill',
  claim: 'Reading at grade level, strong comprehension',
  evidence_ids: []
}
```

---

## VII. EVIDENCE → SELF PIPELINE

How evidence flows to SELF updates.

### Reading List → SELF

```
ReadingEntry (re-read 3x)
    │
    ├── → SELF.preferences.favorites.books
    │
    └── ReadingEntry.themes (recurring)
        │
        └── → SELF.values (inferred)
```

### Activity → SELF

```
Activity (WRITE)
    │
    ├── → SKILLS.WRITE dimensions
    │
    └── → SELF.linguistic_style
        └── → SELF.interests (topics)
        └── → SELF.emotional_patterns (expression)
```

### Media → SELF

```
MediaEntry (survey favorite)
    │
    └── → SELF.preferences.favorites.movies
```

---

## VIII. EVIDENCE METRICS

Track evidence quality and quantity.

### Per-Entry Metrics

```typescript
interface EvidenceMetrics {
  // Quantity
  activity_count: number;
  attestation_count: number;
  
  // Quality
  average_tier: number;
  highest_tier: 1 | 2 | 3 | 4 | 5;
  
  // Temporal
  first_evidence: Date;
  last_evidence: Date;
  evidence_recency: number;      // Days since last evidence
  
  // Derived
  confidence_score: number;      // 0-1, based on tier and count
}
```

### Confidence Calculation

```
confidence = (tier_weight × count_weight × recency_weight)

tier_weight:
  CERTIFIED (1): 1.0
  VERIFIED (2): 0.8
  ATTESTED (3): 0.6
  OBSERVED (4): 0.4
  REPORTED (5): 0.2

count_weight:
  1-2 activities: 0.5
  3-5 activities: 0.7
  6-10 activities: 0.9
  10+ activities: 1.0

recency_weight:
  < 7 days: 1.0
  7-30 days: 0.9
  30-90 days: 0.7
  90+ days: 0.5
```

---

## IX. VERSIONING

### Immutability Rules

- Activities are IMMUTABLE once captured
- Reading entries can be UPDATED (status, times_consumed)
- Attestations are IMMUTABLE once recorded
- Deletions are NOT permitted (only archival)

### Audit Trail

Every modification records:
- What changed
- When
- Why (activity ID, attestation ID)
- Previous value

---

## X. COMPLIANCE CHECKLIST

Before accepting evidence:

- [ ] Evidence tier assigned
- [ ] Verification flags set
- [ ] Linked to relevant claims (SKILLS or SELF)
- [ ] Temporal data complete (dates)

Before updating reading list:

- [ ] Entry deduplicated (same title = update, not create)
- [ ] times_consumed incremented if re-read
- [ ] SELF signals extracted
- [ ] Themes and genres tagged

Before accepting attestation:

- [ ] Attestor role identified
- [ ] Claim type classified
- [ ] Linked evidence specified
- [ ] Date recorded

---

END OF FILE — EVIDENCE–TEMPLATE v1.0
