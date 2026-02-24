#!/usr/bin/env python3
"""
Process approved pipeline candidates: merge into SELF, EVIDENCE, prompt; run export_prp; optionally push.

Usage:
    python scripts/process_approved_candidates.py           # dry run
    python scripts/process_approved_candidates.py --apply   # perform merge
    python scripts/process_approved_candidates.py --apply --push  # merge + git push

Requires repo root as cwd. For merge-from-Telegram: run this after approving in Telegram.
"""

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_ID = "pilot-001"
PROFILE_DIR = REPO_ROOT / "users" / USER_ID
PENDING_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
SELF_PATH = PROFILE_DIR / "SELF.md"
EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"
PROMPT_PATH = REPO_ROOT / "bot" / "prompt.py"
PRP_PATH = REPO_ROOT / "grace-mar-abby-prp.txt"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _yaml_get(block: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+?)(?:\n|$)", block, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"\'')


def _next_id(content: str, prefix: str) -> str:
    ids = [int(m.group(1)) for m in re.finditer(rf"{prefix}-(\d+)", content)]
    n = max(ids, default=0) + 1
    return f"{prefix}-{n:04d}"


def get_approved_in_candidates() -> list[dict]:
    """Return approved candidates from the Candidates section (not yet processed)."""
    content = _read(PENDING_PATH)
    if not content:
        return []
    # Split at ## Processed — we only want candidates before that
    parts = content.split("## Processed")
    candidates_section = parts[0] if parts else ""
    approved: list[dict] = []
    for m in re.finditer(r"### (CANDIDATE-\d+)(?:\s*\([^)]*\))?\s*\n```yaml\n(.*?)```", candidates_section, re.DOTALL):
        block = m.group(2)
        if "status: approved" not in block:
            continue
        approved.append({
            "id": m.group(1),
            "block": block,
            "full_match": m.group(0),
            "summary": _yaml_get(block, "summary") or "(no summary)",
            "mind_category": _yaml_get(block, "mind_category") or "knowledge",
            "profile_target": _yaml_get(block, "profile_target") or "IX-A. KNOWLEDGE",
            "suggested_entry": _yaml_get(block, "suggested_entry") or "",
            "prompt_addition": _yaml_get(block, "prompt_addition") or "none",
        })
    return approved


def merge_candidate(c: dict, dry_run: bool) -> bool:
    """Merge one candidate. Returns True if ok."""
    if dry_run:
        print(f"  [DRY RUN] would merge {c['id']}: {c['summary'][:60]}...")
        return True

    today = datetime.now().strftime("%Y-%m-%d")
    evidence_content = _read(EVIDENCE_PATH)
    self_content = _read(SELF_PATH)
    prompt_content = _read(PROMPT_PATH)

    # 1. Create ACT entry
    act_id = _next_id(evidence_content, "ACT")
    source_exchange = _yaml_get(c["block"], "source_exchange")
    source = "pipeline merge (Telegram approve)" if not source_exchange else "pipeline merge"
    act_entry = f'''
  - id: {act_id}
    date: {today}
    modality: text (pipeline merge)
    activity_type: knowledge — curated observation
    mind_category: {c["mind_category"]}
    source: {source}
    summary: "{c["summary"][:200].replace(chr(34), "'")}"
    curated_by: user
    evidence_tier: 3
'''
    # Insert before "## VI. ATTESTATION LOG" or at end of ACT entries
    att_m = re.search(r"\n## VI\. ATTESTATION LOG", evidence_content)
    if att_m:
        evidence_content = (
            evidence_content[: att_m.start()] + act_entry + evidence_content[att_m.start() :]
        )
    else:
        evidence_content += act_entry
    _write(EVIDENCE_PATH, evidence_content)

    # 2. Add to SELF
    cat = c["mind_category"].lower()
    safe_entry = (c["suggested_entry"] or "")[:200].replace('"', "'")
    entry_id: str
    if "knowledge" in cat or "IX-A" in c["profile_target"]:
        entry_id = _next_id(self_content, "LEARN")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    topic: "{safe_entry}"
    source: pipeline merge
    evidence_id: {act_id}
    provenance: human_approved

