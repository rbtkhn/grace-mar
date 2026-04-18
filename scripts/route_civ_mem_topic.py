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
  python3 scripts/route_civ_mem_topic.py "hormuz shipping" --focus-config config/civ_mem_routing_focus.yaml
  python3 scripts/route_civ_mem_topic.py "test" --no-focus
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "civ_mem_topic_routes.yaml"
FOCUS_CONFIG_PATH = REPO_ROOT / "config" / "civ_mem_routing_focus.yaml"
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


def _parse_iso_to_utc(s: str, *, end_of_day: bool) -> datetime:
    """Parse YAML date or datetime string to UTC-aware datetime."""
    raw = s.strip()
    if len(raw) <= 10 and raw.count("-") == 2:
        d = date.fromisoformat(raw[:10])
        if end_of_day:
            return datetime(
                d.year, d.month, d.day, 23, 59, 59, 999999, tzinfo=timezone.utc
            )
        return datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)
    if raw.endswith("Z") and "+" not in raw[-6:]:
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _focus_is_valid(focus: dict) -> bool:
    try:
        now = datetime.now(timezone.utc)
        vf = focus.get("valid_from")
        vt = focus.get("valid_until")
        if vf is not None and str(vf).strip():
            if now < _parse_iso_to_utc(str(vf), end_of_day=False):
                return False
        if vt is not None and str(vt).strip():
            if now > _parse_iso_to_utc(str(vt), end_of_day=True):
                return False
        return True
    except (ValueError, TypeError, OSError):
        return False


def _sticky_bonuses(focus: dict, query_lower: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in focus.get("sticky_keywords") or []:
        if not isinstance(item, dict):
            continue
        kw = (item.get("keyword") or "").strip().lower()
        pid = item.get("profile")
        if not kw or not pid:
            continue
        bonus = int(item.get("bonus", 1))
        alt = kw.replace("-", " ")
        if kw in query_lower or alt in query_lower:
            out[str(pid)] = out.get(str(pid), 0) + bonus
    return out


def _pick_profile(
    cfg: dict,
    query: str,
    override: str | None,
    focus: dict | None,
    *,
    focus_active: bool,
) -> tuple[str, dict, dict]:
    """Returns (profile_id, profile, audit dict for stdout / JSONL)."""
    profiles = cfg.get("profiles") or {}
    audit: dict = {
        "focus_active": bool(focus_active),
        "focus_version": (focus or {}).get("focus_version"),
        "valid_from": (focus or {}).get("valid_from"),
        "valid_until": (focus or {}).get("valid_until"),
        "per_profile": {},
        "nonzero_focus_adjustment": False,
    }

    if override:
        if override not in profiles:
            print(f"error: unknown profile {override}", file=sys.stderr)
            sys.exit(1)
        audit["reason"] = "profile_override"
        return override, profiles[override], audit

    q = query.lower()
    profile_bonuses: dict[str, int] = {}
    sticky_map: dict[str, int] = {}
    if focus_active and focus:
        for k, v in (focus.get("profile_overlap_bonus") or {}).items():
            try:
                profile_bonuses[str(k)] = max(0, int(v))
            except (TypeError, ValueError):
                continue
        sticky_map = _sticky_bonuses(focus, q)

    best_id: str | None = None
    best_prof: dict | None = None
    best_score = (-1, -1)  # effective_overlap, priority

    for pid, p in profiles.items():
        base, pri = _score_profile(p, query)
        per: dict = {"base_overlap": base, "priority": pri}
        if base < 0:
            per["disqualified"] = True
            audit["per_profile"][pid] = per
            continue

        pb = profile_bonuses.get(pid, 0) if focus_active else 0
        sb = sticky_map.get(pid, 0) if focus_active else 0
        effective = base + pb + sb
        per["profile_overlap_bonus"] = pb
        per["sticky_bonus"] = sb
        per["effective_overlap"] = effective
        audit["per_profile"][pid] = per

        cand = (effective, pri)
        if cand > best_score:
            best_score = cand
            best_id, best_prof = pid, p

    nonzero_focus = False
    for row in audit["per_profile"].values():
        if row.get("disqualified"):
            continue
        if int(row.get("profile_overlap_bonus", 0)) > 0 or int(row.get("sticky_bonus", 0)) > 0:
            nonzero_focus = True
            break
    audit["nonzero_focus_adjustment"] = nonzero_focus

    if best_id is None or best_score[0] == 0:
        default_id = cfg.get("default_profile")
        if default_id and default_id in profiles:
            audit["fallback"] = "default_profile"
            return default_id, profiles[default_id], audit
        first = next(iter(profiles.items()), None)
        if first:
            audit["fallback"] = "first_profile_key"
            return first[0], first[1], audit
        print("error: no profiles in config", file=sys.stderr)
        sys.exit(1)

    audit["fallback"] = None
    return best_id, best_prof, audit


def _load_focus_config(path: Path) -> dict | None:
    if yaml is None or not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, yaml.YAMLError) as e:
        print(f"warning: could not load focus config {path}: {e}", file=sys.stderr)
        return None


