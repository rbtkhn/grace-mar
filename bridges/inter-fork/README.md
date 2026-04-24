# Inter-fork package examples

These examples show the shape of bounded inter-fork collaboration packages.

## Status

Example-only, non-authoritative, recipient-gated.

## What these examples demonstrate

- `evidence-share.example.json` — lighter package routed into the recipient recursion gate
- `change-proposal-review.example.json` — material package routed into the recipient change-review queue

## Boundary reminder

The sender does **not** write directly into the recipient fork's canonical surfaces.
The recipient must explicitly import the package with `scripts/import_inter_fork_package.py`.
