# Jiang lectures — divergences from mainstream views

**Purpose:** When building the book/site, mark where Jiang’s **stated claims** **depart** from **named** mainstream or consensus positions — without treating “mainstream” as morally true or false. This is **operator research** (clarity + fair comparison), **not** Voice knowledge until merged through the gate.

**Hard rule:** Always tag **whose** mainstream you mean (jurisdiction, discipline, or institution). “Mainstream” without a scope is vague.

---

## Dimensions of divergence

| `divergence_type` | Meaning | Compare carefully |
|-------------------|---------|-------------------|
| `empirical` | Fact claims (dates, who could read scripture, vote counts) | Primary sources + specialists |
| `interpretive` | Causation, motivation, “what drives” policy | Competing IR / history models |
| `pedagogical_compression` | Simplification for class (not offered as journal-grade) | Label explicitly; not “wrong,” **compressed** |
| `normative` | What *should* happen (justice, “evil,” strategy) | Separate from predictive claims |

---

## Strength (operator judgment)

| `strength` | Use when |
|------------|----------|
| `strong` | Clear opposition to a well-defined consensus in named field |
| `moderate` | One contested school among several |
| `nuance` | Mostly aligns; emphasis or framing differ |
| `unclear` | Need more sourcing on both sides |

---

## How to write a good row

1. **`jiang_claim`** — Short, fair paraphrase (can quote transcript in `lecture_ref`).  
2. **`mainstream_anchor`** — Name the consensus: e.g. “typical US diplomatic history undergraduate narrative,” “Catholic teaching today on scripture access,” “mainstream IR (structural realism) on Middle East alliances.”  
3. **`mainstream_summary`** — One or two sentences; avoid straw men.  
4. **`evidence_notes`** — What would falsify your labeling of “mainstream” or refine the divergence.  
5. **`sources_mainstream`** — URLs or citations (optional but encouraged for non-obvious claims).  

---

## Registry

Append-only JSONL: [registry/divergences.jsonl](registry/divergences.jsonl)

Fields (typical):

- `divergence_id`, `video_id`, `lecture_ref`
- `topic_tags` (array)
- `jiang_claim`, `mainstream_anchor`, `mainstream_summary`
- `divergence_type`, `strength`
- `evidence_notes`, `sources_mainstream` (array), `sources_jiang` (optional; usually lecture URL)

---

## Relation to other lanes

- **[Prediction tracking](../prediction-tracking/README.md)** — Did a **forecast** land? Divergence tracking asks: **does the thesis match how a field usually explains the same topic?**  
- **[Influence tracking](../influence-tracking/README.md)** — Attention, not truth.  
- **CIV-MEM / analysis memos** — Divergence rows can point to `analysis/*-analysis.md` for full argument maps.

## CIV-MEM lens

“Mainstream” often differs by **which institution or seam** a discipline foregrounds (e.g. realist IR vs religious-network causality). Use [CIV-MEM-LENS.md](../CIV-MEM-LENS.md) to state **both** Jiang’s **seam/institution emphasis** and the comparator field’s — reduces straw-man comparisons.

---

## Related

- [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md)  
- [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md)  
