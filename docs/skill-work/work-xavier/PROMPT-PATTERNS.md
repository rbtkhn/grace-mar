# Prompt Patterns — Xavier (copy/paste)

Use these prompts in Cursor chat. Keep them unchanged unless companion asks for a tweak.

---

## 1) Draft a post card from queue item

```text
Draft one post card using our doctrine.

Input source:
- current queue item in content plan docs

Output format:
- Post ID
- Pillar
- Segment
- Draft copy
- Required receipts
- Risk level (low/medium/high)
- Stress-test needed? (yes/no)

Constraints:
- Principle-first tone
- Evidence over emotion
- No personal attacks
- Unofficial voice only
```

## 2) Run stress-test on high-stakes draft

```text
Stress-test this draft using four checks:
1) Tail risk/stale context
2) Reasoning-output alignment
3) Social anchoring pressure
4) Vibe drift over evidence

Return:
- PASS / HOLD / FAIL
- Reason in 1-2 bullets
- If HOLD/FAIL, exact fix list
```

## 3) Source verification pass

```text
Verify the factual claims in this draft against cited sources.

Return:
- Claim-by-claim table
  - claim
  - source provided?
  - source sufficient? (yes/no)
  - action required

No assumptions. Flag anything uncertain as HOLD.
```

## 4) Weekly recap builder (from live posts only)

```text
Build a weekly recap thread from posts that were actually published this week.

Requirements:
- No new claims
- Keep numbered thread format
- Include registration reminder only if date/source verified
- Add unofficial disclaimer in final post
```

## 5) Week-close KPI + budget summary

```text
Summarize week performance from the KPI/budget log.

Return:
- Planned vs shipped
- Source integrity
- Stress-test outcomes
- Spend vs cap
- 3 carry-forward insights for next week
```

