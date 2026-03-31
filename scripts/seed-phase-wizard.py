#!/usr/bin/env python3
"""
Seed Phase Wizard — grace-mar adapted

Interactive operator bootstrap under users/<id>/ (reflection-proposals, seed/,
self-memory.md touches). Does **not** write SELF or EVIDENCE: durable facts enter only
through RECURSION-GATE and approval per docs/identity-fork-protocol.md.

Usage:
  python3 scripts/seed-phase-wizard.py
  python3 scripts/seed-phase-wizard.py --user my-fork
  GRACE_MAR_USER_ID=my-fork python3 scripts/seed-phase-wizard.py
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import CANONICAL_RECORD_FILES_REQUIRED, DEFAULT_USER_ID, resolve_self_memory_path


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ask(question: str, default: str = "") -> str:
    prompt = f"{question} "
    if default:
        prompt += f"[{default}] "
    answer = input(prompt).strip()
    return answer if answer else default


def confirm(question: str) -> bool:
    answer = input(f"{question} (y/N) ").strip().lower()
    return answer == "y"


def save_file(path: Path, content: str, *, repo_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"{Colors.OKGREEN}Created{Colors.ENDC} {path.relative_to(repo_root)}")


def user_profile_dir(repo_root: Path, user_id: str) -> Path:
    return repo_root / "users" / user_id


def canonical_record_ready(repo_root: Path, user_id: str) -> bool:
    root = repo_root / "users" / user_id
    if not root.is_dir():
        return False
    return all((root / name).is_file() for name in CANONICAL_RECORD_FILES_REQUIRED)


def append_good_morning_tone_memory(profile: Path, tone: str, *, when: str, repo_root: Path) -> None:
    mem = resolve_self_memory_path(profile)
    block = (
        f"\n\n### Seed wizard (operator)\n"
        f"*Written by seed-phase-wizard at {when} — ephemeral; not Record. "
        f"See docs/memory-template.md.*\n\n"
        f"- **Good morning tone:** {tone}\n"
    )
    if mem.exists():
        existing = mem.read_text(encoding="utf-8", errors="replace").rstrip()
        mem.write_text(existing + block + "\n", encoding="utf-8")
    else:
        mem.write_text(
            "# MEMORY — Self-memory (short / medium / long)\n\n"
            "> Not part of the Record. See docs/memory-template.md.\n\n"
            "## Short-term\n\n## Medium-term\n\n## Long-term\n"
            + block
            + "\n",
            encoding="utf-8",
        )
    print(f"{Colors.OKGREEN}Updated{Colors.ENDC} {mem.relative_to(repo_root)}")


def run_validators(repo: Path, user_id: str, *, require_proposal_class: bool) -> None:
    print(f"\n{Colors.OKBLUE}Running validators{Colors.ENDC}")
    miss = missing_canonical_record_files(user_id)
    if miss:
        print(
            f"{Colors.WARNING}Skipping integrity/governance: users/{user_id}/ not ready — "
            f"missing: {', '.join(miss)}{Colors.ENDC}"
        )
        print("Complete users/_template scaffold or copy from docs/self-template.md, then re-run.")
        return

    cmd_i = [
        sys.executable,
        str(repo / "scripts" / "validate-integrity.py"),
        "--user",
        user_id,
    ]
    if require_proposal_class:
        cmd_i.append("--require-proposal-class")
    r1 = subprocess.run(cmd_i, cwd=str(repo), capture_output=True, text=True)
    print(r1.stdout, end="")
    if r1.stderr:
        print(r1.stderr, end="", file=sys.stderr)
    tag = "OK" if r1.returncode == 0 else "FAILED"
    color = Colors.OKGREEN if r1.returncode == 0 else Colors.WARNING
    print(f"{color}validate-integrity.py: {tag} (exit {r1.returncode}){Colors.ENDC}")

    r2 = subprocess.run(
        [sys.executable, str(repo / "scripts" / "governance_checker.py")],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    print(r2.stdout, end="")
    if r2.stderr:
        print(r2.stderr, end="", file=sys.stderr)
    tag2 = "OK" if r2.returncode == 0 else "FAILED"
    color2 = Colors.OKGREEN if r2.returncode == 0 else Colors.WARNING
    print(f"{color2}governance_checker.py: {tag2} (exit {r2.returncode}){Colors.ENDC}")
    if r2.returncode != 0:
        print(
            f"{Colors.WARNING}If failures reference .venv or site-packages, run from a clean tree "
            f"or see scripts/governance_checker.py scope.{Colors.ENDC}"
        )


def run_wizard(
    *,
    repo_root: Path,
    user_id: str,
    require_proposal_class: bool,
) -> None:
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 50)
    print("     grace-mar  SEED PHASE WIZARD (instance paths)")
    print("=" * 50)
    print(f"{Colors.ENDC}")

    print(
        "Creates operator seed artifacts under users/<id>/. "
        "Does not merge into self.md or self-archive.md — use RECURSION-GATE.\n"
    )

    if not confirm("Are you at the repository root and is this the intended instance?"):
        print("Run from the grace-mar repo root.")
        sys.exit(1)

    instance = ask("Companion instance id (directory under users/)", user_id).strip() or user_id
    profile = user_profile_dir(repo_root, instance)
    profile.mkdir(parents=True, exist_ok=True)
    (profile / "reflection-proposals").mkdir(parents=True, exist_ok=True)
    (profile / "seed").mkdir(parents=True, exist_ok=True)

    when = _now_utc_iso()

    print(f"\n{Colors.BOLD}Step 1: Founding intention{Colors.ENDC}")
    print("What draws you to building this companion self? One paragraph; end with an empty line.")
    lines: list[str] = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    founding = "\n".join(lines).strip() or "(not provided)"
    save_file(
        profile / "reflection-proposals" / "SEED-founding-intent.md",
        f"# Founding intention\n\n{founding}\n\nSeeded (UTC): {when}\n",
        repo_root=repo_root,
    )

    print(f"\n{Colors.BOLD}Step 2: Good morning tone{Colors.ENDC}")
    tone = ask(
        "Preferred morning tone? (warm-direct / analytical-crisp / curious-playful / other)",
        "analytical-crisp",
    )
    append_good_morning_tone_memory(profile, tone, when=when, repo_root=repo_root)

    print(f"\n{Colors.BOLD}Step 3: Minimal core (JSON only){Colors.ENDC}")
    print("5–10 foundational facts the companion should eventually hold (one per line, empty to finish).")
    print(f"{Colors.WARNING}These are NOT merged into self.md here — stage LEARN/IX-A via the gate.{Colors.ENDC}")
    core_facts: list[str] = []
    while True:
        fact = input("> ").strip()
        if not fact:
            break
        core_facts.append(fact)

    minimal_core = {
        "instanceName": instance,
        "seededAt": when,
        "coreFacts": core_facts,
        "preferredProgressUnits": ["behavioral-change", "identity-coherence", "evidence-quality"],
        "note": "Promote facts through RECURSION-GATE; do not paste this file into self.md directly.",
    }
    save_file(
        profile / "seed" / "minimal-core.json",
        json.dumps(minimal_core, indent=2) + "\n",
        repo_root=repo_root,
    )

    print(f"\n{Colors.BOLD}Step 4: Initial curiosity{Colors.ENDC}")
    curiosity = ask("One open question or skill edge to explore recursively?")
    save_file(
        profile / "reflection-proposals" / "SEED-initial-sparks.md",
        f"# Initial curiosity sparks\n\n- {curiosity}\n\nSeeded (UTC): {when}\n",
        repo_root=repo_root,
    )

    print(f"\n{Colors.BOLD}Step 5: System tensions (optional){Colors.ENDC}")
    annotation = ask("Notes on tensions / mysteries (optional):", "")
    if annotation.strip():
        save_file(
            profile / "reflection-proposals" / "SEED-tensions-note.md",
            f"# Seed — tensions note\n\n{annotation.strip()}\n\nSeeded (UTC): {when}\n",
            repo_root=repo_root,
        )

    run_validators(repo_root, instance, require_proposal_class=require_proposal_class)

    marker = {
        "instanceName": instance,
        "seededAt": when,
        "wizardVersion": "1.0-grace-mar",
        "status": "SEED_PHASE_COMPLETED",
        "nextSteps": [
            "Stage knowledge via RECURSION-GATE; merge with process_approved_candidates.py after approval",
            "python3 scripts/harness_warmup.py -u " + instance + " --compact",
            "python3 scripts/good-morning-brief.py -u " + instance,
            "For full morning stack see .cursor/skills/coffee/SKILL.md",
            "Template sync: docs/merging-from-companion-self.md",
        ],
    }
    save_file(
        profile / "SEED-PHASE-COMPLETED.json",
        json.dumps(marker, indent=2) + "\n",
        repo_root=repo_root,
    )

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
    print("=" * 50)
    print("     SEED PHASE COMPLETED (operator artifacts only)")
    print("=" * 50)
    print(f"{Colors.ENDC}")
    print(f"Instance **{instance}** — artifacts under users/{instance}/.")
    print("Durable Record changes still require companion approval through the gate.\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "-u",
        "--user",
        default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER_ID).strip() or DEFAULT_USER_ID,
        help="Fork id (users/<id>/)",
    )
    ap.add_argument(
        "--require-proposal-class",
        action="store_true",
        help="Pass through to validate-integrity.py (matches CI strictness)",
    )
    args = ap.parse_args()
    try:
        run_wizard(
            repo_root=REPO_ROOT,
            user_id=args.user.strip(),
            require_proposal_class=args.require_proposal_class,
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Wizard interrupted.{Colors.ENDC}")
        sys.exit(130)


if __name__ == "__main__":
    main()
