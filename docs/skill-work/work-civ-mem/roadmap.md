# work-civ-mem — Roadmap

**Status:** New territory. Current goal: establish a clean Grace-Mar stewardship surface for the `civilization_memory` repository without importing CMC runtime operations into Grace-Mar.

---

## Phase 0 — Current state

**Scope:** Manual and repo-level. `civilization_memory` exists as an external repository; Grace-Mar can reference it, route to it in limited ways, and manage related work through docs and operator judgment.

| Deliverable | Status | Description |
|-------------|--------|-------------|
| **Territory definition** | This phase | Define purpose, boundaries, and principles for `work-civ-mem`. |
| **Repo awareness** | Exists | Grace-Mar already knows the repo and references CMC in docs such as `cmc-routing.md`. |
| **Bounded scope** | This phase | Keep the territory focused on stewardship, not live CMC operations. |
| **Workspace runbook** | Added | `workspace.md` provides the first lightweight operator surface for repo-management loops. |
| **Initial audit snapshot** | Added | `audit-report.md` establishes the first baseline view of repo strengths, likely risks, and next stewardship steps. |

---

## Phase 1 — Read and audit

**Scope:** Read-only repository stewardship.

| Deliverable | Description |
|-------------|-------------|
| **Repo audit surface** | Review README, governance docs, mode contracts, tooling, and validation paths. |
| **Drift detection** | Identify stale docs, inconsistent workflow descriptions, dead scripts, or management gaps. |
| **Maintenance backlog** | Collect concrete repo-management tasks for future execution. |
| **Workspace refinement** | Expand `workspace.md` as recurring management rituals, commands, or checkpoints stabilize. |
| **Audit refinement** | Turn the baseline `audit-report.md` into a recurring, more systematic management report as stewardship deepens. |

**Output:** Reports, notes, and prioritized management backlog. No upstream writes required.

---

## Phase 2 — Suggest and prepare

**Scope:** Bounded proposal generation for `civilization_memory`.

| Deliverable | Description |
|-------------|-------------|
| **Contribution candidates** | Prepare doc fixes, governance clarifications, validation improvements, or workflow cleanups. |
| **Patch framing** | Describe why a change is useful, where it belongs, and what boundary it respects. |
| **Operator workflow notes** | Add `workspace.md` if recurring commands, repo rituals, or review sequences need a persistent surface. |

**Output:** Ready-to-review suggestions and scoped patch ideas. Human still decides what goes upstream.

---

## Phase 3 — Stage bounded contributions

**Scope:** Prepare contribution artifacts within approved boundaries.

| Deliverable | Description |
|-------------|-------------|
| **Patch preparation** | Produce diffs, PR drafts, or structured edit plans for `civilization_memory`. |
| **Validation loop** | Ensure proposed changes preserve CMC governance and pass local validation. |
| **Contribution log** | Track what was proposed, approved, applied, or deferred. |

**Output:** Ready-to-submit repository changes, still human-gated.

---

## Phase 4 — Bounded autonomous maintenance

**Scope:** Future, only within explicit approval boundaries.

| Deliverable | Description |
|-------------|-------------|
| **Approved maintenance scope** | Human defines which surfaces may be maintained semi-autonomously. |
| **Routine hygiene** | Periodic drift scans, validation runs, stale-doc detection, and contribution prep. |
| **Escalation path** | Governance-sensitive changes always return to human review. |

**Constraint:** No autonomous change to CMC governance or doctrine without explicit approval.

---

## Adjacent Companion Self Product Priorities

These are intentionally recorded here as **adjacent leverage items**, not as first-pass implementation commitments for `work-civ-mem`.

1. **Approval inbox**  
   Improve `RECURSION-GATE` review ergonomics with batching, dedupe, and risk-tiered review.

2. **Provenance surfaces**  
   Make source and approval status more legible across profile, miniapp, and export surfaces.

3. **Portability bundle**  
   Strengthen the canonical export package with clearer approved/staged/absent distinctions and provenance manifesting.

These matter strategically because better governance, clearer provenance, and stronger portability improve Grace-Mar's value as identity infrastructure, but they are not part of this territory's initial repository-management scope.

---

## First-Pass Success Criteria

- `work-civ-mem` exists as a clearly bounded territory.
- The README makes repo stewardship the primary scope.
- This roadmap separates present scope from future phases.
- Adjacent product priorities are recorded without being mistaken for immediate work.
- The territory now has baseline `workspace.md` and `audit-report.md` surfaces ready for refinement as recurring management work grows.
