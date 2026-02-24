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
INTENT_PATH = PROFILE_DIR / "INTENT.md"
PROMPT_PATH = REPO_ROOT / "bot" / "prompt.py"
SELF_ARCHIVE_PATH = PROFILE_DIR / "SELF-ARCHIVE.md"
PRP_PATH = REPO_ROOT / "grace-mar-abby-prp.txt"
MERGE_RECEIPTS_PATH = PROFILE_DIR / "MERGE-RECEIPTS.jsonl"
MIN_EVIDENCE_TIER = 3


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
    global USER_ID, PROFILE_DIR, PENDING_PATH, SELF_PATH, EVIDENCE_PATH, INTENT_PATH, MERGE_RECEIPTS_PATH, SELF_ARCHIVE_PATH
    USER_ID = user_id.strip()
    PROFILE_DIR = REPO_ROOT / "users" / USER_ID
    PENDING_PATH = PROFILE_DIR / "PENDING-REVIEW.md"
    SELF_PATH = PROFILE_DIR / "SELF.md"
    EVIDENCE_PATH = PROFILE_DIR / "EVIDENCE.md"
    INTENT_PATH = PROFILE_DIR / "INTENT.md"
    MERGE_RECEIPTS_PATH = PROFILE_DIR / "MERGE-RECEIPTS.jsonl"
    SELF_ARCHIVE_PATH = PROFILE_DIR / "SELF-ARCHIVE.md"


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
        "min_evidence_tier": MIN_EVIDENCE_TIER,
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
    min_tier = receipt.get("min_evidence_tier", MIN_EVIDENCE_TIER)
    if not isinstance(min_tier, int) or min_tier < MIN_EVIDENCE_TIER:
        return False, f"receipt min_evidence_tier must be int >= {MIN_EVIDENCE_TIER}"
    receipt_ids = sorted(str(x).strip() for x in receipt["candidate_ids"] if str(x).strip())
    current_ids = _canonical_candidate_ids(approved)
    if receipt_ids != current_ids:
        return False, "receipt candidate_ids do not match currently approved candidates"
    return True, ""


def _append_merge_receipt(receipt: dict) -> None:
    MERGE_RECEIPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MERGE_RECEIPTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, ensure_ascii=True) + "\n")


def _emit_validation_failure(candidate_id: str | None, reason: str, actor: str | None = None) -> None:
    candidate_arg = candidate_id or "none"
    extras = [
        f"reason={reason[:200]}",
        "source=process_approved_candidates",
        "channel_key=operator:cli",
    ]
    if actor:
        extras.append(f"actor={actor}")
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            USER_ID,
            "validation_failed",
            candidate_arg,
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def _run_integrity_validation(min_evidence_tier: int) -> tuple[bool, str]:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate-integrity.py",
            "--user",
            USER_ID,
            "--min-evidence-tier",
            str(min_evidence_tier),
            "--json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return True, ""
    try:
        payload = json.loads(result.stdout.strip() or "{}")
        errors = payload.get("errors") or []
        if errors:
            return False, str(errors[0])
    except Exception:
        pass
    msg = (result.stderr or result.stdout or "integrity validation failed").strip()
    return False, msg.splitlines()[0] if msg else "integrity validation failed"


