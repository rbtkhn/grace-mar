"""One-time / operator tool: build metadata/quotes.yaml from quote-candidates + sources.

Curators should edit quotes.yaml by hand after bootstrap. Not run in default CI.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"

# ch03 = analysis chapter (empire + religion + strategic imagination); keep regex narrower than generic "empire".
CH03 = re.compile(
    r"(strategic imagination|psychohistory|Christian Zion|Zionism|dispensational|"
    r"Sunni|Shia|evangelical|premillennial|theolog|Augustine|religious legitimacy|"
    r"Second American Civil|polarization.*civil|Putin.*Soul|War for the Soul|"
    r"Iran Trap|invad.*Iran|petrodollar|Saudi.*Iran|Iran.*Saudi|Middle East.*rival|"
    r"imperial hubris|hubris.*empire|Breton woods|Bretton)",
    re.I,
)
CH02 = re.compile(
    r"\b(civilization|civilizational|formation|education|narrative|school|"
    r"elite capture|financializ|manufacturing|workers|civil society)\b",
    re.I,
)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def map_path_to_source(rel_path: str, sources: list[dict]) -> tuple[str | None, str | None]:
    """Return (source_id, analysis_id or None). analysis_id set when path is analysis memo."""
    for s in sources:
        lp = s.get("lecture_path") or ""
        ap = s.get("analysis_path") or ""
        if rel_path.replace("\\", "/") == ap.replace("\\", "/"):
            return s.get("source_id"), s.get("source_id")
        if rel_path.replace("\\", "/") == lp.replace("\\", "/"):
            return s.get("source_id"), None
    return None, None


def guess_concepts(text: str) -> list[str]:
    t = text.lower()
    out: list[str] = []
    pairs = [
        ("empire-order", r"\bempire|imperial|Pax|hegemon"),
        ("financialization-empire", r"financializ|Wall Street|speculat"),
        ("strategic-imagination", r"strategic imagination|nested game|scenario"),
        ("christian-zionism", r"Zionism|evangelical|dispensational"),
        ("religious-legitimacy", r"religion|theolog|Augustine|legitimacy"),
        ("iran-strategy-matrix", r"Iran.*matrix|matrix.*Iran"),
        ("empire-hubris", r"hubris|overextend"),
        ("asymmetrical-warfare", r"asymmetr"),
        ("saudi-iran-axis", r"Saudi|Iran"),
        ("putinism-soul", r"Putin|Russia"),
        ("second-civil-war", r"civil war|polarization"),
        ("psychohistory-metaphor", r"psychohistory|machine learning pedagogy"),
        ("education-narrative", r"education|school|narrative"),
        ("civ-formation", r"civilization|formation"),
        ("middle-east-alliance", r"Middle East|alliance"),
    ]
    for cid, pat in pairs:
        if re.search(pat, t, re.I):
            if cid not in out:
                out.append(cid)
    return out[:4]


def guess_chapters(text: str) -> list[str]:
    if CH03.search(text):
        return ["ch03"]
    if CH02.search(text):
        return ["ch02"]
    return ["ch01"]


def skip_prose(text: str) -> bool:
    s = text.strip()
    if s.startswith("**Topic:**"):
        return True
    if s.startswith("`") and s.count("`") >= 6:
        return True
    if s.startswith("**") and "**Empire** **death**" in s:
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=55)
    args = ap.parse_args()

    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources") or []
    cand_doc = load_yaml(WORK_DIR / "metadata" / "quote-candidates.yaml")
    candidates = cand_doc.get("candidates") or []

    picked: list[dict] = []
    ch03_count = 0
    for c in candidates:
        if len(picked) >= args.count:
            break
        text = (c.get("text") or "").strip()
        if skip_prose(text):
            continue
        rel = c.get("path") or ""
        sid, aid = map_path_to_source(rel, sources)
        if not sid:
            continue
        chapters = guess_chapters(text)
        if "ch03" in chapters:
            ch03_count += 1

        qid = f"q-{len(picked) + 1:04d}"
        picked.append(
            {
                "quote_id": qid,
                "source_id": sid,
                "analysis_id": aid,
                "text": text,
                "quote_type": "lecture" if "lectures/" in rel else "analysis",
                "themes": [],
                "concept_ids": guess_concepts(text),
                "chapter_ids": chapters,
                "rank": min(5, max(1, int(round(c.get("score") or 1)))),
                "speaker": "Jiang Xueqin",
                "notes": "ASR/transcript line; verify phrasing before scholarly citation.",
            }
        )

    # Ensure ch03 has at least 5 quotes
    if ch03_count < 5:
        for c in candidates:
            if ch03_count >= 5:
                break
            text = (c.get("text") or "").strip()
            if skip_prose(text):
                continue
            if not CH03.search(text):
                continue
            rel = c.get("path") or ""
            sid, aid = map_path_to_source(rel, sources)
            if not sid:
                continue
            if any(p.get("text") == text for p in picked):
                continue
            picked.append(
                {
                    "quote_id": f"q-{len(picked) + 1:04d}",
                    "source_id": sid,
                    "analysis_id": aid,
                    "text": text,
                    "quote_type": "lecture" if "lectures/" in rel else "analysis",
                    "themes": [],
                    "concept_ids": guess_concepts(text),
                    "chapter_ids": ["ch03"],
                    "rank": min(5, max(1, int(round(c.get("score") or 1)))),
                    "speaker": "Jiang Xueqin",
                    "notes": "ASR/transcript line; verify phrasing before scholarly citation.",
                }
            )
            ch03_count += 1

    out_path = WORK_DIR / "metadata" / "quotes.yaml"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("# Curated quotation bank (source of truth). Bootstrap: bootstrap_quotes_from_candidates.py\n")
        yaml.safe_dump({"quotes": picked}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Wrote {len(picked)} quotes to {out_path.relative_to(ROOT)} (ch03-tagged lines: {ch03_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
