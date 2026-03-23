#!/usr/bin/env python3
"""
Fork Simulation Engine — "What would Grace-Mar decide in this scenario?"

Grounded on the keyword retriever + SYSTEM_PROMPT (same contract as grounded chat).
Stages only via recursion-gate when --auto-stage; never merges into the Record.

Environment:
  OPENAI_API_KEY, OPENAI_MODEL (default gpt-4o)
  GRACE_MAR_PROFILE_DIR — optional; set by --git-ref to a materialized profile tree

SLO: aim for under --max-wall-seconds (default 180) for typical n_queries 5 and parallel 3.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent import futures
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv

from repo_io import fork_root, load_fork_config

MODES = ("conservative", "exploratory", "value-aligned")

MODE_BIAS: dict[str, str] = {
    "conservative": (
        "Answer strictly from the record excerpts below. Do not speculate beyond them. "
        "If the scenario is not covered, say you don't know that yet."
    ),
    "exploratory": (
        "Use the record as the base, then briefly note curiosity gaps or long-term angles "
        "suggested by IX-B-style interests — still cite the record where you rely on it, "
        "and mark guesses as uncertain."
    ),
    "value-aligned": (
        "Weight IX-C personality observations and stated values; cite the record. "
        "Prefer answers that fit what is documented as distinctive about this self."
    ),
}

QUERY_ANGLES = [
    "Angle 1 — immediate risks and consequences",
    "Angle 2 — long-term fit with curiosity and values",
    "Angle 3 — what the Record already suggests about similar situations",
    "Angle 4 — personality and emotional fit",
    "Angle 5 — information gaps: what would need to be learned before deciding",
    "Angle 6 — second-order effects on relationships or routines",
    "Angle 7 — what a cautious vs bold stance would each require",
]

ABSTAIN_MARKERS = (
    "don't know that yet",
    "i don't know",
    "haven't learned",
)


def _materialize_git_ref(*, repo_root: Path, git_ref: str, user_id: str, dest: Path) -> None:
    """Write files from `git show` into dest (profile root: contains self.md)."""
    dest.mkdir(parents=True, exist_ok=True)
    rel_base = f"users/{user_id}"
    names = [
        "self.md",
        "self-evidence.md",
        "skills.md",
        "skill-think.md",
        "skill-write.md",
        "work-alpha-school.md",
        "work-jiang.md",
    ]
    for name in names:
        obj = f"{git_ref}:{rel_base}/{name}"
        r = subprocess.run(
            ["git", "-C", str(repo_root), "show", obj],
            capture_output=True,
            text=True,
        )
        if r.returncode == 0 and (r.stdout or "").strip():
            (dest / name).write_text(r.stdout, encoding="utf-8")
    if not (dest / "self.md").exists():
        raise SystemExit(
            f"git ref {git_ref!r} did not yield {rel_base}/self.md — check ref and path."
        )


def _merge_chroma_snippets(user_id: str, query_text: str, top_k: int) -> list[str]:
    """Optional vector snippets; empty if index or key missing."""
    try:
        from semantic_query import query as chroma_query
    except ImportError:
        from scripts.semantic_query import query as chroma_query  # type: ignore
    rows = chroma_query(user_id=user_id, query_text=query_text, top_k=top_k)
    out = []
    for r in rows:
        doc = (r.get("document") or "").strip()
        if doc:
            out.append(f"[chroma:{r.get('id', '?')}] {doc[:500]}")
    return out


def _estimate_confidence(response: str) -> float:
    low = response.lower()
    cites = len(re.findall(r"\[(?:LEARN|CUR|PER|ACT|READ|WRITE|CREATE)-\d+\]", response))
    if any(m in low for m in ABSTAIN_MARKERS):
        return 40.0
    if cites >= 2:
        return 85.0
    if cites == 1:
        return 72.0
    return 55.0


def _count_pending_gate(user_id: str) -> int:
    from recursion_gate_review import parse_review_candidates

    rows = parse_review_candidates(user_id=user_id)
    return sum(1 for r in rows if (r.get("status") or "").strip().lower() == "pending")


def _pending_cap(user_id: str) -> int | None:
    cfg = load_fork_config(user_id) or {}
    q = cfg.get("quotas") or {}
    m = q.get("pending_candidates_max")
    if m is None:
        return None
    try:
        return int(m)
    except (TypeError, ValueError):
        return None


def _run_single_query(
    *,
    idx: int,
    scenario: str,
    mode: str,
    user_id: str,
    top_k: int,
    use_chroma: bool,
    max_tokens: int,
    model: str,
) -> dict:
    """One grounded LLM call; imports bot stack lazily."""
    from openai import OpenAI

    from bot.core import GROUNDED_PROMPT_APPENDIX
    from bot.prompt import SYSTEM_PROMPT
    from bot.retriever import retrieve

    angle = QUERY_ANGLES[idx % len(QUERY_ANGLES)]
    bias = MODE_BIAS[mode]
    user_msg = f"{bias}\n\nScenario:\n{scenario}\n\n{angle}\n\nWhat would you decide or advise, and why? Answer as this Record's Voice (first person where natural)."

    combined_q = f"{scenario} {angle}"
    chunks = retrieve(combined_q, top_k=top_k)
    excerpt_parts = [text for _, text in chunks]
    if use_chroma:
        excerpt_parts.extend(_merge_chroma_snippets(user_id, combined_q, min(5, top_k)))

    if excerpt_parts:
        excerpt_block = "\nRelevant record excerpts:\n" + "\n\n".join(excerpt_parts)
    else:
        excerpt_block = "\nNo relevant record excerpts found for this question."

    system = SYSTEM_PROMPT + GROUNDED_PROMPT_APPENDIX + excerpt_block
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "").strip())
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    reply = (resp.choices[0].message.content or "").strip()
    cited_ids = re.findall(r"\[((?:LEARN|CUR|PER|ACT|READ|WRITE|CREATE)-\d+)\]", reply)
    return {
        "query_id": idx,
        "angle": angle,
        "response": reply,
        "chunk_ids": [c[0] for c in chunks],
        "cited_ids": list(dict.fromkeys(cited_ids)),
        "confidence": _estimate_confidence(reply),
    }


def _build_report(
    *,
    scenario: str,
    mode: str,
    user_id: str,
    git_ref: str | None,
    results: list[dict],
    prp_excerpt: str,
) -> str:
    mean_conf = sum(r["confidence"] for r in results) / max(len(results), 1)
    src = git_ref or "working tree (no --git-ref)"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Fork simulation",
        "",
        f"**Scenario:** {scenario}",
        f"**Mode:** {mode}",
        f"**User / fork:** {user_id}",
        f"**Record source:** {src}",
        f"**Run at:** {ts}",
        "",
        "## PRP excerpt (export_prp head)",
        "",
        prp_excerpt[:8000] + ("…" if len(prp_excerpt) > 8000 else ""),
        "",
        "## Query runs",
        "",
    ]
    for r in sorted(results, key=lambda x: x["query_id"]):
        lines.append(f"### Query {r['query_id'] + 1} — {r['angle']}")
        lines.append("")
        lines.append(f"**Retriever chunk IDs:** {', '.join(r['chunk_ids']) or '(none)'}")
        lines.append("")
        lines.append(r["response"])
        lines.append("")
        lines.append(f"*Heuristic confidence: {r['confidence']:.0f}/100*")
        lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append(f"**Mean confidence:** {mean_conf:.1f}/100")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Simulation only — not merged into the Record. Approve via recursion-gate if useful.*"
    )
    return "\n".join(lines)


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    load_dotenv(REPO_ROOT / "bot" / ".env")

    ap = argparse.ArgumentParser(description="Simulate fork decision for a scenario (grounded)")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")
    ap.add_argument("--scenario", required=True, help="Hypothetical decision or question")
    ap.add_argument("--mode", choices=MODES, default="conservative")
    ap.add_argument("--n-queries", type=int, default=5, help="Parallel grounded runs (different angles)")
    ap.add_argument("--top-k", type=int, default=8, help="Retriever top-k chunks per query")
    ap.add_argument("--parallel", type=int, default=3, help="Max concurrent LLM calls")
    ap.add_argument("--max-wall-seconds", type=float, default=180.0)
    ap.add_argument("--max-tokens", type=int, default=350)
    ap.add_argument("--git-ref", default=None, help="Git ref (tag/commit) to materialize users/<user>/ into a temp profile")
    ap.add_argument(
        "--output",
        "-o",
        default=None,
        help="Report markdown path (default: users/<user>/artifacts/simulation-reports/YYYY-MM-DD_sim.md)",
    )
    ap.add_argument("--use-chroma", action="store_true", help="Merge Chroma snippets when index + OPENAI_API_KEY exist")
    ap.add_argument("--auto-stage", action="store_true", help="Stage full report to recursion-gate as SIMULATION_RESULT")
    ap.add_argument("--stage-title", default=None, help="Candidate title when --auto-stage")
    ap.add_argument("--auto-score", action="store_true", help="Run score_gate_candidates.py after staging")
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY", "").strip():
        print("OPENAI_API_KEY is required for simulation.", file=sys.stderr)
        return 1

    os.environ["GRACE_MAR_USER_ID"] = args.user

    artifact_dir = fork_root(args.user) / "artifacts" / "simulation-reports"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    profile_tmp: str | None = None
    saved_profile_dir = os.environ.get("GRACE_MAR_PROFILE_DIR")
    try:
        if args.git_ref:
            artifact_dir.mkdir(parents=True, exist_ok=True)
            profile_tmp = tempfile.mkdtemp(prefix="sim-snapshot-", dir=str(artifact_dir))
            _materialize_git_ref(
                repo_root=REPO_ROOT,
                git_ref=args.git_ref,
                user_id=args.user,
                dest=Path(profile_tmp),
            )
            os.environ["GRACE_MAR_PROFILE_DIR"] = profile_tmp
        else:
            os.environ.pop("GRACE_MAR_PROFILE_DIR", None)

        # Import after fork env so retriever resolves the right profile_dir.
        import importlib

        import bot.retriever as retriever_mod

        importlib.reload(retriever_mod)

        from export_prp import export_prp

        prp_full = export_prp(user_id=args.user)
        prp_excerpt = prp_full[:12000]

        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        indices = list(range(args.n_queries))
        results: list[dict] = []
        deadline = time.monotonic() + args.max_wall_seconds
        executor = futures.ThreadPoolExecutor(max_workers=max(1, args.parallel))
        try:
            futs = {
                executor.submit(
                    _run_single_query,
                    idx=i,
                    scenario=args.scenario,
                    mode=args.mode,
                    user_id=args.user,
                    top_k=args.top_k,
                    use_chroma=args.use_chroma,
                    max_tokens=args.max_tokens,
                    model=model,
                ): i
                for i in indices
            }
            for fut in futures.as_completed(futs):
                if time.monotonic() > deadline:
                    print("Exceeded --max-wall-seconds; cancelling remaining tasks.", file=sys.stderr)
                    for f in futs:
                        f.cancel()
                    break
                try:
                    results.append(fut.result(timeout=max(1.0, deadline - time.monotonic())))
                except futures.CancelledError:
                    pass
                except Exception as e:
                    print(f"Query failed: {e}", file=sys.stderr)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        if len(results) < args.n_queries:
            print(
                f"Warning: only {len(results)}/{args.n_queries} queries completed.",
                file=sys.stderr,
            )

        report = _build_report(
            scenario=args.scenario,
            mode=args.mode,
            user_id=args.user,
            git_ref=args.git_ref,
            results=results,
            prp_excerpt=prp_excerpt,
        )

        if args.output:
            out_path = Path(args.output)
        else:
            day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            safe = re.sub(r"[^a-zA-Z0-9_\-]+", "_", args.scenario[:48]).strip("_") or "run"
            out_path = artifact_dir / f"{day}_{safe}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(str(out_path))

        if args.auto_stage:
            cap = _pending_cap(args.user)
            if cap is not None:
                pending = _count_pending_gate(args.user)
                if pending >= cap:
                    print(
                        f"Pending candidates ({pending}) at or above fork quota ({cap}); not staging.",
                        file=sys.stderr,
                    )
                    return 1
            title = args.stage_title or f"Simulation: {args.scenario[:80]}"
            summary = f"[{args.mode}] {args.scenario[:200]}"
            stage_cmd = [
                sys.executable,
                str(REPO_ROOT / "scripts" / "stage_gate_candidate.py"),
                "-u",
                args.user,
                "--title",
                title,
                "--summary",
                summary,
                "--proposal-class",
                "SIMULATION_RESULT",
            ]
            if args.auto_score:
                stage_cmd.append("--auto-score")
            proc = subprocess.run(
                stage_cmd,
                input=report,
                text=True,
                capture_output=True,
            )
            if proc.returncode != 0:
                print(proc.stderr or proc.stdout, file=sys.stderr)
                return proc.returncode
    finally:
        if profile_tmp and Path(profile_tmp).exists():
            shutil.rmtree(profile_tmp, ignore_errors=True)
        if saved_profile_dir is not None:
            os.environ["GRACE_MAR_PROFILE_DIR"] = saved_profile_dir
        else:
            os.environ.pop("GRACE_MAR_PROFILE_DIR", None)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
