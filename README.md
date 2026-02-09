# cog-em

**Cognitive Emulator** — A system where students teach an AI that grows to emulate their mind.

## Concept

The student teaches the system what they know. The system grows only as the student progresses. Over years, it becomes a cognitive twin: an externalized, queryable representation of the student's knowledge, reasoning patterns, and intellectual personality.

Unlike traditional education tools that teach students, cog-em inverts the relationship: **the student is the teacher**.

## Core Differentiators

- **Direction**: Student teaches system (not system teaches student)
- **Function**: Living credential (diploma + CV that can be queried)
- **Portability**: Cross-border, cross-curriculum, cross-age
- **Duration**: 12+ year relationship (childhood → career)
- **Depth**: Captures *how* you think, not just *what* you know

## Status

**Phase**: Pre-pilot  
**Target**: Solo pilot with 1 student (age 6), 2 months

## Architecture

The cognitive twin has two core modules:

| Module | Contains | Analogue |
|--------|----------|----------|
| **SELF** | Personality, preferences, linguistic style, values, reasoning patterns | CMC's MIND files |
| **SKILLS** | Academic knowledge, practical abilities, creative works, domain expertise | CMC's MEM files |

See [Architecture](docs/ARCHITECTURE.md) for full details.

## Repository Structure

```
cog-em/
├── README.md                    # This file
├── docs/
│   ├── COG-EM-CORE.md          # System core governance (canonical)
│   ├── ARCHITECTURE.md         # SELF + SKILLS module design
│   ├── SELF-TEMPLATE.md        # SELF module governance
│   ├── SKILLS-TEMPLATE.md      # SKILLS module governance
│   ├── EVIDENCE-TEMPLATE.md    # Evidence storage & reading list
│   ├── CONCEPT.md              # Full concept explanation
│   ├── PILOT-PLAN.md           # 2-month pilot structure
│   ├── COMPETITIVE-ANALYSIS.md # Market landscape
│   ├── ANTI-CHEATING.md        # Verification framework
│   ├── DIFFERENTIATION.md      # Competitive moats
│   ├── TEAM.md                 # Hiring plan
│   └── LETTER-TO-STUDENT.md    # Letter to first pilot student
├── users/
│   └── pilot-001/              # First pilot user (6-year-old student)
│       ├── SELF.md             # Personality profile
│       ├── SKILLS.md           # Capability containers
│       ├── EVIDENCE.md         # Reading/Writing/Creation logs
│       └── SESSION-LOG.md      # Interaction history
├── app/                        # Future: iPad app
├── backend/                    # Future: API/services
└── research/
    └── pilot-notes/            # Pilot observations
```

## Quick Links

- [COG-EM-CORE](docs/COG-EM-CORE.md) — **System core governance (canonical)**
- [Architecture](docs/ARCHITECTURE.md) — SELF + SKILLS module design
- [SELF Template](docs/SELF-TEMPLATE.md) — Personality module governance
- [SKILLS Template](docs/SKILLS-TEMPLATE.md) — Capability module governance
- [Evidence Template](docs/EVIDENCE-TEMPLATE.md) — Evidence storage, reading list, attestations
- [Full Concept](docs/CONCEPT.md)
- [Pilot Plan](docs/PILOT-PLAN.md)
- [Competitive Analysis](docs/COMPETITIVE-ANALYSIS.md)

## License

Proprietary. All rights reserved.
