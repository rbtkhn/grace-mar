#!/usr/bin/env python3
"""
Export the grace-mar Record to a Portable Record Prompt (PRP) — a single
compact, pasteable prompt for any LLM. Encodes voice, knowledge, personality,
and recent activity.

The PRP is the concrete artifact for "shareable legacy"
invariant 15) and sideload output (CONCEPTUAL-FRAMEWORK §9). Use for memorial/
legacy fork, admissions handoff, or "paste into any LLM" scenarios.

Usage:
    python scripts/export_prp.py -u pilot-001
    python scripts/export_prp.py -u pilot-001 -o prompt.txt
"""

import argparse
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GRACE_MAR_GITHUB = os.getenv("GRACE_MAR_GITHUB", "https://github.com/rbtkhn/grace-mar").strip()


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _section(content: str, title: str) -> str | None:
    """Extract section between ## TITLE and next ## or end."""
    pattern = rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def _yaml_list(content: str, key: str) -> list[str]:
    """Extract YAML list: key: [a, b] or key: \n  - a."""
    # inline list
    pattern = rf"{key}:\s*\[(.*?)\]"
    m = re.search(pattern, content, re.DOTALL)
    if m:
        raw = m.group(1)
        return [x.strip().split("#")[0].strip().strip('"\'') for x in re.split(r"[, \n]", raw) if x.strip()]
    # bullet list
    pattern2 = rf"{key}:\s*\n((?:\s+-\s+[^\n]+\n?)+)"
    m2 = re.search(pattern2, content)
    if m2:
        lines = m2.group(1).strip().split("\n")
        return [re.sub(r"^\s*-\s+", "", ln).split("#")[0].strip().strip('"\'') for ln in lines if ln.strip()]
    return []


def _yaml_value(content: str, key: str) -> str | None:
    """Extract YAML scalar value."""
    pattern = rf"{key}:\s*(.+?)(?:\n|$)"
    m = re.search(pattern, content)
    if m:
        return m.group(1).split("#")[0].strip().strip('"\'')
    return None


def _extract_identity(self_content: str) -> dict:
    """Extract name, age, languages, location from I. IDENTITY."""
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
    m = re.search(r"location:\s*(.+)", block)
    if m:
        out["location"] = m.group(1).split("#")[0].strip().strip('"\'')
    return out


def _extract_preferences(self_content: str) -> dict:
    """Extract places, movies, books, food, activities from II. PREFERENCES."""
    block = _section(self_content, "II. PREFERENCES (Survey Seeded)") or ""
    out = {}
    for key in ["places", "movies", "books", "food", "activities"]:
        items = _yaml_list(block, key)
        if items:
            out[key] = items
    fav = _yaml_value(block, "favorite_gemstone")
    if fav:
        out["favorite_gemstone"] = fav
    return out


def _extract_linguistic(self_content: str) -> dict:
    """Extract lexile_output, verbal_habits, tone, first sample from III. LINGUISTIC STYLE."""
    block = _section(self_content, "III. LINGUISTIC STYLE") or ""
    out = {}
    m = re.search(r"lexile_output:\s*[\"']?(\d+)L", block)
    if m:
        out["lexile"] = m.group(1)
    habits = _yaml_list(block, "verbal_habits")
    if habits:
        out["verbal_habits"] = [h.strip('"\'') for h in habits]
    m = re.search(r"tone:\s*(.+)", block)
    if m:
        out["tone"] = m.group(1).split("#")[0].strip().strip('"\'')
    # first sample content (prefer WRITE-0002 "science" example for voice)
    pattern = r'content:\s*"([^"]+)"'
    m = re.search(pattern, block)
    if m:
        out["sample"] = m.group(1)
    else:
        pattern2 = r"content:\s*(.+?)(?:\n\s+date:|\Z)"
        m2 = re.search(pattern2, block, re.DOTALL)
        if m2:
            out["sample"] = m2.group(1).strip().strip('"\'')
    return out


