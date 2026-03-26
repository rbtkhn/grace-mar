# No-terminal operating prompts (work-dev mirror)

Copy and paste these into Cursor chat.

---

## 1) Continuity warm start

```text
Read these files and give me a continuity brief:
- companion-xavier/users/xavier/session-log.md
- companion-xavier/users/xavier/recursion-gate.md

Output:
1) what is in progress
2) what is blocked
3) what requires human approval
4) the safest next action
```

## 2) Stage-only candidate drafting

```text
Use my latest notes to draft recursion-gate candidates only.

Rules:
- edit only companion-xavier/users/xavier/recursion-gate.md
- do not edit self.md or self-evidence.md
- mark uncertainty clearly
- include concise rationale and provenance hints

Show diff before applying.
```

## 3) Provenance check before posting

```text
Audit this draft for source integrity.

For each factual claim:
- mark supported / weak / missing source
- cite source file name if present
- suggest the smallest fix needed

Do not rewrite tone unless needed for factual safety.
```

## 4) Reliability stress-test pass

```text
Run a quick reliability pass on this output.

Check:
- instruction-following vs final action mismatch
- missing escalation for risky claims
- ambiguous ownership or approval steps

Return PASS / HOLD / FAIL with one-line reasons.
```

