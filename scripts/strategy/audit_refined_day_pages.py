#!/usr/bin/env python3
"""Audit refined pages under strategy-notebook/experts vs refined-page-template.md.

Checks mirror the template compliance checklist (structural / grep-level only).
Excludes *-page-template.md compat stubs.

Usage (repo root): python3 scripts/strategy/audit_refined_day_pages.py
Optional: --json for machine-readable summary.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def appendix_bullets(appendix_body: str) -> list[str]:
    bullets: list[str] = []
    for ln in appendix_body.splitlines():
        s = ln.strip()
        if s.startswith("- **"):
            bullets.append(s)
    return bullets


def appendix_issues(bullets: list[str]) -> list[str]:
    if not bullets:
        return ["appendix_no_bullets"]

    def idx(pred) -> int | None:
        for i, b in enumerate(bullets):
            if pred(b.lower()):
                return i
        return None

    i_verbatim = idx(lambda b: "full verbatim" in b)
    i_inbox = idx(lambda b: "inbox" in b and ("triage" in b or "daily-strategy" in b))
    i_thread = idx(lambda b: "`thread:" in b)
    i_canon = idx(
        lambda b: "canonical primary" in b
        or "canonical video" in b
        or "canonical url" in b
        or b.strip().startswith("- **canonical")
    )

    iss: list[str] = []
    if i_verbatim is None:
        iss.append("appendix_missing_full_verbatim_bullet")
    if i_inbox is None:
        iss.append("appendix_missing_inbox_triage_bullet")
    if i_thread is None:
        iss.append("appendix_missing_thread_line_bullet")
    if i_canon is None:
        iss.append("appendix_missing_canonical_primary_bullet")

    order = [i for i in (i_verbatim, i_inbox, i_thread, i_canon) if i is not None]
    if len(order) >= 2 and order != sorted(order):
        iss.append("appendix_required_bullets_out_of_order")

    return iss


def issues_for(text: str) -> list[str]:
    iss: list[str] = []
    lines = text.splitlines()

    head = "\n".join(lines[:120])
    if not any("WORK only" in ln and "not Record" in ln for ln in lines[:40]):
        iss.append("missing_WORK_line")

    h1 = next((ln for ln in lines if ln.startswith("# ")), "")
    if h1:
        low = h1.lower()
        if "day page" in low:
            iss.append("title_uses_day_page")
        elif "refined page" in low:
            pass
        elif "strategy page" in low:
            iss.append("title_uses_strategy_page_not_refined_page")
        else:
            iss.append("title_missing_refined_page_phrase")

    art_ok = "refined page (standalone file under" in head
    if not art_ok:
        lowh = head.lower()
        if "strategy-page file" in head or "strategy page file" in lowh:
            iss.append("artifact_wrong_strategy_page_wording")
        else:
            iss.append("artifact_missing_refined_page_line")

    has_verbatim = bool(
        re.search(r"^### Verbatim\s*$", text, re.M)
        or re.search(r"^### Chronicle\s*$", text, re.M)
    )
    if not has_verbatim:
        iss.append("missing_###_Verbatim_or_legacy_Chronicle")

    for sec in ("### Reflection", "### Foresight", "### Appendix"):
        if sec not in text:
            iss.append(f"missing_{sec.replace(' ', '_').replace('#', '')}")

    vb_m = re.search(r"^### Verbatim\s*$", text, re.M) or re.search(
        r"^### Chronicle\s*$", text, re.M
    )
    if vb_m:
        pre = text[: vb_m.start()]
        tail_nonempty = [ln.strip() for ln in pre.splitlines() if ln.strip()]
        last8 = tail_nonempty[-8:] if tail_nonempty else []
        if "---" not in last8:
            iss.append("no_hr_immediately_before_Verbatim")

    ap_m = re.search(r"^### Appendix\s*$", text, re.M)
    fo_m = list(re.finditer(r"^### Foresight\s*$", text, re.M))
    if ap_m and fo_m:
        fo_end = fo_m[-1].end()
        between = text[fo_end : ap_m.start()]
        if not re.search(r"^---\s*$", between, re.M):
            iss.append("no_hr_before_Appendix")

    if ap_m:
        rest = text[ap_m.end() :]
        iss.extend(appendix_issues(appendix_bullets(rest)))

    vb = re.search(r"^### Verbatim\s*$", text, re.M) or re.search(
        r"^### Chronicle\s*$", text, re.M
    )
    rf = re.search(r"^### Reflection\s*$", text, re.M)
    if vb and rf:
        verb = text[vb.end() : rf.start()]
        if re.search(r"\bverify:\b", verb, re.I):
            iss.append("verify_token_in_Verbatim_body")

    return iss


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    repo = Path(__file__).resolve().parents[2]
    root = repo / "docs/skill-work/work-strategy/strategy-notebook/experts"
    files = sorted(
        x for x in root.rglob("*-page-*.md") if not x.name.endswith("-page-template.md")
    )

    rows: list[dict[str, object]] = []
    for path in files:
        rel = path.relative_to(repo).as_posix()
        try:
            t = path.read_text(encoding="utf-8")
        except OSError as e:
            rows.append({"path": rel, "issues": ["read_error"], "detail": str(e)})
            continue
        iss = issues_for(t)
        expert = path.parent.name
        rows.append({"path": rel, "expert": expert, "issues": iss})

    bad = [r for r in rows if r["issues"]]
    c: Counter[str] = Counter()
    for r in bad:
        for x in r["issues"]:  # type: ignore[union-attr]
            c[str(x)] += 1

    summary = {
        "total": len(rows),
        "clean": len(rows) - len(bad),
        "with_issues": len(bad),
        "issue_counts": dict(c.most_common()),
        "by_expert": Counter(str(r["expert"]) for r in bad),
    }

    if args.json:
        print(json.dumps({"summary": summary, "failures": bad}, indent=2))
        return

    print("Refined page audit vs refined-page-template.md (checklist-level)")
    print("TOTAL", summary["total"], "| CLEAN", summary["clean"], "| WITH_ISSUES", summary["with_issues"])
    print()
    print("Issue counts:")
    for k, v in c.most_common():
        print(f"  {v:3}  {k}")
    print()
    print("Failures by expert:")
    for ex, n in summary["by_expert"].most_common():
        print(f"  {n:3}  {ex}")
    print()
    print("Failure paths:")
    for r in sorted(bad, key=lambda x: x["path"]):  # type: ignore[index,no-any-return]
        print(f"  {r['path']}")
        for i in r["issues"]:  # type: ignore[union-attr]
            print(f"    - {i}")


if __name__ == "__main__":
    main()
