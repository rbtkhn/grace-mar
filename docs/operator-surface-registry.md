# Operator surface registry

## 1. Purpose

Grace-Mar uses many **generated and semi-generated** operator-facing outputs under `artifacts/`, in `docs/workflows/`, and alongside scripts: dashboards, indexes, reports, receipts, packets, sidecars, and machine feeds. They make review, lane work, and governance **easier to inspect** without opening every source file.

This document is a **taxonomy and registry**: it classifies those **operator surfaces** and states their **authority status**. It is **governance and navigation**—not a new capability, not a dashboard, and not a second truth for the Record or the gate.

**Single source of truth for build lines:** Producer commands and policy per path remain in [artifacts/README.md](../artifacts/README.md) (Path / Produced by / Policy table) and, for covered targets, per-artifact `*.derived-rationale.json` sidecars next to generated files. This registry **does not** replace that inventory; it **classifies and links** it.

## 2. Surface classes

### Dashboard

A compact operator-facing view meant for **repeated** use. Summarizes state, links, queues, or work status. **Derived, non-canonical.**

### Index

A **navigational** or **catalog** view: locate records, artifacts, files, or other surfaces.

### Report

A generated or semi-generated **analysis** output: run summary, posture, uncertainty, classification, or strategy result.

### Receipt

A run-level or operation-level **audit** artifact: what happened, what boundary applied, optional load-lift or execution metadata.

### Packet

A **bounded** bundle intended to support **human judgment** (e.g. review packet).

### Sidecar

A **companion** file to another artifact (often machine-readable provenance; e.g. `*.derived-rationale.json`).

### Machine feed

JSON or structured output **primarily** for scripts, tools, or downstream views—not a narrative operator page by itself.

### Lane-local surface

A surface **scoped to one** work lane or territory (e.g. work-dev, work-strategy) rather than a single global “home.”

## 3. Authority status

| Status | Meaning |
|--------|--------|
| `canonical` | Durable source of truth (rare for `artifacts/`; use only when doctrine explicitly names a path as canonical). |
| `derived_non_authoritative` | Regenerated from sources; **not** Record; does not override `users/<id>/self.md` or gate. |
| `advisory` | Guidance, partner-facing summary, or posture text—**not** merge authority. |
| `review_support` | Supports review (e.g. gate snapshots); **not** a substitute for `recursion-gate.md`. |
| `machine_feed` | Structured feed for tooling; same non-authority as other derived outputs unless stated otherwise. |
| `deprecated` | Superseded or kept only for migration; do not treat as current without checking `notes` / `supersedes`. |
| `unknown_needs_classification` | Reserved for **rare** use when ownership or producer is unclear after inspection. |

**Default for most `artifacts/`:** `derived_non_authoritative`, `advisory`, `review_support`, or `machine_feed`—**not** canonical.

## 4. Registry fields

When recording a surface in the table below (or in a future JSON instance validated by [operator-surface.v1.json](../schema-registry/operator-surface.v1.json)):

| Field | Role |
|-------|------|
| `surface_id` | Stable id (e.g. `library-index`, `work-lanes-json`). |
| `path` | Repo-relative path. |
| `class` | One of the surface classes in §2. |
| `owner_lane` | Primary work lane or `multi` / `operator` / `docs` as appropriate. |
| `producer` | Script or doc author; for details see [artifacts README](../artifacts/README.md). |
| `source_inputs` | What it reads (paths, inboxes, runtime files). |
| `authority_status` | One of §3. |
| `canonical_surfaces_touched` | `false` for almost all operator surfaces: does not modify Record by itself. |
| `rebuild_command` | **Prefer:** sidecar or [artifacts README](../artifacts/README.md); or `regenerate_all_derived.py` where applicable. |
| `staleness_check` | How to know it is stale; see [operator-surface-staleness.md](operator-surface-staleness.md) (§3–§4). |
| `operator_use` | What decision or inspection this supports. |
| `related_surfaces` | Sibling paths, feed + dashboard pairs, or docs. |
| `supersedes` | If this surface replaced another id. |
| `notes` | Drift, CI, or lane caveats. |
| `staleness_level` (optional) | One of: `current_declared`, `current_unknown`, `stale_possible`, `stale_likely`, `historical_only` — see [operator-surface-staleness.md](operator-surface-staleness.md) §4. For JSON instances, see [operator-surface.v1.json](../schema-registry/operator-surface.v1.json). |
| `last_generated` (optional) | ISO-8601-ish string when the surface or an operator last knew generation time (machine or human). |
| `freshness_notes` (optional) | Free text: cadence, CI, or “verify after X”. |

