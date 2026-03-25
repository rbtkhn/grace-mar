# work-build-ai integration status

**Canonical source:** the work-dev control plane and generated snapshot.

- **Edit:** [docs/skill-work/work-dev/control-plane/integration_status.yaml](../work-dev/control-plane/integration_status.yaml)
- **Generated table:** [docs/skill-work/work-dev/generated/integration-status.generated.md](../work-dev/generated/integration-status.generated.md)
- **Narrative / reading rule:** [docs/skill-work/work-dev/integration-status.md](../work-dev/integration-status.md)

Do not duplicate the status table here; it drifts. Run:

```bash
python scripts/work_dev/render_control_plane_docs.py
python scripts/work_dev/validate_control_plane.py
```
