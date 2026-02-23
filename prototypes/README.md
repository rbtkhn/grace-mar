# Prototype Instantiations

Prototype Portable Record Prompts (PRPs) for specific deployments. Same Record, different display names or variants.

| File | Name | Source | Notes |
|------|------|--------|-------|
| `abby-prp.txt` | Abby | pilot-001 | Grace-Mar Record instantiated as "Abby". Everything else identical. |

**Regenerate:**
```bash
python scripts/export_prp.py -u pilot-001 -n Abby -o prototypes/abby-prp.txt
```
