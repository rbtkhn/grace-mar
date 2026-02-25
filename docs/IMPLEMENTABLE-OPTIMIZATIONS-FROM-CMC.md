# Implementable Optimizations from CMC Substance

Concrete code and prompt changes proposed from [NOTES-CMC-SUBSTANCE](NOTES-CMC-SUBSTANCE.md). **Proposals only** — implement after approval.

---

## 1. Response contract in system prompt (duty of competence + multiple perspectives)

**Source:** CMC duty of competence (§9), mandatory verdict block (§11), tensions preserved (§10).

**Proposal:** Add one bullet under `IMPORTANT CONSTRAINTS` in `bot/prompt.py` (after the LOOKUP RULE / MICRO-COPY block):

- **Response contract:** (1) Every answer is either from your Record or you explicitly abstain / offer to look it up. (2) When your Record has more than one view on a topic (e.g. different memories or tensions), you may say both instead of picking one — e.g. "I have this in my record … and also …" so the companion sees the angles you have.

**Files:** `bot/prompt.py` (SYSTEM_PROMPT, in the IMPORTANT CONSTRAINTS section).

**Scope:** One short bullet; no change to model or API. Optional: add a single example line in MICRO-COPY for "when I have two things in my record I can say both."

---

## 2. Analyst: explicit contradiction-preservation rule

**Source:** CMC Scholar non-synthesis rule (§5), MEM authoritative over Scholar (§7).

**Proposal:** In `bot/prompt.py`, in the ANALYST_PROMPT **Rules** section, add:

- **CONTRADICTION PRESERVATION:** If the signal could support an alternative interpretation or **conflicts** with existing profile, still stage it and note the tension in your output. Do **not** resolve contradictions or harmonize; preserve both. You record learning events, not conclusions. When in doubt, stage and let the companion decide.

Strengthen the existing line ("If the signal could support an alternative interpretation or conflict with existing profile, note it briefly") into this full rule so the analyst never silently drops or reconciles conflicting signals.

**Files:** `bot/prompt.py` (ANALYST_PROMPT, Rules section).

**Scope:** One new rule bullet; possible small tweak to output format to include optional `tension_with: [entry_id]` or `alternative_interpretation: "…"` when relevant.

---

## 3. Optional scope/constraint on IX entries (schema + docs)

**Source:** CMC hard constraints per doctrine (§4).

**Proposal:**

- **Schema/doc:** In `docs/SELF-TEMPLATE.md` (or `docs/EVIDENCE-TEMPLATE.md` if IX is documented there) and in `docs/SELF-TEMPLATE.md` Section IX, add an **optional** field for LEARN/CUR/PER entries:
  - `scope:` or `constraint:` (optional) — when this belief does not apply or would be invalid (e.g. "Only for pre-modern steppe cases" or "If X then this narrows"). Free text or a short list.
- **Usage:** No requirement to backfill existing entries. New pipeline merges may add `scope` or `constraint` when the candidate implies a boundary (e.g. from analyst "alternative interpretation" note). Prompt and PRP export can ignore the field initially; it is for audit and future use.

**Files:** `docs/SELF-TEMPLATE.md`, optionally `docs/EVIDENCE-TEMPLATE.md`; `AGENTS.md` File Update Protocol table could mention "optional scope/constraint when merging."

**Scope:** Documentation and optional field; no change to `process_approved_candidates.py` logic unless we later want to copy `constraint` from candidate YAML into SELF.

---

## 4. Governance checker: whitelist of writers to Record

**Source:** CMC doctrine does not learn; State → Scholar only by relay (§3, §8).

**Proposal:** In `scripts/governance_checker.py`:

- Add a **whitelist** of paths/scripts that are allowed to write to `users/*/SELF.md`, `users/*/EVIDENCE.md`, or `users/*/PENDING-REVIEW.md` (e.g. `scripts/process_approved_candidates.py`, and optionally `bot/core.py` only for appending to PENDING-REVIEW when staging). Any other code in `bot/` or `scripts/` that matches "write to SELF.md / EVIDENCE.md" (or open for write) and is **not** on the whitelist → violation.
- Implement as: (1) extend `MERGE_WITHOUT_APPROVAL_PATTERNS` or add a new check that looks for `SELF.md` or `EVIDENCE.md` in a write/open path; (2) when a match is found, allow it only if the file doing the write is in the whitelist (e.g. `process_approved_candidates.py`). Exclude `governance_checker.py` and test files.

**Files:** `scripts/governance_checker.py`.

**Scope:** One new pattern or function; whitelist as a constant. May need to relax or refine if other legitimate writers exist (e.g. export scripts that don’t modify Record).

---

## 5. Explicit "relay only" comment in core

**Source:** CMC State → Scholar only by explicit relay (§8).

**Proposal:** In `bot/core.py`, at the top of `get_response` (or just before the branch that calls `analyze_activity_report` / `_run_analyst_background`), add a one-line comment:

- `# Session (State) never writes to SELF/EVIDENCE; staging is the only path. Merge only via process_approved_candidates after companion approval.`

**Files:** `bot/core.py`.

**Scope:** Comment only; no behavior change. Helps future readers and aligns with CMC relay rule.

---

## 6. Optional: response-boundary spot check (lightweight)

**Source:** CMC mandatory verdict block (§11); knowledge boundary.

**Proposal:** Add an **optional** heuristic or script that, given the last assistant message and the current SYSTEM_PROMPT (or a summary of "topics in Record"), flags possible boundary violations:

- Heuristic: e.g. detect sentences that look like factual claims ("X is …", "Y was …") and check whether a small set of claimed entities/topics appear in a tokenized set of "allowed" terms from the prompt. High false-positive rate acceptable; used for operator audit only.
- Or: a separate script `scripts/spot_check_response_boundary.py` that takes a message + user_id, loads prompt or PRP, and runs a simple rule or LLM call: "Does this message claim knowledge outside the following Record summary? Yes/No + brief reason." Output to stdout or a log; no automatic blocking.

**Files:** New `scripts/spot_check_response_boundary.py` (or similar), or a small function in `bot/core.py` that logs to a dedicated file when enabled via env (e.g. `GRACE_MAR_BOUNDARY_CHECK=1`). Not enabled by default.

**Scope:** Optional; no impact on production path unless enabled. Proposal only; implementation detail (heuristic vs LLM) to be decided.

---

## Summary

| # | Proposal | File(s) | Scope |
|---|----------|---------|--------|
| 1 | Response contract (abstain or cite; multiple perspectives) | `bot/prompt.py` | 1 bullet in SYSTEM_PROMPT |
| 2 | Analyst contradiction-preservation rule | `bot/prompt.py` | 1 rule in ANALYST_PROMPT; optional output field |
| 3 | Optional scope/constraint on IX entries | `docs/SELF-TEMPLATE.md`, AGENTS | Doc + optional field |
| 4 | Governance: whitelist writers to Record | `scripts/governance_checker.py` | New check + whitelist constant |
| 5 | Relay-only comment in core | `bot/core.py` | 1 comment |
| 6 | Optional response-boundary spot check | New script or core | Optional audit only |

**Implementation status:** 5, 1, 2, 3, 4 implemented (2026-02-24). 6 optional (not implemented).
