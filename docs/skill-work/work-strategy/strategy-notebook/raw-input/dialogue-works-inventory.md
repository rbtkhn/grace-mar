# Dialogue Works — raw-input inventory
<!-- word_count: ~420 -->

**Purpose:** Single tracker for **Dialogue Works** (host **Nima Alkhorshid**) captures already present under **`raw-input/`**, grouped by how strongly the file identifies the show. **WORK only** — not Record.

**Last audited:** 2026-04-28 — grep for `Dialogue Works`, `show: Dialogue Works`, `Nima Alkhorshid`, `Dialogue Works (Nima)`, and filename `*nima*` / `*dialogue-works*` under `raw-input/`.

**Routing reminder:** For symmetric expert mirroring, same-episode ingests should carry **`thread:<guest>`** plus **`thread:alkorshid`** where host prompts matter — see [`experts/alkorshid/profile.md`](../experts/alkorshid/profile.md).

---

## Tier A — Confirmed (standalone artifact)

Full markdown files with **`show: Dialogue Works`** (and host/guest) in YAML; treat as canonical Dialogue Works corpus rows in this tree.

| pub_date | Path (under `raw-input/`) | Guest | `thread` / routing | source_url | Notes |
|----------|-----------------------------|-------|--------------------|------------|--------|
| 2026-04-28 | `2026-04-28/transcript-marandi-dialogue-works-trump-plan-dead-after-strike-2026-04-28.md` | Seyed Mohammad Marandi | `thread: marandi` | *(pin canonical `watch?v=` — do not conflate with Judging Freedom same-day row)* | Full cleaned operator transcript; `source_note` in YAML flags prior inbox duplicate URL bug. |
| 2026-04-27 | `2026-04-27/transcript-baud-dialogue-works-nima-2026-04-27.md` | Col. Jacques Baud | `thread: baud` | https://www.youtube.com/watch?v=iZ5xSBYxxyQ | Operator-cleaned transcript; title in body matches frontmatter. |
| 2026-04-24 | `2026-04-24/transcript-nima-freeman-israel-agenda-collapsing-2026-04-24.md` | Amb. Chas W. Freeman | `thread: freeman` | *(pin canonical watch URL in frontmatter when known)* | `source_note` asks to pin canonical YouTube URL; `title_slug` present. |
| 2026-04-21 | `2026-04-21/transcript-marandi-blockade-trump-nima-2026-04-21.md` | Seyed Mohammad Marandi | `thread_expert: marandi` | *(pin canonical watch URL when known)* | Opening voice date in transcript may differ from `pub_date`; see file `source_note`. |

---

## Tier B — Likely (lane transcript stubs, not full standalone SSOT)

These files are **`kind: transcript`** blocks **`source_path` → expert `transcript.md`** routing dumps. They **name** Dialogue Works/Nima in **cold lines** but do **not** carry **`show: Dialogue Works`** in the file-level YAML. Use for grep/registry; prefer **Tier A** files (or pinned **`watch?v=`**) when you need a single canonical verbatim for an episode.

| pub_date | Path (under `raw-input/`) | Expert lane stub | Dialogue Works signal in body | Notes |
|----------|-----------------------------|------------------|----------------------------------|--------|
| 2026-04-17 | `2026-04-17/transcript-freeman.md` | `thread: freeman` | `Amb. Charles Freeman (Dialogue Works (Nima), …)` | YouTube URL in line may still be **`TBD-`** placeholder — verify before cite-grade. |
| 2026-04-18 | `2026-04-18/transcript-freeman.md` | `thread: freeman` | Same pattern + separate **Freeman × Diesen** line (not Dialogue Works — Glenn Diesen show) | Do **not** conflate **Dialogue Works** line with **Diesen** joint episode on same date section. |
| 2026-04-18 | `2026-04-18/transcript-marandi.md` | `thread: marandi` | `Show \| cold: **Dialogue Works** (**Nima**) + Seyed Mohammad Marandi` | Placeholder **`TBD-pin-`** URL in stub — pin canonical watch URL when known. |

---

## Tier C — Not Dialogue Works (disambiguation)

- **The Grayzone**, **Judging Freedom**, **The Duran**, **Deep Dive** (Daniel Davis), etc., are **distinct** outlets — see cold-line tags in inbox and expert threads. Do not merge with Dialogue Works rows without an explicit source line.

---

## Maintenance

When adding a new Dialogue Works capture:

1. Prefer **`show: Dialogue Works`**, **`host:`**, **`guest:`**, **`pub_date`**, **`source_url:`**, and **`thread:`** (guest) in frontmatter per [raw-input README](README.md) § File template.
2. Append a row to **Tier A** (or move a stub from **Tier B** when promoted to standalone file).
3. In [daily-strategy-inbox.md](../daily-strategy-inbox.md), add a **second** paste-ready line with **`thread:alkorshid`** immediately after the guest **`thread:<guest>`** row (**same** episode URL / raw-input pointer).
4. Re-run a quick grep: `rg -l "Dialogue Works|show:\\s*Dialogue Works" raw-input` from `strategy-notebook/`.
