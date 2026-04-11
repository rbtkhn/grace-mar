# GRACE-MAR Architecture

**Governed by**: [GRACE-MAR-CORE v2.0](grace-mar-core.md)

Terminology primer: see [glossary.md](glossary.md) for canonical definitions of Grace-Mar terms (Record, Voice, companion, recursion-gate).

---

## Core Principle

The cognitive fork records **identity** (**SELF** + **SELF-KNOWLEDGE**), **reference** (**SELF-LIBRARY**, including **CIV-MEM**), **capability** (**SKILLS**), and **evidence** — as structured, evidence-grounded data. Identity and library are **different surfaces**: domain corpora belong in SELF-LIBRARY, not in IX-A. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           COGNITIVE FORK                                     │
├──────────────────┬────────────────────┬────────────────────────────────────┤
│      SELF        │      SKILLS        │        SELF-LIBRARY                 │
│  identity +      │  what the Record   │  governed reference (not identity)  │
│  SELF-KNOWLEDGE  │  can evidence      │  · return-to sources                │
│  (IX-A/B/C)      │  they CAN DO       │  · CIV-MEM subdomain → CMC lookup   │
├──────────────────┴────────────────────┴────────────────────────────────────┤
│  EVIDENCE — READ/WRITE/CREATE/ACT logs (provenance, immutable where set)   │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## State governance: proposed, interface, and canonical

Companion-self–style instances are **state-governance architectures** for identity-bearing systems: they preserve a clear distinction between **draft or proposed material**, **interface-visible behavior**, and **canonical durable state**. The decisive act is not storage, retrieval, or synthesis alone—it is **legitimate incorporation** into the Record.

**Three layers**

| Layer | Role | Examples |
|-------|------|----------|
| **Proposed** | Drafts, harvested outputs, staged candidates—not yet canonical | `recursion-gate.md` pending blocks, operator drafts, imports staged for review |
| **Interface-visible** | How the companion experiences the system—constrained by prompt, policy, and harness | Voice (Telegram), PRP / runtime surfaces, query-time rendering |
| **Canonical durable** | Approved, auditable self and evidence | `self.md`, `self-skills.md`, `self-archive.md` (EVIDENCE), merged `bot/prompt.py` obligations |

**Merge contract.** Only the **companion** (or the governed pipeline acting on explicit companion approval) may satisfy the contract that moves content from proposed into canonical state. See [AGENTS.md](../AGENTS.md) § Gated Pipeline — agents **stage**; they do not **merge** into SELF, EVIDENCE, or prompt without approval.

**Voice as interface.** The Voice is **not** identical with selfhood: it is an **interface** over governed state plus permitted runtime reasoning. Inside the documented boundary it should be fast and useful; outside it should abstain rather than invent authority—see [knowledge-boundary-framework.md](knowledge-boundary-framework.md).

**Anti-patterns** (how forks lose auditability when it matters most):

- Convenience merges or hidden writes into canonical surfaces
- Prompt-level patches masquerading as durable state
- One-off exceptions that bypass review
- Treating runtime shortcuts or session fluency as equivalent to governed change

**Method — add one boundary at a time:** (1) staging boundaries so drafts do not pretend to be canonical; (2) approval boundaries so incorporation requires an explicit contract; (3) integrity boundaries (exports, provenance, drift checks); (4) interface boundaries so the Voice stays scoped. Deeper identity-oriented capabilities belong **after** these layers exist.

> Draft is not state; retrieval is not authorization; synthesis is not incorporation; fluency is not grounding; convenience is not governance.

---

## System boundaries and harness

**Voice = model + harness.** What the companion experiences as the Voice is the underlying model plus prompt, pipeline, tools, and approval gate. Improvements to prompt, pipeline, or tooling are first-class; the model is one component. When debugging behavior, consider: model limit, prompt gap, pipeline miss, or tool/context issue. See [IMPLEMENTABLE-INSIGHTS](implementable-insights.md).

