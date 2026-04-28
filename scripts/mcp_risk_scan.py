#!/usr/bin/env python3
"""
MCP capability risk / permission scanner — reads registry + policy YAML only.

Does not execute MCP servers, use credentials, or invoke network tools.

Exit codes:
  0 — no hard blockers on admission-eligible capabilities (non-prohibition stance).
  1 — validation failure, or any hard blocker on a capability that is not
      PROHIBITED_BY_POLICY only.

See docs/mcp/mcp-risk-permission-scanner.md.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CAPABILITIES = REPO_ROOT / "config" / "mcp-capabilities.yaml"
DEFAULT_CAPABILITY_SCHEMA = REPO_ROOT / "schemas" / "mcp-capability.v1.json"
DEFAULT_POLICY = REPO_ROOT / "config" / "mcp-risk-policy.yaml"
DEFAULT_POLICY_SCHEMA = REPO_ROOT / "schemas" / "mcp-risk-scan-policy.v1.json"
DEFAULT_MARKDOWN = REPO_ROOT / "artifacts" / "mcp-risk-report.md"
DEFAULT_JSON = REPO_ROOT / "artifacts" / "mcp-risk-report.json"

# --- Pattern needles (lowercase matching on joined capability strings) ---
_SHELL_ALLOWED = (
    "shell_execute",
    "execute_command",
    "run_command",
    "subprocess",
    "subprocess_spawn",
    "interactive_terminal",
    "/bin/sh",
    "/bin/bash",
    "powershell",
    "cmd.exe",
    "terminal",
)
_MERGE_FORCE_ALLOWED = (
    "merge_to_main",
    "merge_pr",
    "force_push",
    "bypass_review",
    "push_commit",
    "delete_branch",
)
_CREDENTIAL_EXFIL = (
    "credential_exfiltration",
    "exfiltrate",
    "steal_secret",
    "steal_token",
)
_CANONICAL_WRITE_FRAGMENTS = (
    "users/grace-mar/self.md",
    "users/grace-mar/self-archive",
    "users/grace-mar/recursion-gate",
)
_MEMORY_WRITE_FRAGMENTS = (
    "upsert",
    "vector",
    "embedding",
    "thoughts_row",
    "silent_profile",
)
_GITHUB_REQUIRED_PROHIBITIONS = ("merge_to_main", "force_push", "bypass_review")

# Hard blocker ids suppressed for PROHIBITED_BY_POLICY stance (declarative prohibition rows).
PERMISSIVE_HARD_BLOCKERS: frozenset[str] = frozenset(
    {
        "shell_execute",
        "execute_command",
        "run_command",
        "merge_to_main",
        "force_push",
        "bypass_review",
        "credential_exfiltration",
        "direct_canonical_evidence_append",
        "external_memory_write_without_review",
    }
)


def _git_short_hash(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return "unknown"


def load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("PyYAML required (pip install -r requirements-dev.txt)") from e
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_json_schema(instance: Any, schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as e:
        raise RuntimeError("jsonschema required (pip install -r requirements-dev.txt)") from e
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)


def _hay(parts: list[str] | None) -> str:
    if not parts:
        return ""
    return " ".join(parts).lower()


def _write_capable(cap: dict[str, Any]) -> bool:
    return bool(cap.get("writes")) or bool(cap.get("durable_state_write"))


def dangerous_shell_in_hay(hay: str) -> bool:
    return any(n in hay for n in _SHELL_ALLOWED)


def dangerous_merge_in_hay(hay: str) -> bool:
    return any(n in hay for n in _MERGE_FORCE_ALLOWED)


def credential_exfil_in_hay(hay: str) -> bool:
    return any(n in hay for n in _CREDENTIAL_EXFIL)


def canonical_record_in_writes(cap: dict[str, Any]) -> bool:
    wh = _hay(cap.get("writes") or [])
    return any(f in wh for f in _CANONICAL_WRITE_FRAGMENTS)


def direct_canonical_append_in_allowed(hay: str) -> bool:
    return (
        "append_canonical_evidence" in hay
        or "silent_profile_merge" in hay
        or "direct canonical evidence" in hay
    )


def scm_needs_github_prohibitions(cap: dict[str, Any]) -> bool:
    if cap.get("category") != "scm":
        return False
    if cap.get("network_access") == "full":
        return True
    return bool(cap.get("writes"))


def github_prohibitions_complete(cap: dict[str, Any]) -> bool:
    ph = _hay(cap.get("prohibited_actions") or [])
    return all(req in ph for req in _GITHUB_REQUIRED_PROHIBITIONS)


def is_prohibited_by_policy_stance(cap: dict[str, Any]) -> bool:
    """
    Intentional prohibition-only registry rows: output_lane prohibited and no
    dangerous permission expressed in allowed_actions/writes (danger may appear in prohibited_actions).
    """
    if cap.get("output_lane") != "prohibited":
        return False
    ah = _hay(cap.get("allowed_actions") or [])
    wh = _hay(cap.get("writes") or [])
    combined = ah + " " + wh
    if dangerous_shell_in_hay(combined):
        return False
    if dangerous_merge_in_hay(combined):
        return False
    if credential_exfil_in_hay(combined):
        return False
    if canonical_record_in_writes(cap):
        return False
    if direct_canonical_append_in_allowed(combined):
        return False
    # Memory upsert in allowed/writes would contradict prohibition-only stance
    if cap.get("category") == "memory":
        mem = combined + _hay(cap.get("writes") or [])
        if any(x in mem for x in _MEMORY_WRITE_FRAGMENTS):
            return False
    return True


def evaluate_capability(cap: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Return one finding dict for Markdown/JSON/tests."""
    weights: dict[str, int] = policy["risk_weights"]
    thresholds: dict[str, Any] = policy["risk_thresholds"]
    recs: dict[str, str] = policy["recommendations"]
    cid = cap["id"]

    ahay = _hay(cap.get("allowed_actions") or [])
    whay = _hay(cap.get("writes") or [])
    phay = _hay(cap.get("prohibited_actions") or [])
    allowed_writes_hay = ahay + " " + whay

    prohibited_stance = is_prohibited_by_policy_stance(cap)
    score = 0
    breakdown: dict[str, int] = {}

    def bump(wkey: str) -> None:
        nonlocal score
        v = weights[wkey]
        score += v
        breakdown[wkey] = breakdown.get(wkey, 0) + v

    if cap.get("credential_requirements") == "required":
        bump("credential_required")
    if cap.get("network_access") == "full":
        bump("network_full")
    if cap.get("writes"):
        bump("writes_nonempty")
    if cap.get("durable_state_write"):
        bump("durable_state_write")
    loc = cap.get("local_or_cloud")
    if loc == "cloud":
        bump("cloud")
    elif loc == "hybrid":
        bump("hybrid")

    # Shell / SCM / memory patterns — score only from permissive surfaces (allowed + writes).
    shell_surface = allowed_writes_hay
    if not prohibited_stance:
        if cap.get("category") == "shell":
            bump("shell_execution")
        elif dangerous_shell_in_hay(shell_surface):
            bump("shell_execution")
        if dangerous_merge_in_hay(shell_surface):
            bump("scm_merge_or_force")
        memhw = whay + ahay
        if any(x in memhw for x in ("insert", "update", "ddl", "upsert", "vector")):
            if cap.get("category") in ("database", "memory"):
                bump("memory_or_database_write")

    if canonical_record_in_writes(cap):
        bump("canonical_record_write")

    if not cap.get("requires_receipt"):
        bump("receipt_missing")
    if not cap.get("gate_required_for_record_change"):
        bump("gate_missing")

    if scm_needs_github_prohibitions(cap) and not github_prohibitions_complete(cap):
        bump("missing_github_prohibitions")

    risk_level = tier_for_score(score, thresholds)
    recommendation = recs[risk_level]

    hard_blockers: list[str] = []
    warnings: list[str] = []

    if scm_needs_github_prohibitions(cap) and not github_prohibitions_complete(cap):
        miss = [r for r in _GITHUB_REQUIRED_PROHIBITIONS if r not in phay]
        warnings.append(
            f"`{cid}` (scm): prohibited_actions missing recommended tokens: {', '.join(miss)}"
        )

    # Hard blockers (structural + permissive)
    if cap.get("category") == "shell" and not prohibited_stance:
        hard_blockers.append("shell_execute")

    if not prohibited_stance:
        if dangerous_shell_in_hay(allowed_writes_hay):
            hard_blockers.append("shell_execute")
        if any(x in ahay for x in ("execute_command", "run_command")):
            hard_blockers.extend([b for b in ("execute_command", "run_command") if b in ahay])
        if dangerous_merge_in_hay(allowed_writes_hay):
            merged_h = allowed_writes_hay
            if "merge_to_main" in merged_h or "merge_pr" in merged_h:
                hard_blockers.append("merge_to_main")
            if "force_push" in merged_h:
                hard_blockers.append("force_push")
            if "bypass_review" in merged_h:
                hard_blockers.append("bypass_review")
            if "push_commit" in merged_h:
                hard_blockers.append("merge_to_main")
            if "delete_branch" in merged_h:
                hard_blockers.append("merge_to_main")
        if credential_exfil_in_hay(allowed_writes_hay):
            hard_blockers.append("credential_exfiltration")
        if direct_canonical_append_in_allowed(ahay) and "without_review" not in phay:
            hard_blockers.append("direct_canonical_evidence_append")

    if canonical_record_in_writes(cap):
        wh = _hay(cap.get("writes") or [])
        if "users/grace-mar/self.md" in wh:
            hard_blockers.append("write_users_grace_mar_self_md")
        if "self-archive" in wh:
            hard_blockers.append("write_users_grace_mar_self_archive_md")
        if "recursion-gate" in wh:
            hard_blockers.append("write_users_grace_mar_recursion_gate_md")

    if cap.get("durable_state_write") and not cap.get("gate_required_for_record_change"):
        hard_blockers.append("durable_state_write_without_gate")

    if cap.get("writes") and not cap.get("requires_receipt"):
        hard_blockers.append("write_without_receipt")

    # External memory write posture
    if cap.get("category") == "memory" and not prohibited_stance:
        mem_surface = ahay + whay
        has_mem_write = any(x in mem_surface for x in _MEMORY_WRITE_FRAGMENTS)
        has_review_prohibitions = "upsert_embedding_store" in phay and "silent_profile_merge" in phay
        if has_mem_write and cap.get("writes") and not has_review_prohibitions:
            hard_blockers.append("external_memory_write_without_review")

    # De-dupe preserve order
    seen: set[str] = set()
    hb: list[str] = []
    for b in hard_blockers:
        if b not in seen:
            seen.add(b)
            hb.append(b)

    # PROHIBITED_BY_POLICY rows: drop permissive blockers only (structural contradictions still fail).
    if prohibited_stance:
        hb = [b for b in hb if b not in PERMISSIVE_HARD_BLOCKERS]

    return {
        "id": cid,
        "name": cap.get("name", ""),
        "score": score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "prohibited_by_policy": prohibited_stance,
        "hard_blockers": hb,
        "warnings": warnings,
        "score_breakdown": breakdown,
    }