### Staleness expectations

Every registered surface should **eventually** declare **freshness expectations** (or point here). **Optional** metadata `staleness_level`, `last_generated`, and `freshness_notes` may be added to JSON registry entries (schema) or to this doc over time; **this PR does not require** every row in the §5 table to list them.

**Convention:** [operator-surface-staleness.md](operator-surface-staleness.md) defines levels, a standard **staleness note** blockquote, and the rule that **staleness does not change authority**.

**Typical default by class (heuristic, not a rule):**

| Class | Typical default | When it goes stale |
|-------|-----------------|---------------------|
| dashboard, index | `stale_possible` | After listed **source inputs** change without regen |
| report | `stale_possible` or `historical_only` | After new runs or new source data; old run = historical |
| receipt | `historical_only` | Receipts are run records; not “refreshed” in place |
| packet | `stale_possible` | If bound item or evidence changed |
| sidecar | follows paired artifact | Regenerate when parent artifact regen required |
| machine feed | `stale_possible` | When upstream JSON/inputs change |
| lane_local_surface | `stale_possible` | Lane inputs or regen script path change |

**Honesty:** If rebuild command or last run time is **unknown**, use `current_unknown` or leave freshness fields empty until known—**do not** guess timestamps.

**Path note:** `artifacts/strategy-run-report.md` is **registered** when the script is used to generate it; the file may be **absent** until a run—do not add an empty file just to “have” a surface.

## 5. Registered surfaces (major)

Authoritative **producer and policy** rows: [artifacts/README.md](../artifacts/README.md). **Rebuild lines** for covered paths: `*.derived-rationale.json` next to the artifact, or [derived regeneration](skill-work/work-dev/derived-regeneration.md).

