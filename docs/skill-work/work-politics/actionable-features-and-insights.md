# Actionable features and insights

**Purpose:** Concrete features, copy, and process items to implement or adopt. Prioritized by impact vs effort. **Use:** Pick items to ship, add to one-pager/capability statement, or adopt in workflow.

**Implemented (as of last pass):** Method name "Polyphonic cognition protocol" in one-pager and capability statement. Cheat sheet ([cheat-sheet-polyphonic-cognition-protocol.md](cheat-sheet-polyphonic-cognition-protocol.md)) and loadable protocol skill ([polyphonic-cognition-protocol-skill.md](polyphonic-cognition-protocol-skill.md)) created. Spec updated: reversibility row, post-decision capture, 600L tier, visual export, integrations, parallel agents note, no model branding. Before/after artifact placeholder in capability statement. Copy snippets (full field, checkpoint, one principal) in one-pager. "We did X" already in prep-before-call.

**Related:** [state-evolved-assistant-brain-heads-of-state.md](state-evolved-assistant-brain-heads-of-state.md), [competitor-research-assistant-brain-judgment-testing.md](competitor-research-assistant-brain-judgment-testing.md), [lessons-solo-founder-ai-video.md](lessons-solo-founder-ai-video.md), [lessons-perplexity-computer-video.md](lessons-perplexity-computer-video.md).

---

## Features (product / UX)

| # | Feature | What to do | Why |
|---|---------|------------|-----|
| 1 | **Instinct-as-input (first step)** | In the flow: before returning A/B/C, prompt user: "What's your read? / Where are you leaning?" Then in the same response show A/B/C and one line: "Your lean sits closer to [B]. A would push back by …; C would push back by …" | Makes "testing your judgment" literal; differentiator; already in spec. |
| 2 | **Reversibility row** | In every output, add one explicit line or tag: "Reversibility: [what becomes irreversible if we do X / delay / escalate]." Optional: make it a fixed slot or sub-bullet under C (liability). | Barnes/federal audience cares; competitors don't name it. |
| 3 | **Contradiction badge in output** | When A and B or A and C (etc.) conflict, always append a visible line: "Tension: [A] and [C] conflict here. We do not resolve." | Reinforces "we never give you one answer"; builds trust. |
| 4 | **Post-decision capture (optional)** | After the principal decides, optional step: "What did you do? What happened?" — one short field or relay. Stored only if user says "record." Feeds learning loop (solo-founder lesson). | Supports "we did X" and institutional learning; differentiator. |
| 5 | **Plain-language / 600L tier** | Offer output in simple language (e.g. 600L) as an option in UI or prompt. | Accessibility; some principals prefer brevity and clarity. |
| 6 | **Catalyst reframe (C then A′, B′)** | When C (liability) is salient, next response includes: "A reframed in light of C: …" and "B reframed in light of C: …" | Sharpens other perspectives; already in concept doc; implement in prompt/logic. |
| 7 | **Polyphonic-cognition protocol skill** | Draft a **skill.md** (or skill block) that any agent or implementer can load: fixed A/B/C/D, instinct-as-input optional, contradiction badge, no write unless relay. Publish for OpenClaw/Cursor/agent-skills ecosystems and for human-run protocol. | Spreads the method without building the full product; aligns with Perplexity/Cream-style "agent skills." See [lessons-perplexity-computer-video.md](lessons-perplexity-computer-video.md). |
| 8 | **Parallel perspective agents (implementation)** | If building: one orchestrator; A, B, C (and optional D) as parallel sub-agents; each produces its slot; aggregate **without synthesis**; add tension labels. | Same pattern as Perplexity sub-agents but "combine, don't resolve." |
| 9 | **Optional visual export** | Export run as one-pager PDF or simple A/B/C diagram (three boxes + tension arrows). | Principals who prefer visual over text; "way easier to understand" (cf. Perplexity interactive outputs). |
| 10 | **Integrations (optional)** | List in spec: calendar connector, briefing/doc source; authenticate once; no autonomous scraping. | Puts context in flow; small set, not 400; see lessons-perplexity-computer-video.md. |

---

## Copy and messaging (drop-in)

Use these in one-pager, capability statement, VivaBarnesLaw post, or leave-behinds.

- **Tagline:** "We never give you one answer."
- **Headline:** "Get the full field in one place — no extra meetings to gather every perspective. You decide."
- **Conviction:** "Supports conviction: see where your read sits in the full set of options; then commit."
- **Checkpoint:** "Pre-decision checkpoint: high-quality decision point with full context, so you can direct what happens next."
- **One principal:** "One principal, full field. No committee. You hold the perspectives; you decide."
- **Overhead:** "Strip decision overhead. One place, full options, you decide — no extra meetings."
- **Research:** "Aligned with prescriptive AI research: we test your judgment against the full field; we don't replace it (e.g. arXiv 2512.04480)."

---

## Process and ops

| # | Action | What to do | Why |
|---|--------|------------|-----|
| 1 | **Name the method** | Choose one: "Polyphonic cognition protocol" or "Sovereign decision protocol." Use it in capability statement and one-pager. | Buyers get method + tool; staff can be trained on it. |
| 2 | **Short training / cheat sheet** | One-page: when to query (before call/decision), instinct-as-input optional, read A/B/C and tensions, relay only if "record." | Enables staff to run it; principal owns the call. |
| 3 | **"We did X" after each use** | After using the assistant for a decision, operator says "we did X" (e.g. "we ran the assistant before the call and chose Y") so it stages to RECURSION-GATE / session log. | Keeps Record current; reinforces habit from we-did-x-habit.md. |
| 4 | **Before/after artifact** | When you have a safe, anonymized example: one run where principal's instinct was X, field showed A/B/C, principal chose Y and (if possible) later said the liability view changed their read. Put in capability statement or proof-ledger. | Proof of "testing judgment" in practice. |
| 5 | **No model branding in UI** | In any UI or exported output, show only "A / B / C" and content — no "Claude said" or model names. | Focus on structure; reduce vendor lock-in. |

---

## Priority (suggested order)

**Quick wins (copy + process, no build):**  
- Add the copy snippets above to one-pager and capability statement where they fit.  
- Name the method and add it to both docs.  
- Adopt "we did X" after each assistant use.

**Next (prompt / logic):**  
- Instinct-as-input: add the prompt step and one-line mapping in the response.  
- Contradiction badge: add the "Tension: A and C conflict here. We do not resolve." line when perspectives conflict.  
- Reversibility: add one line or tag per output.

**Later (product):**  
- Post-decision capture (optional relay).  
- Catalyst reframe (A′/B′ after C).  
- Plain-language tier.  
- Polyphonic-cognition protocol skill (skill.md).  
- Optional visual export (PDF / A/B/C diagram).  
- Integrations (calendar, briefing source).  
- Parallel perspective agents (if building implementation).

---

*Refresh when new lessons or competitor insights land.*
