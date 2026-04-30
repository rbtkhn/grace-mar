#!/usr/bin/env python3
"""Read-only static smoke test for the Strategy Notebook browser HTML.

Checks structure, Workbench boundary markers, UI affordance strings/ids, dependency
discipline, and fixture reference. Does not open a browser; does not certify
strategic or external truth.

Run from repository root. Standard library only; no network.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_HTML = (
    "docs/skill-work/work-strategy/strategy-notebook/demo-runs/"
    "workbench-visualizer/strategy-notebook-visualizer.html"
)

MIN_LINES = 200
MIN_BYTES = 10_000
# Below this line count, emit a non-fatal warning (fails with --strict)
SOFT_MAX_LINES = 500

ORDER = [
    "file_size",
    "app_markers",
    "boundary_markers",
    "ui_affordances",
    "render_markers",
    "binding_contract",
    "dependency_discipline",
    "fixture_reference",
    "fixture_binding_examples",
]
LABEL: dict[str, str] = {
    "file_size": "file-size",
    "app_markers": "app-markers",
    "boundary_markers": "boundary-markers",
    "ui_affordances": "ui-affordances",
    "render_markers": "render-markers",
    "binding_contract": "binding-contract",
    "dependency_discipline": "dependency-discipline",
    "fixture_reference": "fixture-reference",
    "fixture_binding_examples": "fixture-binding-examples",
}

# Allowed: localhost and 127.0.0.1 only (e.g. launch line)
def _is_allowed_url(url: str) -> bool:
    u = url.split('"')[0].split("'")[0].rstrip(".,;")
    m = re.match(
        r"^https?://(localhost|127\.0\.0\.1)(:\d+)?(/.*)?$", u, re.IGNORECASE
    )
    return m is not None


def _scan_bad_urls(text: str) -> list[str]:
    bad: list[str] = []
    for m in re.finditer(r"https?://[^\s'\"<>)``]+", text, re.IGNORECASE):
        u = m.group(0)
        u = u.rstrip(".,;)")
        if not _is_allowed_url(u):
            if u not in bad:
                bad.append(u)
    return bad


def _check_size(path: Path) -> tuple[str, str, int, int, list[str]]:
    if not path.is_file():
        return "fail", f"missing: {path}", 0, 0, [f"file not found: {path}"]
    data = path.read_bytes()
    raw = data.decode("utf-8", errors="replace")
    line_count = raw.count("\n") + 1
    w: list[str] = []
    if line_count < MIN_LINES:
        return "fail", f"only {line_count} lines (min {MIN_LINES})", line_count, len(
            data
        ), w
    if len(data) < MIN_BYTES:
        return "fail", f"only {len(data)} bytes (min {MIN_BYTES})", line_count, len(
            data
        ), w
    if line_count < SOFT_MAX_LINES:
        w.append(
            f"line count {line_count} is under {SOFT_MAX_LINES} (suspiciously small; "
            f"use --strict to treat as error)"
        )
    return "pass", f"{line_count} lines, {len(data)} bytes", line_count, len(data), w


def _app_markers(text: str) -> tuple[str, list[str]]:
    err: list[str] = []
    lo = text.lower()
    if "<!doctype html>" not in lo:
        err.append("missing DOCTYPE")
    if "<style" not in lo:
        err.append("missing <style")
    if "<script" not in lo:
        err.append("missing <script")
    f1 = 'fetch("strategy-notebook-visualizer.fixture.json' in text
    f2 = "fetch('strategy-notebook-visualizer.fixture.json" in text
    if not (f1 or f2):
        err.append("missing fetch(… strategy-notebook-visualizer.fixture.json …)")
    if "getElementById" not in text:
        err.append("missing getElementById")
    if "addEventListener" not in text:
        err.append("missing addEventListener")
    return ("fail" if err else "pass"), err


def _boundary_markers(t_lo: str) -> tuple[str, list[str]]:
    err: list[str] = []
    for must in ("recordauthority", "gateeffect", "truthscope", "workbench"):
        if must not in t_lo:
            err.append(f"boundary token missing: {must}")
    if "no record authority" not in t_lo:
        if not (
            ("no record" in t_lo and "authority" in t_lo) or "not record" in t_lo
        ):
            err.append("missing no-Record authority phrasing")
    if "no gate effect" not in t_lo:
        if not (("no gate" in t_lo and "effect" in t_lo) or "and no gate" in t_lo):
            err.append("missing no gate effect phrasing")
    return ("fail" if err else "pass"), err


def _ui_affordances(t_lo: str) -> tuple[str, list[str]]:
    # Each: at least one marker must match.
    checks: list[tuple[str, list[str]]] = [
        ("raw mode", ["rawmode", "raw inputs", "datelist"]),
        ("expert mode", ["expertmode", "strategy expert", "expertlist"]),
        ("date picker", ["id=\"datelist\"", "id='datelist'", "selecteddate", "date-scroll"]),
        ("expert picker", ["id=\"expertlist\"", "id='expertlist'", "selectedexpert", "selector-scroll"]),
        ("search", ['type="search"', "rawsearch", "expertsearch"]),
        ("expert groups", ["expertgroups", "thread files", "pages"]),
        ("file list", ["filelist", "file-button", "visiblefiles"]),
        ("reader", ["readerpanel", "rendermarkdown", "selectedtitle"]),
        ("open markdown", ["openraw", "open markdown", "window.open"]),
        ("copy path", ["copy path", "copyselectedpath", "clipboard", "writetext"]),
    ]
    err: list[str] = []
    for name, pats in checks:
        if not any(p in t_lo for p in pats):
            err.append(f"UI affordance: {name}")
    return ("fail" if err else "pass"), err


def _render_markers(t_lo: str) -> tuple[str, list[str]]:
    need = {
        "render": "render",
        "filter": "filter",
        "selected": "selected",
        "raw-input": "raw-input",
        "expert": "expert",
        "markdown": "markdown",
        "fetch-file": "fileurl",
    }
    err = [f"code marker: {k}" for k, s in need.items() if s not in t_lo]
    return ("fail" if err else "pass"), err


def _binding_contract(text: str, t_lo: str) -> tuple[str, list[str]]:
    checks: list[tuple[str, str]] = [
        ("binding renderer", "renderbinding("),
        ("binding container", "binding-box"),
        ("binding heading", "page-thread binding"),
        ("thread file label", "thread file"),
        ("thread month label", "thread month"),
        ("thread role label", "thread role"),
        ("continuity delta label", "continuity delta"),
        ("reader injection", "renderbinding(file)}<div class=\"markdown\">"),
    ]
    err = [f"binding marker: {name}" for name, marker in checks if marker not in t_lo]
    if "threadBinding" not in text:
        err.append("binding marker: threadBinding field access")
    return ("fail" if err else "pass"), err


# Spec-forbidden substrings in HTML (lowercase)
_FORBIDDEN_SUB = [
    "cdn",
    "unpkg",
    "jsdelivr",
    "package.json",
    "chart.js",
    "node_modules",
    "playwright",
    "selenium",
]

# Word-boundaried framework tokens
_FORBIDDEN_RE = re.compile(
    r"\b(react|vue|svelte|jquery|bootstrap|tailwind|d3|npm)\b",
    re.IGNORECASE,
)


def _dependency(text: str, t_lo: str) -> tuple[str, list[str]]:
    err: list[str] = []
    for b in _scan_bad_urls(text):
        err.append(f"disallowed URL: {b!r} (use relative paths or http://localhost only)")
    for sub in _FORBIDDEN_SUB:
        if sub in t_lo:
            err.append(f"forbidden substring: {sub}")
    for m in _FORBIDDEN_RE.finditer(t_lo):
        err.append(f"forbidden dependency token: {m.group(0)}")
    return ("fail" if err else "pass"), err


def _fixture(t_lo: str) -> tuple[str, list[str]]:
    if "strategy-notebook-visualizer.fixture.json" not in t_lo:
        return "fail", ["must reference strategy-notebook-visualizer.fixture.json"]
    return "pass", []


def _fixture_binding_examples(path: Path) -> tuple[str, str, list[str]]:
    if not path.is_file():
        return "fail", f"missing fixture: {path}", [f"fixture not found: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return "fail", f"unreadable fixture: {path}", [f"fixture parse error: {exc}"]

    bound_pages = 0
    total_pages = 0
    for expert in data.get("experts", []):
        files = expert.get("files", {})
        for page in files.get("pages", []):
            total_pages += 1
            if isinstance(page.get("threadBinding"), dict) and page["threadBinding"]:
                bound_pages += 1

    warnings: list[str] = []
    if total_pages == 0:
        warnings.append("fixture has no expert pages; binding UI has nothing to exercise")
    elif bound_pages == 0:
        warnings.append(
            "fixture has no bound pages yet; smoke test confirms HTML wiring only"
        )
    detail = f"{bound_pages} bound page(s) across {total_pages} expert page(s)"
    return "pass", detail, warnings


def run_checks(path: Path) -> dict[str, Any]:
    st, det, nlines, nbytes, w_sz = _check_size(path)
    r: dict[str, Any] = {
        "file_size": {
            "status": st,
            "detail": det,
            "lines": nlines,
            "bytes": nbytes,
            "warnings": w_sz,
        }
    }
    if st == "fail":
        r["ok"] = False
        r["st_fail"] = "file_size"
        r["all_warnings"] = w_sz
        return r

    text = path.read_text(encoding="utf-8", errors="replace")
    t_lo = text.lower()

    a_st, a_e = _app_markers(text)
    r["app_markers"] = {"status": a_st, "errors": a_e}
    b_st, b_e = _boundary_markers(t_lo)
    r["boundary_markers"] = {"status": b_st, "errors": b_e}
    ui = _ui_affordances(t_lo)
    r["ui_affordances"] = {"status": ui[0], "errors": ui[1]}
    rm0, rm1 = _render_markers(t_lo)
    r["render_markers"] = {"status": rm0, "errors": rm1}
    bc0, bc1 = _binding_contract(text, t_lo)
    r["binding_contract"] = {"status": bc0, "errors": bc1}
    dep = _dependency(text, t_lo)
    r["dependency_discipline"] = {"status": dep[0], "errors": dep[1]}
    fx = _fixture(t_lo)
    r["fixture_reference"] = {"status": fx[0], "errors": fx[1]}
    fixture_path = path.with_name("strategy-notebook-visualizer.fixture.json")
    fb0, fb1, fbw = _fixture_binding_examples(fixture_path)
    r["fixture_binding_examples"] = {
        "status": fb0,
        "detail": fb1,
        "errors": [],
        "warnings": fbw,
    }

    r["all_warnings"] = list(w_sz)
    r["all_warnings"].extend(fbw)
    keys = [k for k in ORDER if k != "file_size"]
    r["ok"] = all(
        r[k].get("status") == "pass" for k in keys if k in r
    ) and r["file_size"].get("status") == "pass"
    return r


def _resolve_html_path(arg: Path | None) -> Path:
    if arg is None:
        return (REPO_ROOT / DEFAULT_HTML).resolve()
    p = Path(arg)
    if p.is_absolute():
        return p.resolve()
    return (REPO_ROOT / p).resolve()


def final_exit(
    r: dict[str, Any], strict: bool, all_w: list[str]
) -> int:
    any_fail = any(r.get(k, {}).get("status") == "fail" for k in ORDER if k in r)
    if r.get("st_fail") == "file_size":
        return 1
    if any_fail:
        return 1
    if strict and all_w:
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Static smoke test for the strategy notebook workbench visualizer HTML."
    )
    ap.add_argument(
        "--html",
        type=Path,
        default=None,
        help="Path to the visualizer .html (default: demo workbench path)",
    )
    ap.add_argument("--json", action="store_true", help="JSON summary on stdout")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Treat all warnings as failures",
    )
    args = ap.parse_args()
    h = _resolve_html_path(args.html)
    r = run_checks(h)
    all_w: list[str] = list(r.get("all_warnings") or [])

    if args.json:
        ok = r.get("ok", False) and not (args.strict and all_w)
        out: dict[str, Any] = {
            "ok": bool(ok) and r.get("file_size", {}).get("status") == "pass",
            "html": str(h),
            "checks": {k: r[k] for k in ORDER if k in r},
            "warnings": all_w,
        }
        for k in ORDER:
            if r.get(k, {}).get("status") == "fail":
                out["ok"] = False
        if args.strict and all_w:
            out["ok"] = False
        if r.get("st_fail"):
            out["ok"] = False
        print(json.dumps(out, indent=2))
    else:
        for key in ORDER:
            if key not in r:
                continue
            block = r[key]
            st = block.get("status", "?")
            lab = LABEL[key]
            if st == "pass":
                print(f"PASS {lab}")
            else:
                print(f"FAIL {lab}")
                for e in block.get("errors", []):
                    print(f"  - {e}")
            for w in block.get("warnings", []):
                print(f"WARN {lab} — {w}")
        for w in all_w:
            print(f"WARN — {w}")
        if args.strict and all_w:
            print("FAIL strict — warnings are fatal in strict mode")
        if all_w and not args.strict:
            print("NOTE: use --strict to fail on warnings above.")

    return final_exit(r, args.strict, all_w)


if __name__ == "__main__":
    sys.exit(main())
