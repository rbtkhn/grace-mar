# Daily brief — Tri-Frame mind overlays (workflow)

**Purpose:** Optional **second stage** after the shared daily brief (`daily-brief-YYYY-MM-DD.md` in [`../`](../README.md)). One canonical brief; **sidecar** files in [`outputs/`](outputs/) hold lens scaffolds or completed analysis — **not** merged into the brief body by default.

**Civ-mem grounding (when the brief touches an entity X in `civilization_memory`):** Before filling mind scaffolds, follow [CIV-MEM-TRI-FRAME-ROUTING.md](CIV-MEM-TRI-FRAME-ROUTING.md): `MEM–RELEVANCE–X` → shared **1–2** primary MEMs → **up to 1–2 additional MEMs per mind** (Barnes / Mearsheimer / Mercouris) from the relevance dimensions that match each lens → `CIV–STATE–X` (and `CIV–SCHOLAR–X` / ARC as needed). Keeps Tri-Frame **evidence-heavy** without three unrelated repo walks.

**Write mode (`daily-brief-minds-config.json`):** **`scaffold`** — the generator script does **not** call an LLM. It writes markdown files with title, paths to the daily brief and trimmed `CIV-MIND-*.md` stubs, a **copy-paste prompt bundle**, and a placeholder body for the operator or a Cursor agent to complete. Full lens prose is produced in-editor or via **`strategy`** / agent session, same as [skill-strategy post-entry lens](../../../../.cursor/skills/skill-strategy/SKILL.md) discipline.

**Trimmed minds (load these):**

| Mind | File (under `docs/skill-work/work-strategy/`) |
|------|-----------------------------------------------|
| Barnes | [`strategy-notebook/minds/CIV-MIND-BARNES.md`](../strategy-notebook/minds/CIV-MIND-BARNES.md) |
| Mearsheimer | [`strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md`](../strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md) |
| Mercouris | [`strategy-notebook/minds/CIV-MIND-MERCOURIS.md`](../strategy-notebook/minds/CIV-MIND-MERCOURIS.md) |

Entry stubs (pointers only): [`README.md`](README.md).

**Config & menu:**

- Machine-readable: [`../daily-brief-minds-config.json`](../daily-brief-minds-config.json)
- Human menu: [`../daily-brief-minds-menu.md`](../daily-brief-minds-menu.md)

**CLI (implementation: `scripts/generate_wap_daily_brief.py`):**

```bash
# Generate brief only (unchanged)
python3 scripts/generate_work_politics_daily_brief.py -u grace-mar \
  -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md

# After brief exists: print Tri-Frame menus to stdout
python3 scripts/generate_wap_daily_brief.py -u grace-mar --offer-minds \
  --brief-path docs/skill-work/work-strategy/daily-brief-2026-04-11.md --skip-brief

# Write one scaffold (example: Barnes, first menu option = material_constraints)
python3 scripts/generate_wap_daily_brief.py -u grace-mar --skip-brief \
  --brief-path docs/skill-work/work-strategy/daily-brief-2026-04-11.md \
  --mind barnes --mind-option material_constraints

# Write scaffolds for first option (A) of each mind
python3 scripts/generate_wap_daily_brief.py -u grace-mar --skip-brief \
  --brief-path docs/skill-work/work-strategy/daily-brief-2026-04-11.md \
  --mind-all
```

**Output naming:** `outputs/YYYY-MM-DD-<mind-key>-<suffix>.md` (suffix from config `output_suffix`, e.g. `2026-04-11-barnes-material-constraints.md`).

**Operator habit:** Coffee does **not** auto-run the brief generator ([coffee SKILL](../../../../.cursor/skills/coffee/SKILL.md)). Run the brief when ready, then optional mind overlays.

**Boundary:** WORK only — not Voice, not SELF, not automatic merge into the Record.