def _format_focus_block(
    audit: dict,
    focus_raw: dict | None,
    focus_active: bool,
    no_focus: bool,
) -> list[str]:
    """Markdown lines for routing focus audit (empty list if nothing to show)."""
    if no_focus:
        return ["- **routing_focus:** _disabled (`--no-focus`)_", "",]

    lines: list[str] = ["## Routing focus", ""]

    if not focus_raw:
        lines.append("_No focus file loaded._")
        lines.append("")
        return lines

    fv = focus_raw.get("focus_version", "?")
    lines.append(f"- **focus_version:** {fv}")
    lines.append(f"- **focus_file_active:** {'yes' if focus_active else 'no'}")
    if not focus_active:
        lines.append(
            "- **note:** File present but outside `valid_from`/`valid_until` (UTC) or invalid dates — bonuses not applied."
        )
    vf, vt = focus_raw.get("valid_from"), focus_raw.get("valid_until")
    if vf or vt:
        lines.append(f"- **valid_window (UTC):** `{vf}` → `{vt}`")

    lines.append(
        f"- **nonzero_focus_adjustment:** {'yes' if audit.get('nonzero_focus_adjustment') else 'no'}"
    )

    per = audit.get("per_profile") or {}
    if per:
        lines.append("- **per-profile scores:**")
        for pid in sorted(per.keys()):
            row = per[pid]
            if row.get("disqualified"):
                lines.append(f"  - `{pid}`: _disqualified (`required_tokens`)_")
                continue
            lines.append(
                f"  - `{pid}`: base={row.get('base_overlap', 0)} "
                f"+ profile_bonus={row.get('profile_overlap_bonus', 0)} "
                f"+ sticky={row.get('sticky_bonus', 0)} "
                f"→ **effective={row.get('effective_overlap', 0)}** (priority {row.get('priority', 0)})"
            )
    lines.append("")
    return lines


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
    ap.add_argument(
        "--focus-config",
        type=Path,
        default=FOCUS_CONFIG_PATH,
        help="Optional civ_mem_routing_focus.yaml (ignored with --no-focus)",
    )
    ap.add_argument(
        "--no-focus",
        action="store_true",
        help="Do not load or apply routing focus bonuses",
    )
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

    focus_raw: dict | None = None
    if not args.no_focus:
        focus_raw = _load_focus_config(args.focus_config)
    focus_active = bool(focus_raw and _focus_is_valid(focus_raw))

    profile_id, prof, route_audit = _pick_profile(
        cfg, query, args.profile, focus_raw, focus_active=focus_active
    )

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
    ]

    lines.extend(_format_focus_block(route_audit, focus_raw, focus_active, args.no_focus))
    lines.extend(
        [
            "## Per civilization",
            "",
        ]
    )

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
        winner_detail = (route_audit.get("per_profile") or {}).get(profile_id, {})
        row = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "profile": profile_id,
            "civ_order": civ_order,
            "mem_ids": mem_ids_collected[:24],
            "repo_sha": _git_sha(),
            "routing_rules_version": cfg.get("routing_rules_version"),
            "expand_connections": bool(args.expand_connections),
            "focus_version": route_audit.get("focus_version"),
            "focus_active": focus_active,
            "focus_applied": bool(route_audit.get("nonzero_focus_adjustment")),
            "score_components": winner_detail,
            "routing_fallback": route_audit.get("fallback"),
        }
        if not args.no_focus:
            row["routing_focus_config"] = str(
                args.focus_config.resolve().relative_to(REPO_ROOT)
            )
        with DEFAULT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"\n(logged to {DEFAULT_LOG.relative_to(REPO_ROOT)})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