**Harness lock-in (industry).** Coding and knowledge-work agents diverge less on raw model scores than on **harness**: where state lives, tool integration, session memory, trust boundary (local shell vs isolated sandbox). Teams compound workflows, skills, and verification **around** a harness; switching harnesses resets process — not just “another model.” Grace-Mar’s harness choice is **git + gated pipeline + small auditable core**: institutional memory lives in **approved Record artifacts**, not in a vendor’s session-only context; see [IMPLEMENTABLE-INSIGHTS §11](implementable-insights.md#11-harness-lock-in-and-compound-workflows). Major agent stacks converge on **decompose → parallelize → verify → iterate**; Grace-Mar maps **verify** to companion approval and **iterate** to pipeline + git history; see [design-notes §11.11](design-notes.md#1111-harness-convergence--decompose-parallelize-verify-iterate). **Component / write inventory:** [harness-inventory.md](harness-inventory.md).

**Explicit non-goals.** Grace-Mar does not:
- Merge into the Record without companion approval (stage only; companion merges).
- Learn from the open web or from model training data; knowledge is gated and evidence-linked.
- Pursue autonomous long-horizon or self-set instrumental goals (no unbounded agentic optimizer).
- Allow the model to edit SELF or EVIDENCE directly; "continual learning" is human-gated writes only.

Any future agentic or orchestration layer (e.g. Claw-style) must keep merge authority human-only; orchestration may suggest or stage, not merge.

**Rebuilt around, not bolted onto.** Most personal AI systems bolt memory or continuity onto an existing chat interface. Grace-Mar's architecture was rebuilt around what AI makes possible: disposable agents that read state from disk, structured handoffs across session boundaries where memory goes to zero, and a gated pipeline where the human holds merge authority while the execution layer is commoditized and replaceable. This is a design criterion, not an accident — when evaluating new features, prefer approaches that assume the agent is disposable and continuity lives in artifacts, not approaches that depend on session persistence.

### Portable harness lanes

Grace-Mar's harness is portable because it separates **canonical truth** from **runtime continuity** and **audit** rather than collapsing them into one opaque memory store.

| Lane | What it contains | Canonical? | Typical files |
|------|------------------|------------|---------------|
| **record** | Companion-owned identity, evidence, and **reference library** (distinct surfaces) | Yes | `self.md` (identity + SELF-KNOWLEDGE), `self-skills.md`, **`self-archive.md`** (EVIDENCE body), optional `self-evidence.md` pointer, `self-library.md` (SELF-LIBRARY; CIV-MEM subdomain), PRP exports |
| **runtime** | Continuity aids for a live session | No | `self-memory.md` (bundle/runtime lane may mirror as `self-memory.md`), `session-transcript.md`, warmup digests, session-log tails |
| **audit** | Replay, provenance, operational traces | No, but append-only | `pipeline-events.jsonl`, `merge-receipts.jsonl`, `compute-ledger.jsonl`, `harness-events.jsonl`, `fork-manifest.json`, `fork-lineage.jsonl` (lifecycle / export trail; audit-adjacent) |
| **policy** | Intent and constitutional alignment surfaces | Yes for policy, not identity | `intent.md`, `intent_snapshot.json`, manifest-declared constraints |

The runtime lane is portable, but it is **not** Record truth. A downstream runtime may consume `self-memory.md` (or legacy `memory.md`) or a warmup block for continuity, yet only the Record lane defines who Grace-Mar is. This keeps runtime swaps possible without making any one harness the owner of memory.

**Profile root vs `runtime-bundle/`.** For a live instance, audit and runtime files under `users/<id>/` are canonical. A **`runtime-bundle/`** subtree may mirror the same names (e.g. `runtime-bundle/audit/pipeline-events.jsonl`) for portable export. Loaders that synthesize replay views should prefer the profile root and fall back to the bundle when a root file is missing or empty, so snapshots are not double-counted.

### Runtime modes

Grace-Mar may be exported in different **runtime modes** depending on how much continuity a downstream harness should receive:

| Mode | Meaning | Included emphasis |
|------|---------|-------------------|
| **`adjunct_runtime`** | Grace-Mar supports another runtime alongside the canonical repo | Record + policy + light runtime continuity |
| **`primary_runtime`** | A downstream runtime is the main live operating surface, while the repo remains canonical | Record + policy + fuller runtime lane + audit |
| **`portable_bundle_only`** | Produce a transport bundle without assuming any live runtime | Record + policy, minimal runtime aids |

These modes change **packaging and oversight cadence**, not sovereignty. In every mode, the gate remains human-only and the Record remains git-backed and companion-owned.

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
     Git tags: grace-mar-age-6, grace-mar-age-7
     Immutable. Shows who the user was at that age.
```

**Single companion, lifetime system.** There is no parent mode and no child mode. A facilitator or operator may help when the companion is young or needs support. The companion grows into full ownership. The system is age-neutral: the first instance (grace-mar) happens to be young; the architecture applies to any age. See [OPERATOR-BRIEF](operator-brief.md), [LETTER-TO-USER](letter-to-user.md).

---

## Module 1: SELF (Identity Record)

Contains who the companion IS — their identity, story, and way of being in the world.

**SELF-KNOWLEDGE** — The identity-facing slice of SELF (notably IX-A Knowledge, plus seed preferences/narrative): what she knows *about herself* and identity-relevant facts. **Not** long-form historical corpora or civilization reference inventories; those belong in **SELF-LIBRARY** (see Module 1b).

**Core principle: Accurate recording.** The goal is faithful documentation of the companion's actual personality, preferences, reasoning, and voice — not an idealized or curated version. The record should capture them as they are, including quirks and imperfections.

### Module 1b: SELF-LIBRARY (reference surface)

| File / path | Role |
|-------------|------|
| `users/[id]/self-library.md` | Canonical **governed library**: LIB entries, scopes, lookup routing. **Reference-facing**, not identity. |
| `users/[id]/SELF-LIBRARY/` | Navigator docs: domain index, **CIV-MEM** subdomain description (links to corpus + LIB stubs). |

**CIV-MEM** — Sub-library within SELF-LIBRARY: civilizational / historical / cultural reference material (LIB rows + `docs/civilization-memory/`, hybrid encyclopedia, CMC). Routing to CMC = lookup into this domain, not into identity. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), [library-integration.md](library-integration.md). **Domain registry:** [self-library-domains.md](self-library-domains.md) lists installed library domains (metadata, routing, mutation policy).

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
- **Observed from interaction**: Emerges from what the companion does and says
- **Seeded early**: Initial survey captures starting point
- **Inferred**: System detects patterns in companion's activity
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
- Interests ← all modules
- Personality ← observed patterns
- Values ← THINK choices, WRITE content

### Evolution

The SELF record updates as the system observes:
- How the companion explains things (linguistic fingerprint)
- What topics they gravitate toward (interests)
- How they respond to challenges (reasoning style)
- What they care about (values)

History is always preserved. Changes do not overwrite.

---

## Module 2: SKILLS (Capability Record)

Contains what the companion CAN DO — capabilities that grow through authentic activity.

### The Record-Bound Skill Modules

Skills organize under **two Record-bound cognitive modules: THINK and WRITE**. For a formal specification of module boundaries, output functions (Voice and profile as functions of skill-write), and invariants, see [SKILLS-MODULARITY](skills-modularity.md). **Standard labels** (for APIs, docs, cross-references): **self-skill-write** and **self-skill-think**. See [ID-TAXONOMY § Standard capability labels](id-taxonomy.md#standard-capability-labels-self-skill-). These modules are objective-topic-specialized components (teacher/tutor, evaluator, record keeper) for what the Record can evidence directly.

**THINK doctrine (intake, evidence, promotion to IX):** [skill-think README](skill-think/README.md) — complements this section without replacing SKILLS-MODULARITY.

| Module | Function | Activities |
|--------|----------|------------|
| **WRITE** | Production, expression | Journal, stories, explanations, messages |
| **THINK** | Intake, learning, comprehension (multimodal) | Text, video, music/audio, images/diagrams/maps, mixed media; summaries and interpretations |

### Separate work / execution layer

Work is now a separate layer rather than a self-skill module. It lives in:

- `docs/skill-work/work-*/` for reusable work territories
- `users/[id]/work-*.md` for instance work contexts

Work territories may use broader LLM capability, external tools, APIs, and planning loops than the Record allows. They can produce artifacts, plans, and candidate proposals. But they do not write Record truth directly, and they remain gated whenever they would update SELF, EVIDENCE, or prompt.

### Reference assist from SELF-LIBRARY / CIV-MEM

WORK territories are also the primary place where `SELF-LIBRARY` and `CIV-MEM` should be used as **governed reference assist**. In practice, the work harness may route queries through CMC or other library lookup paths to improve grounding, synthesis, and provenance for instrumental outputs.

This boundary matters:

- the **work layer** is the caller,
- `SELF-LIBRARY` / `CIV-MEM` is the reference source,
- `WRITE` remains the capability constraint for how polished and complex the output can be,
- `SELF` remains authoritative for identity, personality, and Voice-facing style.

Reference use in WORK does not by itself create Record truth, does not automatically become `READ-*` evidence, and does not introduce new gate schema. If a resulting artifact should update `SKILLS`, `SELF`, or `EVIDENCE`, that remains a separate gated pipeline step.

### Semi-Independent Executor Policy

THINK and WRITE may run as semi-independent executors with differentiated behavior, but they remain non-sovereign and share one gate. Work territories may also have their own execution loops, but those loops are adjacent to the Record rather than part of the self-skill set.

| Executor | Primary objective | SELF input emphasis | Default posture |
|----------|-------------------|---------------------|-----------------|
| **THINK** | Perception and comprehension fidelity | IX-B Curiosity first, IX-A Knowledge second, IX-C Personality third | Explore broadly; abstain when evidence is thin |
| **WRITE** | Expression and explanation in-character | IX-C Personality first, IX-A Knowledge second, IX-B Curiosity third | Preserve voice and tone; avoid unsupported claims |

Shared constraints for Record-bound executors:
- stage-only authority (never merge),
- evidence-linked output,
- knowledge boundary compliance,
- conflict resolution through companion approval.

THINK-specific capture contract (normative):
- treat THINK as media-agnostic (not text-only),
- record input modality and source/artifact reference in activity evidence,
- evaluate comprehension/inference per modality, then route profile-relevant signals through the same gated pipeline.

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
├── THINK/
│   ├── comprehension/    # Understanding content
│   ├── inference/        # Conclusions beyond explicit
│   ├── vocabulary/       # Words acquired
│   └── interests/        # What they choose
│
work/
├── territories/         # Reusable work domains and operator doctrine
└── contexts/            # Instance-specific work files and live execution state
```

### Activity-Based Growth

The companion doesn't explicitly "teach" skills — they **do** things. Grace-Mar observes and records.

```
Activity: Daily journal entry (WRITE)
├── Content captured: full text
├── Analysis: vocabulary, complexity, style, topics
├── SELF observations: linguistic markers, emotional tone
└── Capability claims updated: WRITE.vocabulary, WRITE.expression
```

### Characteristics

- **Activity-driven**: Grows from authentic production, not explicit teaching
- **Module-organized**: THINK and WRITE as Record structure; work lives alongside as an execution layer
- **Dimension-tracked**: Each module has measurable sub-dimensions
- **Level-based**: 5 developmental levels per dimension
- **Evidence-linked**: Every claim traces to captured activities

---

## Interaction Between Modules

### SELF → SKILLS (Prediction)

- **Interests** (SELF) predict which modules develop fastest
- **Reasoning patterns** (SELF) can shape adjacent work style and project selection

### SKILLS → SELF (Inference)

Each module feeds different SELF components:

```
WRITE Activity ──→ analyst stages signals for SELF.linguistic_style
                   analyst stages IX-B / IX-C observations when warranted

THINK Activity ───→ analyst stages preferences, values, IX-B, IX-C signals

Work-context activity ──→ analyst stages reasoning, IX-C, and interest signals
```

### The WRITE → SELF Pipeline

WRITE activities can surface SELF signals through analyst staging:

| WRITE dimension | Possible SELF signal surfaced |
|-----------------|-------------------------------|
| vocabulary | linguistic_style range and level |
| complexity | sentence-pattern observations |
| style | linguistic_style tone, verbal habits, `IX-C` style markers |
| expression | emotional or interpersonal patterns staged to `IX-C` when identity-relevant |
| topics | interests and curiosity signals |

### The THINK → SELF Pipeline

THINK activities can surface SELF signals through analyst staging:

| THINK data | Possible SELF signal surfaced |
|-----------|-------------------------------|
| content chosen | interests and curiosity topics |
| genres preferred | preferences.favorites |
| themes returned to | values or value expressions |
| emotional reactions | `IX-C` emotional patterns when evidenced |
| difficulty level | developmental context, not automatic identity truth |

### Both Required for Full Record

A complete cognitive fork needs both:
- SELF alone = personality without capability
- SKILLS alone = capabilities without character
- SELF + SKILLS = the full picture of this specific person

**Key insight:** WRITE is both a skill and the primary language-evidence source for SELF. Identity still enters canonically through analyst staging and approval.

---

## Evidence Grounding Principle

When the system interacts with the companion, it should reference their own evidence.

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
- Reference the companion's actual work and data
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

The Record-bound SKILLS modules (THINK, WRITE) are **containers** that define what the companion currently knows and can do inside the Record. The system proposes Record-facing activities at the **edge** of these containers. Work territories may also have their own operational edge, but that edge belongs to the work layer rather than to SKILLS.

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
│   THINK: books read, vocabulary acquired                     │
│   WRITE: words used, complexity achieved                    │
│   Adjacent work context: approved execution evidence        │
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

Activities proposed at the boundary of current capability, where the companion can succeed with guidance.

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
> "What's [user]'s reading comprehension level?" → SKILLS.THINK
> "How creative/original is [user]?" → approved evidence and work-layer artifacts (historical BUILD creation dimensions may still inform this)

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
  
  ix_c: {
    id: string;                  // PER-XXXX
    date: Date;
    observation: string;
    evidence_id: string;         // ACT-XXXX
    provenance: 'human_approved';
    facet?:
      | 'behavioral_tendency'
      | 'emotional_pattern'
      | 'interpersonal_posture'
      | 'aesthetic_tendency'
      | 'value_expression'
      | 'style_marker';
    evidence_strength?: 'single_signal' | 'repeated_pattern' | 'cross_context';
    stability?: 'emerging' | 'recurring' | 'stable';
    valence?: 'attraction' | 'aversion' | 'mixed' | 'neutral';
    tension_with?: string[];
    scope?: string;
    constraint?: string;
  }[];
  
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
  
  modules: {
    WRITE: ModuleProfile;
    THINK: ModuleProfile;
  };
  
  activities: Activity[];
  capabilities: CapabilityClaim[];
  gaps: GapEntry[];
  struggles: StruggleEntry[];
  
  created_at: Date;
  updated_at: Date;
}

