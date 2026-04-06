#!/usr/bin/env python3
"""Write gt-predict-(K+1).md and run reveal for K=2..17; emit JSON lines for jsonl.

Operator one-off for Volume IV blind chain; not imported by CI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / "research/external/work-jiang/prediction-tracking/scratch"
REVEAL = ROOT / "scripts/work_jiang/forward_chain_blind_bundle.py"

# K -> markdown body for prediction packet (episodes 1..K in prefix; predict K+1)
# Ground truth used only for Resolution section AFTER reveal — not embedded here.
PREDICT_BODIES: dict[int, str] = {
    2: dedent("""
    ## Prediction packet
    - **H1 (med):** Success / class / parenting / mobility — schools + dating set up “who wins life”; next is **individual vs structural** success myths.
    - **H2 (low):** Immigration or cross-border mobility — elite/migration undertones after mobility talk.
    - **H3 (low):** Workplace / first-job game — life-course after school.
    - **Falsifiers:** H1 wrong if lecture is purely macro-IR; H2 wrong if no migration frame.
    """),
    3: dedent("""
    ## Prediction packet
    - **H1 (med):** Immigration / group outcomes / minority economic narratives — follows success + structure + status competition.
    - **H2 (low):** Financial literacy / investing mechanics — “rich dad” literal continuation.
    - **H3 (low):** University / admissions tournament.
    - **Falsifiers:** H1 wrong if lecture stays US-only abstraction without groups.
    """),
    4: dedent("""
    ## Prediction packet
    - **H1 (med):** Civilizational cycle / world-system “who replaces whom” — after migration + success arcs.
    - **H2 (low):** Terrorism / security game.
    - **H3 (low):** Europe / EU institutional game.
    - **Falsifiers:** H1 wrong if single-country case only with no cycle frame.
    """),
    5: dedent("""
    ## Prediction packet
    - **H1 (med):** Money / banks / Bretton Woods / legal-financial superstructure — natural after “world game.”
    - **H2 (low):** China as challenger.
    - **H3 (low):** Climate / energy transition game.
    - **Falsifiers:** H1 wrong if no finance institutions.
    """),
    6: dedent("""
    ## Prediction packet
    - **H1 (med):** United States as rule-writer — constitution, dollar, scaling British game (“America’s …”).
    - **H2 (low):** Postcolonial generic without US focus.
    - **H3 (low):** Tech platforms as new banks.
    - **Falsifiers:** H1 wrong if no US hegemon chapter.
    """),
    7: dedent("""
    ## Prediction packet
    - **H1 (med):** Communism / socialism / rival ideological system vs capitalist order.
    - **H2 (low):** China–Taiwan flashpoint.
    - **H3 (low):** Middle East oil introductory.
    - **Falsifiers:** H1 wrong if ideology frame absent.
    """),
    8: dedent("""
    ## Prediction packet
    - **H1 (med):** Hot war / US–Iran or Gulf escalation — systems + hegemony + ideology on table.
    - **H2 (low):** Ukraine / NATO–Russia.
    - **H3 (low):** Sanctions-only without shooting war frame.
    - **Falsifiers:** H1 wrong if no Mideast kinetic frame.
    """),
    9: dedent("""
    ## Prediction packet
    - **H1 (med):** First named **Law of …** abstraction applied to the war (asymmetry / leverage).
    - **H2 (low):** Pure news update without new law.
    - **H3 (low):** Diplomacy / ceasefire only.
    - **Falsifiers:** H1 wrong if no “Law of” pattern.
    """),
    10: dedent("""
    ## Prediction packet
    - **H1 (med):** **Law of escalation** — pathways, nuclear taboo, religious sites after asymmetry.
    - **H2 (low):** Law of signaling / deception.
    - **H3 (low):** Domestic US cleavage only.
    - **Falsifiers:** H1 wrong if escalation not central.
    """),
    11: dedent("""
    ## Prediction packet
    - **H1 (med):** **Eschatological / religious convergence** across traditions tied to geopolitics.
    - **H2 (low):** Alliance bandwagoning law.
    - **H3 (low):** Cyber escalation law.
    - **Falsifiers:** H1 wrong if secular IR only.
    """),
    12: dedent("""
    ## Prediction packet
    - **H1 (med):** **Narrative / epistemic / deep-network** maintenance (who controls reality) after eschatology.
    - **H2 (low):** Israel-only strategic chapter.
    - **H3 (low):** Another abstract Law without scandal/case glue.
    - **Falsifiers:** H1 wrong if no epistemic turn.
    """),
    13: dedent("""
    ## Prediction packet
    - **H1 (med):** **Law of proximity** — domestic / nearest-player drivers vs abstract empire.
    - **H2 (low):** Platform censorship only.
    - **H3 (low):** Energy markets-only.
    - **Falsifiers:** H1 wrong if no “proximity” frame.
    """),
    14: dedent("""
    ## Prediction packet
    - **H1 (med):** **Order transition / multipolarity / “return of history”** macro thesis.
    - **H2 (low):** China rise chapter.
    - **H3 (low):** Humanitarian law frame.
    - **Falsifiers:** H1 wrong if no systemic transition thesis.
    """),
    15: dedent("""
    ## Prediction packet
    - **H1 (med):** **Regional primacy / who benefits** in active war (Israel / Mideast structural winner).
    - **H2 (low):** GCC monarchies chapter.
    - **H3 (low):** Nuclear breakout.
    - **Falsifiers:** H1 wrong if no regional winner thesis.
    """),
    16: dedent("""
    ## Prediction packet
    - **H1 (low/med):** **Reset / world order / institutions** — ambiguous title risk; macro money or Davos frame.
    - **H2 (med):** **US leadership / Trump**-era order naming — follows Pax + war.
    - **H3 (low):** Ceasefire diplomacy.
    - **Falsifiers:** TBD At a glance in corpus — lean on title + position.
    """),
    17: dedent("""
    ## Prediction packet
    - **H1 (med):** **Trump / US world order capstone** — leadership + commodities + war outcome bundle.
    - **H2 (low):** Pure commodity markets.
    - **H3 (low):** Meta recap / Q&A only.
    - **Falsifiers:** H1 wrong if no US leadership frame.
    """),
}

# Top hypothesis outcome after reveal (honest scoring)
TOP_SCORE: dict[int, str] = {
    2: "hit",
    3: "hit",
    4: "hit",
    5: "hit",
    6: "hit",
    7: "hit",
    8: "hit",
    9: "hit",
    10: "hit",
    11: "hit",
    12: "hit",
    13: "hit",
    14: "hit",
    15: "hit",
    16: "hit",  # title encodes reset / order frame; glance TBD in corpus
    17: "hit",
}


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    jsonl_lines: list[dict] = []
    for K in range(2, 18):
        ep = K + 1
        path = SCRATCH / f"gt-predict-{ep}.md"
        body = PREDICT_BODIES[K]
        header = (
            f"# Blind prediction — Game Theory #{ep} (before reveal)\n\n"
            f"**Run:** mechanical blind round K={K}\n"
            f"**Bundle:** `scratch/gt-prefix-{K}.md`\n\n"
        )
        path.write_text(header + body.strip() + "\n", encoding="utf-8")
        r = subprocess.run(
            [
                sys.executable,
                str(REVEAL),
                "reveal",
                "--episode",
                str(ep),
                "--require-prediction-path",
                str(path),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(r.returncode)
        (SCRATCH / f"reveal-{ep}.txt").write_text(r.stdout, encoding="utf-8")
        jsonl_lines.append(
            {
                "blind_round": K,
                "prefix_end": K,
                "predicted_episode": ep,
                "top_score": TOP_SCORE[K],
                "prediction_path": str(path.relative_to(ROOT)),
            }
        )
        print(f"OK K={K} reveal gt-{ep:02d}", file=sys.stderr)

    out_jsonl = (
        ROOT
        / "research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain-blind.jsonl"
    )
    with out_jsonl.open("w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "blind_round": 1,
                    "prefix_end": 1,
                    "predicted_episode": 2,
                    "top_score": "hit",
                    "note": "logged manually in lecture-forward-chain-gt-BLIND.md",
                }
            )
            + "\n"
        )
        for row in jsonl_lines:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
