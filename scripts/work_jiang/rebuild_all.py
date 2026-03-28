"""Run full work-jiang rebuild: registry, renders, validators. Exit non-zero on first failure."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STEPS = [
    ["python3", "scripts/work_jiang/build_source_registry.py"],
    ["python3", "scripts/work_jiang/link_supporting_registries.py"],
    ["python3", "scripts/work_jiang/extract_concept_mentions.py"],
    ["python3", "scripts/work_jiang/render_concept_dictionary.py"],
    ["python3", "scripts/work_jiang/link_claims_to_thesis.py"],
    ["python3", "scripts/work_jiang/render_claims_overview.py"],
    ["python3", "scripts/work_jiang/render_book_architecture.py"],
    ["python3", "scripts/work_jiang/render_thesis_map.py"],
    ["python3", "scripts/work_jiang/render_chapter_queue.py"],
    ["python3", "scripts/work_jiang/build_all_evidence_packs.py"],
    ["python3", "scripts/work_jiang/render_status_dashboard.py"],
    ["python3", "scripts/work_jiang/extract_quote_candidates.py"],
    ["python3", "scripts/work_jiang/render_quote_bank.py"],
    ["python3", "scripts/work_jiang/link_quotes_to_chapters.py"],
    ["python3", "scripts/work_jiang/build_quote_index.py"],
    ["python3", "scripts/work_jiang/render_analysis_backlog.py"],
    ["python3", "scripts/work_jiang/render_counter_readings.py"],
    ["python3", "scripts/work_jiang/link_counter_readings.py"],
    ["python3", "scripts/work_jiang/render_intellectual_chronology.py"],
    ["python3", "scripts/work_jiang/validate_work_jiang.py", "--require-analysis-frontmatter"],
    ["python3", "scripts/work_jiang/validate_argument_layer.py"],
    ["python3", "scripts/work_jiang/validate_comparative_layer.py"],
    ["python3", "scripts/work_jiang/validate_patterns_registry.py"],
]


def main() -> int:
    for i, cmd in enumerate(STEPS):
        print(f"[{i + 1}/{len(STEPS)}] {' '.join(cmd)}", flush=True)
        r = subprocess.run(cmd, cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {' '.join(cmd)}", file=sys.stderr)
            return r.returncode
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
