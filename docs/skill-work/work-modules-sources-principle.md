# Work modules — authorized sources lists

**Design principle:** Each **work** territory (`work-*`) should carry a single hand-maintained file naming **authorized sources** — channels, podcasts, newsletters, or principal social accounts that **orient** operator work in that lane (framing, cadence, provenance).

| Convention | Meaning |
|--------------|---------|
| **Filename** | `<territory-id>-sources.md` (e.g. `work-dev-sources.md`, `work-jiang-sources.md`, `work-politics-sources.md`) |
| **Location** | `docs/skill-work/<territory>/` alongside that territory’s README and workspace |
| **Content** | Short table: source name, URL, optional notes. Add rows manually. |
| **Not** | Record truth, Voice knowledge, or automatic ingest config. RSS / daily-brief feeds and **brief-source-registry**-style intake live elsewhere. |

**Fence:** These lists document **where ideas and vocabulary often come from**, not what is true. Integration facts stay in [work-dev/integration-status.md](work-dev/integration-status.md). Work-politics ship copy stays **cited** and grounded in [principal-profile.md](work-politics/principal-profile.md) and territory briefs — not in the sources list alone.

**Existing lists:**

| Territory | File |
|-----------|------|
| work-dev | [work-dev/work-dev-sources.md](work-dev/work-dev-sources.md) |
| work-jiang | [work-jiang/work-jiang-sources.md](work-jiang/work-jiang-sources.md) |
| work-politics | [work-politics/work-politics-sources.md](work-politics/work-politics-sources.md) |
| work-strategy | [work-strategy/work-strategy-sources.md](work-strategy/work-strategy-sources.md) |

Other `work-*` territories should add a `*-sources.md` when the operator wants explicit provenance for external discourse.

**Renote:** `discourse-sources.md` in work-dev was renamed to **`work-dev-sources.md`** to match this convention; old links may use a stub redirect file.

**See also:** [work-modules-history-principle.md](work-modules-history-principle.md) — append-only **`work-*-history.md`** logs per territory (distinct from this sources list). **New lane:** [work-template.md](work-template.md).