def tier_for_score(score: int, thresholds: dict[str, Any]) -> str:
    if score <= thresholds["low"]["max"]:
        return "low"
    if score <= thresholds["medium"]["max"]:
        return "medium"
    if score <= thresholds["high"]["max"]:
        return "high"
    return "critical"


def scan_passes(findings: list[dict[str, Any]]) -> bool:
    for f in findings:
        if f["prohibited_by_policy"]:
            continue
        if f["hard_blockers"]:
            return False
    return True


def build_markdown(
    *,
    findings: list[dict[str, Any]],
    policy_path: Path,
    caps_path: Path,
    generated_at_utc: str,
    git_ref: str,
    passes: bool,
) -> str:
    lines = [
        "# MCP risk / permission scan report",
        "",
        f"- **Generated (UTC):** {generated_at_utc}",
        f"- **Git:** `{git_ref}`",
        f"- **Capabilities:** `{caps_path.relative_to(REPO_ROOT)}`",
        f"- **Policy:** `{policy_path.relative_to(REPO_ROOT)}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Pass (no hard blockers on admission-eligible capabilities)** | `{str(passes).lower()}` |",
        f"| **Capabilities checked** | {len(findings)} |",
    ]
    tier_counts: dict[str, int] = {}
    for f in findings:
        tier_counts[f["risk_level"]] = tier_counts.get(f["risk_level"], 0) + 1
    for tier in ("low", "medium", "high", "critical"):
        lines.append(f"| **Tier: {tier}** | {tier_counts.get(tier, 0)} |")

    blk_n = sum(len(f["hard_blockers"]) for f in findings if not f["prohibited_by_policy"])
    lines.extend(["", f"| **Hard blocker hits (non-prohibition stance)** | {blk_n} |", ""])

    lines.extend(
        [
            "## Final status",
            "",
            "**PASS** — no hard blockers on admission-eligible capabilities."
            if passes
            else "**FAIL** — hard blockers present; fix registry or classify as prohibited-only before admission.",
            "",
            "## Capability findings",
            "",
        ]
    )

    for f in sorted(findings, key=lambda x: x["id"]):
        lines.append(f"### `{f['id']}`")
        lines.append("")
        lines.append(f"- **Score:** {f['score']}")
        lines.append(f"- **Risk level:** `{f['risk_level']}`")
        lines.append(f"- **Recommendation:** `{f['recommendation']}`")
        lines.append(f"- **PROHIBITED_BY_POLICY stance:** `{str(f['prohibited_by_policy']).lower()}`")
        if f["hard_blockers"]:
            lines.append("- **Hard blockers:**")
            for b in f["hard_blockers"]:
                lines.append(f"  - `{b}`")
        else:
            lines.append("- **Hard blockers:** _none_")
        if f["warnings"]:
            lines.append("- **Warnings:**")
            for w in f["warnings"]:
                lines.append(f"  - {w}")
        lines.append("- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.")
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "This scanner evaluates **permission posture**, not factual truth of MCP claims. Passing does **not** approve live MCP integration.",
            "",
        ]
    )
    return "\n".join(lines)


