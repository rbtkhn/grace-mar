---
date: 2026-04-30
work_lane: work-dev
title: Autoresearch dry run narrowed derived regeneration
source_pr:
source_commit:
affected_files:
  - docs/skill-work/work-dev/autoresearch-runs/2026-04-30-derived-regeneration-shallow.md
  - docs/skill-work/work-dev/derived-regeneration.md
problem_type: research-scaffold-falsification
reusable_pattern: Use a WORK-only Autoresearch dry run to convert a broad systems question into one source-backed next wedge without claiming implementation.
self_catching_test: only-if-invoked-manually
gate_candidate: false
record_status: work-only
---

# Compound Note: Autoresearch dry run narrowed derived regeneration

## Context

The operator selected the Engineer path to convert the first Autoresearch dry run into a compound note. The dry run asked: "Where is derived regeneration still shallow?" It lives at [2026-04-30-derived-regeneration-shallow.md](../autoresearch-runs/2026-04-30-derived-regeneration-shallow.md).

## What happened

The Autoresearch packet was tested against a live work-dev question without installing upstream skills or running regeneration commands. The dry run inspected the existing derived-regeneration contract and workspace state, then produced a documented-only finding: the shallow edge is target coverage and incremental confidence, not missing scripts.

## Reusable lesson

An Autoresearch run is useful when it reduces a broad architectural concern into a falsifiable next wedge. For work-dev, the pattern is:

- name the baseline,
- cite the source files,
- distinguish documented-only from implemented,
- produce one next wedge with a dry-run check,
- keep the result WORK-only unless a separate gate path is explicitly chosen.

This keeps research scaffolding from becoming yet another aspirational architecture note.

## Failure pattern

The risk was status inflation: because the repo already has regeneration scripts, a research note could too easily imply the rebuild layer is mature. The dry run caught the sharper distinction: scripts exist, but coverage and incremental behavior still need target-by-target proof.

## Self-catching test

Would the current Grace-Mar system catch this issue next time?

- only-if-invoked-manually

The packet now has templates and checklist prompts, but nothing automatically forces an Autoresearch run before derived-regeneration claims are expanded.

## Candidate follow-up

Pick one additional derived artifact with an obvious source -> output mapping. Register it, confirm the change detector lists its inputs, and run the changed incremental dry-run path before treating the target as live.

## Gate recommendation

No gate action. This remains a work-only implementation lesson.
