# Privacy and Redaction

**Purpose:** Document what is excluded when sharing the Record with schools or publicly. Use `scripts/export_view.py` to generate redacted exports.

**See also:** [PORTABILITY](PORTABILITY.md), [ADMISSIONS-LINK-USE-CASE](ADMISSIONS-LINK-USE-CASE.md).

---

## Views

| View | Use case | Exclusions |
|------|----------|------------|
| **school** | Hand to a school, tutor, or admissions office | Birthdate, exact location, places_lived, relationships, family members, family dynamics |
| **public** | Portfolio, public-facing "meet me" page | All identity (name, age, location), birthdate, narrative, raw evidence; keeps preferences, interests, values, IX summary, skills summary |

---

## school view

**Included:** Identity (name, age, languages — but birthdate and location redacted), preferences, linguistic style, personality, interests, values, reasoning, narrative (with redactions), post-seed growth (IX-A/B/C).

**Excluded / redacted:**
- `birthdate` → `[redacted]`
- `location` → `[state/region only]` (or generalized)
- `places_lived` → `[redacted]`
- `relationships` → `[redacted]`
- `members` (family) → `[redacted]`
- `dynamics` (family) → `[redacted]`

**Favorites** (places like Elitch Gardens, San Diego) are included — they are preferences, not addresses. If a place is identifying (e.g. home address), add it to the redaction list in `export_view.py`.

---

## public view

**Included:** Preferences, interests, values, post-seed growth summary, skills summary (high level).

**Excluded:** Identity (name, age, location, birthdate), linguistic style, personality details, narrative, raw evidence, writing samples, artifact references.

---

## Usage

```bash
python scripts/export_view.py --view school -u grace-mar -o school-export.md
python scripts/export_view.py --view public -u grace-mar -o portfolio.md
```

---

## Extending redaction

To add new redaction rules, edit `scripts/export_view.py` and add helper functions (e.g. `_redact_X`). Update this doc to describe the change.

---

*Document version: 1.0*
*Last updated: February 2026*
