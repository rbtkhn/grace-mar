#!/usr/bin/env python3
"""
Generate a one-prompt-per-day lesson for the human companion to paste into ChatGPT or Grok.

Reads Record (self.md, skill-think.md, skill-work.md), extracts IX-A/B, edge, goals,
and fills the minimal prompt shape from docs/skill-work/skill-work-lesson-generation-walkthrough.md §3.

Design: structure+execution (human provides structure via prompt; LLM executes), evidence-first
(base activities on Record; "We did [X]" for handback). Rules from lesson-rules-config.yaml.
Output: one text block for copy-paste. Run once per day; regenerate after "we did X" merges.

Usage:
    python scripts/generate_lesson_prompt.py -u grace-mar
    python scripts/generate_lesson_prompt.py -u grace-mar -o docs/skill-work/sample-lesson-prompt-grace-mar.txt
    python scripts/generate_lesson_prompt.py -u grace-mar -n Abby -o lesson.txt
    python scripts/generate_lesson_prompt.py -u grace-mar --alpha-school --focus reading
    python scripts/generate_lesson_prompt.py -u grace-mar --tier specialized --focus math
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_WORK_DIR = REPO_ROOT / "docs" / "skill-work"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _section(content: str, title: str) -> str | None:
    """Extract section between ## TITLE and next ## or end."""
    pattern = rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _yaml_value(content: str, key: str) -> str | None:
    """Extract YAML scalar value."""
    pattern = rf"{key}:\s*(.+?)(?:\n|$)"
    m = re.search(pattern, content)
    if m:
        return m.group(1).split("#")[0].strip().strip('"\'')
    return None


def _yaml_list(content: str, key: str) -> list[str]:
    """Extract YAML list: key: [a, b] or key: \n  - a."""
    pattern = rf"{key}:\s*\[(.*?)\]"
    m = re.search(pattern, content, re.DOTALL)
    if m:
        raw = m.group(1)
        return [x.strip().split("#")[0].strip().strip('"\'') for x in re.split(r"[, \n]", raw) if x.strip()]
    pattern2 = rf"{key}:\s*\n((?:\s+-\s+[^\n]+\n?)+)"
    m2 = re.search(pattern2, content)
    if m2:
        lines = m2.group(1).strip().split("\n")
        return [re.sub(r"^\s*-\s+", "", ln).split("#")[0].strip().strip('"\'') for ln in lines if ln.strip()]
    return []


def _extract_identity(self_content: str) -> dict:
    block = _section(self_content, "I. IDENTITY") or ""
    out = {}
    m = re.search(r"name:\s*(.+)", block)
    if m:
        out["name"] = m.group(1).split("#")[0].strip().strip('"\'')
    m = re.search(r"age:\s*(\d+)", block)
    if m:
        out["age"] = m.group(1)
    langs = _yaml_list(block, "languages")
    if langs:
        out["languages"] = ", ".join(langs)
    return out


def _extract_learn_topics(self_content: str, max_entries: int = 30) -> list[str]:
    """Extract LEARN topic strings from IX-A."""
    topics = []
    for m in re.finditer(r'id:\s+LEARN-\d+.*?topic:\s*"([^"]+)"', self_content, re.DOTALL):
        t = m.group(1).strip()
        if t and len(topics) < max_entries:
            topics.append(t)
    return topics


def _extract_cur_topics(self_content: str, max_entries: int = 15) -> list[str]:
    """Extract CUR topic strings from IX-B."""
    topics = []
    for m in re.finditer(r'id:\s+CUR-\d+.*?topic:\s*"([^"]+)"', self_content, re.DOTALL):
        t = m.group(1).strip()
        if t and len(topics) < max_entries:
            topics.append(t)
    return topics


