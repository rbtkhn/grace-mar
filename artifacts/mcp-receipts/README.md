# MCP execution receipts (derived)

JSON files in this directory are **runtime / WORK audit artifacts** emitted by [`scripts/mcp_receipt.py`](../../scripts/mcp_receipt.py). They are **not** canonical Record truth.

- Receipts may later **support** evidence stubs or gate candidates; they do **not** substitute companion approval.
- **Receipt ≠ approval.** Tool success and documented posture are not merge authority.
- Validate entries with [`scripts/mcp_receipt_audit.py`](../../scripts/mcp_receipt_audit.py) (writes [`artifacts/mcp-receipt-report.md`](../mcp-receipt-report.md)).
- Schema: [`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json). **Not** the same contract as [`schema-registry/execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json) (runtime worker receipts).

See **[`docs/mcp/mcp-execution-receipts.md`](../../docs/mcp/mcp-execution-receipts.md)**.
