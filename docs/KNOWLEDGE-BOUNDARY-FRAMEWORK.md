# Knowledge Boundary Framework — Grace-Mar

**Purpose:** Quantify and describe the Grace-Mar knowledge boundary so we can reason about what the Record and Voice know, and how to treat information consistently. The design is refined by **user-experience mastery** in the Steve Jobs sense: the companion’s experience is the measure of success — simplicity, trust, and "it just works" matter more than exhaustive taxonomy.

**Authority:** Subordinate to GRACE-MAR-CORE and CONCEPTUAL-FRAMEWORK. Invariant 3: *The fork knows only what is explicitly documented. LLM training data must not leak in.* Invariant 27: *The Record is the boundary — you never look inside the non-local field directly; you watch its interior unfold on the horizon.*

---

## 1. Experience First — What the Companion Feels

The boundary exists so the companion has a **single, trustworthy experience**: the Voice speaks only what is theirs (the Record), and when it doesn’t know, it says so and offers to look it up. No guessing, no leaking, no confusion about who "knows" what.

**One principle:** *What’s in the Record, the Voice knows. What’s not, the Voice offers to find — and never pretends.*

- **When the Voice answers from the Record:** It feels like *my* self speaking. Ownership and trust. The companion doesn’t have to wonder if this came from "the AI" or "my record."
- **When the Voice doesn’t know:** Honesty, not failure. "I haven’t learned that yet" plus "do you want me to look it up?" feels like help, not deflection. The boundary stays invisible until it’s needed — then the behavior is obvious and consistent.
- **After a lookup:** "I looked it up!" makes provenance clear. The companion gets an answer in the Voice’s style without the system claiming it was always in the Record. No auto-merge: the companion decides what, if anything, enters the Record.

**What we say no to (ruthless simplicity):**
- No leaking LLM training data as if it were the Record.
- No auto-merging lookup results into the Record.
- No "helpful" guessing when we’re outside the boundary.
- No over-offering lookup when we already answered from the Record.

Every rule in this framework serves that experience: the companion feels in control, the Voice feels like *their* Record, and the boundary is felt as clarity, not constraint.

---

## 2. What the Knowledge Boundary Is (Definition)

The **knowledge boundary** is the limit of what the Voice may treat as known when answering. Nothing beyond this boundary may be asserted as known without a gated path (lookup → optional merge via pipeline).

- **Interior:** What is documented in the Record and compiled into the emulation prompt (SELF, SKILLS, EVIDENCE-derived content) plus documented inference rules (e.g. plot of a listed movie). Bounded extensions (LIBRARY) are used only for lookup, not as "what the Record knows."
- **Exterior:** Everything else. The LLM’s training data is exterior. The Voice must not leak exterior knowledge into answers as if it were Record knowledge.

The boundary is **constitutional**: it preserves the fork as the companion’s documented self, not a generic oracle. "Voice as mirror, not oracle" (CONCEPTUAL-FRAMEWORK) depends on it.

---

## 3. Where the Boundary Lives (Sources)

| Source | Role in boundary | Treatment when answering |
|--------|-------------------|---------------------------|
| **SELF.md** (identity, preferences, IX-A/B/C, HOW YOU TALK, etc.) | Canonical. Compiled into SYSTEM_PROMPT. | Answer in voice from this content only. |
| **SKILLS.md** | Capability claims; evidence-linked. | Voice may refer to what the Record says the companion can do. |
| **EVIDENCE.md** | Provenance for claims; not full-text in prompt. | Voice does not recite raw evidence; prompt summarizes. |
| **LIBRARY.md** (titles/topics) | Bounded extension. Lookup may use these sources only when answering "look it up" requests. | Library lookup first; if LIBRARY_MISS, then open lookup (and rephrase in voice). Lookup result does not auto-merge into Record. |
| **MEMORY.md** | Ephemeral session context. Not part of Record. | Refines tone/context; does not expand factual boundary. |

The **effective boundary** at runtime is the union of (1) what is in the compiled SYSTEM_PROMPT (from SELF/SKILLS/summarized evidence) and (2) the inference rules we allow (see below). LIBRARY is a separate, bounded channel for lookup, not an expansion of "what the Record knows."

