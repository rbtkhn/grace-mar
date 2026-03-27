# TEMPLATE-BASELINE — companion-self governance pin

**Purpose:** Pin the **companion-self** commit used as the baseline for grace-mar template sync and SELF-LIBRARY governance alignment.

| Field | Value |
|-------|--------|
| **Baseline date** | 2026-03-27 |
| **Source** | In-repo [users/_template/README.md](../../../users/_template/README.md) + [canonical-paths.md](../../../canonical-paths.md) |
| **companion-self git** | **[`main` @ `3eaf7b1`](https://github.com/rbtkhn/companion-self/commit/3eaf7b17090ae1e8d497856544febf397cb4e98a)** — doctrine sync pass (change-review cluster, `template-version` contract). Prior pin: `288b438` (SELF-LIBRARY template governance). |

**Note:** Land **SELF-LIBRARY** template alignment per [COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md](COMPANION-SELF-SELF-LIBRARY-ALIGNMENT.md). Re-run manifest diff after each material companion-self pull; `main` tip may advance beyond this pin.

**Audit:** [`audit-report-manifest.md`](audit-report-manifest.md) — `python3 scripts/template_diff.py --no-clone --use-manifest -o docs/skill-work/work-companion-self/audit-report-manifest.md`