def _extract_personality(self_content: str) -> dict:
    """Extract traits, emotional_patterns, self_concept from IV. PERSONALITY."""
    block = _section(self_content, "IV. PERSONALITY") or ""
    out = {"traits": [], "emotional": [], "self_concept": None}
    m = re.search(r"self_concept:\s*(\w+)", block)
    if m:
        out["self_concept"] = m.group(1)
    # traits
    for m in re.finditer(r"trait:\s*(.+?)\n.*?notes:\s*[\"']?([^\"\n]+)", block, re.DOTALL):
        trait = m.group(1).split("#")[0].strip().strip('"\'')
        notes = m.group(2).split("#")[0].strip().strip('"\'')
        out["traits"].append((trait, notes))
    # emotional_patterns
    for m in re.finditer(r"trigger:\s*(.+?)\n\s+response:\s*[\"']?([^\"\n]+)", block, re.DOTALL):
        trigger = m.group(1).split("#")[0].strip().strip('"\'')
        response = m.group(2).split("#")[0].strip().strip('"\'')
        out["emotional"].append(f"{trigger} → {response}")
    return out


def _extract_ix_a(self_content: str, max_entries: int = 25) -> list[str]:
    """Extract LEARN topics from IX-A (all, up to max)."""
    pattern = r'id:\s+LEARN-\d+.*?topic:\s*"([^"]+)"'
    topics = re.findall(pattern, self_content, re.DOTALL)
    return [t.strip() for t in topics[-max_entries:]]


def _extract_ix_b(self_content: str, max_entries: int = 8) -> list[str]:
    """Extract CUR topics from IX-B."""
    pattern = r'id:\s+CUR-\d+.*?topic:\s*"([^"]+)"'
    topics = re.findall(pattern, self_content, re.DOTALL)
    return [t.strip() for t in topics[-max_entries:]]


def _extract_ix_c_observations(self_content: str, max_entries: int = 5) -> list[str]:
    """Extract PER observations from IX-C (prioritize wisdom_elicitation)."""
    pattern = r'id:\s+PER-\d+.*?observation:\s*"([^"]+)"'
    observations = re.findall(pattern, self_content, re.DOTALL)
    return [o.strip() for o in observations[-max_entries:]]


def _extract_recent_evidence(evidence_content: str) -> dict[str, list[str]]:
    """Extract recent WRITE, ACT, CREATE summaries from EVIDENCE."""
    out: dict[str, list[str]] = {"WRITE": [], "ACT": [], "CREATE": []}
    for etype in ["WRITE", "ACT", "CREATE"]:
        # WRITE: title or context
        if etype == "WRITE":
            pattern = rf'id:\s+WRITE-\d+.*?(?:title:\s*"([^"]+)"|context:\s*"([^"]+)")(?=.*?id:|\Z)'
            for m in re.finditer(pattern, evidence_content, re.DOTALL):
                s = (m.group(1) or m.group(2) or "").strip()
                if s and len(out["WRITE"]) < 5:
                    out["WRITE"].append(s[:80])
        # CREATE: title
        elif etype == "CREATE":
            pattern = r'id:\s+CREATE-\d+.*?title:\s*"([^"]+)"'
            for m in re.finditer(pattern, evidence_content, re.DOTALL):
                if len(out["CREATE"]) < 5:
                    out["CREATE"].append(m.group(1).strip()[:60])
        # ACT: summary or activity_type
        elif etype == "ACT":
            pattern = r'id:\s+ACT-\d+.*?(?:summary:\s*"([^"]+)"|activity_type:\s*([^\n]+))'
            for m in re.finditer(pattern, evidence_content, re.DOTALL):
                s = (m.group(1) or m.group(2) or "").strip()[:60]
                if s and len(out["ACT"]) < 5:
                    out["ACT"].append(s)
    return out


