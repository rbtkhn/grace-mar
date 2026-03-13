#!/usr/bin/env python3
"""
Generate a read-only HTML dashboard of pending RECURSION-GATE candidates.

One book (recursion-gate.md), human door (this page). Run after gate changes:

    python scripts/generate_gate_dashboard.py -u grace-mar
    open users/grace-mar/gate-dashboard.html
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from recursion_gate_territory import TERRITORY_WAP, iter_pending_blocks, territory_from_yaml_block

DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"


def _parse_ts(body: str) -> str | None:
    m = re.search(r"^timestamp:\s*(.+)$", body, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip("\"'")[:32]


def _days_since(ts: str | None) -> str:
    if not ts:
        return "—"
    try:
        # "2026-02-24" or "2026-02-24 14:07:50"
        part = ts[:10]
        then = datetime.strptime(part, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        d = (now - then).days
        return f"{d}d" if d >= 0 else "—"
    except Exception:
        return "—"


def _pending_rows(full_md: str) -> list[dict]:
    rows = []
    for cid, body in iter_pending_blocks(full_md):
        terr = territory_from_yaml_block(body)
        sm = re.search(r"^summary:\s*(.+)$", body, re.MULTILINE)
        summary = (sm.group(1).strip().strip("\"'") if sm else "")[:300]
        ck_m = re.search(r"^channel_key:\s*(.+)$", body, re.MULTILINE)
        channel_key = ck_m.group(1).strip().strip("\"'") if ck_m else ""
        ts = _parse_ts(body)
        rows.append(
            {
                "id": cid,
                "summary": summary,
                "territory": terr,
                "territory_label": "WAP" if terr == TERRITORY_WAP else "Companion",
                "channel_key": channel_key,
                "timestamp": ts or "",
                "age": _days_since(ts),
            }
        )
    return rows


def build_html(user_id: str, rows: list[dict], gate_rel: str) -> str:
    gen = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n = len(rows)
    wap_n = sum(1 for r in rows if r["territory"] == TERRITORY_WAP)
    comp_n = n - wap_n

    cards = []
    for r in rows:
        cards.append(
            f"""
    <article class="card" data-territory="{html.escape(r['territory'])}">
      <header>
        <span class="id">{html.escape(r['id'])}</span>
        <span class="pill pill-{r['territory_label'].lower()}">{html.escape(r['territory_label'])}</span>
        <span class="age" title="since timestamp">{html.escape(r['age'])}</span>
      </header>
      <p class="summary">{html.escape(r['summary'] or '(no summary)')}</p>
      <footer>
        <span class="meta">{html.escape(r['channel_key'] or '—')}</span>
        <span class="meta">{html.escape(r['timestamp'] or '—')}</span>
      </footer>
    </article>"""
        )

    rows_html = "\n".join(cards) if cards else '<p class="empty">No pending candidates. Edit <code>recursion-gate.md</code> to approve/reject, then merge.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>RECURSION-GATE pending — {html.escape(user_id)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..72,600;1,9..72,600&display=swap" rel="stylesheet"/>
  <style>
    :root {{
      --bg: #0f1419;
      --card: #1a2332;
      --text: #e8ecf1;
      --muted: #8b9cb3;
      --wap: #c4a574;
      --companion: #7eb8da;
      --accent: #c17f59;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: "DM Sans", system-ui, sans-serif;
      font-size: 15px;
      line-height: 1.45;
      padding: 1.25rem clamp(1rem, 4vw, 2rem) 3rem;
    }}
    h1 {{
      font-family: Fraunces, Georgia, serif;
      font-weight: 600;
      font-size: clamp(1.35rem, 3vw, 1.75rem);
      margin: 0 0 0.25rem;
      letter-spacing: -0.02em;
    }}
    .sub {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 1.25rem;
    }}
    .sub code {{ color: var(--companion); font-size: 0.85em; }}
    .stats {{
      display: flex; flex-wrap: wrap; gap: 0.75rem;
      margin-bottom: 1rem;
    }}
    .stat {{
      background: var(--card);
      padding: 0.5rem 0.9rem;
      border-radius: 8px;
      font-size: 0.9rem;
    }}
    .stat strong {{ color: var(--accent); }}
    .filters {{
      display: flex; gap: 0.5rem; margin-bottom: 1.25rem; flex-wrap: wrap;
    }}
    .filters button {{
      font: inherit;
      padding: 0.4rem 0.85rem;
      border-radius: 999px;
      border: 1px solid var(--muted);
      background: transparent;
      color: var(--text);
      cursor: pointer;
    }}
    .filters button.active {{ background: var(--card); border-color: var(--accent); color: var(--accent); }}
    .grid {{
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
    }}
    .card {{
      background: var(--card);
      border-radius: 12px;
      padding: 1rem 1.1rem;
      border: 1px solid rgba(255,255,255,.06);
    }}
    .card header {{
      display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
      margin-bottom: 0.6rem;
    }}
    .id {{ font-weight: 600; font-family: ui-monospace, monospace; font-size: 0.9rem; color: var(--accent); }}
    .pill {{
      font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em;
      padding: 0.2rem 0.5rem; border-radius: 4px;
    }}
    .pill-wap {{ background: rgba(196,165,116,.2); color: var(--wap); }}
    .pill-companion {{ background: rgba(126,184,218,.15); color: var(--companion); }}
    .age {{ margin-left: auto; color: var(--muted); font-size: 0.8rem; }}
    .summary {{ margin: 0; color: var(--text); }}
    .card footer {{
      margin-top: 0.75rem; padding-top: 0.65rem;
      border-top: 1px solid rgba(255,255,255,.06);
      display: flex; flex-direction: column; gap: 0.2rem;
    }}
    .meta {{ font-size: 0.75rem; color: var(--muted); word-break: break-all; }}
    .empty {{ color: var(--muted); }}
    .foot {{
      margin-top: 2rem; padding-top: 1rem;
      border-top: 1px solid rgba(255,255,255,.08);
      font-size: 0.8rem; color: var(--muted);
    }}
    .card.hidden {{ display: none; }}
  </style>
</head>
<body>
  <h1>Pending candidates</h1>
  <p class="sub">Read-only view of <code>{html.escape(gate_rel)}</code> · edit status in the markdown file, then merge. Generated {html.escape(gen)}</p>
  <div class="stats">
    <span class="stat"><strong>{n}</strong> pending</span>
    <span class="stat">WAP <strong>{wap_n}</strong></span>
    <span class="stat">Companion <strong>{comp_n}</strong></span>
  </div>
  <div class="filters" role="tablist">
    <button type="button" class="active" data-filter="all">All</button>
    <button type="button" data-filter="{html.escape(TERRITORY_WAP)}">WAP</button>
    <button type="button" data-filter="companion">Companion</button>
  </div>
  <div class="grid" id="grid">
{rows_html}
  </div>
  <p class="foot">Grace-Mar harness — human door only. Voice stages here; companion approves. Regenerate: <code>python scripts/generate_gate_dashboard.py -u {html.escape(user_id)}</code></p>
  <script>
    document.querySelectorAll('.filters button').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        document.querySelectorAll('.filters button').forEach(function(b) {{ b.classList.remove('active'); }});
        btn.classList.add('active');
        var f = btn.getAttribute('data-filter');
        document.querySelectorAll('.card').forEach(function(card) {{
          var t = card.getAttribute('data-territory');
          var show = f === 'all' || (f === 'companion' && t !== '{TERRITORY_WAP}') || t === f;
          card.classList.toggle('hidden', !show);
        }});
      }});
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate gate-dashboard.html from recursion-gate.md")
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument("-o", "--output", default=None, help="Output path (default users/<id>/gate-dashboard.html)")
    args = ap.parse_args()
    user_dir = REPO_ROOT / "users" / args.user
    gate = user_dir / "recursion-gate.md"
    if not gate.exists():
        print(f"Missing {gate}", file=sys.stderr)
        return 1
    md = gate.read_text(encoding="utf-8")
    rows = _pending_rows(md)
    out = Path(args.output) if args.output else user_dir / "gate-dashboard.html"
    gate_rel = f"users/{args.user}/recursion-gate.md"
    out.write_text(build_html(args.user, rows, gate_rel), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
