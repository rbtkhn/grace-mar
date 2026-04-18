#!/usr/bin/env python3
"""Topic-aware civ-mem routing (ROME-first profiles, MEM CONNECTIONS expansion).

Reads config/civ_mem_topic_routes.yaml, scores the query against profiles, then
emits suggested civilization order, MEM–RELEVANCE suggestions where present, ROME
seeds otherwise, and optional MEM CONNECTIONS neighbors.

WORK only; not Record. Requires research/repos/civilization_memory checkout for
full output.

Usage:
  python3 scripts/route_civ_mem_topic.py "Pope Leo XIV visit France"
  python3 scripts/route_civ_mem_topic.py --profile latin_catholic_sphere "test"
  python3 scripts/route_civ_mem_topic.py "Algiers mosque dialogue" --expand-connections --log-decision
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "civ_mem_topic_routes.yaml"
CIV_BASE = REPO_ROOT / "research" / "repos" / "civilization_memory" / "content" / "civilizations"
DEFAULT_LOG = REPO_ROOT / "artifacts" / "skill-work" / "work-civ-mem" / "routing-decisions.jsonl"

# Permissive: MEM–ROME–CONSTANTINOPLE — style ids
MEM_ID_PATTERN = re.compile(r"MEM[–\-][A-Za-z0-9–\-]+")


def _keyword_overlap(profile: dict, query_lower: str) -> int:
    kws = profile.get("keywords") or []
    n = 0
    for k in kws:
        kl = k.lower()
        if kl in query_lower or kl.replace("-", " ") in query_lower:
            n += 1
    return n


def _score_profile(profile: dict, query: str) -> tuple[int, int]:
    """Returns (overlap_count, priority). Disqualified → (-1, priority)."""
    q = query.lower()
    req = profile.get("required_tokens") or []
    if req:
        if not any(r.lower() in q for r in req):
            return -1, profile.get("priority", 0)
    overlap = _keyword_overlap(profile, q)
    return overlap, profile.get("priority", 0)


def _pick_profile(cfg: dict, query: str, override: str | None) -> tuple[str, dict]:
    profiles = cfg.get("profiles") or {}
    if override:
        if override not in profiles:
            print(f"error: unknown profile {override}", file=sys.stderr)
            sys.exit(1)
        return override, profiles[override]

    best_id: str | None = None
    best_prof: dict | None = None
    best_score = (-1, -1)  # overlap, priority

    for pid, p in profiles.items():
        overlap, pri = _score_profile(p, query)
        if overlap < 0:
            continue
        cand = (overlap, pri)
        if cand > best_score:
            best_score = cand
            best_id, best_prof = pid, p

    if best_id is None or best_score[0] == 0:
        default_id = cfg.get("default_profile")
        if default_id and default_id in profiles:
            return default_id, profiles[default_id]
        # fallback: first profile key
        first = next(iter(profiles.items()), None)
        if first:
            return first
        print("error: no profiles in config", file=sys.stderr)
        sys.exit(1)

    return best_id, best_prof  # type: ignore


def _relevance_path(entity: str) -> Path:
    return CIV_BASE / entity / f"MEM–RELEVANCE–{entity}.md"


def _run_suggest(entity: str, max_per_section: int) -> str:
    script = REPO_ROOT / "scripts" / "suggest_civ_mem_from_relevance.py"
    proc = subprocess.run(
        [sys.executable, str(script), entity, "--max-per-section", str(max_per_section)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return f"_(suggest_civ_mem_from_relevance {entity} failed: {proc.stderr.strip()})_"
    return proc.stdout.strip()


def extract_mem_connection_ids(
    text: str,
    *,
    max_edges: int,
    prefer_rome_prefix: bool,
) -> list[str]:
    """Parse MEM–* ids from text after first 'MEM CONNECTIONS' header (tests use inline fixtures)."""
    parts = re.split(r"(?is)MEM CONNECTIONS", text, maxsplit=1)
    chunk = parts[1] if len(parts) > 1 else text
    raw = MEM_ID_PATTERN.findall(chunk)
    seen: list[str] = []
    for m in raw:
        norm = m.replace("-", "–")
        if norm not in seen:
            seen.append(norm)
    rome_first = [x for x in seen if x.startswith("MEM–ROME–")]
    rest = [x for x in seen if not x.startswith("MEM–ROME–")]
    ordered = (rome_first + rest) if prefer_rome_prefix else seen
    return ordered[:max_edges]


def _expand_connections(
    seed_relative: str,
    *,
    max_edges: int,
    prefer_rome_prefix: bool,
) -> list[str]:
    path = CIV_BASE / seed_relative
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return extract_mem_connection_ids(
        text, max_edges=max_edges, prefer_rome_prefix=prefer_rome_prefix
    )


def _git_sha() -> str:
    try:
        p = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
        )
        if p.returncode == 0:
            return p.stdout.strip()[:12]
    except OSError:
        pass
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("topic", nargs="*", help="Free-text topic / query")
    ap.add_argument("--profile", help="Override matched profile id")
    ap.add_argument("--config", type=Path, default=CONFIG_PATH, help="Path to civ_mem_topic_routes.yaml")
    ap.add_argument("--budget", type=int, default=12, help="Global MEM open budget (informative cap)")
    ap.add_argument("--max-per-section", type=int, default=2, help="Passed to suggest_civ_mem_from_relevance")
    ap.add_argument("--expand-connections", action="store_true", help="List MEM ids from first ROME seed § connections")
    ap.add_argument("--max-cross-civ", type=int, default=None, help="Max connection edges (default: profile value)")
    ap.add_argument("--dry-run", action="store_true", help="Skip subprocess suggest calls")
    ap.add_argument("--log-decision", action="store_true", help=f"Append JSON line to {DEFAULT_LOG.relative_to(REPO_ROOT)}")
    args = ap.parse_args()

    cfg_path = args.config
    if not cfg_path.is_file():
        print(f"error: config not found: {cfg_path}", file=sys.stderr)
        return 1

    if yaml is None:
        print("error: PyYAML required", file=sys.stderr)
        return 1
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    query = " ".join(args.topic).strip() or "(empty query — using default profile)"
    profile_id, prof = _pick_profile(cfg, query, args.profile)

    rome_seeds = cfg.get("rome_seed_files") or []
    primary = prof.get("primary_civ", "ROME")
    secondaries = list(prof.get("secondary_civs") or [])
    civ_order = [primary] + [c for c in secondaries if c != primary]

    max_cross = args.max_cross_civ if args.max_cross_civ is not None else int(prof.get("max_cross_civ_edges") or 4)

    lines: list[str] = [
        f"# Civ-mem topic route",
        "",
        f"- **routing_rules_version:** {cfg.get('routing_rules_version', '?')}",
        f"- **matched_profile:** `{profile_id}`",
        f"- **query:** {query}",
        f"- **civ_order:** {' → '.join(civ_order)}",
        f"- **attention_pct (profile):** {prof.get('attention_pct', {})}",
        f"- **mem_budget (informative):** {args.budget}",
        "",
        "## Per civilization",
        "",
    ]

    mem_ids_collected: list[str] = []

    for civ in civ_order:
        lines.append(f"### {civ}")
        rel = _relevance_path(civ)
        if rel.is_file():
            lines.append(f"- **MEM–RELEVANCE:** `{rel.relative_to(REPO_ROOT)}`")
            if not args.dry_run:
                lines.append("")
                lines.append(_run_suggest(civ, args.max_per_section))
                lines.append("")
            else:
                lines.append(f"_(dry-run: would run suggest_civ_mem_from_relevance {civ})_")
        else:
            lines.append(f"- **MEM–RELEVANCE:** _absent_ at `{rel.relative_to(REPO_ROOT)}`")
            if civ == "ROME":
                lines.append("- **ROME seeds (manual / Tier B):**")
                for s in rome_seeds:
                    p = CIV_BASE / "ROME" / s
                    lines.append(f"  - `{p.relative_to(REPO_ROOT)}`")
                    mem_ids_collected.append(s.replace(".md", ""))
            else:
                lines.append(f"- **Note:** Open `CIV–INDEX–{civ}.md` or scoped search under this folder — no packaged seeds in config.")
        lines.append("")

    if args.expand_connections and rome_seeds:
        seed_file = rome_seeds[0]
        lines.append("## MEM CONNECTIONS expansion (from first ROME seed)")
        lines.append("")
        ex = _expand_connections(
            f"ROME/{seed_file}",
            max_edges=max_cross,
            prefer_rome_prefix=True,
        )
        if not CIV_BASE.is_dir():
            lines.append("_Upstream checkout missing — skipping._")
        elif not ex:
            lines.append("_No MEM ids parsed (file missing or section empty)._")
        else:
            for m in ex:
                lines.append(f"- `{m}`")
                mem_ids_collected.append(m)
        lines.append("")

    if not CIV_BASE.is_dir():
        lines.append("## Warning")
        lines.append("")
        lines.append(f"`{CIV_BASE.relative_to(REPO_ROOT)}` missing — clone civilization_memory (see docs/ci/README.md).")
        lines.append("")

    sys.stdout.write("\n".join(lines).rstrip() + "\n")

    if args.log_decision:
        DEFAULT_LOG.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "profile": profile_id,
            "civ_order": civ_order,
            "mem_ids": mem_ids_collected[:24],
            "repo_sha": _git_sha(),
            "routing_rules_version": cfg.get("routing_rules_version"),
            "expand_connections": bool(args.expand_connections),
        }
        with DEFAULT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"\n(logged to {DEFAULT_LOG.relative_to(REPO_ROOT)})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
