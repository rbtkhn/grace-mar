# Polyphonic cognition protocol

Fixed-perspective decision options (A/B/C and, when relevant, D). From civ-mem STATE. No single answer; you decide.

## What it does

This skill runs the **polyphonic cognition protocol** from the civilization-memory (civ-mem) **STATE** framework: it surfaces fixed perspectives **A** (legitimacy), **B** (structure), **C** (liability) and, when the user has the civ-mem corpus or asks for the civ-mem/condition/seam angle, **D** (civ-mem lens: condition, seam, one subject many tongues, face vs category, abundance, growth). It does **not** recommend one option or synthesize them. You get the full field, plus reversibility and explicit tension labels when perspectives conflict. The protocol embeds **abundance** and **growth** mindsets: where relevant, options assume room to coordinate or expand the field (non-zero-sum) and the moment is framed as one where the principal can learn or adapt, not only succeed or fail once. Optional: state your leaning first to see how it maps to A/B/C/D ("instinct-as-input").

## How to use

- Ask for "decision options," "pre-call prep," or "angles on [topic]."
- Say "run the protocol," "give me A/B/C," or "polyphonic cognition on [X]."
- To include the civ-mem lens: ask for "civ-mem angle," "condition," "seam," "one subject many tongues," or ensure the civ-mem corpus is available—the agent will add **D**.
- Optionally state your instinct first: "I'm leaning toward X — give me A/B/C."

The agent will return labeled blocks A, B, C (and D when relevant), a reversibility line, and tension callouts when views conflict.

## Civ-mem and this skill

The protocol **is** the civ-mem **STATE** operating mode in skill form: present-moment options, multiple perspectives, tensions preserved, no write to the long-term record unless the user explicitly relays. A/B/C map to the civ-mem three minds (legitimacy, structure, liability). **D** applies the civ-mem frame to the decision: condition (purpose, reassembly), seam (two propositions held in view), one subject many tongues (how different traditions name this moment), face vs category, and where relevant **abundance** (non-zero-sum, room to coordinate) and **growth** (this moment as learning or capability-building). The protocol also embeds abundance and growth mindsets across A/B/C/D when they add substance—options that don’t assume zero-sum; the decision as a moment to learn from, not only to win or lose.

## Example

A chief of staff preps for a 30-minute call with a key ally. They ask: *"I'm leaning toward asking for the endorsement—give me A/B/C and the civ-mem angle."* The agent returns: **A** (legitimacy), **B** (structure), **C** (liability), and **D** (civ-mem lens: one subject many tongues—how the ally might name the ask; seam—want their yes vs don't burn the relationship; face vs category). Plus reversibility and tension: "A and C conflict here. We do not resolve." The staffer briefs the principal; the principal decides. After the call they note "we did X." No single recommendation—just the full field so the human decides.

## Requirements

- An AI agent that can load natural-language skills (OpenClaw, Cursor, or similar).
- No API keys, no external services, no dependencies.

## Security and permissions

**This skill is instructions-only.**

- It contains **no executable code**. No TypeScript, no shell scripts, no runtime.
- It does **not** access the network, filesystem, browser, shell, or notifications.
- It does **not** read or write any data outside the current conversation.
- It runs entirely via the agent’s natural-language entry point: the agent follows the protocol text in SKILL.md.

ClawHub manifest lists `permissions: []`. No justification for network, filesystem, or other permissions is needed because none are used.

## Troubleshooting

- **Agent gives one recommendation:** Remind it to follow the protocol: "Give me A, B, C only. No synthesis."
- **Output feels generic:** Ask for "A/B/C about this specific decision" and paste the exact context again.
- **Want simpler language:** Ask for "600L" or "plain language" — same structure, shorter sentences.

## License

MIT.
