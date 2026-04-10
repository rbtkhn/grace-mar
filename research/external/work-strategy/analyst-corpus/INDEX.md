# Analyst corpus — INDEX

**Rules:** One row per **transcript file** (or per **logical episode** if you split files). **transcript_path** is **repo-root-relative**. Empty cells use `—`.

**Column definitions**

| Column | Required | Meaning |
|--------|----------|---------|
| `analyst_slug` | yes | Stable id: `theodore-postol`, `robert-pape`, … |
| `display_name` | yes | Human label for sorting and prose. |
| `transcript_path` | yes | Path to the markdown (usually under `research/external/work-strategy/transcripts/`). |
| `episode_title` | yes | Short title; can match the `#` heading in the file. |
| `source_url` | no | Watch or listen URL when known. |
| `published` | no | Air / publish date (**ISO `YYYY-MM-DD`** if possible). |
| `ingested` | yes | Date the file landed in-repo (**ISO**). |
| `topics` | no | Semicolon-separated tags: `iran; nuclear; bmd; ukraine`. |
| `digest_one_line` | no | Single-line thesis for search skimming. |
| `verify_focus` | no | What to check before ship-facing copy (comma-separated hints). |
| `notes_path` | no | Optional `analysts/<slug>/…` or `docs/skill-work/...` stub. |

---

## Active rows (newest first)

| analyst_slug | display_name | transcript_path | episode_title | source_url | published | ingested | topics | digest_one_line | verify_focus | notes_path |
|--------------|--------------|-----------------|---------------|------------|-----------|----------|--------|-----------------|--------------|------------|
| crooke | Alastair Crooke | research/external/work-strategy/transcripts/2026-04-10-davis-crooke-centcom-iran-hormuz-islamabad.md | Davis × Crooke — CENTCOM vs “empowerment,” Hormuz, 10-point, Islamabad | — | 2026-04-10 | 2026-04-10 | iran; hormuz; lebanon; islamabad; centcom; vance; israel | Briefing claims vs attrition read; Netanyahu/Lebanon; Vance clip; toll/Kharg math | All numbers; CJCS/Pentagon; Hebrew press; Ben-David | — |
| mercouris | Alexander Mercouris | research/external/work-strategy/transcripts/mercouris-2026-04-10-good-friday-hormuz-lebanon-islamabad.md | Good Friday 2026 — Hormuz, Lebanon, Islamabad, FT oil, GCC / Russia / Ukraine | — | 2026-04-10 | 2026-04-10 | iran; hormuz; lebanon; gcc; islamabad; ft; ukraine; russia | Fragile truce vs Lebanon kinetics; Hormuz + FT/Hochstein; Islamabad table; pivot-year close | FT figures; Iranian doc; battlefield lines; inflation %; primary cites | — |
| mearsheimer | John Mearsheimer | research/external/work-strategy/transcripts/2026-04-10-diesen-mearsheimer-iran-ceasefire-truth-social.md | Diesen × Mearsheimer — Iran ceasefire, Apr 6 tweets, Hormuz / NATO / Ukraine | https://www.youtube.com/watch?v=H2K3qDshr70 | 2026-04-10 | 2026-04-10 | iran; trump; hormuz; lebanon; nato; ukraine; vance; multipolarity; rationality | Two-tweet read as desperation + 10-point basis; Hormuz/Lebanon linkage; economy driver; speaker assertions | NYT bases story; aircraft-loss day; CFR historians poll; all quantitative claims | — |
| tucker-carlson | Tucker Carlson | research/external/work-strategy/transcripts/2026-04-02-tucker-carlson-trump-end-global-american-empire.md | End of global American empire — Hormuz / unipolarity / Holy Week | https://www.youtube.com/watch?v=GyYy-QmxttU | 2026-04-02 | 2026-04-01 | iran; hormuz; unipolarity; china; gcc; protestant-leadership; hemisphere | Who reopens Hormuz = power; US “take the lead” read as capacity limit; Graham/Esther vs gospel frame | Trump clip quotes; troop claims; GCC strike/FDI figures; Canada-Mexico claims | — |
| theodore-postol | Theodore Postol | research/external/work-strategy/transcripts/theodore-postol-2025-03-striving-nuclear-armageddon-able-archer-diesen.md | Striving for Nuclear Armageddon — Able Archer 1983 | https://www.youtube.com/watch?v=2GbJg8bb4Dg | ~2025-03 | 2026-04-02 | able-archer; nuclear; inf; germany-2026; abm; poseidon; escalation | Exercise ladder to general war by day 5; fire/fallout/blast; Germany 2026 = nuclear must; INF reinstatement | Declassified exercise record vs this retelling; Chernobyl multiples; Poseidon yield; policy claims | — |
| theodore-postol | Theodore Postol | research/external/work-strategy/transcripts/theodore-postol-2026-03-irans-missiles-drones-underestimated.md | Iran's missiles & drones underestimated (YouTube) | — | ~2026-03 | 2026-04-02 | iran; israel; drones; bmd; tunnels; starlink; rusi | Tunnels + drone radar-kill + cheap precision; ~5% BM intercept claim; RUSI depletion table | RUSI primary; intercept rates; Starlink policy; radar strike dates; cost figures | — |
| mercouris | Alexander Mercouris | research/external/work-strategy/transcripts/mercouris-2026-03-30-israel-iran-china-g7-ukraine.md | Israel AD / China / G7 / Ukraine monologue | — | 2026-03-30 | 2026-03-30 | iran; israel; ad; ukraine; china; oil | Haaretz-sourced leak-through narrative; Hormuz/Brent stress; GT editorial frame | battle claims; intercept rates; Kuwait strike reports | — |
| larry-johnson | Larry Johnson | research/external/work-strategy/transcripts/larry-johnson-2026-03-30-full-escalation-yemen-hezbollah.md | Yemen / Hezbollah / escalation (digest) | — | 2026-03-30 | 2026-03-30 | yemen; hezbollah; escalation | (see file Perceiver) | primary sources for ops claims | — |
| parsi-davis | Parsi & Davis | research/external/work-strategy/transcripts/no-threat-can-force-iran-surrender-parsi-davis.md | No threat can force Iran to surrender | — | — | — | iran; diplomacy | (see file) | — | — |

---

## Template row (copy below the header row)

```markdown
| theodore-postol | Theodore Postol | research/external/work-strategy/transcripts/YYYY-MM-DD-iran-nuclear-deterrent-diesen.md | Iran nuclear deterrent (Diesen) | https://… | YYYY-MM-DD | YYYY-MM-DD | iran; nuclear; latency; israel | HEU breakout + mass-fire scenario; deterrence to Israeli first use | IAEA kg; cascade count; scenario vs doctrine | research/external/work-strategy/analysts/theodore-postol/RECURRING-MOVES.md |
```

*(Remove the code fence when pasting into the table; keep pipe alignment roughly tidy.)*

---

## Optional: machine-readable export

If you later want scripts to consume this index, add a sibling **`index.tsv`** with the same columns (tab-separated, header row). Do not delete this markdown INDEX; treat TSV as derived if you automate.
