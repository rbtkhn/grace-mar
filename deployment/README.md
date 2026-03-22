# Deployment artifacts

- **Root [Dockerfile](../Dockerfile)** and **[docker-compose.yml](../docker-compose.yml)** — primary local and container paths. `WORKDIR /app`; app entry: `python apps/miniapp_server.py`.
- **[render.yaml](../render.yaml)** and **[procfile](../procfile)** — Render/Heroku-style starts; keep in sync with `apps/` entrypoints.
- **GitHub Actions** live only under **[.github/workflows/](../.github/workflows/)** (GitHub requires this path; do not move workflows here).
- **Generated HTML & tags:** [docs/deployment/ci-generated-artifacts.md](../docs/deployment/ci-generated-artifacts.md) — profile workflow, miniapp notes, optional version tags.