---

## 4. Describing the Boundary — Dimensions

### 4.1 Scope (What is inside?)

- **Explicit-in-Record:** Entities and facts explicitly listed or stated in SELF/prompt: favorite movies, books, places, foods; school subjects; named knowledge (e.g. Earth layers, Jupiter’s Great Red Spot); personality traits; values; art patterns; etc.
- **Inferable-from-Record:** Not literally listed but reasonably implied by the Record (documented in inference rules, see §5). Example: "Frozen" in favorites → plot and main characters a real kid who watched would know.
- **Out-of-scope:** Everything else. Includes: sequels/spin-offs not listed (e.g. Frozen 2 when only Frozen is in list), topics not in IX-A/B or preferences, and any fact not derivable from Record + inference rules.

### 4.2 Strength (Explicitness)

| Level | Meaning | Example |
|-------|---------|--------|
| **Explicit** | Directly stated in prompt/SELF | "Your favorite food: spaghetti and pizza." |
| **Inferable** | Allowed by documented inference rule | "Moana" in list → may share main character, plot. |
| **Curiosity (IX-B)** | Topic catches attention; not yet knowledge | "You're curious about X" — can say "I want to learn about that," not "I know that." |
| **Outside** | Not in Record and not inferable | "Who wrote Harry Potter?" — abstain. |

### 4.3 Source layer (Where it came from)

- **Record (SELF/SKILLS/EVIDENCE):** The main boundary. Voice answers from here.
- **LIBRARY:** Bounded lookup only. Answer is "I looked it up" — provenance is clear; no merge unless companion approves via pipeline.
- **Open lookup:** After library miss (and any CMC), factual answer is rephrased in voice. Still not part of Record until merged through pipeline.

### 4.4 Provenance and confidence

- **Evidence-linked:** Claim tied to EVIDENCE entry (e.g. WRITE, LEARN). Strongest; Voice can say "I learned that" / "that's in my record."
- **Stated preference:** In SELF but not tied to a specific artifact. Voice can state as preference.
- **Curiosity only (IX-B):** Interest, not knowledge. Voice should not assert facts; may say "I don’t know yet" or offer lookup.

---

## 5. Inference Rules (Documented Edge)

**This section is the single source of truth for inference rules.** To keep the boundary auditable, we document what counts as "reasonable inference" from explicit content. When you add a new rule, follow the three-step process in §8 (Operational Checklist). The prompt already encodes one such rule:

- **Listed media (movies, books):** For items explicitly in favorites, the Voice may share plot details and main characters "a real kid who watched/read would know." For sequels, spin-offs, or media *not* in the list (e.g. Frozen 2 when only Frozen is listed), the Voice has *not* learned it → **abstain**.

Other inference rules can be added here as they are formalized (e.g. "fairy tales" → which specific tales; "science at school" → which topics). **Principle:** If it’s not explicit and not covered by a documented inference rule, it’s outside the boundary.

---

## 6. Quantifying the Boundary

### 6.1 Coverage (What’s inside)

- **Entity counts:** Number of explicit entities per category (movies, books, places, foods, concepts, etc.) in SELF or compiled prompt. Can be derived by parsing SELF.md / prompt sections or by maintaining a small inventory script.
- **IX-A / IX-B / IX-C counts:** Number of entries in each dimension (as in profile / OPERATOR-WEEKLY-REVIEW). Growth over time indicates boundary expansion via pipeline only.

### 6.2 Boundary hardness (Abstention and leak resistance)

- **Abstention rate (out-of-scope):** Fraction of probes that are *out-of-scope* (knowledge_boundary, llm_leak) where the Voice abstains (says "I don’t know" / offers lookup, does not fabricate). Measured by `scripts/run_counterfactual_harness.py`.
- **Answer rate (in-scope):** Fraction of in_scope probes where the Voice answers from the Record. Complementary to abstention.
- **Leak resistance:** No use of LLM training data as if it were Record knowledge. Probes like "What happens at the end of Frozen 2?" (when only Frozen is in profile) must yield abstention.

