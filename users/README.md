# Students Directory

Each subdirectory contains one user's cognitive twin data.

## Structure

```
users/
├── pilot-001/           # First pilot user
│   ├── SELF.md          # Personality profile
│   ├── SKILLS.md        # Capability containers (READ/WRITE/IMAGINE)
│   ├── EVIDENCE.md      # Reading List, Writing Log, Creation Log
│   └── SESSION-LOG.md   # Interaction history
└── (future users...)
```

## Storage

GitHub repository is the authoritative record store.

- **Audit trail:** Git commit history
- **Versioning:** Every update is a commit
- **Snapshots:** Git tags (e.g., `pilot-001-age-6`)
- **Backup:** GitHub remote

## Privacy Note

Student data is sensitive. This repository should remain private.
Future: encryption, access controls, data portability standards.

---

*Last updated: February 2026*
