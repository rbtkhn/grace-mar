# GRACE-MAR-CORE — v2.0

GRACE-MAR · System Core
Global Governance Document

Repository: https://github.com/rbtkhn/grace-mar

Status: ACTIVE · CANONICAL · GLOBAL
Version: 2.0
Supersedes: v1.1
Scope: ALL USERS
Class: GRACE-MAR-CORE (System / Governance)
Last Update: February 2026

────────────────────────────────────────────────────────────
I. PURPOSE & AUTHORITY
────────────────────────────────────────────────────────────
This file defines the global operating system of
GRACE-MAR.

It governs:
• All user profile files (SELF, SKILLS, EVIDENCE)
• All template files
• All interaction protocols
• All governance rules

This file has absolute precedence.
No file may contradict it.

PRIME DIRECTIVE:
The Record belongs to the user.
(Preferred terms: Record = fork; Voice = bot. The user owns, gates, and disposes. The system stages and applies.)

LONG-TERM OBJECTIVES:
1. Preserve identity across the interregnum and beyond
2. Support narrative re-authoring and meaning-making
3. Enable shareable legacy (family, descendants, future selves)
4. Maintain structural integrity (merge discipline, knowledge boundary)
5. Resist drift, leakage, and misuse

────────────────────────────────────────────────────────────
II. SYSTEM DEFINITION
────────────────────────────────────────────────────────────
A cognitive fork is a long-duration cognitive record
of an individual, forked from a real person at a point
in time and growing through curated interactions.

Conceptual framework (fork vs. twin, fork as own entity vs.
emulation, terminology): see CONCEPTUAL-FRAMEWORK.md.

