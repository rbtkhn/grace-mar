# Three minds (polyphonic cognition implementation)

**Purpose:** This folder holds the **three mind profiles** ported from upstream CMC (`research/repos/civilization_memory/docs/templates/`). They are the **specific implementation** of polyphonic cognition in civ-mem: named perspectives, fixed roles, fixed option slots (A/B/C).

**Provenance:** Copied from upstream. Canonical source: `research/repos/civilization_memory/docs/templates/CIV–MIND–*.md`. Grace-Mar does not run the CMC console or MEMs; these files are **reference** for the STATE-evolved assistant brain and for the concept of polyphonic cognition.

---

## Files

| File | Mind | Role | Focus |
|------|------|------|--------|
| **CIV–MIND–MERCOURIS.md** | Mercouris | Primary (host) | Legitimacy, civilizational continuity, narrative, evidence (ARC quotes). Always active; holds the base reading. |
| **CIV–MIND–MEARSHEIMER.md** | Mearsheimer | Advisory (sharpening) | Structure, power distribution, geographic constraints. OGE-invoked; sharpens the primary. |
| **CIV–MIND–BARNES.md** | Barnes | Catalyst (required third) | Liability, mechanism, defection incentive, "who defects first." Triggers reframe in the other two; post-Barnes options: Mercouris responds to Barnes, Mearsheimer responds to Barnes. |

---

## Use in Grace-Mar

- **Assistant brain (STATE-evolved):** Fixed perspectives A/B/C map to Legitimacy (Mercouris-like), Structure (Mearsheimer-like), Liability/mechanism (Barnes-like). Optional D = civ-mem lens when corpus is ingested. See [state-evolved-assistant-brain-heads-of-state.md](../../skill-work/work-politics/state-evolved-assistant-brain-heads-of-state.md) and [concept-cognitive-polyphony.md](../notes/concept-cognitive-polyphony.md) § For Grace-Mar.
- **Polyphonic cognition:** These profiles define the **named voices** that implement "multiple perspectives, tensions preserved, no single resolution." See [concept-cognitive-polyphony.md](../notes/concept-cognitive-polyphony.md) § Implementation: upstream (three minds).
- **Reference only:** The full linguistic fingerprints (hedging, pivots, metaphors, etc.) are in the source files. For Grace-Mar's product, the **roles and focus** (legitimacy, structure, liability) are what matter unless we implement voice-specific output.

---

## Upstream

- **Repo:** `research/repos/civilization_memory`
- **Templates:** `docs/templates/CIV–MIND–MERCOURIS.md`, `CIV–MIND–MEARSHEIMER.md`, `CIV–MIND–BARNES.md`
- **Governance:** CIV–MEM–CORE, CIV–MIND–TEMPLATE. MERCOURIS is primary; MEARSHEIMER advisory; BARNES catalyst. Every MEM must satisfy a Barnes dimension (or N/A).
