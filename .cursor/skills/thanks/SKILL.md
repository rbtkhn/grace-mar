---
name: thanks
preferred_activation: thanks
description: "Grace-Mar micro-pause cadence beat. Primary trigger: thanks (optionally followed by a short park line). Logs one line to work-cadence-events.md via log_cadence_event.py --kind thanks. No dream stack, no integrity/digest, no Record merge. Lighter than signing-off coffee or bridge; heavier than silence."
---

# Thanks (micro-pause)

**Preferred activation (operator):** say **`thanks`** — optionally **same message**, after a space or punctuation, a **short park line** (what you are leaving on the desk).

`thanks` is a **bookmark**, not gratitude training for the model. It exists so **pauses** show up in **cadence telemetry** and the next thread can see a **one-line anchor** without running **`dream`**.

---

## When to run

- Stepping away for a meeting, meal, or context switch **mid-day**.
- Closing a **work block** that does **not** merit **`dream`** (no day-close maintenance).
- You want **`work-cadence-events.md`** to show a **pause** without **`coffee`** menu or **`bridge`** transfer packet.

**Not for:** end-of-day consolidation (use **`dream`**), Cursor session seal (use **`bridge`**), full reorientation (use **`coffee`**).

---

## Disambiguation (agent)

- **Treat as this ritual** when the message is **clearly** a pause close: e.g. message is **`thanks`** alone, **`Thanks.`**, **`thanks — …`**, **`thanks:`** + park line, or **`thank you`** in the same minimal shape **and** no substantive new task in the same turn.
- **Do not** treat as this ritual when **`thanks`** is **inside** a longer technical or conversational message (e.g. “the function thanks the caller for …”) or when the operator is **also** assigning new work — answer the work; **skip** cadence logging unless they say **`thanks`** as its own beat afterward.
- If **ambiguous**, ask one short question: **“Log a pause beat (thanks), or conversational only?”**

---

## Steps (agent)

1. **Parse** optional **park** text: trim the leading **`thanks`** / **`thank you`** (case-insensitive) and punctuation; remainder = **park** (collapse internal newlines to spaces; empty is OK).
2. **Reply** with a tiny **Pause beat** block:
   - **Park:** the park text, or **_(none)_** if empty.
   - **Next thread:** one line — e.g. “Resume from park line or run **`coffee`**.”
3. **Log** (operator repo, default user **`grace-mar`** unless context names another id):

```bash
python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok --kv park=<one-line-or-placeholder>
```

Use **`park=—`** or **`park=none`** when there is no park text (some shells dislike empty values; use a visible placeholder).

Pass **`--cursor-model "…"`** when the Cursor UI model name is known (parity with other cadence lines); else rely on **`CURSOR_MODEL`** env or **`unknown`**.

4. **Do not** run **`auto_dream.py`**, **`operator_handoff_check.py`**, full **`coffee`** Step 1, **`bridge`**, or **RECURSION-GATE** merges as part of this skill unless the operator explicitly asks in the **same** or **next** message.

5. **No** full **A–E** **coffee** menu unless the operator pivots to **`coffee`**.

---

## Guardrails

- **Read-only** for Record: no **`self.md`**, **`self-archive.md`**, or **`process_approved_candidates`** from **`thanks`** alone.
- **Park** text is **operator ephemera** — keep it short; it is **not** SELF truth.
- Cadence file: [docs/skill-work/work-cadence/work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md).

---

## Relation to other rituals

| Ritual | Role |
|--------|------|
| **coffee** | Framing + menu (many per day) |
| **thanks** | Micro-pause + optional park + one telemetry line |
| **dream** | Day-close maintenance |
| **bridge** | Session seal + transfer prompt |

See [work-cadence README](../../../docs/skill-work/work-cadence/README.md).
