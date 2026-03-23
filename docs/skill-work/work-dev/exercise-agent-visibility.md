# Exercise — Agent visibility (export + handback vs memory)

**Purpose:** One short operator ritual so you always know what an agent session actually saw and what stayed outside the repo.

**Time:** ~10 minutes.

---

## 1. Name the surface

Answer in one line:

- Is this session using **repo files** (Cursor/OpenClaw with workspace), **export bundle only**, or **chat memory only**?

There is no wrong answer — only ambiguity to remove.

---

## 2. Trace the export path (if any)

If the runtime loads an identity export:

- Where did the bundle come from on disk (path or “not from this repo”)?
- Which format was used (`md+manifest`, `fork-json`, etc.) if you know it?

If there was **no** export from this repo, write: **“No code dependency — identity not refreshed from grace-mar export this session.”**

---

## 3. Trace the handback path (if any)

If something might enter the Record:

- Was output **staged** to `recursion-gate.md` only, or also **merged**?
- Who can merge (companion / operator script), and did that happen in this session?

If nothing was staged, write: **“Handback: none this session.”**

---

## 4. Continuity check (optional but recommended)

From repo root:

```bash
python scripts/continuity_read_log.py -u grace-mar --dry-run
```

Confirm the three files (`session-log`, `recursion-gate`, `self-evidence`) are the ones you mentally “read” before work. If you skipped them, note that — visibility is the goal.

---

## 5. One-line summary

Finish with a single sentence you could paste into `session-log` or a handoff, e.g.:

- “OpenClaw used local export from `users/grace-mar/`; staged one candidate; no merge.”
- “IDE only; no export; no handback.”

---

## Related docs

- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) — read order, stage vs merge
- [session-continuity-contract.md](session-continuity-contract.md) — files + scripts + CI
- [openclaw-integration.md](../../openclaw-integration.md) — full integration guide
