"""Scan work-jiang lectures (+ analysis memos for geo lane); emit scored quote candidates (YAML).

Writes one file per lecture series so Geo-Strategy keyword bias does not drown Vol II/III:

- metadata/quote-candidates.yaml — Geo-Strategy only (backward compatible default for bootstrap / CI).
- metadata/quote-candidates-secret-history.yaml — Secret History.
- metadata/quote-candidates-civilization.yaml — Civilization.

Analysis memos are merged into the geo output only (same as historical behavior).
"""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_DIR / "lectures"
ANALYSIS = WORK_DIR / "analysis"
METADATA = WORK_DIR / "metadata"

# Geo-Strategy: book/analytical IR + empire + religion (original corpus).
KEYWORDS_GEO = re.compile(
    r"\b(empire|imperial|religion|religious|civilization|civilizational|"
    r"strategic|geopolit|Iran|dollar|petrodollar|Bretton|gold|financializ|"
    r"neoliberal|legitimacy|Zionism|evangelical|Russia|China|Ukraine|"
    r"asymmetr|sanction|alliance|narrative|formation|education|prediction|"
    r"psychohistory|polarization|sovereignty|Augustine|theology)\b",
    re.I,
)

# Secret History (Vol. III): evil arc, theology, secret societies, capital — distinct lexicon.
KEYWORDS_SECRET_HISTORY = re.compile(
    r"\b(evil|Frank|Sabbatai|Frankism|messiah|Messiah|church|Church|empire|"
    r"Satan|theolog|orthodox|papacy|Islam|Jewish|Jews|Christian|capital|"
    r"transnational|illuminati|freemason|conspiracy|civilization|surveillance|"
    r"psycholog|Freud|Marx|individual|liberal|Darwin)\b",
    re.I,
)

# Civilization (Vol. II): history-of-thought and empires — broader literary/philosophical signals.
KEYWORDS_CIVILIZATION = re.compile(
    r"\b(civilization|empire|Rome|Greek|Homer|Dante|Augustine|Constantine|"
    r"reformation|revolution|modernism|bureaucracy|meritocr|collapse|Bronze|"
    r"religion|philosoph|theolog|narrative|legitimacy|sovereignty|Mandate|Heaven)\b",
    re.I,
)

MAX_CANDIDATES_GEO = 400
MAX_CANDIDATES_SERIES = 250
MIN_LEN = 48
MAX_LEN = 520

GENERATOR = "scripts/work_jiang/extract_quote_candidates.py"


def score_line(text: str, keywords: re.Pattern[str]) -> float:
    t = text.strip()
    if len(t) < MIN_LEN or len(t) > MAX_LEN:
        return 0.0
    s = 0.0
    s += min(len(t) / 200.0, 2.0)
    s += len(keywords.findall(t)) * 0.85
    if "?" in t:
        s += 0.3
    if re.search(r"\b(okay|so |which means|the idea is)\b", t, re.I):
        s += 0.15
    return round(s, 3)


def iter_body_lines(path: Path) -> list[tuple[int, str]]:
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = 0
    if raw_lines and raw_lines[0].strip() == "---":
        for j in range(1, len(raw_lines)):
            if raw_lines[j].strip() == "---":
                start = j + 1
                break

    out: list[tuple[int, str]] = []
    for i in range(start, len(raw_lines)):
        raw = raw_lines[i]
        line_no = i + 1
        stripped = raw.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith("```"):
            continue
        if not stripped or stripped.startswith("|"):
            continue
        if stripped.startswith("**") and stripped.endswith("**") and len(stripped) < 80:
            continue
        out.append((line_no, raw))
    return out


def normalize_key(text: str) -> str:
    return hashlib.sha256(re.sub(r"\s+", " ", text.strip().lower()).encode()).hexdigest()[:16]


def collect_for_files(
    paths: list[Path],
    keywords: re.Pattern[str],
    max_candidates: int,
) -> list[dict]:
    seen_norm: set[str] = set()
    candidates: list[dict] = []

    for path in paths:
        rel = str(path.relative_to(WORK_DIR))
        try:
            numbered = iter_body_lines(path)
        except OSError:
            continue
        for line_no, raw in numbered:
            text = raw.strip()
            if not text:
                continue
            sc = score_line(text, keywords)
            if sc <= 0:
                continue
            nk = normalize_key(text)
            if nk in seen_norm:
                continue
            seen_norm.add(nk)
            candidates.append(
                {
                    "path": rel,
                    "line_number": line_no,
                    "text": text,
                    "score": sc,
                }
            )

    candidates.sort(key=lambda x: (-x["score"], x["path"], x["line_number"]))
    return candidates[:max_candidates]


def write_candidates(out_path: Path, *, series: str, candidates: list[dict]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "generated_by": GENERATOR,
        "series": series,
        "candidates": candidates,
    }
    with out_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"Wrote {len(candidates)} candidates to {out_path.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--geo-only",
        action="store_true",
        help="Only regenerate metadata/quote-candidates.yaml (skip secret-history and civilization files).",
    )
    args = ap.parse_args()

    geo_lectures = sorted(LECTURES.glob("geo-strategy-*.md"))
    sh_lectures = sorted(LECTURES.glob("secret-history-*.md"))
    civ_lectures = sorted(LECTURES.glob("civilization-*.md"))

    analysis_files: list[Path] = []
    for p in sorted(ANALYSIS.glob("*.md")):
        if p.name == ".gitkeep":
            continue
        analysis_files.append(p)

    # Geo: lectures + all analysis memos (preserves prior behavior).
    geo_paths = list(geo_lectures)
    geo_paths.extend(analysis_files)
    geo_cand = collect_for_files(geo_paths, KEYWORDS_GEO, MAX_CANDIDATES_GEO)
    write_candidates(METADATA / "quote-candidates.yaml", series="geo-strategy", candidates=geo_cand)

    if args.geo_only:
        return 0

    sh_cand = collect_for_files(sh_lectures, KEYWORDS_SECRET_HISTORY, MAX_CANDIDATES_SERIES)
    write_candidates(
        METADATA / "quote-candidates-secret-history.yaml",
        series="secret-history",
        candidates=sh_cand,
    )

    civ_cand = collect_for_files(civ_lectures, KEYWORDS_CIVILIZATION, MAX_CANDIDATES_SERIES)
    write_candidates(
        METADATA / "quote-candidates-civilization.yaml",
        series="civilization",
        candidates=civ_cand,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
