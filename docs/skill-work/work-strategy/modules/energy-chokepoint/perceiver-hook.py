# Prototype — will move to scripts/ after gating. WORK-only; no Record writes.
from datetime import datetime


def ingest_chokepoint_data(event_summary: str) -> dict:
    """
    Placeholder for real OpenClaw / maritime API call.
    In production: replace with actual data source.
    Output is for WORK docs (briefs, session notes); do not write to self-evidence.md.
    """
    data = {
        "hormuz_tankers_24h": 42,  # example
        "price_spike_pct": 8.7,
        "sanction_signal": "Treasury considering lift on Iranian oil",
        "timestamp": datetime.utcnow().isoformat(),
    }
    # Emit to WORK output / session log only (use emit_pipeline_event for applied merges, not routine runs)
    print(f"EMIT: energy-chokepoint-ingested {data}")  # replace with real WORK-side emit
    return data
