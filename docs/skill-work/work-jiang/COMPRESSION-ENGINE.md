# Jiang Compression Engine v1

**Lane:** operator research — [work-jiang](../../../users/grace-mar/work-jiang.md) / `research/external/work-jiang/`. **Not** Record until merged through **RECURSION-GATE**.

## Purpose

Turn a bulky work artifact (analysis, handoff, planning notes) into a **small JSON pack** that declares:

- **Category** — `operational` | `analytical` | `synthesis` | `other`
- **One-sentence outcome**
- **1–3 executable next actions**
- **Evidence links** (paths, ACT/READ ids, doc names)
- Optional tie to **seed** context (`users/<id>/seed/minimal-core.json`) and **founding intent** (`reflection-proposals/SEED-founding-intent.md`)

This fights **layer drift** and **truth density** by forcing a labeled, linkable summary before more execution.

**Alpha-style analogy:** Alpha uses a hard **~90% mastery** bar before unlocking the next lesson; Jiang compress asks for **one-sentence clarity**, **linked evidence**, and **next actions** before treating a work artifact as ready to build on — operator discipline parallel to “no Swiss cheese before advancing.” See [alpha-mastery-adaptation.md](../../alpha-mastery-adaptation.md) and [bloom-mastery-adaptation.md](../../bloom-mastery-adaptation.md) (Bloom / 2 Sigma layer).

## Commands

```bash
python3 scripts/jiang-compress.py -u grace-mar
python3 scripts/jiang-compress.py -u grace-mar --input research/external/work-jiang/STATUS.md
python3 scripts/jiang-compress.py -u grace-mar --print-gate-stub   # always print gate stub at end
```

## Checklist vs gate

The script opens with an **operator compression checklist** (y/N). That is **discipline**, not the companion **RECURSION-GATE**. If the compression should change SELF/EVIDENCE, use the printed **gate stub** (or write your own candidate) in `users/<id>/recursion-gate.md` and approve per [identity-fork-protocol.md](../../identity-fork-protocol.md).

## Outputs

| Output | Location |
|--------|----------|
| Compression JSON | `research/external/work-jiang/compressions/<slug>-YYYYMMDD.json` |
| Schema | `research/external/work-jiang/schemas/jiang-compression-v1.schema.json` |
| Daily intention note (optional) | `users/<id>/reflection-proposals/DAILY-INTENTION-YYYY-MM-DD.md` (append) |

**Sprint bundles (future):** `research/external/work-jiang/sprints/` — see README there.

## Related

- [compressions/README.md](../../../research/external/work-jiang/compressions/README.md)
- [seed-phase-wizard.md](../../seed-phase-wizard.md) / [good-morning-brief.py](../../../scripts/good-morning-brief.py)
- [work-jiang-feature-checklist](../../../.cursor/skills/work-jiang-feature-checklist/SKILL.md)
