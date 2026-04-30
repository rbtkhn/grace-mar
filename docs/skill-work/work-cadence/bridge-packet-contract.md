# Bridge packet contract

**Status:** WORK artifact. Not Record. Not a merge path.

Canonical shape for the `bridge` transfer prompt. Use this when sealing one session and handing context to a fresh session, new thread, or different model.

## Section contract

| Section | Required | Notes |
|---------|----------|-------|
| `# Session Bridge - [YYYY-MM-DD]` | Yes | Title line for the packet. |
| `## Session Arc` | Yes | Episodic layer. Two to four sentences on what happened, in order. |
| `## Session Output` | Yes | Semantic layer. Two to five bullets: decisions, artifacts, patterns, open questions. |
| `## Carry-forward from last dream` | Yes | Condensed from `last-dream.json`, or say missing/stale. |
| `## RECURSION-GATE snapshot` | Yes | Pending count plus top candidates, or `Gate clear.` |
| `## Active territories` | Yes | One line per lane with recent motion. Skip lanes with none. |
| `## Priority lanes for next session` | Yes | Ranked next-session focus. |
| `## Watch this` | Yes | Single most important alert. |
| `## Since last bridge` | Yes | Delta vs last bridge state, or first bridge / no prior delta. |
| `## Bridge transfer quality` | Yes | Confidence, signals, gaps, seal. |
| `## Next session posture` | Yes | One posture plus short rationale. |
| `## Not transferred on purpose` | Optional | Max two bullets. |
| `## Commits sealed in this bridge` | Yes | Per repo summary of what was committed or skipped. |
| `## Recent commits` | Yes | Last five to ten commit lines, verbatim. |
| `## Agent surface` | Yes | Model label for the sending session. |
| `## Model transition note` | Optional | Include when the receiving session may use a different model, thread, or tool posture. |
| `## Instructions for next session` | Yes | Ends with lone `coffee` line. |

## Agent surface

Always include:

- **Cursor model:** model name from the sending session UI when visible; otherwise `unknown`.

## Model transition note

Include this section when any of the following is true:

- the next session is likely to use a different model
- the operator is switching tools or threads
- the current work depends on model-specific habits such as verbosity, tool discipline, or review style

Keep it short. One to three bullets is enough. Good content:

- expected differences in verbosity or initiative
- places where the next model should be more literal, more skeptical, or more execution-heavy
- assumptions that were still tacit in the sending session and should be made explicit

Avoid generic filler. This section is for practical receiving guidance, not model marketing.

## Closing rule

The packet must end with a final line that is exactly:

```text
coffee
```

That line must be alone on its line and not inside a code fence.
