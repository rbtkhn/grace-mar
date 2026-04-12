#!/usr/bin/env python3
"""
Web-based gate review dashboard — pending RECURSION-GATE candidates (canonical review shape).

Supports approve, reject, defer, and reclassify (proposal_class via target surface mapping).
Actions update recursion-gate.md; merge runs via process_approved_candidates. Gate remains
canonical; this app does not edit SELF or EVIDENCE directly.

Run from repo root (so bot.core and scripts resolve paths correctly):
    OPERATOR_SECRET=your_secret python apps/gate-review-app.py
    # Or: FLASK_APP=apps/gate-review-app.py flask run --port 5001

Deploy alongside apps/miniapp_server.py on Render; protect with OPERATOR_SECRET (Bearer token).
"""

import html
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from flask import Flask, jsonify, request

app = Flask(__name__)
USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
OPERATOR_SECRET = os.getenv("OPERATOR_SECRET", "").strip() or os.getenv("OPERATOR_FETCH_SECRET", "").strip()

from repo_io import assert_canonical_record_layout  # noqa: E402
from work_politics_engine import NotFound, PolicyViolation, WorkPoliticsEngine  # noqa: E402

assert_canonical_record_layout(USER_ID, context="gate-review-app")

# WORK-lane SQLite state for work-politics (clients, review queue, funnel). Not RECURSION-GATE.
WP = WorkPoliticsEngine(USER_ID, REPO_ROOT)
WP.init_db()

from gate_review_normalize import normalize_review_item  # noqa: E402
from grace_mar.merge.impact_preview import preview_candidate_impact  # noqa: E402

_RECLASSIFY_SURFACE_OPTIONS = (
    ("self", "self (IX / identity-facing)"),
    ("self_library", "self_library"),
    ("civ_mem", "civ_mem"),
    ("skills", "skills"),
    ("evidence", "evidence"),
    ("work_layer", "work_layer"),
)


def _auth():
    if not OPERATOR_SECRET:
        return True
    auth = request.headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        return auth[7:].strip() == OPERATOR_SECRET
    return request.args.get("token") == OPERATOR_SECRET


def _age_label(age_days):
    return "—" if age_days is None else f"{age_days}d"