| Surface | Class | Owner lane | Authority status | Source inputs (summary) | Rebuild / producer ref | Operator use | Related surfaces |
|--------|-------|------------|------------------|---------------------------|-------------------------|--------------|------------------|
| `artifacts/library-index.md` | dashboard | work-strategy / library | derived_non_authoritative | `users/<id>/self-library.md` `entries` YAML | [artifacts README — row](../artifacts/README.md) + `build_library_index.py` | At-a-glance library + lane appendix | [operator-dashboards](operator-dashboards.md), sidecar if present |
| `artifacts/lane-dashboards/README.md` | dashboard | multi / operator | derived_non_authoritative | Lane configs, `work-lanes-dashboard.json` when used | [artifacts README](../artifacts/README.md), `build_lane_dashboards.py` | Lane health / runtime snapshot | `work-lanes-dashboard.json` |
| `artifacts/review-dashboard.md` | dashboard | review / gate | review_support | Fenced `CANDIDATE-*` in `recursion-gate.md` (parse) | `build_review_dashboard.py` | Pending / processed gate overview | [users/…/recursion-gate.md](../users/grace-mar/recursion-gate.md) (authoritative) |
| `artifacts/gate-board.md` | dashboard | review / gate | review_support | Same gate file | `build_gate_board.py` | Kanban-style candidate view | `review-dashboard`, gate file |
| `artifacts/governance-posture.md` | report | operator / safety | advisory | Config + policy inputs per script | `report_governance_posture.py` | Triad, gate, audit one-pager | [safety-story-ux](skill-work/work-dev/safety-story-ux.md) |
| `artifacts/work-lanes-dashboard.json` | machine_feed | work / multi | machine_feed | WORK telemetry / observations | `build_work_lanes_dashboard.py` | Input to lane dashboard script | `lane-dashboards/README.md` |
| `artifacts/work_dev_dashboard.md` | dashboard | work-dev | derived_non_authoritative | work-dev status inputs | `scripts/work_dev/build_dashboard.py` (see [compound loop](skill-work/work-dev/compound-loop.md)) | work-dev at-a-glance | `work_dev_dashboard.json` |
| `artifacts/work_dev_dashboard.json` | machine_feed | work-dev | machine_feed | work-dev status sources | `build_dashboard.py` (same as `.md`) | Programmatic same slice | `work_dev_dashboard.md` |
| `artifacts/work-dev-compound-dashboard.md` | lane_local_surface | work-dev | derived_non_authoritative | Compound notes, refresh/export | `build_work_dev_compound_dashboard.py` | Single-page compound layer [compound-dashboard](skill-work/work-dev/compound-dashboard.md) | `work-dev-compound-refresh.md`, gate-candidates export |
| `artifacts/strategy-run-report.md` | report | work-strategy | derived_non_authoritative | `artifacts/strategy-runs/`, `run-receipts/` | `build_strategy_run_report.py` | Recent run table | [STRATEGY-RUN-ARCHITECTURE](skill-work/work-strategy/STRATEGY-RUN-ARCHITECTURE.md) |
| `artifacts/review-packets/` | packet | review / runtime | review_support | Task-anchored orchestration | `review_orchestrator.py` (optional) | Human judgment bundles | [folder README](../artifacts/review-packets/README.md) |
| `artifacts/classification-reports/` | report | runtime / review | advisory | Surfaces for misclassification | `surface_misclassification_detector.py` | Risk flags | [doc](orchestration/surface-misclassification-detector.md) |
| `artifacts/route-recommendations/` | receipt | operator / multi | advisory | Inline task description + [`config/route_recommendation.json`](../config/route_recommendation.json) | [`recommend_route.py`](../scripts/recommend_route.py) | Cold-thread lane sniff; not gate authority | [`docs/route-recommendation.md`](route-recommendation.md), [bucket README](../artifacts/route-recommendations/README.md) |
| `artifacts/shadow-merges/` | report | review / sim | advisory | Simulated merge inputs | `shadow_merge_simulator.py` | Pre-merge preview | [orchestration doc](orchestration/shadow-merge-simulator.md) |
| `artifacts/workflow-observability/` | report | runtime / work | machine_feed (reports) + advisory | workflow events / aggregates | per [workflow-observability.md](workflow-observability.md) (regen via scripts) | Health / threshold view | [workflow-observability](workflow-observability.md) |
| `artifacts/workflow-depth/` | machine_feed + index | prepared_context / work | machine_feed | depth receipts / JSONL | [runtime doc](../runtime/workflow-depth/README.md) | depth tier audit | [workflow-depth-contract](runtime/workflow-depth-contract.md) |
| `artifacts/forecast/` | report + machine_feed | work-forecast (when used) | derived_non_authoritative | baselines / operator messages | `run_forecast_baselines.py` | Forecast artifacts | [forecast policy](../artifacts/forecast/README.md) |
| `artifacts/uncertainty-reports/` | report + sidecar | work-strategy / runtime | advisory | uncertainty envelope JSON (optional) | operator / CI optional | Envelope legibility | [folder README](../artifacts/uncertainty-reports/README.md) |
| `docs/workflows/known-path-workflows/` | index + registry (docs) | `multi` (workflows) | derived_non_authoritative (docs) | n/a (documentation SSOT) | human edits + PR | Known-path **eligibility** and templates | this file §8, [README](workflows/known-path-workflows/README.md) |
| `docs/workflows/known-path-workflows/load-lift-receipts.md` | report (doctrine) + receipt spec | `multi` | derived_non_authoritative | n/a | human | Load-lift evaluation spec | [schema](../schema-registry/load-lift-receipt.v1.json), [examples](workflows/known-path-workflows/examples/) |

