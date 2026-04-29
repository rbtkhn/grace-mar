"""Heuristic scoring for Conductor action MCQ blocks (WORK observability only)."""

from __future__ import annotations

import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(_REPO_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_REPO_SCRIPTS))

from cadence_conductor_resolution import (  # noqa: E402
    KNOWN_CONDUCTOR_SLUGS,
    normalize_conductor_slug,
)

# Fidelity keyword hints — stylistic proxy aligned with CONDUCTOR_MCQ attribute strings;
# bounded weights in _fidelity_score (not a second slug SSOT).
_FIDELITY_KEYWORDS: dict[str, frozenset[str]] = {
    "toscanini": frozenset({"verify", "seam", "falsify", "tier", "precision", "claims"}),
    "furtwangler": frozenset({"tension", "watch", "conditions", "flow", "line"}),
    "bernstein": frozenset({"stakes", "live", "judgment", "pulse", "vitality"}),
    "karajan": frozenset({"arc", "balance", "trim", "elegance", "proportion"}),
    "kleiber": frozenset({"hotspot", "refuse", "depth", "narrow", "selectivity"}),
}

_LANE_TOKENS = frozenset({"work-strategy", "work-dev", "work-politics", "work-coffee"})


def _line_has_weak_opener(line: str) -> bool:
    low = line.lower().strip()
    probes = (
        "consider ",
        "think about",
        "reflect on",
        "perhaps ",
        "maybe ",
        "perhaps\n",
    )
    head = low[:120]
    return any(p in head for p in probes) or low.startswith("consider") or low.startswith(
        "reflect"
    )
_PATHISH = re.compile(
    r"(?:docs/|scripts/|users/|[\w\-]+\.md|`[^`]+`|work-[a-z\-]+)",
    re.IGNORECASE,
)
# Conductor MCQ lines match `format_conductor_mcq_block`: `**` + letter + `.**` + body (period before closing bold). Plain `A. body` lines also match.
_OPTION_LINE_BOLD = re.compile(r"^\s*\*\*([A-E])\.\*\*\s*(.+)$", re.IGNORECASE | re.DOTALL)
_OPTION_LINE_PLAIN = re.compile(r"^\s*([A-E])\.\s*(.+)$", re.IGNORECASE | re.DOTALL)
_WORD = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _tokens(s: str) -> set[str]:
    return {m.group(0).lower() for m in _WORD.finditer(s)}


def _bigrams(s: str) -> set[tuple[str, str]]:
    toks = [m.group(0).lower() for m in _WORD.finditer(s)]
    return set(zip(toks, toks[1:])) if len(toks) >= 2 else set()


def parse_action_menu_lines(markdown: str) -> list[str]:
    """Extract **A.**–**E.** option bodies in letter order (skip missing letters)."""
    by_letter: dict[str, str] = {}
    for raw in markdown.splitlines():
        stripped = raw.strip()
        m = _OPTION_LINE_BOLD.match(stripped)
        if m is None:
            m = _OPTION_LINE_PLAIN.match(stripped)
        if not m:
            continue
        letter = m.group(1).upper()
        body = (m.group(2) or "").strip()
        by_letter[letter] = body
    out: list[str] = []
    for letter in ("A", "B", "C", "D", "E"):
        if letter in by_letter:
            out.append(by_letter[letter])
    return out


def _pairwise_avg_jaccard(lines: list[str]) -> float:
    if len(lines) < 2:
        return 0.0
    sets_t = [_tokens(L) for L in lines]
    sims: list[float] = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = sets_t[i], sets_t[j]
            if not a and not b:
                continue
            inter = len(a & b)
            union = len(a | b)
            sims.append(inter / union if union else 1.0)
    return sum(sims) / len(sims) if sims else 0.0


def _pairwise_bigram_overlap(lines: list[str]) -> float:
    if len(lines) < 2:
        return 0.0
    bsets = [_bigrams(L) for L in lines]
    sims: list[float] = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = bsets[i], bsets[j]
            if not a and not b:
                continue
            inter = len(a & b)
            union = len(a | b)
            sims.append(inter / union if union else 1.0)
    return sum(sims) / len(sims) if sims else 0.0


def _leading_verbs(lines: list[str]) -> list[str]:
    verbs: list[str] = []
    for line in lines:
        toks = [m.group(0).lower() for m in _WORD.finditer(line)]
        verbs.append(toks[0] if toks else "")
    return verbs


