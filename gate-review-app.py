#!/usr/bin/env python3
"""
Web-based gate review dashboard — approve/reject pending RECURSION-GATE candidates.

Serves a live view of pending candidates with Approve/Reject buttons. Actions update
recursion-gate.md and optionally run quick-merge (process_approved_candidates). Gate
remains canonical; this app does not edit SELF or EVIDENCE directly.

Run from repo root (so bot.core and scripts resolve paths correctly):
    OPERATOR_SECRET=your_secret python gate-review-app.py
    # Or: FLASK_APP=gate-review-app.py flask run --port 5001

Deploy alongside miniapp_server on Render; protect with OPERATOR_SECRET (Bearer token).
"""

import html
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from flask import Flask, jsonify, request

app = Flask(__name__)
USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
OPERATOR_SECRET = os.getenv("OPERATOR_SECRET", "").strip() or os.getenv("OPERATOR_FETCH_SECRET", "").strip()

from repo_io import assert_canonical_record_layout  # noqa: E402

assert_canonical_record_layout(USER_ID, context="gate-review-app")


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
    from recursion_gate_territory import TERRITORY_WAP

    rows = parse_review_candidates(USER_ID)
    pending = filter_review_candidates(rows, status="pending")
    n = len(pending)
    wap_n = sum(1 for r in pending if r.get("territory") == TERRITORY_WAP)
    comp_n = n - wap_n

    cards = []
    for r in pending:
        dup = r.get("duplicate_hints") or []
        hint = f'<p class="hint">{html.escape(dup[0])}</p>' if dup else ""
        cid = html.escape(r["id"])
        summary = html.escape(r.get("summary") or "(no summary)")
        territory = html.escape(r.get("territory", ""))
        risk = html.escape(r.get("risk_tier", ""))
        label = html.escape(r.get("territory_label", ""))
        pill_slug = "wap" if r.get("territory") == TERRITORY_WAP else "companion"
        age = _age_label(r.get("age_days"))
        channel = html.escape(r.get("channel_key") or "—")
        ts = html.escape(r.get("timestamp") or "—")
        quick = "true" if r.get("ready_for_quick_merge") else "false"
        cards.append(
            f'<article class="card" data-territory="{territory}" data-risk="{risk}">'
            f'<header><span class="id">{cid}</span>'
            f'<span class="pill pill-{pill_slug}">{label}</span>'
            f'<span class="pill pill-risk">{risk}</span>'
            f'<span class="age">{age}</span></header>'
            f'<p class="summary">{summary}</p>{hint}'
            f'<footer><span class="meta">{channel}</span><span class="meta">{ts}</span></footer>'
            f'<div class="actions">'
            f'<button type="button" class="btn approve" data-id="{cid}" data-quick="{quick}">Approve</button>'
            f'<button type="button" class="btn reject" data-id="{cid}">Reject</button>'
            f'</div></article>'
        )
    rows_html = "\n".join(cards) if cards else '<p class="empty">No pending candidates.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Gate review — {html.escape(USER_ID)}</title>
  <style>
    :root {{ --bg: #0f1419; --card: #1a2332; --text: #e8ecf1; --muted: #8b9cb3; --accent: #c17f59; --good: #7dc09a; --danger: #dd8e91; --wap: #c4a574; --companion: #7eb8da; }}
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
    .age {{ margin-left: auto; color: var(--muted); font-size: 0.8rem; }}
    .summary {{ margin: 0; }}
    .hint {{ margin: 0.6rem 0 0; color: var(--muted); font-size: 0.82rem; }}
    .card footer {{ margin-top: 0.75rem; padding-top: 0.65rem; border-top: 1px solid rgba(255,255,255,.06); font-size: 0.75rem; color: var(--muted); }}
    .actions {{ margin-top: 0.75rem; display: flex; gap: 0.5rem; }}
    .btn {{ padding: 0.4rem 0.8rem; border-radius: 8px; border: none; cursor: pointer; font-size: 0.9rem; }}
    .btn.approve {{ background: rgba(125,192,154,0.2); color: var(--good); }}
    .btn.reject {{ background: rgba(221,142,145,0.2); color: var(--danger); }}
    .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
    .empty {{ color: var(--muted); }}
  </style>
</head>
<body>
  <h1>Gate review</h1>
  <p class="sub">Approve or reject pending candidates. Merge runs via process_approved_candidates.</p>
  <div class="stats">
    <span class="stat"><strong>{n}</strong> pending</span>
    <span class="stat">Work-politics <strong>{wap_n}</strong></span>
    <span class="stat">Companion <strong>{comp_n}</strong></span>
  </div>
  <div class="grid" id="grid">{rows_html}</div>
  <script>
    var secret = document.location.search.match(/token=([^&]+)/) ? decodeURIComponent(document.location.search.match(/token=([^&]+)/)[1]) : '';
    function doAction(cid, action, btn) {{
      btn.disabled = true;
      fetch('/action', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ candidate_id: cid, action: action }})
      }}).then(function(r) { return r.json(); }).then(function(data) {{
        if (data.error) {{ alert(data.error); btn.disabled = false; return; }}
        var card = btn.closest('.card');
        if (card) card.remove();
      }}).catch(function() {{ btn.disabled = false; }});
    }}
    document.querySelectorAll('.btn.approve').forEach(function(btn) {{
      btn.onclick = function() { doAction(btn.getAttribute('data-id'), 'approve', btn); }};
    }});
    document.querySelectorAll('.btn.reject').forEach(function(btn) {{
      btn.onclick = function() { doAction(btn.getAttribute('data-id'), 'reject', btn); }};
    }});
  </script>
