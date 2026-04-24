# Cici — architect / end-user prompts session (RTF ingest)

**Captured in grace-mar:** [cici-rtf-architect-enduser-prompts-2026-04-24.rtf](cici-rtf-architect-enduser-prompts-2026-04-24.rtf) (export title: *Prompt for senior software architect to help the system* — includes follow-on lines describing repo exploration and committing **two** production markdown prompts).

**Canonical source of truth (Cici repo, `main`):** the same material ships as first-class docs (merged on GitHub, not only this export):

| Artifact | URL on `main` |
|----------|----------------|
| Senior architect (system) prompt | [docs/prompts/architect-system-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/prompts/architect-system-prompt.md) |
| End-user (system users) prompt | [docs/prompts/end-user-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/prompts/end-user-prompt.md) |
| Session bootstrap (context pack) | [docs/session-bootstrap-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/session-bootstrap-prompt.md) (see PR [#7](https://github.com/Xavier-x01/Cici/pull/7)) |

**PR alignment:** [PR #6](https://github.com/Xavier-x01/Cici/pull/6) (*docs: add senior architect and end-user system prompts*).

## Notes (from RTF text)

- Session narrative: explore **repo structure first**, then write **grounded** prompts; payload themes include full stack (Supabase, pgvector, MCP, Edge Functions, OpenRouter), **governed-state** three-layer model and conflict rule (governed wins over raw Supabase), seven governed surfaces, proposal → approval → promote workflow, evidence tiers **A / B / C**, BrewMind vs Cici operational framing, and behavioral rules (e.g. PLAN-first, one challenge per decision, no retrieval-as-truth, proposal echo before governed changes).

**Repo check:** `docs/prompts/` listing verified via GitHub API on ingest date; tip [work-cici-history.md](../work-cici-history.md) for current `main` SHA.