@app.route("/")
def index():
    """Serve gate review UI with pending candidates and Approve/Reject buttons."""
    from recursion_gate_review import filter_review_candidates, parse_review_candidates
    from recursion_gate_territory import TERRITORY_WORK_POLITICS

    rows = parse_review_candidates(USER_ID)
    signal_filter = (request.args.get("signal") or "").strip().lower()
    fc_kwargs: dict = {}
    if signal_filter == "reflection":
        fc_kwargs["signal_type"] = "reflection-cycle"
    pending = filter_review_candidates(rows, status="pending", **fc_kwargs)
    n = len(pending)
    politics_n = sum(1 for r in pending if r.get("territory") == TERRITORY_WORK_POLITICS)
    comp_n = n - politics_n

    cards = []
    for r in pending:
        norm = normalize_review_item(r)
        raw_id = r["id"]
        cid = html.escape(raw_id)
        dup = r.get("duplicate_hints") or []
        hint = f'<p class="hint">{html.escape(dup[0])}</p>' if dup else ""
        br = r.get("boundary_review") if isinstance(r.get("boundary_review"), dict) else {}
        br_html = ""
        if br and (br.get("target_surface") or br.get("suggested_surface")):
            t0 = html.escape(str(br.get("target_surface") or ""))
            s0 = html.escape(str(br.get("suggested_surface") or ""))
            mw0 = (br.get("misfiled_warning") or "").strip()
            mw_html = f'<p class="boundary-misfiled">{html.escape(mw0)}</p>' if mw0 else ""
            hrs = br.get("hint_reasons") if isinstance(br.get("hint_reasons"), list) else []
            hr_line = html.escape("; ".join(str(x) for x in hrs[:6] if str(x).strip()))
            hr_part = f'<p class="boundary-why"><em>{hr_line}</em></p>' if hr_line else ""
            cf = html.escape(str(br.get("confidence") or ""))
            br_html = (
                f'<div class="boundary-review">'
                f"<p><strong>Boundary:</strong> {t0} → suggested <strong>{s0}</strong> "
                f'(confidence: {cf})</p>{mw_html}{hr_part}'
                f"</div>"
            )
        sug_pc = norm.get("suggested_reclassify_proposal_class") or ""
        sug_btn = ""
        if sug_pc and sug_pc.strip() != (norm.get("proposal_class") or "").strip():
            esc_pc = html.escape(sug_pc.strip(), quote=True)
            sug_btn = (
                f'<button type="button" class="btn suggested-class" data-id="{cid}" '
                f'data-new-pc="{esc_pc}">Apply suggested class ({html.escape(sug_pc.strip())})</button>'
            )
        summary = html.escape(norm["summary"])
        territory = html.escape(r.get("territory", ""))
        risk_tier = html.escape(r.get("risk_tier", ""))
        label = html.escape(r.get("territory_label", ""))
        pill_slug = "pol" if r.get("territory") == TERRITORY_WORK_POLITICS else "companion"
        age = _age_label(r.get("age_days"))
        channel = html.escape(str(norm["channel_key"]))
        ts = html.escape(str(norm["timestamp"]))
        quick = "true" if r.get("ready_for_quick_merge") else "false"
        sig = html.escape((r.get("signal_type") or "").strip())
        pc = html.escape(norm["proposal_class"])
        tsurf = html.escape(norm["target_surface"])
        mat = html.escape(norm["materiality"])
        rvt = html.escape(norm["review_type"])
        recl = "yes" if norm["requires_reclassification"] else "no"
        pill_recl = "pill-warn" if norm["requires_reclassification"] else "pill-ok"
        cur_surf = norm["target_surface"]
        select_opts = "".join(
            f'<option value="{html.escape(v)}"'
            f'{" selected" if v == cur_surf else ""}>'
            f"{html.escape(lbl)}</option>"
            for v, lbl in _RECLASSIFY_SURFACE_OPTIONS
        )
        impact = preview_candidate_impact(r, user_id=USER_ID)
        impact_files = ", ".join(
            f'<code>{html.escape(f.split("/")[-1])}</code>'
            for f in impact["files_touched"]
        )
        impact_flags_html = "".join(
            f'<span class="pill pill-warn" title="boundary flag">{html.escape(f)}</span>'
            for f in impact["boundary_flags"]
        )
        impact_prompt = ""
        if impact["prompt_effect"] != "none":
            impact_prompt = (
                f'<span class="pill pill-warn" title="prompt effect">'
                f'prompt: {html.escape(impact["prompt_effect"])}</span>'
            )
        impact_html = (
            f'<div class="impact-row">'
            f'<span class="impact-label">Impact:</span> {impact_files}'
            f" {impact_flags_html}{impact_prompt}"
            f"</div>"
        )
        cards.append(
            f'<article class="card" data-territory="{territory}" data-risk="{risk_tier}" data-signal="{sig}" data-candidate-id="{html.escape(raw_id)}">'
            f'<header><span class="id">{cid}</span>'
            f'<span class="pill pill-{pill_slug}">{label}</span>'
            f'<span class="pill pill-risk-tier">{risk_tier}</span>'
            f'<span class="age">{age}</span></header>'
            f'<div class="pill-row">'
            f'<span class="pill pill-meta" title="proposal_class">{pc}</span>'
            f'<span class="pill pill-meta" title="target_surface">{tsurf}</span>'
            f'<span class="pill pill-meta" title="materiality">{mat}</span>'
            f'<span class="pill pill-meta" title="review_type">{rvt}</span>'
            f'<span class="pill pill-meta {pill_recl}" title="requires_reclassification">reclassify: {recl}</span>'
            f"</div>"
            f"{impact_html}"
            f'<p class="summary">{summary}</p>{hint}{br_html}'
            f'<div class="suggested-class-row">{sug_btn}</div>'
            f'<footer><span class="meta">{channel}</span><span class="meta">{ts}</span></footer>'
            f'<div class="actions">'
            f'<button type="button" class="btn approve" data-id="{cid}" data-quick="{quick}">Approve</button>'
            f'<button type="button" class="btn reject" data-id="{cid}">Reject</button>'
            f'<button type="button" class="btn defer" data-id="{cid}">Defer</button>'
            f"</div>"
            f'<details class="reclass-details"><summary>Reclassify</summary>'
            f'<div class="reclass-form">'
            f'<label class="reclass-label">Target surface (maps to proposal_class)'
            f'<select class="reclass-surface">{select_opts}</select></label>'
            f'<textarea class="reclass-note" rows="2" placeholder="Optional review note (audit trail)"></textarea>'
            f'<button type="button" class="btn reclassify" data-id="{cid}">Apply reclassify</button>'
            f"</div></details>"
            f"</article>"
        )
    rows_html = "\n".join(cards) if cards else '<p class="empty">No pending candidates.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Gate review — {html.escape(USER_ID)}</title>
  <style>
    :root {{ --bg: #0f1419; --card: #1a2332; --text: #e8ecf1; --muted: #8b9cb3; --accent: #c17f59; --good: #7dc09a; --danger: #dd8e91; --pol: #c4a574; --companion: #7eb8da; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; padding: 1.25rem; }}
    h1 {{ font-size: 1.35rem; margin: 0 0 0.25rem; }}
    .sub {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 1rem; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1rem; }}
    .stat {{ background: var(--card); padding: 0.5rem 0.9rem; border-radius: 8px; font-size: 0.9rem; }}
    .grid {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); }}
    .card {{ background: var(--card); border-radius: 12px; padding: 1rem; border: 1px solid rgba(255,255,255,.06); }}
    .card header {{ display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.6rem; }}
    .id {{ font-weight: 600; font-family: monospace; font-size: 0.9rem; color: var(--accent); }}
    .pill {{ font-size: 0.7rem; text-transform: uppercase; padding: 0.2rem 0.5rem; border-radius: 4px; }}
    .pill-row {{ display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.5rem; }}
    .impact-row {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 0.5rem; padding: 0.3rem 0.5rem; background: rgba(255,255,255,.04); border-radius: 4px; display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; }}
    .impact-label {{ font-weight: 600; color: var(--text); }}
    .pill-meta {{ background: rgba(255,255,255,.08); color: var(--muted); text-transform: none; font-size: 0.65rem; }}
    .pill-warn {{ background: rgba(221,142,145,0.25); color: var(--danger); }}
    .pill-ok {{ background: rgba(125,192,154,0.15); color: var(--good); }}
    .age {{ margin-left: auto; color: var(--muted); font-size: 0.8rem; }}
    .summary {{ margin: 0; }}
    .hint {{ margin: 0.6rem 0 0; color: var(--muted); font-size: 0.82rem; }}
    .boundary-review {{ margin: 0.6rem 0 0; padding: 0.5rem 0.65rem; border-radius: 8px; background: rgba(193,127,89,0.12); border: 1px solid rgba(193,127,89,0.35); font-size: 0.82rem; }}
    .boundary-misfiled {{ margin: 0.35rem 0 0; color: var(--danger); }}
    .boundary-why {{ margin: 0.35rem 0 0; color: var(--muted); }}
    .suggested-class-row {{ margin-top: 0.5rem; }}
    .btn.suggested-class {{ background: rgba(125,192,154,0.15); color: var(--good); font-size: 0.8rem; }}
    .card footer {{ margin-top: 0.75rem; padding-top: 0.65rem; border-top: 1px solid rgba(255,255,255,.06); font-size: 0.75rem; color: var(--muted); }}
    .actions {{ margin-top: 0.75rem; display: flex; gap: 0.5rem; }}
    .btn {{ padding: 0.4rem 0.8rem; border-radius: 8px; border: none; cursor: pointer; font-size: 0.9rem; }}
    .btn.approve {{ background: rgba(125,192,154,0.2); color: var(--good); }}
    .btn.reject {{ background: rgba(221,142,145,0.2); color: var(--danger); }}
    .btn.defer {{ background: rgba(139,156,179,0.2); color: var(--muted); }}
    .btn.reclassify {{ background: rgba(193,127,89,0.25); color: var(--accent); }}
    .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    .reclass-details {{ margin-top: 0.65rem; font-size: 0.85rem; color: var(--muted); }}
    .reclass-details summary {{ cursor: pointer; color: var(--accent); }}
    .reclass-form {{ display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem; }}
    .reclass-label {{ display: flex; flex-direction: column; gap: 0.25rem; color: var(--text); }}
    .reclass-surface, .reclass-note {{ background: var(--bg); color: var(--text); border: 1px solid rgba(255,255,255,.12); border-radius: 6px; padding: 0.35rem; font-size: 0.85rem; }}
    .empty {{ color: var(--muted); }}
  </style>
