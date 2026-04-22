# strategy-state-iran (institutional / elite lane)

**Purpose:** Parallel notebook tree for **Iranian institutional and elite-authored** material (Majlis, MFA-adjacent social, Tasnim-class republication, repost chains) that **complements** Western **`thread:`** **commentators** (main notebook [`experts/`](../experts/) — analysts / hosts, **not** office-holders here). Same **chapters + per-official-voice folder** shape, **not** the same ingestion scripts until wired. **Terminology:** these are **official** / **state** voices — **not** “experts” in the notebook’s commentator sense.

**Relation to the main notebook:**

| Main strategy-notebook | strategy-state-iran (this tree) |
|------------------------|----------------------------------|
| [`experts/<expert_id>/`](../experts/) — indexed **commentators** (`thread:`) | [`voices/<voice_id>/`](voices/) — Iranian **official** / institutional **voices** (e.g. `mb_ghalibaf`, `araghchi`, `drpezeshkian`) — **monthly journal + `strategy-page` blocks** live in **one** file: [`voices/iri-institutional/thread.md`](voices/iri-institutional/thread.md) (tri-voice subsections); per-voice folders keep **profile** + redirect **`thread.md`** stub |
| [`chapters/YYYY-MM/days.md`](../chapters/2026-04/days.md) — full chronology | [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) — **thin calendar index** → **[`daily/YYYY-MM-DD.md`](chapters/2026-04/daily/)** per day |
| [`raw-input/`](../raw-input/) | Same [`raw-input/`](../raw-input/) paths — **point here**, do not duplicate verbatim |

**Rules:** WORK only; not Record. **Cross-weave** with main `days.md` and [`daily-strategy-inbox.md`](../daily-strategy-inbox.md); **do not** collapse MFA primaries, Majlis rhetoric, and U.S.-side **`thread:`** commentator lanes without **tier** and **seam** tags.

## Workflow (v1 — docs-first)

1. **Raw-input first:** Tables and captures live under **`raw-input/`** with stable **slice anchors** (see bundle footers). **Grep fallback:** first table cell `| YYYY-MM-DD |` in any bundle row.
2. **Institutional thread / strategy-page:** Prefer **`<!-- strategy-page:start … -->`** blocks under **`## YYYY-MM`**, inside **`### Voice — …`** subsections, in [`voices/iri-institutional/thread.md`](voices/iri-institutional/thread.md) (same fence pattern as [strategy-page-template.md](../strategy-page-template.md)).
3. **Seam to main notebook:** Fold Iran-lane Judgment into main [`chapters/…/days.md`](../chapters/2026-04/days.md) as **seams**, not replacements for **`thread:`** or wire primaries.
4. **Split-both discipline:** **[`daily/`](chapters/2026-04/daily/)** holds **institutional tri-voice** consolidation; main **`days.md`** keeps the **full** arc — duplicate **only** what the seam needs, with explicit **tier** awareness.
5. **Month-gate ledger (not daily):** Under **`## YYYY-MM`** in [`voices/iri-institutional/thread.md`](voices/iri-institutional/thread.md) (**### Voice — …** each), keep **one** **`### Month ledger (YYYY-MM)`** block per office — ingest span, seam objects, refresh hooks. **Light metrics** (optional): word budget sanity, link depth to bundles, **seam** score to main notebook (operator judgment, not automation).

**Pages:** Optional standalone notes may live under [`pages/`](pages/) when a capture is not yet assigned to a voice folder.

**April 2026 chapter:** [`chapters/2026-04/`](chapters/2026-04/) — [`days.md`](chapters/2026-04/days.md), [`daily/`](chapters/2026-04/daily/), [`april-2026-slice-registry.md`](chapters/2026-04/april-2026-slice-registry.md), [`meta.md`](chapters/2026-04/meta.md).
