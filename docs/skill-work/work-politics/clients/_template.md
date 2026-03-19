# Client template — WAP

Copy to `clients/<jurisdiction>-<slug>.md`. One active client per file.

---

## Identity

| Field | Value |
|-------|--------|
| **Client / principal** | |
| **Office sought** | (e.g. US House KY-4, State Senate CA-12, Mayor — City) |
| **Jurisdiction** | `US-federal` \| `US-state-<ST>` \| `US-local-<ST>-<locality>` \| `intl-<CC>` |
| **Election date / cycle** | |
| **channel_key (RECURSION-GATE)** | `operator:wap:<jurisdiction>-<slug>` — e.g. `operator:wap:us-ky4-massie` |
| **territory** | Always `work-politics` |

---

## Compliance

| Field | Value |
|-------|--------|
| **Compliance checklist** | [compliance-checklist.md](../compliance-checklist.md) — completed Y/N |
| **Signed date** | |
| **Notes** | (FEC/state/local/FARA/intl — short) |

---

## Working docs

| Artifact | Path (relative to work-politics) |
|----------|-------------------------------------------|
| Principal profile | `principal-profile.md` or client-specific copy |
| Calendar | `calendar-YYYY.md` or client calendar |
| Opposition | `opposition-brief.md` or client brief |
| Revenue | Rows in `revenue-log.md` tagged to client |

---

## Status

| Field | Value |
|-------|--------|
| **Phase** | diagnostic \| active \| paused \| closed |
| **Last touch** | YYYY-MM-DD |
