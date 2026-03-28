#!/usr/bin/env python3
"""
Process approved pipeline candidates: merge into SELF, EVIDENCE, prompt; run export_prp; optionally push.
After --apply, stderr reminds to refresh OpenClaw / external USER.md if --export-openclaw was not used.

Territory batch merge (work-politics vs companion):
    --territory work-politics  # preferred (aliases: pol, wp; legacy: wap)
    --territory companion  # only the rest
    --territory all        # default — every approved row in Candidates section
    Generate receipt and apply with the same --territory so candidate_ids match.

Usage:
    python scripts/process_approved_candidates.py           # dry run
    python scripts/process_approved_candidates.py --apply   # perform merge
    python scripts/process_approved_candidates.py --apply --push  # merge + git push
    python scripts/process_approved_candidates.py -u grace-mar --generate-receipt /tmp/receipt.json --approved-by operator

Requires repo root as cwd. For merge-from-Telegram: run this after approving in Telegram.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
_SRC = REPO_ROOT / "src"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from grace_mar.merge.evidence_log import append_act_entry, upsert_reading_list_entry
from grace_mar.merge.prompt_sync import insert_prompt_addition, rebuild_observation_sections_from_self
from grace_mar.merge.self_ix import insert_ix_a_entry, insert_ix_b_entry, insert_ix_c_entry
from emit_pipeline_event import append_pipeline_event
from harness_events import append_harness_event
from pipeline_correlation import find_staged_event_id_for_candidate
from recursion_gate_review import split_gate_sections
from recursion_gate_territory import TERRITORY_WORK_POLITICS, normalize_territory_cli, territory_from_yaml_block
from identity_library_boundary_rules import collect_ix_a_violations_from_self_md
from repo_io import CANONICAL_EVIDENCE_BASENAME

USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
PROFILE_DIR = REPO_ROOT / "users" / USER_ID
RECURSION_GATE_PATH = PROFILE_DIR / "recursion-gate.md"
SELF_PATH = PROFILE_DIR / "self.md"
EVIDENCE_PATH = PROFILE_DIR / CANONICAL_EVIDENCE_BASENAME
INTENT_PATH = PROFILE_DIR / "intent.md"
PROMPT_PATH = REPO_ROOT / "bot" / "prompt.py"
PRP_PATH = REPO_ROOT / "grace-mar-llm.txt"
MERGE_RECEIPTS_PATH = PROFILE_DIR / "merge-receipts.jsonl"
MIN_EVIDENCE_TIER = 3

ALLOWED_ORIGIN = frozenset(
    {
        "seed_capture",
        "session_interaction",
        "operator_observation",
        "artifact_ingest",
        "parent_merge",
        "self_library_curation",
    }
)
ALLOWED_LINEAGE_CLASS = frozenset(
    {
        "fork_native",
        "real_world_update",
        "boundary_reclassification",
        "snapshot_only",
    }
)


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
    global USER_ID, PROFILE_DIR, RECURSION_GATE_PATH, SELF_PATH, EVIDENCE_PATH, INTENT_PATH, MERGE_RECEIPTS_PATH
    USER_ID = user_id.strip()
    PROFILE_DIR = REPO_ROOT / "users" / USER_ID
    RECURSION_GATE_PATH = PROFILE_DIR / "recursion-gate.md"
    SELF_PATH = PROFILE_DIR / "self.md"
    EVIDENCE_PATH = PROFILE_DIR / CANONICAL_EVIDENCE_BASENAME
    INTENT_PATH = PROFILE_DIR / "intent.md"
    MERGE_RECEIPTS_PATH = PROFILE_DIR / "merge-receipts.jsonl"


def _prp_output_path() -> Path:
    if USER_ID == "grace-mar":
        return PRP_PATH
    return PROFILE_DIR / f"{USER_ID}-llm.txt"


def _utc_now_iso() -> str:
    return datetime.now().isoformat()


def _canonical_candidate_ids(candidates: list[dict]) -> list[str]:
    return sorted(c["id"] for c in candidates)


def _merge_receipt_line_count() -> int:
    if not MERGE_RECEIPTS_PATH.is_file():
        return 0
    return len([ln for ln in MERGE_RECEIPTS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()])


def _prev_receipt_hash_from_file() -> str:
    if not MERGE_RECEIPTS_PATH.is_file():
        return ""
    lines = [ln for ln in MERGE_RECEIPTS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return ""
    try:
        last = json.loads(lines[-1])
        return str(last.get("receipt_hash") or "")
    except json.JSONDecodeError:
        return ""


def _receipt_body_hash(receipt: dict) -> str:
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    payload = json.dumps(body, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_receipt(approved: list[dict], approved_by: str, territory: str = "all") -> dict:
    from grace_mar.fork_state import load_fork_state

    n = _merge_receipt_line_count() + 1
    receipt_id = f"MR-{n:04d}"
    session_ids = sorted(
        {str(c.get("session_id") or "").strip() for c in approved if str(c.get("session_id") or "").strip()}
    )
    lineage_summary = dict(Counter((c.get("lineage_class") or "").strip() or "fork_native" for c in approved))
    try:
        st = load_fork_state(REPO_ROOT, USER_ID)
    except OSError:
        st = None
    fork_phase_before = str((st or {}).get("phase") or "interact")
    fork_phase_after = fork_phase_before
    if fork_phase_before == "merge_pending":
        fork_phase_after = "interact"
    r = {
        "receipt_id": receipt_id,
        "user_id": USER_ID,
        "approved_by": approved_by.strip(),
        "approved_at": _utc_now_iso(),
        "min_evidence_tier": MIN_EVIDENCE_TIER,
        "candidate_ids": _canonical_candidate_ids(approved),
        "session_ids": session_ids,
        "fork_phase_before": fork_phase_before,
        "fork_phase_after": fork_phase_after,
        "lineage_summary": lineage_summary,
        "prev_receipt_hash": _prev_receipt_hash_from_file(),
    }
    if territory and territory != "all":
        r["territory"] = territory
    r["receipt_hash"] = _receipt_body_hash(r)
    return r


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
    """Load minimal intent profile from intent.md YAML block."""
    raw = _read(INTENT_PATH)
    if not raw:
        return {"ok": False, "reason": "missing intent.md", "tradeoff_rules": []}
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
        [sys.executable, "scripts/fork_checksum.py", "-u", USER_ID],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checksum_lines = (result.stdout or "").strip().splitlines()
    if result.returncode != 0 or not checksum_lines:
        return False, (result.stderr or "checksum failed").strip()
    return True, checksum_lines[-1].strip()


def _is_meta_infra_candidate(candidate: dict) -> bool:
    """META_INFRA: infrastructure proposal — no SELF/EVIDENCE/prompt merge."""
    return (_yaml_get(candidate.get("block", ""), "proposal_class") or "").strip().upper() == "META_INFRA"


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
    content = _read(RECURSION_GATE_PATH)
    if not content:
        return []
    candidates_section, _processed_section = split_gate_sections(content)
    approved: list[dict] = []
    for m in re.finditer(r"### (CANDIDATE-\d+)(?:\s*\([^)]*\))?\s*\n```yaml\n(.*?)```", candidates_section, re.DOTALL):
        block = m.group(2)
        if "status: approved" not in block:
            continue
        intake = (
            _yaml_get(block, "intake_evidence_id")
            or _yaml_get(block, "evidence_ref")
            or ""
        ).strip()
        if intake.lower() in ("null", "none", ""):
            intake = ""
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
            "prompt_merge_mode": (_yaml_get(block, "prompt_merge_mode") or "").strip().lower(),
            "evidence_record_type": (_yaml_get(block, "evidence_record_type") or "act").strip().lower(),
            "channel_key": _yaml_get(block, "channel_key") or "telegram",
            "intake_evidence_id": intake,
            "origin": (_yaml_get(block, "origin") or "").strip(),
            "lineage_class": (_yaml_get(block, "lineage_class") or "").strip(),
            "session_id": (_yaml_get(block, "session_id") or "").strip(),
            "operator_source": (_yaml_get(block, "operator_source") or "").strip(),
        })
    return approved


def _validate_lifecycle_for_merge(approved: list[dict]) -> tuple[bool, str]:
    """Require origin, lineage_class, and session_id or operator_source on each candidate."""
    for c in approved:
        oid = (c.get("origin") or "").strip()
        lc = (c.get("lineage_class") or "").strip()
        sid = (c.get("session_id") or "").strip()
        ops = (c.get("operator_source") or "").strip()
        if _is_meta_infra_candidate(c):
            continue
        if oid not in ALLOWED_ORIGIN:
            return False, f"{c['id']}: origin must be one of {sorted(ALLOWED_ORIGIN)}"
        if lc not in ALLOWED_LINEAGE_CLASS:
            return False, f"{c['id']}: lineage_class must be one of {sorted(ALLOWED_LINEAGE_CLASS)}"
        if not sid and not ops:
            return False, f"{c['id']}: session_id or operator_source required"
    return True, ""


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


# Gated approved log: self-archive.md § VIII (canonical EVIDENCE file; self-evidence.md optional compat pointer).
GATED_LOG_SECTION = "## VIII. GATED APPROVED LOG (SELF-ARCHIVE)"
_END_FILE_LINE = re.compile(r"(?m)^END OF FILE.*$")


def _gated_log_section_prologue() -> str:
    return (
        "\n\n"
        + GATED_LOG_SECTION
        + "\n\n"
        + "> Append-only log of approved activity for the self (voice and non-voice). "
        + "Written only when candidates are merged via process_approved_candidates. "
        + "Lives in this file as § VIII (see docs/canonical-paths.md).\n\n"
        + "---\n\n"
    )


def _ensure_gated_log_section(evidence: str) -> str:
    if GATED_LOG_SECTION in evidence:
        return evidence
    m = _END_FILE_LINE.search(evidence)
    if m:
        return evidence[: m.start()].rstrip() + _gated_log_section_prologue() + evidence[m.start() :]
    return evidence.rstrip() + _gated_log_section_prologue()


def _append_gated_evidence_log_entry(
    candidate_id: str,
    act_id: str,
    channel_key: str,
    summary: str,
    source_snippet: str,
) -> None:
    """Append one APPROVED entry to self-archive.md § VIII (gated merge path only)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = _channel_label(channel_key)
    lines = [f"**[{ts}]** `APPROVED` ({label})\n", f"> {candidate_id} → {act_id}\n", f"> {summary[:300]}\n"]
    if source_snippet:
        for line in source_snippet.splitlines():
            lines.append(f"> {line[:400]}\n")
    lines.append("\n")
    block = "".join(lines)
    content = _read(EVIDENCE_PATH)
    if not content.strip():
        raise OSError(f"EVIDENCE missing or empty: {EVIDENCE_PATH}")
    content = _ensure_gated_log_section(content)
    m = _END_FILE_LINE.search(content)
    if m:
        insertion = "\n" + block.strip() + "\n"
        new_content = content[: m.start()] + insertion + content[m.start() :]
    else:
        new_content = content.rstrip() + "\n\n" + block.strip() + "\n"
    _write(EVIDENCE_PATH, new_content)


