# Claude Surface Contract

This document defines the standard **invocation contract** for Grace-Mar’s operator-facing surfaces (commands, workflows, helpers, skills, generated interface artifacts, and review-related docs).

## Why this exists

Grace-Mar is a governance-first system with four canonical Record surfaces and a gated review path. Claude-facing commands, workflows, and helpers should make **mutation scope** and **review boundaries** explicit so operators know what each surface can touch before they run it.

## Standard contract fields

Each surface doc can repeat this short block at the top:

- **Surface type** — `command` | `workflow` | `helper` | `skill` | `interface artifact` | `review surface`
- **Primary purpose** — one-sentence description
- **When to use** — short trigger condition
- **Inputs** — arguments, ids, paths, or lane scope
- **Outputs** — artifact, generated interface surface, report, context file, or gate candidate
- **Mutation scope** — see vocabulary below
- **Canonical Record access** — `none` | `read-only` | `indirect via review flow`
- **Typical next step** — what usually follows
- **Do not use for** — short anti-pattern list

This is intentionally small: legibility, not a heavy metadata schema.

## Mutation scope vocabulary

- **runtime-only** — may read or write runtime artifacts only (including prepared-context scratch paths), not canonical Record files
- **may stage review artifact** — may write a candidate or review object (for example into `recursion-gate.md`), but not update canonical Record by itself
- **canonical Record updates only through approved merge path** — may participate in a governed merge sequence; never direct silent mutation of SELF, SKILLS, EVIDENCE, or prompt outside the pipeline

## Canonical Record reminder

Grace-Mar’s canonical Record surfaces are:

- **SELF**
- **SELF-LIBRARY**
- **SKILLS**
- **EVIDENCE**

Runtime retrieval, prepared context, and observation-led workflows do **not** bypass review. Durable changes flow through the Approval Inbox and companion-approved merge tooling.

## Recommended adoption order

Apply this contract first to:

1. Runtime retrieval docs ([memory-retrieval.md](runtime/memory-retrieval.md))
2. Read-hint and memory-brief docs ([read-hints.md](runtime/read-hints.md))
3. Provenance staging docs ([provenance-staging.md](runtime/provenance-staging.md))
4. Observation expansion / prepared context ([observation-expansion.md](runtime/observation-expansion.md))
5. [start-here.md](start-here.md)
6. Later: selected skill docs, operator workflow docs, top-level runtime helper README pages