</head>
<body>
  <h1>Gate review</h1>
  <p class="sub">Approve, reject, defer, or reclassify pending candidates. Normalized review fields show surface, materiality, and review type. Merge runs via process_approved_candidates.</p>
  <p class="sub">Filter: <a href="/">All</a> · <a href="/?signal=reflection">Reflection only</a></p>
  <div class="stats">
    <span class="stat"><strong>{n}</strong> pending</span>
    <span class="stat">Work-politics <strong>{politics_n}</strong></span>
    <span class="stat">Companion <strong>{comp_n}</strong></span>
  </div>
  <div class="grid" id="grid">{rows_html}</div>
  <script>
    var secret = document.location.search.match(/token=([^&]+)/) ? decodeURIComponent(document.location.search.match(/token=([^&]+)/)[1]) : '';
    function headers() {{
      var h = {{ 'Content-Type': 'application/json' }};
      if (secret) h['Authorization'] = 'Bearer ' + secret;
      return h;
    }}
    function removeCard(btn) {{
      var card = btn.closest('.card');
      if (card) card.remove();
    }}
    function doAction(cid, action, btn, extra) {{
      btn.disabled = true;
      var body = {{ candidate_id: cid, action: action }};
      if (extra) for (var k in extra) body[k] = extra[k];
      fetch('/action', {{
        method: 'POST',
        headers: headers(),
        body: JSON.stringify(body)
      }}).then(function(r) {{ return r.json(); }}).then(function(data) {{
        if (data.error) {{ alert(data.error); btn.disabled = false; return; }}
        if (action === 'reclassify') {{ location.reload(); return; }}
        removeCard(btn);
      }}).catch(function() {{ btn.disabled = false; }});
    }}
    document.querySelectorAll('.btn.approve').forEach(function(btn) {{
      btn.onclick = function() {{ doAction(btn.getAttribute('data-id'), 'approve', btn); }};
    }});
    document.querySelectorAll('.btn.reject').forEach(function(btn) {{
      btn.onclick = function() {{ doAction(btn.getAttribute('data-id'), 'reject', btn); }};
    }});
    document.querySelectorAll('.btn.defer').forEach(function(btn) {{
      btn.onclick = function() {{ doAction(btn.getAttribute('data-id'), 'defer', btn); }};
    }});
    document.querySelectorAll('.btn.reclassify').forEach(function(btn) {{
      btn.onclick = function() {{
        var card = btn.closest('.card');
        var surf = card.querySelector('.reclass-surface').value;
        var note = card.querySelector('.reclass-note').value;
        doAction(btn.getAttribute('data-id'), 'reclassify', btn, {{ new_surface: surf, review_note: note }});
      }};
    }});
    document.querySelectorAll('.btn.suggested-class').forEach(function(btn) {{
      btn.onclick = function() {{
        var pc = btn.getAttribute('data-new-pc');
        doAction(btn.getAttribute('data-id'), 'reclassify', btn, {{
          new_proposal_class: pc,
          review_note: 'Applied suggested boundary class (gate-review-app)'
        }});
      }};
    }});
  </script>
