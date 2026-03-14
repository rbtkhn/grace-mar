# Civ-mem test run — 2026-03-14

**Status:** DRAFT — NOT APPROVED FOR RELEASE (G3 open)  
**Principal context:** WAP / Rep. Massie shadow-campaign support (tone: constitutional restraint, Congress’s role).  
**Purpose:** Exercise **human-always-approves** pipeline once end-to-end.

---

## G0 — Brief (human: ☐ approve)

| Field | Value |
|-------|--------|
| **Use case** | Short talking points: *Why Congress matters on war and spending* (60–90 sec) |
| **Audience** | Friendly primary voter / liberty-leaning (INTERNAL DRAFT ONLY until G3) |
| **Red lines** | No personal attacks; no claims not in principal materials unless tagged `{analyst}` |
| **CMC allowed** | Yes — for **historical framing** only; not as “what Massie said” |

**Operator sign-off G0:** _________________ **Date:** _______

---

## G1 — Scaffold (human: ☐ approve)

Machine step: `python3 tools/cmc-index-search.py query "war powers congress" --limit 5`  
(Run from `civilization_memory` repo root; index must be built.)

### Provenance pull (CMC)

| MEM path | Relevance (one line) |
|----------|----------------------|
| `content/civilizations/AMERICA/MEM–AMERICA–LAW–CONGRESS.md` | Congress’s constitutional war power vs executive practice — tension explicit in corpus |
| `content/civilizations/AMERICA/MEM–AMERICA–REVOLUTION–CONTINENTAL–CONGRESS.md` | Origin story: weak central body, no tax power — *analogy only* |
| `content/civilizations/AMERICA/MEM–AMERICA–REVOLUTION.md` | Coordination under Articles-era limits |

### Outline (scaffold)

1. Hook — representation beats remote war-by-drift `{analyst}`
2. Frame — Article I responsibility `{CMC: MEM–AMERICA–LAW–CONGRESS.md}` (historical pattern, not current vote count)
3. Close — ask for support / primary date `{principal}` (fill from calendar)

**Operator sign-off G1:** _________________ **Date:** _______

---

## G2 — Sample draft (human: ☐ approve)

**NOT FINAL COPY. Do not post, email, or attribute to principal without G3.**

---

**Talking points (sample, ~90 sec)** {analyst} + {CMC}

- The Constitution put the hard power of war in **Congress** on purpose — so no one person could drag us in. `{CMC: MEM–AMERICA–LAW–CONGRESS.md}`  
- We’ve lived through decades where that line blurred — not because the text changed, because **habit** changed. `{analyst}`  
- Our founders knew what it looked like when a central body **couldn’t** compel or tax — that was the Continental Congress era. Today’s problem is the opposite: too much done **without** a vote you can hold anyone accountable for. `{CMC: MEM–AMERICA–REVOLUTION–CONTINENTAL–CONGRESS.md}` *(analogy — not equation)*  
- If you want less dumb wars, **demand votes** — and representatives who show up for them. `{analyst}`

**Principal-specific line (placeholder — replace from principal-profile):**  
- *“[Massie line on AUMF / declarations / spending — operator insert].”* `{principal}`

---

## G3 — Release

| Channel | Approved text hash / version | Approver | Date |
|---------|-------------------------------|----------|------|
| (none) | — | — | PENDING |

---

## Test-run checklist

- [x] Protocol doc exists: [civ-mem-draft-protocol.md](civ-mem-draft-protocol.md)  
- [x] Index query executed; paths recorded above  
- [x] Every substantive bullet has `{CMC}` / `{analyst}` / `{principal}`  
- [ ] G0 signed  
- [ ] G1 signed  
- [ ] G2 signed  
- [ ] G3 signed (only when shipping)

---

## What this proved

1. **CMC retrieval** can seed a speech scaffold in minutes.  
2. **Human-always-approves** stays intact: this file is explicitly **not approved**.  
3. Next run: swap query terms for another theme (e.g. spending, Fourth Amendment) and repeat G0→G2.
