# Work domain template

- **[DOMAIN.md](DOMAIN.md)** — scaffold for a **`work-<slug>/`** directory with an uppercase **`<SLUG>.md`** wisdom surface (e.g. `politics` → `work-politics/POLITICS.md`).
- **Create an instance:** from repo root, `python3 scripts/create-domain.py <name>`.

Placeholders in the template (`{{DOMAIN}}`, `{{DOMAIN_TITLE}}`, `{{DOMAIN_LOWER}}`) are filled by the script. Do not use a bare substring replace for `DOMAIN` in prose (it would corrupt words like “cross-domain”).
