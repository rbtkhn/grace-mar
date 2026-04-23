"""Strategy notebook extension: receipts, graph scaffolds (WORK only; not Record)."""

from .receipts import (
    NotebookReceipt,
    PageOperation,
    append_receipt,
    default_receipt_log_path,
)

__all__ = [
    "NotebookReceipt",
    "PageOperation",
    "append_receipt",
    "default_receipt_log_path",
]