</body>
</html>"""


@app.route("/action", methods=["POST"])
def action():
    """Apply approve, reject, defer, or reclassify; update recursion-gate and optionally quick-merge."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401
    from bot.core import (
        is_low_risk_candidate,
        quick_merge_candidate,
        reclassify_gate_candidate,
        update_candidate_status,
    )

    payload = request.get_json(silent=True) or {}
    candidate_id = (payload.get("candidate_id") or "").strip()
    action_type = (payload.get("action") or "").strip().lower()
    if action_type not in ("approve", "reject", "defer", "reclassify"):
        return jsonify({"error": "action must be approve, reject, defer, or reclassify"}), 400
    if not candidate_id.startswith("CANDIDATE-"):
        return jsonify({"error": "invalid candidate_id"}), 400

    from recursion_gate_review import get_review_candidate
    row = get_review_candidate(USER_ID, candidate_id)
    if not row:
        return jsonify({"error": f"{candidate_id} not found"}), 404

    operator_name = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web").strip() or "operator-web"
    channel_key = "operator:gate-review-app"
    source = "gate-review-app"

    if action_type == "reject":
        reason = (payload.get("rejection_reason") or "").strip() or None
        ok = update_candidate_status(
            candidate_id,
            "rejected",
            rejection_reason=reason,
            channel_key=channel_key,
            actor=operator_name,
            source=source,
        )
        if not ok:
            return jsonify({"error": f"could not reject {candidate_id}"}), 409
        return jsonify({"ok": True, "action": "rejected"})

    if action_type == "defer":
        if row.get("status") != "pending":
            return jsonify({"error": f"{candidate_id} already {row.get('status')}"}), 409
        ok = update_candidate_status(
            candidate_id,
            "deferred",
            channel_key=channel_key,
            actor=operator_name,
            source=source,
        )
        if not ok:
            return jsonify({"error": f"could not defer {candidate_id}"}), 409
        return jsonify({"ok": True, "action": "deferred"})

    if action_type == "reclassify":
        if row.get("status") != "pending":
            return jsonify({"error": f"{candidate_id} already {row.get('status')}"}), 409
        new_surface = (payload.get("new_surface") or "").strip() or None
        new_pc = (payload.get("new_proposal_class") or "").strip() or None
        review_note = (payload.get("review_note") or "").strip() or None
        if not new_surface and not new_pc:
            return jsonify({"error": "new_surface or new_proposal_class required for reclassify"}), 400
        ok = reclassify_gate_candidate(
            candidate_id,
            new_proposal_class=new_pc,
            new_surface=new_surface,
            review_note=review_note,
            channel_key=channel_key,
            actor=operator_name,
            source=source,
        )
        if not ok:
            return jsonify({"error": f"could not reclassify {candidate_id} (invalid class or not pending)"}), 409
        return jsonify({"ok": True, "action": "reclassified"})

    if row.get("status") != "pending":
        return jsonify({"error": f"{candidate_id} already {row.get('status')}"}), 409
    low_risk = is_low_risk_candidate(candidate_id)
    ok = update_candidate_status(
        candidate_id,
        "approved",
        channel_key=channel_key,
        actor=operator_name,
        source=source,
    )
    if not ok:
        return jsonify({"error": f"could not approve {candidate_id}"}), 409
    if low_risk:
        try:
            merge_ok, msg = quick_merge_candidate(candidate_id, operator_name)
            return jsonify(
                {
                    "ok": True,
                    "action": "approved",
                    "merged": merge_ok,
                    "message": msg[:80] if msg else "",
                }
            )
        except Exception as e:
            return jsonify({"ok": True, "action": "approved", "merged": False, "message": str(e)[:80]})
    return jsonify(
        {
            "ok": True,
            "action": "approved",
            "merged": False,
            "message": "Run process_approved_candidates.py --apply to merge.",
        }
    )


