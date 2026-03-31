#!/usr/bin/env python3
"""
Interactive metrics dashboard — pipeline health, Record completeness, optional growth/density.

Run from repo root: streamlit run apps/metrics-dashboard.py
Deploy on Render as a web service (streamlit run --server.port 8501 apps/metrics-dashboard.py).
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import streamlit as st
try:
    from scripts.metrics import (
        compute_pipeline_health,
        compute_record_completeness,
        compute_intent_drift,
    )
except ImportError:
    import metrics as _m
    compute_pipeline_health = _m.compute_pipeline_health
    compute_record_completeness = _m.compute_record_completeness
    compute_intent_drift = _m.compute_intent_drift

st.set_page_config(page_title="Grace-Mar metrics", layout="wide")
st.title("Grace-Mar metrics")

col1, col2, col3 = st.columns(3)
with col1:
    health = compute_pipeline_health()
    st.metric("Pending candidates", health.pending_count)
    st.metric("Stale (7d+)", health.stale_candidates)
with col2:
    st.metric("Applied total", health.applied_total)
    st.metric("Rejected total", health.rejected_total)
    if health.approval_rate is not None:
        st.metric("Approval rate", f"{100 * health.approval_rate:.0f}%")
with col3:
    st.metric("Days since last activity", f"{health.days_since_last_activity:.1f}" if health.days_since_last_activity is not None else "—")
    if health.last_applied_ts:
        st.caption(f"Last applied: {health.last_applied_ts[:19]}")

rec = compute_record_completeness()
st.subheader("Record completeness (IX)")
try:
    import plotly.graph_objects as go
    fig = go.Figure(data=[
        go.Bar(name="Knowledge (IX-A)", x=["IX-A"], y=[rec.ix_a]),
        go.Bar(name="Curiosity (IX-B)", x=["IX-B"], y=[rec.ix_b]),
        go.Bar(name="Personality (IX-C)", x=["IX-C"], y=[rec.ix_c]),
    ])
    fig.update_layout(barmode="group", title="IX dimension counts", height=300)
    st.plotly_chart(fig, use_container_width=True)
except ImportError:
    st.write(f"**IX-A:** {rec.ix_a} · **IX-B:** {rec.ix_b} · **IX-C:** {rec.ix_c} · **Total:** {rec.total_ix}")

drift = compute_intent_drift(window_days=30)
if drift.total_conflicts > 0:
    st.subheader("Intent drift (last 30d)")
    st.write(f"Conflicts: {drift.total_conflicts}")
    if drift.rejection_categories:
        st.json(drift.rejection_categories)

try:
    from work_politics_engine import WorkPoliticsEngine

    wp = WorkPoliticsEngine(user_id=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    wp.init_db()

    st.subheader("Work-politics")
    metrics_wp = wp.funnel_metrics(days=30)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("30d work-politics revenue", f"${metrics_wp['total_revenue_usd']:.2f}")
    with col_b:
        pending_wp = len(wp.list_review_queue(status="pending"))
        st.metric("Pending work-politics review items", pending_wp)

    stage_rows = []
    for stage, data in metrics_wp["stages"].items():
        stage_rows.append(
            {
                "stage": stage,
                "total": data["total"],
                "revenue_usd": round(data["revenue"], 2),
                "outcomes": data["outcomes"],
            }
        )

    if stage_rows:
        st.write(stage_rows)
    else:
        st.caption("No work-politics funnel data yet.")
except ImportError:
    st.caption("work_politics_engine not available.")
except Exception as e:
    st.warning(f"Work-politics metrics: {e}")

st.subheader("Replay and provenance")
st.caption(
    "Synthesis from audit JSONL (profile root, runtime-bundle fallback). "
    "Weights are heuristic — not per-message model attribution. See docs/harness-replay-spec.md."
)
try:
    from repo_io import profile_dir

    _uid = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
    _prof = profile_dir(_uid)
    from grace_mar.replay.synthesis import build_replay_events, replay_provenance_summary

    summary = replay_provenance_summary(_prof, REPO_ROOT)
    prov = summary["provenance"]
    counts = prov.get("class_counts") or {}
    st.metric("Pipeline rows (loaded)", summary["total_pipeline_rows"])
    st.metric("Synthesized replay events (tail)", summary["total_replay_synthesized"])
    st.metric("Harness rows (loaded)", summary["total_harness_rows"])
    st.metric("Unresolved heuristic (recent window)", summary["unresolved_provenance_recent_window"])
    st.write("**Answer source mix (heuristic, recent window):**")
    st.json(
        {
            "dominant_class": prov.get("answer_class"),
            "record_weight_estimated": prov.get("record_weight_estimated"),
            "runtime_weight_estimated": prov.get("runtime_weight_estimated"),
            "policy_weight_estimated": prov.get("policy_weight_estimated"),
            "audit_weight_estimated": prov.get("audit_weight_estimated"),
            "class_counts": counts,
        }
    )
    st.write("**Top pipeline event types (last 500 lines):**")
    st.json(dict(summary["top_event_categories"]))
    replay_tail = build_replay_events(_prof, REPO_ROOT, limit=20)
    st.write("**Latest replay events (tail of pipeline, max 20 shown):**")
    st.dataframe(replay_tail, use_container_width=True)
    st.write("**Full provenance aggregate (same as mix above):**")
    st.json(prov)
except Exception as e:
    st.warning(f"Replay / provenance: {e}")

st.caption("Data from users/grace-mar (recursion-gate, self.md, pipeline-events). Regenerate profile for latest.")
