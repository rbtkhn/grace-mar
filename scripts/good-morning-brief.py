#!/usr/bin/env python3
"""
Good Morning Brief — grace-mar adapted

Short operator ritual: greeting, light context from seed/memory/archive tail,
optional daily intention (reflection-proposals, not Record). For gate state and
pending candidates, prefer: python3 scripts/harness_warmup.py -u <id>

Usage:
  python3 scripts/good-morning-brief.py
  python3 scripts/good-morning-brief.py -u grace-mar
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import CANONICAL_EVIDENCE_BASENAME, DEFAULT_USER_ID


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _tail_text(path: Path, *, max_chars: int = 1200) -> str:
    if not path.is_file():
        return ""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return raw[-max_chars:] if len(raw) > max_chars else raw


def _detect_tone_from_memory(content: str) -> str:
    if "warm-direct" in content:
        return "warm-direct"
    if "curious-playful" in content:
        return "curious-playful"
    if "analytical-crisp" in content:
        return "analytical-crisp"
    return "analytical-crisp"


def user_profile_dir(repo_root: Path, user_id: str) -> Path:
    return repo_root / "users" / user_id


def _yesterday_intention(profile: Path, today: date) -> str | None:
    y = today - timedelta(days=1)
    rp = profile / "reflection-proposals" / f"DAILY-INTENTION-{y.isoformat()}.md"
    if not rp.is_file():
        return None
    try:
        t = rp.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None
    return (t[:220] + "…") if len(t) > 220 else t


def _recent_signal_line(profile: Path) -> str | None:
    ev = profile / CANONICAL_EVIDENCE_BASENAME
    tail = _tail_text(ev, max_chars=2500)
    if not tail.strip():
        return None
    for line in reversed(tail.splitlines()):
        stripped = line.strip()
        if re.search(r"\b(ACT|READ|LEARN)-\d{4}\b", stripped):
            return stripped[:120] + ("…" if len(stripped) > 120 else "")
    return None


def ask(question: str, default: str = "") -> str:
    prompt = f"{question} "
    if default:
        prompt += f"[{default}] "
    answer = input(prompt).strip()
    return answer if answer else default


def save_daily_intention(profile: Path, today: date, text: str) -> Path:
    profile.mkdir(parents=True, exist_ok=True)
    rp_dir = profile / "reflection-proposals"
    rp_dir.mkdir(parents=True, exist_ok=True)
    path = rp_dir / f"DAILY-INTENTION-{today.isoformat()}.md"
    body = (
        f"# Daily intention — {today.isoformat()}\n\n{text}\n\n"
        f"_Written during good-morning-brief (not part of the Record; not merged via gate)._"
    )
    path.write_text(body + "\n", encoding="utf-8")
    return path


def suggest_harness_warmup(repo: Path, user_id: str) -> None:
    print(
        f"\n{Colors.OKBLUE}For RECURSION-GATE / session tail / full warmup:{Colors.ENDC}\n"
        f"  python3 scripts/harness_warmup.py -u {user_id} --compact\n"
    )
    if ask("Run harness_warmup now? (y/N)", "n").lower() == "y":
        subprocess.run(
            [sys.executable, str(repo / "scripts" / "harness_warmup.py"), "-u", user_id, "--compact"],
            cwd=str(repo),
        )


def run_brief(*, repo_root: Path, user_id: str, skip_warmup_prompt: bool) -> None:
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 50)
    print("               GOOD MORNING BRIEF")
    print("=" * 50)
    print(f"{Colors.ENDC}")

    today = date.today()
    today_s = today.isoformat()
    profile = user_profile_dir(repo_root, user_id)

    minimal_core = _load_json(profile / "seed" / "minimal-core.json")
    instance_name = user_id
    if isinstance(minimal_core, dict):
        instance_name = str(minimal_core.get("instanceName") or user_id)

    tone = "analytical-crisp"
    mem_path = profile / "memory.md"
    if mem_path.is_file():
        try:
            mem_text = mem_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            mem_text = ""
        tone = _detect_tone_from_memory(mem_text)

    greetings = {
        "warm-direct": f"Good morning, {instance_name}. Ready to sharpen thinking today?",
        "analytical-crisp": f"Morning, {instance_name}. Recursion depth: active. Where next?",
        "curious-playful": f"Good morning! What thread from yesterday is still alive for you?",
    }
    greeting = greetings.get(tone, greetings["analytical-crisp"])
    print(f"\n{Colors.OKBLUE}{greeting}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Today's snapshot ({today_s}){Colors.ENDC}")
    y_intent = _yesterday_intention(profile, today)
    if y_intent:
        print(f"  Yesterday's intention (reflection): {y_intent}")
    sig = _recent_signal_line(profile)
    if sig:
        print(f"  Recent evidence tail: {sig}")
    if minimal_core and isinstance(minimal_core.get("coreFacts"), list) and minimal_core["coreFacts"]:
        fact = random.choice(minimal_core["coreFacts"])
        print(f"  Core seed anchor: {fact}")

    sess_tail = _tail_text(profile / "session-log.md", max_chars=800)
    if sess_tail.strip():
        last_lines = [ln for ln in sess_tail.splitlines() if ln.strip()][-2:]
        if last_lines:
            print(f"  Session log (tail): {last_lines[-1][:100]}…")

    print(f"\n{Colors.BOLD}Intention{Colors.ENDC}")
    print("One thing to understand or create better today? (empty to skip)")
    daily = input("\n> ").strip()
    if daily:
        out = save_daily_intention(profile, today, daily)
        print(f"{Colors.OKGREEN}Saved{Colors.ENDC} {out.relative_to(repo_root)}")

    print(f"\n{Colors.BOLD}Suggested session shapes{Colors.ENDC}")
    options = [
        "Deep work — one skill domain",
        "Analyst — review gate + recent evidence",
        "Curiosity — one question from reflection-proposals/",
        "Light capture — stage candidates, short reflection",
    ]
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    choice = ask("\nWhich fits today? (number or free text)", "1")
    print(f"{Colors.OKGREEN}Noted: {choice}{Colors.ENDC}")

    seed_marker = profile / "SEED-PHASE-COMPLETED.json"
    print(f"\n{Colors.BOLD}Status{Colors.ENDC}")
    if seed_marker.is_file():
        print("  Seed phase marker: present")
    else:
        print(f"{Colors.WARNING}  Seed phase: no SEED-PHASE-COMPLETED.json — run scripts/seed-phase-wizard.py{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Sovereign merge{Colors.ENDC}")
    print("  Durable truth: RECURSION-GATE → approval → process_approved_candidates.py")
    print(f"  {Colors.OKBLUE}Stay within intention. Protect boundaries.{Colors.ENDC}\n")

    if not skip_warmup_prompt:
        suggest_harness_warmup(repo_root, user_id)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-u",
        "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID,
    )
    ap.add_argument(
        "--skip-warmup-prompt",
        action="store_true",
        help="Do not offer to run harness_warmup (for non-interactive tests)",
    )
    args = ap.parse_args()
    try:
        run_brief(
            repo_root=REPO_ROOT,
            user_id=args.user.strip(),
            skip_warmup_prompt=args.skip_warmup_prompt,
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Brief interrupted.{Colors.ENDC}")
        sys.exit(130)


if __name__ == "__main__":
    main()
