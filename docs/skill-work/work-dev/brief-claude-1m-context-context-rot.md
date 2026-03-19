# Brief: Claude 1M Context Window and Context Rot

**Source:** YouTube — "Did Claude's 1M Context Window Defeat Context Rot?" (transcript).  
**Use:** Reference for context-window strategy, when to clear, and model comparison.  
**Status:** External commentary; verify against current Anthropic/Claude release notes.

---

## Claim

Anthropic’s 1M-token context for **Opus 4.6** and **Sonnet 4.6** may be the first very large context window that stays usable — i.e. an answer to **context rot**. Previously, windows over ~200K tokens tended to be “fool’s gold”: more budget but big performance drop past 100K–200K.

---

## Numbers (long-context retrieval, “eight-needle” test)

- **Opus 4.6:** ~**78.3** at 1M input tokens; only ~14% drop from 256 to 1M over ~750K tokens.
- **Comparison:** GPT-4.5 ~36, Gemini 3.1 ~26, Sonnet 4.5 ~18.5; Opus 4.5 was near Gemini (~27 at 128K). So 4.5→4.6: ~5× context (200K→1M) and ~3× effectiveness on this test.
- **Implication:** Opus 4.6 at 1M still beats or matches others; the drop-off with length is much flatter than in earlier “context rot” studies (e.g. Chroma summer study).

---

## Eight-needle test (short)

- Long conversation fills the context with many similar tasks (e.g. “write a poem about X” repeated).
- At several points (e.g. 100K, 1M tokens), the model is asked to retrieve **specific** earlier outputs (e.g. “the first poem about dogs,” “the second poem about dogs”) — the “needles.”
- Measures whether the model can still find and return the right item in a large, repetitive context (analogous to finding the right code in a large codebase).

---

## Context window management (rule of thumb from video)

- **Old heuristic (post–Chroma context-rot study):** Clear/reset around 100K–120K tokens or performance suffered.
- **With Opus 4.6 1M:** Much more wiggle room. If the drop is roughly linear, ~2% per 100K tokens is cited as a plausible rule of thumb.
- **When to clear:** Use-case dependent. If you don’t need long continuity, clearing earlier (e.g. 200K) avoids any degradation. If you need huge codebase or long continuity, you can run much longer without the previous “clear or tank” pressure.
- **Claude Code / autocompact:** Autocompact buffer ~33K tokens still applies; “when to clear” is then a product of that plus the new 1M behavior.

---

## Access and pricing (as of video)

- 1M context **generally available** for Opus 4.6 and Sonnet 4.6 (e.g. Claude Code: Max plan or Teams/Enterprise).
- **No extra multiplier** past 200K tokens; same price from ~9K to ~900K tokens.
- **Multimodal:** Up to ~600 images or PDF pages in context with good performance cited.

---

## Actionable insights

| Action | When / why |
|--------|------------|
| **Relax the 100K clear rule** | If you're on Opus 4.6 or Sonnet 4.6, you no longer need to clear at 100K–120K by default. Use length when it helps. |
| **Choose clear by use case** | Don't need long continuity (e.g. one-off task, small codebase)? Clear around 200K to avoid any degradation. Need full codebase or long thread? Run longer. |
| **Prefer Opus 4.6 for long-context retrieval** | When the task is "find and use the right thing in a big context" (code, docs, long Q&A), use 4.6 over 4.5 or other models in the same stack. |
| **Don't avoid long context for cost** | With no multiplier past 200K, cost is flat across the window. Use 1M when it improves outcomes; don't trim for pricing. |
| **Check your plan for 1M access** | Claude Code 1M needs Max / Teams / Enterprise. If you rely on long context, confirm your plan includes it. |
| **Use the runway for big-codebase work** | Large monorepos, many files, or long agent runs: you can keep more in context instead of aggressive summarization or clearing. |
| **Revisit autocompact settings** | Autocompact (~33K) still applies. If you're now comfortable with longer context, decide whether to clear less often or tune autocompact so it doesn't over-trim. |

---

## Improvements and feature ideas

*Beyond the transcript: product/UX and workflow ideas that would make 1M context more usable.*

### For context-window tools (Claude Code, Cursor, etc.)

- **Context budget / quality indicator** — Show current token count and an estimated "retrieval quality" or degradation band (e.g. "~92% of baseline" at 400K) so the user can decide when to clear with data, not guesswork.
- **Session presets** — "Small task" (suggest clear at 200K), "Big codebase" (use full runway), "Agent run" (keep until N tokens or N hours). One click or setting instead of ad hoc discipline.
- **Retrieval-confidence signal** — When the model is uncertain about which of several similar items the user meant (needle-in-haystack case), surface that: e.g. "I found three possible matches; which did you mean?" or a "Re-check references" action so the user knows when to refine or clear.
- **Partial clear / labeled regions** — Let the user label context regions ("codebase," "spec," "chat") and clear only some (e.g. clear chat, keep codebase index) if the API supports it, to preserve what matters and drop the rest.
- **Needle-style self-check (critical tasks)** — Optional command: "Before you rely on this answer, re-retrieve the key references I used" — a quick internal check that the model actually pulled the right needles, with a short report. Useful for legal, compliance, or high-stakes code.
- **Cost/quality tradeoff** — A simple control: "Optimize for speed/cost" vs "Optimize for retrieval quality" that suggests clear points or model (Sonnet vs Opus) for the current task type.

### For this repo / operator workflow

- **Long-context staging** — When staging to RECURSION-GATE or preparing evidence, include larger chunks of session or codebase in one request so the model has full picture; fewer "missing context" failures now that 1M is viable.
- **Session continuity snapshots** — At intervals (e.g. every 200K tokens or at clear points), export a compact "session state" (summary + key file refs + open decisions) so the next session can load that and continue without re-reading the whole thread.
- **Brief as checklist for tooling** — When configuring Cursor/Claude/OpenClaw, use this section as a "what would make 1M context better" checklist and feed back to tool choices or feature requests where possible.

---

## One-liner

Opus 4.6’s 1M context appears to hold retrieval quality much better than earlier large windows, reducing “context rot” and changing the tradeoff on when to clear context; treat clearing as use-case dependent rather than mandatory at 100K–120K.
