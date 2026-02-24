#!/usr/bin/env python3
"""
Process approved pipeline candidates: merge into SELF, EVIDENCE, prompt; run export_prp; optionally push.

Usage:
    python scripts/process_approved_candidates.py           # dry run
    python scripts/process_approved_candidates.py --apply   # perform merge
    python scripts/process_approved_candidates.py --apply --push  # merge + git push
    python scripts/process_approved_candidates.py -u pilot-001 --generate-receipt /tmp/receipt.json --approved-by operator

Requires repo root as cwd. For merge-from-Telegram: run this after approving in Telegram.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_ID = os.getenv("GRACE_MAR_USER_ID", "pilot-001").strip() or "pilot-001"
PROFILE_DIR = REPO_ROOT / "users" / USER_ID
PENDING_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
SELF_PATH = PROFILE_DIR / "SELF.md"
EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"
PROMPT_PATH = REPO_ROOT / "bot" / "prompt.py"
PRP_PATH = REPO_ROOT / "grace-mar-abby-prp.txt"
MERGE_RECEIPTS_PATH = PROFILE_DIR / "MERGE-RECEIPTS.jsonl"


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


def _set_user(user_id: str) -> None:
    """Configure per-user paths for this invocation."""
    global USER_ID, PROFILE_DIR, PENDING_PATH, SELF_PATH, EVIDENCE_PATH, MERGE_RECEIPTS_PATH
    USER_ID = user_id.strip()
    PROFILE_DIR = REPO_ROOT / "users" / USER_ID
    PENDING_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
    SELF_PATH = PROFILE_DIR / "SELF.md"
    EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"
    MERGE_RECEIPTS_PATH = PROFILE_DIR / "MERGE-RECEIPTS.jsonl"


def _prp_output_path() -> Path:
    if USER_ID == "pilot-001":
        return PRP_PATH
    return PROFILE_DIR / f"{USER_ID}-prp.txt"


PROMPT_SECTION_HEADERS = {
    "YOUR KNOWLEDGE": "## YOUR KNOWLEDGE (from observations)",
    "YOUR CURIOSITY": "## YOUR CURIOSITY (what catches your attention)",
    "YOUR PERSONALITY": "## YOUR PERSONALITY (observed)",
}


def _insert_prompt_addition(prompt_content: str, prompt_section: str, addition: str) -> str:
    """
    Insert prompt addition under an explicit section header.
    Falls back to previous anchors only if section header is missing.
    """
    line = f"- {addition.strip()}"
    if not addition.strip() or line in prompt_content:
        return prompt_content

    section_key = (prompt_section or "").strip().upper()
    header = PROMPT_SECTION_HEADERS.get(section_key)
    if header and header in prompt_content:
        start = prompt_content.find(header)
        next_header = prompt_content.find("\n## ", start + len(header))
        if next_header == -1:
            next_header = len(prompt_content)
        section_block = prompt_content[start:next_header]
        if line in section_block:
            return prompt_content
        insertion = f"{header}\n\n{line}\n"
        return prompt_content.replace(header + "\n", insertion, 1)

    # Legacy fallback anchors for compatibility with historical prompt layouts.
    if section_key == "YOUR KNOWLEDGE":
        return prompt_content.replace("## WHAT YOU LOVE", line + "\n\n## WHAT YOU LOVE", 1)
    if section_key in ("YOUR CURIOSITY", "YOUR PERSONALITY"):
        return prompt_content.replace("## HOW YOU HANDLE THINGS", line + "\n\n## HOW YOU HANDLE THINGS", 1)
    return prompt_content


def _utc_now_iso() -> str:
    return datetime.now().isoformat()


def _canonical_candidate_ids(candidates: list[dict]) -> list[str]:
    return sorted(c["id"] for c in candidates)


def _build_receipt(approved: list[dict], approved_by: str) -> dict:
    return {
        "user_id": USER_ID,
        "approved_by": approved_by.strip(),
        "approved_at": _utc_now_iso(),
        "candidate_ids": _canonical_candidate_ids(approved),
    }


def _validate_receipt(receipt: dict, approved: list[dict]) -> tuple[bool, str]:
    if not isinstance(receipt, dict):
        return False, "receipt must be a JSON object"
    if receipt.get("user_id") != USER_ID:
        return False, f"receipt user_id must be {USER_ID}"
    approved_by = str(receipt.get("approved_by") or "").strip()
    approved_at = str(receipt.get("approved_at") or "").strip()
    if not approved_by:
        return False, "receipt missing approved_by"
    if not approved_at:
        return False, "receipt missing approved_at"
    if not isinstance(receipt.get("candidate_ids"), list):
        return False, "receipt missing candidate_ids list"
    receipt_ids = sorted(str(x).strip() for x in receipt["candidate_ids"] if str(x).strip())
    current_ids = _canonical_candidate_ids(approved)
    if receipt_ids != current_ids:
        return False, "receipt candidate_ids do not match currently approved candidates"
    return True, ""


def _append_merge_receipt(receipt: dict) -> None:
    MERGE_RECEIPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MERGE_RECEIPTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, ensure_ascii=True) + "\n")


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
            "prompt_section": _yaml_get(block, "prompt_section") or "",
            "prompt_addition": _yaml_get(block, "prompt_addition") or "none",
        })
    return approved


def merge_candidate_in_memory(
    c: dict,
    self_content: str,
    evidence_content: str,
    prompt_content: str,
    today: str,
) -> tuple[str, str, str, str]:
    """Merge one candidate into in-memory content; returns updated contents + act_id."""

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
    # 3. Update prompt.py if prompt_addition is not "none"
    if c["prompt_addition"] and c["prompt_addition"].lower() != "none":
        prompt_section = c.get("prompt_section") or ""
        if not prompt_section:
            if "knowledge" in cat:
                prompt_section = "YOUR KNOWLEDGE"
            elif "curiosity" in cat:
                prompt_section = "YOUR CURIOSITY"
            else:
                prompt_section = "YOUR PERSONALITY"
        prompt_content = _insert_prompt_addition(
            prompt_content,
            prompt_section,
            c["prompt_addition"],
        )
    return self_content, evidence_content, prompt_content, act_id


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


def _transactional_write(files: dict[Path, str]) -> None:
    """
    Best-effort transactional write with rollback.
    Writes all files, and restores originals if any write fails.
    """
    originals: dict[Path, str | None] = {}
    for path in files:
        originals[path] = _read(path) if path.exists() else None
    try:
        for path, content in files.items():
            _write(path, content)
    except Exception:
        for path, original in originals.items():
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    _write(path, original)
            except Exception:
                pass
        raise


def _emit_applied_event(candidate_id: str, evidence_id: str, approved_by: str) -> None:
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "applied",
            candidate_id,
            f"evidence_id={evidence_id}",
            "source=process_approved_candidates",
            f"actor={approved_by}",
            "channel_key=operator:cli",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", "-u", default=USER_ID, help="User id (default: GRACE_MAR_USER_ID or pilot-001)")
    ap.add_argument("--apply", action="store_true", help="Perform merge (default: dry run)")
    ap.add_argument("--push", action="store_true", help="Git add, commit, push after merge")
    ap.add_argument("--approved-by", default="", help="Human approver id/name (required for --apply)")
    ap.add_argument("--receipt", default="", help="Path to approval receipt JSON (required for --apply)")
    ap.add_argument("--generate-receipt", default="", help="Generate approval receipt JSON and exit")
    args = ap.parse_args()
    _set_user(args.user)
    dry_run = not args.apply

    approved = get_approved_in_candidates()
    if not approved:
        print("No approved candidates to process.")
        return

    if args.generate_receipt:
        if not args.approved_by.strip():
            raise SystemExit("--approved-by is required with --generate-receipt")
        receipt = _build_receipt(approved, args.approved_by)
        out_path = Path(args.generate_receipt)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote receipt template: {out_path}")
        return

    print(f"Found {len(approved)} approved candidate(s).")
    if dry_run:
        for c in approved:
            print(f"  [DRY RUN] would merge {c['id']}: {c['summary'][:60]}...")
        print("Dry run. Use --apply to perform merge.")
        print("To create a receipt template: --generate-receipt receipt.json --approved-by <name>")
        return

    if not args.approved_by.strip():
        raise SystemExit("--approved-by is required with --apply")
    if not args.receipt.strip():
        raise SystemExit("--receipt is required with --apply")

    receipt_path = Path(args.receipt)
    if not receipt_path.exists():
        raise SystemExit(f"receipt file not found: {receipt_path}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    ok, reason = _validate_receipt(receipt, approved)
    if not ok:
        raise SystemExit(f"invalid receipt: {reason}")

    today = datetime.now().strftime("%Y-%m-%d")
    self_content = _read(SELF_PATH)
    evidence_content = _read(EVIDENCE_PATH)
    prompt_content = _read(PROMPT_PATH)
    pending_content = _read(PENDING_PATH)
    blocks_to_move: list[str] = []
    applied_pairs: list[tuple[str, str]] = []
    for c in approved:
        self_content, evidence_content, prompt_content, act_id = merge_candidate_in_memory(
            c, self_content, evidence_content, prompt_content, today
        )
        blocks_to_move.append(c["full_match"])
        applied_pairs.append((c["id"], act_id))

    # Move blocks from Candidates to Processed in PENDING-REVIEW
    for block in blocks_to_move:
        pending_content = pending_content.replace(block, "", 1)
    pending_content = re.sub(r"\n{3,}", "\n\n", pending_content)
    # Insert processed blocks at start of Processed section
    insertion = "\n".join(blocks_to_move) + "\n\n"
    if "## Processed\n\n" in pending_content:
        pending_content = pending_content.replace("## Processed\n\n", "## Processed\n\n" + insertion, 1)
    elif "## Processed" in pending_content:
        pending_content = pending_content.replace("## Processed", "## Processed\n\n" + insertion, 1)
    else:
        pending_content = pending_content.rstrip() + "\n\n## Processed\n\n" + insertion

    original_files = {
        SELF_PATH: _read(SELF_PATH),
        EVIDENCE_PATH: _read(EVIDENCE_PATH),
        PROMPT_PATH: _read(PROMPT_PATH),
        PENDING_PATH: _read(PENDING_PATH),
    }
    file_plan = {
        SELF_PATH: self_content,
        EVIDENCE_PATH: evidence_content,
        PROMPT_PATH: prompt_content,
        PENDING_PATH: pending_content,
    }
    _transactional_write(file_plan)

    try:
        # Export PRP
        subprocess.run(
            [sys.executable, "scripts/export_prp.py", "-u", USER_ID, "-n", "Abby", "-o", str(_prp_output_path())],
            cwd=REPO_ROOT,
            check=True,
        )
        print("PRP exported.")

        receipt_event = {
            **receipt,
            "merged_at": _utc_now_iso(),
            "merge_source": "process_approved_candidates",
        }
        _append_merge_receipt(receipt_event)
        print(f"Merge receipt appended: {MERGE_RECEIPTS_PATH}")

        for candidate_id, act_id in applied_pairs:
            _emit_applied_event(candidate_id, act_id, args.approved_by.strip())
    except Exception:
        rollback_plan = {
            SELF_PATH: original_files[SELF_PATH],
            EVIDENCE_PATH: original_files[EVIDENCE_PATH],
            PROMPT_PATH: original_files[PROMPT_PATH],
            PENDING_PATH: original_files[PENDING_PATH],
        }
        _transactional_write(rollback_plan)
        raise

    if args.push:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN not set — skip push")
            return
        subprocess.run(
            ["git", "add", str(PROFILE_DIR), str(PROMPT_PATH), str(_prp_output_path())],
            cwd=REPO_ROOT,
            check=True,
        )
        subprocess.run(["git", "commit", "-m", "merge approved candidates via process_approved_candidates"], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True, env={**os.environ, "GITHUB_TOKEN": token})
        print("Pushed.")


if __name__ == "__main__":
    main()
