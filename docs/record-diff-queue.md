# Record Diff Queue

## Purpose

The Record Diff Queue provides a **unified review surface** for every pending governed-state change across the companion-self system. Instead of viewing candidates through separate tools (recursion-gate YAML, identity-diff JSON, change proposals), this queue normalizes them into standardized **diff cards** that present the same structure regardless of origin.

## What it shows

Each diff card contains:

| Field | Source | Required |
|-------|--------|----------|
| **Scope** | `category` + `userSlug` | Yes |
| **Prior State** | `before` object | Yes |
| **Proposed State** | `after` object | Yes |
| **Change Summary** | `changeSummary` | Yes |
| **Why It Matters** | `whyItMatters` | No |
| **Evidence** | `evidenceRefs` | Yes (≥1) |
| **Confidence Delta** | `confidenceDelta.before` / `.after` | No |
| **Conflict Note** | `conflictNote` | No |
| **Recommended Action** | `recommendedAction` enum | No |

Cards are sorted by **confidence delta magnitude** (largest change first), then alphabetically by `diffId`.

## Data model

All diff cards conform to `schema-registry/identity-diff.v1.json` (v1.0.0). Two optional fields extend the base schema:

- **`recommendedAction`** — one of `accept`, `reject`, `defer`, `merge_partially`. Advisory only; companion approval is still required.
- **`whyItMatters`** — prose explanation of the change's significance relative to the Record.

These are non-breaking additions; existing diffs without them remain valid.

## What it does NOT do

- **Merge.** The queue is read-only. It does not modify `self.md`, `self-archive.md`, `bot/prompt.py`, or any Record artifact.
- **Replace the gate.** `recursion-gate.md` remains the canonical staging surface. The diff queue reads from it (via adapter); it does not supplant or duplicate it.
- **Auto-approve.** `recommendedAction` is advisory. Companion approval through the gated pipeline is still required for any merge.
- **Filter by policy.** The queue shows all pending diffs. Filtering and prioritization are companion/operator decisions, not queue logic.

## How it relates to the canonical gate

```
recursion-gate.md  ──adapter──▶  identity-diff JSON  ──renderer──▶  diff cards
```

- **`scripts/gate_to_diff_adapter.py`** (instance-specific) converts `recursion-gate.md` YAML blocks into identity-diff v1 JSON objects.
- **`scripts/render_record_diff_queue.py`** (template-portable) reads identity-diff JSON files from any source and renders the unified Markdown queue.
- The adapter infers `before` from the current SELF where possible and maps gate fields (`summary` → `changeSummary`, `conflicts_detected` → `conflictNote`).

## CLI usage

```bash
# Render from a directory of identity-diff JSON files
python3 scripts/render_record_diff_queue.py users/demo/review-queue/diffs/

# Render from specific files
python3 scripts/render_record_diff_queue.py diff-a.json diff-b.json

# Write output to file
python3 scripts/render_record_diff_queue.py --output queue.md users/demo/review-queue/diffs/

# Output as JSON array (for programmatic consumption)
python3 scripts/render_record_diff_queue.py --json users/demo/review-queue/diffs/

# Instance-specific: render from recursion-gate (grace-mar)
python3 scripts/render_record_diff_queue.py --from-gate -u grace-mar
```

## Web UI

Grace-Mar's `apps/gate-review-app.py` exposes a `/diff-queue` endpoint that renders the queue as HTML, pulling from `recursion-gate.md` via the adapter. This is the browser-facing equivalent of the CLI `--from-gate` mode.

## Template portability

The renderer (`scripts/render_record_diff_queue.py`), the schema extension, demo data, and this spec are template-portable — they belong in both `companion-self` and instance repos. The gate adapter and Flask wiring are instance-specific.