Rows **omit** one-off or rarely used paths; add them via PR when a surface becomes part of the default operator path. **Not listed as separate rows:** `work-dev/rebuild-receipts/`, `derived-regeneration-manifest.json`—covered by [derived regeneration](skill-work/work-dev/derived-regeneration.md) and [artifacts README](../artifacts/README.md).

**`unknown_needs_classification`:** none for the table above at registration time; use sparingly (1–3 items repo-wide) only when a path’s producer is genuinely unclear.

## 6. Dashboard anti-sprawl policy

**No new dashboard** (or dashboard-shaped Markdown under `artifacts/` with the same role) may be added unless it satisfies **at least one** of:

1. It **consolidates or replaces** an existing operator dashboard.
2. It is a **new section** of an existing dashboard (same file or clearly linked file family).
3. It is **explicitly lane-local** and named as such in path or title (e.g. under `artifacts/work-dev/` for work-dev only).
4. It is **registered** in this document with **owner lane**, **source inputs**, **rebuild or producer ref**, **authority status**, and **relationship** to existing surfaces in §5 (and a row in [artifacts README](../artifacts/README.md) when the artifact is build-generated).

**Additional rules for any new dashboard-like surface**

- State **which operator decision** it supports (review, triage, navigation, not “truth”).
- State **which surface it does not replace** (e.g. not `recursion-gate.md`, not SELF).
- Declare **human-facing**, **machine-facing**, or **both** (e.g. JSON + `.md` pair is common).
- Declare **staleness** or regen expectation (CI, manual command, or “after X edits”).
- **Do not** imply **merge** authority for the gate or Record.
- **Do not** become a second source of truth for gate contents or `users/<id>/` canonical files.

## 7. Preferred alternatives to new dashboards

Before adding a new dashboard, prefer in order when possible:

- A **row or section** on an existing dashboard (e.g. library, lane, review, gate, work_dev compound).
- A new **receipt** type (load-lift, execution, run) with existing receipt doctrine.
- A **report** or one-off Markdown under an existing **lane** `artifacts/` subtree with clear doc link.
- A **packet** (review) or **sidecar** (provenance).
- A **machine feed** (JSON) without a new narrative dashboard—consume from scripts or a single existing view.
- Improving **this registry** or **links** from an existing surface.
- Improving the **known-path** workflow doc or a **load-lift** example (see [load-lift-receipts](workflows/known-path-workflows/load-lift-receipts.md)).

## 8. Known-path workflow placement

[Known-path workflows](workflows/known-path-workflows/README.md) describe **repeatable** processes with explicit authority class; they **do not** automatically get a new standalone operator dashboard. Visibility should be:

- A **row or pointer** in this registry (if operator-facing);
- A **load-lift** or other **receipt** after a run;
- A **section** of an existing lane or operator surface; or
- A **review packet** or **report**.

Add a **dedicated Known-path workflow dashboard** only if **this registry** plus existing surfaces **and** load-lift/review flows prove insufficient—then register it under §5–6 like any other dashboard.

## 9. Related docs

- [Operator surface staleness](operator-surface-staleness.md) — levels, note format, anti-authority rule.
- [Operator dashboards (derived Markdown)](operator-dashboards.md) — regeneration order, CI, design notes.
- [Artifacts (derived) README](../artifacts/README.md) — Path → producer → policy table.
- [Runtime vs Record](runtime-vs-record.md) — non-canonical boundary.
- [Authority map](authority-map.md) — normative **policy language**; this registry does not extend write classes.

---

**Operator surfaces** is the **umbrella** term. Not every file under `artifacts/` is a “dashboard”; use the class names in §2.
