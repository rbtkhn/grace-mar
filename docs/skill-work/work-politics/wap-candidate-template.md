# work-politics candidate template (RECURSION-GATE)

Paste a new `### CANDIDATE-XXXX` block **above** `## Processed` in `users/grace-mar/recursion-gate.md` (or let the bot stage; then add missing fields). Replace `XXXX` with the next id (match repo sequence). **Territory** is required so work-politics pending shows under `--territory wap` and batch merge works.

### `channel_key` — multi-client convention

Always **`territory: work-politics`**. Distinguish clients/artifacts with:

| Pattern | Example |
|---------|---------|
| `operator:wap:us-ky4-massie` | Primary Massie KY-4 |
| `operator:wap:us-state-<ST>-<slug>` | State client |
| `operator:wap:us-local-<ST>-<city>-<slug>` | Local client |
| `operator:wap:intl-<CC>-<slug>` | International (compliance cleared only) |
| `operator:wap:<artifact-slug>` | Milestone not tied to one client file |

Align with [clients/_template.md](clients/_template.md) and [README § Gate convention](README.md).

---

## Minimal milestone (ACT / evidence trail)

Use when you want a **merge receipt** and **ACT-** (or prompt slice) without bloating Abby’s IX with campaign content — tune `suggested_entry` and `profile_target` to what companion actually wants in SELF.

**Header line (in recursion-gate.md):**  
`### CANDIDATE-XXXX (work-politics — <short label>)`

**YAML body (paste under header):**

```yaml
status: pending
timestamp: YYYY-MM-DD HH:MM:SS
channel_key: operator:wap:us-ky4-massie   # or operator:wap:<jurisdiction>-<slug> — see above
territory: work-politics
# Optional — traceability to work-jiang research artifacts (merge script ignores if unused).
# Repo-relative path(s); use one string or YAML list. Examples: compressions/*.json, *.paste-snippet.md
jiang_ref: ""
source: operator — companion approved work-politics milestone
source_exchange:
  operator: "Shipped / locked: docs/skill-work/work-politics/<file>.md — <one line>"
  grace_mar: "[work-politics milestone — merge for ACT / audit only unless IX requested]"
mind_category: knowledge
signal_type: we_did / wap_milestone
priority_score: 3
summary: work-politics — <artifact> v<N> | optional revenue-log row REF
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Milestone only — see WORK doc path (minimal IX if needed)"
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
```

---

## With deliverable + revenue cross-ref

Add to `summary` or `source_exchange`:

```yaml
summary: work-politics — iran-brief v2 | revenue-log 2026-03-xx
```

```yaml
source_exchange:
  operator: "Paid deliverable closed — see revenue-log.md; artifact iran-foreign-policy-brief.md"
```

---

## Commands (after approve)

```bash
# work-politics-only batch
python scripts/process_approved_candidates.py -u grace-mar --territory wap \
  --generate-receipt /tmp/wap.json --approved-by "<name>"
python scripts/process_approved_candidates.py -u grace-mar --territory wap \
  --apply --approved-by "<name>" --receipt /tmp/wap.json
```

---

## Do not

- Stage **unsourced** political claims — knowledge boundary still applies; cite doc + companion approval in `source_exchange`.
- Put **strategy you don’t want in Voice** into `prompt_addition` — use `none` and keep detail in WORK docs unless INTENT/companion says otherwise.

See [README § Sync with RECURSION-GATE](README.md) for when to stage vs doc-only.
