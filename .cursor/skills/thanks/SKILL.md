---
name: thanks
preferred_activation: thanks
description: "DEPRECATED for grace-mar operator workflow (2026-04). Prefer Conductor sessions or coffee light/minimal for mid-day beats. Legacy: micro-pause — thanks + optional park, two-block reply, log_cadence_event --kind thanks. See conductor SKILL + coffee SKILL."
---

# Thanks (micro-pause) — **deprecated operator workflow**

**Status (grace-mar):** The operator **no longer uses** **`thanks`** as a primary cadence command. **Prefer instead:** a **Conductor** pass ([`.cursor/skills/conductor/SKILL.md`](../conductor/SKILL.md) — master name, **`conductor`**, orientation + action MCQ), or **`coffee` light** / **`coffee` minimal** for thin reorientation without the full hub. This file stays **authoritative for legacy behavior** if an old thread or script still says **`thanks`**, and historical **`thanks`** lines remain valid in `work-cadence-events.md`.

**Preferred activation (legacy):** say **`thanks`** — optionally **same message**, after a space or punctuation, a **short park line** (what you are leaving on the desk).

`thanks` was a **bookmark**, not gratitude training for the model. It put **pauses** in **cadence telemetry** with a **one-line anchor** without running **`dream`**. **Conductors** now cover the more interesting mid-day “shape the next move” slot; **`thanks`** is redundant for that purpose.

---

## When to run (legacy only)

- **Do not** steer new operator habit toward **`thanks`.** Use **Conductor** or **`coffee` light/minimal** first.
- If the operator **explicitly** says **`thanks`** as a cadence beat (or you are finishing a documented legacy flow), run the steps below.
- **Not for:** end-of-day consolidation (use **`dream`**), Cursor session seal (use **`bridge`**), full **`coffee`** (use normal **`coffee`**).

---

## Disambiguation (agent)

- **Deprecation-first:** If the operator seems to want a **mid-day beat** but did not insist on **`thanks`**, you may **one line** suggest **Conductor** or **`coffee` minimal** — then honor a clear **`thanks`** if they repeat it.
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

3. **Parse** optional **park** text: trim the leading **`thanks`** / **`thank you`** (case-insensitive) and punctuation; remainder = **park** (collapse internal newlines to spaces; empty is OK). **Examples** of useful slugs (dash-joined; still a single `park=` value): `lane-work-dev`, `routing-focus`, `lane-strategy` — helps grep of `work-cadence-events.md` later. **After a strategy-notebook “conductor” block** (see [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)), slugs like `conductor-toscanini`, `conductor-furtwangler`, `conductor-bernstein-pulse`, `conductor-karajan-arc`, `conductor-kleiber`, `conductor-morning` make the pause grep-friendly. **Auto-park:** if the operator did not provide park text, the agent **must** infer a short 3–8 word dash-joined slug from the most recent substantive topic in this thread (e.g. `cadence-auto-park-design`, `template-sync-lockfile-impl`). Pass the inferred slug as `park=<slug>` — do **not** default to `park=none`. The script also has a git-based fallback (`auto:` prefix) but the agent should provide richer context when possible.

4. **Reply** with a **two-block** **Pause beat** only (friendly to a **new companion-self user** — no internal ops jargon in labels):
   - **Recent rhythm:** the line from step 2 (synthesis, empty-log fixed sentence, or thread fallback).
   - **Leaving on the desk:** the park text or agent-inferred slug **—** resume here, run **`coffee`** when you return, or open a **Conductor** pass when you want a scored next-move menu.

5. **Log** (operator repo, default user **`grace-mar`** unless context names another id):

```bash
python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok --kv park=<park-slug>
```

The `<park-slug>` is either the operator's park text or the agent-inferred slug from step 3. If neither the agent nor the operator provides park text, the script's auto-park fallback will generate a git-based slug with an `auto:` prefix. Use **`--no-auto-park`** to suppress the script fallback and keep `park=none` as-is.

Pass **`--cursor-model "…"`** when the Cursor UI model name is known (parity with other cadence lines); else rely on **`CURSOR_MODEL`** env or **`unknown`**.

6. **Do not** run **`auto_dream.py`**, **`operator_handoff_check.py`**, full **`coffee`** Step 1, **`bridge`**, or **RECURSION-GATE** merges as part of this skill unless the operator explicitly asks in the **same** or **next** message.

7. **No** full **`coffee` A–D** hub unless the operator pivots to **`coffee`**.

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
| **thanks** | **Deprecated** for new workflow — use **conductor** / **coffee** instead. Legacy: micro-pause + prior-line synthesis + park + two-block reply + one telemetry line |
| **dream** | Day-close maintenance |
| **bridge** | Session seal + transfer prompt |

**Optional — “Symphony of Civilization” (strategy notebook):** A longer **morning** [conductor cadence](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md) (embodied seeds, WORK layer) is **separate** from the Cursor **`coffee`** trigger above. Use `park=conductor-*` after a movement if you want the pause to show up in cadence grep.

See [work-cadence README](../../../docs/skill-work/work-cadence/README.md).