def _discrimination_score(lines: list[str]) -> tuple[float, str]:
    if len(lines) < 2:
        return 0.5, "fewer than two options; discrimination neutral-default."
    tok_sim = _pairwise_avg_jaccard(lines)
    bi_sim = _pairwise_bigram_overlap(lines)
    blended = 0.6 * tok_sim + 0.4 * bi_sim
    verbs = _leading_verbs(lines)
    distinct_verbs = len({v for v in verbs if v})
    verb_bonus = min(0.15, max(0.0, (distinct_verbs - len(lines) * 0.5) * 0.05))
    raw = 1.0 - blended + verb_bonus
    score = max(0.0, min(1.0, raw))
    note = f"token_sim~{tok_sim:.2f} bigram_sim~{bi_sim:.2f} verb_bonus~{verb_bonus:.2f}; capped 0–1."
    return score, note


def _count_grounding_refs(line: str) -> int:
    n = 0
    if _PATHISH.search(line):
        n += len(_PATHISH.findall(line))
    for tok in _LANE_TOKENS:
        if tok in line.lower():
            n += 1
    if "`" in line:
        n += line.count("`") // 2
    return n


def _grounding_score(lines: list[str]) -> tuple[float, str, int]:
    if not lines:
        return 0.0, "no lines parsed.", 0
    total_refs = sum(_count_grounding_refs(L) for L in lines)
    per_line = total_refs / max(len(lines), 1)
    # saturate
    raw = 1.0 - math.exp(-per_line / 2.0)
    score = max(0.0, min(1.0, raw))
    note = f"refs_total={total_refs}; per_line~{per_line:.2f}; heuristic saturation."
    return score, note, total_refs


def _actionability_score(lines: list[str]) -> tuple[float, str]:
    if not lines:
        return 0.0, "no lines parsed."
    imperative_like = re.compile(
        r"\b(open|run|read|edit|add|fix|verify|ship|commit|merge|stage|close|pick)\b",
        re.I,
    )
    scores: list[float] = []
    for line in lines:
        weak = _line_has_weak_opener(line)
        has_imp = imperative_like.search(line) is not None
        has_concrete = bool(_PATHISH.search(line)) or len(_tokens(line)) >= 6
        if weak and not has_concrete:
            scores.append(0.35)
        elif has_imp or has_concrete:
            scores.append(0.85 if has_imp else 0.65)
        else:
            scores.append(0.5)
    avg = sum(scores) / len(scores)
    note = "average line actionability; weak openers penalized unless scoped concrete cues."
    return max(0.0, min(1.0, avg)), note


def _fidelity_score(slug: str, lines: list[str]) -> tuple[float, str]:
    s = normalize_conductor_slug(slug)
    if s not in KNOWN_CONDUCTOR_SLUGS:
        return 0.0, "unknown conductor slug."
    keys = _FIDELITY_KEYWORDS.get(s, frozenset())
    if not lines:
        return 0.0, "no lines parsed."
    blob = " ".join(lines).lower()
    hits = sum(1 for k in keys if k in blob)
    cap = min(len(keys), 8) if keys else 1
    raw = min(1.0, hits / max(cap, 1))
    note = f"keyword_hits={hits} cap={cap}; stylistic proxy only."
    return raw, note


@dataclass(frozen=True)
class EvalScores:
    discrimination_score: float
    grounding_score: float
    actionability_score: float
    fidelity_score: float
    grounding_reference_count: int
    score_notes: dict[str, str]


def evaluate_action_menu(
    slug: str,
    lines: list[str],
    repo_root: Path | None = None,
) -> EvalScores:
    """
    Pure heuristic scores for up to five option lines (bodies only or full lines).

    ``repo_root`` reserved for future path existence checks; unused in v1.
    """
    _ = repo_root
    if not lines:
        return EvalScores(
            discrimination_score=0.0,
            grounding_score=0.0,
            actionability_score=0.0,
            fidelity_score=0.0,
            grounding_reference_count=0,
            score_notes={
                "discrimination": "no lines.",
                "grounding": "no lines.",
                "actionability": "no lines.",
                "fidelity": "no lines.",
            },
        )

    d, nd = _discrimination_score(lines)
    g, ng, gr = _grounding_score(lines)
    a, na = _actionability_score(lines)
    f, nf = _fidelity_score(slug, lines)

    return EvalScores(
        discrimination_score=d,
        grounding_score=g,
        actionability_score=a,
        fidelity_score=f,
        grounding_reference_count=gr,
        score_notes={
            "discrimination": nd,
            "grounding": ng,
            "actionability": na,
            "fidelity": nf,
        },
    )


def evaluate_markdown_menu(
    slug: str,
    markdown: str,
    repo_root: Path | None = None,
) -> tuple[list[str], EvalScores]:
    """Parse markdown then score."""
    lines = parse_action_menu_lines(markdown)
    return lines, evaluate_action_menu(slug, lines, repo_root=repo_root)