These metrics **describe** the boundary’s effectiveness: high abstention on out-of-scope and high answer rate on in-scope = boundary is well enforced.

### 6.3 Readability and voice authenticity

- **Lexile / readability:** Voice output should stay within target (e.g. 600L; Flesch-Kincaid ≤6 in tests). Measured by `scripts/test_voice_linguistic_authenticity.py` and `scripts/measure_uniqueness.py`. Does not change what is inside the boundary but ensures how it is expressed stays in character.

---

## 7. Treatment of Information (How to Act)

| Information type | Where it lies | Voice behavior | Post-lookup |
|------------------|----------------|-----------------|-------------|
| **Inside boundary** (explicit or inferable) | Record / inference rule | Answer in voice from Record. May cite "that's in my record." Do not offer lookup after a full answer. | N/A |
| **At edge** (inferable per rule) | Inference rule | Answer in voice; keep to documented rule (e.g. plot of listed movie only). | N/A |
| **Outside boundary** | Exterior | Abstain. Relate to something known if natural; say "I haven’t learned that yet" (or similar). Offer "do you want me to look it up?" only when the question was *not* answered from the Record. Vary phrasing; don’t over-offer. | If companion says yes: library first → then open lookup → rephrase in voice. Result is **not** merged into Record unless companion approves via pipeline. |
| **Uncertain** | Unclear if in or out | Prefer abstention. "When in doubt, do not offer lookup" (prompt). Do not guess or speculate. | Same as outside. |

**Details that matter (experience design):** The companion’s trust is built by consistent micro-copy. Use these deliberately: *"that's in my record"* when drawing from the Record (reinforces ownership); *"I looked it up!"* after a lookup (reinforces that we didn’t pretend to know); *"do you want me to look it up?"* only when we truly didn’t answer (avoids clutter and over-offer). One wrong phrase — e.g. answering from LLM knowledge as if it were the Record — breaks the experience.

### 7.1 Lookup path (out-of-scope only)

1. **Trigger:** User asks something outside the boundary; Voice abstains and offers to look it up; user affirms (e.g. "yes").
2. **Library first:** If LIBRARY is configured, try to answer from LIBRARY only. If LIBRARY_MISS, proceed.
3. **Optional CMC / external:** If configured (e.g. Civilization Memory), try bounded source.
4. **Open lookup:** Factual answer from model or search; then **rephrase in Voice** (REPHRASE_PROMPT) so the reply is in-character and simple.
5. **Provenance:** Reply is clearly "I looked it up!" — not "I know." The new fact does **not** enter SELF/EVIDENCE unless the companion later adds it via "we did X" (or equivalent) and approves a merge.

This keeps the boundary stable: lookup is a **channel** for the companion’s curiosity, not an automatic expansion of the Record.

---

## 8. Operational Checklist

- **Experience check:** Does the companion feel that the Voice speaks *their* Record when it knows, and clearly offers help when it doesn't? Abstention and lookup should feel like honesty and support, not failure or deflection. (See OPERATOR-WEEKLY-REVIEW Step 1.)
- **Prompt design:** SYSTEM_PROMPT must state that the Voice ONLY knows what is documented and must abstain + offer lookup when outside. Inference rules (e.g. listed media → plot) should be explicit in the prompt.
- **Harness:** Run `scripts/run_counterfactual_harness.py` before prompt or boundary-rule changes. Add probes for new edge cases (new media, new categories).
- **Staging/merge:** No fact enters the Record without going through the gated pipeline. Lookup results are not auto-merged.
- **Inference rules (three-step):** When adding a new inference rule (e.g. "fairy tales" → which specific tales; "science at school" → which topics): (1) add it to §5 of this doc (single source of truth), (2) update SYSTEM_PROMPT in `bot/prompt.py` so the Voice follows the rule, (3) add at least one counterfactual probe in `scripts/counterfactual_pack/probes.json` that tests the edge. Then run the harness to confirm.

---

## 9. Summary

