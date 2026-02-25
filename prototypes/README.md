# Prototype Instantiations

Prototype Portable Record Prompts (PRPs) for specific deployments. Same Record, different display names or variants.

| File | Name | Source | Notes |
|------|------|--------|-------|
| `abby-llm.txt` | Abby | grace-mar | Grace-Mar Record instantiated as "Abby". Everything else identical. |

**Regenerate:**
```bash
python scripts/export_prp.py -u grace-mar -n Abby -o prototypes/abby-llm.txt
```