@app.route("/diff-queue")
def diff_queue():
    """Render the Record Diff Queue as HTML — unified diff-card view of pending gate candidates."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    import sys as _sys
    _sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from gate_to_diff_adapter import convert_gate
    from render_record_diff_queue import render_queue

    diffs = convert_gate(USER_ID)
    if not diffs:
        md = "# Record Diff Queue\n\n0 pending change(s)\n"
    else:
        md = render_queue(diffs)

    md_html = _md_to_html(md)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Diff Queue — {html.escape(USER_ID)}</title>
  <style>
    :root {{ --bg: #0f1419; --card: #1a2332; --text: #e8ecf1; --muted: #8b9cb3; --accent: #c17f59; --good: #7dc09a; --danger: #dd8e91; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; padding: 1.25rem; max-width: 52rem; margin: 0 auto; }}
    h1 {{ font-size: 1.35rem; }}
    h3 {{ color: var(--accent); border-bottom: 1px solid rgba(255,255,255,.08); padding-bottom: 0.35rem; margin-top: 1.5rem; }}
    h4 {{ font-size: 0.95rem; color: var(--muted); margin: 0.75rem 0 0.25rem; }}
    hr {{ border: none; border-top: 1px solid rgba(255,255,255,.08); margin: 1.5rem 0; }}
    code {{ background: rgba(255,255,255,.08); padding: 0.15em 0.35em; border-radius: 4px; font-size: 0.9em; }}
    ul {{ padding-left: 1.25rem; }}
    p, li {{ line-height: 1.55; }}
    a {{ color: var(--accent); }}
    .nav {{ margin-bottom: 1rem; font-size: 0.9rem; }}
    .nav a {{ margin-right: 1rem; }}
  </style>
</head>
<body>
  <div class="nav"><a href="/">← Gate review</a></div>
  {md_html}
</body>
</html>"""


