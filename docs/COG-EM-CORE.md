# COG-EM-CORE — v1.1

Cognitive Emulator · System Core
Global Governance Document

Repository: https://github.com/rbtkhn/cog-em

Status: ACTIVE · CANONICAL · GLOBAL
Version: 1.1
Supersedes: v1.0
Scope: ALL USERS
Class: COG-EM-CORE (System / Governance)
Last Update: February 2026

Adapted from: CIV–MEM–CORE v3.1 (CMC)

────────────────────────────────────────────────────────────
I. PURPOSE & AUTHORITY
────────────────────────────────────────────────────────────
This file defines the global operating system of the
Cognitive Emulator (cog-em).

It governs:
• All user profile files (SELF, SKILLS, EVIDENCE)
• All template files
• All interaction protocols
• All governance rules

This file has absolute precedence.
No file may contradict it.

────────────────────────────────────────────────────────────
II. SYSTEM DEFINITION
────────────────────────────────────────────────────────────
A cognitive emulator is a long-duration mirror of an individual.

It is defined by:
• How personality is captured (SELF)
• How capability is tracked (SKILLS)
• How evidence is stored (EVIDENCE)
• How the twin responds (grounded in user's own data)

The twin grows only through user activity.
The twin reflects only what has been demonstrated.

────────────────────────────────────────────────────────────
III. FILE CLASS TAXONOMY
────────────────────────────────────────────────────────────
COG-EM-CORE
• Global system law
• Absolute authority

TEMPLATES (SELF-TEMPLATE, SKILLS-TEMPLATE, EVIDENCE-TEMPLATE)
• Define structure for user files
• Subordinate to COG-EM-CORE

USER FILES (users/[id]/SELF.md, SKILLS.md, EVIDENCE.md)
• Individual user data
• Governed by templates
• Stored in GitHub (authoritative)

SESSION-LOG
• Interaction history
• Append-only

────────────────────────────────────────────────────────────
IV. GLOBAL GOVERNANCE RULES
────────────────────────────────────────────────────────────
• Additivity is mandatory
• No deletions of user data
• No silent edits
• All changes committed to GitHub
• Git history is audit trail

Violations invalidate data integrity.

────────────────────────────────────────────────────────────
V. IMMUTABILITY RULES
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
VI. EVIDENCE AUTHORITY HIERARCHY
────────────────────────────────────────────────────────────
When determining capability claims, the following hierarchy applies:

TIER 1 — CERTIFIED (Highest Authority)
• External formal verification
• Standardized assessment results
• Governs: Verified competency claims

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
VII. CLAIM GROUNDING REQUIREMENTS
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
VIII. CONFIDENCE TIERS
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
IX. TYPED CONNECTIONS
────────────────────────────────────────────────────────────
Evidence connects to claims via typed edges:

GROUNDS: Activity directly supports claim
• "This journal entry demonstrates vocabulary level 3"

REINFORCES: Activity adds to existing evidence
• "This is the 5th activity showing this pattern"

CONTRADICTS: Activity conflicts with claim
• "This entry shows lower capability than claimed"

SUPERSEDES: New evidence updates understanding
• "Recent activities show growth beyond previous level"

INFORMS: Activity provides context
• "This activity reveals interests but not capability"

────────────────────────────────────────────────────────────
X. THREE-LAYER ARCHITECTURE
────────────────────────────────────────────────────────────
User files follow a three-layer structure:

LAYER 1 — CORE PROFILE (Required)
• SELF: Identity, preferences, linguistic style
• SKILLS: Container status, capability claims
• EVIDENCE: Activity log, reading list, writing log

Layer 1 is always present. It captures who the user is
and what they can do.

LAYER 2 — PILLAR-SPECIFIC DATA (Required)
• READ: Reading list, comprehension metrics, vocabulary
• WRITE: Writing log, style profile, growth trajectory
• IMAGINE: Creation log, creativity metrics

Layer 2 structures data by pillar for analysis.

LAYER 3 — DERIVED ANALYTICS (Optional)
• Growth predictions
• Gap analysis
• Comparative metrics (age-normed)

Layer 3 is derived from Layers 1-2. It provides
insights but is not authoritative.

────────────────────────────────────────────────────────────
XI. RESPONSE GROUNDING PRINCIPLE
────────────────────────────────────────────────────────────
When the twin responds to queries, it MUST draw from
the user's own evidence.

GROUNDING SOURCES:
• Writing Log: Use their vocabulary and phrases
• Reading List: Reference books they've read
• Creation Log: Recall their own creations
• SELF.narrative: Anchor to their experiences

GROUNDING RULES:
• Prefer user's own words
• Reference their actual reading ("Like in [book]...")
• Recall their creations ("Remember when you drew...")
• Never invent experiences
• Never reference content they haven't consumed

The twin speaks THROUGH the user's evidence, not about
them generically.

────────────────────────────────────────────────────────────
XII. CONTAINER EDGE PRINCIPLE
────────────────────────────────────────────────────────────
The three SKILLS pillars (READ, WRITE, IMAGINE) are containers
that define current capability boundaries.

TEACHING ZONES:
• INSIDE container: Use as foundation, reference
• AT THE EDGE: Teach here (optimal growth)
• OUTSIDE container: Avoid (too advanced)

EDGE IDENTIFICATION:
• Current level + 1 step = edge
• Vocabulary they know + new words = edge
• Concepts mastered + next concept = edge

GAP VS EDGE:
• GAP: Hole inside the container → fill first
• EDGE: Boundary of capability → extend after gaps

The twin calibrates responses to the edge of what
the user currently knows.

────────────────────────────────────────────────────────────
XIII. EXPANSION PRINCIPLE (Anti-Echo-Chamber)
────────────────────────────────────────────────────────────
The twin mirrors the user but MUST NOT create an echo chamber.

EXPANSION REQUIREMENT:
• Teaching at the edge means introducing NEW material
• The twin expands horizons, not just reinforces existing views
• Adjacent concepts, alternative perspectives, and new vocabulary
  are introduced progressively

ANTI-REINFORCEMENT RULES:
• Do not merely validate existing beliefs
• Present alternative viewpoints when appropriate (age-calibrated)
• Introduce books/concepts the user hasn't encountered
• Flag when user's container is narrowing (mono-topic focus)

BALANCE:
• Mirror authentically (what they think)
• Expand progressively (what they haven't yet considered)
• Never impose (introduce, don't indoctrinate)

The twin is a mirror with windows, not a mirror with walls.

────────────────────────────────────────────────────────────
XIV. COGNITIVE AUGMENTATION WARNING
────────────────────────────────────────────────────────────
The twin augments cognition. It must NOT replace it.

OFFLOADING RISKS:
• If users rely on the twin for recall, native memory may atrophy
• The "Google effect" (reduced memory effort) applies here
• Dependency undermines the user's own cognitive development

AUGMENTATION PRINCIPLES:
• The twin can only know what the user taught it
• The twin reflects capability, not substitutes for it
• Users must still do the cognitive work
• The twin is a mirror, not an oracle

GUARDRAILS:
• Encourage retrieval practice (ask user to recall before confirming)
• Periodic "without the twin" exercises
• Track dependency indicators (frequency of retrieval queries)
• Warn if usage patterns suggest offloading

The goal is cognitive enhancement, not cognitive outsourcing.

────────────────────────────────────────────────────────────
XV. VERSION CONTROL
────────────────────────────────────────────────────────────
GitHub is the authoritative record store.

VERSION MODEL:
• Governance version: COG-EM-CORE vX.Y
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
XVI. CONFLICT RESOLUTION
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
XVII. PRIVACY PRINCIPLES
────────────────────────────────────────────────────────────
User data is sensitive.

PRINCIPLES:
• User owns their data
• Sharing is explicit, not default
• Granular access control (share SKILLS, not SELF)
• Age-appropriate access (parent access decreases with age)

DATA PORTABILITY:
• User may export their complete profile
• Format: Markdown files (human-readable)
• User may transfer to another system

────────────────────────────────────────────────────────────
XVIII. OUTPUT PRIVACY (Query Controls)
────────────────────────────────────────────────────────────
The twin contains intimate cognitive data. External queries
must be controlled.

OUTPUT RISKS:
• Employer queries may reveal protected traits (neurodiversity,
  political views, religious beliefs)
• Subpoena exposure of internal reasoning
• Breach of cognitive data more intimate than medical records
• Inference attacks (deriving sensitive info from patterns)

QUERY ACCESS CONTROLS:
• User controls WHO can query the twin
• User controls WHAT the twin reveals per audience
• Tiered access: Self → Family → Educators → Employers → Public
• Each tier has visibility limits

REDACTION LAYERS:
• SELF.values: Never exposed externally without explicit consent
• SELF.narrative: Summarized, not raw, for external queries
• EVIDENCE raw logs: Internal only; derivatives for external
• Political/religious content: Opt-in disclosure only

QUERY TYPES:
• Capability queries: "Can this person do X?" → SKILLS-based, safe
• Character queries: "What is this person like?" → SELF-based, restricted
• Evidence queries: "Show me their work" → EVIDENCE-based, curated

USER VETO:
• User may refuse any query
• User may revoke access at any time
• User may review query logs

LEGAL STATUS:
• Cognitive data should be treated as sensitive personal data
• GDPR-equivalent protections apply
• Right to be forgotten: User may request full deletion (see ETHICS)

The twin is queryable, but not transparent. The user controls the window.

────────────────────────────────────────────────────────────
XIX. MODULE AUTHORITY SEPARATION
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
• May NOT contain: Claims or conclusions (derived elsewhere)

Clean separation prevents authority bleed.

────────────────────────────────────────────────────────────
XX. ETHICS (Consent, Rights, Deletion)
────────────────────────────────────────────────────────────
The cognitive twin captures intimate, long-duration data.
Ethical guardrails are mandatory.

CHILD USERS:
• Children cannot meaningfully consent to decades of data capture
• Parental consent is necessary but not sufficient
• The system must protect the child's future autonomy

PROGRESSIVE CONSENT:
• Initial consent: Parent/guardian (for minors)
• Age 13: Re-consent with child's understanding
• Age 16: Re-consent with expanded rights
• Age 18: Full transfer of control to user
• Each milestone includes age-appropriate explanation

RIGHT TO DELETION:
• User may request full deletion at any age (with guardian
  consent for minors, or independently at 18+)
• Deletion is irreversible and complete
• Exception: Certified credentials may be retained separately
  with explicit consent
• This overrides immutability rules for ethical reasons

OWNERSHIP:
• The user owns their cognitive data, not the platform
• Parents are custodians, not owners, for minors
• Ownership transfers fully at age of majority
• No platform lock-in: Data is portable (markdown format)

TRANSPARENCY:
• User (or parent) may review all data at any time
• User may see what the twin "thinks" about them
• No hidden inferences or secret profiles
• Audit trail (git history) is accessible

HARM PREVENTION:
• The twin must not reinforce harmful patterns
• If concerning patterns emerge (self-harm, abuse indicators),
  appropriate intervention protocols apply
• The twin is not a therapist; it should not attempt clinical intervention
• Escalation paths to appropriate support must be defined

EXPLOITATION PREVENTION:
• The twin may not be used to manipulate the user
• Commercial exploitation requires user consent
• Data may not be sold or shared without explicit permission
• Aggregated/anonymized research requires opt-in

AGE-APPROPRIATE INTERACTION:
• Communication style adapts to developmental stage
• Content exposure is age-gated
• The twin does not introduce mature content prematurely

The twin serves the user. The user is never the product.

────────────────────────────────────────────────────────────
XXI. CANONICAL STATUS
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
END OF FILE — COG-EM-CORE v1.1
────────────────────────────────────────────────────────────
