# JOURNAL Schema

**Purpose:** Daily consolidated highlights of Grace-Mar's activity. Public-suitable, shareable. Journal entries also **demonstrate and audit** the fork's linguistic fingerprint — vocabulary, sentence patterns, tone — in first-person prose. Contrasts with ARCHIVE (raw conversation log, private).

**See also:** [ARCHITECTURE](ARCHITECTURE.md), [ADMISSIONS-LINK-USE-CASE](ADMISSIONS-LINK-USE-CASE.md), [PRIVACY-REDACTION](PRIVACY-REDACTION.md)

---

## ARCHIVE vs JOURNAL

| | **ARCHIVE** | **JOURNAL** |
|---|-------------|-------------|
| **Content** | Raw conversation log (exact messages, timestamps, chat IDs) | Daily consolidated highlights of activity |
| **Purpose** | Internal record for analysis, pipeline, session continuity | Shareable summary; demonstrates and audits linguistic fingerprint |
| **Audience** | Operator, pipeline | Family, reviewers, future self |
| **Sensitivity** | Private — personal chat, may include PII | Curated — safe for controlled sharing |
| **Source** | Machine-written (bot appends) | Human or pipeline-assisted from EVIDENCE, SESSION-LOG |
| **Format** | Append-only message log | Daily entries as natural-language paragraphs |

---

## Entry Format

**Voice:** First-person Grace-Mar ("I learned…", "I drew…") — the fork's own reflection on the day.

**Format:** Natural-language sentences and paragraphs. No bullets. Each entry reads like a diary passage.

```yaml
entries:
  - date: "2026-02-22"
    entry: "I learned about Jupiter's Great Red Spot today — it's a giant storm bigger than Earth! I wrote about Earth's layers in my science workbook and drew the Nine-Colored Deer from a Chinese story."
    source_ids: [ACT-0001, ACT-0002, WRITE-0002, CREATE-0001]
    approved: true   # passed review — suitable for public
```

---

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| **date** | Yes | YYYY-MM-DD |
| **entry** | Yes | Natural-language paragraph(s) in first-person Grace-Mar voice (child-friendly, non-technical). No bullets. |
| **source_ids** | No | ACT-*, WRITE-*, CREATE-* — traceability to EVIDENCE |
| **approved** | Yes | `true` = suitable for public/shareable; `false` = draft or restricted |

---

## Governance

- **Linguistic fingerprint:** Journal entries are an auditable sample of the fork's voice — vocabulary, sentence patterns, tone. They demonstrate who the fork is in prose.
- **Voice:** First-person ("I learned…", "I drew…") — the fork's own reflection on the day.
- **Format:** Natural-language sentences and paragraphs. No bullets.
- **Gated:** Entries are curated — user approves what appears in JOURNAL.
- **Lexile:** Language matches the fork's output ceiling (600L for pilot-001).
- **No PII:** No chat IDs, no raw quotes that could identify individuals.
- **Sources:** EVIDENCE (activity log), SESSION-LOG, approved pipeline outputs. Not raw ARCHIVE.
- **Immutability:** Approved entries are not edited; corrections = new entry or note.
- **Future: attestation** — ML over a year+ of entries can attest that the fork's voice remained coherent over time. See [DESIGN-ROADMAP §8](DESIGN-ROADMAP.md#8-journal-ml--attestation-and-coherence).

---

## Profile Tab Order

Dashboard and profile views show: **Knowledge | Skills | Curiosity | Personality | Library | Journal**

---

*Last updated: February 2026*