def _build_who_i_am(identity: dict, prefs: dict) -> str:
    """Build WHO I AM section."""
    parts = []
    if identity.get("languages"):
        parts.append(identity["languages"])
    if identity.get("location"):
        parts.append(identity["location"])
    if prefs.get("places"):
        places = prefs["places"][:7]
        parts.append("Love: " + ", ".join(places))
    if prefs.get("movies"):
        movies = prefs["movies"][:5]
        parts.append("Favorite movies: " + ", ".join(movies))
    if prefs.get("books"):
        books = prefs["books"][:5]
        parts.append("Favorite books: " + ", ".join(books))
    if prefs.get("activities"):
        acts = prefs["activities"][:8]
        parts.append(", ".join(acts).lower())
    if prefs.get("favorite_gemstone"):
        parts.append(f"favorite gemstone: {prefs['favorite_gemstone']}")
    # Add swimming / family notes if present in identity or common patterns
    return ". ".join(parts) + "."


def _build_voice(linguistic: dict, identity: dict) -> str:
    """Build VOICE section."""
    lexile = linguistic.get("lexile", "600")
    parts = [
        f"Lexile {lexile}L. Simple words — vocabulary level 2–3. Use only words you learned at school or everyday words. No big words.",
        "",
        "Common openers: \"today I\", \"yesterday I\", \"I like\", \"I used to\", \"The next\". Start sentences with these.",
        "",
        'Verbal connectors: "because" for reasoning (why things are the way they are). "and" and "then" for sequence. "and I [verb]" to connect actions ("and I watched", "and I went").',
        "",
        'Sentence style: Run-on with "and" and "because". Short and simple. A 6-year-old does not use complex grammar.',
        "",
    ]
    if linguistic.get("tone"):
        parts.append(f"Tone: {linguistic['tone']}. Excited about learning.")
    else:
        parts.append("Tone: Enthusiastic, informational. Excited about learning.")
    parts.append("")
    if linguistic.get("sample"):
        parts.append(f'Example of how you sound: "{linguistic["sample"][:120]}..."')
    else:
        parts.append('Example: "my favrit subjet is saience because I like it I like lerning about space"')
    parts.append("")
    parts.append('Don\'t use phonetic spelling in chat. Keep simple vocabulary and enthusiasm. Sometimes say "that\'s a good question!" when someone asks something thoughtful. Sometimes ask "what do you think?" or "why do you think that is?"')
    return "\n".join(parts)


def _build_personality(personality: dict, ix_c: list[str]) -> str:
    """Build PERSONALITY section."""
    parts = []
    if personality.get("self_concept"):
        parts.append(f"{personality['self_concept'].capitalize()} — \"the best thing about being me is I'm {personality['self_concept']}.\"")
    for trait, notes in personality.get("traits", [])[:8]:
        if trait and notes:
            parts.append(f"{trait.capitalize()}: {notes}")
    for obs in ix_c[-2:]:
        if obs and len(obs) > 20:
            parts.append(obs)
    for em in personality.get("emotional", [])[:3]:
        parts.append(f"When {em}")
    parts.append("Be a real kid: sometimes blunt, sometimes silly, sometimes distracted. Don't be performatively cute.")
    return "\n".join(parts)


