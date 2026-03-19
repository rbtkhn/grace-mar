# Contradiction Timeline

**Purpose:** A **time-ordered view** of how the Record evolved: when a belief, preference, skill claim, or library fact **changed**, what **evidence** (ACT-*, READ-*, gate candidate) **triggered** the change, and whether a **contradiction** was **resolved**, **deferred** (e.g. rejected candidate), or **still open**. Aligns with **git history** + **gated pipeline** + [contradiction-resolution.md](contradiction-resolution.md).

**See also:** [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md), [agents.md](../agents.md) (contradiction preservation).

---

## Why it fits Grace-Mar

| Layer | Role in the timeline |
|-------|----------------------|
| **Git** | Immutable ordering of merges into `self.md`, `skills.md`, `self-library.md`, `self-evidence.md` |
| **Pipeline** | `pipeline-events.jsonl` — `staged` → `applied` / `rejected`; schema 2 adds **ix_entry_id** (LEARN/CUR/PER), **surface**, **summary_snippet**. See [pipeline-events-schema.md](pipeline-events-schema.md). |
| **EVIDENCE** | ACT entries hold **mind_category**, **summary** — proxy for “what changed” |
| **Contradiction spec** | Resolution types (`growth`, `correction`, `context`, `reject_new`, `exception`) become **timeline states** once encoded on entries |

---

## Event types (target model)

| Timeline row | Meaning |
|--------------|---------|
| **merged_identity** | Gate approved → IX-A/B/C or prompt line; evidence **ACT-*** |
| **merged_library** | LIB or civ-mem perimeter change (future explicit event) |
| **merged_skills** | SKILLS claim upgrade (often same gate or manual) |
| **contradiction_flagged** | Candidate carried `conflicts_detected` (staged, not yet merged) |
| **contradiction_resolved** | Merge chose a resolution type; old entry **superseded** or scoped |
| **contradiction_deferred** | Candidate **rejected** or deferred; tension remains **open** in Record |
| **contradiction_open** | Both poles still in SELF with **tension_with** / no supersession yet |

---

## Resolution state on the timeline

| State | User-visible label | Typical source |
|-------|-------------------|----------------|
| **Resolved** | Merged with `growth` / `correction` / `context` / `exception` | `superseded_by`, `valid_until`, or paired entries with scope |
| **Deferred** | Rejected gate row or “parked” operator note | `rejected` pipeline event; no ACT merge |
| **Open** | Flagged conflict, no merge yet | Pending candidate with conflicts; or both IX lines retained |

---

## Data sources (MVP → full)

1. **`users/[id]/pipeline-events.jsonl`** — authoritative for **when** gate actions happened and **ACT-*** linkage.
2. **`git log`** on Record paths — coarse **file-level** commits when events are missing or for operator edits.
3. **Processed blocks in `recursion-gate.md`** — optional scrape for **summary** + **conflicts** (heavy).
4. **Future:** structured **contradiction objects** + **emit_pipeline_event** fields (`resolution_type`, `supersedes_entry_id`) for a first-class UI.

---

## Operator tooling (MVP)

```bash
python3 scripts/contradiction_timeline_digest.py -u grace-mar
```

Prints a **markdown digest**: applied / rejected pipeline events plus recent **git touches** to `self.md`, `skills.md`, `self-library.md`. Use as input to a dashboard or weekly review.

---

## UI (future)

- Filter by surface: SELF-KNOWLEDGE · SELF-LIBRARY · SKILLS.
- Click row → candidate snippet + ACT summary + link to commit.
- Badge: **resolved** / **deferred** / **open**.

---

## Invariants

- Timeline is **read-mostly**; it does not merge. Truth stays in git + Record files.
- **No fabricated history** — rows must trace to an event or commit.