</body>
</html>"""


@app.route("/action", methods=["POST"])
def action():
    """Apply approve or reject; update recursion-gate and optionally quick-merge."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401
    from bot.core import is_low_risk_candidate, quick_merge_candidate, update_candidate_status

    payload = request.get_json(silent=True) or {}
    candidate_id = (payload.get("candidate_id") or "").strip()
    action_type = (payload.get("action") or "").strip().lower()
    if action_type not in ("approve", "reject"):
        return jsonify({"error": "action must be approve or reject"}), 400
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
            candidate_id, "rejected",
            rejection_reason=reason, channel_key=channel_key, actor=operator_name, source=source,
        )
        if not ok:
            return jsonify({"error": f"could not reject {candidate_id}"}), 409
        return jsonify({"ok": True, "action": "rejected"})

    if row.get("status") != "pending":
        return jsonify({"error": f"{candidate_id} already {row.get('status')}"}), 409
    ok = update_candidate_status(
        candidate_id, "approved",
        channel_key=channel_key, actor=operator_name, source=source,
    )
    if not ok:
        return jsonify({"error": f"could not approve {candidate_id}"}), 409
    if is_low_risk_candidate(candidate_id):
        try:
            merge_ok, msg = quick_merge_candidate(candidate_id, operator_name)
            return jsonify({"ok": True, "action": "approved", "merged": merge_ok, "message": msg[:80] if msg else ""})
        except Exception as e:
            return jsonify({"ok": True, "action": "approved", "merged": False, "message": str(e)[:80]})
    return jsonify({"ok": True, "action": "approved", "merged": False, "message": "Run process_approved_candidates.py --apply to merge."})


@app.route("/api/candidates")
def api_candidates():
    """JSON list of pending candidates for external UIs."""
    if not _auth():
        return jsonify({"error": "Unauthorized"}), 401
    from recursion_gate_review import filter_review_candidates, parse_review_candidates
    rows = filter_review_candidates(parse_review_candidates(USER_ID), status="pending")
    return jsonify({"user_id": USER_ID, "count": len(rows), "items": rows})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), debug=os.getenv("FLASK_DEBUG", "").lower() in ("1", "true"))
