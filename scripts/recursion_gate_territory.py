#!/usr/bin/env python3
"""
Territory lens for RECURSION-GATE pending candidates.

Work-politics bucket: territory: work-politics
  OR legacy: work-political-consulting, work-american-politics
  OR channel_key: operator:pol / operator:pol:* (preferred) or operator:wap / operator:wap:* (legacy)

CLI: --territory work-politics (preferred), or shorthand pol / wp, or legacy wap.
Everything else = companion.
"""

from __future__ import annotations

import re

# Canonical territory string for new and migrated YAML
TERRITORY_WORK_POLITICS = "work-politics"
# Human-facing label for dashboards / review UIs (matches "Companion" casing)
TERRITORY_LABEL_WORK_POLITICS = "Work-politics"
TERRITORY_WORK_POLITICS_LEGACY = ("work-political-consulting", "work-american-politics")
# channel_key prefixes (pol preferred in new YAML; wap still accepted)
CHANNEL_PREFIXES_WORK_POLITICS = ("operator:pol", "operator:wap")

# Backward compatibility — deprecated names (avoid in new code)
TERRITORY_WAP = TERRITORY_WORK_POLITICS
TERRITORY_LABEL_WAP = TERRITORY_LABEL_WORK_POLITICS
TERRITORY_WAP_LEGACY = TERRITORY_WORK_POLITICS_LEGACY

# CLI/API tokens that mean "work-politics bucket" (merge receipts prefer work-politics).
TERRITORY_CLI_WORK_POLITICS_ALIASES = frozenset({"pol", "wap", "wp", "work-politics"})


def normalize_territory_cli(s: str) -> str:
    """
    Normalize --territory (or HTTP/API) values.

    Maps pol, wap, wp, work-politics -> work-politics. Leaves all and companion unchanged.
    """
    key = (s or "").strip().lower()
    if key in TERRITORY_CLI_WORK_POLITICS_ALIASES:
        return TERRITORY_WORK_POLITICS
    return key


def territory_cli_argparse_choices() -> tuple[str, ...]:
    """Allowed values for argparse --territory across operator scripts."""
    return ("all", "companion", "pol", "wap", "wp", "work-politics")


def channel_key_is_work_politics(k: str) -> bool:
    low = (k or "").strip().lower()
    return any(low.startswith(p) for p in CHANNEL_PREFIXES_WORK_POLITICS)


def territory_from_yaml_block(yaml_body: str) -> str:
    """Return TERRITORY_WORK_POLITICS (politics bucket) or 'companion'."""
    ck = re.search(r"^channel_key:\s*(.+)$", yaml_body, re.MULTILINE)
    if ck:
        k = ck.group(1).strip().strip("\"'")
        if channel_key_is_work_politics(k):
            return TERRITORY_WORK_POLITICS
    tm = re.search(r"^territory:\s*(.+)$", yaml_body, re.MULTILINE)
    if tm:
        t = tm.group(1).strip().strip("\"'")
        if t == TERRITORY_WORK_POLITICS or t in TERRITORY_WORK_POLITICS_LEGACY or t.lower() in (
            "pol",
            "wap",
            "work_american_politics",
            "work_political_consulting",
            "work_politics",
        ):
            return TERRITORY_WORK_POLITICS
    return "companion"


def iter_pending_blocks(full_md: str):
    """Yield (candidate_id, yaml_body) for each pending CANDIDATE block."""
    for m in re.finditer(
        r"###\s*(CANDIDATE-\d+).*?```yaml\s*\n(.*?)```",
        full_md,
        re.DOTALL,
    ):
        if not re.search(r"status:\s*pending\b", m.group(2)):
            continue
        yield m.group(1), m.group(2)


def pending_by_territory(full_md: str) -> tuple[list[dict], list[dict]]:
    """
    Return (work_politics_rows, companion_rows) where each row is
    {id, summary, territory, channel_key?} summary best-effort.
    """
    politics: list[dict] = []
    companion: list[dict] = []
    for cid, body in iter_pending_blocks(full_md):
        terr = territory_from_yaml_block(body)
        sm = re.search(r"^summary:\s*(.+)$", body, re.MULTILINE)
        summary = (sm.group(1).strip().strip("\"'") if sm else "")[:200]
        ck_m = re.search(r"^channel_key:\s*(.+)$", body, re.MULTILINE)
        channel_key = ck_m.group(1).strip().strip("\"'") if ck_m else ""
        row = {"id": cid, "summary": summary, "territory": terr, "channel_key": channel_key}
        (politics if terr == TERRITORY_WORK_POLITICS else companion).append(row)
    return politics, companion
