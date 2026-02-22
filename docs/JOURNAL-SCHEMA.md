# JOURNAL Schema

**Purpose:** Daily consolidated highlights of Grace-Mar's activity. Public-suitable, shareable. Contrasts with ARCHIVE (raw conversation log, private).

**See also:** [ARCHITECTURE](ARCHITECTURE.md), [ADMISSIONS-LINK-USE-CASE](ADMISSIONS-LINK-USE-CASE.md), [PRIVACY-REDACTION](PRIVACY-REDACTION.md)

---

## ARCHIVE vs JOURNAL

| | **ARCHIVE** | **JOURNAL** |
|---|-------------|-------------|
| **Content** | Raw conversation log (exact messages, timestamps, chat IDs) | Daily consolidated highlights of activity |
| **Purpose** | Internal record for analysis, pipeline, session continuity | Shareable summary — family, schools, admissions |
| **Audience** | Operator, pipeline | Family, reviewers, future self |
| **Sensitivity** | Private — personal chat, may include PII | Curated — safe for controlled sharing |
| **Source** | Machine-written (bot appends) | Human or pipeline-assisted from EVIDENCE, SESSION-LOG |
| **Format** | Append-only message log | Daily entries with highlights |

---

## Entry Format

```yaml
entries:
  - date: "2026-02-22"
    highlights:
      - "Learned about Jupiter's Great Red Spot"
      - "Wrote about Earth's layers"
      - "Drew the Nine-Colored Deer from a Chinese story"
    source_ids: [ACT-0001, ACT-0002, WRITE-0002, CREATE-0001]
    approved: true   # passed review — suitable for public
```

---

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| **date** | Yes | YYYY-MM-DD |
| **highlights** | Yes | 3–8 short bullets (child-friendly, non-technical) |
| **source_ids** | No | ACT-*, WRITE-*, CREATE-* — traceability to EVIDENCE |
| **approved** | Yes | `true` = suitable for public/shareable; `false` = draft or restricted |

---

## Governance

- **Gated:** Highlights are curated — user approves what appears in JOURNAL.
- **Lexile:** Language matches the fork's output ceiling (600L for pilot-001).
- **No PII:** No chat IDs, no raw quotes that could identify individuals.
- **Sources:** EVIDENCE (activity log), SESSION-LOG, approved pipeline outputs. Not raw ARCHIVE.
- **Immutability:** Approved entries are not edited; corrections = new entry or note.

---

## Profile Tab Order

Dashboard and profile views show: **Knowledge | Skills | Curiosity | Personality | Library | Journal**

---

*Last updated: February 2026*
