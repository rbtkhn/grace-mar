"""
Conflict detection for pipeline staging.

Compares new candidates against existing SELF profile and flags contradictions
before they hit PENDING-REVIEW. Surfaces for user resolution; does not block staging.
See docs/CONTRADICTION-RESOLUTION.md.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = Path(__file__).resolve().parent / "conflict_rules.yaml"
PROFILE_DIR = REPO_ROOT / "users" / "pilot-001"
SELF_PATH = PROFILE_DIR / "SELF.md"


def _load_rules() -> dict:
    """Load conflict rules from YAML. No PyYAML dependency — simple regex parse."""
    if not RULES_PATH.exists():
        return {"personality_opposites": []}
    content = RULES_PATH.read_text()
    pairs = []
    for m in re.finditer(r"-\s*\[\s*([^,\]]+)\s*,\s*([^\]\]]+)\s*\]", content):
        a, b = m.group(1).strip().strip('"').strip("'"), m.group(2).strip().strip('"').strip("'")
        if a and b:
            pairs.append([a, b])
    return {"personality_opposites": pairs}


def _load_self_personality_summary() -> str:
    """Extract personality-related text from SELF.md (traits + IX-C observations)."""
    if not SELF_PATH.exists():
        return ""
    content = SELF_PATH.read_text()
    parts = []

    # Seed traits: "trait: independent", "trait: creative", etc.
    for m in re.finditer(r"trait:\s*([^\n]+)", content, re.IGNORECASE):
        parts.append(m.group(1).strip().lower())

    # Seed baseline (analyst prompt style): "Personality: creative, independent, ..."
    m = re.search(r"Personality:\s*([^\n]+)", content, re.IGNORECASE)
    if m:
        parts.append(m.group(1).lower())

    # IX-C entries: observation fields
    ix_c = re.search(r"### IX-C\. PERSONALITY.*?```yaml\n(.*?)```", content, re.DOTALL)
    if ix_c:
        for obs in re.finditer(r"observation:\s*[\"']?([^\"'\n]+)", ix_c.group(1)):
            parts.append(obs.group(1).lower())

    return " ".join(parts)


def _parse_candidate_yaml(analysis_yaml: str) -> dict:
    """Extract fields from analyst YAML."""
    data = {}
    for m in re.finditer(r"^(\w+):\s*(.+?)(?=\n\w+:|$)", analysis_yaml, re.MULTILINE | re.DOTALL):
        key, val = m.group(1).lower(), m.group(2).strip().strip('"')
        data[key] = val
    return data


def check_conflicts(analysis_yaml: str) -> list[dict]:
    """
    Check new candidate against existing profile. Returns list of conflicts.

    Each conflict: {"rule": str, "existing_hint": str, "new_hint": str, "pair": [a, b]}
    """
    rules = _load_rules()
    opposites = rules.get("personality_opposites", [])
    if not opposites:
        return []

    data = _parse_candidate_yaml(analysis_yaml)
    mind_category = data.get("mind_category", "")
    if mind_category != "personality":
        return []  # v1: only check personality

    new_text = " ".join([
        data.get("suggested_entry", ""),
        data.get("summary", ""),
        data.get("prompt_addition", ""),
    ]).lower()

    existing_text = _load_self_personality_summary()
    if not new_text or not existing_text:
        return []

    # Word-boundary check: avoid "dependent" matching inside "independent"
    def _word_present(word: str, text: str) -> bool:
        return bool(re.search(rf"\b{re.escape(word)}\b", text))

    conflicts = []
    for pair in opposites:
        a, b = pair[0].lower(), pair[1].lower()
        a_in_existing = _word_present(a, existing_text)
        b_in_existing = _word_present(b, existing_text)
        a_in_new = _word_present(a, new_text)
        b_in_new = _word_present(b, new_text)
        if (a_in_existing and b_in_new) or (b_in_existing and a_in_new):
            in_profile = a if a_in_existing else b
            in_new = b if a_in_existing else a
            conflicts.append({
                "rule": "personality_opposites",
                "pair": [a, b],
                "existing_hint": f"profile has '{in_profile}'",
                "new_hint": f"candidate has '{in_new}'",
            })

    return conflicts


def format_conflicts_for_yaml(conflicts: list[dict]) -> str:
    """Format conflicts as YAML block to append to candidate."""
    if not conflicts:
        return ""
    lines = ["conflicts_detected:", "  count: " + str(len(conflicts))]
    for i, c in enumerate(conflicts, 1):
        lines.append(f"  - rule: {c['rule']}")
        lines.append(f"    pair: [{c['pair'][0]}, {c['pair'][1]}]")
        lines.append(f"    existing_hint: \"{c['existing_hint']}\"")
        lines.append(f"    new_hint: \"{c['new_hint']}\"")
    return "\n" + "\n".join(lines)
