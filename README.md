# grace-mar

**Grace-Mar** — A system that creates and maintains cognitive forks: versioned, evidence-grounded records of an individual's cognitive development, initialized from a real person and growing through curated interactions over a lifetime.

## Concept

The cognitive fork exists inside the user's mind — their mental model of an individual, made explicit and structured. It captures who the person is (identity, personality, voice) and what they can do (skills, knowledge, creative capability). Over time, the fork becomes a living cognitive record that can be queried, emulated, and preserved.

The fork grows only through what the user explicitly provides. An optional emulation layer (Telegram and/or WeChat bots) acts as an observation window — a channel through which the user selectively exposes thoughts and information to the fork's awareness.

## Architecture

Two core modules define the fork:

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Personality, linguistic style, life narrative, preferences, values, reasoning patterns | Who they ARE |
| **SKILLS** | READ, WRITE, IMAGINE, BUSINESS capability containers | What they CAN DO |

Post-seed growth is organized into a **three-channel mind model**:

| Channel | What it captures |
|---------|-----------------|
| **Knowledge** (IX-A) | Facts entering awareness through observation |
| **Curiosity** (IX-B) | Topics that catch attention, engagement signals |
| **Personality** (IX-C) | Observed behavioral patterns, art style, speech traits |

See [Architecture](docs/ARCHITECTURE.md) for full details.

## Gated Pipeline

All profile changes pass through a user-controlled gate:

1. **Signal detection** — identify knowledge, curiosity, and personality signals from input
2. **Candidate staging** — structured proposals written to PENDING-REVIEW.md
3. **User review** — approve, reject, or modify each candidate
4. **Integration** — approved changes committed across profile, evidence, prompt, and session log

Two input channels feed the pipeline:
- **Bot (automated)** — Telegram and/or WeChat conversations analyzed by an LLM analyst
- **Operator (manual)** — real-world observations (school work, art, conversations) brought directly by the user

## Status

**Phase:** Pilot (post-seed, active pipeline)
**Pilot user:** pilot-001 (fork name: Grace-Mar)
**Seeding:** Complete (6 phases — identity, personality, academics, creativity, writing voice, core personality)
**Emulation:** Active via Telegram bot; WeChat optional (see `bot/WECHAT-SETUP.md`)
**Pipeline:** Active — knowledge, curiosity, and personality channels populated

## Repository Structure

```
grace-mar/
├── README.md                        # This file
├── AGENTS.md                        # AI coding assistant guardrails
├── GRACE-MAR-BOOTSTRAP.md           # Session bootstrap for Cursor
├── .cursor/rules/grace-mar.mdc      # Cursor-specific governance rule
├── docs/
│   ├── GRACE-MAR-CORE.md            # Canonical governance (v2.0)
│   ├── ARCHITECTURE.md              # Full system architecture
│   ├── SELF-TEMPLATE.md             # SELF module template
│   ├── SKILLS-TEMPLATE.md           # SKILLS module template
│   ├── EVIDENCE-TEMPLATE.md         # EVIDENCE module template
│   ├── CONCEPT.md                   # Full concept explanation
│   ├── PILOT-PLAN.md                # Pilot structure
│   ├── COMPETITIVE-ANALYSIS.md      # Market landscape
│   ├── DIFFERENTIATION.md           # Competitive moats
│   ├── ANTI-CHEATING.md             # Verification framework
│   ├── TEAM.md                      # Hiring plan
│   ├── PIPELINE-MAP.md              # Flow diagrams, gaps, feedback loops
│   ├── FRICTION-AUDIT.md            # Top friction points and interventions
│   ├── ID-TAXONOMY.md               # Identifier prefixes and relationships
│   ├── CONTRADICTION-RESOLUTION.md  # Conflict resolution format (spec)
│   └── LETTER-TO-STUDENT.md         # Letter to first pilot student
├── scripts/
│   ├── generate_dashboard.py        # Dashboard generator
│   ├── fork_checksum.py            # Fork state checksum (--manifest writes FORK-MANIFEST.json)
│   ├── export_fork.py              # Export fork to portable JSON
│   └── validate-integrity.py       # Integrity validator
├── dashboard/
│   └── index.html                   # Fork dashboard (run generate_dashboard.py to refresh)
├── miniapp/
│   └── index.html                   # Q&A Mini App UI
├── miniapp_server.py                # Q&A server (Flask: / + /api/ask) — deploy to Railway/Render
├── Procfile                         # For miniapp_server deployment
├── requirements.txt                 # miniapp_server deps
├── bot/
│   ├── core.py                      # Shared emulation logic (Telegram + WeChat)
│   ├── bot.py                       # Telegram bot
│   ├── wechat_bot.py                # WeChat Official Account bot (webhook server)
│   ├── prompt.py                    # LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
│   └── WECHAT-SETUP.md              # WeChat integration setup guide
│   └── requirements.txt             # Python dependencies
└── users/
    └── pilot-001/                   # First pilot user
        ├── SELF.md                  # Identity + three-channel mind
        ├── SKILLS.md                # Capability containers
        ├── EVIDENCE.md              # Activity log
        ├── SESSION-LOG.md           # Interaction history
        ├── PENDING-REVIEW.md        # Pipeline staging
        ├── ARCHIVE.md               # Conversation archive (Telegram, Mini App)
        ├── artifacts/               # Raw files (writing, artwork)
        ├── SEED-PHASE-2-SURVEY.md   # Seed phase 2 survey data
        ├── SEED-PHASE-3-SURVEY.md   # Seed phase 3 survey data
        └── SURVEY-CAPTURE.md        # Survey capture data
```

