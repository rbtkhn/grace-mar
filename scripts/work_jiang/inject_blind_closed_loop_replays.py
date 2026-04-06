#!/usr/bin/env python3
"""Inject ### Replay blocks into BLIND.md (documentation maintenance).

Does **not** validate prediction honesty. If replays describe **prefix-only** runs,
that must match how `gt-predict-*.md` was actually authored — this script does not check."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLIND = (
    ROOT
    / "research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND.md"
)

# (round_R, next_round_header_line_after_---) — replay body only, no trailing ---
REPLAYS: dict[int, str] = {
    6: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** `bundle --closed-loop` chain; prediction from `gt-prefix-6.md`.

#### Prediction packet (as filed, replay)

- **H1 (med):** U.S. as rule-writer — constitution, dollar, British inheritance.
- **H2 (low):** EU / multilateral without US center.
- **H3 (low):** Tech platforms as money rails.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Finance → named U.S. hegemon** confirmed; next default = **ideological rival system** lecture.

#### miss_taxonomy (replay)

—

""",
    7: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Closed-loop chain.

#### Prediction packet (as filed, replay)

- **H1 (med):** Rival ideological system (communism / socialism vs capitalist order).
- **H2 (low):** China–Taiwan flashpoint.
- **H3 (low):** Middle East oil introductory.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**U.S. rules → ideological mirror** confirmed; next **kinetic Mideast** high prior.

#### miss_taxonomy (replay)

—

""",
    8: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Closed-loop chain.

#### Prediction packet (as filed, replay)

- **H1 (med):** Hot war / US–Iran or Gulf.
- **H2 (low):** Ukraine / NATO–Russia.
- **H3 (low):** Sanctions-only.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Ideology stack → US–Iran kinetic** confirmed; next extract **named Law** from war.

#### miss_taxonomy (replay)

—

""",
    9: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Closed-loop chain.

#### Prediction packet (as filed, replay)

- **H1 (med):** First named Law of … (asymmetry).
- **H2 (low):** News update without law.
- **H3 (low):** Diplomacy / ceasefire only.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Law of asymmetry** installs; follow with **Law of escalation**.

#### miss_taxonomy (replay)

—

""",
    10: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** `bundle --trim-at-full-transcript` from K=10.

#### Prediction packet (as filed, replay)

- **H1 (med):** Law of escalation — nuclear taboo, religious sites.
- **H2 (low):** Law of signaling.
- **H3 (low):** US domestic cleavage only.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Escalation ladder** after asymmetry; next **eschatological convergence** arc.

#### miss_taxonomy (replay)

—

""",
    11: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle.

#### Prediction packet (as filed, replay)

- **H1 (med):** Eschatology / multi-tradition convergence.
- **H2 (low):** Second Law without religious convergence.
- **H3 (low):** Iran-only tactical.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Eschatology** after escalation; next **epistemic / elite network** (narrative maintenance).

#### miss_taxonomy (replay)

—

""",
    12: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle.

#### Prediction packet (as filed, replay)

- **H1 (med):** Epistemic / elite maintenance / narrative control.
- **H2 (low):** Fourth Law non-eschatology.
- **H3 (low):** Israel–Iran tactical only.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Epstein’s World** = narrative + operator-network sketch; next **Law of proximity** (domestic/nearest game).

#### miss_taxonomy (replay)

—

""",
    13: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle.

#### Prediction packet (as filed, replay)

- **H1 (med):** Law of proximity / domestic driver.
- **H2 (low):** Cyber / platform only.
- **H3 (low):** Mideast chapter without Law title.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**Proximity** after transnational narrative; next **macro order exhaustion** (“return of history”).

#### miss_taxonomy (replay)

—

""",
    14: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle.

#### Prediction packet (as filed, replay)

- **H1 (med):** Macro return of history / systemic transition.
- **H2 (low):** Regional war outcome / who benefits.
- **H3 (low):** AI governance pivot.

#### Scores

- **H1:** hit
- **H2:** partial (war + order embedded in macro decay thesis)
- **H3:** miss

#### Adjustment (mergeable)

**Return of History**; next **regional primacy / Pax thesis** (active war beneficiary).

#### miss_taxonomy (replay)

—

""",
    15: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle.

#### Prediction packet (as filed, replay)

- **H1 (med):** Regional primacy / Pax thesis — who benefits in active war.
- **H2 (low):** Commodity supercycle without war thesis.
- **H3 (low):** Diplomatic off-ramp.

#### Scores

- **H1:** hit
- **H2:** partial (commodities implied in war/endgame framing)
- **H3:** miss

#### Adjustment (mergeable)

**Pax Judaica Rising** caps regional-beneficiary arc; next **Great Reset / order rewrite** language.

#### miss_taxonomy (replay)

—

""",
    16: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle. gt-17 At a glance TBD in corpus — score mechanism cautiously.

#### Prediction packet (as filed, replay)

- **H1 (med):** Great reset / order exhaustion / rules rewrite.
- **H2 (low):** Leader cult without systems.
- **H3 (low):** China-only closing.

#### Scores

- **H1:** hit (title + reset frame; glance TBD)
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

**TBD glance:** down-rank mechanism confidence; **title** still anchors reset / order frame per appendix heuristic.

#### miss_taxonomy (replay)

TBD_glance_mechanism

""",
    17: """
### Replay (closed-loop calibration)

**Date:** 2026-04-06  
**Note:** Trimmed prefix bundle. Terminal in-repo round (predict gt-18).

#### Prediction packet (as filed, replay)

- **H1 (med):** Capstone — leadership + commodities + world order synthesis.
- **H2 (low):** Pure recap Q&A.
- **H3 (low):** Single-issue only.

#### Scores

- **H1:** hit
- **H2:** miss
- **H3:** miss

#### Adjustment (mergeable)

Volume IV in-repo chain **complete** for blind calibration; **gt-19** = live path or new file only.

#### miss_taxonomy (replay)

—

""",
}


def main() -> None:
    text = BLIND.read_text(encoding="utf-8")
    for r in range(6, 18):
        ep = r + 1
        replay = REPLAYS[r].strip("\n") + "\n"
        # Insert after first "### miss_taxonomy\n\n—" that precedes next round header
        marker_start = f"## Blind round {r} — predict gt-{ep:02d} (K={r})"
        marker_end = f"## Blind round {r + 1} — predict"
        if r == 17:
            marker_end = "## Chain summary"
        i0 = text.find(marker_start)
        if i0 == -1:
            sys.exit(f"missing section start {r}")
        i1 = text.find(marker_end, i0)
        if i1 == -1:
            sys.exit(f"missing section end after round {r}")
        chunk = text[i0:i1]
        anchor = "### miss_taxonomy\n\n—\n"
        j = chunk.rfind(anchor)
        if j == -1:
            sys.exit(f"miss_taxonomy anchor not found in round {r}")
        start_abs = i0 + j + len(anchor)
        after = text[start_abs:]
        if after.startswith("\n\n\n---\n\n"):
            cut = len("\n\n\n---\n\n")
        elif after.startswith("\n\n---\n\n"):
            cut = len("\n\n---\n\n")
        elif after.startswith("\n---\n\n"):
            cut = len("\n---\n\n")
        else:
            cut = 0
        # Avoid double-inject
        if "Replay (closed-loop calibration)" in text[i0:i1]:
            continue
        text = (
            text[:start_abs]
            + "\n\n"
            + replay
            + "\n---\n\n"
            + text[start_abs + cut :]
        )
    BLIND.write_text(text, encoding="utf-8")
    print("OK", BLIND, file=sys.stderr)


if __name__ == "__main__":
    main()