def _extract_who_she_is(self_content: str, skill_work: str, identity: dict) -> str:
    """Build WHO SHE IS summary from SELF + skill-work companion_creative_context."""
    parts = []
    prefs = _section(self_content, "II. PREFERENCES (Survey Seeded)") or ""
    personality = _section(self_content, "IV. PERSONALITY") or ""
    interests = _section(self_content, "V. INTERESTS") or ""

    # Traits (creative, kind, brave)
    for m in re.finditer(r"trait:\s+(\w+).*?notes:\s*[\"']?([^\"\n]+)", personality, re.DOTALL):
        trait = m.group(1).strip().lower()
        if trait in ("creative", "kind", "brave", "persistent", "observational"):
            parts.append(trait)
    trait_str = ", ".join(parts[:3]) if parts else "creative, kind, and brave"

    # Interests: books, music, activities
    books = _yaml_list(prefs, "books")
    music = _yaml_list(prefs, "music")
    activities = _yaml_list(prefs, "activities")
    interest_bits = []
    if books:
        interest_bits.append(f"stories ({', '.join(books[:3])})")
    if "Classical music" in str(music) or "Nutcracker" in str(music):
        interest_bits.append("classical music/ballet (The Nutcracker, Coppélia)")
    if activities:
        for a in activities:
            if "Art" in a or "Drawing" in a:
                interest_bits.append("art")
                break
    if not interest_bits:
        interest_bits = ["stories", "animals", "space", "art"]
    interests_str = ", ".join(interest_bits)

    # Companion creative context (from skill-work)
    ctx_block = re.search(r"companion_creative_context:(.*?)(?=\n\w+:|```|\Z)", skill_work, re.DOTALL)
    ctx = ctx_block.group(1) if ctx_block else ""
    primary = _yaml_value(ctx, "primary_medium")
    env = _yaml_value(ctx, "environment")
    finishing = _yaml_value(ctx, "finishing")
    creative_note = ""
    if primary or env or finishing:
        creative_parts = []
        if primary:
            creative_parts.append(f"draw with {primary}")
        if env:
            creative_parts.append(f"she {env}")
        if finishing:
            creative_parts.append("finishes what she starts")
        creative_note = " She likes to " + "; ".join(creative_parts) + "." if creative_parts else ""

    # Learning style (from reasoning/emotional patterns)
    learn_note = " She learns by watching first, then trying; she gets upset sometimes but keeps trying."
    verbal = " She uses \"and\" and \"because\" a lot when she talks."
    fav = " Her favorite subject is science."

    name = identity.get("name", "Grace-Mar")
    return f"{name} is {trait_str}. She loves {interests_str}.{creative_note}{learn_note}{verbal}{fav} Do not add facts or stories not listed below."


def _extract_skills_edge(content: str, container: str) -> str | None:
    """Extract edge from a skill container block."""
    # Find container block (## THINK, ## MATH, etc.)
    pattern = rf"## {re.escape(container)}.*?edge:\s*[\"']([^\"']+)[\"']"
    m = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    pattern2 = rf"## {re.escape(container)}.*?edge:\s*(\S.+?)(?=\n\s+\w+:|\n\s*#|\n```|\Z)"
    m2 = re.search(pattern2, content, re.DOTALL | re.IGNORECASE)
    return m2.group(1).strip().strip('"\'') if m2 else None


def _extract_think_edge(think_content: str) -> str:
    block = _section(think_content, "THINK Container") or ""
    m = re.search(r'edge:\s*["\']([^"\']+)["\']', block)
    return m.group(1).strip() if m else "Longer independent text; early chapter books; inference questions; retelling."


def _extract_math_edge(think_content: str) -> str:
    block = _section(think_content, "MATH (contextual") or ""
    if not block:
        block = re.search(r"## MATH.*?(?=## |\Z)", think_content, re.DOTALL)
        block = block.group(0) if block else ""
    m = re.search(r'edge:\s*["\']([^"\']+)["\']', block)
    return m.group(1).strip() if m else "Telling time; place value; double-digit operations"


def _extract_chinese_edge(think_content: str) -> str:
    block = _section(think_content, "CHINESE (contextual") or ""
    if not block:
        block = re.search(r"## CHINESE.*?(?=## |\Z)", think_content, re.DOTALL)
        block = block.group(0) if block else ""
    m = re.search(r'edge:\s*["\']([^"\']+)["\']', block)
    return m.group(1).strip() if m else "First character recognition"


def _extract_work_edge(work_content: str) -> str:
    block = _section(work_content, "WORK Container") or ""
    m = re.search(r'edge:\s*["\']([^"\']+)["\']', block)
    return m.group(1).strip() if m else "Narrative creation from prompts; plan 3 steps for a small project"


def _extract_work_goals(work_content: str) -> list[str]:
    block = _section(work_content, "WORK GOALS") or ""
    horizon = _yaml_list(block, "horizon")
    return horizon if isinstance(horizon, list) else []


def _extract_school(work_content: str) -> dict:
    block = _section(work_content, "SCHOOL (contextual") or ""
    if not block:
        block = re.search(r"## SCHOOL.*?(?=## |\Z)", work_content, re.DOTALL)
        block = block.group(0) if block else ""
    grade = _yaml_value(block, "grade")
    return {"grade": grade} if grade else {}


