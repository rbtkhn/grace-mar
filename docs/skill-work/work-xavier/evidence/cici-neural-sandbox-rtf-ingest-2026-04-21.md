# Neural Sandbox (Telegram) — RTF transcript ingest (WORK)

**Captured:** 2026-04-21  
**Territory:** work-xavier **evidence** — community / onboarding context; not Xavier’s Record; not a gate merge.

| Source (Downloads) | Stored in-repo |
|--------------------|----------------|
| `Neural Sandbox transcript 04-21-2026 (3).rtf` | [cici-rtf-neural-sandbox-transcript-2026-04-21.rtf](cici-rtf-neural-sandbox-transcript-2026-04-21.rtf) |

Text extracted with `textutil -convert txt` on macOS for summary; RTF binary preserved for audit.

---

## What the transcript is

**Channel:** Neural Sandbox (Telegram), framed as a **collaborative AI learning** space around **[Cici](https://github.com/Xavier-x01/Cici)**.

**Pinned / rules document (“Neural Sandbox — Rules of Engagement”)** — structured sections:

1. **Access control** — Invite/approval by Xavier; **each member forks Cici** to their own GitHub + **own free Supabase** (no shared central instance); **secrets** (e.g. MCP access, OpenRouter) never in Telegram/GitHub public; **no access to others’ endpoints**; PRs welcome, Xavier reviews.

2. **Testing limitations** — Sandbox = **your fork only**; **do not test against Xavier-x01/Cici `main` directly**; avoid careless bulk/stress use (OpenRouter credits); no production PII in sandbox DB; share **findings**, not raw DB dumps.

3. **Data usage (Tier A / B / C)** — **Tier A:** governed-state in Git (canonical); **Tier B:** prepared-context; **Tier C:** Supabase / AI output — **not truth** for decisions; PII masking before public share; **Cici codebase** MIT + respect upstream OB1.

4. **Collaboration norms** — Async-first, blame-free, no gatekeeping, credit ideas, constructive critique.

5. **Violations** — Leaked key → rotate + notify; abuse → discussion/mute; hostility → 1:1; persistent non-compliance → removal.

6. **New member checklist** — Fork Cici, own Supabase, no secrets in Git, understand tiers, introduce self.

**Footer:** Maintained by Xavier-x01 · Last updated April 2026.

---

## Chat thread (excerpt)

- **Cebuano/Bisaya** onboarding: need ~10 people; create **GitHub on website** (laptop or phone OK).
- One member (**PenguinPH739**) shared GitHub username; Xavier confirmed and pointed to **pinned message** for next steps.

---

## Cici repo verification (GitHub API)

| Field | Value |
|--------|--------|
| **`main` HEAD** | [`b02b5da`](https://github.com/Xavier-x01/Cici/commit/b02b5da) (2026-04-20 — memory-policy apply) |
| **Change implied by this RTF alone** | **None** — transcript is **community rules + onboarding**, not a Claude Code session or merge narrative. |

If Xavier later adds `docs/neural-sandbox.md` (or similar) to [Cici](https://github.com/Xavier-x01/Cici), verify with a new commit on `main`; this ingest does **not** claim that file exists.

---

## Operator note

- **Alignment:** Tier A/B/C language **matches** Cici’s **evidence → prepared-context → governed-state** story; **fork-your-own** model matches README’s **no shared instance** posture.
- **Coaching:** Reinforce **never test against upstream `main`** and **never post keys** — already explicit in the rules text.
