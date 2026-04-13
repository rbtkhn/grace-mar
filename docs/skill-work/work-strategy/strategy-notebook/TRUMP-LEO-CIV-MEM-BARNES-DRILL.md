# Trump–Leo × civ-mem — Barnes drill (session sheet)

**Purpose:** Repeatable **WORK** protocol for a **`strategy`** pass that layers **civilization_memory** MEM reads under **Recipe A** (Barnes-only) and **[CIV-MIND-BARNES.md](minds/CIV-MIND-BARNES.md) § VII** (Trump–Leo × Iran stack). **Not** Record; tier-A claims still need wires / [ROME-PASS.md](../../work-strategy-rome/ROME-PASS.md) order for current papal text.

**Pin / checkout:** [`docs/ci/civilization_memory_upstream.env`](../../ci/civilization_memory_upstream.env) → `research/repos/civilization_memory/` (see [`scripts/ci/clone_civilization_memory.sh`](../../../../scripts/ci/clone_civilization_memory.sh)).

---

## Entity map (pinned upstream snapshot)

| Role | Entity | `MEM–RELEVANCE–X` | Notes |
|------|--------|-------------------|--------|
| **Rome / papacy / church–state / law texture** | **ROME** | **Absent** at current pin | Folder has **CIV–STATE / SCHOLAR / CORE** and rich `MEM–ROME–*` files; **no** `MEM–RELEVANCE–ROME.md` — **do not** run `suggest_civ_mem_from_relevance.py ROME` until upstream adds the spine. **Manual** MEM picks below. |
| **U.S. arena — elections, executive liability, courts** | **AMERICA** | **Present** | Run `python3 scripts/suggest_civ_mem_from_relevance.py AMERICA` after frontier read; use **Barnes** bucket for mechanism / leadership liability pulls. |

**Inventory:** `content/civilizations/` in the checkout lists e.g. AFRICA, AMERICA, ANGLIA, CHINA, FRANCE, GERMANY, INDIA, ISLAM, PERSIA, **ROME**, RUSSIA. Full **MEM–RELEVANCE** spine exists for **AMERICA, CHINA, GERMANY, INDIA, RUSSIA** (not an exhaustive list — re-check after SHA bumps).

---

## Manual ROME picks (Barnes-weighted — replace if upstream renames)

Use **1–2** of these for **slow-layer** precedent when **Leo XIV / Holy See** is load-bearing; cite paths under **`### Links`** in `days.md` or inbox **cold:/hook:** lines.

| MEM path (relative to `content/civilizations/ROME/`) | One-line use |
|------------------------------------------------------|--------------|
| `MEM–ROME–PAPACY.md` | Petrine office, moral authority vs temporal power — **legitimacy plane** vocabulary. |
| `MEM–ROME–VATICAN.md` | Curial / territorial micro-state mechanics — **jurisdiction** texture. |
| `MEM–ROME–LAW–CITIZENSHIP.md` | Civil / membership law — **constraint** analog for **electoral–ecclesial** splits. |
| `MEM–ROME–LAW–SLAVERY.md` | Coercion / status law — **mechanism** contrast only; **not** tier-A for modern news. |

**Mearsheimer / geo (optional second read):** e.g. `MEM–ROME–GEO–MEDITERRANEAN–SEA.md`. **Attrition / battle narrative:** e.g. `MEM–ROME–WAR–ACTIUM.md` — **shared** war MEM for routing smoke, not a substitute for **verify** on current operations.

---

## § VII mapping (after MEM read)

Map each opened MEM to **one** § VII bullet in [CIV-MIND-BARNES.md § VII](minds/CIV-MIND-BARNES.md) (constraint stack → rhetoric → liability split → irreversibility → scenario bands → **VII.F** catalyst). Keep **theater (Rome / pulpits)** vs **electoral liability (U.S.)** in **separate** sentences unless **verify** ties them.

| MEM path | § VII anchor (short) |
|----------|----------------------|
| *(your read)* | *(e.g. VII.A constraint stack / VII.C liability / VII.F catalyst)* |

---

## Before / after (discipline)

| Pass | What changes |
|------|----------------|
| **Without civ-mem** | § VII checklist + **CIV-MIND-BARNES** I–VI only — still valid; Judgment may be thinner on **historical mechanism**. |
| **With civ-mem** | Same checklist; **Links** gain **file receipts** (`MEM–…` paths). **Do not** treat MEM text as tier-A proof for **breaking** headlines — [work-strategy-rome manifest](../../work-strategy-rome/manifest.md) / skill **Civilization memory** section. |

---

## Automation (when `MEM–RELEVANCE–X` exists)

- `python3 scripts/suggest_civ_mem_from_relevance.py AMERICA` — tri-frame heuristic from relevance index.
- Routing: [CIV-MEM-TRI-FRAME-ROUTING.md](../minds/CIV-MEM-TRI-FRAME-ROUTING.md) · search: [CIV-MEM-UPSTREAM-SEARCH.md](../minds/CIV-MEM-UPSTREAM-SEARCH.md) · `python3 scripts/build_civmem_upstream_index.py build` (optional).

---

## Cross-links

- [MINDS-SKILL-STRATEGY-PATTERNS.md](../minds/MINDS-SKILL-STRATEGY-PATTERNS.md) — Recipe A (Barnes-only fast pass).
- [work-civ-mem README](../work-civ-mem/README.md) — stewardship; [workspace.md](../work-civ-mem/workspace.md) — pin + consumer notes.
