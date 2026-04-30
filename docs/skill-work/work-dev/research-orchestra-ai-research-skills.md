# Orchestra Research AI Research Skills

**Status:** WORK-layer external reference. **Not** Record truth. **Not** imported skill authority.

**Source check:** As checked on 2026-04-30, the public GitHub README for [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs) describes **98 skills across 23 categories** and positions the library as an end-to-end AI research skills library from idea to paper. The npm package is [`@orchestra-research/ai-research-skills`](https://www.npmjs.com/package/@orchestra-research/ai-research-skills). Do not treat these counts as stable without rechecking the upstream README.

## Why It Matters

This library is unusually strong WORK-layer material because it covers a full research lifecycle rather than a narrow productivity surface:

1. idea generation and research ideation,
2. orchestration through Autoresearch,
3. experiment and engineering execution across model, data, training, inference, evaluation, safety, RAG, agents, and multimodal domains,
4. paper writing, plotting, and presentation.

The central pattern worth borrowing is not "install everything." It is **research as a staged lifecycle**: ask a better question, route to the right tools, produce inspectable artifacts, and keep evidence separate from identity.

For Grace-Mar, the stakes are project judgment: Autoresearch should make work-dev questions sharper, proofs more visible, and next wedges easier to choose, while leaving meaning, identity, and durable truth outside the automation.

## Grace-Mar Mapping

| Grace-Mar layer | Fit | Guidance |
|-----------------|-----|----------|
| **WORK** | Strong fit. Autoresearch and domain skills can help plan, execute, draft, and evaluate research projects. | Use selected categories as project templates or agent prompts. Keep outputs in `docs/skill-work/` unless separately staged. |
| **SKILLS / Record-bound capability** | Possible only after real use produces personal capability evidence. | Gate only companion-specific learnings, proof traces, or reflected capability claims. Do not import upstream skill text into SELF. |
| **Voice** | Possible as a rendering layer after the Record supports it. | Voice may surface options in the companion's style, but should not pretend the companion has mastered a skill because the repo exists. |
| **SELF-LIBRARY** | Possible governed reference if the companion approves it later. | Treat the repo like a reference collection, not identity. Preserve dated use traces and provenance if it enters the library. |

## Best Borrowable Ideas

| Idea | Grace-Mar use |
|------|---------------|
| **Autoresearch orchestration** | A WORK conductor for research projects: survey, route, execute, synthesize, and draft. |
| **Two-loop research architecture** | Inner loop for experiment/tool optimization; outer loop for synthesis, judgment, and paper-level coherence. |
| **Ideation pair** | Better research-question generation before implementation begins. |
| **Paper-writing skills** | Structured academic outputs with citations, LaTeX discipline, and conference-talk shaping. |
| **Academic plotting** | Evidence-friendly figures for reports, demos, and publication-style artifacts. |
| **Evaluation and safety skills** | Stronger proof discipline before status upgrades. |
| **Domain bundles** | Choose one domain per project, such as RAG, mech interp, post-training, or agents. |
| **Progressive disclosure structure** | Short `SKILL.md` entrypoints with deeper references behind them. |
| **Official-source grounding** | Prefer official docs, real issues, release notes, and troubleshooting trails over vague summaries. |
| **Install/update ergonomics** | Useful model for future Grace-Mar portable skill distribution, even if Grace-Mar does not install this bundle wholesale. |

## Starter Bundle

For Grace-Mar, start small:

1. **Autoresearch** as WORK orchestration.
2. **Research ideation** for question generation and creative framing.
3. **ML paper writing + academic plotting** for structured outputs.
4. **Evaluation / safety** for proof and failure discipline.
5. **One domain bundle per project** based on the actual question.

Avoid installing or importing every category by default. The safer pattern is a selected bundle tied to a concrete research question and an explicit proof artifact.

## Autoresearch Adapter

**V1 purpose:** better work-dev research project execution. This adapter is operator-facing WORK scaffolding. It does not create a Voice behavior, install upstream skills, run `npx`, clone external repositories, or write to Record surfaces.

Publicly legible version: this is a safe research scaffold, not an autonomous research-agent claim. It helps an operator turn a question into sources, a dated research note, and possibly a gate candidate draft; it does not decide what Grace-Mar knows, what the companion has learned, or what enters the Record.

Use the packet templates:

| Template | Use |
|----------|-----|
| [autoresearch-wrapper.md](templates/autoresearch-wrapper.md) | Frame the research question, hypothesis, success metric, milestones, and stop conditions. |
| [autoresearch-run-note.md](templates/autoresearch-run-note.md) | Produce the default dated WORK artifact for a run. |
| [autoresearch-gate-candidate-example.md](templates/autoresearch-gate-candidate-example.md) | Shape a full paste-ready candidate only when sources plus log justify review. |
| [autoresearch-operator-checklist.md](templates/autoresearch-operator-checklist.md) | Pre-run and post-run guardrails. |

The detailed lifecycle lives in the templates: bootstrap, optimization vs discovery mode, experiment protocol, result labels, stuck behavior, and direction decisions. This note stays the conceptual index.

### Two-Loop Mapping

| Orchestra pattern | Grace-Mar adapter |
|-------------------|-------------------|
| **Inner loop** | Bounded WORK exploration: inspect sources, run small analyses, draft one artifact, and record logs. |
| **Outer loop** | Milestone checkpoints: question framed, sources gathered, first synthesis, candidate decision. |
| **Research output** | Dated WORK research note by default. Gate candidate only when warranted. |
| **Research memory** | WORK notes and logs only; no automatic SELF, SKILLS, EVIDENCE, SELF-LIBRARY, or Voice update. |

Invocation shape:

```text
use-autoresearch <hypothesis> <success-metric> <time-budget>
```

The time budget is a ceiling, not permission to run without review. V1 pauses at milestones rather than assuming continuous autonomy.

### Candidate Rule

A full candidate may be prepared only when the run has:

1. cited sources,
2. a dated WORK log or run artifact,
3. a clear target surface such as IX-B curiosity, SKILLS evidence, or SELF-LIBRARY reference,
4. an explicit distinction between draft, documented-only, and implemented status.

Rejected or inconclusive runs remain WORK-only unless the human separately chooses to stage an EVIDENCE candidate. The gate example is a drafting aid, not approval.

### Falsification Checks

The adapter should stay small enough to justify itself. Treat it as too heavy, too vague, or redundant if any of these become true:

- **Too heavy:** a simple work-dev question needs more template-filling than evidence gathering.
- **Too vague:** a run note cannot name sources, a proxy metric, a baseline, and a next wedge.
- **Too redundant:** the output is no better than a normal [Compound Work Loop](compound-loop.md) note.
- **Too authority-blurry:** the run starts implying Voice, Record, or companion learning without a gate path.
- **Too speculative:** a candidate draft appears without cited sources plus a dated WORK log.

First dry-run example: [2026-04-30-derived-regeneration-shallow.md](autoresearch-runs/2026-04-30-derived-regeneration-shallow.md).

## Tracer-Bullet Integration Example

Use [Ubiquitous Language + Tracer-Bullet Plans](ubiquitous-language-and-tracer-bullets.md) before any real integration.

| Part | Choice |
|------|--------|
| **Input** | One research question or project idea from a WORK lane. |
| **Path touched** | Autoresearch-style outline -> selected domain skill -> one draft artifact under `docs/skill-work/`. |
| **Output** | A WORK note, experiment plan, literature synthesis, plot, or paper-outline draft. |
| **Proof** | Cited sources, runnable commands if code is involved, and an explicit implemented / documented-only / draft status line. |
| **Stop criteria** | Stop if the plan cannot cite sources, identify a domain bundle, or distinguish draft from implemented capability. |
| **Expansion path** | Only after one artifact is inspected should the operator choose a second domain skill or broader research loop. |

Forbidden claims:

- Do not claim Grace-Mar has an autonomous research agent because this repo exists.
- Do not claim a companion has acquired a capability without evidence and gate review.
- Do not treat upstream skills as Record content.
- Do not install or run package commands as part of documentation-only analysis.

## Integration Guardrail

This repo can deepen Grace-Mar's research scaffolding, especially for reflective, long-horizon, or academic-style projects. Its role is instrumental: it can help WORK produce better candidates, drafts, and proofs. The companion gate remains the only route by which any personal learning, capability evidence, or SELF-LIBRARY reference becomes durable Record material.
