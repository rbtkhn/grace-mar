# CI, generated HTML, and releases

## Profile site (`profile/`)

- **Workflow:** [.github/workflows/deploy-profile.yml](../../.github/workflows/deploy-profile.yml) runs `python scripts/generate_profile.py` on pushes that touch `users/grace-mar/**`, `scripts/generate_profile.py`, or `profile/CNAME`.
- **Committed HTML:** The repo may still contain pre-generated `profile/**/index.html` for deploy simplicity; the workflow refreshes them before Pages upload.
- **Operator:** After local Record edits, run `python scripts/generate_profile.py` if you need matching HTML before push.

## Mini App (`miniapp/`)

- There is **no** dedicated CI job that regenerates `miniapp/index.html` today. Treat it as **source-controlled** unless a generator script is added later.
- Deploy surfaces: [deployment/README.md](../../deployment/README.md) (`apps/miniapp_server.py`, Docker, Render).

## Release tags (optional discipline)

- After significant merges, consider a tag such as `v2026.03.21` or semantic `v0.x.y` for deploy and audit trails.
- Tags are **manual** unless you add a release workflow; keep workflow files under `.github/workflows/` at the repo root (GitHub requirement).

## Editable Python package

- CI may run `pip install -e .` to verify [pyproject.toml](../../pyproject.toml) and the `grace-mar` CLI; see [.github/workflows/test.yml](../../.github/workflows/test.yml).