@app.route("/api/diff-queue")
def api_diff_queue():
    """JSON list of pending candidates as identity-diff v1 objects."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    import sys as _sys
    _sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from gate_to_diff_adapter import convert_gate

    diffs = convert_gate(USER_ID)
    return jsonify({"user_id": USER_ID, "count": len(diffs), "diffs": diffs})


def _md_to_html(md_text: str) -> str:
    """Minimal Markdown-to-HTML for diff queue rendering (no external deps)."""
    lines = md_text.split("\n")
    out: list[str] = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h4>{html.escape(stripped[5:])}</h4>")
        elif stripped.startswith("# "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("---"):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("<hr/>")
        elif stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            content = stripped[2:]
            content = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", content)
            content = re.sub(r"`([^`]+)`", r"<code>\1</code>", content)
            out.append(f"<li>{content}</li>")
        elif stripped.startswith("**") and stripped.endswith("**"):
            if in_list:
                out.append("</ul>")
                in_list = False
            inner = stripped[2:-2]
            out.append(f"<p><strong>{html.escape(inner)}</strong></p>")
        elif stripped:
            if in_list:
                out.append("</ul>")
                in_list = False
            content = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html.escape(stripped))
            content = re.sub(r"`([^`]+)`", r"<code>\1</code>", content)
            out.append(f"<p>{content}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


@app.route("/api/candidates")
def api_candidates():
    """JSON list of pending candidates for external UIs (raw + normalized review shape)."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401
    from recursion_gate_review import filter_review_candidates, parse_review_candidates

    rows = filter_review_candidates(parse_review_candidates(USER_ID), status="pending")
    normalized = [normalize_review_item(r) for r in rows]
    return jsonify(
        {
            "user_id": USER_ID,
            "count": len(rows),
            "items": rows,
            "items_normalized": normalized,
        }
    )