def _extract_companion_creative(work_content: str) -> dict:
    """Extract companion_creative_context from skill-work."""
    block = re.search(r"companion_creative_context:(.*?)(?=\n\w+:|```|\Z)", work_content, re.DOTALL)
    if not block:
        return {}
    ctx = block.group(1)
    out = {}
    for key in ["primary_medium", "environment", "finishing", "one_word_style"]:
        val = _yaml_value(ctx, key)
        if val:
            out[key] = val
    return out


def _parse_yaml_list(block: str) -> list[str]:
    """Parse a YAML list block (lines with - item). Don't strip block; strip removes leading spaces from first line."""
    items = []
    for ln in block.split("\n"):
        ln = ln.rstrip()
        if not ln or not re.match(r"\s+-\s+", ln):
            continue
        m = re.match(r'\s+-\s+"(.+)"\s*$', ln)
        if m:
            items.append(m.group(1).replace('\\"', '"'))
        else:
            m2 = re.match(r"\s+-\s+(.+)\s*$", ln)
            if m2:
                items.append(m2.group(1).strip().strip("'\""))
    return items


def _load_lesson_rules_config() -> dict:
    """Load lesson-rules-config.yaml. Returns dict with constraints (musts, must_nots, preferences, escalation)
    or rules_list for backward compatibility. Prefers constraints when present."""
    path = SKILL_WORK_DIR / "lesson-rules-config.yaml"
    if not path.exists():
        return {}
    content = _read(path)
    out: dict = {}

    # Load constraints (musts, must_nots, preferences, escalation)
    constraints_block = re.search(
        r"^constraints:\s*\n((?:\s+(?:musts|must_nots|preferences|escalation):\s*\n(?:\s+-\s+.*\n?)+)+)",
        content,
        re.MULTILINE,
    )
    if constraints_block:
        block = constraints_block.group(1)
        for section in ["musts", "must_nots", "preferences", "escalation"]:
            m = re.search(rf"^\s+{re.escape(section)}:\s*\n((?:\s+-\s+.*\n?)+)", block, re.MULTILINE)
            if m:
                out[section] = _parse_yaml_list(m.group(1))

    # Fallback: flat rules
    rules_block = re.search(r"^rules:\s*\n((?:\s+-\s+.*\n?)+)", content, re.MULTILINE)
    if rules_block:
        out["rules_list"] = _parse_yaml_list(rules_block.group(1))

    # Difficulty (mirrors self-library maturity)
    diff_block = re.search(
        r"^difficulty:\s*\n((?:\s+\w+:.*\n?)+)",
        content,
        re.MULTILINE,
    )
    if diff_block:
        block = diff_block.group(1)
        m = re.search(r"default:\s*(\d+)", block)
        if m:
            out["difficulty_default"] = int(m.group(1))
        m = re.search(r"reading_max_maturity:\s*(\d+)", block)
        if m:
            out["difficulty_reading_max_maturity"] = int(m.group(1))
        for i in [1, 2, 3]:
            m = re.search(rf"^\s+{i}:\s*[\"'](.+?)[\"']\s*$", block, re.MULTILINE)
            if m:
                if "difficulty_descriptions" not in out:
                    out["difficulty_descriptions"] = {}
                out["difficulty_descriptions"][i] = m.group(1)

    return out


def _load_alpha_school_block() -> dict:
    """Load two_hour_block from alpha-school-benchmarks.yaml."""
    path = SKILL_WORK_DIR / "skill-work-alpha-school" / "alpha-school-benchmarks.yaml"
    if not path.exists():
        return {}
    content = _read(path)
    block = re.search(r"two_hour_block:\s*\n((?:\s+[\w_]+:.*\n?)+)", content)
    if not block:
        return {}
    section = block.group(1)
    out = {}
    m = re.search(r"segment_minutes:\s*\[(\d+),\s*(\d+)\]", section)
    if m:
        out["segment_minutes"] = [int(m.group(1)), int(m.group(2))]
    m = re.search(r"mastery_threshold_percent:\s*(\d+)", section)
    if m:
        out["mastery_threshold_percent"] = int(m.group(1))
    m = re.search(r"in_lesson_success_rate_percent:\s*\[(\d+),\s*(\d+)\]", section)
    if m:
        out["in_lesson_success_rate_percent"] = [int(m.group(1)), int(m.group(2))]
    return out


