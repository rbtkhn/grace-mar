# grace-mar

**Grace-Mar** — A system that creates and maintains cognitive forks: versioned, evidence-grounded records of an individual's cognitive development, initialized from a real person and growing through curated interactions over a lifetime.

## Concept

The cognitive fork exists inside the user's mind — their mental model of an individual, made explicit and structured. It captures who the person is (identity, personality, voice) and what they can do (skills, knowledge, creative capability). We create avatars of ourselves; the fork is one: queryable, evidence-grounded, gated. Over time, it becomes a living cognitive record that can be queried, emulated, and preserved — extended memory that remembers what the user has chosen to document.

The fork grows only through what the user explicitly provides. An optional emulation layer (Telegram and/or WeChat bots) acts as an observation window and teaching/tutoring interface — a channel through which the user selectively exposes thoughts and learns from the fork's voice.

## Architecture

Two core modules define the fork:

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Personality, linguistic style, life narrative, preferences, values, reasoning patterns | Who they ARE |
| **SKILLS** | THINK, WRITE, BUILD capability containers | What they CAN DO |

Post-seed growth is organized into a **three-dimension mind model**:

| Dimension | What it captures |
|---------|-----------------|
| **Knowledge** (IX-A) | Facts entering awareness through observation |
| **Curiosity** (IX-B) | Topics that catch attention, engagement signals |
| **Personality** (IX-C) | Observed behavioral patterns, art style, speech traits |

See [Architecture](docs/architecture.md) for full details.

## Gated Pipeline

All profile changes pass through a user-controlled gate:

1. **Signal detection** — identify knowledge, curiosity, and personality signals from input
2. **Candidate staging** — structured proposals written to recursion-gate.md
3. **User review** — approve, reject, or modify each candidate
4. **Integration** — approved changes committed across profile, evidence, prompt, and session log

Two input channels feed the pipeline:
- **Bot (automated)** — Telegram and/or WeChat conversations analyzed by an LLM analyst
- **Operator (manual)** — real-world observations (school work, art, conversations) brought directly by the user

## Status