interface ModuleProfile {
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
  module_primary: 'WRITE' | 'THINK' | 'WORK_CONTEXT';
  module_secondary?: 'WRITE' | 'THINK' | 'WORK_CONTEXT';
  
  content: {
    text?: string;
    image_file?: string;
    user_description?: string;
  };
  
  analysis: {
    module_metrics: Record<string, any>;
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
  module: 'WRITE' | 'THINK';
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
- Contains IX-A/B/C identity data, linguistic style, values, and narrative
- Highest privacy tier
- User-controlled access at all ages

### SKILLS (Sensitive)
- Contains Record-bound capability data across THINK/WRITE
- Can be shared for credential purposes
- Pillar-limited access possible

### Access Control

| Accessor | SELF Access | SKILLS Access |
|----------|-------------|---------------|
| User | Full | Full |
| Parent (user <12) | Full (custodial) | Full |
| Parent (user 12-18) | Summary | Full |
| Parent (user 18+) | None (unless granted) | None (unless granted) |
| Employer | None (unless granted) | Granted modules only |
| University | None (unless granted) | Granted modules only |

There is no parent mode — operators or guardians have age-appropriate access to the user's single system when the user is a minor.

---

## Storage and Versioning

GitHub repository is the authoritative record store. Git IS the fork.

### Storage Model

```
GitHub Repository (rbtkhn/grace-mar)
├── docs/                    # Templates and governance
├── users/
│   └── grace-mar/
│       ├── self.md          # Identity record
│       ├── self-skills.md   # Capability index (legacy skills.md still resolved)
│       ├── self-archive.md  # EVIDENCE — activity log + § VIII gated approved (canonical body)
│       ├── self-evidence.md # Optional compatibility pointer (not the EVIDENCE body)
│       ├── self-memory.md   # self-memory — short/medium/long continuity (optional; not part of Record)
│       ├── session-log.md   # Interaction history
│       ├── journal.md       # Daily highlights (public-suitable, shareable)
│       └── artifacts/       # Raw files (writing, artwork)
└── (future users...)
```

Each `users/<id>/` directory is one fork’s isolated namespace; quotas, retention, permissions, and export/import are per-fork. See [Fork isolation and multi-tenant](fork-isolation-and-multi-tenant.md).

### Version Control

| Concept | Implementation |
|---------|----------------|
| Audit trail | Git commit history |
| Change tracking | Git diffs |
| Rollback | Git revert |
| Snapshots | Git tags (e.g., `grace-mar-age-6`) |
| Backup | GitHub remote |
| The fork itself | The git repository |

### Commit Protocol

Every session that updates user data:
1. Update relevant files (SELF, SKILLS, EVIDENCE)
2. Commit with descriptive message
3. Push to GitHub

### MEMORY (Self-memory)

`self-memory.md` (**self-memory**; legacy `memory.md`) holds **short-, medium-, and long-horizon** continuity — session tone and thread, multi-day open loops, and long-horizon **meta/pointers** (not a second Record). **Ephemeral** here means **non-canonical and rotatable**, not “only intraday.” It is **not part of the Record**. SELF is authoritative; when MEMORY conflicts with SELF, follow SELF. Rotate or prune per horizon (see [MEMORY-TEMPLATE](memory-template.md)). Optional; the system runs normally if absent.

### JOURNAL (Shareable Daily Highlights)

journal.md consolidates daily highlights of activity — what Grace-Mar read, wrote, created, learned. Entries are written in **first-person Grace-Mar voice** ("I learned…", "I drew…") and serve to **demonstrate and audit** the fork's linguistic fingerprint (vocabulary, sentence patterns, tone). Public-suitable; contrasts with SESSION-TRANSCRIPT (raw conversation log) and SELF-ARCHIVE (gated approved activity); both private. Sources: EVIDENCE, SESSION-LOG. See [JOURNAL-SCHEMA](journal-schema.md). Profile tab order: Knowledge | Skills | Curiosity | Personality | Library | Journal.

### Snapshots

Age-based snapshots = git tags:
```
git tag grace-mar-age-6 -m "Snapshot at age 6"
```

Tags preserve the exact state at that point in time.

---

## Lattice Model

The system can be viewed as a **lattice**: nodes (data and components) connected by bonds (flows, pipelines, linkages). The **PRP URL** serves as the primary **anchor** — a single, stable public entry point for instantiation.

### Nodes

| Node | Role |
|------|------|
| **SELF** | Identity, IX-A/B/C, voice, personality |
| **SKILLS** | Capability containers (THINK, WRITE) |
| **EVIDENCE** | Activity log, WRITE/ACT/CREATE entries |
| **SELF-LIBRARY** (`self-library.md`) | Reference-facing governed domains; **CIV-MEM** subdomain; bot lookup first hop |
| **RECURSION-GATE** | Staging area before merge |
| **prompt.py** | Emulation prompt (SYSTEM, ANALYST, LOOKUP, REPHRASE) |
| **CMC** | CIV-MEM domain lookup (SELF-LIBRARY → CMC → LLM) |
| **PRP** | Portable Record Prompt — pasteable identity for any LLM |
| **Telegram / WeChat** | Bot adapters (observation window) |

### Bonds

| Bond | Flow |
|------|------|
| **Pipeline** | Signal detection → RECURSION-GATE → user approval → merge into SELF, EVIDENCE, prompt |
| **PRP refresh** | Merge triggers `export_prp` → PRP file updated → anchor stays in sync with Record |
| **Lookup flow** | User question → SELF-LIBRARY → CIV-MEM (CMC) → LLM → rephrased answer |
| **Evidence linkage** | EVIDENCE entries reference SELF; RECENT in PRP pulls from EVIDENCE |
| **PRP → GitHub** | GITHUB CONNECTIVITY in PRP: model searches repo for system design, governance |

### The Anchor

The PRP URL (e.g. `https://raw.githubusercontent.com/rbtkhn/grace-mar/main/grace-mar-llm.txt`) is the **anchor**: one-fetch instantiation, portable, refreshable. The anchor stays fixed; the lattice grows as SELF, EVIDENCE, LIBRARY, and SKILLS evolve. Post-merge PRP refresh keeps the anchor aligned with the Record.

### Two Instantiation Paths

| Path | What the model has |
|------|--------------------|
| **PRP URL only** | Persona (VOICE, KNOWLEDGE, CURIOSITY, PERSONALITY, RECENT) + GitHub search for system questions. No LIBRARY, no CMC. |
| **Telegram / WeChat bot** | Full persona + LIBRARY → CMC lookup flow. Complete lattice access. |

PRP-only is lightweight and pasteable anywhere; the bot offers the full observation-window experience. See [PORTABLE-RECORD-PROMPT](portable-record-prompt.md).

### Related Architectures

Grace-Mar shares conceptual DNA with other patterns: **multi-agent debate before answer** (e.g. Grok 4.2 — multiple perspectives before synthesis); **society of mind** (agents greater than sum of parts); **user as final arbiter** (human gates what enters the Record). The analyst stages; the user merges. Debate and divergence are valued; convergence is gated.

---

## Emulation Layer

The cognitive fork can optionally power an **emulation** — a live conversational interface that behaves as the self would. The instance supports Telegram (`bot/bot.py`) and WeChat (`bot/wechat_bot.py`). Both share the same emulation core (`bot/core.py`) and use the SELF profile to generate responses constrained to the self's knowledge, vocabulary, and personality. **Teaching/tutoring** is one of the Voice's functions: it answers questions, explains concepts, and helps the user learn — in-character, at the Record's Lexile level, and within the knowledge boundary.

### THINK/WRITE Refinement in Emulation

For triadic-cognition clarity (MIND, RECORD, VOICE):

- `THINK` is the intake function that processes text, video, music/audio, images, and mixed media into evidence-linked signals.
- Those signals feed the **Record** through the gated pipeline.
- `WRITE` is the expression function used by the Voice to render responses from the Record.
- The **Voice** is the interface wrapper around this expression path; it is not identical to `WRITE` by itself.

Canonical flow: **THINK -> Record -> WRITE-through-Voice**.

### The Observation Window Model

The fork exists inside the user's mind. It is the user's mental model of the self, made explicit and structured.

The emulation layer (Telegram, WeChat, or other bot adapters) is not where the fork lives — it is an **observation window**. The user selectively exposes thoughts and information to the fork's awareness through this window. The fork processes what it observes, and the user decides what takes permanent root.

```
┌──────────────────────────────────────────────────┐
│                  USER'S MIND                      │
│                                                    │
│   ┌──────────────────────────────┐                │
│   │      COGNITIVE FORK          │                │
│   │   (structured in self.md)    │                │
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

The emulation layer enforces a **knowledge boundary**: the fork can only reference what has been explicitly merged into its profile. LLM world knowledge must not leak through. See [KNOWLEDGE-BOUNDARY-FRAMEWORK](knowledge-boundary-framework.md) for quantifying, describing, and treating information at the boundary.

**Reactive and agentic:** The current Voice is **reactive** (query-triggered, never unbidden). Future Grace-Mar versions will support both reactive and agentic modes; the Record is the shared substrate. Agentic versions will require additional design (world models, guard rails). See [CONCEPTUAL-FRAMEWORK](conceptual-framework.md) invariant 38.

---

## Input Channels

The fork's profile grows through two independent input channels. Both feed the same gated pipeline and the same profile files.

### Channel 1: Bot (Automated)

**Multi-channel staging:** Telegram, WeChat, operator activity reports, and other callers share **one** `recursion-gate.md` per user. An LLM analyst (`ANALYST_PROMPT` in `bot/prompt.py`) detects profile-relevant signals and stages candidates (with `channel_key`) after bot exchanges; operator scripts may stage without the bot. **One gate, one merge path** — not Telegram-only.

```
User ↔ Bot conversation
       │
       ▼
  Analyst (LLM)
       │
       ▼
  recursion-gate.md (staged candidates)
       │
       ▼
  User approves/rejects
       │
       ▼
  self.md, self-archive.md (EVIDENCE), prompt.py updated
```

**Multiple bots:** You can run several Telegram bots (one per person) from the same codebase and shared LLM: each process uses a different `TELEGRAM_BOT_TOKEN` and `GRACE_MAR_USER_ID`, pointing at different `users/<id>/` profiles. See [MULTI-BOT-CENTRAL-MODEL](multi-bot-central-model.md).

### Channel 2: Operator (Manual)

The user brings real-world observations directly — school worksheets, art projects, overheard conversations, anything observed outside the bot. The operator (this conversation, or any session with the system maintainer) runs signal detection manually and stages candidates the same way.

```
User: "we learned about volcanoes today" [+ optional artifact]
       │
       ▼
  Operator runs signal detection
       │
       ▼
  recursion-gate.md (staged candidates)
       │
       ▼
  User approves/rejects
       │
       ▼
  self.md, self-archive.md (EVIDENCE), prompt.py updated
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
| **Knowledge** | Facts entering the self's awareness | IX-A in self.md |
| **Curiosity** | Topics that catch attention, engagement signals | IX-B in self.md |
| **Personality** | Behavioral patterns, speech traits, values, art style | IX-C in self.md |

### Pipeline Stages

1. **Signal detection** — Identify profile-relevant information in the input
2. **Candidate staging** — Write structured candidates to `recursion-gate.md` with analysis and recommendations
3. **User review** — User approves, rejects, or modifies each candidate
4. **Relay to record** — Approved candidates are merged into `self.md` (profile), **`self-archive.md`** (canonical EVIDENCE / activity log + § VIII), `bot/prompt.py` (emulation prompt), and `session-log.md` (history). This step is the **relay**: raw input has been gated and now crosses into the permanent Record.

### Candidate Structure

Each candidate specifies:
- `mind_category`: knowledge, curiosity, or personality
- `signal_type`: the specific type of signal detected
- `summary`: what was observed
- `profile_target`: which section of self.md it updates
- `suggested_entry`: the proposed profile text
- `prompt_section`: which part of the emulation prompt to update

### The Gate

The gate is the user's discernment. The system proposes; the user disposes. This is not a technical filter — it reflects the user's judgment about what matters and what should become part of the fork's permanent record.

---

## Three-Dimension Mind Model

Post-seed growth is organized into three dimensions within Section IX of self.md. The seed baseline (Sections I–VIII) remains intact; these dimensions capture everything learned after seeding.

### IX-A. Knowledge

Facts that entered the self's awareness through observation. Each entry records what was learned, the source, and how the self would express it in their own words.

### IX-B. Curiosity

Topics that caught the self's attention — what they're drawn to, what resonates. Tracked with an intensity score and the triggering signal. Distinct from seed interests (Section VI) because these emerge from post-seed observation.

### IX-C. Personality (Observed)

Emergent personality patterns detected through the observation window. Art media choices, speech patterns, emotional responses, value expressions, and interpersonal posture may all appear here. These are not declared traits or personality-test results — they are observed, evidence-linked, and documented with contradiction preservation when tensions appear.

### Multi-Dimension Signals

**IX-A/B/C extraction is done by the analyst**, not by the skill modules. Skill modules update only capability (SKILLS); the analyst stages knowledge/curiosity/personality candidates for SELF. One input (e.g. art, music, journal, work artifact) can therefore feed both a skill container and SELF. See [SKILLS-TEMPLATE § III](skills-template.md#iii-skill-interactions-and-the-self).

A single artifact can generate entries in all three dimensions simultaneously. For example, a painted pharaoh portrait produces:
- **Knowledge**: Egyptian pharaohs / King Tut's death mask
- **Curiosity**: Deepening engagement with ancient Egypt
- **Personality**: First use of paint as art medium, bold color choices

This mirrors how real cognition works — a single experience produces knowledge, interest, and identity signals at the same time.

---

---

## Forced Absorption Risk

**Forced absorption** is the risk that unreviewed content enters canonical state through convenience paths — passive indexing, retrieval-as-authorization, synthesis-as-incorporation, or infrastructure defaults that widen write surfaces without explicit review. The term is borrowed from financial regulation: a rule change that silently forces downstream holders to absorb risk they never agreed to. In grace-mar, the downstream holder is the Record.

**Standing line:** Identity never enters canonical state through convenience paths. Only governed review and authorized merge may change the Record.

### How grace-mar defends against it

| Defense | Implementation | What it prevents |
|---------|---------------|------------------|
| Sovereign Merge Rule | `process_approved_candidates.py` is the only merge path; AGENTS.md §2 | Direct writes to self.md, self-archive.md, bot/prompt.py |
| Gated pipeline | `recursion-gate.md` staging → companion approval → merge script | State changes that bypass human review |
| Integrity validator | `scripts/validate-integrity.py` — 12 check families including convenience-path audit | Untraceable candidates, orphan references, stale exports |
| Governance checker | `scripts/governance_checker.py` — regex scan for unauthorized merge patterns | Scripts or agents that attempt direct Record writes |
| Gate review app | `apps/gate-review-app.py` — Flask UI for inspecting pending candidates | Invisible or unreviewed queue state |
| Derived export freshness | `validate-integrity.py` → `validate_derived_exports` | Stale runtime bundles, PRP, or manifests diverging from Record |

### Convenience paths to watch for

1. **Retrieval treated as authorization.** An agent retrieves content from EVIDENCE or prepared context and presents it as Record truth. Retrieval is a read operation, not a governance decision.
2. **Synthesis treated as incorporation.** An agent synthesizes across evidence and the synthesis enters governed state without a gate candidate. Synthesis is analytical work, not a merge.
3. **Prepared context promoted without review.** A runtime bundle, PRP, or prepared-context object is treated as canonical because it looks clean. Prepared context is input to review, not output of review.
4. **Infrastructure defaults that widen write surfaces.** A new script or integration writes to a governed surface without checking the authority model. New tooling must route through the existing pipeline.

### Doctrine reference

This section operationalizes the **forced-absorption** risk pattern defined in the companion-self template ([docs/forced-absorption.md](https://github.com/rbtkhn/companion-self/blob/main/docs/forced-absorption.md)). The template names the risk; this instance implements the defenses.

---

*Document version: 3.1*
*Last updated: April 2026*