def _append_session_log_for_merge(candidate_ids: list[str], approved_by: str) -> None:
    """Append one line per merged candidate under ## Pipeline merge (automated)."""
    path = PROFILE_DIR / "session-log.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = "\n".join(
        f"- {ts} | pipeline merge | {cid} | approved by {approved_by}" for cid in candidate_ids
    )
    section = "\n\n## Pipeline merge (automated)\n\n"
    existing = _read(path)
    if not existing.strip():
        _write(path, f"# SESSION LOG — {USER_ID}\n\n{section.strip()}\n\n{lines}\n")
        return
    if "## Pipeline merge (automated)" not in existing:
        _write(path, existing.rstrip() + section + lines + "\n")
    else:
        _write(path, existing.rstrip() + "\n" + lines + "\n")


def merge_candidate_in_memory(
    c: dict,
    self_content: str,
    evidence_content: str,
    prompt_content: str,
    today: str,
    evidence_tier: int,
) -> tuple[str, str, str, str, str]:
    """Merge one candidate into in-memory content; returns contents + act_id + ix_entry_id (LEARN/CUR/PER)."""

    prompt_merge_mode = (c.get("prompt_merge_mode") or "").strip().lower()
    evidence_record_type = (c.get("evidence_record_type") or "act").strip().lower()

    # 1. Create ACT entry
    act_id = _next_id(evidence_content, "ACT")
    source_exchange = _yaml_get(c["block"], "source_exchange")
    source = "pipeline merge (Telegram approve)" if not source_exchange else "pipeline merge"
    if evidence_record_type == "read":
        activity_type = "reading — curated"
    elif evidence_record_type == "write":
        activity_type = "writing — curated"
    else:
        activity_type = "knowledge — curated observation"

    act_entry = f'''
  - id: {act_id}
    date: {today}
    modality: text (pipeline merge)
    activity_type: {activity_type}
    mind_category: {c["mind_category"]}
    source: {source}
    summary: "{c["summary"][:200].replace(chr(34), "'")}"
    curated_by: user
    evidence_tier: {evidence_tier}
'''
    evidence_content = append_act_entry(evidence_content, act_entry)

    if evidence_record_type == "read":
        read_id = _next_id(evidence_content, "READ")
        evidence_content = upsert_reading_list_entry(
            evidence_content,
            read_id=read_id,
            title=(c.get("suggested_entry") or c.get("summary") or "")[:500],
            evidence_tier=evidence_tier,
            status="completed",
        )

    # 2. Add to SELF
    cat = c["mind_category"].lower()
    safe_entry = (c["suggested_entry"] or "")[:200].replace('"', "'")
    intake_line = ""
    iid = (c.get("intake_evidence_id") or "").strip()
    if iid and re.match(r"^READ-[\w-]+$", iid, re.I):
        intake_line = f"    intake_evidence_id: {iid}\n"
    entry_id: str
    if "knowledge" in cat or "IX-A" in c["profile_target"]:
        entry_id = _next_id(self_content, "LEARN")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    topic: "{safe_entry}"
    source: pipeline merge
    evidence_id: {act_id}
{intake_line}    provenance: human_approved

