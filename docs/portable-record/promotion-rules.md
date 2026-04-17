# Promotion rules — portable working-identity candidates

Where approved portable working-identity candidates belong in the four canonical Record surfaces. These rules apply after a candidate passes the [portability review checklist](portability-review-checklist.md) and receives companion approval through the gated pipeline.

---

## Surface routing

### SELF

**What belongs here:** Stable behavioral preferences, interaction tolerances, cognitive-response patterns, communication style defaults.

**Examples:**
- "Prefers short prompts with full agent output" → SELF (behavioral preference)
- "Responds to ambiguity with hypothesis-first probing" → SELF (cognitive pattern)
- "Low tolerance for filler explanations" → SELF (interaction tolerance)

### SELF-LIBRARY

**What belongs here:** Durable domains, vocabularies, reference ecosystems, conceptual maps, knowledge substrates.

**Examples:**
- "Deep familiarity with geopolitical analysis frameworks" → SELF-LIBRARY (domain knowledge)
- "Maintains structured reading/lecture intake across multiple languages" → SELF-LIBRARY (knowledge ecosystem)

### SKILLS

**What belongs here:** Reusable workflows, critique patterns, output defaults, calibration methods, repeatable procedures.

**Examples:**
- "Uses proposal-first workflow: scope → approach → files → approval" → SKILLS (workflow pattern)
- "Applies critique-then-claim pattern to external proposals" → SKILLS (evaluation method)
- "Compresses ideas in 2–3 rounds: summary → refine → tighter" → SKILLS (output calibration)

### EVIDENCE

**What belongs here:** Artifact exemplars, rationale notes, demonstrated capability traces, concrete production history.

**Examples:**
- "Produced a 12-part analytical series on post-Cold War institutional decay" → EVIDENCE (artifact trace)
- "Built a gated pipeline system for cognitive forks from scratch" → EVIDENCE (demonstrated capability)

---

## Misplacement examples

| Candidate claim | Wrong surface | Correct surface | Why |
|---|---|---|---|
| "Knows game theory deeply" | SKILLS | SELF-LIBRARY | This is a knowledge domain, not a reusable workflow |
| "Always reviews PRs with a 3-step checklist" | SELF | SKILLS | This is a repeatable procedure, not a personality trait |
| "Built the companion-self template repo" | SELF-LIBRARY | EVIDENCE | This is a concrete artifact, not a knowledge domain |
| "Dislikes verbose agent output" | SKILLS | SELF | This is a behavioral preference, not a workflow |
| "Reads Jiang lectures in Mandarin" | EVIDENCE | SELF-LIBRARY | This is a knowledge-intake pattern, not a one-time artifact |

---

## Rules

1. **Not every candidate must be promoted.** Some extracted claims are accurate but too granular, too ephemeral, or too context-specific to merit a Record entry. Rejection is normal.

2. **Promotion follows review and fit.** The companion decides what enters the Record. The script stages; the companion approves; the merge script promotes. No shortcuts.

3. **Candidates with `sensitivity_class: non_portable` or `portability_class: non_exportable`** are typically rejected unless the companion explicitly chooses to keep them as internal-only Record entries.

4. **Abstraction before promotion** is sometimes the right move. If a claim references an employer, client, or proprietary system by name, abstract it to the underlying pattern before approving.

5. **Deduplication against existing Record.** Before approving, check whether SELF, SELF-LIBRARY, SKILLS, or EVIDENCE already contain equivalent content. Fold into existing entries rather than stacking duplicates.

---

## Related

- [portability-review-checklist.md](portability-review-checklist.md) — review supplement for WI candidates
- [import-external-working-identity.md](import-external-working-identity.md) — how candidates are imported
- [working-identity-candidates.md](working-identity-candidates.md) — candidate schema and lifecycle
- [current-capability-map.md](current-capability-map.md) — portability capability inventory
- [artifact-rationale.md](artifact-rationale.md) — portable rationale format for EVIDENCE entries
