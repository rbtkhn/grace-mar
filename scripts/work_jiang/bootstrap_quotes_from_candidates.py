"""One-time / operator tool: build metadata/quotes.yaml from quote-candidates + sources.

Curators should edit quotes.yaml by hand after bootstrap. Not run in default CI."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"

VERIFY_MARKERS = ("[verify:", "[unclear]")


def contains_verify_markers(text: str) -> bool:
    return any(marker in text for marker in VERIFY_MARKERS)


def infer_quote_status(text_clean: str, verification: str | None = None) -> str:
    if contains_verify_markers(text_clean):
        return "cleaned"
    if verification == "verified_against_audio":
        return "verified"
    return "cleaned"


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
    ap = argparse.ArgumentParser(
        description="Bootstrap metadata/quotes.yaml from a quote-candidates*.yaml file.",
    )
    ap.add_argument("--count", type=int, default=55)
    ap.add_argument(
        "--candidates",
        type=Path,
        default=None,
        help=(
            "Path to quote candidates YAML (default: metadata/quote-candidates.yaml). "
            "Use metadata/quote-candidates-secret-history.yaml or "
            "metadata/quote-candidates-civilization.yaml for other volumes; "
            "review and merge into quotes.yaml by hand if you already have geo quotes."
        ),
    )
    args = ap.parse_args()

    cand_path: Path = args.candidates or (WORK_DIR / "metadata" / "quote-candidates.yaml")
    if args.candidates and not cand_path.is_absolute():
        cwd_p = Path.cwd() / cand_path
        wj_p = WORK_DIR / cand_path
        if cwd_p.is_file():
            cand_path = cwd_p.resolve()
        elif wj_p.is_file():
            cand_path = wj_p.resolve()
        else:
            cand_path = cand_path.resolve()

    sources = load_yaml(WORK_DIR / "metadata" / "sources.yaml").get("sources") or []
    cand_doc = load_yaml(cand_path)
    candidates = cand_doc.get("candidates") or []
    if not candidates:
        try:
            disp = str(cand_path.relative_to(ROOT))
        except ValueError:
            disp = str(cand_path)
        print(f"No candidates in {disp}", file=sys.stderr)
        return 1

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
        text_raw = text
        text_clean = re.sub(r"\s+", " ", text_raw).strip()
        picked.append(
            {
                "quote_id": qid,
                "source_id": sid,
                "analysis_id": aid,
                "text": text_clean,
                "text_raw": text_raw,
                "text_clean": text_clean,
                "transcript_source": "raw",
                "status": infer_quote_status(text_clean),
                "verification": "unverified",
                "quote_type": "lecture" if "lectures/" in rel else "analysis",
                "themes": [],
                "concept_ids": guess_concepts(text_clean),
                "chapter_ids": chapters,
                "rank": min(5, max(1, int(round(c.get("score") or 1)))),
                "speaker": "Jiang Xueqin",
                "notes": "ASR/transcript line; verify phrasing before scholarly citation. Auto-bootstrapped as cleaned, not draft_safe.",
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
            text_raw = text
            text_clean = re.sub(r"\s+", " ", text_raw).strip()
            if any((p.get("text_clean") or p.get("text")) == text_clean for p in picked):
                continue

            picked.append(
                {
                    "quote_id": f"q-{len(picked) + 1:04d}",
                    "source_id": sid,
                    "analysis_id": aid,
                    "text": text_clean,
                    "text_raw": text_raw,
                    "text_clean": text_clean,
                    "transcript_source": "raw",
                    "status": infer_quote_status(text_clean),
                    "verification": "unverified",
                    "quote_type": "lecture" if "lectures/" in rel else "analysis",
                    "themes": [],
                    "concept_ids": guess_concepts(text_clean),
                    "chapter_ids": ["ch03"],
                    "rank": min(5, max(1, int(round(c.get("score") or 1)))),
                    "speaker": "Jiang Xueqin",
                    "notes": "ASR/transcript line; verify phrasing before scholarly citation. Auto-bootstrapped as cleaned, not draft_safe.",
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