def _load_intent_profile() -> dict:
    """Load minimal intent profile from INTENT.md YAML block."""
    raw = _read(INTENT_PATH)
    if not raw:
        return {"ok": False, "reason": "missing INTENT.md", "tradeoff_rules": []}
    m = re.search(r"```(?:yaml|yml)\s*\n(.*?)```", raw, re.DOTALL)
    if not m:
        return {"ok": False, "reason": "missing YAML block", "tradeoff_rules": []}
    block = m.group(1)
    rules: list[dict] = []
    rules_block = re.search(
        r"^tradeoff_rules:\s*\n((?:^[ \t]+.+\n?)*)",
        block,
        re.MULTILINE,
    )
    if rules_block:
        chunks = re.findall(r"(?:^[ \t]*-\s+.+(?:\n(?![ \t]*-\s).+)*)", rules_block.group(1), re.MULTILINE)
        for idx, chunk in enumerate(chunks, 1):
            rid_m = re.search(r"\bid:\s*([^\n]+)", chunk)
            prio_m = re.search(r"\bprioritize:\s*([^\n]+)", chunk)
            de_m = re.search(r"\bdeprioritize:\s*([^\n]+)", chunk)
            when_m = re.search(r"\bwhen:\s*([^\n]+)", chunk)
            applies_to_m = re.search(r"\bapplies_to:\s*\[([^\]]*)\]", chunk)
            priority_m = re.search(r"\bpriority:\s*([^\n]+)", chunk)
            strategy_m = re.search(r"\bconflict_strategy:\s*([^\n]+)", chunk)
            applies_to = []
            if applies_to_m:
                applies_to = [
                    token.strip().strip("\"'")
                    for token in applies_to_m.group(1).split(",")
                    if token.strip()
                ]
            priority = 100
            if priority_m:
                raw = priority_m.group(1).strip().strip("\"'")
                if raw.isdigit():
                    priority = int(raw)
            rules.append(
                {
                    "id": (rid_m.group(1).strip().strip("\"'") if rid_m else f"INTENT-RULE-{idx:03d}"),
                    "when": (when_m.group(1).strip().strip("\"'") if when_m else ""),
                    "prioritize": (prio_m.group(1).strip().strip("\"'") if prio_m else ""),
                    "deprioritize": (de_m.group(1).strip().strip("\"'") if de_m else ""),
                    "applies_to": applies_to,
                    "priority": priority,
                    "conflict_strategy": (
                        strategy_m.group(1).strip().strip("\"'")
                        if strategy_m
                        else "escalate_to_human"
                    ),
                }
            )
    return {"ok": True, "tradeoff_rules": rules}