## Key Documents

| Document | Purpose |
|----------|---------|
| [GRACE-MAR-CORE](docs/GRACE-MAR-CORE.md) | Canonical governance — absolute authority |
| [Architecture](docs/ARCHITECTURE.md) | Full system design including observation window, pipeline, mind model |
| [Design Notes](docs/DESIGN-NOTES.md) | White paper & business proposal input (positioning, agent-web insights) |
| [AGENTS.md](AGENTS.md) | Guardrails for AI coding assistants |
| [Portability](docs/PORTABILITY.md) | School transfer, ownership, handoff workflow |
| [Simple User Interface](docs/SIMPLE-USER-INTERFACE.md) | Chat-based workflow for families (no GitHub) |
| [Admissions Link Use Case](docs/ADMISSIONS-LINK-USE-CASE.md) | Share link so admissions/employers can chat with applicant's fork |
| [Privacy and Redaction](docs/PRIVACY-REDACTION.md) | School/public views, what gets excluded |
| [Concept](docs/CONCEPT.md) | Full concept explanation |
| [Pilot Plan](docs/PILOT-PLAN.md) | Two-month pilot structure |

## Dashboard

Generate an HTML dashboard for the pilot fork (summary, pipeline queue, SKILLS, recent exchanges, benchmarks):

```bash
python3 scripts/generate_dashboard.py
open dashboard/index.html
```

The dashboard is **browser-only** (e.g. deployed to GitHub Pages). A separate **Q&A Mini App** lets users ask Grace-Mar questions and see her voice — deploy `miniapp_server.py` to Railway/Render and set `DASHBOARD_MINIAPP_URL` in `bot/.env` to that URL. See [docs/MINIAPP-SETUP.md](docs/MINIAPP-SETUP.md).

## Archive Rotation

When `ARCHIVE.md` exceeds ~1 MB or 2,500 entries, rotate oldest content to dated files:

```bash
python scripts/rotate_telegram_archive.py          # Dry run (report only)
python scripts/rotate_telegram_archive.py --apply  # Perform rotation
```

Rotated content goes to `users/pilot-001/archives/ARCHIVE-YYYY-MM.md`. The main archive keeps the last 2,000 entries.

## Portability (school transfer)

The Record is user-owned. When changing schools, the user brings their Record. See [Portability](docs/PORTABILITY.md) for the transfer workflow, checklist, and handoff format.

---

## Fork attestation and export

Compute a checksum of the fork state (SELF + EVIDENCE + prompt) and optionally write a manifest for the dashboard Disclosure view:

```bash
python scripts/fork_checksum.py              # Print checksum
python scripts/fork_checksum.py --manifest   # Also write users/pilot-001/FORK-MANIFEST.json
```

Export the fork to a single JSON file (SELF, EVIDENCE, LIBRARY, optional manifest) for backup or portability:

```bash
python scripts/export_fork.py                      # Print JSON to stdout
python scripts/export_fork.py -o fork-export.json  # Write to file
python scripts/export_fork.py --no-raw -o summary.json  # Summary + manifest only
```

## Uniqueness measurement

Quantify how different Grace-Mar's responses are from a generic LLM:

```bash
pip install textstat  # optional, for readability gap
python3 scripts/measure_uniqueness.py
python3 scripts/measure_uniqueness.py --limit 5   # quick run
python3 scripts/measure_uniqueness.py -v          # verbose
```

Outputs: **abstention score** (boundary enforcement), **divergence score** (answer uniqueness via embeddings), **readability gap** (simpler = Lexile-constrained), and a **composite uniqueness** value.

## Growth rate and cognitive density

Measure how fast the fork is growing and how dense its content is:

```bash
python3 scripts/measure_growth_and_density.py
```

Reports: **entries per day**, **pipeline throughput** (if PIPELINE-EVENTS exists), **words per IX entry**, **evidence backing %**, **topic diversity**, **channel balance** (IX-A:IX-B:IX-C), and **git history delta**.

## Validation

Run the integrity validator to check evidence references, SELF structure, and PENDING-REVIEW format:

```bash
python scripts/validate-integrity.py
```

See [docs/ID-TAXONOMY.md](docs/ID-TAXONOMY.md) for identifier prefixes and relationships.

## For AI Coding Assistants

Read [AGENTS.md](AGENTS.md) before making any changes. Critical constraints:

- **Never leak LLM knowledge** into the fork's profile or emulation
- **Never commit profile changes** without user approval through the gated pipeline
- **"We [did X]"** from the user is a pipeline invocation — go straight to signal detection
- **Update all affected files together** when integrating approved candidates

## License

Proprietary. All rights reserved.
