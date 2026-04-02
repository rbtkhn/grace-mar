---
name: strategy-postol
preferred_activation: strategy postol
description: >-
  Apply a Postol-style technical pass (missiles, BMD, drones, tunnels, nuclear latency) to operator WORK drafts
  or fresh transcript ingests; corpus-backed via analyst-corpus INDEX + transcripts; use POSTOL-CHECKLIST.md.
  WORK only — not Record or Voice knowledge unless gated.
---

# Strategy — Postol pass

**Preferred activation (operator):** **`strategy postol`** (aliases: **`postol pass`**, **`postol ingest`** when filing a new clip).

**Purpose:** Use **Theodore Postol’s recurring technical lenses** (and the same stress tests on **non-Postol** text that makes similar claims) in a **bounded, citable** way. The skill does **not** “channel” Postol without **file + date** evidence in [analyst-corpus](../../../research/external/work-strategy/analyst-corpus/INDEX.md) or a **pasted** primary.

**Corpus (source of truth):**

| Artifact | Path |
|----------|------|
| Registry | [research/external/work-strategy/analyst-corpus/INDEX.md](../../../research/external/work-strategy/analyst-corpus/INDEX.md) — filter rows with `analyst_slug` **`theodore-postol`**. |
| Transcripts | [research/external/work-strategy/transcripts/theodore-postol-*.md](../../../research/external/work-strategy/transcripts/) |
| Checklist | [POSTOL-CHECKLIST.md](POSTOL-CHECKLIST.md) |
| Iran triangulation stub (optional) | [docs/skill-work/work-strategy/triangulation-iran-war-pape-postol-stub.md](../../../docs/skill-work/work-strategy/triangulation-iran-war-pape-postol-stub.md) |

---

## Lane

- **Think:** Procedure **A** only — **checklist table + paragraph in chat**; **no** repo writes, **no** gate merge, **no** `self.md` / prompt edits.
- **Ship (ingest):** Procedure **B** — write transcript + **INDEX** per [transcripts README](../../../research/external/work-strategy/transcripts/README.md); then **`git commit`** by default per **[Commit policy (ingest → git)](../../../research/external/work-strategy/transcripts/README.md#commit-policy-ingest--git)** (**unless** operator says **draft only** / **no commit** / **PLAN** without files).
- **Push:** **Not** part of ingest. **EXECUTE** (with push), **DOCSYNC** (with push), or explicit **git push** only.

---

## When to run

- Operator pastes **Postol** (or similar) **claims** / a **draft paragraph** / a **URL** to a Postol appearance.
- Operator says **`postol ingest`** with **transcript text** → produce **file-shaped** output for [transcripts README](../../../research/external/work-strategy/transcripts/README.md) (header, Perceiver ≤200 words, strategy hooks table, full body).
- Operator wants **triangulation** setup for **Iran** (energy + missiles/nukes): point to **stub** after running this pass on the **Postol** side.

---

## Procedure

### A — Stress-test existing copy (no new file)

1. **Load** [POSTOL-CHECKLIST.md](POSTOL-CHECKLIST.md).
2. If the operator references a **known episode**, open the matching **`theodore-postol-*.md`** from INDEX; if unknown, ask for **one** URL or paste **or** proceed on the **draft text only** (weaker evidence footnote).
3. **Run** the checklist mentally → output a **short table**:

   | Issue | Severity (H/M/L) | Fix or verify |

4. **One paragraph:** **integrated takeaway** for **work-strategy / work-politics** (operator tone), with **no** unsourced numbers.

### B — Ingest new transcript (`postol ingest`)

1. **Header:** Source, **watch URL** (placeholder if unknown), **air date** (best effort), **ingested** (today ISO), scope line + **ASR** note (Postol / BeiDou).
2. **Perceiver** — neutral summary **≤200 words** (same standard as [transcripts README](../../../research/external/work-strategy/transcripts/README.md)).
3. **Strategy hooks** — markdown table for **lenses / STRATEGY §IV (work-strategy execution memory) / triangulation**.
4. **Full transcript** — operator paste, light cleanup only.
5. **Append** [INDEX.md](../../../research/external/work-strategy/analyst-corpus/INDEX.md) row (`theodore-postol`, **digest_one_line**, **verify_focus**).
6. **`git commit`** transcript + INDEX (and checklist/stub if touched in the same ingest), **unless** operator opted out — see [Commit policy](../../../research/external/work-strategy/transcripts/README.md#commit-policy-ingest--git).

### C — Triangulation handoff

If topic is **Iran** and **both** **energy / Hormuz / power** and **missiles / BMD / latency** matter: after **A** or **B**, suggest filling [triangulation-iran-war-pape-postol-stub.md](../../../docs/skill-work/work-strategy/triangulation-iran-war-pape-postol-stub.md) **neutral fact** block and **lens** rows — **do not** assert Record facts.

---

## Guardrails (Grace-Mar)

- **WORK only** — see [AGENTS.md](../../../AGENTS.md); transcripts are **not** Voice knowledge.
- **Scenario** (effects illustrations, deterrent walkthroughs) ≠ **forecast** — label explicitly.
- **Strong technical claims** require **primary**, **official**, or **corpus-quoted** support before **public** or **campaign** ship.
- Do **not** treat **video absence of intercept** as **global** proof without **wider** methodology discussion (checklist).
- **Starlink / commercial tech** claims: always split **engineering** vs **policy / enforcement** (checklist).

---

## Related

- [current-events-analysis.md](../../../docs/skill-work/work-strategy/current-events-analysis.md) — pipeline (Perceiver → chokepoint if energy → lenses).
- [work-politics analytical-lenses](../../../docs/skill-work/work-politics/analytical-lenses/manifest.md) — three-lens block after neutral facts.
- [fact-check](../fact-check/SKILL.md) — external **web** triage on a **specific** stat or headline; use **after** or **parallel** to this pass as needed.
