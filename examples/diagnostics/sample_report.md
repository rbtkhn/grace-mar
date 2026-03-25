<!-- Example output shape; regenerate via run_diagnostics + render_diagnostics_report -->

# Diagnostics report — grace-mar

Run:

```bash
python scripts/work_dev/run_diagnostics.py --config examples/diagnostics/sample_input.yaml --json-out /tmp/d.json
python scripts/work_dev/render_diagnostics_report.py --input /tmp/d.json -o examples/diagnostics/sample_report.generated.md
```