def _keywords(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", (text or "").lower())}


def _candidate_agent_source(candidate: dict) -> str:
    channel = _yaml_get(candidate.get("block", ""), "channel_key") or ""
    prefix = channel.split(":", 1)[0].strip().lower()
    mapping = {
        "telegram": "voice",
        "wechat": "voice",
        "extension": "browser_extension",
        "handback": "handback",
        "operator": "operator_cli",
        "openclaw": "openclaw",
    }
    return mapping.get(prefix, prefix or "unknown")


def _detect_intent_conflicts(candidate: dict, intent_profile: dict, candidate_source: str) -> list[dict]:
    """
    Advisory check only:
    If candidate text contains deprioritized terms but misses prioritized terms
    from the same intent rule, flag potential conflict.
    """
    if not intent_profile.get("ok"):
        return []
    text = " ".join(
        [
            candidate.get("summary", ""),
            candidate.get("suggested_entry", ""),
            candidate.get("prompt_addition", ""),
        ]
    )
    observed = _keywords(text)
    conflicts: list[dict] = []
    for rule in intent_profile.get("tradeoff_rules", []):
        applies_to = [str(x).strip().lower() for x in (rule.get("applies_to") or []) if str(x).strip()]
        if applies_to and candidate_source.lower() not in applies_to and "all" not in applies_to:
            continue
        deprioritized = _keywords(rule.get("deprioritize", ""))
        prioritized = _keywords(rule.get("prioritize", ""))
        if not deprioritized:
            continue
        hits_de = observed & deprioritized
        if not hits_de:
            continue
        hits_pr = observed & prioritized if prioritized else set()
        if hits_pr:
            continue
        conflicts.append(
            {
                "rule_id": rule.get("id", "UNKNOWN"),
                "severity": "advisory",
                "candidate_source": candidate_source,
                "rule_applies_to": applies_to or ["all"],
                "priority": int(rule.get("priority", 100)),
                "conflict_strategy": rule.get("conflict_strategy", "escalate_to_human"),
                "reason": (
                    f"candidate may over-optimize for deprioritized terms: "
                    f"{', '.join(sorted(hits_de))}"
                ),
            }
        )
    return sorted(conflicts, key=lambda x: int(x.get("priority", 100)))


def _emit_intent_conflict(
    candidate_id: str,
    conflict: dict,
    actor: str | None = None,
    event_type: str = "intent_conflict",
) -> None:
    extras = [
        f"rule_id={str(conflict.get('rule_id') or 'UNKNOWN')}",
        f"severity={str(conflict.get('severity') or 'advisory')}",
        f"candidate_source={str(conflict.get('candidate_source') or 'unknown')}",
        f"rule_applies_to={','.join(conflict.get('rule_applies_to') or ['all'])}",
        f"priority={str(conflict.get('priority') or '100')}",
        f"conflict_strategy={str(conflict.get('conflict_strategy') or 'escalate_to_human')}",
        f"reason={str(conflict.get('reason') or '')[:220]}",
        "source=process_approved_candidates",
        "channel_key=operator:cli",
    ]
    if actor:
        extras.append(f"actor={actor}")
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            USER_ID,
            event_type,
            candidate_id,
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def _emit_constitutional_critique_event(
    candidate_id: str,
    candidate_source: str,
    status: str,
    rule_ids: list[str],
    actor: str | None = None,
) -> None:
    extras = [
        f"status={status}",
        f"candidate_source={candidate_source}",
        f"rule_ids={','.join(rule_ids) if rule_ids else 'none'}",
        "source=process_approved_candidates",
        "channel_key=operator:cli",
    ]
    if actor:
        extras.append(f"actor={actor}")
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            USER_ID,
            "intent_constitutional_critique",
            candidate_id,
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def _emit_constitutional_revision_suggested(
    candidate_id: str,
    conflict: dict,
    actor: str | None = None,
) -> None:
    extras = [
        f"rule_id={str(conflict.get('rule_id') or 'UNKNOWN')}",
        f"candidate_source={str(conflict.get('candidate_source') or 'unknown')}",
        f"reason={str(conflict.get('reason') or '')[:220]}",
        "source=process_approved_candidates",
        "channel_key=operator:cli",
    ]
    if actor:
        extras.append(f"actor={actor}")
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            USER_ID,
            "intent_constitutional_revision_suggested",
            candidate_id,
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def _compute_fork_checksum() -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "scripts/fork_checksum.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checksum_lines = (result.stdout or "").strip().splitlines()
    if result.returncode != 0 or not checksum_lines:
        return False, (result.stderr or "checksum failed").strip()
    return True, checksum_lines[-1].strip()


def _validate_candidate_before_merge(candidate: dict, min_evidence_tier: int) -> tuple[bool, str]:
    block = candidate.get("block", "")
    summary = (candidate.get("summary") or "").strip()
    suggested_entry = (candidate.get("suggested_entry") or "").strip()
    mind_category = (candidate.get("mind_category") or "").strip().lower()
    if not summary:
        return False, "missing summary"
    if not suggested_entry:
        return False, "missing suggested_entry"
    if mind_category not in {"knowledge", "curiosity", "personality"}:
        return False, f"invalid mind_category: {mind_category or '(empty)'}"
    tier_match = re.search(r"^evidence_tier:\s*(\d+)", block, re.MULTILINE)
    if tier_match and int(tier_match.group(1)) < min_evidence_tier:
        return False, f"candidate evidence_tier below minimum {min_evidence_tier}"
    return True, ""


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
            "channel_key": _yaml_get(block, "channel_key") or "telegram",
        })
    return approved


def _channel_label(channel_key: str) -> str:
    """Human-readable channel for SELF-ARCHIVE (Telegram, Test, WeChat, Mini App)."""
    k = (channel_key or "").strip().lower()
    if k.startswith("telegram:") or k.startswith("chat "):
        return "Telegram"
    if k.startswith("test:"):
        return "Test"
    if k.startswith("wechat:"):
        return "WeChat"
    if k.startswith("miniapp:") or k.startswith("miniapp_"):
        return "Mini App"
    if k.startswith("operator:") or k == "operator:cli":
        return "Operator"
    return channel_key or "Unknown"


def _extract_source_exchange_snippet(block: str, max_chars: int = 600) -> str:
    """Extract source_exchange section from candidate block for SELF-ARCHIVE snippet."""
    m = re.search(r"source_exchange:\s*\n(.*?)(?=\n[A-Za-z_]+:|\n```|\Z)", block, re.DOTALL)
    if not m:
        return ""
    raw = m.group(1).strip()
    # Collapse newlines to space for single-line snippet
    out = " ".join(raw.split()).strip()
    return (out[:max_chars] + "...") if len(out) > max_chars else out