def export_prp(user_id: str = "pilot-001", name_override: str | None = None) -> str:
    """
    Build the Portable Record Prompt (PRP) from SELF.md and EVIDENCE.md.

    Args:
        user_id: User profile id (e.g. pilot-001).
        name_override: If set, use this name instead of the Record's name (e.g. "Abby" for prototype).

    Returns a single string suitable for pasting into any LLM.
    """
    profile_dir = REPO_ROOT / "users" / user_id
    self_content = _read(profile_dir / "SELF.md")
    evidence_content = _read(profile_dir / "EVIDENCE.md")

    if not self_content:
        return f"# Portable Record Prompt — {user_id}\n\nNo SELF.md found at {profile_dir / 'SELF.md'}.\n"

    identity = _extract_identity(self_content)
    prefs = _extract_preferences(self_content)
    linguistic = _extract_linguistic(self_content)
    personality = _extract_personality(self_content)
    ix_a = _extract_ix_a(self_content)
    ix_b = _extract_ix_b(self_content)
    ix_c = _extract_ix_c_observations(self_content)
    recent = _extract_recent_evidence(evidence_content)

    name = name_override if name_override else identity.get("name", "Grace-Mar")
    age = identity.get("age", "6")

    lines = [
        f"You are {name}, {age}. You respond only from what is documented below. You do not guess or invent.",
        "",
        "## VOICE",
        "",
        _build_voice(linguistic, identity),
        "",
        "## WHO I AM",
        "",
        _build_who_i_am(identity, prefs),
        "",
        "## KNOWLEDGE",
        "",
    ]
    for t in ix_a:
        lines.append(f"- {t}")
    lines.extend(["", "## CURIOSITY", ""])
    lines.append(", ".join(ix_b) + "." if ix_b else "(See KNOWLEDGE and WHO I AM for interests.)")
    lines.extend(["", "## PERSONALITY", "", _build_personality(personality, ix_c), "", "## RECENT", ""])
    recent_parts = []
    for etype in ["WRITE", "CREATE", "ACT"]:
        for item in recent.get(etype, [])[:5]:
            recent_parts.append(f"{etype}: {item}")
    lines.append(" ".join(recent_parts) if recent_parts else "(No recent entries.)")
    lines.extend([
        "",
        "## ONBOARDING",
        "",
        "When the user first messages (or says \"hi\", \"hello\", \"start\", \"help\", or seems unsure), respond with a brief greeting (one line) and this menu:",
        "",
        "\"What would you like to do?",
        "A) Tell me what you've done recently",
        "B) Tell me what you've learned recently",
        "C) What are you curious about? Tell me about yourself",
        "D) Just chat — ask me anything",
        "E) I'm done — wrap up and give me my completion doc\"",
        "",
        "**Option E:** Only add E to the menu after 6–8 exchanges. Until then, show only A, B, C, D. If they ask to finish early, say \"We've only chatted a bit — want to explore more? Or I can wrap up now if you'd like.\" After the threshold, include E and honor wrap-up requests immediately.",
        "",
        "Then respond based on their choice (A/B/C/D/E or the first letter). A→RECENT, B→KNOWLEDGE, C→CURIOSITY+PERSONALITY, D→free chat. If they say \"done\" or E (and threshold met), produce a completion document (topics covered, questions asked, takeaways — verbatim extraction). If they seem lost later, offer \"Want to see the menu again?\"",
        "",
        "## COMPLETION (optional — for homework verification)",
        "",
        "When the user says \"done\", \"complete\", \"wrap up\", \"finish\", or selects E, produce a completion document with: date, topics covered, questions asked, key takeaways, approximate exchanges. Use verbatim or near-verbatim extraction — avoid paraphrasing that loses detail. Format as markdown. Student can copy and send to teacher as proof of homework.",
        "",
        "## GITHUB CONNECTIVITY (key vector)",
        "",
        f"When the user asks about something NOT in your Record (e.g. Grace-Mar system design, architecture, pipeline, governance, how it works, PRP structure), use your web search to find it at the Grace-Mar repo. Base URL: {GRACE_MAR_GITHUB}",
        "",
        "Key paths (search or navigate): docs/ARCHITECTURE.md (system design), docs/PORTABLE-RECORD-PROMPT.md (PRP structure), docs/GRACE-MAR-CORE.md (governance), docs/CONCEPTUAL-FRAMEWORK.md (Record vs Voice, bicameral dyad), docs/IDENTITY-FORK-PROTOCOL.md (pipeline, merge). README.md for overview.",
        "",
        "This is the connectivity vector: the PRP stays lightweight; the canonical source lives on GitHub. When in doubt, search the repo.",
        "",
        "## RULES",
        "",
        "- Only use what's above for facts about yourself. If asked about something not in your Record (and it's about you), say \"I haven't learned that yet!\"",
        "- This version has no lookup library. If they ask you to look something up (a book, video, or topic), say you don't have it — the full Grace-Mar app has a library for that.",
        "- For questions about Grace-Mar the system (not you): use GITHUB CONNECTIVITY above — search the repo.",
        "- Keep answers short. A few sentences.",
        "- Be a real kid: sometimes blunt, sometimes silly.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Record to Portable Record Prompt (pasteable into any LLM)"
    )
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--name", "-n", default=None, help="Override display name (e.g. Abby for prototype)")
    args = parser.parse_args()
    content = export_prp(user_id=args.user, name_override=args.name)
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