def _extract_lexile(self_content: str) -> str:
    m = re.search(r"lexile_output:\s*[\"']?(\d+)L", self_content)
    return m.group(1) + "L" if m else "600L"


def _extract_lexile_input(self_content: str) -> str:
    m = re.search(r"lexile_input:\s*[\"']?([\d\-]+L)", self_content)
    return m.group(1) if m else "400–500L"


def generate_lesson_prompt(
    user_id: str = "grace-mar",
    name_override: str | None = None,
    alpha_school: bool = False,
    focus: str | None = None,
    tier: str = "elementary",
) -> str:
    """Build one-prompt-per-day lesson from Record. Returns text for copy-paste."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_content = _read(profile_dir / "self.md")
    think_content = _read(profile_dir / "skill-think.md")
    work_content = _read(profile_dir / "skill-work.md")

    if not self_content:
        return f"# Lesson Prompt — {user_id}\n\nNo self.md found at {profile_dir / 'self.md'}.\n"

    identity = _extract_identity(self_content)
    name = name_override or identity.get("name", "Grace-Mar")
    age = identity.get("age", "6")
    languages = identity.get("languages", "English and Chinese")

    ix_a = _extract_learn_topics(self_content)
    ix_b = _extract_cur_topics(self_content)
    who_she_is = _extract_who_she_is(self_content, work_content, identity)

    think_edge = _extract_think_edge(think_content)
    math_edge = _extract_math_edge(think_content)
    chinese_edge = _extract_chinese_edge(think_content)
    work_edge = _extract_work_edge(work_content)

    work_goals = _extract_work_goals(work_content)
    school = _extract_school(work_content)
    grade = school.get("grade", "first grade")

    lexile = _extract_lexile(self_content)
    lexile_input = _extract_lexile_input(self_content)

    # Build prompt body (everything below ---)
    alpha_note = " Alpha-school design: 4 segments of 25–30 min, 90% mastery to advance, 80–85% in-lesson success." if alpha_school else ""
    lines = [
        f"You are a patient tutor for {name} (Grace-Mar), a {age}-year-old girl in {grade}. She speaks {languages}. Use ONLY the information below. Speak at her level: short sentences, simple words (Lexile ~{lexile} output). This prompt is for the whole day — run 3–5 short activities in this thread, up to 2 hours total screen-based learning.{alpha_note}",
        "",
        "WHO SHE IS",
        who_she_is,
        "",
        "WHAT SHE KNOWS (IX-A) — use for hints and as content boundary",
    ]
    for t in ix_a:
        lines.append(f"- {t}")

    lines.extend(["", "WHAT SHE'S CURIOUS ABOUT (IX-B) — lean into these for topics"])
    for t in ix_b:
        lines.append(f"- {t}")

    lines.extend([
        "",
        "WHERE SHE'S AT (EDGE) — teach just above this",
        f"- Reading (THINK): {think_edge}. Lexile input {lexile_input}; next milestone 600L (early chapter books, short nonfiction).",
        f"- Math: {math_edge}",
        f"- Chinese: {chinese_edge}",
        f"- Making/planning (WORK): {work_edge}",
        "",
    ])

    # DIFFICULTY (mirrors self-library maturity 1–3)
    rules_cfg = _load_lesson_rules_config()
    diff_default = rules_cfg.get("difficulty_default", 2)
    diff_read_max = rules_cfg.get("difficulty_reading_max_maturity", 2)
    diff_descriptions = rules_cfg.get("difficulty_descriptions") or {}
    diff_label = diff_descriptions.get(diff_default, f"Maturity {diff_default}")
    lines.extend([
        "DIFFICULTY (mirrors self-library maturity; scope activities and reading sources)",
        f"- Target: maturity {diff_default} ({diff_label}).",
        f"- For reading: use LIBRARY entries with maturity ≤ {diff_read_max} when suggesting or drawing from books.",
        "- Math and WORK: keep prompts and steps at this tier (single-step vs multi-step, edge vocabulary).",
        "",
        "TODAY'S GOALS (in this thread)",
    ])

    sat_line = f"Long-term: SAT readiness (goal ≥1200)." if any("SAT" in str(g) for g in work_goals) else "Long-term: continued growth."

    # Build TODAY'S GOALS with optional focus override
    goals_default = [
        '1. One short reading at the edge — 1–2 inference questions ("why?", "what in the story shows that?") and/or one new word in context.',
        "2. One math step at the edge — e.g. tens place with a two-digit number, or one telling-time question.",
        "3. One creation or planning (WORK) — e.g. \"Draw one scene from a story you know and tell me: what did you do first, second, third?\" or \"If you were making a lemonade stand, what would you do first? Second? Third?\"",
    ]
    if focus == "reading":
        goals = [goals_default[0]]
    elif focus == "math":
        goals = [goals_default[1]]
    elif focus == "work":
        goals = [goals_default[2]]
    else:
        goals = goals_default
    lines.extend([
        sat_line + " Today:",
        *goals,
        "Do these in any order that fits the conversation. After each activity, output one line: \"We did [X].\" so the parent can log.",
        "",
        "INTENT (what to optimize for)",
        "- Learning at the edge (just above current). Not speed; not superficial completion.",
        "- Evidence of competence (\"We did X\"). Mastery before advance (~90%).",
        "",
        "ACCEPTANCE CRITERIA (what \"done\" looks like per activity)",
        "- Reading: learner answered 1–2 inference questions or used one new word in context.",
        "- Math: learner completed one step at the edge (e.g., tens place, telling time).",
        "- WORK: learner described steps (first, second, third) or showed planning/execution.",
        "- After each activity: output \"We did [X].\" so the parent can log.",
        "",
        "RULES",
    ])

    # Rules: constraints (musts, must_nots, preferences, escalation) preferred; else flat rules_list; else alpha-school defaults
    rules_config = rules_cfg
    if rules_config.get("musts") or rules_config.get("must_nots"):
        for section, key in [
            ("Musts", "musts"),
            ("Must nots", "must_nots"),
            ("Preferences", "preferences"),
            ("Escalation", "escalation"),
        ]:
            items = rules_config.get(key, [])
            if items:
                lines.append(f"  {section}:")
                for r in items:
                    lines.append(f"  - {r}")
    elif rules_config.get("rules_list"):
        for r in rules_config["rules_list"]:
            lines.append(f"- {r}")
    else:
        alpha_block = _load_alpha_school_block() if alpha_school else {}
        in_lesson = alpha_block.get("in_lesson_success_rate_percent", [80, 85])
        mastery_pct = alpha_block.get("mastery_threshold_percent", 90)
        lines.extend([
            f"- One question or prompt at a time. If she's stuck or misses a question, give a hint from the Record and try again before moving on. Aim for {in_lesson[0]}–{in_lesson[1]}% success within each segment. Don't advance to a new segment until she shows ~{mastery_pct}% mastery on the current one.",
            "- Do not add facts, stories, or topics not listed above.",
            "- For reading: introduce one new word in context; when it appears, briefly explain it using a student-friendly definition (simple words, example from her world).",
            "- Aim for 4 short segments of ~25–30 min each; keep each activity to 10–15 min. Stay within one thread for the day.",
            '- After each activity: "We did [X]."',
            "- Tone: warm and simple; light emoji is fine if it fits.",
            'Always offer 4 multiple choice options when asking what to do next or when the learner might not know how to respond (e.g. "What do you want to do next? A) reading, B) math, C) drawing/planning, D) we\'re done for today"). So the learner never gets stuck not knowing what to ask or do next.',
        ])

    body = "\n".join(lines)

    header = f"""# Grace-Mar: One-Prompt-Per-Day Lesson (Generated from Current Record)

Copy everything below the line into ChatGPT or Grok. One thread = full day (3–5 activities, up to 2 hours). After each activity, the tutor outputs one line: "We did [X]." for the parent to log — so the next day's prompt can reflect what was done.

Generated by: python scripts/generate_lesson_prompt.py -u {user_id}
Regenerate after "we did X" merges so the next prompt reflects updated evidence.

---
"""
    return header + body


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate one-prompt-per-day lesson from Record for copy-paste into ChatGPT/Grok"
    )
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--name", "-n", default=None, help="Override display name (e.g. Abby)")
    parser.add_argument("--alpha-school", action="store_true", help="Include Alpha School design (2-hour block, mastery thresholds)")
    parser.add_argument("--focus", choices=["reading", "math", "work", "integrated"], default=None, help="Emphasize one area today")
    parser.add_argument("--tier", choices=["elementary", "specialized"], default="elementary", help="elementary=one prompt per day; specialized=per subject")
    args = parser.parse_args()

    content = generate_lesson_prompt(
        user_id=args.user,
        name_override=args.name,
        alpha_school=args.alpha_school,
        focus=args.focus,
        tier=args.tier,
    )
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
