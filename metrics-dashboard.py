#!/usr/bin/env python3
"""
Interactive metrics dashboard — pipeline health, Record completeness, optional growth/density.

Run from repo root: streamlit run metrics-dashboard.py
Deploy on Render as a web service (streamlit run --server.port 8501 metrics-dashboard.py).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
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

st.caption("Data from users/grace-mar (recursion-gate, self.md, pipeline-events). Regenerate profile for latest.")
