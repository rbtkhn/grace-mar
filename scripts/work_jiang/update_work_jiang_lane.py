"""Refresh `status` in users/grace-mar/work-jiang.md Instance work context (YAML) from metadata."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
LANE = ROOT / "users" / "grace-mar" / "work-jiang.md"


def lane_status(arch: dict, queue: list) -> str:
    chapters = (arch.get("book") or {}).get("chapters") or []
    if any((c.get("status") or "") == "draft_in_progress" for c in chapters):
        return "DRAFTING"
    if len(chapters) >= 3 and (arch.get("project") or {}).get("thesis_one_sentence"):
        return "OUTLINE_ACTIVE"
    src_ct = len((WORK_DIR / "lectures").glob("geo-strategy-*.md"))
    ana_ct = len(list((WORK_DIR / "analysis").glob("*.md")))
    if src_ct >= 8 and ana_ct >= 6:
        return "RESEARCH_ACTIVE"
    return "SEED"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply update to work-jiang.md",
    )
    args = parser.parse_args()

    arch = yaml.safe_load(
        (WORK_DIR / "metadata" / "book-architecture.yaml").read_text(encoding="utf-8")
    )
    cq = yaml.safe_load(
        (WORK_DIR / "metadata" / "chapter-queue.yaml").read_text(encoding="utf-8")
    )
    q = cq.get("chapter_queue") or []
    new_status = lane_status(arch, q)

    text = LANE.read_text(encoding="utf-8")
    # Primary: work_jiang.context.yaml WORK_JIANG_CONTEXT_V1
    pattern = re.compile(
        r"(<!--\s*work_jiang\.context\.yaml\s+WORK_JIANG_CONTEXT_V1\s*-->\s*\n```yaml\n)(status: )(\w+)",
    )
    legacy = re.compile(
        r"(<!--\s*WORK-JIANG-(?:CONTAINER|HEARTBEAT)-START\s*-->\s*\n```yaml\n)(status: )(\w+)",
    )
    if pattern.search(text):

        def repl(m: re.Match) -> str:
            return f"{m.group(1)}{m.group(2)}{new_status}"

        new_text = pattern.sub(repl, text, count=1)
    elif legacy.search(text):

        def repl_leg(m: re.Match) -> str:
            return f"{m.group(1)}{m.group(2)}{new_status}"

        new_text = legacy.sub(repl_leg, text, count=1)
    else:
        print(
            "No instance work context markers found; add "
            "<!-- work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 --> ... "
            "<!-- /work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 --> "
            "around the yaml fence in work-jiang.md (see skills-modularity §2a)."
        )
        return 1

    if args.write:
        LANE.write_text(new_text, encoding="utf-8")
        print(f"Set instance work context status to {new_status}")
    else:
        print(f"Would set instance work context status to {new_status} (use --write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