'''
        # Find IX-A yaml block, insert before closing ```
        ix_a = re.search(r"(### IX-A\. KNOWLEDGE.*?```yaml\n.*?)(\n```)", self_content, re.DOTALL)
        if ix_a:
            self_content = self_content[: ix_a.end(1)] + new_entry + self_content[ix_a.start(2) :]
    elif "curiosity" in cat or "IX-B" in c["profile_target"]:
        entry_id = _next_id(self_content, "CUR")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    topic: "{safe_entry}"
    trigger: pipeline merge
    response_signal: approved
    intensity: 3
    evidence_id: {act_id}
    provenance: human_approved

'''
        ix_b = re.search(r"(### IX-B\. CURIOSITY.*?```yaml\n.*?)(\n```)", self_content, re.DOTALL)
        if ix_b:
            self_content = self_content[: ix_b.end(1)] + new_entry + self_content[ix_b.start(2) :]
    else:
        entry_id = _next_id(self_content, "PER")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    type: observed
    observation: "{safe_entry}"
    evidence_id: {act_id}
    provenance: human_approved

'''
        ix_c = re.search(r"(### IX-C\..*?```yaml\n.*?)(\n```)", self_content, re.DOTALL)
        if ix_c:
            self_content = self_content[: ix_c.end(1)] + new_entry + self_content[ix_c.start(2) :]
    _write(SELF_PATH, self_content)

    # 3. Update prompt.py if prompt_addition is not "none"
    if c["prompt_addition"] and c["prompt_addition"].lower() != "none":
        # Append to YOUR KNOWLEDGE, YOUR CURIOSITY, or YOUR PERSONALITY
        add_line = f"- {c['prompt_addition'].strip()}\n"
        if "knowledge" in cat:
            prompt_content = prompt_content.replace("## WHAT YOU LOVE", add_line + "\n## WHAT YOU LOVE")
        elif "curiosity" in cat:
            prompt_content = prompt_content.replace("## HOW YOU HANDLE THINGS", add_line + "\n## HOW YOU HANDLE THINGS")
        else:
            prompt_content = prompt_content.replace("## HOW YOU HANDLE THINGS", add_line + "\n## HOW YOU HANDLE THINGS")
        _write(PROMPT_PATH, prompt_content)

    # 4. Emit applied event
    subprocess.run(
        ["python", "scripts/emit_pipeline_event.py", "applied", c["id"], f"evidence_id={act_id}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    return True


def move_to_processed(content: str, candidate_blocks: list[str]) -> str:
    """Move approved candidate blocks from Candidates to Processed."""
    for block in candidate_blocks:
        content = content.replace(block, "")
    # Ensure ## Processed exists and append blocks
    if "## Processed" not in content:
        content += "\n## Processed\n\n"
    processed_blocks = "\n".join(candidate_blocks)
    content = content.replace("## Processed\n\n", "## Processed\n\n" + processed_blocks + "\n")
    return content


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Perform merge (default: dry run)")
    ap.add_argument("--push", action="store_true", help="Git add, commit, push after merge")
    args = ap.parse_args()
    dry_run = not args.apply

    approved = get_approved_in_candidates()
    if not approved:
        print("No approved candidates to process.")
        return

    print(f"Found {len(approved)} approved candidate(s).")
    blocks_to_move: list[str] = []
    for c in approved:
        merge_candidate(c, dry_run)
        blocks_to_move.append(c["full_match"])

    if dry_run:
        print("Dry run. Use --apply to perform merge.")
        return

    # Move blocks from Candidates to Processed in PENDING-REVIEW
    content = _read(PENDING_PATH)
    for block in blocks_to_move:
        content = content.replace(block, "", 1)
    content = re.sub(r"\n{3,}", "\n\n", content)
    # Insert processed blocks at start of Processed section
    insertion = "\n".join(blocks_to_move) + "\n\n"
    content = content.replace("## Processed\n\n", "## Processed\n\n" + insertion, 1)
    _write(PENDING_PATH, content)

    # Export PRP
    subprocess.run(
        ["python", "scripts/export_prp.py", "-u", USER_ID, "-n", "Abby", "-o", str(PRP_PATH)],
        cwd=REPO_ROOT,
        check=True,
    )
    print("PRP exported.")

    if args.push:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN not set — skip push")
            return
        subprocess.run(["git", "add", str(PROFILE_DIR), str(PROMPT_PATH), str(PRP_PATH)], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "commit", "-m", "merge approved candidates via process_approved_candidates"], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True, env={**os.environ, "GITHUB_TOKEN": token})
        print("Pushed.")


if __name__ == "__main__":
    main()
