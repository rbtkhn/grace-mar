#!/usr/bin/env python3
"""
Jiang Compression Engine v1 — grace-mar

Compresses a work artifact into a small JSON pack under
research/external/work-jiang/compressions/. Uses users/<id>/seed/minimal-core.json
and reflection-proposals for founding intent / daily intention links.

Does not write RECURSION-GATE.md or SELF — use --print-gate-stub and paste manually
if a merge should be staged.

Usage:
  python3 scripts/jiang-compress.py
  python3 scripts/jiang-compress.py -u grace-mar --input /path/to/artifact.md
  python3 scripts/jiang-compress.py --print-gate-stub
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import DEFAULT_USER_ID

CATEGORIES = frozenset({"operational", "analytical", "synthesis", "other"})
WORK_JIANG = Path("research/external/work-jiang")
COMPRESSIONS = WORK_JIANG / "compressions"
SCHEMA_REL = "research/external/work-jiang/schemas/jiang-compression-v1.schema.json"


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def user_profile_dir(repo_root: Path, user_id: str) -> Path:
    return repo_root / "users" / user_id


def load_minimal_core(profile: Path) -> dict:
    path = profile / "seed" / "minimal-core.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def founding_intent_rel_path(user_id: str) -> str | None:
    rel = f"users/{user_id}/reflection-proposals/SEED-founding-intent.md"
    if (REPO_ROOT / rel).is_file():
        return rel
    return None


def slugify_title(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80] or "compression"


def run_compression_checklist() -> None:
    print(f"\n{Colors.BOLD}=== Compression checklist (operator) ==={Colors.ENDC}")
    print("(Not companion RECURSION-GATE — approve merges separately in recursion-gate.md.)\n")
    questions = [
        "Does this compression preserve core intention?",
        "Is every claim linkable to evidence, curiosity, or a cited path?",
        "Have you removed unnecessary operational noise?",
        "Is the output under ~1 page equivalent?",
    ]
    for q in questions:
        answer = input(f"{q} (y/N) ").strip().lower()
        if answer != "y":
            print(f"{Colors.FAIL}Checklist blocked. Aborting.{Colors.ENDC}")
            sys.exit(1)
    print(f"{Colors.OKGREEN}Checklist passed.{Colors.ENDC}\n")


def confirm(question: str) -> bool:
    answer = input(f"{question} (y/N) ").strip().lower()
    return answer == "y"


def read_raw_content(repo_root: Path, input_path: Path | None) -> str:
    if input_path is not None:
        p = input_path if input_path.is_absolute() else repo_root / input_path
        if not p.is_file():
            print(f"{Colors.FAIL}Input file not found: {p}{Colors.ENDC}", file=sys.stderr)
            sys.exit(1)
        return p.read_text(encoding="utf-8", errors="replace").strip()
    print("Paste artifact body; finish with a line containing only END (or Ctrl-D / empty line twice):")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        if not line.strip() and lines and not lines[-1].strip():
            lines.pop()
            break
        lines.append(line)
    return "\n".join(lines).strip()


def prompt_category() -> str:
    print("\nCategory: operational | analytical | synthesis | other")
    while True:
        c = input("> ").strip().lower()
        if c in CATEGORIES:
            return c
        print(f"{Colors.WARNING}Invalid. Choose one of: {', '.join(sorted(CATEGORIES))}{Colors.ENDC}")


def core_facts_referenced(minimal_core: dict, raw_content: str) -> list[str]:
    raw_lower = raw_content.lower()
    facts = minimal_core.get("coreFacts")
    if not isinstance(facts, list):
        return []
    out: list[str] = []
    for f in facts:
        if not isinstance(f, str) or not f.strip():
            continue
        words = f.split()[:3]
        if words and any(w.lower() in raw_lower for w in words if len(w) > 2):
            out.append(f)
    return out


def append_daily_intention_compression(
    repo_root: Path, user_id: str, title: str, one_sentence: str
) -> None:
    profile = user_profile_dir(repo_root, user_id)
    rp = profile / "reflection-proposals"
    rp.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    path = rp / f"DAILY-INTENTION-{today}.md"
    block = (
        f"\n\n## Jiang compression — {title}\n\n{one_sentence}\n"
    )
    if path.is_file():
        path.write_text(path.read_text(encoding="utf-8", errors="replace").rstrip() + block + "\n", encoding="utf-8")
    else:
        path.write_text(
            f"# Daily intention — {today}\n\n{block.lstrip()}\n\n"
            f"_Includes jiang-compress note (not part of the Record)._\n",
            encoding="utf-8",
        )
    print(f"{Colors.OKGREEN}Appended to{Colors.ENDC} {path.relative_to(repo_root)}")


def build_gate_stub(
    *,
    user_id: str,
    title: str,
    category: str,
    one_sentence: str,
    output_rel: str,
) -> str:
    return f"""### CANDIDATE-JIANG-COMPRESS (stub — edit id/status before use)

```yaml
status: pending
timestamp: {datetime.now(timezone.utc).date().isoformat()}
channel_key: operator:jiang-compress
source: jiang-compress.py gate stub — companion must approve before merge
mind_category: knowledge
signal_type: jiang_compression_followup
priority_score: 2
summary: {one_sentence[:200]}
profile_target: IX-A. KNOWLEDGE
suggested_entry: (derive from compression: {title} — category {category})
proposal_class: SELF_KNOWLEDGE_ADD
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
compression_artifact: {output_rel}
```

