# Agent Surfaces Artifacts

This directory contains generated, derived views of the Agent Sprawl Control Plane registry.

The authoritative source is:
config/agent-surfaces.v1.json

Generated files here:
- are not canonical Record
- are not approval
- are not merge authority
- may be regenerated
- are for operator inspection only

To regenerate:
python3 scripts/work_dev/render_agent_surfaces_table.py

To check freshness:
python3 scripts/work_dev/render_agent_surfaces_table.py --check