'''
        self_content = insert_ix_a_entry(self_content, new_entry)
    elif "curiosity" in cat or "IX-B" in c["profile_target"]:
        entry_id = _next_id(self_content, "CUR")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    topic: "{safe_entry}"
    trigger: pipeline merge
    response_signal: approved
    intensity: 3
    evidence_id: {act_id}
{intake_line}    provenance: human_approved

'''
        self_content = insert_ix_b_entry(self_content, new_entry)
    else:
        entry_id = _next_id(self_content, "PER")
        new_entry = f'''  - id: {entry_id}
    date: {today}
    type: observed
    observation: "{safe_entry}"
    evidence_id: {act_id}
{intake_line}    provenance: human_approved

'''
        self_content = insert_ix_c_entry(self_content, new_entry)

    # 3. Update prompt.py: optional rebuild from IX, else append-style addition
    if prompt_merge_mode == "rebuild_ix":
        prompt_content = rebuild_observation_sections_from_self(prompt_content, self_content)
    elif c["prompt_addition"] and c["prompt_addition"].lower() != "none":
        prompt_section = c.get("prompt_section") or ""
        if not prompt_section:
            if "knowledge" in cat:
                prompt_section = "YOUR KNOWLEDGE"
            elif "curiosity" in cat:
                prompt_section = "YOUR CURIOSITY"
            else:
                prompt_section = "YOUR PERSONALITY"
        prompt_content = insert_prompt_addition(
            prompt_content,
            prompt_section,
            c["prompt_addition"],
        )
    return self_content, evidence_content, prompt_content, act_id, entry_id


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


