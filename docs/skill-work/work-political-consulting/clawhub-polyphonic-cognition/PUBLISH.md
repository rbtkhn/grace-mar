# Publish to ClawHub — checklist

Use this when submitting the skill to ClawHub.

## Pre-submit

- [ ] Set `author` in `skill.yaml` to your ClawHub username.
- [ ] Fill `support_url` and `homepage` in `clawhub.json` if you have a repo or issues URL.
- [ ] Optional: add 1–2 screenshots (1920×1080 or 1280×720 PNG) showing example A/B/C output. For instructions-only skills, a single example run is enough.
- [ ] Optional: 30–90s demo video (real usage); add URL to listing if you have one.

## Permission justification (for review)

This skill requests **no permissions** (`permissions: []`). It is natural-language instructions only. No code runs; no network, filesystem, browser, or shell access. See README.md and SECURITY.md.

## Package and submit

```bash
cd docs/skill-work/work-political-consulting
tar -czf clawhub-polyphonic-cognition.tar.gz clawhub-polyphonic-cognition/
```

Upload `clawhub-polyphonic-cognition.tar.gz` at ClawHub → Publish New Skill. Metadata is in `clawhub.json`; tagline is ≤80 chars.

## After publish

- Bump `version` in both `skill.yaml` and `clawhub.json` for updates.
- Add CHANGELOG.md entries for non-trivial changes.