@app.route("/api/work-politics/review")
def api_work_politics_review():
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    client_id = (request.args.get("client_id") or "").strip() or None
    try:
        items = WP.list_review_queue(status="pending", client_id=client_id)
        return jsonify({"user_id": USER_ID, "count": len(items), "items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/work-politics/client", methods=["POST"])
def api_work_politics_client():
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    try:
        cid = WP.create_or_update_client(
            client_slug=payload["client_slug"],
            display_name=payload["display_name"],
            channel_key=payload["channel_key"],
            principal_type=payload.get("principal_type", "candidate"),
            compliance_status=payload.get("compliance_status", "pending"),
            reviewed_by=os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web"),
            notes=payload.get("notes") or {},
            active=bool(payload.get("active", True)),
        )
        return jsonify({"ok": True, "client_id": cid})
    except KeyError as e:
        return jsonify({"error": f"missing field: {e.args[0]}"}), 400
    except PolicyViolation as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/work-politics/engagement", methods=["POST"])
def api_work_politics_engagement():
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    try:
        engagement_id, decision = WP.submit_engagement(
            client_id=payload["client_id"],
            title=payload["title"],
            work_type=payload["work_type"],
            created_by=os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web"),
            public_attribution=bool(payload.get("public_attribution", False)),
            record_touch=bool(payload.get("record_touch", False)),
            metadata=payload.get("metadata") or {},
        )
        return jsonify(
            {
                "ok": True,
                "engagement_id": engagement_id,
                "requires_review": decision.requires_review,
                "policy_reason": decision.reason,
            }
        )
    except KeyError as e:
        return jsonify({"error": f"missing field: {e.args[0]}"}), 400
    except PolicyViolation as e:
        return jsonify({"error": str(e)}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/work-politics/review-action", methods=["POST"])
def api_work_politics_review_action():
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    review_id = (payload.get("review_id") or "").strip()
    action_type = (payload.get("action") or "").strip().lower()
    operator_name = os.getenv("GRACE_MAR_OPERATOR_NAME", "operator-web").strip() or "operator-web"

    if not review_id.startswith("WPR-"):
        return jsonify({"error": "invalid review_id"}), 400

    try:
        if action_type == "approve":
            WP.approve_review(
                review_id=review_id,
                reviewed_by=operator_name,
                approved_candidate_id=(payload.get("approved_candidate_id") or "").strip() or None,
                review_note=(payload.get("review_note") or "").strip() or None,
            )
            return jsonify({"ok": True, "action": "approved"})

        if action_type == "reject":
            WP.reject_review(
                review_id=review_id,
                reviewed_by=operator_name,
                review_note=(payload.get("review_note") or "").strip(),
            )
            return jsonify({"ok": True, "action": "rejected"})

        return jsonify({"error": "action must be approve or reject"}), 400
    except PolicyViolation as e:
        return jsonify({"error": str(e)}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/work-politics/funnel-event", methods=["POST"])
def api_work_politics_funnel_event():
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    try:
        event_id = WP.log_funnel_event(
            stage=payload["stage"],
            outcome=payload.get("outcome"),
            source=payload.get("source"),
            client_id=payload.get("client_id"),
            engagement_id=payload.get("engagement_id"),
            amount_usd=payload.get("amount_usd"),
            notes=payload.get("notes") or {},
            event_ts=payload.get("event_ts"),
        )
        return jsonify({"ok": True, "event_id": event_id})
    except KeyError as e:
        return jsonify({"error": f"missing field: {e.args[0]}"}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), debug=os.getenv("FLASK_DEBUG", "").lower() in ("1", "true"))