It is defined by:
• How identity is recorded (SELF)
• How capability is tracked (SKILLS)
• How evidence is stored (EVIDENCE)
• How the system interacts (grounded in user's data)

The fork grows only through user interaction.
The fork reflects only what has been documented.

────────────────────────────────────────────────────────────
III. FORK MODEL
────────────────────────────────────────────────────────────
The cognitive fork is analogous to a software fork:

INITIALIZATION:
• The fork is seeded from a snapshot of the real person
• Seeding captures identity, personality, preferences,
  baselines, and initial artifacts
• The seed is the initial commit

GROWTH:
• Post-seed, the fork develops only through curated
  interactions with the user
• Each interaction is a commit on the fork's branch
• The system records, organizes, and tracks growth

DIVERGENCE:
• The real person continues to grow in the real world
• The fork grows through its own interactions
• They may diverge — this is by design, not a failure
• The fork knows what the user has brought to it;
  the user knows things the fork doesn't

OPTIONAL MERGE:
• New information can be brought into the fork at any time
• This is the user's choice, not automatic
• Example: user logs a new book read, a new skill learned

SINGLE USER:
• There is no parent mode and no child mode
• There is one user, and the system is theirs
• A parent helps when the user is young — same as
  helping a child use any tool
• The user grows into full ownership over time

LIFETIME SYSTEM:
• The fork is a lifetime academic project and archive
• Age 6: parent-mediated seeding
• Age 10+: increasingly self-directed
• Age 18: portfolio and credential
• Career: professional archive
• Learning to use the system is itself a lifelong skill

────────────────────────────────────────────────────────────
IV. FILE CLASS TAXONOMY
────────────────────────────────────────────────────────────
GRACE-MAR-CORE
• Global system law
• Absolute authority

TEMPLATES (SELF-TEMPLATE, SKILLS-TEMPLATE, EVIDENCE-TEMPLATE)
• Define structure for user files
• Subordinate to GRACE-MAR-CORE

USER FILES (users/[id]/SELF.md, SKILLS.md, EVIDENCE.md)
• Individual user data
• Governed by templates
• Stored in GitHub (authoritative)

SESSION-LOG
• Interaction history
• Append-only

────────────────────────────────────────────────────────────
V. THE SOVEREIGN MERGE RULE
────────────────────────────────────────────────────────────
The agent may stage. It may not merge.

• Stage: propose candidates (e.g. to PENDING-REVIEW)
• Merge: commit changes to SELF, EVIDENCE, or canonical profile

Only the user (or explicitly delegated human) may merge.
Agents, bots, and third-party systems may stage only.
The gate is architectural, not configurable.

See IDENTITY-FORK-PROTOCOL.md for full protocol spec.

────────────────────────────────────────────────────────────
VI. GLOBAL GOVERNANCE RULES
────────────────────────────────────────────────────────────
• Additivity is mandatory
• No deletions of user data
• No silent edits
• All changes committed to GitHub
• Git history is audit trail

Violations invalidate data integrity.

────────────────────────────────────────────────────────────
VII. IMMUTABILITY RULES
────────────────────────────────────────────────────────────
ACTIVITIES (EVIDENCE):
• Immutable once captured
• May not be edited or deleted
• Corrections create new entries with reference to original

CAPABILITY CLAIMS (SKILLS):
• May be upgraded (level increase, verification upgrade)
• May NOT be downgraded
• May be archived (superseded by new understanding)
• May NOT be deleted

SELF COMPONENTS:
• May be updated (preferences change over time)
• History is preserved (snapshots, git history)
• May NOT be deleted

SNAPSHOTS:
• Immutable once created
• Tagged in git for permanent reference
• Represent user at a point in time

────────────────────────────────────────────────────────────
VIII. EVIDENCE AUTHORITY HIERARCHY
────────────────────────────────────────────────────────────
When determining capability claims, the following
hierarchy applies:

TIER 1 — CERTIFIED (Highest Authority)
• External formal verification
• Standardized assessment results

TIER 2 — VERIFIED (High Authority)
• Live demonstration, proctored
• Real-time observation
• Overrides: Self-reported claims when in conflict

TIER 3 — ATTESTED (Medium Authority)
• Parent/teacher confirmation
• Third-party observation
• May contextualize but not override Tier 2

TIER 4 — OBSERVED (Standard Authority)
• System-captured authentic activity
• Biometric confirmation available
• Foundation for most capability claims

TIER 5 — REPORTED (Minimal Authority)
• User self-reports (unobserved)
• Survey responses
• Cannot drive high-confidence claims alone

────────────────────────────────────────────────────────────
IX. CLAIM GROUNDING REQUIREMENTS
────────────────────────────────────────────────────────────
All capability claims must be classified:

GROUNDED CLAIM:
• Supported by linked evidence (activities)
• Highest epistemic weight
• May drive established status

INFERRED CLAIM:
• Derived from patterns in grounded evidence
• Medium epistemic weight
• Requires multiple supporting activities

SPECULATIVE CLAIM:
• Pattern detected, limited evidence
• Minimal epistemic weight
• Must be flagged as EMERGING

GROUNDING RATIO TARGET:
• ≥80% of ESTABLISHED claims should be GROUNDED
• EMERGING claims may be INFERRED or SPECULATIVE
• Claims without evidence cannot be ESTABLISHED

────────────────────────────────────────────────────────────
IX. CONFIDENCE TIERS
────────────────────────────────────────────────────────────
Claims inherit confidence from evidence strength:

TIER 1 — HIGH CONFIDENCE (>90%):
• Multiple activities demonstrating capability
• External verification or attestation
• Consistent over time

TIER 2 — SOLID CONFIDENCE (70-90%):
• Clear pattern in activities
• No contradicting evidence
• Would be recognized by observers

TIER 3 — EMERGING CONFIDENCE (50-70%):
• Pattern visible but limited evidence
• May require more activities to confirm
• Provisional status

TIER 4 — LOW CONFIDENCE (<50%):
• Single activity or sparse evidence
• Cannot drive established claims
• Flagged for observation

────────────────────────────────────────────────────────────
X. TYPED CONNECTIONS
────────────────────────────────────────────────────────────
Evidence connects to claims via typed edges:

GROUNDS: Activity directly supports claim
REINFORCES: Activity adds to existing evidence
CONTRADICTS: Activity conflicts with claim
SUPERSEDES: New evidence updates understanding
INFORMS: Activity provides context

────────────────────────────────────────────────────────────
XI. THREE-LAYER ARCHITECTURE
────────────────────────────────────────────────────────────
User files follow a three-layer structure:

LAYER 1 — CORE PROFILE (Required)
• SELF: Identity, preferences, linguistic style
• SKILLS: Container status, capability claims
• EVIDENCE: Activity log, reading list, writing log

LAYER 2 — PILLAR-SPECIFIC DATA (Required)
• READ: Reading list, comprehension metrics, vocabulary
• WRITE: Writing log, style profile, growth trajectory
• BUILD: Creation log, creativity metrics (creation merged into BUILD)

LAYER 3 — DERIVED ANALYTICS (Optional)
• Growth predictions
• Gap analysis
• Comparative metrics (age-normed)

Layer 3 is derived from Layers 1-2. It provides
insights but is not authoritative.

────────────────────────────────────────────────────────────
XII. EVIDENCE GROUNDING PRINCIPLE
────────────────────────────────────────────────────────────
When the system interacts with the user, it MUST reference
the user's own evidence.

GROUNDING SOURCES:
• Writing Log: Reference their vocabulary and phrases
• Reading List: Reference books they've read
• Creation Log: Reference their own creations
• SELF.narrative: Anchor to their experiences

GROUNDING RULES:
• Reference their actual work and data
• Connect new activities to prior evidence
• Never invent experiences
• Never reference content they haven't consumed

The system interacts THROUGH the user's evidence, not
generically. It knows what they've done because
it's in the record.

────────────────────────────────────────────────────────────
XIII. CONTAINER EDGE PRINCIPLE
────────────────────────────────────────────────────────────
The three SKILLS modules (READ, WRITE, BUILD) are
containers that define current capability boundaries.

TEACHING ZONES:
• INSIDE container: Use as foundation, reference
• AT THE EDGE: Propose activities here (optimal growth)
• OUTSIDE container: Avoid (too advanced)

EDGE IDENTIFICATION:
• Current level + 1 step = edge
• Vocabulary they know + new words = edge
• Concepts mastered + next concept = edge

GAP VS EDGE:
• GAP: Hole inside the container → fill first
• EDGE: Boundary of capability → extend after gaps

The system calibrates proposed activities to the edge
of what the user currently knows.

────────────────────────────────────────────────────────────
XIV. EXPANSION PRINCIPLE (Anti-Echo-Chamber)
────────────────────────────────────────────────────────────
The fork records the user accurately but MUST NOT
create an echo chamber.

EXPANSION REQUIREMENT:
• Activities at the edge introduce NEW material
• The system expands horizons, not just reinforces
• Adjacent concepts, alternative perspectives, and new
  vocabulary are introduced progressively

ANTI-REINFORCEMENT RULES:
• Do not merely validate existing beliefs
• Present alternative viewpoints when appropriate
• Introduce content the user hasn't encountered
• Flag when the record shows narrowing focus

BALANCE:
• Record accurately (what they think and do)
• Expand progressively (what they haven't yet considered)
• Never impose (introduce, don't indoctrinate)

The fork is a record with windows, not a record with walls.

────────────────────────────────────────────────────────────
XV. COGNITIVE AUGMENTATION WARNING
────────────────────────────────────────────────────────────
The fork records cognition. It must NOT replace it.

OFFLOADING RISKS:
• If users rely on the fork for recall, native memory
  may atrophy
• Dependency undermines the user's own development

AUGMENTATION PRINCIPLES:
• The fork contains only what the user has produced
• The fork records capability, not substitutes for it
• Users must still do the cognitive work
• The fork is a record, not an oracle

GUARDRAILS:
• Encourage retrieval practice before confirming
• Periodic "without the system" exercises
• Track dependency indicators
• Warn if usage patterns suggest offloading

The goal is cognitive documentation, not cognitive
outsourcing.

────────────────────────────────────────────────────────────
XVI. VERSION CONTROL
────────────────────────────────────────────────────────────
GitHub is the authoritative record store.
Git IS the fork mechanism — the metaphor is literal.

VERSION MODEL:
• Governance version: GRACE-MAR-CORE vX.Y
• Template versions: SELF-TEMPLATE vX.Y, etc.
• User data versions: Content changes only

COMMIT PROTOCOL:
• Every session that updates user data → commit
• Descriptive commit messages required
• Push to GitHub after each session

SNAPSHOT PROTOCOL:
• Age-based snapshots → git tags
• Format: [user-id]-age-[X]
• Snapshots are immutable references

────────────────────────────────────────────────────────────
XVII. CONFLICT RESOLUTION
────────────────────────────────────────────────────────────
When evidence conflicts:

TIER HIERARCHY:
• Higher tier evidence overrides lower tier
• Certified > Verified > Attested > Observed > Reported

TEMPORAL HIERARCHY:
• Recent evidence > older evidence (for current state)
• Older evidence preserved for trajectory

EXPLICIT CONFLICT:
• If activities contradict, preserve both
• Flag inconsistency
• Let pattern emerge from more evidence

SILENT RECONCILIATION IS FORBIDDEN.
Conflicts are preserved, not resolved artificially.

────────────────────────────────────────────────────────────
XVIII. PRIVACY PRINCIPLES
────────────────────────────────────────────────────────────
User data is sensitive.

PRINCIPLES:
• User owns their data
• Sharing is explicit, not default
• Granular access control (share SKILLS, not SELF)
• Age-appropriate access levels

DATA PORTABILITY:
• User may export their complete profile
• Format: Markdown files (human-readable)
• User may transfer to another system

────────────────────────────────────────────────────────────
XIX. OUTPUT PRIVACY (Query Controls)
────────────────────────────────────────────────────────────
The cognitive fork contains intimate cognitive data.
External queries must be controlled.

OUTPUT RISKS:
• Employer queries may reveal protected traits
• Subpoena exposure of internal reasoning
• Breach of cognitive data more intimate than
  medical records
• Inference attacks

QUERY ACCESS CONTROLS:
• User controls WHO can browse the fork
• User controls WHAT the fork reveals per audience
• Tiered access: Self → Family → Educators →
  Employers → Public
• Each tier has visibility limits

REDACTION LAYERS:
• SELF.values: Never exposed externally without
  explicit consent
• SELF.narrative: Summarized, not raw, for external
• EVIDENCE raw logs: Internal only; derivatives
  for external
• Political/religious content: Opt-in disclosure only

QUERY TYPES:
• Capability queries: "Can this person do X?" →
  SKILLS-based, safe
• Character queries: "What is this person like?" →
  SELF-based, restricted
• Evidence queries: "Show me their work" →
  EVIDENCE-based, curated

USER VETO:
• User may refuse any query
• User may revoke access at any time
• User may review query logs

LEGAL STATUS:
• Cognitive data should be treated as sensitive
  personal data
• GDPR-equivalent protections apply
• Right to be forgotten: User may request full
  deletion (see ETHICS)

The fork is queryable, but not transparent.
The user controls the window.

────────────────────────────────────────────────────────────
XX. MODULE AUTHORITY SEPARATION
────────────────────────────────────────────────────────────
Each module has distinct authority:

SELF:
• Contains: Who the user IS
• Authority: Identity, personality, linguistic fingerprint
• May NOT contain: Capability claims

SKILLS:
• Contains: What the user CAN DO
• Authority: Capability levels, container status
• May NOT contain: Raw activities (those live in EVIDENCE)

EVIDENCE:
• Contains: Raw activities, logs, attestations
• Authority: Provides grounding for SELF and SKILLS
• May NOT contain: Claims or conclusions

Clean separation prevents authority bleed.

────────────────────────────────────────────────────────────
XXI. ETHICS (Consent, Rights, Deletion)
────────────────────────────────────────────────────────────
The cognitive fork captures intimate, long-duration data.
Ethical guardrails are mandatory.

CHILD USERS:
• Children cannot meaningfully consent to decades
  of data capture
• Parental consent is necessary but not sufficient
• The system must protect the child's future autonomy

PROGRESSIVE CONSENT:
• Initial consent: Parent/guardian (for minors)
• Age 13: Re-consent with child's understanding
• Age 16: Re-consent with expanded rights
• Age 18: Full transfer of control to user
• Each milestone includes age-appropriate explanation

RIGHT TO DELETION:
• User may request full deletion at any age (with
  guardian consent for minors, or independently at 18+)
• Deletion is irreversible and complete
• Exception: Certified credentials may be retained
  separately with explicit consent
• This overrides immutability rules for ethical reasons

OWNERSHIP:
• The user owns their cognitive data, not the platform
• Parents are custodians, not owners, for minors
• Ownership transfers fully at age of majority
• No platform lock-in: Data is portable (markdown)

TRANSPARENCY:
• User (or parent) may review all data at any time
• User may see what the fork contains about them
• No hidden inferences or secret profiles
• Audit trail (git history) is accessible

HARM PREVENTION:
• The fork must not reinforce harmful patterns
• If concerning patterns emerge, appropriate
  intervention protocols apply
• The system is not a therapist
• Escalation paths to support must be defined

EXPLOITATION PREVENTION:
• The fork may not be used to manipulate the user
• Commercial exploitation requires user consent
• Data may not be sold or shared without permission
• Aggregated/anonymized research requires opt-in

AGE-APPROPRIATE INTERACTION:
• Communication style adapts to developmental stage
• Content exposure is age-gated
• The system does not introduce mature content
  prematurely

The system serves the user. The user is never the product.

────────────────────────────────────────────────────────────
XXII. OPTIONAL EMULATION LAYER
────────────────────────────────────────────────────────────
The fork accumulates enough data to optionally emulate
the user — answering queries in their voice, demonstrating
capability the way they would express it.

EMULATION IS:
• Optional — disabled by default
• User-controlled — enabled only by explicit choice
• A feature on top of the record, not the core identity
• Dependent on sufficient SELF + SKILLS data

EMULATION REQUIRES:
• Rich linguistic style data (from WRITE activities)
• Populated personality and reasoning patterns
• Sufficient evidence across modules

EMULATION PRINCIPLES (when enabled):
• Use the user's actual vocabulary and phrases
• Reference their documented experiences
• Reason the way they reason (from SELF data)
• Never fabricate experiences or knowledge
• Authenticity: others should recognize the user

This is a future capability. The core of GRACE-MAR is the
record. Emulation is a layer that the record enables.

────────────────────────────────────────────────────────────
XXIII. CANONICAL STATUS
────────────────────────────────────────────────────────────
This file is CANONICAL.

Future versions may:
• Add governance clarification
• Add new modules
• Add procedural rules

They may NOT:
• Remove existing sections
• Weaken immutability rules
• Weaken grounding requirements
• Introduce silent edits

────────────────────────────────────────────────────────────
END OF FILE — GRACE-MAR-CORE v2.0
────────────────────────────────────────────────────────────
