#!/usr/bin/env python3
"""
Territory lens for RECURSION-GATE pending candidates.

WPC (work-politics): territory: work-politics
  OR legacy: work-political-consulting, work-american-politics
  OR channel_key: operator:wap (or operator:wap:*)

CLI flag remains --territory wap (alias). Everything else = companion.
"""

from __future__ import annotations

import re

# Canonical territory string for new and migrated YAML
TERRITORY_WAP = "work-politics"
TERRITORY_WAP_LEGACY = ("work-political-consulting", "work-american-politics")
CHANNEL_WAP_PREFIX = "operator:wap"


def territory_from_yaml_block(yaml_body: str) -> str:
    """Return TERRITORY_WAP (politics bucket) or 'companion'."""
    ck = re.search(r"^channel_key:\s*(.+)$", yaml_body, re.MULTILINE)
    if ck:
        k = ck.group(1).strip().strip("\"'").lower()
        if k.startswith(CHANNEL_WAP_PREFIX):
            return TERRITORY_WAP
    tm = re.search(r"^territory:\s*(.+)$", yaml_body, re.MULTILINE)
    if tm:
        t = tm.group(1).strip().strip("\"'")
        if t == TERRITORY_WAP or t in TERRITORY_WAP_LEGACY or t.lower() in (
            "wap",
            "work_american_politics",
            "work_political_consulting",
            "work_politics",
        ):
            return TERRITORY_WAP
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
    Return (wap_rows, companion_rows) where each row is
    {id, summary, territory, channel_key?} summary best-effort.
    """
    wap: list[dict] = []
    companion: list[dict] = []
    for cid, body in iter_pending_blocks(full_md):
        terr = territory_from_yaml_block(body)
        sm = re.search(r"^summary:\s*(.+)$", body, re.MULTILINE)
        summary = (sm.group(1).strip().strip("\"'") if sm else "")[:200]
        ck_m = re.search(r"^channel_key:\s*(.+)$", body, re.MULTILINE)
        channel_key = ck_m.group(1).strip().strip("\"'") if ck_m else ""
        row = {"id": cid, "summary": summary, "territory": terr, "channel_key": channel_key}
        (wap if terr == TERRITORY_WAP else companion).append(row)
    return wap, companion
