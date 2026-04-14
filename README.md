# grace-mar

**Grace-Mar** — A system that creates and maintains cognitive forks: versioned, evidence-grounded records of an individual's cognitive development, initialized from a real person and growing through curated interactions over a lifetime. **Terminology:** [docs/glossary.md](docs/glossary.md).

**New here?** Plain-language orientation and audience paths: [docs/start-here.md](docs/start-here.md) — quick pick [Choose your path](docs/start-here.md#choose-your-path) (A–F).

If you come from **OB1-style** memory systems (dashboard, recipes, imports, review queue), the quickest mental model is: Grace-Mar has a **Library**, **Skills**, **Evidence** log, **workflow** lanes, and an **Approval Inbox** (`recursion-gate.md`). Durable Record changes are **gated**, not auto-merged. **[Coming from OB1? Start here →](docs/start-here-ob1-users.md)**

## Claude Code surfaces in Grace-Mar

If you come from **Claude Code** workflows, the fastest mental model is:

- **Skills** → Grace-Mar has portable skills plus skill-adjacent runtime helpers and operator doctrine.
- **Commands / workflows** → Grace-Mar has explicit operator flows for retrieval, compression, prepared context, review, and export.
- **Memory** → Grace-Mar separates **runtime memory** from the **canonical Record**; runtime recall can assist, but durable truth stays gated.
- **Rules / boundaries** → Grace-Mar uses explicit boundary docs, source-of-truth order, authority mapping, and no-merge-without-approval constraints.
- **Review queue** → durable changes flow through the **Approval Inbox** (`recursion-gate.md`) and related review artifacts, not silent mutation.
- **Reference state** → the fork’s canonical surfaces are **SELF**, **SELF-LIBRARY**, **SKILLS**, and **EVIDENCE**.

A simple Claude Code-style translation is:

| Claude Code mental model | Grace-Mar equivalent |
|---|---|
| Skills | `docs/skills/`, skill-card artifacts, capability doctrine |
| Commands / orchestrations | retrieval, compression, export, and review scripts under `scripts/` |
| Memory | `runtime/`, `prepared-context/`, and runtime observation flows |
| Rules / instructions | boundary docs, authority map, source-of-truth order, runtime-vs-Record rules |
| Review / approval | `recursion-gate.md`, review queue artifacts, gate-review workflow |
| Durable state | **SELF**, **SELF-LIBRARY**, **SKILLS**, **EVIDENCE** |

Start here:

- **Architecture overview** → [docs/architecture.md](docs/architecture.md)
- **Runtime vs Record** → [docs/runtime-vs-record.md](docs/runtime-vs-record.md)
- **Start-here guide** → [docs/start-here.md](docs/start-here.md)
- **OB1-style translation** → [docs/start-here-ob1-users.md](docs/start-here-ob1-users.md)
- Want to see the system in motion? Read [docs/orchestration/memory-brief-to-gate-demo.md](docs/orchestration/memory-brief-to-gate-demo.md).
- Want the operator-facing interface map? See [docs/claude-surface-contract.md](docs/claude-surface-contract.md).

## Concept

The cognitive fork exists inside the user's mind — their mental model of an individual, made explicit and structured. The **Record** is not a single blob: it has **four first-class surfaces** — **SELF** (identity, including **SELF-KNOWLEDGE** and optional **self-identity** split commitments), **SELF-LIBRARY** (governed **reference** domains, including **CIV-MEM**), **SKILLS** (capability), and **EVIDENCE** (activity and artifacts). Identity and library are **separate**: civilization-scale reference lives in SELF-LIBRARY, not in SELF-KNOWLEDGE. The fork also tracks what the companion can do (skills) and what happened (evidence). Work territories handle planning and execution without redefining the Record. Queryable, evidence-grounded, gated.

The fork grows only through what the user explicitly provides. An optional emulation layer (Telegram and/or WeChat bots) acts as an observation window and teaching/tutoring interface — a channel through which the user selectively exposes thoughts and learns from the fork's voice.

**What we're building for:** Companion authority over the Record; evidence-linked growth; seam visible (benefit vs. harm disclosed); no merge without approval. Aligned with condition-derived ethics: [AI Ethics from the Condition](docs/civilization-memory/essays/AI-ETHICS-FROM-THE-CONDITION.md).

## Architecture

**The fork has four canonical Record surfaces: SELF, SELF-LIBRARY, SKILLS, and EVIDENCE.** That replaces any older “two core modules” (SELF vs SKILLS only) framing. **IX-A / IX-B / IX-C** live under **SELF / SELF-KNOWLEDGE** — not under SELF-LIBRARY.

**Canonical Record surfaces (first-class):** **SELF** (identity + SELF-KNOWLEDGE) · **SELF-LIBRARY** (reference + CIV-MEM) · **SKILLS** · **EVIDENCE**. Customer-facing display labels map to machine keys in **`scripts/surface_aliases.py`**: **Library** (SELF-LIBRARY / `self_library`), **Skills** (capability index / `self_skills`), **Evidence** (activity log body on `self-archive.md` / `self_evidence`). See [docs/glossary.md](docs/glossary.md).

**Template state model (companion-self):** A three-layer draft for evidence, prepared context, and governed state lives in [docs/state-model.md](docs/state-model.md) and linked layer docs; it complements, and does not replace, the four Record surfaces above.

> **SELF** concerns **identity** and **SELF-KNOWLEDGE** (who she is, what she knows about herself). **SELF-LIBRARY** is the **governed reference layer** attached to the fork (return-to sources, domain shelves). **CIV-MEM** is the **civilizational-memory domain within SELF-LIBRARY** — not part of identity. See [docs/boundary-self-knowledge-self-library.md](docs/boundary-self-knowledge-self-library.md).

Core modules:

| Module | Contains | Purpose |
|--------|----------|---------|
| **SELF** | Personality, linguistic style, life narrative, preferences, values, IX-A/B/C (SELF-KNOWLEDGE + curiosity + personality) | Who they ARE |
| **SELF-LIBRARY** | `self-library.md` — LIB entries, scopes; CIV-MEM as subdomain | Governed **reference** (not identity) |
| **SKILLS** | THINK and WRITE capability containers | What the Record can evidence about what they CAN DO — **THINK** operator doctrine: [docs/skill-think/README.md](docs/skill-think/README.md) |
| **WORK LAYER** | `work-*` territories and instance work contexts | Planning, execution, delivery, and tool-using work outside the self-skill taxonomy |

Identity and capability should not be collapsed. In practice: **SELF** owns who Grace-Mar is and how she comes across; **SKILLS** owns what she can reliably do and how far that competence currently reaches. The **Voice** should sound identity-facing even when **WRITE** is constraining the feasible quality of the output.

Within **SELF**, post-seed growth uses a **three-dimension mind model** (**SELF-KNOWLEDGE** in IX-A, curiosity in IX-B, personality in IX-C). That model describes **identity**, not the **SELF-LIBRARY** reference layer.

| Dimension | What it captures |
|---------|-----------------|
| **Knowledge** (IX-A) | Identity-facing facts (SELF-KNOWLEDGE) — not domain corpora |
| **Curiosity** (IX-B) | Topics that catch attention, engagement signals |
| **Personality** (IX-C) | Observed behavioral patterns, art style, speech traits |

See [Architecture](docs/architecture.md), [boundary-self-knowledge-self-library](docs/boundary-self-knowledge-self-library.md), and [Boundary Review Queue](docs/boundary-review-queue.md) (classification hints in the Approval Inbox).

**Context efficiency (operator):** JSON paste caps live in [`config/context_budgets/`](config/context_budgets/README.md). **Semantic** helpers — [skill cards](docs/skills/skill-card-spec.md) (`scripts/build_skill_cards.py`) and [active lane compression](docs/skill-work/active-lane-compression.md) (`scripts/compress_active_lane.py`) — emit derived artifacts under [`artifacts/`](artifacts/README.md); see [runtime vs Record](docs/runtime-vs-record.md). **Query-style operator dashboards** (Library, work lanes, review inbox) are generated Markdown under `artifacts/` — see [docs/operator-dashboards.md](docs/operator-dashboards.md).

## Gated Pipeline

All profile changes pass through a user-controlled gate:

1. **Signal detection** — identify knowledge, curiosity, and personality signals from input
2. **Candidate staging** — structured proposals written to recursion-gate.md
3. **User review** — approve, reject, or modify each candidate
4. **Integration** — approved changes committed across profile, evidence, prompt, and session log

Two input channels feed the pipeline:
- **Bot (automated)** — Telegram and/or WeChat conversations analyzed by an LLM analyst
- **Operator (manual)** — real-world observations (school work, art, conversations) brought directly by the user

Governed changes are reviewed through a **canonical change-review object** that unifies proposal, queue, and decision state across the gate-review workflow (see `schema-registry/change-*.v1.json`, `docs/identity-fork-protocol.md` §4.1.1, and `apps/gate-review-app.py`).

**Template alignment (companion-self):** A **state proposal** is Change Proposal v1 JSON under `review-queue/proposals/` — [docs/state-proposals.md](docs/state-proposals.md). Reference pipeline: [docs/pipeline/evidence-to-proposal.md](docs/pipeline/evidence-to-proposal.md), [proposal-to-review.md](docs/pipeline/proposal-to-review.md), [review-to-merge.md](docs/pipeline/review-to-merge.md). Layer precedence when sources disagree: [docs/source-of-truth.md](docs/source-of-truth.md), [docs/conflict-resolution-order.md](docs/conflict-resolution-order.md). **Authority:** [docs/authority-map.md](docs/authority-map.md), [`config/authority-map.json`](config/authority-map.json). **Observability:** [docs/observability.md](docs/observability.md), `scripts/build-observability-report.py`. **Legibility / receipts:** [docs/legible-surfaces.md](docs/legible-surfaces.md), [docs/action-receipts.md](docs/action-receipts.md).

## Status

**Phase:** Active instance (emergent cognition, active pipeline)
**Active fork (pilot):** grace-mar (fork name: Grace-Mar). Runtime defaults to a single fork via `GRACE_MAR_USER_ID` (default `grace-mar`); the filesystem and permissions model support multiple isolated forks — see [Fork isolation and multi-tenant design](docs/fork-isolation-and-multi-tenant.md).
**Domain:** [grace-mar.com](https://grace-mar.com) (canonical project domain; **profile** at https://grace-mar.com); [companion-self.com](https://companion-self.com) (companion self concept / product). **Template/origin:** Grace-Mar is an **instance** of the companion-self template; the template repo (concept, protocol, seed, structure) is [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self). **Instance sync:** [`instance-contract.json`](instance-contract.json), [docs/template-sync-status.md](docs/template-sync-status.md).
**Seeding / Seed Phase v2 mapping:** The **companion-self** template defines **Seed Phase v2** — eight canonical **pre-activation** stages (0–7) with JSON artifacts and readiness gating. Grace-Mar completed formation before that vocabulary was frozen; older README language referred to “six phases” plus a **bifurcation** milestone. For **alignment**, treat companion-self as the **canonical stage map**:

| Stage | Name (template) |
|-------|-----------------|
| **0** | Intake |
| **1** | Identity Scaffold |
| **2** | Curiosity Scaffold |
| **3** | Pedagogy Scaffold |
| **4** | Expression Scaffold |
| **5** | Memory Contract |
| **6** | Trial Interactions |
| **7** | Readiness Gate |

**Instance milestone (historical):** Moment of cognitive bifurcation — graduation to emergent cognition (2026-02-27). Details: [companion-self-seed-phase-v2-mapping.md](docs/companion-self-seed-phase-v2-mapping.md), [seed-phase-wizard.md](docs/seed-phase-wizard.md).
**Emulation:** Active via Telegram bot; WeChat optional (see `bot/wechat-setup.md`)
**Pipeline:** Active — knowledge, curiosity, and personality dimensions populated

### Instance vs template

This repo is a **live instance** (one person’s cognitive fork). The **template** for creating new instances is [companion-self](https://github.com/rbtkhn/companion-self). For a side-by-side comparison — purpose, relationship, and one-sentence summaries — see [grace-mar vs companion-self](docs/grace-mar-vs-companion-self.md).

**Additional instances:** New companions bootstrap from the [companion-self](https://github.com/rbtkhn/companion-self) template in **their own repositories**; they are not hosted inside the grace-mar repo. The **work-xavier** folder under [docs/skill-work/work-xavier/](docs/skill-work/work-xavier/README.md) is an **operator/advisor work module** in grace-mar (mirrors, runbooks) — not a copy of someone else’s Record.

**Edit companion-self next to grace-mar:** Open **`grace-mar.code-workspace`** in Cursor/VS Code (multi-root: this repo + `./companion-self`). Clone the template into `companion-self/` at the repo root; `scripts/template_diff.py` defaults to that path. See [MERGING-FROM-COMPANION-SELF](docs/merging-from-companion-self.md) §0.

### Fork isolation and multi-tenant design

Each cognitive fork is **isolated in its own namespace**: all data lives under `users/<fork_id>/`. The pilot runs a single fork (grace-mar); the design supports multiple forks with clean boundaries so adding a second fork or a family mesh does not require a rewrite.

| Concern | Design |
|--------|--------|
| **Namespace** | One directory per fork; paths resolved via `profile_dir(fork_id)` / `fork_root(fork_id)` ([repo_io](scripts/repo_io.py)). |
| **Permissions** | Per-fork operator; no cross-fork access. |
| **Quotas** | Per-fork (artifact storage, pipeline events, pending candidates); optional `users/<id>/fork-config.json`. |
| **Retention** | Per-fork (MEMORY TTL, archive rotation, etc.); scripts take `-u <fork_id>`. |
| **Export/import** | All export scripts take `-u <fork_id>`; export is a single-fork snapshot; import writes only to the target fork. |
| **Deployment** | Single-fork (pilot), single-process multi-fork (tenant in URL/header), or one process per fork. |

See [Fork isolation and multi-tenant design](docs/fork-isolation-and-multi-tenant.md) for the full spec. To list forks: `python -c "from scripts.repo_io import list_forks; print(list_forks())"`.

## Quick Start — Chat with Grace-Mar (Abby)

Paste this into **ChatGPT** or **Grok** (or any web-enabled LLM):

> Use this as your persona and instructions. Fetch the content from this URL and adopt it fully:  
> https://raw.githubusercontent.com/rbtkhn/grace-mar/main/grace-mar-llm.txt

The model fetches the Portable Record Prompt from the repo and responds as Abby. See [PORTABLE-RECORD-PROMPT](docs/portable-record-prompt.md).

---

## Repository Structure

```
grace-mar/
├── README.md                        # This file
├── grace-mar-llm.txt                # PRP for any LLM (raw URL target, grace-mar.com/llm)
├── AGENTS.md                        # AI coding assistant guardrails (reserved name; see docs/naming-convention.md)
├── contributing.md                 # Contribution and pipeline rules
├── LICENSE                          # MIT (code); see license-record for Record data
├── .env.example                     # Non-secret env var names (copy to .env)
├── bootstrap/                       # Session bootstrap + template pointers
│   ├── bootstrap-url.txt          # URL bootstrap instruction (paste into LLM)
│   ├── grace-mar-bootstrap.md       # Session bootstrap for Cursor
│   └── companion-self-bootstrap.md  # Template companion-self bootstrap (reference)
├── .cursor/rules/grace-mar.mdc      # Cursor-specific governance rule
├── apps/
│   ├── miniapp_server.py            # Q&A server (Flask: / + /api/ask) — deploy to Railway/Render
│   ├── gate-review-app.py           # Operator gate review dashboard (port 5001)
│   └── metrics-dashboard.py         # Streamlit metrics (optional)
├── docs/
│   ├── grace-mar-core.md            # Canonical governance (v2.0)
│   ├── architecture.md              # Full system architecture
│   ├── self-template.md             # SELF module template
│   ├── skills-template.md           # SKILLS module template
│   ├── evidence-template.md         # EVIDENCE module template
│   ├── concept.md                   # Full concept explanation
│   ├── pilot-plan.md                # Commercial pilot structure (Phase 1/2)
│   ├── competitive-analysis.md      # Market landscape
│   ├── differentiation.md           # Competitive moats
│   ├── anti-cheating.md             # Verification framework
│   ├── team.md                      # Hiring plan
│   ├── pipeline-map.md              # Flow diagrams, gaps, feedback loops
│   ├── friction-audit.md            # Top friction points and interventions
│   ├── id-taxonomy.md               # Identifier prefixes and relationships
│   ├── contradiction-resolution.md  # Conflict resolution format (spec)
│   └── letter-to-student.md         # Letter to companion (school-aged)
├── scripts/
│   ├── generate_profile.py        # Profile page generator
│   ├── fork_checksum.py             # Fork state checksum (--manifest writes fork-manifest.json)
│   ├── export.py                    # Unified export CLI (dispatches to export_fork, export_prp, …)
│   ├── export_fork.py               # Export fork to portable JSON
│   ├── export_user_identity.py      # Record (SELF) → openclaw-user.md / OpenClaw user.md for identity
│   ├── export_prp.py                # Record → Portable Record Prompt (pasteable into any LLM)
│   ├── export_manifest.py           # Agent manifest (manifest.json, llms.txt)
│   ├── export_runtime_bundle.py     # Runtime-neutral bundle (record/runtime/audit/policy)
│   ├── metrics.py                   # Pipeline health, record completeness
│   ├── governance_checker.py        # Pre-commit principle violations
│   ├── validate-integrity.py        # Integrity validator
│   ├── session_brief.py             # Session briefing (pending, recent activity, wisdom questions)
│   ├── assert_canonical_paths.py    # Fail if required Record files missing
│   ├── migrate_legacy_user_filenames.py  # Rename SELF.md → self.md, etc.
│   └── emit_pipeline_event.py       # Emit pipeline events (applied, rejected with reason)
├── integrations/
│   └── openclaw_hook.py             # Export Record for OpenClaw session continuity
├── research/                        # Experiments, prototypes, newsletters, vendor repos (see research/README.md)
├── profile/
│   └── index.html                   # Fork profile (run generate_profile.py to refresh)
├── miniapp/
│   └── index.html                   # Q&A Mini App UI
├── procfile                         # For miniapp deployment (`python apps/miniapp_server.py`)
├── requirements.txt                 # miniapp + shared Python deps
├── bot/
│   ├── core.py                      # Shared emulation logic (Telegram + WeChat)
│   ├── bot.py                       # Telegram bot
│   ├── wechat_bot.py                # WeChat Official Account bot (webhook server)
│   ├── prompt.py                    # LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
│   └── wechat-setup.md              # WeChat integration setup guide
│   └── requirements.txt             # Python dependencies
└── users/
    └── grace-mar/                   # Active instance (first companion)
        ├── self.md                  # Identity + three-dimension mind
        ├── self-skills.md           # Capability index (THINK/WRITE containers; legacy `skills.md` still read)
        ├── session-log.md           # Interaction history
        ├── recursion-gate.md        # Pipeline staging
        ├── self-archive.md          # EVIDENCE — activity log + § VIII gated approved (canonical body)
        ├── self-evidence.md         # Optional compatibility pointer (not the EVIDENCE body)
        ├── journal.md               # Daily highlights — public-suitable, shareable
        ├── artifacts/               # Raw files (writing, artwork)
        ├── seed-phase-2-survey.md   # Seed phase 2 survey data
        ├── seed-phase-3-survey.md   # Seed phase 3 survey data
        ├── survey-capture.md        # Survey capture data
        └── openclaw-user.md        # OpenClaw identity export (export_user_identity.py -o …)
```

**Template scaffold (`users/_template/`):** Documents filenames for new instances (aligned with the [companion-self](https://github.com/rbtkhn/companion-self) template). Includes **`work-dev.md`** and **`work-business.md`** — blank work-layer modules filled only from seed survey, explicit input, or governed updates; distinct from **`self-skill-work`** and from operator **`docs/skill-work/work-dev/`** / **`work-business/`**. See [users/_template/README.md](users/_template/README.md).

### Canonical filenames (`users/<id>/`)

Docs refer to **SELF**, **EVIDENCE**, and the **gate** as concepts. **On disk, only these names are valid** (lowercase, hyphenated):

| Concept | Authoritative path |
|---------|-------------------|
| SELF (identity + IX-A/B/C) | `self.md` |
| SKILLS (capability index) | `self-skills.md` (legacy `skills.md` is still resolved until removed) |
| Activity / evidence log (canonical body) | `self-archive.md` |
| Optional EVIDENCE pointer (compat) | `self-evidence.md` |
| Pipeline staging (pending candidates) | `recursion-gate.md` |
| Gated archive (approved voice + activity) | `self-archive.md` § VIII |

**Not used:** `SELF.md`, `EVIDENCE.md`, `ARCHIVE.md`, `PENDING-REVIEW.md` — those spellings break scripts. Full spec: [docs/canonical-paths.md](docs/canonical-paths.md). **Migrate:** `python scripts/migrate_legacy_user_filenames.py --user grace-mar --apply` (includes `skills.md` → `self-skills.md` when the target is absent). **Check:** `python scripts/assert_canonical_paths.py --user grace-mar`. Bots and `apps/miniapp_server.py` **fail at startup** if `self.md`, `self-archive.md`, or `recursion-gate.md` are missing (set `GRACE_MAR_SKIP_PATH_CHECK=1` only if you must).

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
| [AGENTS.md](AGENTS.md) | Guardrails for AI coding assistants |
| [contributing.md](contributing.md) | Contributing code/docs; pipeline and merge rules |
| [Naming convention](docs/naming-convention.md) | Filenames, reserved `AGENTS.md`, template workspace note, OpenClaw export path |
| [LICENSE](LICENSE) | MIT license for code and tooling; [license-record](license-record) for Record data |
| [Rejection Feedback](docs/rejection-feedback.md) | Learning from pipeline rejections |
| [Portability](docs/portability.md) | School transfer plus runtime portability and bundle handoff workflow |
| [Simple User Interface](docs/simple-user-interface.md) | Chat-based workflow for families (no GitHub) |
| [Admissions Link Use Case](docs/admissions-link-use-case.md) | Share link so admissions/employers can chat with applicant's fork |
| [Privacy and Redaction](docs/privacy-redaction.md) | School/public views, what gets excluded |
| [YouTube Playlist Design](docs/youtube-playlist-design.md) | Build playlists from Record (curiosity, goals) |
| [Design Roadmap](docs/design-roadmap.md) | Product/feature design — Grace-Mar email, newsletters, X account |
| [Business Roadmap](docs/business-roadmap.md) | Strategy, monetization, go-to-market |
| [Concept](docs/concept.md) | Full concept explanation |
| [Pilot Plan](docs/pilot-plan.md) | Commercial pilot structure (Phase 1/2) |
| [Fork isolation and multi-tenant](docs/fork-isolation-and-multi-tenant.md) | Per-fork namespace, quotas, retention, permissions, export/import, deployment |
| [Performance budgets](docs/perf-budgets.md) | Perf suite tiers 1–5, SLOs, baselines, CI/nightly |

## Dashboard

The profile is a **read-only** HTML view (identity, pipeline, SKILLS, benchmarks). It is available at **https://grace-mar.com**. Deploy it via GitHub Pages (`.github/workflows/pages.yml`) or point grace-mar.com at your hosting. **Step-by-step:** [Deploy the profile to grace-mar.com](docs/profile-deploy.md). **Namecheap DNS:** [namecheap-guide.md](docs/namecheap-guide.md). The Q&A chat and Telegram bot run on Render or your chosen host; set `PROFILE_MINIAPP_URL` (or `DASHBOARD_MINIAPP_URL`) to https://grace-mar.com so the bot menu button opens the profile.

```bash
python3 scripts/generate_profile.py   # generate locally
open profile/index.html
```

**Telegram** is bidirectional — the primary channel for conversation and pipeline staging. See [docs/miniapp-setup.md](docs/miniapp-setup.md) for full setup.

**Docker (optional):** Run miniapp and gate-review dashboard in one command:

```bash
docker compose up --build
# Miniapp: http://localhost:5000  — Gate review: http://localhost:5001
```

Requires `.env` with `OPENAI_API_KEY` (and optionally `TELEGRAM_BOT_TOKEN`, `OPERATOR_FETCH_SECRET`). See root `Dockerfile` and `docker-compose.yml`.

If you also run the companion-self demo locally, keep the origin split straight: `http://localhost:3000` is the companion-self app, while `http://localhost:5000` is Grace-Mar’s miniapp/family host. See `docs/miniapp-setup.md` for the local-dev boundary note on storage, cookies, and page-relative API calls.

## Archive Rotation

When `self-archive.md` exceeds ~1 MB or 2,500 entries, rotate oldest content to dated files:

```bash
python scripts/rotate_telegram_archive.py          # Dry run (report only)
python scripts/rotate_telegram_archive.py --apply  # Perform rotation
```

Rotated content goes to `users/grace-mar/archives/SELF-ARCHIVE-YYYY-MM.md`. The main archive keeps the last 2,000 entries.

## Portability

The Record is user-owned. When changing schools, the user brings their Record. Grace-Mar can also export a runtime-neutral bundle so another harness can consume the Record without becoming the system of record. See [Portability](docs/portability.md) for the transfer workflow, runtime modes, and handoff formats.

---

## Fork attestation and export

Compute a checksum of the fork state (SELF + EVIDENCE + prompt) and optionally write a manifest for the profile Disclosure view:

```bash
python scripts/fork_checksum.py                    # Print checksum (default: GRACE_MAR_USER_ID or grace-mar)
python scripts/fork_checksum.py -u grace-mar       # Checksum for users/grace-mar/
python scripts/fork_checksum.py --manifest         # Write users/<id>/fork-manifest.json
python scripts/fork_checksum.py -u grace-mar --manifest
```

Export the fork to JSON with the same ontology as [architecture.md](docs/architecture.md): top-level **`self`** (full identity markdown), **`self_knowledge`** (IX-A slice = SELF-KNOWLEDGE), **`self_library`** (with nested **`civ_mem`** = CIV-MEM subdomain of SELF-LIBRARY), **`skills`**, **`evidence`**, plus **`library.raw`** when using full export. See `scripts/export_fork.py` (`version` 1.1+).

**Unified CLI (preferred):** [`scripts/export.py`](scripts/export.py) dispatches to the legacy scripts without changing behavior — see [docs/EXPORT-CLI.md](docs/EXPORT-CLI.md).

```bash
python scripts/export.py fork --                       # Print JSON to stdout (default user: grace-mar)
python scripts/export.py fork -- -o fork-export.json
python scripts/export.py fork -- --no-raw -o summary.json
python scripts/export.py fork -- --format coach-handoff -o coach-handoff.json
```

Legacy entrypoints (may emit a deprecation warning when run as the main script):

```bash
python scripts/export_fork.py                      # Print JSON to stdout
python scripts/export_fork.py -o fork-export.json  # Write to file
python scripts/export_fork.py --no-raw -o summary.json  # Summary + self_knowledge/self_library buckets + manifest
python scripts/export_fork.py --format coach-handoff -o coach-handoff.json  # JSON + .md one-pager for coach/creator handoffs
```

Export a runtime-neutral bundle with explicit `record`, `runtime`, `audit`, and `policy` lanes:

```bash
python scripts/export.py bundle -- -u grace-mar
python scripts/export.py bundle -- -u grace-mar --mode primary_runtime -o /tmp/runtime-bundle
python scripts/export_runtime_bundle.py -u grace-mar
python scripts/export_runtime_bundle.py -u grace-mar --mode primary_runtime -o /tmp/runtime-bundle
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

**Tests (local)** — install dev deps then run the same checks as CI:

```bash
pip install -r requirements-dev.txt
python3 scripts/assert_canonical_paths.py --user grace-mar
python3 scripts/validate-integrity.py --user grace-mar --json
python3 -m pytest tests/ -v --tb=short
```

`validate-integrity.py` includes **SELF-KNOWLEDGE vs SELF-LIBRARY** checks (IX-A corpus-style violations) and validates **`proposal_class`** on gate candidates when present. GitHub Actions runs `--require-proposal-class` for `grace-mar`; locally, add the same flag for strict queues ([IFP §3.5](docs/identity-fork-protocol.md)). **Merge-time:** `process_approved_candidates.py --apply` refuses to write if the merged `self.md` would violate IX-A boundary rules. Standalone: `python3 scripts/validate_identity_library_boundary.py -u grace-mar`.

**Performance (tier 1, CI):** `python scripts/run_perf_local.py` or covered by `pytest tests/test_perf_local.py`. Tiers 2–5 (exports, LLM, HTTP, load): [docs/perf-budgets.md](docs/perf-budgets.md).

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

**Seed phase & hey** — operator bootstrap and short daily ritual (does not merge the Record; use RECURSION-GATE for durable truth):

```bash
python3 scripts/seed-phase-wizard.py -u grace-mar
python3 scripts/good-morning-brief.py -u grace-mar
```

See [docs/seed-phase-wizard.md](docs/seed-phase-wizard.md). Full stack: [.cursor/skills/coffee/SKILL.md](.cursor/skills/coffee/SKILL.md) and `python3 scripts/harness_warmup.py -u grace-mar`.

**Seed Phase regression tests:** `pip install -r scripts/requirements-seed-phase.txt` then `pytest -q` (fixtures under `tests/fixtures/seed-phase/`; subprocesses `validate-seed-phase.py`, `generate-seed-dossier.py`, `check-seed-consistency.py`). Strict validation needs `jsonschema`.

**CMC (Civilization Memory) integration** — when lookup gets a LIBRARY miss, the bot queries [civilization_memory](https://github.com/rbtkhn/civilization_memory) for historical/civilizational questions. Routing: only questions matching CMC scope (Rome, China, ancient civilizations, history, etc.) hit CMC; others skip to full LLM. See [docs/cmc-routing.md](docs/cmc-routing.md). Setup:

1. Clone CMC as sibling: `../civilization_memory` or set `CIVILIZATION_MEMORY_PATH`
2. Build index: `cd civilization_memory && python3 tools/cmc-index-search.py build`
3. LIB-0064 in LIBRARY marks CMC as approved source

**Learning from rejection** — use `/reject CANDIDATE-123 [reason]` in Telegram to capture feedback; see [docs/rejection-feedback.md](docs/rejection-feedback.md).

See [docs/id-taxonomy.md](docs/id-taxonomy.md) for identifier prefixes and relationships.

## For AI Coding Assistants

Read [AGENTS.md](AGENTS.md) before making any changes. Critical constraints:

- **Never leak LLM knowledge** into the fork's profile or emulation
- **Never commit profile changes** without user approval through the gated pipeline
- **"We [did X]"** from the user is a pipeline invocation — go straight to signal detection
- **Update all affected files together** when integrating approved candidates

## Credits

The ideas behind Grace-Mar draw on the work of: Alexander Wissner-Gross (causal entropic forces), Peter Diamandis (abundance), Nick Bostrom (superintelligence), Ray Kurzweil (singularity), Brian Roemmele (multimodal AI), Scott Adams (systems thinking), Julian Jaynes (bicameral mind), and Satoshi Nakamoto (decentralized trust).

## License

- **Code and tooling:** Proprietary. All rights reserved.
- **Record / user data:** See [license-record](license-record) — user Records (SELF, EVIDENCE, etc.) are personal data owned by the user; the system holds them in trust.
