---
name: thanks
preferred_activation: thanks
description: "Grace-Mar micro-pause cadence beat. Primary trigger: thanks (optionally followed by a short park line). Reads the prior two cadence lines from work-cadence-events.md, synthesizes them into the reply, then logs one thanks line via log_cadence_event.py. No dream stack, no integrity/digest, no Record merge. Lighter than signing-off coffee or bridge; heavier than silence."
---

# Thanks (micro-pause)

**Preferred activation (operator):** say **`thanks`** — optionally **same message**, after a space or punctuation, a **short park line** (what you are leaving on the desk).

`thanks` is a **bookmark**, not gratitude training for the model. It exists so **pauses** show up in **cadence telemetry** and the next thread can see a **one-line anchor** without running **`dream`**. Each beat also **echoes the last two cadence events** (compressed), so the pause lands in **recent rhythm context**, not isolation.

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

1. **Read cadence tail** (before logging this thanks): open **`docs/skill-work/work-cadence/work-cadence-events.md`** at repo root. Below the line `_(Append below this line.)_`, collect lines that match the audit format: `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`. Take the **last two** such lines **already in the file** (the two most recent events **before** this beat). If there is only one line, synthesize that one; if none, say **Cadence tail:** _(no prior events)_.
2. **Synthesize** those lines into **one or two short sentences** in **plain prose** — enough for the operator to feel **what just happened** before this pause (mood, rhythm). **Do not** lead with UTC timestamps or `key=value` telemetry; keep the voice human. **Do not** paste the raw log lines in full unless they are already very short.
3. **Parse** optional **park** text: trim the leading **`thanks`** / **`thank you`** (case-insensitive) and punctuation; remainder = **park** (collapse internal newlines to spaces; empty is OK).
4. **Reply** with a tiny **Pause beat** block:
   - **Cadence tail:** the synthesis from step 2.
   - **Park:** the park text, or **_(none)_** if empty.
   - **Next thread:** one line — e.g. “Resume from park line or run **`coffee`**.”
5. **Log** (operator repo, default user **`grace-mar`** unless context names another id):

```bash
python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok --kv park=<one-line-or-placeholder>
```

Use **`park=—`** or **`park=none`** when there is no park text (some shells dislike empty values; use a visible placeholder).

Pass **`--cursor-model "…"`** when the Cursor UI model name is known (parity with other cadence lines); else rely on **`CURSOR_MODEL`** env or **`unknown`**.

6. **Do not** run **`auto_dream.py`**, **`operator_handoff_check.py`**, full **`coffee`** Step 1, **`bridge`**, or **RECURSION-GATE** merges as part of this skill unless the operator explicitly asks in the **same** or **next** message.

7. **No** full **A–E** **coffee** menu unless the operator pivots to **`coffee`**.

---

## Guardrails

- **Read-only** for Record: no **`self.md`**, **`self-archive.md`**, or **`process_approved_candidates`** from **`thanks`** alone.
- **Park** text is **operator ephemera** — keep it short; it is **not** SELF truth.
- If **`work-cadence-events.md`** is missing or has no lines below the append anchor, **Cadence tail:** note that briefly; still log **`thanks`** if the operator invoked the ritual.
- Cadence file: [docs/skill-work/work-cadence/work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md).

---

## Relation to other rituals

| Ritual | Role |
|--------|------|
| **coffee** | Framing + menu (many per day) |
| **thanks** | Micro-pause + **synthesis of prior two cadence lines** + optional park + one telemetry line |
| **dream** | Day-close maintenance |
| **bridge** | Session seal + transfer prompt |

See [work-cadence README](../../../docs/skill-work/work-cadence/README.md).