def build_json_report(
    *,
    findings: list[dict[str, Any]],
    passes: bool,
    caps_path: Path,
    policy_path: Path,
    generated_at_utc: str,
    git_ref: str,
) -> dict[str, Any]:
    agg_blockers: list[str] = []
    agg_warnings: list[str] = []
    for f in findings:
        if not f["prohibited_by_policy"]:
            agg_blockers.extend(f["hard_blockers"])
        agg_warnings.extend(f["warnings"])
    return {
        "schema_version": 1,
        "generated_at_utc": generated_at_utc,
        "repo_git_ref": git_ref,
        "capabilities_path": str(caps_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "policy_path": str(policy_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "pass": passes,
        "capabilities_checked": len(findings),
        "findings": findings,
        "blockers": sorted(set(agg_blockers)),
        "warnings": agg_warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="MCP capability risk / permission scanner (read-only).")
    ap.add_argument("--capabilities", type=Path, default=DEFAULT_CAPABILITIES)
    ap.add_argument("--capability-schema", type=Path, default=DEFAULT_CAPABILITY_SCHEMA)
    ap.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    ap.add_argument("--policy-schema", type=Path, default=DEFAULT_POLICY_SCHEMA)
    ap.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    ap.add_argument(
        "--json",
        type=Path,
        nargs="?",
        const=DEFAULT_JSON,
        default=None,
        help=f"Write JSON report (default if flag present: {DEFAULT_JSON.relative_to(REPO_ROOT)})",
    )
    args = ap.parse_args()

    caps_path = args.capabilities.resolve()
    cap_schema = args.capability_schema.resolve()
    policy_path = args.policy.resolve()
    pol_schema = args.policy_schema.resolve()

    try:
        caps_doc = load_yaml(caps_path)
        validate_json_schema(caps_doc, cap_schema)
        policy_doc = load_yaml(policy_path)
        validate_json_schema(policy_doc, pol_schema)
    except Exception as e:
        print(f"mcp_risk_scan: validation failed: {e}", file=sys.stderr)
        return 1

    findings = [evaluate_capability(c, policy_doc) for c in caps_doc["capabilities"]]
    passes = scan_passes(findings)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    gref = _git_short_hash(REPO_ROOT)

    md = build_markdown(
        findings=findings,
        policy_path=policy_path,
        caps_path=caps_path,
        generated_at_utc=ts,
        git_ref=gref,
        passes=passes,
    )
    out_md = args.markdown.resolve()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(md, encoding="utf-8")

    if args.json is not None:
        js = build_json_report(
            findings=findings,
            passes=passes,
            caps_path=caps_path,
            policy_path=policy_path,
            generated_at_utc=ts,
            git_ref=gref,
        )
        out_js = args.json.resolve()
        out_js.parent.mkdir(parents=True, exist_ok=True)
        out_js.write_text(json.dumps(js, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"mcp_risk_scan: Wrote {out_md.relative_to(REPO_ROOT)} pass={passes}", file=sys.stderr)
    return 0 if passes else 1


if __name__ == "__main__":
    sys.exit(main())