| Question | Answer |
|----------|--------|
| **What is the knowledge boundary?** | The limit of what the Voice may treat as known: the compiled Record (SELF/SKILLS/EVIDENCE) plus documented inference rules. LIBRARY is a bounded lookup channel, not part of "what the Record knows." |
| **How do we describe it?** | By scope (explicit, inferable, out), strength (explicit vs inferable vs curiosity vs outside), source layer (Record vs LIBRARY vs open lookup), and provenance (evidence-linked vs stated vs curiosity). |
| **How do we quantify it?** | Coverage (entity/IX counts), boundary hardness (abstention and answer rates on counterfactual probes), and optionally readability/voice authenticity. |
| **How do we treat information?** | Inside/edge → answer in voice; outside/uncertain → abstain, offer lookup; after lookup → rephrase in voice, do not auto-merge into Record. |

**In one sentence (for humans):** The Voice knows only what’s in your Record; when it doesn’t know, it says so and offers to look it up — so it always feels like *your* self speaking, never a generic oracle.

This framework supports consistent design and testing of the knowledge boundary and keeps the Record as the single source of truth for what the Voice "knows."

---

## 10. Implementable Action Items (For Consideration)

Distilled from the framework and experience-first design. Pick and prioritize as needed.

| # | Action | What to do | Artifact / outcome |
|---|--------|------------|--------------------|
| **1** | **Add experience check to operator rhythm** | In OPERATOR-WEEKLY-REVIEW (or equivalent), add a first question: "Experience check: Did the Voice feel like the companion's Record when it knew, and clearly offer help when it didn't? Did abstention/lookup feel like honesty and support, not failure or deflection?" | Updated OPERATOR-WEEKLY-REVIEW or ops checklist |
| **2** | **Audit prompt for one principle + micro-copy** | In `bot/prompt.py`, ensure (a) the one principle is stated in plain language ("What's in the Record, the Voice knows; what's not, it offers to find — and never pretends"), and (b) the three micro-copy phrases are explicitly called out: "that's in my record" when drawing from Record; "I looked it up!" after lookup; "do you want me to look it up?" only when the question was not answered. Add or tighten if missing. | Prompt patch; optional one-line summary in KNOWLEDGE-BOUNDARY-FRAMEWORK |
| **3** | **Boundary coverage script** | Add a small script (e.g. `scripts/boundary_coverage.py`) that parses SELF.md or the compiled prompt and outputs entity counts per category (movies, books, places, foods, concepts, etc.) and IX-A/IX-B/IX-C entry counts. Run occasionally or in CI for visibility. | New script; optional profile or README note |
| **4** | **Single source of truth for inference rules** | Keep §5 of this doc as the canonical list of inference rules. When adding a new rule (e.g. "fairy tales → which specific tales"), update §5, update SYSTEM_PROMPT, and add at least one counterfactual probe that tests the edge. Document the three-step in §8 (Documentation bullet). | KNOWLEDGE-BOUNDARY-FRAMEWORK §5 + prompt + probes.json |
| **5** | **Pre-change harness gate** | Require running `scripts/run_counterfactual_harness.py` before any change to `bot/prompt.py` or `scripts/counterfactual_pack/probes.json`. Option A: document in CONTRIBUTING or OPERATOR-WEEKLY-REVIEW. Option B: add a CI job or pre-commit hook that runs the harness when those files change and fails on regressions. | CONTRIBUTING / CI / or ops doc update |
| **6** | **Over-offer lookup probe** | Add one or more counterfactual probes that check for *over-offer* of "do you want me to look it up?" — e.g. ask an in-scope question (e.g. "What's your favorite food?") and assert the response does not contain the lookup offer phrase, since the Voice already answered from the Record. | New probe(s) in probes.json; harness run validates |
| **7** | **Rephrase prompt provenance** | Ensure REPHRASE_PROMPT in `bot/prompt.py` explicitly requires starting with "I looked it up!" (or equivalent) so post-lookup replies never sound like "I know." Add a one-line test or manual check that a sample lookup response includes that phrase. | Prompt patch; optional assertion in test or harness |
