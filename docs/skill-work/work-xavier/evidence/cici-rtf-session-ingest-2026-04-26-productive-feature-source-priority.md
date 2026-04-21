# Cici — RTF session ingest: “most productive feature next” → source-priority (WORK)

**Captured in grace-mar:** 2026-04-26  
**Session content date (transcript):** 2026-04-21  
**Territory:** work-xavier **evidence** — not Xavier’s Record; not a gate merge.

| Source (Downloads) | Stored in-repo |
|--------------------|----------------|
| `what_is_the_most_productive_feature_i_should_develop_next_2.rtf` | [cici-rtf-what-productive-feature-next-2-2026-04-21.rtf](cici-rtf-what-productive-feature-next-2-2026-04-21.rtf) |

Text extracted with `textutil -convert txt` on macOS; RTF preserved.

---

## Summary

**Prompt:** “What is the most productive feature I should develop next?” (Claude Code in [Cici](https://github.com/Xavier-x01/Cici).)

**Grounded read:** No open proposals/loops; **three stub** governed surfaces noted: **source-priority**, **tools**, **runtime-bridges**.

**Recommendation (transcript):** Fill **`source-priority` first** — Tier **A/B/C** evidence rules live in **prose** (`CLAUDE.md`, companion contract) but not as a **governed `policy.json`**; highest leverage for governance consistency; **tools** / **runtime-bridges** can follow.

**Executed in session:**

1. Draft proposal **`prop-20260421-001-source-priority-policy`** → queue JSON.  
2. User **approve** → promote → **`users/cici/governed-state/source-priority/policy.json`** (tier definitions, hierarchy, conflict rules, agent obligations); surface **stub → active**; event `evt-20260421-001`.  
3. Branch **`claude/plan-next-feature-bxJXH`** — direct push to **`main`** blocked by **branch protection** → **PR #3** opened → user **squash-merge** → **`4dba0f3`**.

**Related commits on `main` after the merge (per API, newer first):**

| SHA | Note |
|-----|------|
| [`3b25703`](https://github.com/Xavier-x01/Cici/commit/3b25703) | `feat: add daily-task skill and work journal system (#2)` |
| [`4dba0f3`](https://github.com/Xavier-x01/Cici/commit/4dba0f3) | `governed: activate source-priority surface with canonical policy.json (#3)` |
| [`2e0f6ab`](https://github.com/Xavier-x01/Cici/commit/2e0f6ab) | `add self-directed-learning agent to .claude/agents/` |

**Match to transcript (“PR #3 squash-merge **4dba0f3**”):** **Yes.** Current **`main` HEAD** is [`3b25703`](https://github.com/Xavier-x01/Cici/commit/3b25703) (later PR **#2**); **source-priority** merge is parent in history.

**Operator notes:**

- Validates **grace-mar** handoff alignment: **governed policy** for tiers beats ad-hoc prose for agents.  
- Validator **warnings** on older proposals (full path vs surface ID) called out as **pre-existing** in transcript.

---

## Files in this folder

| File | Role |
|------|------|
| [cici-rtf-what-productive-feature-next-2-2026-04-21.rtf](cici-rtf-what-productive-feature-next-2-2026-04-21.rtf) | RTF export — full session |
| This file | Summary + GitHub verification |
