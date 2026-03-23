#!/usr/bin/env python3
"""
Map validated lecture analysis JSON to staging JSONL lines (operator review before registry append).

Does not write production predictions.jsonl / divergences.jsonl unless --write is passed
and operator confirms workflow. Default: print staging path and row counts.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
_WJ_SCRIPTS = Path(__file__).resolve().parent
if str(_WJ_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_WJ_SCRIPTS))

# Import validator by path
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "vaj",
    Path(__file__).resolve().parent / "validate_lecture_analysis_json.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_mod)
validate_obj = _mod.validate_obj


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path, help="Validated -analysis.json path")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Append staging lines to prediction-tracking/staging/ and divergence-tracking/staging/",
    )
    args = parser.parse_args()

    raw = args.json_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    errors = validate_obj(data)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    from extractors.registry import instantiate_extractor

    stem = args.json_path.stem
    src = data.get("source") or {}
    vid = src.get("video_id") or ""
    sid = src.get("source_id") or ""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    ex = instantiate_extractor(series_id=src.get("series") or None, source_id=sid or None)

    pred_rows = []
    for i, p in enumerate(data.get("predictions") or []):
        row = ex.map_prediction_to_staging(p)
        pred_rows.append(
            {
                "staging_id": f"stg-{stem}-{i}",
                "source_analysis_json": str(args.json_path.relative_to(ROOT)),
                "video_id": vid,
                "source_id": sid,
                "ingested_at_utc": ts,
                "extractor": ex.series_id,
                "row": row,
            }
        )

    div_rows = []
    for i, d in enumerate(data.get("divergences_from_prior") or []):
        drow = ex.map_divergence_to_staging(d)
        div_rows.append(
            {
                "staging_id": f"stg-{stem}-div-{i}",
                "source_analysis_json": str(args.json_path.relative_to(ROOT)),
                "video_id": vid,
                "source_id": sid,
                "ingested_at_utc": ts,
                "extractor": ex.series_id,
                "row": drow,
            }
        )

    print(f"predictions staging rows: {len(pred_rows)}")
    print(f"divergences staging rows: {len(div_rows)}")

    if args.write:
        pd = WORK_DIR / "prediction-tracking" / "staging"
        dd = WORK_DIR / "divergence-tracking" / "staging"
        pd.mkdir(parents=True, exist_ok=True)
        dd.mkdir(parents=True, exist_ok=True)
        pj = pd / f"{stem}-staging.jsonl"
        dj = dd / f"{stem}-staging.jsonl"
        with pj.open("w", encoding="utf-8") as f:
            for r in pred_rows:
                f.write(json.dumps(r, ensure_ascii=True) + "\n")
        with dj.open("w", encoding="utf-8") as f:
            for r in div_rows:
                f.write(json.dumps(r, ensure_ascii=True) + "\n")
        print(f"Wrote {pj}")
        print(f"Wrote {dj}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
