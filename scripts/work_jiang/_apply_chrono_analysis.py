#!/usr/bin/env python3
"""One-off: restore analysis memos from /tmp and apply chronological renumbering."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/external/work-jiang/analysis"

# (temp_path relative name, target filename)
FILES = [
    ("wj-XRk5VSEzJ4Y-interviews-01-analysis.md", "XRk5VSEzJ4Y-interviews-01-analysis.md"),
    ("wj-GSSIm9xNRAE-interviews-02-analysis.md", "GSSIm9xNRAE-interviews-02-analysis.md"),
    ("wj-ORyCS0r2Tpg-interviews-03-analysis.md", "ORyCS0r2Tpg-interviews-03-analysis.md"),
    ("wj-H5lCJ0D4DpY-interviews-04-analysis.md", "H5lCJ0D4DpY-interviews-04-analysis.md"),
    ("wj-uHIdRgFypNo-interviews-05-analysis.md", "uHIdRgFypNo-interviews-05-analysis.md"),
    ("wj-80jUKe0blAQ-interviews-06-analysis.md", "80jUKe0blAQ-interviews-06-analysis.md"),
    ("wj-4Ql24Z8SIeE-interviews-07-analysis.md", "4Ql24Z8SIeE-interviews-07-analysis.md"),
    ("wj-0rIgZD-tk3s-interviews-08-analysis.md", "0rIgZD-tk3s-interviews-08-analysis.md"),
    ("wj-o1DElACHNRo-interviews-09-analysis.md", "o1DElACHNRo-interviews-09-analysis.md"),
    ("wj-2K2nQsTTjQE-interviews-10-analysis.md", "2K2nQsTTjQE-interviews-10-analysis.md"),
]

# Ordered replacements (old substring -> new) — longest first where needed.
TEXT_REPL = [
    # analysis memo filenames (old registry names from committed content)
    ("XRk5VSEzJ4Y-interviews-09-analysis.md", "XRk5VSEzJ4Y-interviews-01-analysis.md"),
    ("GSSIm9xNRAE-interviews-01-analysis.md", "GSSIm9xNRAE-interviews-02-analysis.md"),
    ("ORyCS0r2Tpg-interviews-02-analysis.md", "ORyCS0r2Tpg-interviews-03-analysis.md"),
    ("H5lCJ0D4DpY-interviews-03-analysis.md", "H5lCJ0D4DpY-interviews-04-analysis.md"),
    ("uHIdRgFypNo-interviews-04-analysis.md", "uHIdRgFypNo-interviews-05-analysis.md"),
    ("80jUKe0blAQ-interviews-05-analysis.md", "80jUKe0blAQ-interviews-06-analysis.md"),
    ("4Ql24Z8SIeE-interviews-08-analysis.md", "4Ql24Z8SIeE-interviews-07-analysis.md"),
    ("0rIgZD-tk3s-interviews-06-analysis.md", "0rIgZD-tk3s-interviews-08-analysis.md"),
    ("o1DElACHNRo-interviews-10-analysis.md", "o1DElACHNRo-interviews-09-analysis.md"),
    ("2K2nQsTTjQE-interviews-07-analysis.md", "2K2nQsTTjQE-interviews-10-analysis.md"),
    # lecture paths (specific slugs)
    ("interviews-09-cyrus-janssen-world-is-about-to-change.md", "interviews-01-cyrus-janssen-world-is-about-to-change.md"),
    ("interviews-01-glenn-diesen-west-civilizational-collapse.md", "interviews-02-glenn-diesen-west-civilizational-collapse.md"),
    ("interviews-02-glenn-diesen-predictions-2026-empire-rivalry-collapse.md", "interviews-03-glenn-diesen-predictions-2026-empire-rivalry-collapse.md"),
    ("interviews-03-danny-haiphong-predictions-2026-trump-iran-empire-collapse.md", "interviews-04-danny-haiphong-predictions-2026-trump-iran-empire-collapse.md"),
    ("interviews-04-dimitri-lascaris-trump-iran-davos-canada-china.md", "interviews-05-dimitri-lascaris-trump-iran-davos-canada-china.md"),
    ("interviews-05-glenn-diesen-great-power-wars-new-world-order.md", "interviews-06-glenn-diesen-great-power-wars-new-world-order.md"),
    ("interviews-08-breaking-points-krystal-saagar-us-will-lose-iran-war.md", "interviews-07-breaking-points-krystal-saagar-us-will-lose-iran-war.md"),
    ("interviews-06-nima-iran-war-watershed-middle-east-forever.md", "interviews-08-nima-iran-war-watershed-middle-east-forever.md"),
    ("interviews-10-sneako-end-of-the-world.md", "interviews-09-sneako-end-of-the-world.md"),
    ("interviews-07-tucker-carlson-iran-war-and-global-order.md", "interviews-10-tucker-carlson-iran-war-and-global-order.md"),
]

# Per-file identity: (target filename fragment, analysis_id, episode int, interview_num int, title rest after colon)
IDENT = [
    ("XRk5VSEzJ4Y-interviews-01", "vi-01", 1, 1, "Cyrus Janssen — The World Is About to Change"),
    ("GSSIm9xNRAE-interviews-02", "vi-02", 2, 2, "Glenn Diesen — The West's Civilizational Collapse"),
    ("ORyCS0r2Tpg-interviews-03", "vi-03", 3, 3, "Glenn Diesen — Predictions for 2026 (Empire, Rivalry & Collapse)"),
    ("H5lCJ0D4DpY-interviews-04", "vi-04", 4, 4, "Danny Haiphong — Predictions for 2026: Trump, Iran & Empire Collapse"),
    ("uHIdRgFypNo-interviews-05", "vi-05", 5, 5, "Dimitri Lascaris — Trump’s War on Iran, Davos, Canada–China"),
    ("80jUKe0blAQ-interviews-06", "vi-06", 6, 6, "Glenn Diesen — Great Power Wars Over a New World Order"),
    ("4Ql24Z8SIeE-interviews-07", "vi-07", 7, 7, "Breaking Points — US WILL LOSE Iran War"),
    ("0rIgZD-tk3s-interviews-08", "vi-08", 8, 8, "Nima (Dialogue Works) — The Iran War: The Watershed Moment That Changed the Middle East Forever"),
    ("o1DElACHNRo-interviews-09", "vi-09", 9, 9, "SNEAKO — The End of the World"),
    ("2K2nQsTTjQE-interviews-10", "vi-10", 10, 10, "Tucker Carlson — Iran War and Global Order"),
]


def patch_identity(text: str, interview_num: int, aid: str, ep: int, title: str) -> str:
    text = re.sub(r"^analysis_id: vi-\d+$", f"analysis_id: {aid}", text, flags=re.M)
    text = re.sub(r"^source_id: vi-\d+$", f"source_id: {aid}", text, flags=re.M)
    text = re.sub(r"^episode: \d+$", f"episode: {ep}", text, flags=re.M)
    text = re.sub(
        r"^# Analysis — Interviews #\d+: .+$",
        f"# Analysis — Interviews #{interview_num}: {title}",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^- \*\*series / episode:\*\* Predictive History · Volume VI — Interviews #\d+$",
        f"- **series / episode:** Predictive History · Volume VI — Interviews #{interview_num}",
        text,
        flags=re.M,
    )
    return text


def main() -> None:
    tmp = Path("/tmp")
    for temp_name, dest_name in FILES:
        src = tmp / temp_name
        text = src.read_text(encoding="utf-8")
        for old, new in TEXT_REPL:
            text = text.replace(old, new)
        key = dest_name.replace("-analysis.md", "")
        row = next((r for r in IDENT if r[0] == key), None)
        if not row:
            raise SystemExit(f"Missing IDENT for {key}")
        _, aid, ep, num, title = row
        text = patch_identity(text, num, aid, ep, title)
        (OUT / dest_name).write_text(text, encoding="utf-8")
        print("wrote", dest_name)


if __name__ == "__main__":
    main()
