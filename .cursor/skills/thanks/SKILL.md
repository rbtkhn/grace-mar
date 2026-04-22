---
name: thanks
preferred_activation: thanks
description: "Grace-Mar micro-pause cadence beat. Primary trigger: thanks (optionally followed by a short park line). Reads the most recent cadence event from work-cadence-events.md (with empty-log and file fallbacks), synthesizes **Recent rhythm** in plain language (no internal ops jargon or timestamps in chat), replies in **two blocks** (recent rhythm + leaving on the desk with resume hint), then logs one thanks line via log_cadence_event.py. No dream stack, no integrity/digest, no Record merge. Lighter than signing-off coffee or bridge; heavier than silence."
---

# Thanks (micro-pause)

**Preferred activation (operator):** say **`thanks`** — optionally **same message**, after a space or punctuation, a **short park line** (what you are leaving on the desk).

`thanks` is a **bookmark**, not gratitude training for the model. It exists so **pauses** show up in **cadence telemetry** and the next thread can see a **one-line anchor** without running **`dream`**. Each beat **echoes the most recent cadence line** from this log (as **Recent rhythm** in chat), so the pause lands in context, not isolation.

---

## When to run

- Stepping away for a meeting, meal, or context switch **mid-day**.
- Closing a **work block** that does **not** merit **`dream`** (no day-close maintenance).
- You want **`work-cadence-events.md`** to show a **pause** without **`coffee`** menu or **`bridge`** transfer packet.

**Not for:** end-of-day consolidation (use **`dream`**), Cursor session seal (use **`bridge`**), full reorientation (use **`coffee`**).

---

## Disambiguation (agent)

- **Default — run the ritual without asking:** Message is **`thanks`** alone, **`Thanks.`**, **`thanks — …`**, **`thanks:`** + park line, or **`thank you`** in the same **minimal** shape **and** there is **no substantive new task** in the same turn. Do **not** ask “log or conversational?” for these.
- **Work first:** If the operator **also** assigns substantive work in the same message (“thanks, and fix the script…”), **answer the work**; **skip** cadence logging in that turn unless they send **`thanks`** again as its **own** beat afterward.
- **Do not** treat as this ritual when **`thanks`** is **inside** technical or narrative prose (e.g. “the function thanks the caller for …”).
- **Rare clarify:** Ask **“Log a pause beat (thanks), or conversational only?”** only when **`thanks`** might be **social politeness** inside a **longer conversational** message and intent is genuinely unclear — **not** when the line is clearly thanks-only.

---

## Steps (agent)

1. **Read the most recent cadence line** (before logging this thanks): open **`docs/skill-work/work-cadence/work-cadence-events.md`** at repo root. Below the line `_(Append below this line.)_`, find lines that match the audit format: `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`. Take **only the last** such line **already in the file** (the single most recent event **before** this beat).
   - **File missing or unreadable:** Do **not** fail the ritual. Skip file read; for step 2, set **Recent rhythm** from **one honest sentence** summarizing the **last substantive turn in this thread** (concrete topic, not generic filler).
   - **File OK but no qualifying lines below the anchor:** Use the **fixed empty-log sentence** for **Recent rhythm** in step 2 (exact wording below — do not improvise a different empty-log line).

2. **Synthesize Recent rhythm** into **one short sentence** in **plain prose** — **name concrete specifics** from the chosen cadence line (e.g. prior **coffee** mode, **bridge** feel, **dream** outcome, prior **thanks** park) **or**, when using thread fallback, from the thread. **One sentence only** for this block (the text that appears after the **Recent rhythm:** label in step 4).

   **Empty-log fixed prose (use verbatim when step 1 finds no qualifying lines below the anchor):**

   `No prior cadence events yet — this pause still bookmarks the desk.`

   **Cadence voice** (when synthesizing from a real line or thread): Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided; end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen and grounded**, not debriefed. Name what was learned, not what was executed. No commit hashes, no process names — warm, direct, future-facing.

   **Companion-facing UX:** use the **Recent rhythm** label (or prose only); **do not** include **dates, UTC, or clock times** in this prose (use sequence and plain language: “after bridge,” “then a thanks pause,” “earlier today”). **Do not** lead with a bare telemetry strip. **Do not** paste the raw log line in full unless it is already very short.

