# Cici (`Xavier-x01/Cici`) — ingest summary (WORK)

**Captured:** 2026-04-13  
**Territory:** work-xavier **evidence** — not Xavier’s Record; not a gate merge.  
**Canonical URL:** [https://github.com/Xavier-x01/Cici](https://github.com/Xavier-x01/Cici)

## Purpose

Operator snapshot of the **public GitHub** view of **[Cici](https://github.com/Xavier-x01/Cici)** — README positioning, **repo root** layout, and **`CLAUDE.md`**-style **session persona** (screenshot capture). Use for **advisor / coaching** and alignment with [xavier-journal](../xavier-journal/README.md) / digest (`--repo` default).

**Cross-check:** Public README text summarized below matches the [live repo](https://github.com/Xavier-x01/Cici) as of this ingest window (Open Brain instance framing — not application server source in-tree).

## Public README — high-signal lines (live text)

- **Positioning:** **Xavier’s personal Open Brain instance** — config and documentation; **no server code** in-repo; upstream **OB1**; **BrewMind** as business brand; AI memory via **private Supabase** (see `docs/personal/README.md` for workflow notes — not reproduced here).
- **Open Brain (OB1):** Self-owned persistent memory — **Supabase** + **MCP**; vendor-neutral clients; vector search; dedup fingerprinting; rough cost note at personal scale.
- **Architecture (diagram):** AI clients → MCP (HTTP) → Supabase Edge Function (`open-brain-mcp`) → PostgreSQL (`thoughts`, pgvector, RLS) → OpenRouter for embeddings/models.
- **Governed State Model (Phase 1):** Git-first durable truth — **Evidence** (`evidence/`) → **Prepared context** (`prepared-context/`) → **Governed state** (`users/cici/governed-state/`); **`proposals/`** queue; owner approves. Pointers: `docs/governed-state-doctrine.md`, `docs/migration-compatibility.md`.
- **Repository layout (abbreviated):** `CLAUDE.md`, `README.md`, `evidence/`, `prepared-context/`, `users/` (`_template`, `cici/`), `proposals/` (+ schemas, queue/approved/rejected), `config/authority-map.json`, `bridges/supabase/`, `docs/*`, `scripts/validate-governed-state.py`.
- **Languages (GitHub):** Python **100%** (linguist bar — reflects scripts/validation, not OB1 Edge runtime).

## Screenshots (this folder)

| File | What the capture shows |
|------|-------------------------|
| [cici-github-readme-2026-04-13.png](cici-github-readme-2026-04-13.png) | Long vertical **README** — OB1 overview, architecture, governed state, layout tree. |
| [cici-github-repo-files-2026-04-13.png](cici-github-repo-files-2026-04-13.png) | **Code** tab — root listing (`.cursor/rules`, `.github/workflows`, `bridges/supabase`, `config`, `docs`, `evidence`, `prepared-context`, `proposals`, `scripts`, `users`, `CLAUDE.md`, `README.md`, …). |
| [cici-claude-md-persona-2026-04-13.png](cici-claude-md-persona-2026-04-13.png) | **`CLAUDE.md`** (or equivalent) — AI operating rules: examination/feedback, portable skills, **prioritization** ladder, **deliverables** types, design/success criteria, **output style** (concise, no fluff, leverage-first). |

## Persona document — structure (from capture; verify against file in repo)

Useful for **coach alignment** — how sessions in Cici are steered vs grace-mar **coffee** / **operator-style**:

1. **Examination and feedback** — surface implicit requirements, gaps, conflicts; clarify scope before build.
2. **Portable skills** — e.g. first principles, Occam, Pareto; professionalism, resilience, technical depth, continuous improvement.
3. **Prioritization** — ordered steps: intent → instructions → context → scope → blocking vs optional → assumptions → plan → execute → quality review.
4. **Deliverables** — short audit; prioritized plan; **immediate repo changes** where high-leverage; **handoff** with verification hints.
5. **Output style** — concise, specific, low ceremony; protect operator time; tidy chunks.

*If `CLAUDE.md` changes on `main`, treat this section as a dated snapshot; diff live file.*

## Disambiguation

- **[Cici](https://github.com/Xavier-x01/Cici)** = **canonical OB1 instance repo** for grace-mar journal + digest ([work-xavier-history](../work-xavier-history.md) § 2026-04-10).  
- **Public profile “Popular repositories”** may not list every repo; do not infer absence of **Cici** from an older profile-only ingest ([github-profile-ingest-2026-04-08.md](github-profile-ingest-2026-04-08.md)).

## Next (operator)

- Optional: add **Cici** to a refreshed **GitHub profile** capture when Overview/pinned set changes.  
- **[UPLOAD-PREP.md](../UPLOAD-PREP.md)** — when copying **skill-xavier** into Cici for Xavier-only journal rhythm.
