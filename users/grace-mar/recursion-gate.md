# RECURSION GATE — grace-mar

> Staging file for the gated profile pipeline — **one queue per companion, every channel.**
> Writers include **Telegram**, **WeChat**, **operator/Cursor** (activity reports, `calibrate_from_miss`, `parse_we_did`), **Mini App** (when wired), and **test/harness** runs. Each candidate carries **`channel_key`** (e.g. `telegram:…`, `operator:cursor`, `test:…`) so you can see the source. **Same gate, same merge** — not Telegram-only.
>
> **Workflow (one gate):**
> 1. Review each candidate below
> 2. Change `status: pending` to `status: approved` or `status: rejected`
> 3. Tell the assistant: **"approve"** — the agent immediately processes approved candidates into self.md, self-evidence.md, session-log.md, and prompt.py. No separate "process the review queue" step.
>
> **Merge checklist (correctness before approve):**
> 1. **Grounded** — Tied to something the companion actually said or did (or artifact), not invented or world-knowledge leakage.
> 2. **Merge-ready** — Would you ship this to SELF/EVIDENCE without embarrassment? If it feels like filler or duplicate IX, reject or edit.
> 3. **No duplicate lane** — Same fact already in IX-A/B/C? Reject or fold into existing entry instead of piling candidates.
> 4. **Human pass** — If only the analyst saw the exchange, one quick re-read of `example_from_exchange` / source lines.
> 5. **Portability** — For `portable-working-identity` candidates, also check [portability review checklist](../../docs/portable-record/portability-review-checklist.md).
>
> **Review checklist** (legacy one-liner): Grounded in the exchange? No LLM inference beyond it? No contradiction with existing Record?
>
> **Intent (before approve — long agents / optimization framing):** Models optimize toward task completion; constraints must be explicit. Ask: (1) **What would I not want** even if this candidate "succeeds"? (2) **When should we stop and ask** the companion? (3) **If this conflicts with INTENT**, companion + INTENT win — reject or revise. See **design-notes §11.9** (Misalignment at the interface).
>
> Machine-written by **`bot/core.py`** (Telegram, WeChat, activity reports) and by **operator scripts** that stage here — only edit the `status` field (and optional rejection notes).
>
> **Territory (work-politics vs companion):** For **work-politics** candidates, set **`territory: work-politics`** or **`channel_key: operator:wap`** (optionally `operator:wap:brief-name`). Operator tools then filter: `python scripts/operator_blocker_report.py -u grace-mar --territory wap` (work-politics territory only) or `--territory companion` (Record only). Same file, different lens.
>
> **Invariant:** Every **pending** or **approved-not-yet-merged** candidate must sit **above** `## Processed`. The bot inserts new blocks immediately before `## Processed`. If anything pending appears below Processed, move it up or merge will not see it.

---

## Candidates

## Processed

*(Cleared at reseed 2026-04-14. Previous candidates archived in `archive/companion-freeze-abby-2026-04-14/`. Full history in git tag `companion-freeze/abby-2026-04-14`.)*