_Paste above into users/{user_id}/recursion-gate.md only if Record merge is intended; otherwise keep compression in work-jiang only._
"""


def write_compression_json(
    repo_root: Path,
    user_id: str,
    *,
    title: str,
    raw_content: str,
    category: str,
    one_sentence: str,
    actions: list[str],
    linked: list[str],
    minimal_core: dict,
    intent_link: str | None,
) -> Path:
    when = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    slug = slugify_title(title)
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_dir = repo_root / COMPRESSIONS
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}-{day}.json"

    excerpt = raw_content[:2000] if len(raw_content) > 2000 else raw_content
    payload: dict = {
        "schemaVersion": "1.0",
        "userId": user_id,
        "title": title,
        "category": category,
        "compressedAt": when,
        "sourceLength": len(raw_content),
        "coreFactsReferenced": core_facts_referenced(minimal_core, raw_content),
        "oneSentenceSummary": one_sentence,
        "executableNextActions": actions,
        "linkedEvidence": linked,
        "intentLink": intent_link,
        "sourceExcerpt": excerpt,
        "outputPath": str(out_path.relative_to(repo_root)),
    }
    text = json.dumps(payload, indent=2, ensure_ascii=True) + "\n"
    payload["compressedLength"] = len(text)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return out_path


def run_interactive(
    repo_root: Path,
    user_id: str,
    *,
    input_file: Path | None,
    print_gate_stub: bool,
    skip_checklist: bool,
) -> None:
    if not skip_checklist:
        run_compression_checklist()

    print(f"{Colors.HEADER}{Colors.BOLD}Jiang Compression Engine v1{Colors.ENDC}\n")

    profile = user_profile_dir(repo_root, user_id)
    minimal_core = load_minimal_core(profile)
    instance_name = str(minimal_core.get("instanceName") or user_id)
    print(f"Instance: {instance_name} (user id: {user_id})")

    title = input("\nShort title for this work artifact:\n> ").strip()
    if not title:
        print(f"{Colors.FAIL}Title required.{Colors.ENDC}")
        sys.exit(1)

    raw_content = read_raw_content(repo_root, input_file)
    if len(raw_content) < 50:
        print(f"{Colors.FAIL}Content too short (min ~50 chars).{Colors.ENDC}")
        sys.exit(1)

    print("\nOne-sentence summary of what this work achieved:")
    one_sentence = input("> ").strip()
    if not one_sentence:
        print(f"{Colors.FAIL}Summary required.{Colors.ENDC}")
        sys.exit(1)

    print("\n1–3 executable next actions (one per line, empty to finish):")
    actions: list[str] = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        actions.append(line)
        if len(actions) >= 10:
            break
    if not actions:
        print(f"{Colors.FAIL}At least one next action required.{Colors.ENDC}")
        sys.exit(1)

    print("\nEvidence / curiosity links (comma-separated paths, ACT/READ ids, or names):")
    linked_raw = input("> ").strip()
    linked = [x.strip() for x in linked_raw.split(",") if x.strip()]
    if not linked:
        print(f"{Colors.FAIL}At least one linkedEvidence entry required.{Colors.ENDC}")
        sys.exit(1)

    category = prompt_category()
    intent_link = founding_intent_rel_path(user_id)

    out_path = write_compression_json(
        repo_root,
        user_id,
        title=title,
        raw_content=raw_content,
        category=category,
        one_sentence=one_sentence,
        actions=actions,
        linked=linked,
        minimal_core=minimal_core,
        intent_link=intent_link,
    )
    rel_out = out_path.relative_to(repo_root)
    final_len = len(out_path.read_text(encoding="utf-8"))
    print(f"\n{Colors.OKGREEN}Compression complete.{Colors.ENDC}")
    print(f"  Saved: {rel_out}")
    print(f"  Source chars: {len(raw_content)} → JSON file: {final_len} chars")
    if final_len > 800:
        print(
            f"{Colors.WARNING}  JSON exceeds ~800 char target; trim summary/actions for density.{Colors.ENDC}"
        )

    if confirm("\nAppend summary to today's daily intention (reflection-proposals)?"):
        append_daily_intention_compression(repo_root, user_id, title, one_sentence)

    out_rel = str(rel_out).replace("\\", "/")
    if print_gate_stub or confirm("\nPrint RECURSION-GATE stub to stdout?"):
        print("\n--- gate stub ---\n")
        print(
            build_gate_stub(
                user_id=user_id,
                title=title,
                category=category,
                one_sentence=one_sentence,
                output_rel=out_rel,
            )
        )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-u",
        "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID,
        help="Fork id (users/<id>/)",
    )
    ap.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to artifact body file (repo-relative or absolute)",
    )
    ap.add_argument(
        "--print-gate-stub",
        action="store_true",
        help="After save, also print gate stub (skips prompt if combined with non-interactive)",
    )
    ap.add_argument(
        "--skip-checklist",
        action="store_true",
        help="Skip operator y/N checklist (for tests only)",
    )
    args = ap.parse_args()
    uid = args.user.strip()
    try:
        run_interactive(
            REPO_ROOT,
            uid,
            input_file=args.input,
            print_gate_stub=args.print_gate_stub,
            skip_checklist=args.skip_checklist,
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Interrupted.{Colors.ENDC}")
        sys.exit(130)


if __name__ == "__main__":
    main()