def _safe_pipeline_str(s: str, max_len: int) -> str:
    t = (s or "").replace("\n", " ").replace("\r", " ").strip()
    return t[:max_len] if len(t) > max_len else t


def _record_refs_for_applied(user_id: str, surface: str, profile_target: str, proposal_class: str) -> list[str]:
    """Repo-relative paths for replay / boundary debugging (not a full merge file list)."""
    base = f"users/{user_id}"
    pt = (profile_target or "").upper()
    pc = (proposal_class or "").upper()
    refs: list[str] = []
    if any(tok in pc for tok in ("SELF_LIBRARY", "CIV_MEM", "LIBRARY_")):
        refs.append(f"{base}/self-library.md")
    if surface == "SELF_KNOWLEDGE" or "IX-A" in pt:
        refs.append(f"{base}/self.md#IX-A")
    elif surface == "SELF_CURIOSITY" or "IX-B" in pt:
        refs.append(f"{base}/self.md#IX-B")
    else:
        refs.append(f"{base}/self.md#IX-C")
    if "SKILLS" in pc:
        refs.append(f"{base}/skills.md")
    refs.append(f"{base}/self-archive.md")
    out: list[str] = []
    seen: set[str] = set()
    for r in refs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _emit_applied_event(c: dict, act_id: str, ix_entry_id: str, approved_by: str) -> dict:
    block = c.get("block") or ""
    cat = (c.get("mind_category") or "").lower()
    pt = c.get("profile_target") or ""
    if "knowledge" in cat or "IX-A" in pt.upper():
        surface = "SELF_KNOWLEDGE"
    elif "curiosity" in cat or "IX-B" in pt.upper():
        surface = "SELF_CURIOSITY"
    else:
        surface = "SELF_PERSONALITY"
    pc = (_yaml_get(block, "proposal_class") or _yaml_get(block, "evidence_ref") or "").strip()
    if not pc:
        pc = "SELF_KNOWLEDGE_ADD"
    had_conflicts = bool(
        re.search(r"contradictions_detected|conflicts_detected|CONFLICT:", block, re.I)
    )
    ch = (c.get("channel_key") or "operator:cli").strip() or "operator:cli"
    merge_payload: dict = {
        "event_schema": 2,
        "evidence_id": act_id,
        "ix_entry_id": ix_entry_id,
        "mind_category": _safe_pipeline_str(c.get("mind_category") or "", 80),
        "profile_target": _safe_pipeline_str(pt, 120),
        "summary_snippet": _safe_pipeline_str(c.get("summary") or "", 300),
        "proposal_class": _safe_pipeline_str(pc, 80),
        "had_conflicts": had_conflicts,
        "surface": surface,
        "source": "process_approved_candidates",
        "actor": _safe_pipeline_str(approved_by, 120),
        "channel_key": _safe_pipeline_str(ch, 100),
        "replay_mode": "merge",
        "candidate_ref": f"recursion-gate.md#{c['id']}",
    }
    parent = find_staged_event_id_for_candidate(PROFILE_DIR / "pipeline-events.jsonl", c["id"])
    if parent:
        merge_payload["parent_event_id"] = parent
    merge_payload["record_refs"] = _record_refs_for_applied(USER_ID, surface, pt, pc)
    return append_pipeline_event(USER_ID, "applied", c["id"], merge=merge_payload)


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


