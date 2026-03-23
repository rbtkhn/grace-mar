"""Base class for series-specific lecture analysis extractors."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class LectureExtractor(ABC):
    """Domain plugin: prompts, optional postprocess, series id.

    Core dispatch (`run_comparative_sweep`, ingest tools) resolves an extractor by
    `series_id` or `source_id` prefix so new playlists do not edit monolithic scripts.
    """

    series_id: str = "generic"

    @abstractmethod
    def prompt_system_path(self) -> Path:
        """Path to system prompt markdown."""

    @abstractmethod
    def schema_version(self) -> str:
        """Expected analysis JSON schema_version string."""

    def json_schema_variant(self) -> str | None:
        """If set, names a domain-specific schema doc or prompt variant (optional)."""
        return None

    def staging_namespace(self) -> str:
        """Prefix for staging JSONL rows / filenames (e.g. prediction-tracking/staging)."""
        return self.series_id.replace("-", "_")

    def map_prediction_to_staging(self, row: dict[str, Any]) -> dict[str, Any]:
        """Hook before writing draft registry rows from analysis JSON predictions[]."""
        return dict(row)

    def map_divergence_to_staging(self, row: dict[str, Any]) -> dict[str, Any]:
        """Hook before writing draft rows from divergences_from_prior[]."""
        return dict(row)

    def postprocess(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Optional hook to normalize or enrich validated JSON."""
        return analysis