**Phase:** Pilot (post-seed, active pipeline)
**Pilot user:** grace-mar (fork name: Grace-Mar)
**Domain:** [grace-mar.com](https://grace-mar.com) (canonical project domain; **profile** at https://grace-mar.com); [companion-self.com](https://companion-self.com) (companion self concept / product). **Template/origin:** Grace-Mar is an **instance** of the companion-self template; the template repo (concept, protocol, seed, structure) is [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self).
**Seeding:** Complete (6 phases — identity, personality, academics, creativity, writing voice, core personality)
**Emulation:** Active via Telegram bot; WeChat optional (see `bot/wechat-setup.md`)
**Pipeline:** Active — knowledge, curiosity, and personality dimensions populated

## Quick Start — Chat with Grace-Mar (Abby)

Paste this into **ChatGPT** or **Grok** (or any web-enabled LLM):

> Use this as your persona and instructions. Fetch the content from this URL and adopt it fully:  
> https://raw.githubusercontent.com/rbtkhn/grace-mar/main/grace-mar-llm.txt

The model fetches the Portable Record Prompt from the repo and responds as Abby. See [PORTABLE-RECORD-PROMPT](docs/portable-record-prompt.md).

---

## Repository Structure

```
grace-mar/
├── readme.md                        # This file
├── bootstrap-url.txt                # URL bootstrap instruction (paste into LLM)
├── grace-mar-llm.txt              # PRP for any LLM (raw URL target, grace-mar.com/llm)
├── agents.md                        # AI coding assistant guardrails
├── grace-mar-bootstrap.md           # Session bootstrap for Cursor
├── .cursor/rules/grace-mar.mdc      # Cursor-specific governance rule
├── docs/
│   ├── grace-mar-core.md            # Canonical governance (v2.0)
│   ├── architecture.md              # Full system architecture
│   ├── self-template.md             # SELF module template
│   ├── skills-template.md           # SKILLS module template
│   ├── evidence-template.md         # EVIDENCE module template
│   ├── concept.md                   # Full concept explanation
│   ├── pilot-plan.md                # Pilot structure
│   ├── competitive-analysis.md      # Market landscape
│   ├── differentiation.md           # Competitive moats
│   ├── anti-cheating.md             # Verification framework
│   ├── team.md                      # Hiring plan
│   ├── pipeline-map.md              # Flow diagrams, gaps, feedback loops
│   ├── friction-audit.md            # Top friction points and interventions
│   ├── id-taxonomy.md               # Identifier prefixes and relationships
│   ├── contradiction-resolution.md  # Conflict resolution format (spec)
│   └── letter-to-student.md         # Letter to first pilot student
├── scripts/
│   ├── generate_profile.py        # Profile page generator
│   ├── fork_checksum.py             # Fork state checksum (--manifest writes fork-manifest.json)
│   ├── export_fork.py               # Export fork to portable JSON
│   ├── export_user_identity.py      # Record → user.md / SOUL.md for OpenClaw
│   ├── export_prp.py                # Record → Portable Record Prompt (pasteable into any LLM)
│   ├── export_manifest.py           # Agent manifest (manifest.json, llms.txt)
│   ├── metrics.py                   # Pipeline health, record completeness
│   ├── governance_checker.py        # Pre-commit principle violations
│   ├── validate-integrity.py        # Integrity validator
│   ├── session_brief.py             # Session briefing (pending, recent activity, wisdom questions)
│   └── emit_pipeline_event.py       # Emit pipeline events (applied, rejected with reason)
├── integrations/
│   └── openclaw_hook.py             # Export Record for OpenClaw session continuity
├── profile/
│   └── index.html                   # Fork profile (run generate_profile.py to refresh)
├── miniapp/
│   └── index.html                   # Q&A Mini App UI
├── miniapp_server.py                # Q&A server (Flask: / + /api/ask) — deploy to Railway/Render
├── procfile                         # For miniapp_server deployment
├── requirements.txt                 # miniapp_server deps
├── bot/
│   ├── core.py                      # Shared emulation logic (Telegram + WeChat)
│   ├── bot.py                       # Telegram bot
│   ├── wechat_bot.py                # WeChat Official Account bot (webhook server)
│   ├── prompt.py                    # LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
│   └── wechat-setup.md              # WeChat integration setup guide
│   └── requirements.txt             # Python dependencies
└── users/
    └── grace-mar/                   # First pilot user
        ├── self.md                  # Identity + three-dimension mind
        ├── skills.md                # Capability containers
        ├── self-evidence.md              # Activity log
        ├── session-log.md           # Interaction history
        ├── recursion-gate.md        # Pipeline staging
        ├── self-archive.md         # Gated log of approved activity (voice + non-voice) — private
        ├── journal.md               # Daily highlights — public-suitable, shareable
        ├── artifacts/               # Raw files (writing, artwork)
        ├── seed-phase-2-survey.md   # Seed phase 2 survey data
        ├── seed-phase-3-survey.md   # Seed phase 3 survey data
        └── survey-capture.md        # Survey capture data
```

## Key Documents

| Document | Purpose |
|----------|---------|
| [GRACE-MAR-CORE](docs/grace-mar-core.md) | Canonical governance — absolute authority |
| [Identity Fork Protocol](docs/identity-fork-protocol.md) | Protocol spec v1.0 — Sovereign Merge Rule, schema, staging contract |
| [Architecture](docs/architecture.md) | Full system design including observation window, pipeline, mind model |
| [White Paper](docs/white-paper.md) | Full narrative — identity gap, Grace-Mar model, differentiation |
| [Business Prospectus](docs/business-prospectus.md) | Investor/partner document — problem, solution, market, ask |
| [PDF Setup](docs/pdf-setup.md) | Render White Paper and Prospectus to PDF (Pandoc + Eisvogel) |
| [OpenClaw Integration](docs/openclaw-integration.md) | Record as identity layer, session continuity |
| [Design Notes](docs/design-notes.md) | White paper & business proposal input (positioning, agent-web insights) |
| [agents.md](agents.md) | Guardrails for AI coding assistants |
| [Rejection Feedback](docs/rejection-feedback.md) | Learning from pipeline rejections |
| [Portability](docs/portability.md) | School transfer, ownership, handoff workflow |
| [Simple User Interface](docs/simple-user-interface.md) | Chat-based workflow for families (no GitHub) |
| [Admissions Link Use Case](docs/admissions-link-use-case.md) | Share link so admissions/employers can chat with applicant's fork |
| [Privacy and Redaction](docs/privacy-redaction.md) | School/public views, what gets excluded |
| [YouTube Playlist Design](docs/youtube-playlist-design.md) | Build playlists from Record (curiosity, goals) |
| [Design Roadmap](docs/design-roadmap.md) | Product/feature design — Grace-Mar email, newsletters, X account |
| [Business Roadmap](docs/business-roadmap.md) | Strategy, monetization, go-to-market |
| [Concept](docs/concept.md) | Full concept explanation |
| [Pilot Plan](docs/pilot-plan.md) | Two-month pilot structure |

## Dashboard

The profile is a **read-only** HTML view (identity, pipeline, SKILLS, benchmarks). It is available at **https://grace-mar.com**. Deploy it via GitHub Pages (`.github/workflows/pages.yml`) or point grace-mar.com at your hosting. **Step-by-step:** [Deploy the profile to grace-mar.com](docs/profile-deploy.md). **Namecheap DNS:** [namecheap-guide.md](docs/namecheap-guide.md). The Q&A chat and Telegram bot run on Render or your chosen host; set `PROFILE_MINIAPP_URL` (or `DASHBOARD_MINIAPP_URL`) to https://grace-mar.com so the bot menu button opens the profile.

```bash
python3 scripts/generate_profile.py   # generate locally
open profile/index.html
```

**Telegram** is bidirectional — the primary channel for conversation and pipeline staging. See [docs/miniapp-setup.md](docs/miniapp-setup.md) for full setup.

## Archive Rotation

When `self-archive.md` exceeds ~1 MB or 2,500 entries, rotate oldest content to dated files:

```bash
python scripts/rotate_telegram_archive.py          # Dry run (report only)
python scripts/rotate_telegram_archive.py --apply  # Perform rotation
```

Rotated content goes to `users/grace-mar/archives/SELF-ARCHIVE-YYYY-MM.md`. The main archive keeps the last 2,000 entries.

## Portability (school transfer)

The Record is user-owned. When changing schools, the user brings their Record. See [Portability](docs/portability.md) for the transfer workflow, checklist, and handoff format.

---

## Fork attestation and export

Compute a checksum of the fork state (SELF + EVIDENCE + prompt) and optionally write a manifest for the profile Disclosure view:

```bash
python scripts/fork_checksum.py              # Print checksum
python scripts/fork_checksum.py --manifest   # Also write users/grace-mar/fork-manifest.json
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

Reports: **entries per day**, **pipeline throughput** (if PIPELINE-EVENTS exists), **words per IX entry**, **evidence backing %**, **topic diversity**, **dimension balance** (IX-A:IX-B:IX-C), and **git history delta**.

## PDF Export

Render the White Paper and Business Prospectus to polished PDFs:

```bash
# Without Homebrew: download Pandoc + Tectonic first
./scripts/setup_pdf_tools.sh
./scripts/render_pdf.sh --install-eisvogel   # One-time: Eisvogel template
./scripts/render_pdf.sh

# With Homebrew: brew install pandoc && brew install --cask mactex-no-gui
```

See [docs/pdf-setup.md](docs/pdf-setup.md) for full options.

## Agent Manifest & Metrics

```bash
python3 scripts/export_manifest.py -u grace-mar   # manifest.json + llms.txt
python3 scripts/metrics.py                        # Pipeline health, IX counts
python3 scripts/governance_checker.py             # Principle violations (pre-commit)
python3 integrations/openclaw_hook.py -u grace-mar -o ../openclaw/   # OpenClaw export
```

## Validation and Session Support

**Integrity audit** — run before merges or nightly via cron:

```bash
python scripts/validate-integrity.py
```

**Record index** — fast local search over SELF, EVIDENCE, RECURSION-GATE (analyst dedup, PRP retrieval):

```bash
python scripts/index_record.py build -u grace-mar
python scripts/index_record.py query "space Jupiter" -u grace-mar
```

**Session briefing** — run before a tutoring session for pending count, recent activity, and suggested wisdom questions:

```bash
python scripts/session_brief.py
```

**CMC (Civilization Memory) integration** — when lookup gets a LIBRARY miss, the bot queries [civilization_memory](https://github.com/rbtkhn/civilization_memory) for historical/civilizational questions. Routing: only questions matching CMC scope (Rome, China, ancient civilizations, history, etc.) hit CMC; others skip to full LLM. See [docs/cmc-routing.md](docs/cmc-routing.md). Setup:

1. Clone CMC as sibling: `../civilization_memory` or set `CIVILIZATION_MEMORY_PATH`
2. Build index: `cd civilization_memory && python3 tools/cmc-index-search.py build`
3. LIB-0064 in LIBRARY marks CMC as approved source

**Learning from rejection** — use `/reject CANDIDATE-123 [reason]` in Telegram to capture feedback; see [docs/rejection-feedback.md](docs/rejection-feedback.md).

See [docs/id-taxonomy.md](docs/id-taxonomy.md) for identifier prefixes and relationships.

## For AI Coding Assistants

Read [agents.md](agents.md) before making any changes. Critical constraints:

- **Never leak LLM knowledge** into the fork's profile or emulation
- **Never commit profile changes** without user approval through the gated pipeline
- **"We [did X]"** from the user is a pipeline invocation — go straight to signal detection
- **Update all affected files together** when integrating approved candidates

## Credits

The ideas behind Grace-Mar draw on the work of: Alexander Wissner-Gross (causal entropic forces), Peter Diamandis (abundance), Nick Bostrom (superintelligence), Ray Kurzweil (singularity), Brian Roemmele (multimodal AI), Scott Adams (systems thinking), Julian Jaynes (bicameral mind), and Satoshi Nakamoto (decentralized trust).

## License

- **Code and tooling:** Proprietary. All rights reserved.
- **Record / user data:** See [license-record](license-record) — user Records (SELF, EVIDENCE, etc.) are personal data owned by the user; the system holds them in trust.