def _refresh_derived_exports() -> None:
    commands = [
        [sys.executable, "scripts/export_manifest.py", "-u", USER_ID, "-o", str(PROFILE_DIR)],
        [sys.executable, "scripts/fork_checksum.py", "-u", USER_ID, "--manifest"],
        [sys.executable, "scripts/export_runtime_bundle.py", "-u", USER_ID, "-o", str(PROFILE_DIR / "runtime-bundle")],
    ]
    for cmd in commands:
        subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", "-u", default=USER_ID, help="User id (default: GRACE_MAR_USER_ID or grace-mar)")
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
    ap.add_argument("--quick", default="", help="Quick merge single candidate (implies --apply); e.g. CANDIDATE-0040")
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
    ap.add_argument(
        "--territory",
        choices=("all", "pol", "wap", "wp", "work-politics", "companion"),
        default="all",
        help="Merge only approved candidates in this territory (work-politics = pol/wp aliases; legacy wap; companion = rest). Receipt must match.",
    )
    ap.add_argument(
        "--require-lifecycle-fields",
        action="store_true",
        help="Require origin, lineage_class, and session_id|operator_source on each merged candidate (fork history)",
    )
    args = ap.parse_args()
    territory = normalize_territory_cli(args.territory)
    _set_user(args.user)
    dry_run = not args.apply

    # --quick: single-candidate merge without receipt file (for Telegram one-tap)
    if args.quick.strip():
        args.apply = True
        dry_run = False
        if not args.approved_by.strip():
            raise SystemExit("--approved-by is required with --quick")

    approved = get_approved_in_candidates()
    if territory == "work-politics":
        approved = [c for c in approved if territory_from_yaml_block(c["block"]) == TERRITORY_WORK_POLITICS]
    elif territory == "companion":
        approved = [c for c in approved if territory_from_yaml_block(c["block"]) != TERRITORY_WORK_POLITICS]
    if args.quick.strip():
        quick_id = args.quick.strip()
        if not quick_id.upper().startswith("CANDIDATE-"):
            raise SystemExit(f"--quick expects CANDIDATE-XXXX, got {quick_id}")
        approved = [c for c in approved if c["id"] == quick_id]
        if not approved:
            raise SystemExit(f"No approved candidate {quick_id} — ensure it is approved (e.g. via /review)")

    if not approved:
        print(
            f"No approved candidates to process (territory={territory}). "
            "Approve rows in recursion-gate above ## Processed; work-politics rows need territory: work-politics (or legacy) or channel_key: operator:pol / operator:wap."
        )
        return

    if args.require_lifecycle_fields:
        ok_lc, reason_lc = _validate_lifecycle_for_merge(approved)
        if not ok_lc:
            raise SystemExit(f"lifecycle validation failed: {reason_lc}")

    if args.generate_receipt:
        if not args.approved_by.strip():
            raise SystemExit("--approved-by is required with --generate-receipt")
        receipt = _build_receipt(approved, args.approved_by, territory)
        receipt["min_evidence_tier"] = max(args.min_evidence_tier, MIN_EVIDENCE_TIER)
        out_path = Path(args.generate_receipt)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote receipt template: {out_path} (territory={territory}, {len(approved)} id(s))")
        return

    print(f"Found {len(approved)} approved candidate(s) (territory={territory}).")
    if dry_run:
        for c in approved:
            print(f"  [DRY RUN] would merge {c['id']}: {c['summary'][:60]}...")
        print("Dry run. Use --apply to perform merge.")
        print("To create a receipt template: --generate-receipt receipt.json --approved-by <name>")
        return

    if not args.approved_by.strip():
        raise SystemExit("--approved-by is required with --apply")
    if not args.receipt.strip() and not args.quick.strip():
        raise SystemExit("--receipt is required with --apply (or use --quick for single-candidate)")

    if args.quick.strip():
        receipt = _build_receipt(approved, args.approved_by.strip(), territory)
        receipt["min_evidence_tier"] = max(args.min_evidence_tier, MIN_EVIDENCE_TIER)
    else:
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
    pending_content = _read(RECURSION_GATE_PATH)
    # Keep pre-merge state for rollback; avoid re-reading files later
    original_files = {
        SELF_PATH: self_content,
        EVIDENCE_PATH: evidence_content,
        PROMPT_PATH: prompt_content,
        RECURSION_GATE_PATH: pending_content,
    }
    intent_profile = _load_intent_profile()
    blocks_to_move: list[str] = []
    applied_candidates: list[tuple[dict, str, str]] = []  # (c, act_id, ix_entry_id)
    pre_checksum_ok, pre_checksum = _compute_fork_checksum()
    if not pre_checksum_ok:
        _emit_validation_failure(None, f"checksum_pre_failed: {pre_checksum}", args.approved_by.strip())
        raise SystemExit(f"checksum pre-merge failed: {pre_checksum}")

    for c in approved:
        if _is_meta_infra_candidate(c):
            blocks_to_move.append(c["full_match"])
            applied_candidates.append((c, "META-INFRA", "META-INFRA"))
            print(
                f"[META_INFRA] {c['id']}: moving to Processed without SELF/EVIDENCE/prompt merge — "
                "apply infra patch manually (see docs/meta-class-proposals.md)."
            )
            continue
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
        self_content, evidence_content, prompt_content, act_id, ix_entry_id = merge_candidate_in_memory(
            c, self_content, evidence_content, prompt_content, today, evidence_tier=min_tier
        )
        blocks_to_move.append(c["full_match"])
        applied_candidates.append((c, act_id, ix_entry_id))

    rel_self = f"users/{USER_ID}/self.md"
    boundary_viol = collect_ix_a_violations_from_self_md(self_content, rel_path=rel_self)
    if boundary_viol:
        for v in boundary_viol:
            print(v, file=sys.stderr)
        _emit_validation_failure(
            None,
            "merge_preview_identity_library_boundary: " + boundary_viol[0][:300],
            args.approved_by.strip(),
        )
        raise SystemExit(
            "merge blocked: post-merge self.md would violate SELF-KNOWLEDGE vs SELF-LIBRARY "
            f"({len(boundary_viol)} IX-A issue(s)). Fix IX-A topics or reject candidates; see "
            "docs/boundary-self-knowledge-self-library.md"
        )

    # Move blocks from Candidates to Processed in recursion-gate.md
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

    file_plan = {
        SELF_PATH: self_content,
        EVIDENCE_PATH: evidence_content,
        PROMPT_PATH: prompt_content,
        RECURSION_GATE_PATH: pending_content,
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
        _refresh_derived_exports()
        print("Derived exports refreshed.")

        receipt_event = {
            **receipt,
            "merged_at": _utc_now_iso(),
            "merge_source": "process_approved_candidates",
            "checksum_before": pre_checksum,
        }
        _append_merge_receipt(receipt_event)
        print(f"Merge receipt appended: {MERGE_RECEIPTS_PATH}")

        try:
            from grace_mar.fork_lifecycle import merge_checkpoint

            merge_checkpoint(
                REPO_ROOT,
                USER_ID,
                {
                    "receipt_id": receipt.get("receipt_id"),
                    "merge_receipt_id": receipt.get("receipt_id"),
                    "candidate_ids": receipt.get("candidate_ids"),
                },
            )
        except Exception as exc:
            print(f"Warning: fork lifecycle checkpoint skipped: {exc}", file=sys.stderr)

        applied_pipeline_event_ids: list[str] = []
        staged_parent_event_ids: list[str] = []
        for c, act_id, ix_entry_id in applied_candidates:
            ev = _emit_applied_event(c, act_id, ix_entry_id, args.approved_by.strip())
            eid = ev.get("event_id")
            if eid:
                applied_pipeline_event_ids.append(str(eid))
            pid = ev.get("parent_event_id")
            if pid and str(pid) not in staged_parent_event_ids:
                staged_parent_event_ids.append(str(pid))

        harness_kw: dict = {
            "path": str(MERGE_RECEIPTS_PATH.relative_to(REPO_ROOT)),
            "candidate_ids": receipt.get("candidate_ids"),
            "approved_by": receipt.get("approved_by"),
            "merged_at": receipt_event.get("merged_at"),
            "replay_mode": "merge",
        }
        if applied_pipeline_event_ids:
            harness_kw["applied_pipeline_event_ids"] = applied_pipeline_event_ids
        if staged_parent_event_ids:
            harness_kw["staged_parent_event_ids"] = staged_parent_event_ids
        append_harness_event(
            USER_ID,
            "process_approved_candidates",
            "merge_applied",
            **harness_kw,
        )

        post_ok, post_reason = _run_integrity_validation(min_tier)
        if not post_ok:
            raise RuntimeError(f"post-merge integrity failed: {post_reason}")
        after_ok, after_checksum = _compute_fork_checksum()
        if not after_ok:
            raise RuntimeError(f"checksum post-merge failed: {after_checksum}")
        all_meta = applied_candidates and all(
            _is_meta_infra_candidate(c) for c, _act, _ix in applied_candidates
        )
        if pre_checksum == after_checksum and not all_meta:
            raise RuntimeError("checksum unchanged after merge; expected state change")

        for c, act_id, _ix in applied_candidates:
            _append_gated_evidence_log_entry(
                c["id"],
                act_id,
                c.get("channel_key") or "telegram",
                c["summary"],
                _extract_source_exchange_snippet(c["block"]),
            )
        print("self-archive.md § VIII (gated approved log) updated.")
        try:
            _append_session_log_for_merge([c["id"] for c, _, _ in applied_candidates], args.approved_by.strip())
            print("session-log.md updated.")
        except OSError as exc:
            print(f"Warning: session-log append failed: {exc}", file=sys.stderr)
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

        # Downstream harness drift: repo PRP already regenerated above; copied USER.md / OpenClaw dir may lag.
        if args.export_openclaw:
            print(
                "grace-mar: merge complete — PRP updated in-repo; OpenClaw export ran (--export-openclaw).",
                file=sys.stderr,
            )
        else:
            print(
                "grace-mar: merge complete — PRP updated in-repo. If you use OpenClaw or any external copy of "
                "USER.md/SOUL, refresh or it is stale: "
                f"python3 integrations/openclaw_hook.py --user {USER_ID} --format md+manifest --emit-event",
                file=sys.stderr,
            )
            print(
                "grace-mar: commit with [gated-merge] in the message (pre-commit commit-msg hook), "
                "or ALLOW_GATED_RECORD_EDIT=1 for emergency only.",
                file=sys.stderr,
            )
    except Exception as e:
        _emit_validation_failure(None, f"merge_apply_failed_or_rolled_back: {e}", args.approved_by.strip())
        rollback_plan = {
            SELF_PATH: original_files[SELF_PATH],
            EVIDENCE_PATH: original_files[EVIDENCE_PATH],
            PROMPT_PATH: original_files[PROMPT_PATH],
            RECURSION_GATE_PATH: original_files[RECURSION_GATE_PATH],
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
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "[gated-merge] merge approved candidates via process_approved_candidates",
            ],
            cwd=REPO_ROOT,
            check=True,
        )
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True, env={**os.environ, "GITHUB_TOKEN": token})
        print("Pushed.")


if __name__ == "__main__":
    main()
