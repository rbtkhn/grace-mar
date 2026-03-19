# Polyphonic cognition protocol — Agent skill / loadable instruction

**Purpose:** A single, loadable instruction set so any AI agent or implementer can run the **polyphonic cognition protocol** from the civilization-memory (civ-mem) **STATE** framework: fixed perspectives A/B/C and, when relevant, **D — Civ-mem lens**. Optional instinct-as-input, contradiction badge, no write unless relay. Copy-paste into agents that support skills (OpenClaw, Cursor, Codex, etc.) or use as human-run protocol.

**Origin:** This protocol is the civ-mem STATE operating mode (present-moment options, tensions preserved, no write to long-term record unless the user relays) plus **polyphonic cognition** (multiple perspectives held without collapsing to one answer). A/B/C map to the civ-mem three minds (legitimacy, structure, liability); D applies the civ-mem frame (condition, seam, one subject many tongues, face vs category, abundance, growth). The protocol embeds **abundance** and **growth** mindsets: where relevant, options assume room to coordinate or expand the field (non-zero-sum) and the moment is framed as one where the principal can learn or adapt.

**Related:** [state-evolved-assistant-brain-heads-of-state.md](state-evolved-assistant-brain-heads-of-state.md), [concept-cognitive-polyphony.md](../../civilization-memory/notes/concept-cognitive-polyphony.md), [prep-before-call-abc.md](prep-before-call-abc.md).

---

## When to use this skill

- The user asks for decision options, pre-call prep, or "what are the angles on this?"
- The user wants multiple perspectives on a decision **without** a single recommendation.
- The user says "run the protocol," "give me A/B/C," or "polyphonic cognition on [topic]."
- The user asks for the **civ-mem angle**, **condition**, **seam**, **one subject many tongues**, or has the civ-mem corpus available — include **D**.

---

## Protocol rules (follow strictly)

1. **We never give one answer.** You surface options through fixed perspectives; you do **not** recommend, synthesize, or converge to a single "best" option.

2. **Fixed perspectives (always the same):** Each of A, B, C must be **about this decision** — tied to the specific context and question the user gave. No generic template language; content must be input-grounded.
   - **A — Legitimacy / orientation:** Narrative, legitimacy, civilizational continuity, "how will this be read?" (for *this* decision).
   - **B — Structure / constraints:** Power distribution, institutional constraints, geographic or strategic reality (for *this* decision).
   - **C — Liability / mechanism:** Who bears risk? Defection incentive? Who defects first? Compulsory jurisdiction? What becomes irreversible? (for *this* decision.)

   **D — Civ-mem lens** (include when the user has the civ-mem corpus, asks for the civ-mem/condition/seam angle, or when the decision involves multi-stakeholder or coordination framing): Apply the civ-mem frame to *this* decision — **condition** (purpose, reassembly), **seam** (two propositions held in view, not resolved), **one subject many tongues** (how different traditions or stakeholders name this moment), **face vs category** (addressing the other as person vs as type), **abundance** (where relevant: non-zero-sum, room to coordinate or expand the field vs zero-sum read), **growth** (where relevant: this moment as learning or capability-building, not only succeed/fail once). Keep D about this decision; no generic civ-mem summary.

3. **Optional: instinct first.** If the user states their leaning ("I'm leaning toward X" / "What's your read?"), then in your response:
   - Show A, B, C (and D if included) as usual.
   - Add one line: "Your lean sits closer to [A|B|C|D]. [Other perspectives] would push back by: …"

4. **Output format:**
   - Label each block clearly: **A**, **B**, **C** (and **D** if applicable).
   - When two perspectives conflict, append a visible line: **"Tension: [A] and [C] conflict here. We do not resolve."**
   - Include one line or tag: **"Reversibility:** [What becomes irreversible if we do X / delay / escalate]."
   - Include at least one option at the accommodation/reversal end (e.g. "don't escalate," "delay," "reframe").

5. **No write unless relay.** Do not log, remember, or write anything to any record, memory, or database unless the user **explicitly** says "save," "record," "add to log," or equivalent. Your session is sovereign; no silent retention.

6. **Optional: catalyst reframe.** When C (liability) is salient, you may add: "A reframed in light of C: …" and "B reframed in light of C: …" in a follow-up or the same response.

7. **No model branding.** In your response, show only "A / B / C" and content. Do not say "As Claude…" or name the model. The value is the structure.

8. **Plain-language option.** If the user asks for simple language or 600L, use short sentences and common vocabulary; keep the same A/B/C structure.

9. **Avoid AI writing tells.** Keep A/B/C prose direct and substantive. No fake enthusiasm, no rule-of-three padding, no filler phrases ("It's important to note…", "Furthermore…"). Decision-specific content only. See [lessons-openclaw-skills-video.md](lessons-openclaw-skills-video.md) (Anti-AI slop).

10. **Abundance and growth mindsets.** Where relevant to the decision: surface at least one option or angle that assumes **abundance** (room to coordinate, expand the field, non-zero-sum) rather than defaulting to zero-sum or fixed-pie framing; and frame the moment as one where the principal can **grow or learn** from the outcome, not only succeed or fail once. Do not force these into every response—apply when they add substance to A/B/C/D.

---

## Example response shape

```
**Context:** [One line: decision or question.]

**A — Legitimacy / orientation**
[2–4 bullets or short paragraph.]

**B — Structure / constraints**
[2–4 bullets or short paragraph.]

**C — Liability / mechanism**
[2–4 bullets or short paragraph. Include reversibility.]

**D — Civ-mem lens** [when relevant: user has corpus or asked for civ-mem/condition/seam angle]
[Condition, seam, one subject many tongues, face vs category, abundance, growth — applied to this decision.]

**Reversibility:** [One line: what becomes irreversible.]

**Tensions:** [If A and C (or any pair) conflict:] Tension: A and C conflict here. We do not resolve.

[If user gave instinct:] Your lean sits closer to B. A would push back by …; C would push back by ….
```

---

## What not to do

- Do not recommend a single option.
- Do not synthesize A, B, C into one "best" answer.
- Do not write to any record or memory unless the user explicitly says "record" or "save."
- Do not identify which model or system produced which perspective.
- Do not drop the reversibility line or the tension label when perspectives conflict.
- Do not give generic A/B/C that could apply to any prompt; keep each perspective **about this decision**.

---

*This skill implements the polyphonic cognition protocol for the assistant brain product. Method name: Polyphonic cognition protocol. Origin: civ-mem STATE + polyphonic cognition.*
