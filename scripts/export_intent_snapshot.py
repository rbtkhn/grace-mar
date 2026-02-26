#!/usr/bin/env python3
"""
Export user intent rules as machine-readable JSON.

Reads users/[id]/intent.md and writes a structured intent snapshot for
agent consumption and intent-aware validation.

Usage:
    python scripts/export_intent_snapshot.py --user grace-mar
    python scripts/export_intent_snapshot.py -u grace-mar -o users/grace-mar/intent_snapshot.json
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_yaml_block(content: str) -> str:
    m = re.search(r"```(?:yaml|yml)\s*\n(.*?)```", content, re.DOTALL)
    if not m:
        return ""
    return m.group(1)


def _top_level_scalar(block: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("\"'")


def _nested_scalar(block: str, parent: str, key: str) -> str:
    m_parent = re.search(
        rf"^{re.escape(parent)}:\s*\n((?:^[ \t]+.+\n?)*)",
        block,
        re.MULTILINE,
    )
    if not m_parent:
        return ""
    parent_block = m_parent.group(1)
    m = re.search(rf"^[ \t]+{re.escape(key)}:\s*(.+)$", parent_block, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("\"'")


def _list_block(block: str, key: str) -> list[str]:
    m = re.search(
        rf"^{re.escape(key)}:\s*\n((?:^[ \t]+-\s+.+\n?)*)",
        block,
        re.MULTILINE,
    )
    if not m:
        return []
    lines = []
    for raw in m.group(1).splitlines():
        raw = raw.strip()
        if raw.startswith("- "):
            lines.append(raw[2:].strip().strip("\"'"))
    return [x for x in lines if x]


def _tradeoff_rules(block: str) -> list[dict]:
    m = re.search(
        r"^tradeoff_rules:\s*\n((?:^[ \t]+.+\n?)*)",
        block,
        re.MULTILINE,
    )
    if not m:
        return []
    body = m.group(1)
    chunks = re.findall(r"(?:^[ \t]*-\s+.+(?:\n(?![ \t]*-\s).+)*)", body, re.MULTILINE)
    rules: list[dict] = []
    for idx, chunk in enumerate(chunks, 1):
        rid_m = re.search(r"\bid:\s*([^\n]+)", chunk)
        when_m = re.search(r"\bwhen:\s*([^\n]+)", chunk)
        prio_m = re.search(r"\bprioritize:\s*([^\n]+)", chunk)
        de_m = re.search(r"\bdeprioritize:\s*([^\n]+)", chunk)
        esc_m = re.search(r"\bescalate_if:\s*([^\n]+)", chunk)
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
        rule = {
            "id": (rid_m.group(1).strip().strip("\"'") if rid_m else f"RULE-{idx:02d}"),
            "when": (when_m.group(1).strip().strip("\"'") if when_m else ""),
            "prioritize": (prio_m.group(1).strip().strip("\"'") if prio_m else ""),
            "deprioritize": (de_m.group(1).strip().strip("\"'") if de_m else ""),
            "escalate_if": (esc_m.group(1).strip().strip("\"'") if esc_m else ""),
            "applies_to": applies_to or ["all"],
            "priority": priority,
            "conflict_strategy": (
                strategy_m.group(1).strip().strip("\"'")
                if strategy_m
                else "escalate_to_human"
            ),
        }
        rules.append(rule)
    return rules


def export_intent_snapshot(user_id: str = "grace-mar") -> dict:
    profile_dir = REPO_ROOT / "users" / user_id
    intent_path = profile_dir / "intent.md"
    raw = _read(intent_path)
    if not raw:
        return {
            "ok": False,
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "error": f"missing intent.md at {intent_path}",
            "goals": {},
            "tradeoff_rules": [],
            "escalation_rules": [],
            "never_autonomous_actions": [],
        }

    block = _extract_yaml_block(raw)
    if not block:
        return {
            "ok": False,
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "error": "intent.md missing YAML block",
            "goals": {},
            "tradeoff_rules": [],
            "escalation_rules": [],
            "never_autonomous_actions": [],
        }

    goals = {
        "primary": _nested_scalar(block, "goals", "primary"),
        "secondary": _nested_scalar(block, "goals", "secondary"),
        "tertiary": _nested_scalar(block, "goals", "tertiary"),
    }
    return {
        "ok": True,
        "user_id": user_id,
        "generated_at": datetime.now().isoformat(),
        "source": str(intent_path.relative_to(REPO_ROOT)),
        "goals": goals,
        "tradeoff_rules": _tradeoff_rules(block),
        "escalation_rules": _list_block(block, "escalation_rules"),
        "never_autonomous_actions": _list_block(block, "never_autonomous_actions"),
        "review_cadence": _top_level_scalar(block, "review_cadence"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export intent.md as intent_snapshot.json")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default="", help="Output JSON file (default: stdout)")
    args = parser.parse_args()
    payload = export_intent_snapshot(user_id=args.user)
    text = json.dumps(payload, indent=2, ensure_ascii=True) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}", file=__import__("sys").stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
