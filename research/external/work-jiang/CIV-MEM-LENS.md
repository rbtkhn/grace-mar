# Work-jiang × CIV-MEM — analytic lens

**Purpose:** Use **civilization-memory** framing (conditions, institutions, seams, continuity, horizons) as a **structured overlay** on Jiang operator research — **without** treating CMC essays or retrieval hits as automatic truth about his claims.

**Boundary (repeat):** [`civilization_memory`](../../../docs/skill-work/work-civ-mem/README.md) / [`docs/civilization-memory/`](../../../docs/civilization-memory/README.md) are **external reference surfaces**. They inform **how you analyze** lectures; they do **not** become companion Record unless gated. See [work-jiang.md](../../../users/grace-mar/work-jiang.md).

---

## 1. Why civ-mem fits work-jiang

Jiang’s Geo-Strategy material mixes **power**, **religion as institution**, **empire**, and **alliance seams** — the same family of objects civ-mem is built to hold at civilization scale. The lattice below is a **discipline for your notes**, not a verdict on Jiang.

---

## 2. Lattice → what to look for in a lecture

| Lattice slot | Question for the text | Typical tags |
|----------------|----------------------|--------------|
| **Conditions** | What background is treated as fixed? (e.g. US military dominance, “Pax” / inequality, 1948 Israel) | `conditions`, `constraints`, `starting-assumptions` |
| **Institutions** | What durable bodies carry action? (church, lobby, military, alliance, school) | `institutions`, `governance`, `hierarchy` |
| **Seams** | Where does the speaker expect **cracks**? (NATO vs US, US vs Israel, coalition legitimacy) | `seams`, `friction`, `alliance` |
| **Continuity / memory** | What past is mobilized as authority? (scripture, founding myth, 1953, Holocaust) | `continuity`, `memory`, `founding-narrative` |
| **Time structure** | Eschatology, election cycles, “two vs six years,” empire decline over decades | `time-horizon`, `eschatology`, `forecast-window` |
| **Decline / stress vectors** | Overextension, debt, civil unrest — parallel to civ-mem “decline” patterns | `decline`, `overextension`, `internal-strain` |

Use these in **analysis memos** and optionally in registry rows (see §4).

---

## 3. Map registries → civ-mem use

| Registry | Primary civ-mem move |
|----------|----------------------|
| **Influence** (`influence-tracking/`) | **Attention** over time — *not* truth. Civ-mem asks: *does a spike correlate with a **condition** change* (war news, election) or with **seam** visibility* (alliance drama)? |
| **Predictions** (`prediction-tracking/`) | Treat forecasts as **time-structured claims** against the world. Civ-mem adds: classify **what kind of civilizational object** is predicted (invasion = peak escalation; lobby = institution). |
| **Divergences** (`divergence-tracking/`) | “Mainstream” = **named field consensus**; civ-mem adds: often the real argument is **which institution or seam** the field foregrounds (realist IR vs religious-network accounts). |

---

## 4. Optional fields (future JSONL / memos)

You may extend rows with a **`civ_mem` object** (all strings, operator-written):

```json
"civ_mem": {
  "conditions": "short note",
  "institutions": "short note",
  "seams": "short note",
  "continuity_memory": "what past is invoked",
  "time_structure": "eschatological / electoral / strategic horizon",
  "decline_stress": "if any"
}
```

If empty, omit. **Do not** auto-fill from CMC retrieval without human review.

---

## 5. Retrieval workflow (when you use the corpus)

1. **Human question** — e.g. “How does civ-mem talk about empire + religion + seam?”  
2. **Query** — `cmc-index-search.py` or [in-repo index](../../../docs/civilization-memory/README.md) per your setup.  
3. **Tag provenance** — `{CMC: path}` on any pasted line in drafts (see [civ-mem-draft-protocol.md](../../../docs/skill-work/work-politics/civ-mem-draft-protocol.md) for ship-bound work).  
4. **Separate layers** — Layer A: what **Jiang said**. Layer B: what **CMC** says. Layer C: your **synthesis** (operator).

---

## 6. Worked example (Geo-Strategy #2, conceptual)

| Slot | Geo-Strategy #2 (sketch) |
|------|-------------------------|
| Conditions | US empire role; Israel–Iran tension; inequality under “Pax Americana” |
| Institutions | Church history, lobby, military–foreign-policy apparatus |
| Seams | US–Israel friction, coalition splits, intra-Christian division on eschatology |
| Continuity | Reformation, founding migrations, 1948 |
| Time structure | Second Coming frameworks; “more popular over time” |
| Decline stress | Inequality → appetite for total narratives (lecture’s Q&A thread) |

This table belongs in an **analysis memo**, not the Voice profile, unless gated.

---

## Related

- [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) — Phase E analytic passes  
- [work-civ-mem README](../../../docs/skill-work/work-civ-mem/README.md)  
- [Civilization memory lane (north star)](../../../docs/lanes/civilization-memory.md)  
