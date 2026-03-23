"""Scan geo-strategy lectures + analysis memos; emit scored quote candidates (YAML).

Only `lectures/geo-strategy-*.md` and `analysis/*.md` under work-jiang (not other lecture lanes).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LECTURES = WORK_DIR / "lectures"
ANALYSIS = WORK_DIR / "analysis"
OUT = WORK_DIR / "metadata" / "quote-candidates.yaml"

# Higher signal for book/analytical lines (geo-strategy corpus).
KEYWORDS = re.compile(
    r"\b(empire|imperial|religion|religious|civilization|civilizational|"
    r"strategic|geopolit|Iran|dollar|petrodollar|Bretton|gold|financializ|"
    r"neoliberal|legitimacy|Zionism|evangelical|Russia|China|Ukraine|"
    r"asymmetr|sanction|alliance|narrative|formation|education|prediction|"
    r"psychohistory|polarization|sovereignty|Augustine|theology)\b",
    re.I,
)

MAX_CANDIDATES = 400
MIN_LEN = 48
MAX_LEN = 520


def score_line(text: str) -> float:
    t = text.strip()
    if len(t) < MIN_LEN or len(t) > MAX_LEN:
        return 0.0
    s = 0.0
    s += min(len(t) / 200.0, 2.0)
    s += len(KEYWORDS.findall(t)) * 0.85
    if "?" in t:
        s += 0.3
    if re.search(r"\b(okay|so |which means|the idea is)\b", t, re.I):
        s += 0.15  # lecture cadence but still contentful
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


def main() -> int:
    files: list[Path] = []
    files.extend(sorted(LECTURES.glob("geo-strategy-*.md")))
    for p in sorted(ANALYSIS.glob("*.md")):
        if p.name == ".gitkeep":
            continue
        files.append(p)

    seen_norm: set[str] = set()
    candidates: list[dict] = []

    for path in files:
        rel = str(path.relative_to(WORK_DIR))
        try:
            numbered = iter_body_lines(path)
        except OSError:
            continue
        for line_no, raw in numbered:
            text = raw.strip()
            if not text:
                continue
            sc = score_line(text)
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
    candidates = candidates[:MAX_CANDIDATES]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"generated_by": "scripts/work_jiang/extract_quote_candidates.py", "candidates": candidates},
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
    print(f"Wrote {len(candidates)} candidates to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