def _self_archive_header() -> str:
    return (
        "# SELF-ARCHIVE\n\n"
        "> Append-only log of approved activity for the self (voice and non-voice). "
        "Content is written here only when candidates are merged via process_approved_candidates. "
        "Telegram, WeChat, Mini App today; eventually email, X, and other platform channels.\n\n---\n\n"
    )


def _append_self_archive_entry(
    candidate_id: str,
    act_id: str,
    channel_key: str,
    summary: str,
    source_snippet: str,
) -> None:
    """Append one APPROVED entry to SELF-ARCHIVE (gated merge path only)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = _channel_label(channel_key)
    lines = [f"**[{ts}]** `APPROVED` ({label})\n", f"> {candidate_id} → {act_id}\n", f"> {summary[:300]}\n"]
    if source_snippet:
        for line in source_snippet.splitlines():
            lines.append(f"> {line[:400]}\n")
    lines.append("\n")
    block = "".join(lines)
    content = _read(SELF_ARCHIVE_PATH) if SELF_ARCHIVE_PATH.exists() else ""
    if not content.strip():
        content = _self_archive_header()
    new_content = content.rstrip() + "\n\n" + block.strip() + "\n"
    _write(SELF_ARCHIVE_PATH, new_content)


def merge_candidate_in_memory(
    c: dict,
    self_content: str,
    evidence_content: str,
    prompt_content: str,
    today: str,
    evidence_tier: int,
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
    evidence_tier: {evidence_tier}
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
            "--user",
            USER_ID,
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


def _run_openclaw_export(
    user_id: str,
    fmt: str,
    output_dir: str,
    destination: str,
    post_url: str,
    api_key: str,
) -> tuple[bool, str]:
    cmd = [
        sys.executable,
        "integrations/openclaw_hook.py",
        "--user",
        user_id,
        "--format",
        fmt,
        "--destination",
        destination,
        "--emit-event",
    ]
    if output_dir.strip():
        cmd.extend(["--output", output_dir.strip()])
    if destination == "post":
        if post_url.strip():
            cmd.extend(["--post-url", post_url.strip()])
        if api_key.strip():
            cmd.extend(["--api-key", api_key.strip()])
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        msg = (result.stderr or result.stdout or "openclaw export failed").strip()
        return False, msg
    return True, (result.stdout or "openclaw export complete").strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", "-u", default=USER_ID, help="User id (default: GRACE_MAR_USER_ID or pilot-001)")
    ap.add_argument("--apply", action="store_true", help="Perform merge (default: dry run)")
    ap.add_argument("--push", action="store_true", help="Git add, commit, push after merge")
    ap.add_argument("--approved-by", default="", help="Human approver id/name (required for --apply)")
    ap.add_argument("--receipt", default="", help="Path to approval receipt JSON (required for --apply)")
    ap.add_argument("--generate-receipt", default="", help="Generate approval receipt JSON and exit")
    ap.add_argument(
        "--min-evidence-tier",
        type=int,
        default=MIN_EVIDENCE_TIER,
        help=f"Minimum evidence tier policy for merge validation (default: {MIN_EVIDENCE_TIER})",
    )
    ap.add_argument("--export-openclaw", action="store_true", help="Run OpenClaw export after successful merge")
    ap.add_argument(
        "--openclaw-format",
        choices=["md", "md+manifest", "json+md", "full-prp", "fork-json"],
        default="md+manifest",
        help="OpenClaw export shape when --export-openclaw is used",
    )
    ap.add_argument("--openclaw-output", default="", help="Optional OpenClaw output directory")
    ap.add_argument(
        "--openclaw-destination",
        choices=["local", "post"],
        default="local",
        help="OpenClaw destination mode when --export-openclaw is used",
    )
    ap.add_argument("--openclaw-post-url", default="", help="OpenClaw post destination URL (if destination=post)")
    ap.add_argument("--openclaw-api-key", default="", help="OpenClaw post API key (if destination=post)")
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
        receipt["min_evidence_tier"] = max(args.min_evidence_tier, MIN_EVIDENCE_TIER)
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
    min_tier = max(int(receipt.get("min_evidence_tier", args.min_evidence_tier)), MIN_EVIDENCE_TIER)

    preflight_ok, preflight_reason = _run_integrity_validation(min_tier)
    if not preflight_ok:
        _emit_validation_failure(None, f"preflight_integrity_failed: {preflight_reason}", args.approved_by.strip())
        raise SystemExit(f"preflight integrity failed: {preflight_reason}")

    today = datetime.now().strftime("%Y-%m-%d")
    self_content = _read(SELF_PATH)
    evidence_content = _read(EVIDENCE_PATH)
    prompt_content = _read(PROMPT_PATH)
    pending_content = _read(PENDING_PATH)
    intent_profile = _load_intent_profile()
    blocks_to_move: list[str] = []
    applied_candidates: list[tuple[dict, str]] = []  # (c, act_id) for emit + SELF-ARCHIVE
    pre_checksum_ok, pre_checksum = _compute_fork_checksum()
    if not pre_checksum_ok:
        _emit_validation_failure(None, f"checksum_pre_failed: {pre_checksum}", args.approved_by.strip())
        raise SystemExit(f"checksum pre-merge failed: {pre_checksum}")

    for c in approved:
        candidate_ok, candidate_reason = _validate_candidate_before_merge(c, min_tier)
        if not candidate_ok:
            _emit_validation_failure(c["id"], candidate_reason, args.approved_by.strip())
            raise SystemExit(f"candidate {c['id']} failed validation: {candidate_reason}")
        candidate_source = _candidate_agent_source(c)
        intent_conflicts = _detect_intent_conflicts(c, intent_profile, candidate_source)
        conflict_rule_ids = [str(conflict.get("rule_id") or "UNKNOWN") for conflict in intent_conflicts]
        _emit_constitutional_critique_event(
            c["id"],
            candidate_source,
            status="advisory_flagged" if intent_conflicts else "advisory_clear",
            rule_ids=conflict_rule_ids,
            actor=args.approved_by.strip(),
        )
        for conflict in intent_conflicts:
            _emit_intent_conflict(
                c["id"],
                conflict,
                args.approved_by.strip(),
                event_type="intent_conflict_cross_agent",
            )
            _emit_constitutional_revision_suggested(
                c["id"],
                conflict,
                args.approved_by.strip(),
            )
            print(
                f"[advisory] intent_conflict {c['id']} "
                f"rule={conflict.get('rule_id')} source={candidate_source} "
                f"strategy={conflict.get('conflict_strategy')} reason={conflict.get('reason')}"
            )
        self_content, evidence_content, prompt_content, act_id = merge_candidate_in_memory(
            c, self_content, evidence_content, prompt_content, today, evidence_tier=min_tier
        )
        blocks_to_move.append(c["full_match"])
        applied_candidates.append((c, act_id))

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
            "checksum_before": pre_checksum,
        }
        _append_merge_receipt(receipt_event)
        print(f"Merge receipt appended: {MERGE_RECEIPTS_PATH}")

        for c, act_id in applied_candidates:
            _emit_applied_event(c["id"], act_id, args.approved_by.strip())

        post_ok, post_reason = _run_integrity_validation(min_tier)
        if not post_ok:
            raise RuntimeError(f"post-merge integrity failed: {post_reason}")
        after_ok, after_checksum = _compute_fork_checksum()
        if not after_ok:
            raise RuntimeError(f"checksum post-merge failed: {after_checksum}")
        if pre_checksum == after_checksum:
            raise RuntimeError("checksum unchanged after merge; expected state change")

        for c, act_id in applied_candidates:
            _append_self_archive_entry(
                c["id"],
                act_id,
                c.get("channel_key") or "telegram",
                c["summary"],
                _extract_source_exchange_snippet(c["block"]),
            )
        print("SELF-ARCHIVE updated.")
        if args.export_openclaw:
            export_ok, export_msg = _run_openclaw_export(
                user_id=USER_ID,
                fmt=args.openclaw_format,
                output_dir=args.openclaw_output,
                destination=args.openclaw_destination,
                post_url=args.openclaw_post_url,
                api_key=args.openclaw_api_key,
            )
            if export_ok:
                print("OpenClaw export complete.")
            else:
                # Non-fatal: merge succeeded; export failure is surfaced for operator action.
                print(f"Warning: OpenClaw export failed: {export_msg}")
    except Exception as e:
        _emit_validation_failure(None, f"merge_apply_failed_or_rolled_back: {e}", args.approved_by.strip())
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
