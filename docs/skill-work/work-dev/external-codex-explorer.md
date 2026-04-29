# External Codex Explorer (grace-mar)

**Status:** Active  
**Scope:** WORK-only (`work-dev`)  
**Purpose:** Produce **derived structural-neighborhood reports** for paths inside a checked-out **`civilization_memory`** tree (default: [`research/repos/civilization_memory`](../../../research/repos/civilization_memory)) — without editing upstream, without expanding Record authority.

**Last updated:** 2026-04-27

---

## What this is

A small CLI builds JSON reports describing **filesystem-adjacent** paths around a **subject** file or directory inside the checkout. Reports answer “what sits next to this path in the tree?” — **not** “what does this mean doctrinally?”

**SSOT artifact schema:** [`schema-registry/external-codex-neighborhood-report.v1.json`](../../../schema-registry/external-codex-neighborhood-report.v1.json)

**Outputs:** [`artifacts/external-codex/`](../../../artifacts/external-codex/README.md) (rebuildable; default generated `*.json` under that bucket may be gitignored — see bucket README).

---

## Governance (WORK)

- Outputs are **structural neighborhood receipts** only: **derived**, **non-canonical**, **no upstream mutation**.
- **Do not** substitute these reports for MEM grounding scripts (`suggest_civ_mem_from_relevance.py`, etc.), verify tier, strategy notebook **§1d–§1h**, or upstream **`civilization_memory`** editorial governance.
- **Do not** treat adjacency as semantic entailment ("neighbor list proves X").

---

## Recursion-gate and self-knowledge (RECORD boundaries)

Neighborhood JSON is **lighter than** curated CIV-MEM references for Record purposes: same broad family as **[SELF-LIBRARY / CIV-MEM](../../../users/grace-mar/SELF-LIBRARY/CIV-MEM.md)** (*not* IX-A), but **more derived** — structural maps of upstream paths, **not** companion-endorsed world facts.

### [`recursion-gate.md`](../../../users/grace-mar/recursion-gate.md)

| Do | Don’t |
|----|--------|
| Stage **`CANDIDATE-*`** only when the **companion explicitly wants** a short **workflow / preference** line merged (e.g. optional use of this builder when citing `civilization_memory`) — **human summary** in the candidate, **not** pasted JSON. | Auto-stage after each run; stage artifact paths as “knowledge”; stage report content as doctrine. |

Merge discipline matches [`instance-doctrine.md`](../../../users/grace-mar/instance-doctrine.md) (script-driven merge after approval).

### [`self.md`](../../../users/grace-mar/self.md) IX-A / IX-B / IX-C

- **IX-A:** Do **not** merge **substantive** claims mined from neighborhood graphs. **Rare exception:** companion-approved **meta** one-liner about **how** the companion works with civ paths (**human prose**, not schema dumps).
- **IX-B:** Only if the companion **initiates** curiosity about tooling — **not** assistant-inferred from artifacts.
- **IX-C:** Possible home for **working-style** lines **if** approved — **one sentence**, no file dumps.
- **`bot/prompt.py`:** No explorer-derived injection unless the companion **explicitly** requests a minimal boundary line — **default: omit.**

---

## CLI

From repo root:

```bash
python3 scripts/build_external_codex_neighborhood.py \
  --checkout research/repos/civilization_memory \
  --subject content/civilizations/ROME/CIV--STATE--ROME.md \
  --out-dir artifacts/external-codex
```

| Flag | Meaning |
|------|---------|
| `--checkout` | Directory relative to repo root (must exist). Default: `research/repos/civilization_memory`. |
| `--subject` | Path relative to **checkout** (required). Use forward slashes. |
| `--out-dir` | Directory for `{stem}.json` (default: `artifacts/external-codex`). Created if missing. |
| `--write-md` | Also write `{stem}.summary.md` beside JSON (optional human skim). |
| `--neighbor-limit` | Max neighbor rows (default: 250). |
| `--repo-root` | Override grace-mar repo root (default: parent of `scripts/`). |

Exit **non-zero** if checkout missing, subject escapes checkout, subject missing on disk, path traverses `..`, or path resolves under `.git`.

---

## Structural heuristics (deterministic)

For a **file** subject:

- **`same_directory`:** Other entries in the same directory (siblings), sorted.
- **`parent_directory`:** Entries in the parent of that directory (one level up), sorted — includes the directory that holds the file as orientation.

For a **directory** subject:

- **`same_directory`:** Immediate children of that directory, sorted.
- **`parent_directory`:** Sibling directories/files of that directory in its parent.

Hidden entries (names starting with `.`) except when required are skipped; **`.git`** is never traversed or listed.

---

## Relation to other lanes

- **`skill-write`:** Optional **preflight** context when paste-ready copy **anchors** to checkout paths — JSON stays WORK; see [`docs/skill-write/write-operator-preferences.md`](../../skill-write/write-operator-preferences.md).
- **`skill-strategy` / strategy-notebook:** Optional **Links / References** receipts — **after** MEM relevance picks when both apply; never replaces verify or Judgment authority.
- **`civilizational-strategy-surface.md`:** Thin bridge doc — same “no duplicate corpus” discipline.

---

## See also

- [`artifacts/external-codex/README.md`](../../../artifacts/external-codex/README.md)
- CI checkout helper: [`scripts/ci/clone_civilization_memory.sh`](../../../scripts/ci/clone_civilization_memory.sh)
