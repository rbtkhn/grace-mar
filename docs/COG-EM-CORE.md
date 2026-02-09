# COG-EM-CORE — v1.0

Cognitive Emulator · System Core
Global Governance Document

Repository: https://github.com/rbtkhn/cog-em

Status: ACTIVE · CANONICAL · GLOBAL
Version: 1.0
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
XIII. VERSION CONTROL
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
XIV. CONFLICT RESOLUTION
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
XV. PRIVACY PRINCIPLES
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
XVI. MODULE AUTHORITY SEPARATION
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
XVII. CANONICAL STATUS
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
END OF FILE — COG-EM-CORE v1.0
────────────────────────────────────────────────────────────