3. **Parse** optional **park** text: trim the leading **`thanks`** / **`thank you`** (case-insensitive) and punctuation; remainder = **park** (collapse internal newlines to spaces; empty is OK). **Examples** of useful slugs (dash-joined; still a single `park=` value): `lane-work-dev`, `routing-focus`, `lane-strategy` — helps grep of `work-cadence-events.md` later. **After a strategy-notebook “conductor” block** (see [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)), slugs like `conductor-toscanini`, `conductor-bernstein-pulse`, `conductor-kleiber`, `conductor-morning` make the pause grep-friendly. **Auto-park:** if the operator did not provide park text, the agent **must** infer a short 3–8 word dash-joined slug from the most recent substantive topic in this thread (e.g. `cadence-auto-park-design`, `template-sync-lockfile-impl`). Pass the inferred slug as `park=<slug>` — do **not** default to `park=none`. The script also has a git-based fallback (`auto:` prefix) but the agent should provide richer context when possible.

4. **Reply** with a **two-block** **Pause beat** only (friendly to a **new companion-self user** — no internal ops jargon in labels):
   - **Recent rhythm:** the line from step 2 (synthesis, empty-log fixed sentence, or thread fallback).
   - **Leaving on the desk:** the park text or agent-inferred slug **—** resume here or run **`coffee`** when you return.

5. **Log** (operator repo, default user **`grace-mar`** unless context names another id):

```bash
python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok --kv park=<park-slug>
```

The `<park-slug>` is either the operator's park text or the agent-inferred slug from step 3. If neither the agent nor the operator provides park text, the script's auto-park fallback will generate a git-based slug with an `auto:` prefix. Use **`--no-auto-park`** to suppress the script fallback and keep `park=none` as-is.

Pass **`--cursor-model "…"`** when the Cursor UI model name is known (parity with other cadence lines); else rely on **`CURSOR_MODEL`** env or **`unknown`**.

6. **Do not** run **`auto_dream.py`**, **`operator_handoff_check.py`**, full **`coffee`** Step 1, **`bridge`**, or **RECURSION-GATE** merges as part of this skill unless the operator explicitly asks in the **same** or **next** message.

7. **No** full **A–E** **coffee** menu unless the operator pivots to **`coffee`**.

---

## Guardrails

- **Read-only** for Record: no **`self.md`**, **`self-archive.md`**, or **`process_approved_candidates`** from **`thanks`** alone.
- **Park** text is **operator ephemera** — keep it short; it is **not** SELF truth.
- If **`work-cadence-events.md`** is missing, unreadable, or has **no** qualifying lines below the append anchor, still log **`thanks`** when the operator invoked the ritual — use the **thread fallback** or **fixed empty-log sentence** for **Recent rhythm** as in steps 1–2; do not skip logging.
- Cadence file: [docs/skill-work/work-cadence/work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md).

---

## Relation to other rituals

| Ritual | Role |
|--------|------|
| **coffee** | Framing + menu (many per day) |
| **thanks** | Micro-pause + **synthesis of the prior cadence line** (or fallbacks) + optional park + **two-block** reply + one telemetry line |
| **dream** | Day-close maintenance |
| **bridge** | Session seal + transfer prompt |

**Optional — “Symphony of Civilization” (strategy notebook):** A longer **morning** [conductor cadence](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (embodied seeds, WORK layer) is **separate** from the Cursor **`coffee`** trigger above. Use `park=conductor-*` after a movement if you want the pause to show up in cadence grep.

See [work-cadence README](../../../docs/skill-work/work-cadence/README.md).
